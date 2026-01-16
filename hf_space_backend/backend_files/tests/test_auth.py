"""
Unit tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.main import app
from src.models.user import User, UserCreate
from src.database.database import get_session
from src.services.user_service import create_user


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


def test_user_signup(client: TestClient, session: Session):
    """Test user signup functionality"""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "favorite_teacher": "Mrs. Smith"
    }

    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "john.doe@example.com"
    assert "id" in data
    assert data["first_name"] == "John"


def test_user_signin(client: TestClient, session: Session):
    """Test user signin functionality"""
    # First create a user
    user_data = UserCreate(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        password="securepassword123",
        favorite_teacher="Mr. Johnson"
    )
    create_user(session, user_data)

    # Then try to sign in
    signin_data = {
        "email": "jane.doe@example.com",
        "password": "securepassword123"
    }

    response = client.post("/api/auth/signin", json=signin_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_duplicate_email_signup(client: TestClient, session: Session):
    """Test that duplicate email signup is rejected"""
    # Create first user
    user_data = {
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob@example.com",
        "password": "securepassword123",
        "favorite_teacher": "Mr. Johnson"
    }

    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200

    # Try to create another user with same email
    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 409  # Conflict