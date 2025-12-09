from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr, Field

from app.db import get_db
from app.models.user import User
from app.utils.auth import hash_password, verify_password, create_access_token, create_refresh_token
from app.schema.user import UserCreate, UserResponse, TokenResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # check existing
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hash_password(user_in.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Login request schema
class LoginRequest(BaseModel):
    """Schema for login request."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login endpoint that accepts JSON with email and password."""
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email/password")
    access = create_access_token({"user_id": user.id})
    refresh = create_refresh_token({"user_id": user.id})
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
