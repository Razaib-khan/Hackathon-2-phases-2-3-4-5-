"""
Validation utilities for the Speckit Plus Todo Application
"""
import uuid
from typing import Union
from fastapi import HTTPException


def validate_uuid(uuid_string: str, uuid_type: str = "ID") -> uuid.UUID:
    """
    Validate UUID string and return UUID object
    """
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return uuid_obj
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {uuid_type} format"
        )


def validate_user_id(user_id: str) -> uuid.UUID:
    """
    Validate user ID format
    """
    return validate_uuid(user_id, "user ID")


def validate_task_id(task_id: str) -> uuid.UUID:
    """
    Validate task ID format
    """
    return validate_uuid(task_id, "task ID")


def sanitize_input(input_str: str) -> str:
    """
    Basic input sanitization
    """
    if input_str is None:
        return input_str

    # Remove null bytes
    sanitized = input_str.replace('\x00', '')

    # Remove HTML tags (basic approach)
    import re
    sanitized = re.sub(r'<[^>]*>', '', sanitized)

    # Remove control characters (except common whitespace)
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\t\n\r')

    return sanitized