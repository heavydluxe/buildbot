# If you come from bash you might have to change your $PATH.

# Load secrets file
source ~/.secrets

# Path to your Oh My Zsh installation.
plugins=(git brew sudo zsh-autosuggestions zsh-syntax-highlighting)
export ZSH="$HOME/.oh-my-zsh"
source $ZSH/oh-my-zsh.sh
export PATH="$HOME/.local/bin:$PATH"

# Location of oh-my-posh config file
eval "$(oh-my-posh init zsh --config ~/.mytheme.omp.json)"
zstyle ':omz:update' mode auto        # update automatically without asking
zstyle ':omz:update' frequency 14

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Aliases for Frequent Commands
## Emacs Orgmode Alias (deprecated now that I'm loading emacs direct in app)
## alias sb='cd ~/@embrace_entropy && emacs --eval "(progn (org-agenda nil \"a\") (org-agenda-day-view) (delete-other-windows))"'

## Claude Coach Commands (Claude Code skill; uses default ~/.claude config dir)
alias emacscoach='claude --model haiku "/emacs-coach"'

# Misc 
alias ls='ls -hal'
alias bb='python3 ~/buildbot/buildbot.py'
alias ol='ollama'
alias olon='brew services start ollama'
alias oloff='brew services stop ollama'
alias colon='brew services start colima'
alias coloff='brew services stop colima'

# Dartmouth Claude Config
claude-dart() {
  source ~/.secrets
  CLAUDE_CONFIG_DIR="${HOME}/.claude-dart" claude "$@"
}
