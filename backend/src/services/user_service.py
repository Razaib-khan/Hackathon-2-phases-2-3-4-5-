"""
User service for the Speckit Plus Todo Application
Handles business logic for user operations
"""

import hashlib
from typing import Optional

from sqlmodel import Session, select

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User, UserCreate


def create_user(session: Session, user_data: UserCreate) -> User:
    """
    Create a new user with hashed password
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = pwd_context.hash(user_data.password)

    # Create user object
    db_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=password_hash,
        favorite_teacher=user_data.favorite_teacher,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get user by email address
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password
    """
    from passlib.context import CryptContext

    user = get_user_by_email(session, email)
    if not user:
        return None

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(password, user.password_hash):
        return None

    return user


def update_user_password(session: Session, user_id: str, new_password: str) -> bool:
    """
    Update user password
    """
    from passlib.context import CryptContext

    user = session.get(User, user_id)
    if not user:
        return False

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user.password_hash = pwd_context.hash(new_password)

    session.add(user)
    session.commit()
    return True


def delete_user(session: Session, user_id: str) -> bool:
    """
    Delete user account
    """
    user = session.get(User, user_id)
    if not user:
        return False

    session.delete(user)
    session.commit()
    return True
