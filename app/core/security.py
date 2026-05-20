from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# 1. Initialize the hashing engine with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password string against its stored database hash.
    Ensures both inputs are safely sliced below bcrypt's 72-byte architectural ceiling.
    """
    try:
        # Explicitly truncate the plain password string before handing it to passlib
        safe_plain = str(plain_password)[:72]
        
        return pwd_context.verify(safe_plain, hashed_password)
    except ValueError:
        # Fallback catch in case passlib's context is still holding an internal buffer overflow
        return False

def get_password_hash(password: str) -> str:
    """
    Generates a secure hash from a plain text password.
    """
    safe_password = str(password)[:72]
    return pwd_context.hash(safe_password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """Generates a cryptographically signed JWT token for authenticating future requests."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # The payload contains the 'sub' (User identity) and 'exp' (Expiration time)
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Sign the token using our secret key and algorithm from our .env file
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt