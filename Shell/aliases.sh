# Day-to-day aliases. POSIX-safe so both zsh and bash can source this.
# shellcheck shell=sh

# --- git ---
alias gs='git status -sb'
alias ga='git add'
alias gc='git commit'
alias gco='git checkout'
alias gp='git push'
alias gpl='git pull'
alias gd='git diff'
alias gl='git log --oneline --graph --decorate -20'
alias gb='git branch'

# --- ls (eza if installed, else plain ls) ---
if command -v eza >/dev/null 2>&1; then
  alias ls='eza'
  alias ll='eza -lah --git'
  alias lt='eza --tree --level=2'
else
  alias ll='ls -lah'
fi

# --- docker / compose ---
alias d='docker'
alias dc='docker compose'
alias dps='docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"'
alias dprune='docker system prune -f'

# --- kubernetes ---
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kl='kubectl logs -f'

# --- python ---
alias py='python3'
alias venv='python3 -m venv .venv && . .venv/bin/activate'
alias act='. .venv/bin/activate'

# --- misc ---
alias ..='cd ..'
alias ...='cd ../..'
alias path='echo "$PATH" | tr ":" "\n"'
alias ports='lsof -i -P -n | grep LISTEN'
