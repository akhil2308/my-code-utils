# Bash Cheat Sheet

## Safe script header
```bash
#!/usr/bin/env bash
set -euo pipefail              # exit on error, unset var, pipe failure
IFS=$'\n\t'                    # sane word splitting
trap 'echo "failed at line $LINENO"' ERR
```

## find
```bash
find . -name "*.py"                       # by name
find . -type f -mtime -1                  # files modified in last 24h
find . -type f -size +100M                # bigger than 100MB
find . -name "*.tmp" -delete              # find + delete
find . -type f -exec grep -l "TODO" {} +  # files containing TODO
```

## grep
```bash
grep -rn "pattern" .            # recursive, line numbers
grep -ri "pattern" .            # case-insensitive
grep -rl "pattern" .            # only filenames
grep -rE "foo|bar" .            # regex / alternation
grep -v "pattern"               # invert (lines NOT matching)
grep -A3 -B3 "pattern" file     # 3 lines of context around
```

## xargs
```bash
grep -rl "old" . | xargs sed -i 's/old/new/g'   # mass replace
ls *.log | xargs -P4 -I{} gzip {}               # parallel, 4 at a time
echo "a b c" | xargs -n1                        # one arg per line
```

## sed / awk one-liners
```bash
sed -i 's/foo/bar/g' file       # in-place replace (GNU); macOS: sed -i '' ...
sed -n '10,20p' file            # print lines 10-20
awk '{print $2}' file           # 2nd column
awk -F, '{print $1}' file.csv   # CSV first column
awk '{sum+=$1} END {print sum}' # sum a column
```

## Processes & ports
```bash
ps aux | grep <name>
lsof -i :8080                   # what's using port 8080
kill -9 $(lsof -t -i :8080)     # kill it
top / htop                      # live process view
jobs ; fg ; bg ; disown         # job control
```

## Permissions
```bash
chmod +x script.sh
chmod 644 file                  # rw-r--r--
chmod -R 755 dir                # rwxr-xr-x recursive
chown -R user:group dir
```

## tar / compression
```bash
tar -czf out.tar.gz dir/        # create gzip
tar -xzf out.tar.gz             # extract gzip
tar -tzf out.tar.gz             # list contents
zip -r out.zip dir/  ;  unzip out.zip
```

## Quick tricks
```bash
!!                              # repeat last command
sudo !!                         # repeat last as root
cd -                            # previous directory
Ctrl+R                          # reverse history search
command | tee file.log          # see output AND save it
diff <(cmd1) <(cmd2)            # diff two command outputs
```
