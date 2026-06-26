# SSH Cheat Sheet

## Basic Connection

```bash
ssh user@host                        # connect
ssh -p 2222 user@host                # custom port
ssh -i ~/.ssh/id_rsa user@host       # specify identity file
ssh -v user@host                     # verbose (debug)
```

## ~/.ssh/config

```
Host myserver
    HostName 192.168.1.10
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60           # keep-alive every 60s
    ServerAliveCountMax 3

Host bastion
    HostName bastion.example.com
    User ec2-user
    IdentityFile ~/.ssh/bastion_key

Host private
    HostName 10.0.0.5
    User ubuntu
    ProxyJump bastion                # jump through bastion
```

```bash
ssh myserver                         # uses config above
```

## Key Management

```bash
ssh-keygen -t ed25519 -C "me@example.com"        # generate key (prefer ed25519)
ssh-keygen -t rsa -b 4096 -C "me@example.com"    # RSA fallback
ssh-copy-id user@host                             # copy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@host   # specify key to copy
cat ~/.ssh/id_ed25519.pub | ssh user@host "cat >> ~/.ssh/authorized_keys"  # manual copy
```

## SSH Agent

```bash
eval "$(ssh-agent -s)"              # start agent
ssh-add ~/.ssh/id_ed25519           # add key to agent
ssh-add -l                          # list loaded keys
ssh-add -D                          # remove all keys from agent
ssh -A user@host                    # forward agent (use carefully)
```

## Port Forwarding

```bash
# Local forwarding: access remote service locally
ssh -L 8080:localhost:80 user@host  # localhost:8080 → host:80
ssh -L 5432:db.internal:5432 user@bastion  # tunnel to internal DB

# Remote forwarding: expose local port on remote
ssh -R 9090:localhost:3000 user@host  # host:9090 → local:3000

# Dynamic (SOCKS proxy)
ssh -D 1080 user@host               # SOCKS5 proxy on localhost:1080
# then: curl --socks5 localhost:1080 http://internal-site
```

## Jump Hosts / ProxyJump

```bash
ssh -J bastion user@private-host    # single jump
ssh -J user@b1,user@b2 user@target  # chained jumps

# in ~/.ssh/config (preferred)
Host private
    ProxyJump bastion
```

## Tunnels (persistent)

```bash
# Keep tunnel alive, reconnect on drop
ssh -fNL 5432:db:5432 user@bastion  # -f background, -N no command
autossh -M 20000 -fNL 5432:db:5432 user@bastion  # autossh for auto-reconnect
```

## SCP / SFTP

```bash
scp file.txt user@host:/remote/path/          # upload
scp user@host:/remote/file.txt ./             # download
scp -r ./dir user@host:/remote/               # recursive
scp -P 2222 file.txt user@host:/path/         # custom port

sftp user@host                                # interactive sftp
```

## rsync over SSH

```bash
rsync -avz ./local/ user@host:/remote/        # sync local → remote
rsync -avz user@host:/remote/ ./local/        # sync remote → local
rsync -avz --delete ./local/ user@host:/remote/  # mirror (deletes extras)
rsync -avz -e "ssh -p 2222" ./local/ user@host:/remote/  # custom port
```

## Escape Sequences (during session)

```
~.    disconnect
~C    open command line (for adding port forwards mid-session)
~#    list forwarded connections
~?    help
```

## Hardening Tips

```bash
# /etc/ssh/sshd_config
PasswordAuthentication no
PermitRootLogin no
AllowUsers youruser
Port 2222                            # non-default port
```

## Useful One-liners

```bash
ssh user@host 'uptime'               # run single command
ssh user@host 'bash -s' < script.sh  # run local script remotely
ssh user@host "cat /etc/passwd" | grep root  # pipe remote output locally
ssh -t user@host 'sudo su -'        # force TTY allocation (for sudo)
```
