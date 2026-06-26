# tmux Cheat Sheet

Prefix key: `Ctrl+b` (default)

## Sessions

```bash
tmux                                 # new session
tmux new -s myproject                # named session
tmux ls                              # list sessions
tmux attach -t myproject             # attach by name
tmux attach -t 0                     # attach by index
tmux kill-session -t myproject       # kill session
tmux kill-server                     # kill all sessions
```

### Inside tmux

```
prefix + d          detach
prefix + s          list/switch sessions (interactive)
prefix + $          rename session
prefix + (          previous session
prefix + )          next session
```

## Windows (tabs)

```
prefix + c          new window
prefix + ,          rename window
prefix + n          next window
prefix + p          previous window
prefix + 0-9        switch to window by number
prefix + w          list windows (interactive)
prefix + &          kill window (confirm)
prefix + .          move window (enter new index)
```

## Panes (splits)

```
prefix + %          split vertical (left/right)
prefix + "          split horizontal (top/bottom)
prefix + arrow      navigate panes
prefix + o          cycle panes
prefix + ;          last active pane
prefix + x          kill pane
prefix + z          zoom/unzoom pane (fullscreen toggle)
prefix + {          move pane left
prefix + }          move pane right
prefix + space      cycle pane layouts
prefix + !          break pane into new window
```

## Resize Panes

```
prefix + Ctrl+arrow   resize (hold Ctrl, tap arrow)
prefix + Alt+arrow    resize in larger steps
```

## Copy Mode (scroll / search)

```
prefix + [          enter copy mode
q                   exit copy mode
arrow keys          scroll
Ctrl+b / Ctrl+f     page up / page down
/                   search forward
?                   search backward
n / N               next / previous match
Space               start selection
Enter               copy selection
prefix + ]          paste
```

## Synchronize Panes (type in all panes at once)

```bash
# inside tmux
:setw synchronize-panes on
:setw synchronize-panes off
```

## Useful Config (~/.tmux.conf)

```bash
# remap prefix to Ctrl+a
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# split with | and -
bind | split-window -h
bind - split-window -v

# reload config
bind r source-file ~/.tmux.conf \; display "Reloaded!"

# mouse support
set -g mouse on

# start window/pane numbering at 1
set -g base-index 1
setw -g pane-base-index 1

# increase scrollback
set -g history-limit 10000

# 256 colors
set -g default-terminal "screen-256color"
```

## Scripting / Automation

```bash
# run command in new window
tmux new-window -t myproject -n logs "tail -f /var/log/app.log"

# send keys to a pane
tmux send-keys -t myproject:0.0 "python app.py" Enter

# multi-pane layout script
tmux new-session -d -s dev -n editor
tmux split-window -h -t dev:0
tmux split-window -v -t dev:0.1
tmux send-keys -t dev:0.0 "vim ." Enter
tmux send-keys -t dev:0.1 "python -m pytest -f" Enter
tmux attach -t dev
```

## One-liners

```bash
tmux new-session -A -s main          # attach or create 'main'
tmux list-panes -a -F "#{session_name}:#{window_name}.#{pane_index}"
```
