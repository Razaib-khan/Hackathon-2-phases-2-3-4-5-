"""
Authentication service for the Speckit Plus Todo Application
Handles JWT token generation and validation
"""

import os
from datetime import datetime, timedelta
from typing import Optional

import jwt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from config.security import SecurityConfig

# Load security configuration
SecurityConfig.validate_config()
SECRET_KEY = SecurityConfig.JWT_SECRET_KEY
ALGORITHM = SecurityConfig.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None


def authenticate_user(user: User, password: str) -> bool:
    """
    Authenticate user with provided password
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(password, user.password_hash)


def get_current_user(token: str, session) -> Optional[User]:
    """
    Get current user from token
    """
    payload = verify_token(token)
    if payload is None:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    # Fetch the user from the database
    from models.user import User
    user = session.get(User, user_id)
    return user
