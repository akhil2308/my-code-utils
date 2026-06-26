# Linux Ops Cheat Sheet

## Ports & network
```bash
ss -tulpn                       # listening TCP/UDP ports + PIDs (modern)
lsof -i :8080                   # what's on a port
netstat -tulpn                  # old equivalent
curl -I https://site            # headers only
curl -v https://site            # verbose handshake
dig +short example.com          # DNS lookup
ping -c4 host ; traceroute host
```

## Disk & memory
```bash
df -h                           # disk free, human readable
du -sh *                        # size of each item in cwd
du -sh * | sort -rh | head      # biggest items
free -h                         # memory usage
ncdu                            # interactive disk usage (if installed)
```

## Processes
```bash
top / htop
ps aux --sort=-%mem | head      # top memory hogs
ps aux --sort=-%cpu | head      # top CPU hogs
kill -15 <pid>                  # graceful (SIGTERM)
kill -9 <pid>                   # force (SIGKILL)
pkill -f "pattern"              # kill by command match
nice -n10 cmd ; renice 10 -p <pid>
```

## systemd (services)
```bash
systemctl status nginx
systemctl start|stop|restart nginx
systemctl enable|disable nginx  # auto-start on boot
systemctl daemon-reload         # after editing a unit file
systemctl list-units --type=service --state=running
```

## journalctl (logs)
```bash
journalctl -u nginx -f          # follow a service's logs
journalctl -u nginx --since "1 hour ago"
journalctl -p err -b            # errors since last boot
journalctl --disk-usage ; journalctl --vacuum-time=7d
```

## cron syntax
```
# ┌─ minute (0-59)
# │ ┌─ hour (0-23)
# │ │ ┌─ day of month (1-31)
# │ │ │ ┌─ month (1-12)
# │ │ │ │ ┌─ day of week (0-6, Sun=0)
# * * * * *  command
0 2 * * *      # daily at 02:00
*/15 * * * *   # every 15 minutes
0 9 * * 1      # 09:00 every Monday
@reboot        # at startup
```
```bash
crontab -e ; crontab -l         # edit / list your crontab
```

## Permissions & users
```bash
sudo -u www-data cmd            # run as another user
id ; whoami ; groups
usermod -aG docker $USER        # add user to a group (re-login after)
chmod / chown                   # see Bash cheat sheet
```

## Files & search
```bash
tail -f /var/log/syslog
grep -rn "pattern" /etc
watch -n2 'df -h'               # rerun every 2s
```
