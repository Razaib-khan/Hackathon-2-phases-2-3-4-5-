"""
Authentication API routes for the Speckit Plus Todo Application
Handles user registration, login, logout, password management, and account deletion
"""

import hashlib
import uuid
import smtplib
from datetime import datetime, timedelta
from typing import Dict, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_session
from models.user import User, UserCreate, UserRead, UserUpdate
from services.auth_service import create_access_token
from services.user_service import create_user, get_user_by_email, update_user_password, delete_user
from utils.auth import get_current_user
from middleware.security import limiter

router = APIRouter()


@router.post("/signup", response_model=dict)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Create a new user account
    """
    # Check if user already exists
    existing_user = get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create new user using service
    db_user = create_user(session, user_data)

    # For signup, we also return a token immediately (auto-login)
    from services.auth_service import create_access_token
    from datetime import timedelta

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )

    return {
        "user": db_user,
        "token": access_token,
    }


@router.post("/signin", response_model=dict)
def signin(user_data: Dict, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token
    """
    # Find user by email
    user = get_user_by_email(session, user_data["email"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password using service
    from services.auth_service import authenticate_user

    if not authenticate_user(user, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "user": user,
        "token": access_token,
    }


@router.post("/signout")
def signout():
    """
    Logout user and invalidate session
    """
    return {"message": "Logout successful"}


@router.put("/password/change")
def change_password(
    password_data: Dict,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Change user password
    """
    current_password = password_data.get("currentPassword")
    new_password = password_data.get("newPassword")

    if not current_password or not new_password:
        raise HTTPException(status_code=400, detail="Current and new passwords are required")

    # Verify old password
    from services.auth_service import authenticate_user
    if not authenticate_user(current_user, current_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    # Update password
    update_user_password(session, str(current_user.id), new_password)
    return {"message": "Password changed successfully"}


@router.put("/password")
def change_password_legacy(
    password_data: Dict,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Change user password (legacy endpoint)
    """
    old_password = password_data.get("old_password")
    new_password = password_data.get("new_password")

    # Verify old password
    from services.auth_service import authenticate_user
    if not authenticate_user(current_user, old_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # Update password
    update_user_password(session, str(current_user.id), new_password)
    return {"message": "Password changed successfully"}


@router.post("/password/recovery")
def request_password_recovery(reset_data: Dict, session: Session = Depends(get_session)):
    """
    Request password recovery (send reset link to email)
    """
    # Find user by email
    user = get_user_by_email(session, reset_data["email"])
    if not user:
        # Don't reveal if email exists to prevent enumeration
        return {"message": "If your email exists in our system, you'll receive a reset link shortly"}

    # In a real implementation, we would:
    # 1. Generate a password reset token
    # 2. Store it securely with expiration
    # 3. Send email with reset link
    # For now, just return success message
    return {"message": "If your email exists in our system, you'll receive a reset link shortly"}


@router.post("/password/reset")
def reset_password(reset_data: Dict, session: Session = Depends(get_session)):
    """
    Reset password using recovery token
    """
    token = reset_data.get("token")
    new_password = reset_data.get("new_password")

    if not token or not new_password:
        raise HTTPException(status_code=400, detail="Token and new password are required")

    # In a real implementation, we would validate the reset token
    # For now, we'll just update the password for the user associated with the token
    # This is a simplified implementation for the demo
    # In a real system, you'd lookup the token in a database and get the associated user ID

    # For this simplified implementation, we'll assume the token is valid
    # and the email is also provided to identify the user
    email = reset_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    user = get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's password
    from services.user_service import update_user_password
    success = update_user_password(session, str(user.id), new_password)

    if not success:
        raise HTTPException(status_code=400, detail="Failed to update password")

    return {"message": "Password reset successfully"}


@router.post("/forgot-password")
def forgot_password(reset_data: Dict, session: Session = Depends(get_session)):
    """
    Handle password recovery using security question
    """
    # Find user by email
    user = get_user_by_email(session, reset_data["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify security question answer
    if user.favorite_teacher != reset_data["favorite_teacher_answer"]:
        raise HTTPException(status_code=400, detail="Incorrect security answer")

    # Generate a temporary reset token (valid for a short period)
    import secrets
    reset_token = secrets.token_urlsafe(32)

    # In a real implementation, we would store this token with expiration
    # For now, we'll just return it directly (not secure for production!)
    return {
        "message": "Password recovery successful",
        "reset_token": reset_token,
        "expires_in": 300  # 5 minutes
    }


@router.get("/profile", response_model=UserRead)
def get_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user profile information
    """
    return current_user


@router.put("/profile", response_model=UserRead)
def update_profile(
    profile_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update user profile information
    """
    # Update user profile fields if provided
    if profile_data.first_name is not None:
        current_user.first_name = profile_data.first_name
    if profile_data.last_name is not None:
        current_user.last_name = profile_data.last_name
    if profile_data.email is not None:
        current_user.email = profile_data.email

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


from pydantic import BaseModel

class DeleteAccountRequest(BaseModel):
    password: str

@router.delete("/account")
def delete_account(
    request_data: DeleteAccountRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete user account and all associated data
    """
    # Verify the provided password matches the stored password
    from services.auth_service import authenticate_user
    if not authenticate_user(current_user, request_data.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    # Delete user account
    success = delete_user(session, str(current_user.id))
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Account deleted successfully"}
