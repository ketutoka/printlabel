# Print Label Application - AI Copilot Instructions

## Project Overview
This is a **thermal label printing application** for 58mm printers with the following stack:
- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Frontend**: Vue.js 3 with Element Plus UI components
- **Database**: PostgreSQL
- **Authentication**: JWT tokens with OAuth2PasswordBearer

## Architecture & Key Patterns

### Backend Structure (`/backend`)
- **FastAPI Application**: `main.py` contains all endpoints and CORS configuration
- **Database Models**: `models.py` uses SQLAlchemy with relationship patterns
- **Authentication Flow**: JWT tokens via `auth.py`, password hashing with bcrypt
- **Label Generation**: `label_generator.py` creates 203px wide images optimized for 58mm thermal printers
- **Email Service**: `email_service.py` handles password reset emails via SMTP

### Frontend Structure (`/frontend`)
- **Vue 3 Composition API**: All components use `<script setup>` syntax
- **State Management**: Pinia stores in `/src/stores` (user.js, label.js)
- **UI Framework**: Element Plus with Indonesian language labels
- **API Communication**: Axios with interceptors for token management in `/src/services/api.js`

### Critical Development Workflows

#### Backend Setup & Run
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows specific
pip install -r requirements.txt
# Copy .env.example to .env and configure
uvicorn main:app --reload  # Runs on port 8002
```

#### Frontend Setup & Run  
```bash
cd frontend
npm install
npm run dev  # Runs on port 3002, proxies /api to backend:8002
```

#### Database Initialization
- PostgreSQL required with connection string in `.env`
- Tables auto-created via `Base.metadata.create_all(bind=engine)` in main.py
- No migrations setup - uses direct SQLAlchemy model creation

## Project-Specific Patterns

### Authentication Flow
- Login uses `OAuth2PasswordRequestForm` with email as username
- Token stored in localStorage, automatically added to API calls
- `useUserStore` manages auth state with Pinia
- Protected routes use `get_current_user` dependency

### Label Generation Process
1. User creates label via `/labels/generate` endpoint  
2. `generate_label_with_qr()` creates 203px wide PNG image
3. QR code contains shipping code, sized for thermal printer readability
4. Label layout: Header → Sender → Shipping Code → QR → Date

### Thermal Printer Optimization
- **Critical**: All labels designed for 58mm width (≈203 pixels at 90 DPI)
- Font sizes: 12px large, 8px small for thermal printer clarity
- QR codes: 80x80px with error correction level L
- Images saved to `/backend/labels/` directory

### API Integration Pattern
```javascript
// Frontend API calls follow this pattern:
const result = await userStore.login(credentials)
if (result.success) { /* handle success */ }
else { /* handle result.error */ }
```

### Error Handling
- Backend: HTTPException with status codes and detail messages
- Frontend: ElMessage components for user notifications
- API interceptor redirects to login on 401 responses

## Essential File Dependencies

### Backend Dependencies Chain
- `main.py` → imports from `database.py`, `models.py`, `schemas.py`, `auth.py`, `crud.py`
- `models.py` → defines User/Label relationships for SQLAlchemy
- `label_generator.py` → requires PIL, qrcode libraries for image creation

### Frontend Component Dependencies  
- All views depend on stores: `useUserStore`, `useLabelStore`
- Router guards in `/src/router/index.js` check authentication
- Element Plus components imported globally in `main.js`

## Integration Points

### Cross-Origin Setup
- Backend CORS allows `localhost:3002` and `localhost:5173`
- Frontend Vite proxy: `/api/*` → `localhost:8002`
- API base URL: `http://localhost:8002`

### Email Configuration
- SMTP settings in `.env` for password reset functionality
- Gmail app passwords required for EMAIL_HOST_PASSWORD

## Common Development Tasks

### Adding New Label Fields
1. Update `Label` model in `models.py`
2. Modify `LabelCreate`/`LabelResponse` schemas
3. Update `generate_label_with_qr()` layout function
4. Extend frontend form in `CreateLabel.vue`

### Adding Authentication Endpoints
1. Create route in `main.py` with `current_user` dependency
2. Add corresponding store action in `useUserStore`
3. Update API service calls with error handling

### Modifying Print Layout
- Edit `label_generator.py`: adjust coordinates, fonts, QR size
- Test with 203px width constraint for thermal compatibility
- Verify QR code readability at small sizes