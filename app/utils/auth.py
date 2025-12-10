from datetime import datetime, timedelta
from jose import jwt, JWTError
import bcrypt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.db import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Password helpers
def _truncate_to_72_bytes(password: str) -> str:
    """Truncate password to at most 72 bytes to comply with bcrypt's limit."""
    if not password:
        return password
    
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= 72:
        return password
    
    # Start with 72 bytes and work backwards to find valid UTF-8 boundary
    truncated_bytes = password_bytes[:72]
    
    # Remove bytes from the end until we have valid UTF-8
    # This handles cases where we cut in the middle of a multi-byte character
    for i in range(len(truncated_bytes), 0, -1):
        try:
            result = truncated_bytes[:i].decode('utf-8')
            # Double-check the encoded length is <= 72
            if len(result.encode('utf-8')) <= 72:
                return result
        except UnicodeDecodeError:
            continue
    
    # If all else fails, return first 72 ASCII characters (shouldn't happen)
    return password[:72] if len(password) >= 72 else password

def hash_password(password: str) -> str:
    """Hash a password using bcrypt, truncating if it exceeds bcrypt's 72-byte limit."""
    if not password:
        raise ValueError("Password cannot be empty")
    truncated = _truncate_to_72_bytes(password)
    # Encode password to bytes for bcrypt
    password_bytes = truncated.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string (bcrypt returns bytes)
    return hashed.decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against a hash using bcrypt, truncating if it exceeds bcrypt's 72-byte limit."""
    if not plain or not hashed:
        return False
    truncated = _truncate_to_72_bytes(plain)
    # Encode both to bytes for bcrypt
    password_bytes = truncated.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    # Verify password
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# JWT helpers
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Dependency: returns current user model instance
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
