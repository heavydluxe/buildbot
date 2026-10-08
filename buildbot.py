import os
import sys
import json
import time
import subprocess

# ---------------------------------------------------------------------------
# Helpers!
# ---------------------------------------------------------------------------

def run(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[!] Command failed (exit {result.returncode}): {cmd}")
    return result.returncode == 0

def pause(seconds=1):
    time.sleep(seconds)

def header(text):
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}")

def scrub_handy_keys(path):
    # This repo is public, so blank any AI API keys Handy has saved before
    # the backup gets committed. You'd re-enter them on a new Mac.
    if not os.path.exists(path):
        return
    with open(path) as f:
        data = json.load(f)
    keys = data.get("settings", {}).get("post_process_api_keys", {})
    for name in keys:
        keys[name] = ""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ---------------------------------------------------------------------------
# Config: edit these lists to control what gets installed / backed up
# ---------------------------------------------------------------------------

BREW_CLIS = [
    # Critical infrastructure. Do not remove.
    'install-nothing',

    # Quality of life
    'bat', 'btop', 'coreutils', 'figlet', 'gh', 'git', 'oh-my-posh', 'ripgrep',
    'speedtest-cli', 'sqlite', 'tree',
    
    # Containers
    'colima', 'docker', 'dockutil',

    # AI-related
    'ollama', 'pi-coding-agent',

    # Coding
    'powershell', 'python3',
]

BREW_CASKS = [
    '1password', 'claude', 'claude-code', 'emacs-app', 'espanso', 'firefox',
    'font-jetbrains-mono-nerd-font', 'ghostty', 'handy', 'obs', 'splashtop-business',
    'spotify', 'visual-studio-code', 'windows-app',
]

# Each entry: (live path on machine, path inside this repo)
CONFIGS = [
    ("~/.zshrc",                                                       "./configs/backup.zshrc"),
    ("~/.mytheme.omp.json",                                            "./configs/mytheme.omp.json"),
    ("$HOME/Library/Application Support/com.mitchellh.ghostty/config", "./configs/ghostty.config"),
    ("$HOME/.claude-dart/settings.json",                               "./configs/claude-dart.settings.json"),
    ("$HOME/Library/Application Support/espanso/config/default.yml",   "./configs/espanso.default.yml"),
    ("$HOME/Library/Application Support/espanso/match/base.yml",       "./configs/espanso.base.yml"),
    ("$HOME/Library/Application Support/com.pais.handy/settings_store.json", "./configs/handy.settings.json"),
]

# Handy's backup gets its API keys blanked before commit (see scrub_handy_keys).
HANDY_BACKUP = "./configs/handy.settings.json"

# Emacs is a directory — backed up as a zip of ~/.emacs.d.
# EMACS_HOME_REL is the path RELATIVE to $HOME. Zipping it from within $HOME
# stores entries as ".emacs.d/..." (not "/Users/<you>/.emacs.d/..."), which is
# what lets restore unpack cleanly back into ~/ on any machine.
EMACS_HOME_REL = ".emacs.d"
EMACS_ZIP      = "./configs/emacs.backup.zip"

# Dock layout, restored via dockutil. Apps are pinned left-to-right in this order.
DOCK_APPS = [
    '/Applications/Emacs.app',
    '/Applications/Firefox.app',
    '/Applications/Google Chrome.app',
    '/Applications/Claude.app',
    '/Applications/zoom.us.app',
    '/Applications/Visual Studio Code.app',
    '/Applications/Windows App.app',
    '/Applications/GlobalProtect.app',
    '/Applications/1Password.app',
    '/Applications/Splashtop Business.app',
    '/System/Applications/System Settings.app',
    '/Applications/Spotify.app',
]

# Folders pinned to the Dock's right side: (path, extra dockutil options).
DOCK_FOLDERS = [
    ("~/Downloads", "--view fan --display folder"),
]

# ---------------------------------------------------------------------------
# Restore functions
# ---------------------------------------------------------------------------

def bootstrap_brew():
    header("Checking for Homebrew")
    if run("command -v brew > /dev/null 2>&1"):
        print("Homebrew already installed.")
    else:
        print("Homebrew not found — installing now.")
        print("You may be prompted for your sudo password.")
        run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')

    # Apple Silicon installs brew to /opt/homebrew — inject it into this process's PATH
    # so all subsequent subprocess calls can find it without a shell reload.
    brew_bin = '/opt/homebrew/bin'
    if brew_bin not in os.environ.get('PATH', ''):
        os.environ['PATH'] = brew_bin + ':' + os.environ.get('PATH', '')
        print(f"Added {brew_bin} to PATH.")
    pause()

