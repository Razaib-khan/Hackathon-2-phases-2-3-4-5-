"""
User model for the Speckit Plus Todo Application
Defines the User entity with all required fields and relationships
"""

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel
import re


class UserBase(SQLModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(unique=True, nullable=False)
    favorite_teacher: str = Field(nullable=False)

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        # Remove any HTML/JS potentially harmful characters
        sanitized = re.sub(r'<[^>]+>', '', v)  # Remove HTML tags
        if sanitized != v:
            raise ValueError('Name contains invalid characters')
        return sanitized.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        # Basic email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v.strip().lower()

    @field_validator('favorite_teacher')
    @classmethod
    def validate_favorite_teacher(cls, v):
        if not v or not v.strip():
            raise ValueError('Favorite teacher cannot be empty')
        # Remove any HTML/JS potentially harmful characters
        sanitized = re.sub(r'<[^>]+>', '', v)  # Remove HTML tags
        if sanitized != v:
            raise ValueError('Favorite teacher contains invalid characters')
        return sanitized.strip()


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    # Indexes for common query patterns
    __table_args__ = (
        {"extend_existing": True}
    )


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None)
    favorite_teacher: Optional[str] = Field(default=None)
