# Regex Cheat Sheet

Tools: Python (`re`), `grep -E`, `sed`, JS, `ripgrep` (`rg`)

## Anchors & Boundaries

```
^           start of string (or line in multiline mode)
$           end of string (or line in multiline mode)
\b          word boundary
\B          not a word boundary
\A          start of string (Python/PCRE only, no multiline effect)
\Z          end of string (Python/PCRE only)
```

## Character Classes

```
.           any character except newline
\d          digit [0-9]
\D          non-digit
\w          word character [a-zA-Z0-9_]
\W          non-word character
\s          whitespace (space, tab, newline)
\S          non-whitespace
[abc]       any of a, b, c
[^abc]      none of a, b, c
[a-z]       range a to z
[A-Za-z0-9] alphanumeric
```

## Quantifiers

```
*           0 or more (greedy)
+           1 or more (greedy)
?           0 or 1 (greedy)
{n}         exactly n
{n,}        n or more
{n,m}       between n and m
*?          0 or more (lazy)
+?          1 or more (lazy)
??          0 or 1 (lazy)
```

## Groups & Alternation

```
(abc)       capturing group
(?:abc)     non-capturing group
(?P<name>)  named group (Python)
(?<name>)   named group (PCRE/JS)
a|b         alternation (a or b)
\1          backreference to group 1
\g<name>    backreference by name (Python)
```

## Lookahead / Lookbehind

```
(?=abc)     positive lookahead  — followed by abc
(?!abc)     negative lookahead  — not followed by abc
(?<=abc)    positive lookbehind — preceded by abc
(?<!abc)    negative lookbehind — not preceded by abc
```

```python
import re
re.findall(r'\d+(?= dollars)', 'pay 100 dollars')   # ['100']
re.findall(r'(?<=\$)\d+', 'price $99')              # ['99']
```

## Flags

| Flag | Python | JS | Meaning |
|------|--------|----|---------|
| Case-insensitive | `re.I` | `i` | match regardless of case |
| Multiline | `re.M` | `m` | `^`/`$` match line start/end |
| Dot-all | `re.S` | `s` | `.` matches newline too |
| Verbose | `re.X` | — | allow comments/whitespace in pattern |

## Common Patterns

```python
# Email (practical, not RFC-complete)
r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}'

# UUID v4
r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

# IPv4
r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

# IPv6 (simplified)
r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}'

# URL (http/https)
r'https?://[^\s<>"\'()]+'

# ISO date (YYYY-MM-DD)
r'\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])'

# Time (HH:MM or HH:MM:SS)
r'(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?'

# Slug (URL-safe)
r'[a-z0-9]+(?:-[a-z0-9]+)*'

# Semantic version
r'\d+\.\d+\.\d+'

# Credit card (no spaces)
r'\b(?:\d{4}){3}\d{4}\b'

# Python/JS variable name
r'[a-zA-Z_]\w*'

# Hex color
r'#(?:[0-9a-fA-F]{3}){1,2}\b'
```

## Python `re` Quick Reference

```python
import re

re.match(r'\d+', '123abc')          # match at start only
re.search(r'\d+', 'abc123')         # search anywhere
re.findall(r'\d+', 'a1 b2 c3')      # ['1', '2', '3']
re.finditer(r'\d+', 'a1 b2')        # iterator of match objects
re.sub(r'\s+', ' ', 'a  b   c')     # 'a b c'
re.split(r'[,;]+', 'a,b;;c')        # ['a', 'b', 'c']

m = re.search(r'(?P<year>\d{4})', '2024-01')
m.group('year')                      # '2024'
m.span()                             # (0, 4)

# compiled pattern (reuse)
pat = re.compile(r'\d+', re.I)
pat.findall('A1 B2')
```

## grep / ripgrep

```bash
grep -E '\d{3}-\d{4}' file.txt       # extended regex
grep -P '(?<=@)\w+' file.txt         # PCRE (lookbehind etc.)
rg '\b\w{10,}\b' .                   # words 10+ chars, recursive
rg -o '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' access.log  # extract IPs
```

## sed

```bash
sed 's/foo/bar/g' file.txt           # replace all
sed -E 's/([0-9]{4})-([0-9]{2})/\2\/\1/' file.txt  # swap date parts
sed -n '/^ERROR/p' file.txt          # print matching lines
```
