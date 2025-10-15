from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=70, description="Password must be 6-70 characters")
    
    @validator('password')
    def validate_password_length(cls, v):
        # Ensure password won't exceed bcrypt's 72 byte limit when encoded
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 70:  # Leave some margin for safety
            raise ValueError('Password is too long. Please use a shorter password.')
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LabelCreate(BaseModel):
    sender_name: str
    shipping_code: str

class LabelResponse(BaseModel):
    id: int
    sender_name: str
    shipping_code: str
    image_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None