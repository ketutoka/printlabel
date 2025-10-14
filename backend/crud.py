from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User, Label
from schemas import UserCreate, LabelCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_label(db: Session, label: LabelCreate, user_id: int):
    db_label = Label(
        sender_name=label.sender_name,
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