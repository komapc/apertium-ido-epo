# Rebuild Webhook Setup Guide

## Overview

The rebuild webhook allows the web UI to trigger dictionary rebuilds on the EC2 server without SSH access.

## Architecture

```
Cloudflare Worker → Nginx (port 80) → Webhook Server (port 9100) → Docker exec rebuild.sh
```

## Setup Instructions

### 1. Install Webhook Service on EC2

SSH into your EC2 instance:

```bash
ssh -i ~/.ssh/apertium.pem ubuntu@52.211.137.158
```

Copy the webhook server files to EC2:

```bash
# From your local machine (in ido-epo-translator-web directory)
scp -i ~/.ssh/apertium.pem webhook-server.js ubuntu@52.211.137.158:/tmp/
scp -i ~/.ssh/apertium.pem webhook-server.service ubuntu@52.211.137.158:/tmp/
```

On EC2, install and configure:

```bash
# Move webhook server to application directory
sudo mv /tmp/webhook-server.js /opt/ido-epo-translator/
sudo chmod +x /opt/ido-epo-translator/webhook-server.js

# Install Node.js if not already installed
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install systemd service
sudo mv /tmp/webhook-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable webhook-server
sudo systemctl start webhook-server

# Check status
sudo systemctl status webhook-server
```

### 2. Configure Nginx Proxy

Create or update Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/apy.conf
```

Add the rebuild endpoint:

```nginx
server {
  listen 80 default_server;
  listen [::]:80 default_server;
  server_name _;
  
  # Webhook endpoint
  location = /rebuild {
    proxy_pass http://127.0.0.1:9100/rebuild;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
  
  # APy server
  location / {
    proxy_pass http://127.0.0.1:2737;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }
}
```

Enable and reload Nginx:

```bash
sudo ln -sf /etc/nginx/sites-available/apy.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 3. Configure Cloudflare Worker Environment Variables

Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Workers & Pages → Your Worker → Settings → Variables

Add these environment variables:

- **Variable name:** `REBUILD_WEBHOOK_URL`
  - **Value:** `http://ec2-52-211-137-158.eu-west-1.compute.amazonaws.com/rebuild`
  - **Type:** Plaintext

- **Variable name:** `REBUILD_SHARED_SECRET` (optional but recommended)
  - **Value:** Generate a secure random string: `openssl rand -hex 32`
  - **Type:** Secret

If you set `REBUILD_SHARED_SECRET`, also add it to the EC2 webhook service:

```bash
# On EC2
sudo systemctl edit webhook-server
```

Add in the override file:

```ini
[Service]
Environment="REBUILD_SHARED_SECRET=your-secret-here"
```

Then restart:

```bash
sudo systemctl restart webhook-server
```

### 4. Update Docker Container Name

The webhook server expects the container to be named `ido-epo-apy`. Verify:

```bash
docker ps --format "{{.Names}}"
```

If the name is different, either:
- Rename in `docker-compose.yml` and recreate the container, OR
- Update `webhook-server.js` line 32 with the correct container name

### 5. Test the Setup

Test locally on EC2:

```bash
curl -X POST http://localhost:9100/rebuild
```

Test via Nginx:

```bash
curl -X POST http://localhost/rebuild
```

Test externally from your machine:

```bash
curl -X POST http://ec2-52-211-137-158.eu-west-1.compute.amazonaws.com/rebuild
```

All should return JSON with status "accepted" and rebuild logs.

### 6. Test from Web UI

Open your translator web app and click the **Rebuild** button. You should see:
- Status changes to "running"
- Success message with build logs
- No errors

## Troubleshooting

### Webhook server won't start

Check logs:
```bash
sudo journalctl -u webhook-server -f
```

Common issues:
- Node.js not installed: `node --version`
- Port 9100 already in use: `sudo lsof -i :9100`
- Permissions: `sudo chown ubuntu:ubuntu /opt/ido-epo-translator/webhook-server.js`

### Rebuild fails

Check if Docker container is running:
```bash
docker ps
```

Check webhook logs:
```bash
sudo journalctl -u webhook-server -n 100
```

Test rebuild script manually:
```bash
docker exec ido-epo-apy /opt/apertium/rebuild.sh
```

### 401 Unauthorized

The shared secret doesn't match. Check:
- Cloudflare Worker has `REBUILD_SHARED_SECRET` set
- EC2 webhook service has same secret in environment
- Secrets match exactly (no extra whitespace)

### 404 Not Found from EC2

Nginx isn't proxying correctly:
```bash
sudo nginx -t
sudo systemctl status nginx
sudo journalctl -u nginx -n 50
```

### Web UI shows "Rebuild webhook URL not configured"

The Cloudflare Worker doesn't have `REBUILD_WEBHOOK_URL` set:
- Go to Dashboard → Workers & Pages → Settings → Variables
- Add `REBUILD_WEBHOOK_URL`
- Redeploy Worker or wait a few minutes for changes to propagate

## Security Notes

1. **Use HTTPS in production:** The current setup uses HTTP. For production, configure SSL/TLS on EC2 or use Cloudflare Tunnel.

2. **Restrict access:** Consider adding IP whitelisting in Nginx to only allow requests from Cloudflare IPs.

3. **Use shared secret:** Always set `REBUILD_SHARED_SECRET` to prevent unauthorized rebuilds.

4. **Monitor logs:** Regularly check rebuild logs:
   ```bash
   sudo tail -f /var/log/apertium-rebuild.log
   sudo journalctl -u webhook-server -f
   ```

## Monitoring

Check webhook service health:
```bash
# Service status
sudo systemctl status webhook-server

# Recent logs
sudo journalctl -u webhook-server -n 50

# Rebuild log
sudo tail -50 /var/log/apertium-rebuild.log

# Test endpoint
curl http://localhost:9100/rebuild
```

