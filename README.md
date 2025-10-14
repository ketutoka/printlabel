# Print Label Application

## Aplikasi Cetak Label Paket untuk Thermal Printer 58mm

### Fitur
- Register User (nama/email/password)
- Login (email/password) 
- Reset password dengan kode email
- Cetak Label dengan QR Code otomatis
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
python -m venv .venv
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

### Database
Pastikan PostgreSQL sudah terinstall dan running.
Update connection string di `backend/.env`

## API Endpoints
- `POST /auth/register` - Register user baru
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile
- `POST /auth/reset-password` - Reset password
- `GET /labels` - Get semua label user
- `POST /labels/generate` - Generate label dengan QR code
- `GET /labels/print/{id}` - Get data label untuk print
- `GET /labels/preview/{id}` - Preview image label (returns PNG)

## Print Format
Label dirancang untuk thermal printer lebar 58mm dengan format optimized untuk paket pengiriman.