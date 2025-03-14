## This is a backup script to grab key configuration files and 
## commit them to git & github once they we've nabbed 'em.
echo " _                _                           "
echo "| |__   __ _  ___| | _____  _ __  _   _ _ __  "
echo "| '_ \ / _' |/ __| |/ / _ \| '_ \| | | | '_ \ "
echo "| |_) | (_| | (__|   < (_) | | | | |_| | |_) |"
echo "|_.__/ \__,_|\___|_|\_\___/|_| |_|\__,_| .__/ "
echo "                                       |_|  "
echo "'We fixin' to backup our key config files, peeps."
sleep 1

# Copy key config files to ~/sbemode/config_files folder
## Backup emacs config
echo ">>> Backing up emacs config (~/.emacs)"
cp ~/.emacs ~/sbemode/code/system_code/config_files/backup.emacs.lsp
sleep 1

## Backup zsh config
echo ">>> Backing up zsh config (~/.zshrc)"
cp ~/.zshrc ~/sbemode/code/system_code/config_files/backup.zshrc
sleep 1

## Backup OhMyPosh config
echo ">>> Backing up oh-my-posh config (~/.mytheme.omp.json)"
cp ~/.mytheme.omp.json ~/sbemode/code/system_code/config_files/backup.mytheme.omp.json
sleep 1

## Backup terminal settings
echo ">>> Backing up Terminal preferences (~/Lib/Pref/com.apple.Terminal.plist)"
cp ~/Library/Preferences/com.apple.Terminal.plist ~/sbemode/code/system_code/config_files/backup.com.apple.Terminal.plist
sleep 1

## Backup Finder Preferences
echo ">>> Backing up Finder preferences (~/Lib/Pref/com.apple.finder.plist)"
cp ~/Library/Preferences/com.apple.finder.plist ~/sbemode/code/system_code/config_files/backup.com.apple.finder.plist
sleep 1

## Backup System Preferences
echo ">>> Backing up System Preferences (~Lib/Pref/com.apple.systempreferences.plist)"
cp ~/Library/Preferences/com.apple.systempreferences.plist ~/sbemode/code/system_code/config_files/backup.com.apple.systempreferences.plist
sleep 1


## End of backup procedures
echo "All critical configuration files backed up!"
sleep 2

## Remove old org mode backup files
echo ""
echo "Now it's time for a little housekeeping..."
sleep 1
echo ">>> Cleaning out temp files in ~/zzzemacs-backups"
rm ~/zzzemacs-backups/*
sleep 2

## End and recommend git push of config files
echo "     _                  _ "
echo "  __| | ___  _ __   ___| |"
echo " / _' |/ _ \| '_ \ / _ \ | "
echo "| (_| | (_) | | | |  __/_|"
echo " \__,_|\___/|_| |_|\___(_)"
echo ""
echo "All configuration files have been staged in the ~/code/config_files"
echo "It is strongly recommended that you COMMIT those changes ASAP!!"
sleep 1
