# curl Cheat Sheet

## Basic Requests

```bash
curl https://example.com                        # GET
curl -I https://example.com                     # HEAD only (headers)
curl -i https://example.com                     # include headers in output
curl -s https://example.com                     # silent (no progress)
curl -o output.html https://example.com         # save to file
curl -O https://example.com/file.zip            # save with remote filename
curl -L https://example.com                     # follow redirects
curl -L --max-redirs 5 https://example.com      # limit redirects
```

## HTTP Methods

```bash
curl -X POST https://api.example.com/endpoint
curl -X PUT https://api.example.com/resource/1
curl -X DELETE https://api.example.com/resource/1
curl -X PATCH https://api.example.com/resource/1
```

## Request Body / JSON

```bash
# POST JSON
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# from file
curl -X POST https://api.example.com/data \
  -H "Content-Type: application/json" \
  -d @payload.json

# --data-raw avoids @ file interpretation
curl -X POST https://api.example.com \
  --data-raw '{"key": "value"}'
```

## Headers

```bash
curl -H "Authorization: Bearer TOKEN" https://api.example.com/me
curl -H "X-Api-Key: abc123" -H "Accept: application/json" https://api.example.com
curl -H "Content-Type: application/json" https://api.example.com
```

## Authentication

```bash
curl -u user:pass https://api.example.com           # Basic auth
curl -H "Authorization: Basic $(echo -n user:pass | base64)" https://api.example.com
curl -H "Authorization: Bearer $TOKEN" https://api.example.com  # Bearer token
curl --cookie "session=abc123" https://example.com   # cookie
curl -c cookies.txt -b cookies.txt https://example.com  # save/load cookies
```

## Form Data / File Upload

```bash
# form-encoded
curl -X POST https://example.com/login \
  -d "username=alice&password=secret"

# multipart form (file upload)
curl -X POST https://api.example.com/upload \
  -F "file=@/path/to/file.png" \
  -F "description=my file"

# multiple files
curl -X POST https://api.example.com/upload \
  -F "files[]=@file1.png" \
  -F "files[]=@file2.png"
```

## Timeouts

```bash
curl --connect-timeout 5 https://example.com     # connection timeout (seconds)
curl --max-time 30 https://example.com           # total request timeout
curl -m 10 https://example.com                   # shorthand for --max-time
```

## Debugging / Verbose

```bash
curl -v https://example.com                      # full request + response headers
curl --trace - https://example.com               # hex dump of all traffic
curl -w "\n%{http_code}\n" https://example.com   # print status code after
curl -w "%{time_total}s\n" -o /dev/null -s https://example.com  # time the request
```

## TLS / Certificates

```bash
curl -k https://self-signed.example.com          # skip TLS verification (unsafe)
curl --cacert ca.pem https://example.com         # custom CA
curl --cert client.pem --key client.key https://example.com  # mTLS
```

## Proxy

```bash
curl -x http://proxy:8080 https://example.com
curl --socks5 localhost:1080 https://example.com  # SOCKS5 (e.g. SSH tunnel)
```

## Download / Resume

```bash
curl -O https://example.com/large.zip
curl -C - -O https://example.com/large.zip       # resume partial download
curl --limit-rate 1M -O https://example.com/large.zip  # rate limit
```

## Output Formatting

```bash
curl -s https://api.example.com | jq .           # pretty-print JSON (needs jq)
curl -s https://api.example.com | python3 -m json.tool  # stdlib alternative
curl -w "%{json}" -o /dev/null -s https://example.com   # write-out as JSON (curl 7.70+)
```

## Useful One-liners

```bash
# check HTTP status
curl -o /dev/null -s -w "%{http_code}" https://example.com

# get external IP
curl -s https://ifconfig.me

# test API with env var token
curl -s -H "Authorization: Bearer $API_TOKEN" https://api.example.com/me | jq .

# repeat request N times
for i in $(seq 1 5); do curl -s -o /dev/null -w "%{http_code}\n" https://example.com; done

# send to multiple URLs
curl https://example1.com https://example2.com   # sequential in one call
```
