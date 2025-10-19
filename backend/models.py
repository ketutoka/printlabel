from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)  # Added phone field
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    shipping_labels = relationship("ShippingLabel", back_populates="user")

class ShippingLabel(Base):
    __tablename__ = "shipping_labels"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String(255), nullable=False)
    sender_phone = Column(String(20), nullable=False)
    recipient_name = Column(String(255), nullable=True)  # Made nullable/optional
    recipient_address = Column(Text, nullable=True)  # Made nullable/optional
    recipient_phone = Column(String(20), nullable=True)  # Made nullable/optional
    shipping_code = Column(String(100), nullable=True)  # Made nullable, removed unique constraint
    label_size = Column(String(10), nullable=False, default="58mm")  # New field for label size
    image_path = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="shipping_labels")