from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User, Label, ShippingLabel
from schemas import UserCreate, LabelCreate, ShippingLabelCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Truncate password to 72 bytes to avoid bcrypt limitation
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate password to 72 bytes to match hashing
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,  # Added phone field
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user_update.name is not None:
            db_user.name = user_update.name
        if user_update.email is not None:
            # Check if email already exists for another user
            existing_user = db.query(User).filter(User.email == user_update.email, User.id != user_id).first()
            if existing_user:
                raise ValueError("Email sudah digunakan oleh user lain")
            db_user.email = user_update.email
        if user_update.phone is not None:
            db_user.phone = user_update.phone
        db.commit()
        db.refresh(db_user)
    return db_user

def create_label(db: Session, label: LabelCreate, user_id: int):
    db_label = Label(
        sender_name=label.sender_name,
        sender_phone=label.sender_phone,
        shipping_code=label.shipping_code,
        user_id=user_id
    )
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

def get_label(db: Session, label_id: int, user_id: int):
    return db.query(Label).filter(
        Label.id == label_id, 
        Label.user_id == user_id
    ).first()

def get_user_labels(db: Session, user_id: int):
    return db.query(Label).filter(Label.user_id == user_id).all()

# Shipping Label functions
def create_shipping_label(db: Session, shipping_label: ShippingLabelCreate, user_id: int):
    db_shipping_label = ShippingLabel(
        sender_name=shipping_label.sender_name,
        sender_phone=shipping_label.sender_phone,
        recipient_name=shipping_label.recipient_name,
        recipient_address=shipping_label.recipient_address,
        recipient_phone=shipping_label.recipient_phone,
        shipping_code=shipping_label.shipping_code,
        user_id=user_id
    )
    db.add(db_shipping_label)
    db.commit()
    db.refresh(db_shipping_label)
    return db_shipping_label

def get_shipping_label(db: Session, label_id: int, user_id: int):
    return db.query(ShippingLabel).filter(
        ShippingLabel.id == label_id, 
        ShippingLabel.user_id == user_id
    ).first()

def get_user_shipping_labels(db: Session, user_id: int):
    return db.query(ShippingLabel).filter(ShippingLabel.user_id == user_id).all()

def delete_label(db: Session, label_id: int, user_id: int):
    """Delete a simple label and return the image path for file cleanup"""
    label = db.query(Label).filter(
        Label.id == label_id, 
        Label.user_id == user_id
    ).first()
    
    if not label:
        return None
    
    # Store image path for file cleanup
    image_path = label.image_path
    
    # Delete from database
    db.delete(label)
    db.commit()
    
    return image_path

def delete_shipping_label(db: Session, label_id: int, user_id: int):
    """Delete a shipping label and return the image path for file cleanup"""
    label = db.query(ShippingLabel).filter(
        ShippingLabel.id == label_id, 
        ShippingLabel.user_id == user_id
    ).first()
    
    if not label:
        return None
    
    # Store image path for file cleanup
    image_path = label.image_path
    
    # Delete from database
    db.delete(label)
    db.commit()
    
    return image_path