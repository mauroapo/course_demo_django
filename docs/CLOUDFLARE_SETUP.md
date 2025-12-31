# Cloudflare + HTTPS Setup Guide

## 📋 Overview

This guide will help you configure Cloudflare to provide HTTPS for your Django application running on VPS.

**Architecture:**
```
User → Cloudflare (HTTPS) → Your VPS (HTTP Port 80) → Nginx → Django
```

---

## 🚀 Step 1: Update VPS Configuration

### 1.1 Update docker-compose.yml

Already done! Port changed from `9000:80` to `80:80`.

### 1.2 Deploy to VPS

```bash
# Commit changes
git add docker-compose.yml
git commit -m "Change nginx port to 80 for Cloudflare"
git push origin main

# Or manually on VPS:
ssh -p YOUR_PORT YOUR_USER@80.91.86.135
cd ~/Invisibilidown
git pull origin main
docker compose down
docker compose up -d
```

### 1.3 Open Port 80 on VPS Firewall

```bash
# SSH to VPS
ssh -p YOUR_PORT YOUR_USER@80.91.86.135

# Allow port 80
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp  # For future direct HTTPS if needed
sudo ufw reload

# Verify
sudo ufw status
```

---

## 🌐 Step 2: Configure Domain in Cloudflare

### 2.1 Add Your Domain to Cloudflare

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Click **"Add a Site"**
3. Enter your domain (e.g., `invisibilidown.com`)
4. Select **Free Plan**
5. Click **"Continue"**

### 2.2 Update Nameservers

Cloudflare will provide nameservers like:
```
ns1.cloudflare.com
ns2.cloudflare.com
```

**Update at your domain registrar:**
1. Go to your domain registrar (GoDaddy, Namecheap, etc.)
2. Find DNS/Nameserver settings
3. Replace existing nameservers with Cloudflare's
4. Save changes (can take 24-48 hours to propagate)

---

## 🔧 Step 3: Configure DNS Records

In Cloudflare Dashboard → DNS → Records:

### Add A Record:

| Type | Name | Content | Proxy Status | TTL |
|------|------|---------|--------------|-----|
| A | @ | 80.91.86.135 | ✅ Proxied | Auto |
| A | www | 80.91.86.135 | ✅ Proxied | Auto |

**Important:** Make sure **Proxy status is ON** (orange cloud icon) to enable Cloudflare's SSL.

---

## 🔒 Step 4: Configure SSL/TLS

### 4.1 SSL/TLS Settings

Go to **SSL/TLS** → **Overview**:

**Select:** `Flexible` (for now)

