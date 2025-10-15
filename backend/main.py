from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

from database import SessionLocal, engine
from models import Base, User, Label
from schemas import UserCreate, UserResponse, UserLogin, LabelCreate, LabelResponse
from auth import authenticate_user, create_access_token, get_current_user
from label_generator import generate_label_with_qr, get_label_image

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Print Label API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3002", 
        "http://localhost:5173", 
        "http://localhost:8082",
        "http://printlabel.aberaharja.my.id",
        "https://printlabel.aberaharja.my.id",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Print Label API is running"}

# Auth endpoints
@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    from crud import create_user, get_user_by_email
    
    # Check if user already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    db_user = create_user(db, user)
    return UserResponse(id=db_user.id, name=db_user.name, email=db_user.email)

@app.post("/auth/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/reset-password")
def reset_password(email: str, db: Session = Depends(get_db)):
    from crud import get_user_by_email
    from email_service import send_reset_email
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate reset token and send email
    reset_token = create_access_token(data={"sub": user.email, "reset": True})
    send_reset_email(user.email, reset_token)
    
    return {"message": "Reset password email sent"}

@app.get("/auth/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email
    )

# Label endpoints
@app.post("/labels/generate", response_model=LabelResponse)
def generate_label(
    label: LabelCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import create_label
    
    # Create label in database
    db_label = create_label(db, label, current_user.id)
    
    # Generate QR code and label image
    label_image_path = generate_label_with_qr(
        sender_name=label.sender_name,
        shipping_code=label.shipping_code,
        label_id=db_label.id
    )
    
    # Update label with image path
    db_label.image_path = label_image_path
    db.commit()
    
    return LabelResponse(
        id=db_label.id,
        sender_name=db_label.sender_name,
        shipping_code=db_label.shipping_code,
        image_path=db_label.image_path,
        created_at=db_label.created_at
    )

@app.get("/labels", response_model=list[LabelResponse])
def get_user_labels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import get_user_labels
    
    labels = get_user_labels(db, current_user.id)
    return [
        LabelResponse(
            id=label.id,
            sender_name=label.sender_name,
            shipping_code=label.shipping_code,
            image_path=label.image_path,
            created_at=label.created_at
        )
        for label in labels
    ]

@app.get("/labels/print/{label_id}")
def get_label_for_print(
    label_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import get_label
    
    label = get_label(db, label_id, current_user.id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    
    return {
        "id": label.id,
        "sender_name": label.sender_name,
        "shipping_code": label.shipping_code,
        "image_path": label.image_path,
        "qr_data": label.shipping_code
    }

@app.get("/labels/preview/{label_id}")
def preview_label_image(
    label_id: int,
    token: Optional[str] = None,
    db: Session = Depends(get_db)
):
    from crud import get_label
    from jose import JWTError, jwt
    from auth import SECRET_KEY, ALGORITHM
    from crud import get_user_by_email
    
    current_user = None
    
    # Try to get token from query parameter first
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email:
                current_user = get_user_by_email(db, email)
        except JWTError:
            pass
    
    # If no token in query, try to get from header
    if not current_user:
        try:
            from fastapi import Request
            # This is a fallback, but for image requests we'll rely on token parameter
            pass
        except:
            pass
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    label = get_label(db, label_id, current_user.id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    
    # Check if image file exists
    if not label.image_path or not os.path.exists(label.image_path):
        raise HTTPException(status_code=404, detail="Label image not found")
    
    return FileResponse(
        path=label.image_path,
        media_type="image/png",
        filename=f"preview_label_{label.shipping_code}.png"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)