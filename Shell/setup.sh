#!/usr/bin/env bash
# Fresh-machine bootstrap: install common tools and wire up aliases/functions.
# Supports macOS (Homebrew) and Debian/Ubuntu Linux (apt). Idempotent.
# ponytail: brew/apt only — other distros get a manual hint, not a package-manager matrix.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="fzf bat ripgrep jq tmux git eza"
MARKER="# >>> my-code-utils >>>"

install_mac() {
  if ! command -v brew >/dev/null 2>&1; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  echo "brew install $TOOLS"
  # shellcheck disable=SC2086
  brew install $TOOLS
}

install_linux() {
  if ! command -v apt-get >/dev/null 2>&1; then
    echo "Non-apt Linux detected. Install manually: $TOOLS" >&2
    return 0
  fi
  # Debian package names differ slightly: ripgrep ok, bat ok, eza may be unavailable on old apt.
  sudo apt-get update
  echo "apt-get install fzf bat ripgrep jq tmux git"
  sudo apt-get install -y fzf bat ripgrep jq tmux git || true
  command -v eza >/dev/null 2>&1 || echo "note: 'eza' not in apt here — install via cargo or skip."
}

case "$(uname -s)" in
  Darwin) install_mac ;;
  Linux)  install_linux ;;
  *) echo "Unsupported OS: $(uname -s). Install manually: $TOOLS" >&2 ;;
esac

# Wire aliases + functions into shell rc files, once (guarded by marker).
wire_rc() {
  rc="$1"
  [ -e "$rc" ] || return 0
  if grep -qF "$MARKER" "$rc" 2>/dev/null; then
    echo "already wired: $rc"
    return 0
  fi
  {
    echo ""
    echo "$MARKER"
    echo "[ -f \"$REPO_DIR/Shell/aliases.sh\" ]   && . \"$REPO_DIR/Shell/aliases.sh\""
    echo "[ -f \"$REPO_DIR/Shell/functions.sh\" ] && . \"$REPO_DIR/Shell/functions.sh\""
    echo "# <<< my-code-utils <<<"
  } >>"$rc"
  echo "wired: $rc"
}

wire_rc "$HOME/.zshrc"
wire_rc "$HOME/.bashrc"

echo "Done. Restart your shell or 'source' your rc to pick up aliases/functions."
