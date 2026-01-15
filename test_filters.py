#!/usr/bin/env python3
"""
Test script to validate the search and filtering functionality
for the Speckit Plus Todo Application
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from sqlmodel import Session, SQLModel, create_engine
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from backend.src.models.task import Task, TaskCreate, PriorityEnum
from backend.src.models.user import User
from backend.src.services.task_service import get_tasks_for_user, create_task

# Create an in-memory database for testing
engine = create_engine("sqlite:///:memory:", echo=True)

def setup_test_data():
    """Set up test database and create sample data"""
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create a test user
        test_user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            name="Test User"
        )
        session.add(test_user)
        session.commit()

        # Create sample tasks
        sample_tasks = [
            TaskCreate(
                title="Complete project proposal",
                description="Finish the project proposal document and send for review",
                priority=PriorityEnum.HIGH,
                timestamp=datetime.utcnow() - timedelta(days=1),
                status=False
            ),
            TaskCreate(
                title="Fix authentication bug",
                description="Resolve the login issue reported by users",
                priority=PriorityEnum.CRITICAL,
                timestamp=datetime.utcnow(),
                status=True
            ),
            TaskCreate(
                title="Update documentation",
                description="Update API documentation with new endpoints",
                priority=PriorityEnum.MEDIUM,
                timestamp=datetime.utcnow() + timedelta(days=1),
                status=False
            ),
            TaskCreate(
                title="Code review",
                description="Review pull requests from team members",
                priority=PriorityEnum.LOW,
                timestamp=datetime.utcnow() - timedelta(days=2),
                status=False
            )
        ]

        # Create tasks for the user
        for task_data in sample_tasks:
            create_task(session, str(test_user.id), task_data)

        return str(test_user.id)

def test_search_functionality(user_id):
    """Test search functionality for title and description"""
    print("Testing search functionality...")

    with Session(engine) as session:
        # Test search in title
        results = get_tasks_for_user(session, user_id, search="project")
        print(f"Search 'project': Found {len(results)} tasks")
        for task in results:
            print(f"  - {task.title}")

        # Test search in description
        results = get_tasks_for_user(session, user_id, search="login")
        print(f"Search 'login': Found {len(results)} tasks")
        for task in results:
            print(f"  - {task.title}")

        # Test case-insensitive search
        results = get_tasks_for_user(session, user_id, search="PROJECT")  # Uppercase
        print(f"Search 'PROJECT' (uppercase): Found {len(results)} tasks")
        for task in results:
            print(f"  - {task.title}")

def test_status_filtering(user_id):
    """Test status filtering"""
    print("\nTesting status filtering...")

    with Session(engine) as session:
        # Test completed tasks
        results = get_tasks_for_user(session, user_id, status_filter="complete")
        print(f"Status 'complete': Found {len(results)} tasks")
        for task in results:
            print(f"  - {task.title} (Status: {task.status})")

        # Test incomplete tasks
        results = get_tasks_for_user(session, user_id, status_filter="incomplete")
        print(f"Status 'incomplete': Found {len(results)} tasks")
        for task in results:
            print(f"  - {task.title} (Status: {task.status})")

def test_priority_filtering(user_id):
    """Test priority filtering"""
    print("\nTesting priority filtering...")

    with Session(engine) as session:
        # Test high priority
        results = get_tasks_for_user(session, user_id, priority="High")
        print(f"Priority 'High': Found {len(results)} tasks")
        for task in results:
            print(f"  - {task.title} (Priority: {task.priority})")

def test_timestamp_filtering(user_id):
    """Test timestamp range filtering"""
    print("\nTesting timestamp filtering...")

    with Session(engine) as session:
        # Test tasks from the past
        results = get_tasks_for_user(
            session,
            user_id,
            timestamp_from=datetime.utcnow() - timedelta(days=5),
            timestamp_to=datetime.utcnow() - timedelta(hours=1)
        )
        print(f"Timestamp range (past): Found {len(results)} tasks")
        for task in results:
            print(f"  - {task.title} (Timestamp: {task.timestamp})")

def test_combined_filters(user_id):
    """Test combined filter functionality"""
    print("\nTesting combined filters...")

    with Session(engine) as session:
        # Test search + status
        results = get_tasks_for_user(
            session,
            user_id,
            search="project",
            status_filter="incomplete"
        )
        print(f"Search 'project' + Status 'incomplete': Found {len(results)} tasks")
        for task in results:
            print(f"  - {task.title} (Status: {task.status})")

def run_tests():
    """Run all tests"""
    print("Setting up test data...")
    user_id = setup_test_data()

    print("Running filter tests...\n")

    test_search_functionality(user_id)
    test_status_filtering(user_id)
    test_priority_filtering(user_id)
    test_timestamp_filtering(user_id)
    test_combined_filters(user_id)

    print("\nAll tests completed!")

if __name__ == "__main__":
    run_tests()