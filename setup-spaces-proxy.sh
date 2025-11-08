#!/bin/bash
# Setup script for spaces.pime.ai reverse proxy
# Run this on the VM: bash setup-spaces-proxy.sh

set -e

echo "🚀 Setting up spaces.pime.ai reverse proxy..."
echo ""

# 1. Pull latest code with Nginx config
echo "📥 Pulling latest code..."
cd /home/samihalawa/ai-manus
git pull origin main

# 2. Check for existing wildcard certificate
echo ""
echo "🔒 Checking SSL certificates..."
if sudo certbot certificates | grep -q "*.pime.ai"; then
    echo "✅ Wildcard certificate for *.pime.ai already exists"
    CERT_EXISTS=true
else
    echo "⚠️  No wildcard certificate found"
    CERT_EXISTS=false
fi

# 3. Install Nginx config
echo ""
echo "📝 Installing Nginx configuration..."
sudo cp nginx-spaces-proxy.conf /etc/nginx/sites-available/spaces-proxy

# Create symlink if it doesn't exist
if [ ! -L /etc/nginx/sites-enabled/spaces-proxy ]; then
    sudo ln -s /etc/nginx/sites-available/spaces-proxy /etc/nginx/sites-enabled/spaces-proxy
    echo "✅ Created symlink in sites-enabled"
else
    echo "✅ Symlink already exists"
fi

# 4. Update certificate path if needed
if [ "$CERT_EXISTS" = true ]; then
    echo ""
    echo "📝 Updating certificate paths in Nginx config..."
    # Check if we need to use the wildcard cert
    if sudo ls /etc/letsencrypt/live/*.pime.ai/fullchain.pem 2>/dev/null; then
        CERT_DIR=$(sudo ls -d /etc/letsencrypt/live/*.pime.ai | head -1)
        echo "Using certificate: $CERT_DIR"
    elif sudo ls /etc/letsencrypt/live/pime.ai/fullchain.pem 2>/dev/null; then
        CERT_DIR="/etc/letsencrypt/live/pime.ai"
        echo "Using certificate: $CERT_DIR"
    fi
else
    echo ""
    echo "⚠️  WARNING: No SSL certificate found!"
    echo "You need to obtain a wildcard certificate first:"
    echo ""
    echo "Option 1 - Wildcard cert (recommended):"
    echo "  sudo certbot certonly --manual --preferred-challenges dns -d '*.pime.ai' -d pime.ai"
    echo ""
    echo "Option 2 - Specific subdomain:"
    echo "  sudo certbot certonly --nginx -d '*.spaces.pime.ai' -d spaces.pime.ai"
    echo ""
    echo "After obtaining the certificate, run this script again."
    exit 1
fi

# 5. Test Nginx configuration
echo ""
echo "🧪 Testing Nginx configuration..."
if sudo nginx -t; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration has errors"
    exit 1
fi

# 6. Reload Nginx
echo ""
echo "♻️  Reloading Nginx..."
sudo systemctl reload nginx

# 7. Rebuild and restart Docker containers
echo ""
echo "🐳 Rebuilding Docker containers..."
docker-compose build backend sandbox

echo ""
echo "♻️  Restarting containers..."
docker-compose up -d

# 8. Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 5

# 9. Test the setup
echo ""
echo "🧪 Testing the deployment..."
echo ""

# Check if backend is running
if docker-compose ps | grep -q "backend.*Up"; then
    echo "✅ Backend container is running"
else
    echo "❌ Backend container is not running"
fi

# Check Nginx is listening
if sudo netstat -tuln | grep -q ":443.*LISTEN"; then
    echo "✅ Nginx is listening on port 443"
else
    echo "❌ Nginx is not listening on port 443"
fi

# Check DNS resolution
echo ""
echo "🌐 Testing DNS resolution..."
if nslookup test123-8888.spaces.pime.ai | grep -q "pime.ai"; then
    echo "✅ DNS wildcard is resolving correctly"
else
    echo "⚠️  DNS may not be propagated yet (this can take a few minutes)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test with a simple HTTP server:"
echo "   docker exec -it manus-backend python3 -m http.server 8888 --bind 0.0.0.0"
echo ""
echo "2. Then test the URL:"
echo "   curl https://test123-8888.spaces.pime.ai"
echo ""
echo "3. Deploy a Gradio app via Manus UI to test ExposeTool"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f backend | grep cloudflared"
echo "   sudo tail -f /var/log/nginx/spaces-access.log"
echo "   sudo tail -f /var/log/nginx/spaces-error.log"
