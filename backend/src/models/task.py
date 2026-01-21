"""
Task model for the Speckit Plus Todo Application
Defines the Task entity with all required fields and relationships
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel
import re


class PriorityEnum(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: bool = Field(default=False)

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        # Remove any HTML/JS potentially harmful characters
        sanitized = re.sub(r'<[^>]+>', '', v)  # Remove HTML tags
        if sanitized != v:
            raise ValueError('Title contains invalid characters')
        return sanitized.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v is None:
            return v
        # Remove any HTML/JS potentially harmful characters
        sanitized = re.sub(r'<[^>]+>', '', v)  # Remove HTML tags
        return sanitized


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM, index=True)  # Add index for priority filtering
    status: bool = Field(default=False, index=True)  # Add index for status filtering
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)  # Add index for timestamp filtering

    # Indexes for common query patterns
    __table_args__ = (
        {"extend_existing": True}
    )

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")

    # Relationship to task operation logs
    task_operation_logs: list["TaskOperationLog"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    priority: Optional[PriorityEnum] = Field(default=None)
    status: Optional[bool] = Field(default=None)
    timestamp: Optional[datetime] = Field(default=None)

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v is None:
            return v
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        # Remove any HTML/JS potentially harmful characters
        sanitized = re.sub(r'<[^>]+>', '', v)  # Remove HTML tags
        if sanitized != v:
            raise ValueError('Title contains invalid characters')
        return sanitized.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v is None:
            return v
        # Remove any HTML/JS potentially harmful characters
        sanitized = re.sub(r'<[^>]+>', '', v)  # Remove HTML tags
        return sanitized


class TaskComplete(SQLModel):
    complete: bool
