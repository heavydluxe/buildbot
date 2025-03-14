import os, sys, time

def backup():
    # Implement the backup logic here
    os.system("figlet BackItUp")
    print("Backing up critical files")
    time.sleep(1)
    
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
    
    # Backup Terminal Settings
    print(">>> Backing up Terminal preferences (~/Lib/Pref/com.apple.Terminal.plist)")
    os.system("cp ~/Library/Preferences/com.apple.Terminal.plist ~/sbemode/buildbot/configs/backup.com.apple.Terminal.plist")
    time.sleep(1)
    
    # Clean out emacs backups
    os.system("figlet CleanUp")
    print("A little housekeeping, now...")
    print(">>> Cleaning out temp files in ~/zzzemacs-backups")
    os.system("rm ~/zzzemacs-backups/*")
    time.sleep(1)
    
    # All Done...
    os.system("figlet COMPLETE")
    print("All critical files have been backed up.")
    print("Commit the BuildBot Repo ASAP to cloudify your changes!")
    sys.exit(1)

def restore():
    # Implement the restore logic here
    print("Restoring files...")
    # Example: Copy files from a backup directory back to the original location
    os.system("cp -r /path/to/backup /path/to/source")

def main():
    job = input ("Am I [B]acking up or [R]estoring? ")
    if job == "B":
        backup()
    elif job == "R":
        restore()
    else:
        print("Invalid choice. Please enter 'B' for Backup or 'R' for Restore.")
        sys.exit(1)
        
main()