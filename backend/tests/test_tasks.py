"""
Unit tests for task functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from uuid import uuid4

from src.main import app
from src.models.user import User, UserCreate
from src.models.task import Task, TaskCreate, PriorityEnum
from src.database.database import get_session
from src.services.user_service import create_user
from src.services.task_service import create_task


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(client: TestClient, session: Session):
    # Create a user and get a token
    user_data = UserCreate(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="securepassword123",
        favorite_teacher="Mr. Johnson"
    )
    user = create_user(session, user_data)

    # Sign in to get token
    signin_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = client.post("/api/auth/signin", json=signin_data)
    token = response.json()["access_token"]

    # Add auth header to client
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


def test_create_task(authenticated_client: TestClient, session: Session):
    """Test creating a task"""
    user = session.query(User).first()
    user_id = str(user.id)

    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "Medium"
    }

    response = authenticated_client.post(f"/api/{user_id}/tasks", json=task_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["priority"] == "Medium"


def test_get_tasks(authenticated_client: TestClient, session: Session):
    """Test retrieving tasks for a user"""
    user = session.query(User).first()
    user_id = str(user.id)

    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "Medium"
    }
    authenticated_client.post(f"/api/{user_id}/tasks", json=task_data)

    # Get tasks
    response = authenticated_client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task"


def test_update_task(authenticated_client: TestClient, session: Session):
    """Test updating a task"""
    user = session.query(User).first()
    user_id = str(user.id)

    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Original description",
        "priority": "Medium"
    }
    create_response = authenticated_client.post(f"/api/{user_id}/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "priority": "High"
    }
    response = authenticated_client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"
    assert data["priority"] == "High"


def test_delete_task(authenticated_client: TestClient, session: Session):
    """Test deleting a task"""
    user = session.query(User).first()
    user_id = str(user.id)

    # Create a task first
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "priority": "Medium"
    }
    create_response = authenticated_client.post(f"/api/{user_id}/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Delete the task
    response = authenticated_client.delete(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 200

    # Verify the task is gone
    get_response = authenticated_client.get(f"/api/{user_id}/tasks/{task_id}")
    assert get_response.status_code == 404