def restore_brews():
    header("Restoring Homebrew Packages")

    print("Installing CLI tools...")
    run("brew install " + " ".join(BREW_CLIS))

    print("Installing Casks...")
    run("brew install --cask " + " ".join(BREW_CASKS))

def sys_prep():
    header("System Preparation")

    hostname = input("Enter new hostname for this device: ").strip().lower()
    print("You will need your sudo password for the hostname change.")
    run(f'sudo scutil --set HostName "{hostname}"')
    run(f'sudo scutil --set ComputerName "{hostname}"')
    run(f'sudo scutil --set LocalHostName "{hostname}"')
    print(f"Hostname set to: {hostname}")
    pause()

    print("Configuring git globals...")
    run('git config --global user.name "Brian Dellinger"')
    run('git config --global user.email "bdellinger@gmail.com"')
    run('git config --global init.defaultBranch main')
    run('git config --global alias.graph "log --graph"')
    pause()

    # Oh My Zsh bundles zsh-autosuggestions and zsh-syntax-highlighting
    # (since Sep 2026), so they no longer need cloning separately.
    print("Installing Oh My Zsh...")
    run('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended')
    run('mkdir -p ~/.cache')
    pause()

def restore_settings():
    header("Restoring Config Files")

    for live_path, repo_path in CONFIGS:
        expanded_live = os.path.expandvars(os.path.expanduser(live_path))
        print(f"  Restoring {repo_path} -> {expanded_live}")
        os.makedirs(os.path.dirname(expanded_live), exist_ok=True)
        run(f'cp "{repo_path}" "{expanded_live}"')
        pause()

    print(f"  Restoring emacs config ({EMACS_ZIP} -> ~/)")
    abs_zip = os.path.abspath(EMACS_ZIP)
    home = os.path.expanduser("~")
    # The zip stores paths relative to $HOME (".emacs.d/..."), so extracting
    # with -d $HOME lands everything back in ~/.emacs.d/ exactly where it belongs.
    run(f'unzip -o "{abs_zip}" -d "{home}"')
    pause()

def setup_dock():
    header("Setting Up Dock")
    # dockutil rewrites the Dock's plist. Make every change with --no-restart,
    # then restart the Dock once at the end so it doesn't flicker per item.
    run('defaults write com.apple.dock show-recents -bool false')
    run('dockutil --remove all --no-restart')
    pause()

    for app in DOCK_APPS:
        print(f"  Adding {app}")
        run(f'dockutil --add "{app}" --no-restart')

    for path, opts in DOCK_FOLDERS:
        expanded = os.path.expanduser(path)  # dockutil won't expand ~ itself
        print(f"  Adding folder {path}")
        run(f'dockutil --add "{expanded}" {opts} --no-restart')

    run('killall Dock')
    pause()

def setup_startup_apps():
    header("Starting Espanso and Handy")
    # Register Espanso as a background service that starts at login. Use the
    # app's own binary (not a brew symlink) so an upgrade can't break the path.
    espanso = "/Applications/Espanso.app/Contents/MacOS/espanso"
    run(f'"{espanso}" service register')
    run(f'"{espanso}" start')
    pause()

    # Add Handy as a login item (skipped if it's already there), then launch it.
    run("""osascript -e 'tell application "System Events" to if not (exists login item "Handy") then make login item at end with properties {path:"/Applications/Handy.app", hidden:false}'""")
    run('open -a Handy')
    pause()

def launch_apps():
    header("Launching Apps for Initial Setup")
    apps = [
        '/Applications/"Google Chrome.app"',
        '/Applications/1Password.app',
        '/Applications/Firefox.app',
        '/Applications/"Visual Studio Code.app"',
        '/Applications/"Splashtop Business.app"',
    ]
    for app in apps:
        print(f"  Opening {app}")
        run(f'open -n {app}')
        pause()

def final_prep():
    header("Final Setup")
    os.makedirs(os.path.expanduser("~/sbemode/code"), exist_ok=True)
    _secrets_path = os.path.expanduser("~/.secrets")
    with open(_secrets_path, "w") as f:
        f.write("# API Keys and Tokens\n")
        f.write('export DARTMOUTH_CHAT_API_KEY=""\n')
    print("Folder structure created.")
    pause()
    print("\nDon't forget to do the following before you're done:")
    print("  -> Run 'gh auth login' to authenticate the GitHub CLI")
    print("  -> Clone orgmode, ai_materials, and other code repos")
    print("  -> Populate ~/.secrets with API keys as needed")
    print("  -> Grant Espanso and Handy Accessibility access, and Handy Microphone")
    print("     access (System Settings > Privacy & Security)")
    run('figlet DONE')

# ---------------------------------------------------------------------------
# Backup
# ---------------------------------------------------------------------------

