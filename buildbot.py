import os, sys, time
    
def restore_brews():
    print("Restoring Homebrew Files")
    # Start with brew cli-ish tools
    print("Installing Homebrew CLI files")
    brew_clis = ['emacs', 'coreutils', 'gh', 'oh-my-posh', 'sqlite',
                 'ollama', 'colima', 'docker', 'docker-completion',
                 'macmon', 'nmap', 'speedtest-cli', 'bat', 'tcpdump',
                 'termshark', 'figlet', 'dockutil', 'tree']
    for brew in brew_clis:
        print(f"Installing {brew} via (home)brew")
        os.sys(f'brew install {brew}')
        time.sleep(1)
    
    # Now to brew casks installation
    print("Installing Homebrew Casks")
    brew_casks = ['font-jetbrains-mono', 'font-jetbrains-mono-nerd-font',
                  'font-meslo-lg-nerd-font','1password', 'spotify', 'obs', 
                  'visual-studio-code', 'splashtop-business', 'windows-app']
    for cask in brew_casks:
        print(f"Installing {cask} via (home)brew")
        os.sys(f'brew install {cask}')
        time.sleep(1)

def restore_settings():
    # Set Sysname
    hostname = input("Enter NEW Hostname for this device: ")
    print("You will need to enter your sudo password to proceed")
    os.sys(f'sudo scutil --set HostName "{hostname.lower()}"')
    os.sys(f'sudo scutil --set ComputerName "{hostname.lower()}"')
    os.sys(f'sudo scutil --set LocalHostName "{hostname.lower()}"')
    print(f'This computer has been renamed {hostname.lower()}')
    
    # Configure git
    print("Configuring git...")
    os.sys('git config --global user.name "Brian Dellinger"')
    os.sys('git config --global user.email "bdellinger@gmail.com"')
    os.sys('git config --global init.defaultBranch main')
    
    # OhMyZsh & related secret prep
    os.sys('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
    os.sys('mkdir ~/.cache')
    os.sys('git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting')
    os.sys('git clone https://github.com/zsh-users/zsh-autosuggestions.git ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions')
    
    # System Files Restore
    print('Restoring System Files from Repo')
    os.sys('cp ~/sbemode/buildbot/configs/backup.emacs.lsp ~/.emacs')
    os.sys('cp ~/sbemode/buildbot/configs/backup.zshrc ~/.zshrc')
    os.sys('cp ~/sbemode/buildbot/configs/backup.mytheme.omp.json ~/.mytheme.omp.json')
    
    # Dock Cleanup
    print('Installing dockutil and clearing the decks... er, docks.')
    os.sys('dockutil --remove all')
    echo "Setting up the Dock"
    os.sys('dockutil --add /Applications/Google\ Chrome.app')
    os.sys('dockutil --add /System/Applications/Utilities/Terminal.app')
    os.sys('dockutil --add /Applications/Firefox.app')
    os.sys('dockutil --add /Applications/Visual\ Studio\ Code.app')
    os.sys('dockutil --add /System/Applications/System\ Settings.app')
    os.sys('dockutil --add /Applications/1Password.app')
    os.sys('dockutil --add /Applications/Windows\ App.app')
    os.sys('dockutil --add /Applications/zoom.us.app')
    os.sys('dockutil --add /System/Applications/TextEdit.app')
    os.sys('dockutil --add /Applications/Spotify.app')
    os.sys('dockutil --add /Applications/Splashtop\ Business.app')
    os.sys('dockutil --add /Applications/GlobalProtect.app')
    os.sys("dockutil --add /dockutil --add '~/Downloads' --view fan --display folder")

def launch_apps():
    # Start the GUI apps and get them configured...
    print('Opening key apps for configuration.')
    os.sys('open -n /Applications/Google\ Chrome.app')
    os.sys('open -n /Applications/1Password.app')
    os.sys('open -n /Applications/Firefox.app')
    os.sys('open -n /Applications/Visual\ Studio\ Code.app')
    os.sys('open -n /Applications/Splashtop\ Business.app')
    
    # Launch brew services
    os.sys('brew services start colima')
    os.sys('brew services start ollama')

def cleanup_and_exit():
    # setup sbemode folder
    os.sys('mkdir ~/sbemode')
    os.sys('mkdir ~/sbemode/code')
    print('DO NOT FORGET to do the following things before you are done!')
    print('----> run 'gh auth' to get github cli setup')
    print('----> Clone orgmode, ai_materials, and other code repos')
    os.sys('cd ~/sbemode')
    os.sys('figlet DONE')
    sys.exit(1)
    
def backup():
    # Implement the backup logic here
    os.system("figlet BackItUp")
    print("Backing up critical files")
    time.sleep(1)
    
    ### MIGHT BE NICE TO TURN ALL THIS INTO A VAR / CLASS AND LOOP instead
    
    # Backup Emacs Config
    print(">>> Backing up emacs config (~/.emacs)")
    os.system("cp ~/.emacs ~/sbemode/buildbot/configs/backup.emacs.lsp")
    time.sleep(1)
    
    # Backup Zshrc Config
    print(">>> Backing up zsh config (~/.zshrc)")
    os.system("cp ~/.zshrc ~/sbemode/buildbot/configs/backup.zshrc")
    time.sleep(1)
    
    # Backup OhMyPosh Config
    print(">>> Backing up oh-my-posh config (~/.mytheme.omp.json)")
    os.system("cp ~/.mytheme.omp.json ~/sbemode/buildbot/configs/backup.mytheme.omp.json")
    time.sleep(1)
    
    # Clean out emacs backups
    print("A little housekeeping, now...")
    print(">>> Cleaning out temp files in ~/zzzemacs-backups")
    os.system("rm ~/zzzemacs-backups/*")
    time.sleep(1)
    
    # All Done...
    os.system("figlet COMPLETE")
    print("All critical files have been backed up.")
    # get files into git(hub)
    commit_now = input("Should I push these changes to git(hub) for you now? (Y/N): ")
    if commit_now.upper() == "Y":
        timestamp = time.strftime("%Y-%m-%d @ %H:%M:%S")
        os.system("git add .")
        os.system(f'git commit -m "Backup of critical files {timestamp}"')
        os.system("git push -u origin main")
        os.system("figlet GIT-ED")    
    else:
        print("DO NOT FORGET TO PUSH LATER, FOOL!")
        os.sys("figlet DONE")B 
    sys.exit(1)

def main():
    job = input ("Am I [B]acking up or [R]estoring? ")
    if job.upper() == "B":
        backup()
    elif job.upper() == "R":
        print("Beginning Restoration Work")
        restore_brews()
        restore_settings()
        launch_apps()
        cleanup_and_exit()
        
main()