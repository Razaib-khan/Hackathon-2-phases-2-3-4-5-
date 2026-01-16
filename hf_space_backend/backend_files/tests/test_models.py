"""
Unit tests for database models
"""
import pytest
from datetime import datetime
from uuid import uuid4

from src.models.task import Task, TaskCreate, PriorityEnum
from src.models.user import User, UserCreate


def test_user_model_creation():
    """Test creating a user model instance"""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "favorite_teacher": "Mrs. Smith",
        "password_hash": "hashed_password_here"
    }

    user = User(**user_data)

    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john@example.com"
    assert user.favorite_teacher == "Mrs. Smith"
    assert user.password_hash == "hashed_password_here"


def test_task_model_creation():
    """Test creating a task model instance"""
    user_id = uuid4()
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": PriorityEnum.MEDIUM,
        "status": False,
        "user_id": user_id
    }

    task = Task(**task_data)

    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.priority == PriorityEnum.MEDIUM
    assert task.status == False
    assert task.user_id == user_id


def test_task_create_schema_validation():
    """Test TaskCreate schema validation"""
    task_data = {
        "title": "Valid Task",
        "description": "This is a valid task",
        "priority": "High"
    }

    task_create = TaskCreate(**task_data)

    assert task_create.title == "Valid Task"
    assert task_create.description == "This is a valid task"
    assert task_create.priority == PriorityEnum.HIGH


def test_user_create_schema_validation():
    """Test UserCreate schema validation"""
    user_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "password": "securepassword123",
        "favorite_teacher": "Mr. Johnson"
    }

    user_create = UserCreate(**user_data)

    assert user_create.first_name == "Jane"
    assert user_create.last_name == "Doe"
    assert user_create.email == "jane@example.com"
    assert user_create.password == "securepassword123"
    assert user_create.favorite_teacher == "Mr. Johnson"