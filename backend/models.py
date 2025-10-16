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
    labels = relationship("Label", back_populates="user")
    shipping_labels = relationship("ShippingLabel", back_populates="user")

class Label(Base):
    __tablename__ = "labels"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String(255), nullable=False)
    shipping_code = Column(String(100), unique=True, nullable=False)
    image_path = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="labels")

class ShippingLabel(Base):
    __tablename__ = "shipping_labels"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String(255), nullable=False)
    sender_phone = Column(String(20), nullable=False)
    recipient_name = Column(String(255), nullable=False)
    recipient_address = Column(Text, nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    shipping_code = Column(String(100), nullable=True)  # Made nullable, removed unique constraint
    image_path = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="shipping_labels")