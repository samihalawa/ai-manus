# ExposeTool Fix - Deployment Guide

## Overview

This fix improves ExposeTool to generate **real working public URLs** for exposed services using two methods:

1. **Primary:** Real cloudflared tunnels (`*.trycloudflare.com`)
2. **Fallback:** Reverse proxy on `spaces.pime.ai`

---

## Changes Made

### 1. Backend Code Fix (`backend/app/domain/services/tools/expose.py`)

**Improvements:**
- ✅ Read from **both stdout AND stderr** to capture cloudflared URL
- ✅ Increased timeout from 10s to 20s for tunnel establishment
- ✅ Added concurrent stream reading for better reliability
- ✅ Added debug logging for troubleshooting
- ✅ Changed fallback domain from `apps.pime.ai` to `spaces.pime.ai`

**URL Patterns:**
- **cloudflared:** `https://{random}.trycloudflare.com` (real tunnel)
- **Fallback:** `https://{id}-{port}.spaces.pime.ai` (reverse proxy)

### 2. Nginx Reverse Proxy Configuration (`nginx-spaces-proxy.conf`)

**Features:**
- Dynamic subdomain routing based on pattern `{id}-{port}.spaces.pime.ai`
- SSL/TLS support with wildcard certificate
- WebSocket support for real-time apps
- CORS headers for web applications
- Proper error handling and timeouts

---

## Deployment Instructions

### Step 1: Update Backend Code

The backend code has been updated in `backend/app/domain/services/tools/expose.py`. Deploy this to your VM:

```bash
# On VM
cd /home/samihalawa/ai-manus
git pull origin main
docker-compose build backend
docker-compose up -d
```

### Step 2: Configure DNS for *.spaces.pime.ai

Add a wildcard DNS record in your DNS provider (Cloudflare):

**Type:** `A` record
**Name:** `*.spaces`
**Value:** `34.59.167.52` (your VM IP)
**Proxy:** Disabled (orange cloud OFF)

**Alternative using CNAME:**
**Type:** `CNAME` record
**Name:** `*.spaces`
**Value:** `pime.ai`
**Proxy:** Disabled

### Step 3: Install SSL Certificate for *.spaces.pime.ai

```bash
# On VM
sudo certbot certonly --nginx -d *.spaces.pime.ai -d spaces.pime.ai

# Or use existing wildcard cert if you have one
sudo certbot certonly --manual --preferred-challenges dns -d *.pime.ai
```

**Note:** If you already have a wildcard certificate for `*.pime.ai`, you can use that.

### Step 4: Deploy Nginx Configuration

```bash
# Copy configuration to VM
scp nginx-spaces-proxy.conf samihalawa@34.59.167.52:/tmp/

# On VM, install the configuration
ssh samihalawa@34.59.167.52
sudo mv /tmp/nginx-spaces-proxy.conf /etc/nginx/sites-available/spaces-proxy
sudo ln -s /etc/nginx/sites-available/spaces-proxy /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# If test passes, reload Nginx
sudo systemctl reload nginx
```

### Step 5: Verify Deployment

Test that the reverse proxy works:

```bash
# Start a simple test server on port 8888
python3 -m http.server 8888 --bind 0.0.0.0

# Test URL (replace test123 with any ID)
curl https://test123-8888.spaces.pime.ai
```

---

## Testing the Fixed ExposeTool

### Test 1: Verify cloudflared Tunnel Works

1. Deploy a Gradio app via Manus UI
2. Check the exposed URL format
3. Verify it's a real `*.trycloudflare.com` URL
4. Navigate to the URL and confirm it works

**Expected Result:**
```
✅ Successfully exposed port 7860 using cloudflared
🌐 Public URL: https://abc123xyz.trycloudflare.com
```

### Test 2: Verify Fallback Works (if cloudflared unavailable)

If cloudflared isn't available, the system should use spaces.pime.ai:

**Expected Result:**
```
✅ Exposed port 7860 via reverse proxy
🔗 Public URL: https://xyz789-7860.spaces.pime.ai
⚠️  Cloudflared not available - using reverse proxy fallback
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Manus Agent                              │
│                                                              │
│  ExposeTool.expose_port(7860)                               │
│         │                                                    │
│         ├──── Try cloudflared ────────────────────┐         │
│         │                                          │         │
│         │                                          ▼         │
│         │                                   [cloudflared]    │
│         │                                          │         │
│         │                                          ▼         │
│         │                              *.trycloudflare.com   │
│         │                                    (REAL TUNNEL)   │
│         │                                                    │
│         └──── Fallback if failed ────────────────┐          │
│                                                   │          │
│                                                   ▼          │
│                                        spaces.pime.ai        │
│                                        (REVERSE PROXY)       │
└─────────────────────────────────────────────────────────────┘
                                                   │
                                                   ▼
                                            ┌─────────────┐
                                            │    Nginx    │
                                            │  Reverse    │
                                            │   Proxy     │
                                            └─────────────┘
                                                   │
                                                   ▼
                                         localhost:7860
                                       (Gradio App in Sandbox)
```

---

## Troubleshooting

### Issue: cloudflared URLs still not working

**Check logs:**
```bash
# On VM, check backend logs
docker-compose logs -f backend | grep cloudflared
```

**Verify cloudflared is installed in sandbox:**
```bash
docker exec -it manus-sandbox-{id} which cloudflared
```

**Install cloudflared if missing:**
```bash
# Add to backend/Dockerfile and sandbox/Dockerfile
RUN wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && \
    dpkg -i cloudflared-linux-amd64.deb && \
    rm cloudflared-linux-amd64.deb
```

### Issue: spaces.pime.ai URLs return SSL errors

**Check SSL certificate:**
```bash
sudo certbot certificates | grep spaces.pime.ai
```

**Check Nginx configuration:**
```bash
sudo nginx -t
sudo systemctl status nginx
```

### Issue: spaces.pime.ai URLs return 502/503

**Verify application is bound to 0.0.0.0:**
```python
# Correct:
demo.launch(server_name="0.0.0.0", server_port=7860)

# Wrong:
demo.launch(server_name="localhost", server_port=7860)
```

**Check if port is actually listening:**
```bash
docker exec manus-sandbox-{id} netstat -tuln | grep 7860
```

---

## Rollback Plan

If issues occur, rollback to previous version:

```bash
# On VM
cd /home/samihalawa/ai-manus
git checkout HEAD~1 backend/app/domain/services/tools/expose.py
docker-compose build backend
docker-compose up -d

# Remove Nginx configuration
sudo rm /etc/nginx/sites-enabled/spaces-proxy
sudo systemctl reload nginx
```

---

## Success Criteria

- ✅ cloudflared generates real `*.trycloudflare.com` URLs
- ✅ URLs are publicly accessible and return app content
- ✅ Fallback to `spaces.pime.ai` works when cloudflared unavailable
- ✅ No more mock `apps.pime.ai` URLs
- ✅ Gradio/Streamlit/Flask apps can be shared externally

---

## Next Steps

1. Deploy backend code changes
2. Configure DNS for *.spaces.pime.ai
3. Install SSL certificate
4. Deploy Nginx configuration
5. Test with Gradio app deployment
6. Monitor logs for any issues
7. Update documentation with final URL patterns
