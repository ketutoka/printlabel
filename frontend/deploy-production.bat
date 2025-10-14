@echo off
echo 🚀 Setting up Print Label Frontend for Production...
echo ==================================================

REM Create logs directory
if not exist "logs" mkdir logs

REM Install dependencies
echo 📦 Installing dependencies...
npm ci --production=false

REM Build for production
echo 🔨 Building for production...
npm run build

REM Check if PM2 is installed globally
pm2 --version >nul 2>&1
if errorlevel 1 (
    echo ❌ PM2 is not installed globally
    echo Please install PM2 globally: npm install -g pm2
    pause
    exit /b 1
)

REM Stop existing process if running
echo 🛑 Stopping existing processes...
pm2 stop printlabel-frontend 2>nul
pm2 delete printlabel-frontend 2>nul

REM Start with PM2
echo 🚀 Starting with PM2...
pm2 start ecosystem.config.cjs --env production

REM Save PM2 configuration
echo 💾 Saving PM2 configuration...
pm2 save

REM Show status
echo 📊 PM2 Status:
pm2 status

echo.
echo ✅ Frontend is now running in production mode!
echo 🌐 Frontend URL: http://your-server:3002
echo.
echo Useful PM2 commands:
echo   pm2 status                    - Show status
echo   pm2 logs printlabel-frontend  - Show logs
echo   pm2 restart printlabel-frontend - Restart app
echo   pm2 stop printlabel-frontend  - Stop app
echo   pm2 delete printlabel-frontend - Delete app
echo.
pause