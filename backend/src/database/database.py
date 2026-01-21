"""
Database setup for the Speckit Plus Todo Application
Configures SQLModel with PostgreSQL database (Neon for production, SQLite for development)
"""

import os
import logging
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, create_engine
from sqlalchemy.exc import OperationalError

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./test.db"
)

# Configure engine based on database type
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL configuration for production/Neon
    try:
        engine = create_engine(
            DATABASE_URL,
            echo=True,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,    # Recycle connections
        )
        # Test the connection
        with engine.connect() as conn:
            pass  # If this succeeds, the connection is valid
        logging.info("Successfully connected to PostgreSQL database")
    except OperationalError as e:
        logging.error(f"Failed to connect to PostgreSQL database: {e}")
        logging.info("Falling back to SQLite for development")
        DATABASE_URL = "sqlite:///./fallback_test.db"
        engine = create_engine(DATABASE_URL, echo=True)
elif DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine = create_engine(DATABASE_URL, echo=True)
    logging.info("Using SQLite database for development")
else:
    # Default to SQLite if unknown type
    DATABASE_URL = "sqlite:///./fallback_test.db"
    engine = create_engine(DATABASE_URL, echo=True)
    logging.info("Using default SQLite database")


def get_session() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Create database tables
    """
    # Import models to register them with SQLModel
    # This ensures the tables are created with all relationships
    from models.task import Task  # noqa: F401
    from models.user import User  # noqa: F401
    from models.chat_session import ChatSession  # noqa: F401
    from models.chat_message import ChatMessage  # noqa: F401
    from models.task_operation_log import TaskOperationLog  # noqa: F401
    from sqlmodel import SQLModel

    try:
        SQLModel.metadata.create_all(engine)
        print(f"Database tables created successfully using: {DATABASE_URL}")
    except OperationalError as e:
        print(f"Could not create tables with primary database: {e}")
        print("Attempting to use fallback SQLite database...")
        fallback_url = "sqlite:///./fallback_test.db"
        fallback_engine = create_engine(fallback_url, echo=True)
        SQLModel.metadata.create_all(fallback_engine)
        print(f"Fallback database tables created successfully using: {fallback_url}")
