# Nginx Cheat Sheet

## Service & CLI
```bash
nginx -t                              # test config syntax (do this before every reload)
nginx -s reload                       # reload config, no dropped connections
nginx -s quit                         # graceful shutdown
nginx -T                              # dump the full effective config
nginx -v                              # version
systemctl reload nginx                # reload via systemd
systemctl status nginx                # is it running?
tail -f /var/log/nginx/error.log      # watch errors
tail -f /var/log/nginx/access.log     # watch requests
```

## File layout (Debian/Ubuntu)
```bash
/etc/nginx/nginx.conf                 # main config
/etc/nginx/sites-available/           # one file per site (edit here)
/etc/nginx/sites-enabled/             # symlinks to active sites
ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/   # enable a site
```

## Minimal static site
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example;
    index index.html;

    location / {
        try_files $uri $uri/ =404;     # serve file, dir, else 404
    }
}
```

## Reverse proxy
```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;        # upstream app
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
}
```

## WebSocket proxy
```nginx
location /ws {
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";        # required for WS
}
```

## SSL / TLS (HTTPS)
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    location / { proxy_pass http://127.0.0.1:8000; }
}

# Redirect all HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```
```bash
certbot --nginx -d example.com -d www.example.com   # auto-provision Let's Encrypt cert
```

## Upstream / load balancing
```nginx
upstream backend {
    # default = round robin
    least_conn;                       # or: ip_hash (sticky by client IP)
    server 127.0.0.1:8001;
    server 127.0.0.1:8002 weight=2;   # gets 2x traffic
    server 127.0.0.1:8003 backup;     # only used when others are down
}

server {
    listen 80;
    location / { proxy_pass http://backend; }
}
```

## Rate limiting
```nginx
# in http {} context:
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;   # 10 req/s per IP

server {
    location /api/ {
        limit_req zone=api burst=20 nodelay;   # allow short bursts of 20
        proxy_pass http://backend;
    }
}
```

## Gzip & static caching
```nginx
gzip on;
gzip_types text/plain application/json application/javascript text/css;
gzip_min_length 1024;

location ~* \.(jpg|png|css|js|woff2)$ {
    expires 30d;                       # browser cache
    add_header Cache-Control "public, immutable";
}
```

## Useful snippets
```nginx
client_max_body_size 50m;              # allow large uploads (default is 1m)
add_header X-Frame-Options "SAMEORIGIN";
location = /health { return 200 "ok\n"; access_log off; }   # cheap healthcheck
```
