#!/bin/bash

echo "🚀 Setting up Print Label Frontend for Production..."
echo "=================================================="

# Create logs directory
mkdir -p logs

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --production=false

# Install terser for minification (if not already installed)
echo "🔧 Installing terser for minification..."
npm install --save-dev terser

# Build for production
echo "🔨 Building for production..."
npm run build

# Check if PM2 is installed globally
if ! command -v pm2 &> /dev/null; then
    echo "❌ PM2 is not installed globally"
    echo "Please install PM2 globally: npm install -g pm2"
    exit 1
fi

# Stop existing process if running
echo "🛑 Stopping existing processes..."
pm2 stop printlabel-frontend 2>/dev/null || true
pm2 delete printlabel-frontend 2>/dev/null || true

# Start with PM2
echo "🚀 Starting with PM2..."
pm2 start ecosystem.config.cjs --env production

# Save PM2 configuration
echo "💾 Saving PM2 configuration..."
pm2 save

# Show status
echo "📊 PM2 Status:"
pm2 status

echo "✅ Frontend is now running in production mode!"
echo "🌐 Frontend URL: http://your-server:3002"
echo ""
echo "Useful PM2 commands:"
echo "  pm2 status                    - Show status"
echo "  pm2 logs printlabel-frontend  - Show logs"
echo "  pm2 restart printlabel-frontend - Restart app"
echo "  pm2 stop printlabel-frontend  - Stop app"
echo "  pm2 delete printlabel-frontend - Delete app"