#!/usr/bin/env bash
# Fuzzy-find any snippet/cheat sheet in this repo and copy it to the clipboard.
#   Enter  -> copy the file PATH
#   ctrl-y -> copy the file CONTENTS
# Requires: fzf. Preview uses bat if present, else cat.
set -euo pipefail

if ! command -v fzf >/dev/null 2>&1; then
  echo "fzf not found. Install it: brew install fzf  (mac) | apt-get install fzf (linux)" >&2
  exit 1
fi

cd "$(dirname "$0")"

# ponytail: clipboard cmd resolved once, mac -> wayland -> X11; prints to stdout if none.
clip_cmd() {
  if command -v pbcopy   >/dev/null 2>&1; then echo pbcopy
  elif command -v wl-copy >/dev/null 2>&1; then echo wl-copy
  elif command -v xclip  >/dev/null 2>&1; then echo "xclip -selection clipboard"
  else echo cat
  fi
}
CLIP="$(clip_cmd)"

preview='bat --color=always --style=numbers {} 2>/dev/null || cat {}'
command -v bat >/dev/null 2>&1 || preview='cat {}'

# git ls-files: fast, respects .gitignore, never descends into .git
file="$(git ls-files | fzf --preview "$preview" \
  --header 'Enter: copy path  |  ctrl-y: copy contents' \
  --expect=ctrl-y)" || exit 0

key="$(head -1 <<<"$file")"
path="$(sed -n '2p' <<<"$file")"
[ -n "$path" ] || exit 0

if [ "$key" = "ctrl-y" ]; then
  eval "$CLIP" <"$path"
  echo "Copied contents of: $path"
else
  printf '%s' "$path" | eval "$CLIP"
  echo "Copied path: $path"
fi
