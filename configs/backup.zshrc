# If you come from bash you might have to change your $PATH.

# Load secrets file
source ~/.secrets
cd ~/sbemode

# Path to your Oh My Zsh installation.
plugins=(git brew sudo zsh-autosuggestions zsh-syntax-highlighting)
export ZSH="$HOME/.oh-my-zsh"
source $ZSH/oh-my-zsh.sh
export PATH="$HOME/.local/bin:$PATH"

# Llama.cpp path
export LLAMA_CACHE=~/.llamacpp/cache

# Location of oh-my-posh config file
eval "$(oh-my-posh init zsh --config ~/.mytheme.omp.json)"
zstyle ':omz:update' mode auto        # update automatically without asking
zstyle ':omz:update' frequency 14

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Aliases for Frequent Commands
## Emacs Orgmode Alias
alias sb='cd ~/sbemode/@embrace_entropy && emacs --eval "(progn (org-agenda nil \"a\") (org-agenda-day-view) (delete-other-windows))"'

## AI-related aliases
alias curlclaude="curl https://api.anthropic.com/v1/models -H 'anthropic-version: 2023-06-01' -H 'X-Api-Key: $ANTHROPIC_PERSONAL_API_KEY'"

# Misc 
alias ls='ls -hal'
alias bb='python3 ~/buildbot/buildbot.py'
alias tn='tmux new-session -s'
alias ta='tmux attach -t'
alias tl='tmux ls'

