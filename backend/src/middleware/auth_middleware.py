"""
Authentication Middleware for the AIDO TODO Application
Handles JWT token validation and user authentication
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import Optional
import jwt
from datetime import datetime, timedelta
from config.security import SecurityConfig
from database.database import get_session
from models.user import User

security = HTTPBearer()

class AuthMiddleware:
    """
    Authentication middleware class for handling JWT tokens and user validation
    """

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create a new access token with the provided data"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)  # Default 30 minutes

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SecurityConfig.JWT_SECRET_KEY, algorithm=SecurityConfig.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, credentials_exception):
        """Verify a JWT token and return the user ID"""
        try:
            payload = jwt.decode(token, SecurityConfig.JWT_SECRET_KEY, algorithms=[SecurityConfig.JWT_ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            return user_id
        except jwt.PyJWTError:
            raise credentials_exception

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """
    Dependency to get the current user from the JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = AuthMiddleware.verify_token(credentials.credentials, credentials_exception)
    user = session.get(User, user_id)

    if user is None:
        raise credentials_exception

    return user