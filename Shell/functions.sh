# Small functions stdlib/aliases can't express. Sourced by zsh and bash.
# ponytail: only things that genuinely save keystrokes — no framework.
# shellcheck shell=sh

# Make a dir and cd into it.
mkcd() { mkdir -p "$1" && cd "$1" || return; }

# Extract almost any archive.
extract() {
  [ -f "$1" ] || { echo "extract: '$1' is not a file" >&2; return 1; }
  case "$1" in
    *.tar.bz2|*.tbz2) tar xjf "$1" ;;
    *.tar.gz|*.tgz)   tar xzf "$1" ;;
    *.tar.xz)         tar xJf "$1" ;;
    *.tar)            tar xf  "$1" ;;
    *.bz2)            bunzip2 "$1" ;;
    *.gz)             gunzip  "$1" ;;
    *.zip)            unzip   "$1" ;;
    *.rar)            unrar x "$1" ;;
    *.7z)             7z x    "$1" ;;
    *) echo "extract: don't know how to extract '$1'" >&2; return 1 ;;
  esac
}

# Kill whatever is listening on a TCP port.
killport() {
  [ -n "$1" ] || { echo "usage: killport <port>" >&2; return 1; }
  pid="$(lsof -ti tcp:"$1" 2>/dev/null)"
  [ -n "$pid" ] || { echo "nothing on port $1"; return 0; }
  echo "killing $pid on port $1"; kill -9 $pid
}

# Delete local branches already merged into the default branch.
gclean() {
  base="$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')"
  base="${base:-main}"
  git branch --merged "$base" | grep -vE "^\*|\s$base$" | xargs -r git branch -d
}

# Serve the current dir over HTTP (default port 8000).
serve() { python3 -m http.server "${1:-8000}"; }
