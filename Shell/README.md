# Shell

Day-to-day shell config and a fresh-machine bootstrap.

| File | What |
|---|---|
| [aliases.sh](aliases.sh) | git / ls / docker / k8s / python aliases |
| [functions.sh](functions.sh) | `mkcd`, `extract`, `killport`, `gclean`, `serve` |
| [setup.sh](setup.sh) | install common tools + wire the above into your shell |

## Bootstrap a machine

```bash
bash Shell/setup.sh
```

What it does:

- **macOS** → installs Homebrew (if missing), then `brew install fzf bat ripgrep jq tmux git eza`.
- **Debian/Ubuntu** → `apt-get install` the same (eza may need cargo).
- Appends a guarded block to `~/.zshrc` **and** `~/.bashrc` that sources `aliases.sh` + `functions.sh`. Re-running is safe — the marker block is added only once.

Just want the aliases/functions without installing anything:

```bash
source Shell/aliases.sh Shell/functions.sh
```
