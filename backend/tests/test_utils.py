"""
Unit tests for the utility functions in the AIDO Todo application
"""

import pytest
from src.utils.errors import (
    AIDOTodoException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    DatabaseError,
    ExternalServiceError,
    handle_error,
    validate_required_fields,
    validate_field_length,
    validate_priority,
    validate_uuid_format,
    validate_boolean
)


def test_aido_todo_exception():
    """Test the base AIDOTodoException class"""
    from src.utils.errors import ErrorCode

    exception = AIDOTodoException("Test message", ErrorCode.VALIDATION_ERROR)
    assert exception.message == "Test message"
    assert exception.error_code == ErrorCode.VALIDATION_ERROR
    assert exception.details == {}

    # Test with details
    details = {"key": "value"}
    exception_with_details = AIDOTodoException("Test message", ErrorCode.VALIDATION_ERROR, details)
    assert exception_with_details.details == details


def test_validation_error():
    """Test the ValidationError class"""
    from src.utils.errors import ErrorCode

    field_errors = [{"field": "name", "error": "required"}]
    exception = ValidationError("Validation failed", field_errors)

    assert exception.message == "Validation failed"
    assert exception.error_code == ErrorCode.VALIDATION_ERROR
    assert exception.details["field_errors"] == field_errors


def test_authentication_error():
    """Test the AuthenticationError class"""
    from src.utils.errors import ErrorCode

    exception = AuthenticationError("Invalid credentials")
    assert exception.message == "Invalid credentials"
    assert exception.error_code == ErrorCode.AUTHENTICATION_ERROR


def test_authorization_error():
    """Test the AuthorizationError class"""
    from src.utils.errors import ErrorCode

    exception = AuthorizationError("Access denied")
    assert exception.message == "Access denied"
    assert exception.error_code == ErrorCode.AUTHORIZATION_ERROR


def test_resource_not_found_error():
    """Test the ResourceNotFoundError class"""
    from src.utils.errors import ErrorCode

    # Test with resource type only
    exception = ResourceNotFoundError("User")
    assert "User not found" in exception.message
    assert exception.error_code == ErrorCode.RESOURCE_NOT_FOUND

    # Test with resource type and ID
    exception_with_id = ResourceNotFoundError("Task", "123")
    assert "Task not found" in exception_with_id.message
    assert "123" in exception_with_id.message
    assert exception_with_id.details["resource_type"] == "Task"
    assert exception_with_id.details["resource_id"] == "123"


def test_database_error():
    """Test the DatabaseError class"""
    from src.utils.errors import ErrorCode

    original_error = ValueError("DB connection failed")
    exception = DatabaseError("Database operation failed", original_error)

    assert exception.message == "Database operation failed"
    assert exception.error_code == ErrorCode.DATABASE_ERROR
    assert exception.details["original_error"] == "DB connection failed"


def test_external_service_error():
    """Test the ExternalServiceError class"""
    from src.utils.errors import ErrorCode

    original_error = ConnectionError("Service unavailable")
    exception = ExternalServiceError("OpenAI", "Request failed", original_error)

    assert "External service OpenAI error: Request failed" in exception.message
    assert exception.error_code == ErrorCode.EXTERNAL_SERVICE_ERROR
    assert exception.details["service_name"] == "OpenAI"
    assert exception.details["original_error"] == "Service unavailable"


def test_handle_error():
    """Test the handle_error function"""
    from src.utils.errors import ErrorCode

    # Test with AIDOTodoException
    aidoto_exception = ValidationError("Invalid input", [])
    result = handle_error(aidoto_exception)

    assert result["success"] is False
    assert result["error"] == "Invalid input"
    assert result["error_code"] == ErrorCode.VALIDATION_ERROR.value

    # Test with regular exception
    regular_exception = ValueError("Something went wrong")
    result = handle_error(regular_exception)

    assert result["success"] is False
    assert result["error"] == "An unexpected error occurred"
    assert result["error_code"] == ErrorCode.INTERNAL_ERROR.value
    assert "Something went wrong" in result["details"]["original_error"]


def test_validate_required_fields():
    """Test the validate_required_fields function"""
    data = {"name": "John", "email": "john@example.com"}

    # Test with all required fields present
    missing = validate_required_fields(data, ["name", "email"])
    assert missing == []

    # Test with missing fields
    missing = validate_required_fields(data, ["name", "email", "age"])
    assert missing == ["age"]

    # Test with None value
    data_with_none = {"name": "John", "email": None}
    missing = validate_required_fields(data_with_none, ["name", "email"])
    assert missing == ["email"]


def test_validate_field_length():
    """Test the validate_field_length function"""
    # Test within bounds
    errors = validate_field_length("Hello", "name", min_length=1, max_length=10)
    assert errors == []

    # Test too short
    errors = validate_field_length("Hi", "name", min_length=5, max_length=10)
    assert len(errors) == 1
    assert "at least 5 characters" in errors[0]

    # Test too long
    errors = validate_field_length("This is a very long name", "name", max_length=10)
    assert len(errors) == 1
    assert "no more than 10 characters" in errors[0]

    # Test with None value (should not trigger validation)
    errors = validate_field_length(None, "name", min_length=1, max_length=10)
    assert errors == []


def test_validate_priority():
    """Test the validate_priority function"""
    # Test valid priorities
    for priority in ["Low", "Medium", "High", "Critical"]:
        errors = validate_priority(priority)
        assert errors == []

    # Test invalid priority
    errors = validate_priority("Invalid")
    assert len(errors) == 1
    assert "must be one of" in errors[0]


def test_validate_uuid_format():
    """Test the validate_uuid_format function"""
    import uuid

    # Test valid UUID
    valid_uuid = str(uuid.uuid4())
    errors = validate_uuid_format(valid_uuid, "task_id")
    assert errors == []

    # Test invalid UUID
    errors = validate_uuid_format("invalid-uuid", "task_id")
    assert len(errors) == 1
    assert "must be a valid UUID" in errors[0]

    # Test with None (should not trigger validation)
    errors = validate_uuid_format(None, "task_id")
    assert errors == []


def test_validate_boolean():
    """Test the validate_boolean function"""
    # Test valid booleans
    assert validate_boolean(True, "status") == []
    assert validate_boolean(False, "status") == []

    # Test valid string representations
    assert validate_boolean("true", "status") == []
    assert validate_boolean("false", "status") == []
    assert validate_boolean("1", "status") == []
    assert validate_boolean("0", "status") == []
    assert validate_boolean("yes", "status") == []
    assert validate_boolean("no", "status") == []
    assert validate_boolean("on", "status") == []
    assert validate_boolean("off", "status") == []

    # Test invalid boolean
    errors = validate_boolean("maybe", "status")
    assert len(errors) == 1
    assert "must be a boolean value" in errors[0]

    # Test invalid type
    errors = validate_boolean(123, "status")
    assert len(errors) == 1
    assert "must be a boolean value" in errors[0]

    # Test with None (should not trigger validation)
    errors = validate_boolean(None, "status")
    assert errors == []