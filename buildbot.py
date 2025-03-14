import os, sys, time

def restore():
    os.system("figlet RESTORING")
    print("Setting new system parameters and restoring files...")
    
    # Set system-wide preferences
    print("Configuring git...")
    os.sys('git config --global user.name "Brian Dellinger"')
    os.sys('git config --global user.email "bdellinger@gmail.com"')
    os.sys('git config --global init.defaultBranch main')
    

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
    
    os.sys("figlet ALL DONE")        
    sys.exit(1)

def main():
    job = input ("Am I [B]acking up or [R]estoring? ")
    if job.upper() == "B":
        backup()
    elif job.upper() == "R":
        restore()   

main()