def backup():
    header("Backing Up Critical Files")
    pause()

    for live_path, repo_path in CONFIGS:
        expanded_live = os.path.expandvars(os.path.expanduser(live_path))
        print(f"  Backing up {live_path}")
        run(f'cp "{expanded_live}" "{repo_path}"')
        pause()

    scrub_handy_keys(HANDY_BACKUP)

    print(f"  Backing up emacs config -> {EMACS_ZIP}")
    abs_zip = os.path.abspath(EMACS_ZIP)
    home = os.path.expanduser("~")
    # Start from a clean archive: `zip -r` MERGES into an existing zip, which
    # would keep files you've since deleted from ~/.emacs.d. Removing it first
    # makes each backup a faithful snapshot.
    run(f'rm -f "{abs_zip}"')
    # Zip from within $HOME so entries are stored relative to home (".emacs.d/...").
    # Exclude machine-specific / regenerated cruft so restores stay small and safe:
    #   eln-cache     - native-compiled elisp, tied to this CPU + Emacs version
    #   elpa          - installed packages; init.el reinstalls them on first launch
    #   auto-save-list- transient editor state
    #   ido.last / *~ - transient state and backup files
    run(
        f'cd "{home}" && zip -r "{abs_zip}" "{EMACS_HOME_REL}" '
        f"-x '{EMACS_HOME_REL}/eln-cache/*' "
        f"-x '{EMACS_HOME_REL}/elpa/*' "
        f"-x '{EMACS_HOME_REL}/auto-save-list/*' "
        f"-x '{EMACS_HOME_REL}/ido.last' "
        f"-x '*~'"
    )
    pause()

    print("  Cleaning up old emacs temp files...")
    run('rm -f ~/zzzemacs-backups/*')
    pause()

    run('figlet COMPLETE')
    print("All critical files backed up.")
    pause()

    commit_now = input("Push these changes to GitHub now? (Y/N): ").strip().upper()
    if commit_now == "Y":
        timestamp = time.strftime("%Y-%m-%d @ %H:%M:%S")
        run("git add .")
        run(f'git commit -m "Buildbot copy of critical files {timestamp}"')
        run("git push -u origin main")
        run('figlet GIT-ED')
    else:
        print("Don't forget to push later!")
        run('figlet DONE')

# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------

def update():
    header("Updating Homebrew Packages")
    # --greedy also upgrades apps that normally update themselves (Ghostty,
    # Firefox, 1Password, VS Code, ...), which plain `brew upgrade` skips.
    run("brew update && brew upgrade --greedy")
    run("brew cleanup")
    pause()

    header("Updating Oh My Zsh")
    # `omz update` is a shell function, so call the script behind it directly.
    # This also updates zsh-autosuggestions and zsh-syntax-highlighting, which
    # Oh My Zsh has bundled since Sep 2026.
    run("zsh ~/.oh-my-zsh/tools/upgrade.sh")
    pause()

    run('figlet done-ish')
    print("Run 'source ~/.zshrc' to reload your shell config.")

# ---------------------------------------------------------------------------
# macOS updates
# ---------------------------------------------------------------------------

def macos_updates():
    header("Checking for macOS Updates")
    # List only. Installing may need a restart, so that's left to you.
    run("softwareupdate --list")
    print("\nTo install: System Settings > General > Software Update,")
    print("or run 'sudo softwareupdate --install --all'.")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Homebrew 4.4+ ships a "default ask mode": `brew install`/`brew upgrade`
    # prompt "Proceed? [Y/n]" before doing anything. HOMEBREW_NO_ASK disables it
    # so restores/updates sail through unattended. (HOMEBREW_NO_INTERACTIVE, which
    # used to live here, is not a real Homebrew variable — it never did anything.)
    # NONINTERACTIVE keeps the Homebrew installer and other flows from prompting.
    os.environ['NONINTERACTIVE'] = '1'
    os.environ['HOMEBREW_NO_ASK'] = '1'
    userid = os.getlogin()
    original_dir = os.getcwd()
    os.chdir(f'/Users/{userid}/buildbot')

    run('figlet buildbot')
    print("What should I do?")
    print("  [U] Update (Homebrew + Oh My Zsh)")
    print("  [M] Check for macOS updates")
    print("  [B] Backup critical files")
    print("  [R] Restore (full machine setup)")
    job = input("\nChoice: ").strip().upper()

    if job == "B":
        backup()
    elif job == "R":
        print("\nStarting full restoration...")
        bootstrap_brew()
        sys_prep()
        restore_brews()
        restore_settings()
        setup_dock()
        setup_startup_apps()
        launch_apps()
        final_prep()
    elif job == "U":
        update()
    elif job == "M":
        macos_updates()
    else:
        print("Unknown option. Use U, M, B, or R.")

    os.chdir(original_dir)

main()
