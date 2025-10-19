from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

from database import SessionLocal, engine
from models import Base, User, ShippingLabel
from schemas import UserCreate, UserResponse, UserLogin, UserUpdate, ShippingLabelCreate, ShippingLabelResponse
from auth import authenticate_user, create_access_token, get_current_user
from label_generator import generate_label_with_qr, generate_shipping_label, get_label_image

# Load environment variables
load_dotenv()

# Database migration function
def run_migrations():
    """Run database migrations"""
    try:
        with engine.connect() as connection:
            # Check if phone column exists in users table
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'phone';
            """))
            
            if not result.fetchone():
                # Add phone column to users table
                connection.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN phone VARCHAR(20);
                """))
                connection.commit()
                print("✅ Added phone column to users table")
            
            print("✅ Database migration completed")
    except Exception as e:
        print(f"⚠️ Migration warning: {e}")

# Create database tables
Base.metadata.create_all(bind=engine)

# Run migrations
run_migrations()

app = FastAPI(
    title="Print Label API", 
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    servers=[
        {"url": "/api", "description": "API Server via Nginx Proxy"},
        {"url": "/", "description": "Direct API Server"}
    ]
)

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
        email=current_user.email,
        phone=current_user.phone
    )

@app.put("/auth/me", response_model=UserResponse)
def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import update_user
    
    try:
        updated_user = update_user(db, current_user.id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            phone=updated_user.phone
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Shipping Label endpoints
@app.post("/shipping-labels/generate", response_model=ShippingLabelResponse)
def generate_shipping_label_endpoint(
    shipping_label: ShippingLabelCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import create_shipping_label
    
    # Transform shipping code to uppercase if provided
    if shipping_label.shipping_code:
        shipping_label.shipping_code = shipping_label.shipping_code.upper()
    
    # Create shipping label in database
    db_shipping_label = create_shipping_label(db, shipping_label, current_user.id)
    
    # Generate shipping label image
    label_image_path = generate_shipping_label(
        sender_name=shipping_label.sender_name,
        sender_phone=shipping_label.sender_phone,
        recipient_name=shipping_label.recipient_name,
        recipient_address=shipping_label.recipient_address,
        recipient_phone=shipping_label.recipient_phone,
        shipping_code=shipping_label.shipping_code,
        label_id=db_shipping_label.id,
        label_size=shipping_label.label_size or "58mm"  # Pass label size with default
    )
    
    # Update shipping label with image path
    db_shipping_label.image_path = label_image_path
    db.commit()
    
    return ShippingLabelResponse(
        id=db_shipping_label.id,
        sender_name=db_shipping_label.sender_name,
        sender_phone=db_shipping_label.sender_phone,
        recipient_name=db_shipping_label.recipient_name,
        recipient_address=db_shipping_label.recipient_address,
        recipient_phone=db_shipping_label.recipient_phone,
        shipping_code=db_shipping_label.shipping_code,
        image_path=db_shipping_label.image_path,
        created_at=db_shipping_label.created_at
    )

@app.get("/shipping-labels", response_model=list[ShippingLabelResponse])
def get_user_shipping_labels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import get_user_shipping_labels
    
    shipping_labels = get_user_shipping_labels(db, current_user.id)
    return [
        ShippingLabelResponse(
            id=label.id,
            sender_name=label.sender_name,
            sender_phone=label.sender_phone,
            recipient_name=label.recipient_name,
            recipient_address=label.recipient_address,
            recipient_phone=label.recipient_phone,
            shipping_code=label.shipping_code,
            label_size=getattr(label, 'label_size', '58mm'),  # Include label_size with default
            image_path=label.image_path,
            created_at=label.created_at
        )
        for label in shipping_labels
    ]

@app.get("/shipping-labels/print/{label_id}")
def get_shipping_label_for_print(
    label_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import get_shipping_label
    
    label = get_shipping_label(db, label_id, current_user.id)
    if not label:
        raise HTTPException(status_code=404, detail="Shipping label not found")
    
    return {
        "id": label.id,
        "sender_name": label.sender_name,
        "sender_phone": label.sender_phone,
        "recipient_name": label.recipient_name,
        "recipient_address": label.recipient_address,
        "recipient_phone": label.recipient_phone,
        "shipping_code": label.shipping_code,
        "image_path": label.image_path
    }

@app.get("/shipping-labels/preview/{label_id}")
def preview_shipping_label_image(
    label_id: int,
    token: Optional[str] = None,
    db: Session = Depends(get_db)
):
    from crud import get_shipping_label
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
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    label = get_shipping_label(db, label_id, current_user.id)
    if not label:
        raise HTTPException(status_code=404, detail="Shipping label not found")
    
    # Check if image file exists
    if not label.image_path or not os.path.exists(label.image_path):
        raise HTTPException(status_code=404, detail="Shipping label image not found")
    
    return FileResponse(
        path=label.image_path,
        media_type="image/png",
        filename=f"preview_shipping_label_{label.shipping_code}.png"
    )

# Delete endpoints - Bulk operations MUST come before parameterized routes
@app.delete("/shipping-labels/bulk")
def bulk_delete_shipping_labels(
    label_ids: list[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import delete_shipping_label
    
    results = {
        "deleted_count": 0,
        "failed_count": 0,
        "deleted_files": [],
        "errors": []
    }
    
    for label_id in label_ids:
        try:
            image_path = delete_shipping_label(db, label_id, current_user.id)
            
            if image_path:
                results["deleted_count"] += 1
                results["deleted_files"].append(image_path)
                
                # Delete image file if exists
                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                    except OSError as e:
                        print(f"Warning: Could not delete image file {image_path}: {e}")
            else:
                results["failed_count"] += 1
                results["errors"].append(f"Shipping label {label_id} not found")
                
        except Exception as e:
            results["failed_count"] += 1
            results["errors"].append(f"Shipping label {label_id}: {str(e)}")
    
    return {
        "message": f"Bulk delete completed. {results['deleted_count']} deleted, {results['failed_count']} failed.",
        **results
    }

# Single delete endpoints - MUST come after bulk endpoints
@app.delete("/shipping-labels/{label_id}")
def delete_shipping_label_endpoint(
    label_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from crud import delete_shipping_label
    
    # Delete from database and get image path
    image_path = delete_shipping_label(db, label_id, current_user.id)
    
    if not image_path:
        raise HTTPException(status_code=404, detail="Shipping label not found")
    
    # Delete image file if exists
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
        except OSError as e:
            print(f"Warning: Could not delete image file {image_path}: {e}")
    
    return {"message": "Shipping label deleted successfully", "deleted_file": image_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)