#!/bin/bash

echo "🔧 Quick Fix: Installing terser for Vite build..."
echo "=============================================="

# Install terser
echo "📦 Installing terser..."
npm install --save-dev terser

# Try build again
echo "🔨 Rebuilding with terser..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "🚀 Starting PM2..."
    pm2 start ecosystem.config.cjs --env production
    pm2 save
    pm2 status
    
    echo ""
    echo "✅ Frontend is now running!"
    echo "🌐 Check: http://your-server:3002"
else
    echo "❌ Build failed. Trying with esbuild minifier..."
    
    # Update vite config to use esbuild instead of terser
    sed -i "s/minify: 'terser'/minify: 'esbuild'/g" vite.config.js
    
    echo "🔨 Rebuilding with esbuild..."
    npm run build
    
    if [ $? -eq 0 ]; then
        echo "✅ Build successful with esbuild!"
        pm2 start ecosystem.config.cjs --env production
        pm2 save
        pm2 status
    else
        echo "❌ Build still failed. Please check the errors above."
        exit 1
    fi
fi