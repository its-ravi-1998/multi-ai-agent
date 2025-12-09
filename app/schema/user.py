from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# Request Schema - Registration ke liye
class UserCreate(BaseModel):
    """Schema for user registration request."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password (min 6 characters)")
    full_name: Optional[str] = Field(None, description="User's full name")


# Response Schema - User data return karne ke liye (password nahi)
class UserResponse(BaseModel):
    """Schema for user response (without password)."""
    id: int
    email: str
    full_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy model se automatically convert karega


# Response Schema - Login ke baad token return karne ke liye
class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
