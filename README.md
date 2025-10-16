# Print Label Application

## Aplikasi Cetak Label Paket untuk Thermal Printer 58mm

### Fitur
- Register User (nama/email/no hp/password)
- Login (email/password) 
- Reset password dengan kode email
- Cetak Label Sederhana dengan QR Code otomatis
- Cetak Label Pengiriman lengkap (pengirim → penerima)
- History gabungan untuk semua jenis label
- Preview dan print untuk thermal printer 58mm
- Kode resi opsional (bisa dikosongkan)
- Logout

### Teknologi
- **Backend**: Python FastAPI
- **Frontend**: Vue.js 3
- **Database**: PostgreSQL
- **Printer**: Thermal Printer 58mm

## Setup Development

### Backend (Python FastAPI)
```bash
cd backend

# Option 1: Quick setup (Windows)
setup.bat
run-server.bat

# Option 2: Manual setup
python -m venv .venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your database settings

# Start server (choose one):
python start.py                    # Recommended - with environment checks
uvicorn main:app --reload --port 8002  # Direct uvicorn
run-server.bat                     # Using batch file
```

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev  # Runs on port 3002
```

## Production Deployment

### Frontend Production Setup
```bash
cd frontend

# Install PM2 globally (if not installed)
npm install -g pm2

# Option 1: Automated deployment
deploy-production.bat    # Windows
# or
bash deploy-production.sh  # Linux

# Option 2: Manual deployment
npm ci --production=false
npm run build
pm2 start ecosystem.config.cjs --env production
pm2 save

# Useful PM2 commands
pm2 status                    # Show status
pm2 logs printlabel-frontend  # Show logs
pm2 restart printlabel-frontend # Restart
pm2 stop printlabel-frontend  # Stop
```

### Environment Configuration
Create `.env.production` and update:
```
VITE_API_BASE_URL=/api
VITE_APP_TITLE=Print Label - Production
VITE_APP_ENV=production
```

### Nginx Setup
Example nginx configuration for port 8082:
```nginx
server {
    listen 8082;
    server_name _ your-domain.com;

    # FastAPI Documentation - Exact match (HIGHEST PRIORITY)
    location = /api/docs {
        proxy_pass http://localhost:8002/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location = /api/redoc {
        proxy_pass http://localhost:8002/redoc;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location = /api/openapi.json {
        proxy_pass http://localhost:8002/openapi.json;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API - Strip /api prefix
    location /api/ {
        proxy_pass http://localhost:8002/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Access your app at: `http://your-server:8082`
Documentation at: `http://your-server:8082/api/docs`

### Database
Pastikan PostgreSQL sudah terinstall dan running.
Update connection string di `backend/.env`

## API Endpoints

### Authentication
- `POST /auth/register` - Register user baru (dengan no hp)
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile
- `POST /auth/reset-password` - Reset password

### Simple Labels
- `GET /labels` - Get semua simple label user
- `POST /labels/generate` - Generate simple label dengan QR code
- `GET /labels/print/{id}` - Get data label untuk print
- `GET /labels/preview/{id}` - Preview image label (returns PNG)

### Shipping Labels  
- `GET /shipping-labels` - Get semua shipping label user
- `POST /shipping-labels/generate` - Generate shipping label lengkap
- `GET /shipping-labels/print/{id}` - Get data shipping label untuk print
- `GET /shipping-labels/preview/{id}` - Preview shipping label (returns PNG)

## Print Format
Label dirancang untuk thermal printer lebar 58mm dengan format optimized untuk paket pengiriman.