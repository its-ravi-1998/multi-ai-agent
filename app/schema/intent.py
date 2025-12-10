from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class IntentCreate(BaseModel):
    """Schema for intent creation request."""
    raw_input: str = Field(..., description="Intent raw input")

    class Config:
        orm_mode = True

class IntentResponse(BaseModel):
    name: str
    confidence: float
    