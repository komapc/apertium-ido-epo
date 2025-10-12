# EC2 Setup Script for Ido-Esperanto Translator

## Prerequisites
- Ubuntu 22.04 LTS EC2 instance (t3.micro or larger)
- SSH access with your key
- Security group configured with ports 22, 80, 2737 open

## Quick Setup Script

Run this script on a fresh Ubuntu EC2 instance:

```bash
#!/bin/bash
set -euo pipefail

echo "🚀 Setting up Ido-Esperanto Translator on EC2..."

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo apt-get install -y docker-compose-plugin

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install nginx
sudo apt-get install -y nginx

# Install git
sudo apt-get install -y git

# Clone the project
cd /home/ubuntu
git clone https://github.com/komapc/apertium-ido-epo.git apertium-build
git clone https://github.com/komapc/ido-epo-translator-web.git

# Setup React app
cd ido-epo-translator-web
npm install
npm run build

# Start React app server
nohup serve -s dist -l 3000 > serve.log 2>&1 &

# Configure nginx
sudo tee /etc/nginx/sites-available/ido-translator > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;
    
    # Serve React app
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Proxy API requests to APy server
    location /api/ {
        proxy_pass http://localhost:2737/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/ido-translator /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# Setup Docker container
cd /home/ubuntu/apertium-build
sed -i 's|context: ../..|context: .|' docker-compose.yml
sed -i 's|dockerfile: ido-epo-translator-web/apy-server/Dockerfile|dockerfile: Dockerfile|' docker-compose.yml

# Build and start Docker container
docker compose build --no-cache
docker compose up -d

# Wait for container to start
sleep 30

# Fix missing binary files
docker exec ido-epo-apy bash -c 'cp /usr/local/share/apertium/apertium-ido/ido.automorf.bin /usr/local/share/apertium/apertium-ido-epo/ido-epo.automorf.bin'
docker exec ido-epo-apy bash -c 'cp /usr/local/share/apertium/apertium-epo/epo.autopgen.bin /usr/local/share/apertium/apertium-ido-epo/ido-epo.autopgen.bin'
docker exec ido-epo-apy bash -c 'touch /usr/local/share/apertium/apertium-ido-epo/epo-ido.autopgen.bin'

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me)

echo "✅ Setup complete!"
echo "🌐 Your translator is available at: http://$PUBLIC_IP"
echo "📊 API health check: http://$PUBLIC_IP/api/listPairs"
echo ""
echo "🔧 To test translation:"
echo "curl -X POST http://$PUBLIC_IP/api/translate \\"
echo "  -H 'Content-Type: application/x-www-form-urlencoded' \\"
echo "  -d 'q=La hundo esas bela&langpair=ido|epo'"
```

## Manual Steps After Running Script

1. **Configure Security Group:**
   - Port 22 (SSH): 0.0.0.0/0
   - Port 80 (HTTP): 0.0.0.0/0  
   - Port 2737 (APy API): 0.0.0.0/0

2. **Test the installation:**
   ```bash
   # Test React app
   curl http://$(curl -s ifconfig.me)
   
   # Test API
   curl http://$(curl -s ifconfig.me)/api/listPairs
   
   # Test translation
   curl -X POST http://$(curl -s ifconfig.me)/api/translate \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "q=La hundo esas bela&langpair=ido|epo"
   ```

## Troubleshooting

### If translation fails:
```bash
# Check container logs
docker logs ido-epo-apy

# Restart container
docker compose restart

# Check binary files
docker exec ido-epo-apy ls -la /usr/local/share/apertium/apertium-ido-epo/*.bin
```

### If React app doesn't load:
```bash
# Check if serve is running
ps aux | grep serve

# Restart serve
pkill -f serve
cd /home/ubuntu/ido-epo-translator-web
nohup serve -s dist -l 3000 > serve.log 2>&1 &
```

### If nginx fails:
```bash
# Check nginx status
sudo systemctl status nginx

# Test configuration
sudo nginx -t

# Reload configuration
sudo systemctl reload nginx
```

## File Structure After Setup

```
/home/ubuntu/
├── apertium-build/           # Apertium language data
│   ├── apertium-ido/        # Ido language
│   ├── apertium-epo/        # Esperanto language  
│   ├── apertium-ido-epo/    # Translation pairs
│   └── docker-compose.yml   # Docker configuration
└── ido-epo-translator-web/  # React web application
    ├── dist/                # Built React app
    ├── src/                 # Source code
    └── package.json         # Dependencies
```

## Services Running

- **React App:** Port 3000 (served by nginx on port 80)
- **APy API:** Port 2737 (Docker container)
- **Nginx:** Port 80 (reverse proxy)

## Updates

To update the system:

```bash
# Update React app
cd /home/ubuntu/ido-epo-translator-web
git pull
npm run build
pkill -f serve
nohup serve -s dist -l 3000 > serve.log 2>&1 &

# Update Docker container
cd /home/ubuntu/apertium-build
docker compose down
docker compose build --no-cache
docker compose up -d
# Re-run binary file fixes if needed
```
