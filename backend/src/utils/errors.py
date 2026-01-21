"""
Error handling utilities for the AIDO Todo application
"""

from typing import Dict, Any, List
from enum import Enum


class ErrorCode(Enum):
    """Enumeration of error codes for the application"""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class AIDOTodoException(Exception):
    """Base exception class for AIDO Todo application"""

    def __init__(self, message: str, error_code: ErrorCode, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary representation"""
        return {
            "error": self.message,
            "error_code": self.error_code.value,
            "details": self.details
        }


class ValidationError(AIDOTodoException):
    """Exception raised for validation errors"""

    def __init__(self, message: str, field_errors: List[Dict[str, str]] = None):
        details = {"field_errors": field_errors or []}
        super().__init__(message, ErrorCode.VALIDATION_ERROR, details)


class AuthenticationError(AIDOTodoException):
    """Exception raised for authentication errors"""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.AUTHENTICATION_ERROR)


class AuthorizationError(AIDOTodoException):
    """Exception raised for authorization errors"""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.AUTHORIZATION_ERROR)


class ResourceNotFoundError(AIDOTodoException):
    """Exception raised when a resource is not found"""

    def __init__(self, resource_type: str, resource_id: str = None):
        message = f"{resource_type} not found"
        if resource_id:
            message += f" with ID: {resource_id}"

        details = {"resource_type": resource_type, "resource_id": resource_id}
        super().__init__(message, ErrorCode.RESOURCE_NOT_FOUND, details)


class DatabaseError(AIDOTodoException):
    """Exception raised for database errors"""

    def __init__(self, message: str, original_error: Exception = None):
        details = {"original_error": str(original_error) if original_error else None}
        super().__init__(message, ErrorCode.DATABASE_ERROR, details)


class ExternalServiceError(AIDOTodoException):
    """Exception raised for external service errors"""

    def __init__(self, service_name: str, message: str, original_error: Exception = None):
        details = {
            "service_name": service_name,
            "original_error": str(original_error) if original_error else None
        }
        super().__init__(f"External service {service_name} error: {message}",
                         ErrorCode.EXTERNAL_SERVICE_ERROR, details)


def handle_error(exception: Exception) -> Dict[str, Any]:
    """
    Convert an exception to a standardized error response

    Args:
        exception: The exception to handle

    Returns:
        Dictionary with standardized error response
    """
    if isinstance(exception, AIDOTodoException):
        return {
            "success": False,
            "error": exception.message,
            "error_code": exception.error_code.value,
            "details": exception.details
        }
    else:
        # Handle unexpected errors
        return {
            "success": False,
            "error": "An unexpected error occurred",
            "error_code": ErrorCode.INTERNAL_ERROR.value,
            "details": {"original_error": str(exception)}
        }


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """
    Validate that required fields are present in the data

    Args:
        data: Dictionary containing the data to validate
        required_fields: List of required field names

    Returns:
        List of missing field names
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    return missing_fields


def validate_field_length(value: str, field_name: str, min_length: int = None, max_length: int = None) -> List[str]:
    """
    Validate the length of a string field

    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        min_length: Minimum allowed length
        max_length: Maximum allowed length

    Returns:
        List of validation errors
    """
    errors = []

    if value is not None:
        if min_length and len(value) < min_length:
            errors.append(f"{field_name} must be at least {min_length} characters")
        if max_length and len(value) > max_length:
            errors.append(f"{field_name} must be no more than {max_length} characters")

    return errors


def validate_uuid_format(uuid_str: str, field_name: str) -> List[str]:
    """
    Validate that a string is a valid UUID format

    Args:
        uuid_str: String to validate
        field_name: Name of the field for error messages

    Returns:
        List of validation errors
    """
    from uuid import UUID

    errors = []
    if uuid_str:
        try:
            UUID(uuid_str)
        except ValueError:
            errors.append(f"{field_name} must be a valid UUID")

    return errors


def validate_priority(priority: str) -> List[str]:
    """
    Validate task priority value

    Args:
        priority: Priority value to validate

    Returns:
        List of validation errors
    """
    errors = []
    valid_priorities = ["Low", "Medium", "High", "Critical"]

    if priority and priority not in valid_priorities:
        errors.append(f"Priority must be one of: {', '.join(valid_priorities)}")

    return errors


def validate_boolean(value: Any, field_name: str) -> List[str]:
    """
    Validate that a value is a boolean or can be converted to a boolean

    Args:
        value: Value to validate
        field_name: Name of the field for error messages

    Returns:
        List of validation errors
    """
    errors = []

    if value is not None:
        if not isinstance(value, bool):
            # Try to convert common boolean representations
            if isinstance(value, str):
                if value.lower() not in ['true', 'false', '1', '0', 'yes', 'no', 'on', 'off']:
                    errors.append(f"{field_name} must be a boolean value")
            else:
                errors.append(f"{field_name} must be a boolean value")

    return errors