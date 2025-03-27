import os, sys, time
    
def restore_brews():
    # Brew Items - CLIs and Casks
    brew_clis = ['bat', 'colima', 'coreutils', 'docker', 'docker-completion',
                 'dockutil', 'emacs', 'figlet', 'gh', 'macmon', 'nmap',
                 'oh-my-posh', 'ollama', 'speedtest-cli', 'sqlite',
                 'tcpdump', 'termshark', 'tree']
    
    brew_casks = ['1password', 'font-jetbrains-mono',
                  'font-jetbrains-mono-nerd-font',
                  'font-meslo-lg-nerd-font', 'obs', 'splashtop-business',
                  'spotify', 'visual-studio-code', 'windows-app']
    
    # Run th restoration loops.    
    print("Restoring Homebrew Files")
    print("Installing Homebrew CLI files")
    for brew in brew_clis:
        print(f"Installing {brew} via (home)brew")
        os.system(f'brew install {brew}')
        time.sleep(1)
    print("Installing Homebrew Casks")
    for cask in brew_casks:
        print(f"Installing {cask} via (home)brew")
        os.system(f'brew install {cask}')
        time.sleep(1)

def restore_settings():
    # Set Sysname
    hostname = input("Enter NEW Hostname for this device: ")
    print("You will need to enter your sudo password to proceed")
    os.system(f'sudo scutil --set HostName "{hostname.lower()}"')
    os.system(f'sudo scutil --set ComputerName "{hostname.lower()}"')
    os.system(f'sudo scutil --set LocalHostName "{hostname.lower()}"')
    print(f'This computer has been renamed {hostname.lower()}')
    
    # Configure git
    print("Configuring git...")
    os.system('git config --global user.name "Brian Dellinger"')
    os.system('git config --global user.email "bdellinger@gmail.com"')
    os.system('git config --global init.defaultBranch main')
    
    # OhMyZsh & related secret prep
    os.system('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
    os.system('mkdir ~/.cache')
    os.system('git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting')
    os.system('git clone https://github.com/zsh-users/zsh-autosuggestions.git ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions')
    
    # System Files Restore
    print('Restoring System Files from Repo')
    os.system('cp ~/sbemode/buildbot/configs/backup.emacs.lsp ~/.emacs')
    os.system('cp ~/sbemode/buildbot/configs/backup.zshrc ~/.zshrc')
    os.system('cp ~/sbemode/buildbot/configs/backup.mytheme.omp.json ~/.mytheme.omp.json')
    
    # Dock Cleanup
    dock_apps = ['/Applications/Visual Studio Code.app',  
                 '/Applications/Firefox.app',
                 'Applications/Google Chrome.app',
                 '/System/Applications/System Settings.app',
                 '/Applications/1Password.app',
                 '/Applications/Windows App.app',
                 '/Applications/zoom.us.app',
                 '/Applications/GlobalProtect.app',
                 '/Applications/Splashtop Business.app',
                 '/Applications/Spotify.app']
    print('Installing dockutil and clearing the decks... er, docks.')
    os.system('dockutil --remove all')
    print("Setting up the Dock")
    for apps in dock_apps:
        os.system(f'dockutil --add {apps}')
    os.system("dockutil --add /dockutil --add '~/Downloads' --view fan --display folder")

def launch_apps():
    # Start the GUI apps and get them configured...
    print('Opening key apps for configuration.')
    os.system('open -n /Applications/Google Chrome.app')
    os.system('open -n /Applications/1Password.app')
    os.system('open -n /Applications/Firefox.app')
    os.system('open -n /Applications/Visual Studio Code.app')
    os.system('open -n /Applications/Splashtop Business.app')
    
    # Launch brew services
    os.system('brew services start colima')
    os.system('brew services start ollama')

def cleanup_and_exit():
    # setup sbemode folder
    os.system('mkdir ~/sbemode')
    os.system('mkdir ~/sbemode/code')
    print('DO NOT FORGET to do the following things before you are done!')
    print('----> run "gh auth" to get github cli setup')
    print('----> Clone orgmode, ai_materials, and other code repos')
    os.system('cd ~/sbemode')
    os.system('figlet DONE')
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
        os.system("figlet DONE")
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