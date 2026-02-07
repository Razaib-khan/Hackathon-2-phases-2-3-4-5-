"""
Recurring Task Pattern model for the Speckit Plus Todo Application
Defines the RecurrencePattern entity with frequency, interval, and end conditions
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, field_validator
from sqlmodel import Field, SQLModel
import json


class RecurrenceFrequencyEnum(str, Enum):
    """
    Enum for recurrence frequencies
    """
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class RecurrencePatternBase(BaseModel):
    """
    Base class for recurrence pattern with validation
    """
    frequency: RecurrenceFrequencyEnum
    interval: int = 1  # Every X units (e.g., every 2 weeks)
    end_condition: Optional[str] = None  # "count", "date", or None for never-ending
    end_value: Optional[int] = None  # Count or date depending on end_condition
    exception_dates: Optional[List[datetime]] = []  # Exception dates for recurring tasks
    weekdays: Optional[List[int]] = []  # For weekly patterns (0=Monday, 6=Sunday)

    @field_validator('interval')
    @classmethod
    def validate_interval(cls, v):
        if v < 1:
            raise ValueError('Interval must be at least 1')
        return v

    @field_validator('weekdays')
    @classmethod
    def validate_weekdays(cls, v):
        if v is None:
            return []
        for day in v:
            if day < 0 or day > 6:
                raise ValueError('Weekday must be between 0 (Monday) and 6 (Sunday)')
        return v


class RecurrencePattern(RecurrencePatternBase):
    """
    Complete recurrence pattern model with database fields
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RecurrencePatternCreate(RecurrencePatternBase):
    """
    Model for creating new recurrence patterns
    """
    pass


class RecurrencePatternRead(RecurrencePatternBase):
    """
    Model for reading recurrence patterns with ID
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class RecurrencePatternUpdate(BaseModel):
    """
    Model for updating recurrence patterns
    """
    frequency: Optional[RecurrenceFrequencyEnum] = None
    interval: Optional[int] = None
    end_condition: Optional[str] = None
    end_value: Optional[int] = None
    exception_dates: Optional[List[datetime]] = None
    weekdays: Optional[List[int]] = None

    @field_validator('interval')
    @classmethod
    def validate_interval(cls, v):
        if v is not None and v < 1:
            raise ValueError('Interval must be at least 1')
        return v

    @field_validator('weekdays')
    @classmethod
    def validate_weekdays(cls, v):
        if v is None:
            return v
        for day in v:
            if day < 0 or day > 6:
                raise ValueError('Weekday must be between 0 (Monday) and 6 (Sunday)')
        return v