# cd ~/sbemode
# If you come from bash you might have to change your $PATH.
# Path to your Oh My Zsh installation.
plugins=(git brew sudo zsh-autosuggestions zsh-syntax-highlighting)
export ZSH="$HOME/.oh-my-zsh"
source $ZSH/oh-my-zsh.sh

# Location of oh-my-posh config file
eval "$(oh-my-posh init zsh --config ~/.mytheme.omp.json)"
zstyle ':omz:update' mode auto        # update automatically without asking
zstyle ':omz:update' frequency 14

# Load secrets file
source ~/.secrets

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Aliases for Frequent Commands
## SBEMODE alias
alias sb='cd ~/sbemode/orgmode && emacs --eval "(progn (org-agenda nil \"a\") (org-agenda-day-view) (delete-other-windows))"'

## AI-related aliases
alias morning='cd ~/sbemode/@resist_entropy && claude /morning --permission-mode acceptEdits'
alias night='cd ~/sbemode/@resist_entropy && claude /night --permission-mode acceptEdits'
alias curlmodels="curl https://api.anthropic.com/v1/models -H 'anthropic-version: 2023-06-01' -H 'X-Api-Key: $ANTHROPIC_PERSONAL_API_KEY'"

# Misc 
alias ls='ls -hal'
alias bb='python3 ~/buildbot/buildbot.py'
alias send_it='python3 send_it.py'