**SSL/TLS encryption modes:**
- ✅ **Flexible**: Cloudflare ↔ User (HTTPS), Cloudflare ↔ VPS (HTTP)
- ⚠️ **Full**: Requires SSL on VPS (we'll upgrade to this later)
- ⚠️ **Full (strict)**: Requires valid SSL certificate on VPS

### 4.2 Always Use HTTPS

Go to **SSL/TLS** → **Edge Certificates**:

Enable:
- ✅ **Always Use HTTPS**
- ✅ **Automatic HTTPS Rewrites**
- ✅ **Minimum TLS Version**: TLS 1.2

---

## ⚙️ Step 5: Update Django Settings

### 5.1 Update ALLOWED_HOSTS

Add your domain to `ALLOWED_HOSTS`:

**On VPS** (`~/Invisibilidown/.env`):
```env
ALLOWED_HOSTS=localhost,127.0.0.1,80.91.86.135,invisibilidown.com,www.invisibilidown.com
```

### 5.2 Update CSRF_TRUSTED_ORIGINS

**On VPS** (`~/Invisibilidown/.env`):
```env
CSRF_TRUSTED_ORIGINS=https://invisibilidown.com,https://www.invisibilidown.com
```

Or update `settings.py`:
```python
CSRF_TRUSTED_ORIGINS = [
    "https://invisibilidown.com",
    "https://www.invisibilidown.com",
]
```

### 5.3 Configure Cloudflare Headers

Add to `settings.py`:
```python
# Cloudflare settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
```

### 5.4 Restart Containers

```bash
# On VPS
cd ~/Invisibilidown
docker compose restart web
```

---

## 🎯 Step 6: Configure Cloudflare Page Rules (Optional)

Go to **Rules** → **Page Rules**:

### Rule 1: Force HTTPS
- **URL:** `http://*invisibilidown.com/*`
- **Setting:** Always Use HTTPS

### Rule 2: WWW Redirect
- **URL:** `www.invisibilidown.com/*`
- **Setting:** Forwarding URL (301 - Permanent Redirect)
- **Destination:** `https://invisibilidown.com/$1`

---

## 🚀 Step 7: Performance Optimization

### 7.1 Enable Caching

Go to **Caching** → **Configuration**:
- **Caching Level:** Standard
- **Browser Cache TTL:** 4 hours

### 7.2 Enable Auto Minify

Go to **Speed** → **Optimization**:
- ✅ Auto Minify: JavaScript
- ✅ Auto Minify: CSS
- ✅ Auto Minify: HTML

### 7.3 Enable Brotli Compression

Go to **Speed** → **Optimization**:
- ✅ Brotli

---

## ✅ Step 8: Verify Setup

### 8.1 Test DNS Propagation

```bash
# Check if DNS is pointing to Cloudflare
nslookup invisibilidown.com

# Should show Cloudflare IPs (104.x.x.x or similar)
```

### 8.2 Test HTTPS

Open in browser:
```
https://invisibilidown.com
https://www.invisibilidown.com
```

### 8.3 Check SSL Certificate

Click the padlock icon in browser → Should show:
- **Issued by:** Cloudflare Inc ECC CA-3
- **Valid for:** invisibilidown.com

### 8.4 Test Stripe Webhook

Update Stripe webhook URL to:
```
https://invisibilidown.com/checkout/webhook/stripe/
```

---

## 🔐 Step 9: Upgrade to Full SSL (Recommended)

For better security, upgrade from Flexible to Full SSL:

### 9.1 Generate SSL Certificate on VPS

```bash
# SSH to VPS
ssh -p YOUR_PORT YOUR_USER@80.91.86.135

# Install Certbot
sudo apt update
sudo apt install certbot

# Generate self-signed certificate (for Cloudflare Full mode)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt \
  -subj "/CN=invisibilidown.com"
```

### 9.2 Update Nginx Configuration

Create `nginx/nginx-ssl.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        listen 443 ssl;
        server_name invisibilidown.com www.invisibilidown.com;

        ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
        ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

        client_max_body_size 100M;

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }
    }
}
```

### 9.3 Update docker-compose.yml

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx/nginx-ssl.conf:/etc/nginx/nginx.conf:ro
    - /etc/ssl/certs/nginx-selfsigned.crt:/etc/ssl/certs/nginx-selfsigned.crt:ro
    - /etc/ssl/private/nginx-selfsigned.key:/etc/ssl/private/nginx-selfsigned.key:ro
    - static_volume:/app/staticfiles:ro
    - media_volume:/app/media:ro
  depends_on:
    - web
```

### 9.4 Change Cloudflare SSL Mode

Go to **SSL/TLS** → **Overview**:
- Change from `Flexible` to `Full`

---

## 📊 Monitoring & Troubleshooting

### Check Cloudflare Analytics

Go to **Analytics & Logs** → **Traffic**

### Common Issues

**Issue 1: "Too many redirects"**
- **Cause:** SSL mode mismatch
- **Fix:** Use Flexible mode if VPS has no SSL

**Issue 2: "Connection timed out"**
- **Cause:** Port 80 blocked on VPS
- **Fix:** `sudo ufw allow 80/tcp`

**Issue 3: "Invalid CSRF token"**
- **Cause:** Missing CSRF_TRUSTED_ORIGINS
- **Fix:** Add domain to CSRF_TRUSTED_ORIGINS

---

## 🎉 Final Checklist

- ✅ Domain added to Cloudflare
- ✅ Nameservers updated
- ✅ DNS A records created (proxied)
- ✅ SSL/TLS set to Flexible
- ✅ Always Use HTTPS enabled
- ✅ Port 80 open on VPS
- ✅ ALLOWED_HOSTS updated
- ✅ CSRF_TRUSTED_ORIGINS updated
- ✅ Application accessible via HTTPS
- ✅ Stripe webhook URL updated

---

## 🔗 Useful Links

- [Cloudflare Dashboard](https://dash.cloudflare.com/)
- [Cloudflare SSL Guide](https://developers.cloudflare.com/ssl/)
- [Django Security Settings](https://docs.djangoproject.com/en/4.2/topics/security/)

**Your site is now live with HTTPS!** 🚀
