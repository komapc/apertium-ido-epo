#!/bin/bash
# EC2 Setup Script for Ido-Esperanto APy Server
# Run this on your EC2 instance

set -e

echo "╔═══════════════════════════════════════════════════╗"
echo "║  EC2 APy Server Setup for Ido-Esperanto         ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker installed"
else
    echo "✅ Docker already installed"
fi

# Install Docker Compose
echo "📦 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed"
else
    echo "✅ Docker Compose already installed"
fi

# Install Git
echo "📦 Installing Git..."
sudo apt-get install -y git

# Create app directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/ido-epo-translator
sudo chown $USER:$USER /opt/ido-epo-translator
cd /opt/ido-epo-translator

# Clone repositories
echo "📥 Cloning Apertium repositories..."
if [ ! -d "apertium-ido" ]; then
    git clone https://github.com/apertium/apertium-ido.git
fi

if [ ! -d "apertium-epo" ]; then
    git clone https://github.com/apertium/apertium-epo.git
fi

if [ ! -d "apertium-ido-epo" ]; then
    git clone https://github.com/komapc/apertium-ido-epo.git
fi

# Create Dockerfile
echo "🐳 Creating Dockerfile..."
cat > Dockerfile << 'EOF'
FROM debian:bookworm-slim

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install dependencies
RUN apt-get update && apt-get install -y \
  curl ca-certificates gnupg python3 python3-pip git \
  build-essential autoconf automake libtool pkg-config \
  libxml2-dev libxml2-utils xsltproc flex libicu-dev \
  gawk cmake wget \
  && rm -rf /var/lib/apt/lists/*

# Install Apertium
RUN curl -sS https://apertium.projectjj.com/apt/install-nightly.sh | bash && \
  apt-get update && apt-get install -y apertium-all-dev && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /opt/apertium

# Copy language data
COPY apertium-ido /opt/apertium/apertium-ido
COPY apertium-epo /opt/apertium/apertium-epo
COPY apertium-ido-epo /opt/apertium/apertium-ido-epo

# Build languages
RUN cd apertium-ido && ./autogen.sh && ./configure && make -j$(nproc) && make install && ldconfig && \
    cd ../apertium-epo && ./autogen.sh && ./configure && make -j$(nproc) && make install && ldconfig && \
    cd ../apertium-ido-epo && autoreconf -fi && \
    ./configure --with-lang1=/opt/apertium/apertium-ido --with-lang2=/opt/apertium/apertium-epo && \
    make -j$(nproc) && make install && ldconfig

# Install APy
RUN git clone https://github.com/apertium/apertium-apy.git /opt/apertium-apy && \
    cd /opt/apertium-apy && \
    pip3 install --break-system-packages tornado bottle requests pyyaml lxml regex simplejson

EXPOSE 2737

WORKDIR /opt/apertium-apy
CMD ["python3", "apy.py", "-p", "2737", "-j1", "/usr/local/share/apertium/modes"]
EOF

# Create docker-compose.yml
echo "🐳 Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  apy-server:
    build: .
    container_name: ido-epo-apy
    ports:
      - "2737:2737"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:2737/listPairs"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
EOF

# Create update script
echo "📝 Creating update script..."
cat > update-dictionaries.sh << 'EOF'
#!/bin/bash
set -e

echo "🔄 Updating dictionaries..."

cd /opt/ido-epo-translator

# Pull latest changes
echo "📥 Pulling latest code..."
cd apertium-ido-epo && git pull origin main && cd ..
cd apertium-ido && git pull origin master && cd ..
cd apertium-epo && git pull origin master && cd ..

# Rebuild Docker image
echo "🐳 Rebuilding Docker image..."
docker-compose build --no-cache

# Restart service
echo "🔄 Restarting service..."
docker-compose down
docker-compose up -d

echo "✅ Update complete!"
EOF

chmod +x update-dictionaries.sh

# Create systemd service for auto-start
echo "⚙️ Setting up systemd service..."
sudo tee /etc/systemd/system/ido-epo-apy.service > /dev/null << EOF
[Unit]
Description=Ido-Esperanto APy Translation Server
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/ido-epo-translator
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ido-epo-apy.service

# Configure firewall
echo "🔥 Configuring firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 22/tcp
    sudo ufw allow 2737/tcp
    sudo ufw --force enable
    echo "✅ Firewall configured"
fi

# Build and start
echo "🏗️ Building Docker image (this will take 10-15 minutes)..."
docker-compose build

echo "🚀 Starting APy server..."
docker-compose up -d

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║          ✅ EC2 Setup Complete! ✅               ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
echo "📋 Next steps:"
echo "1. Wait for build to complete: docker-compose logs -f"
echo "2. Test translation: curl http://localhost:2737/listPairs"
echo "3. Get public IP: curl ifconfig.me"
echo "4. Your EC2 IP: \$(curl -s ifconfig.me)"
echo "5. Update Cloudflare Pages env: APY_SERVER_URL=http://\$(curl -s ifconfig.me):2737"
echo ""
echo "🔄 To update dictionaries: ./update-dictionaries.sh"
echo ""

