"""
Task service for the Speckit Plus Todo Application
Handles business logic for task operations
"""

import uuid
from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.task import Task, TaskComplete, TaskCreate, TaskUpdate
from models.user import User


def create_task(session: Session, user_id: str, task_data: TaskCreate) -> Task:
    """
    Create a new task for a user
    """
    # Validate user exists
    user = session.get(User, uuid.UUID(user_id))
    if not user:
        raise ValueError("User not found")

    # Create task object
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        timestamp=task_data.timestamp,
        status=task_data.status,
        user_id=uuid.UUID(user_id),
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def get_tasks_for_user(
    session: Session,
    user_id: str,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    status_filter: Optional[str] = None,
    timestamp_from: Optional[datetime] = None,
    timestamp_to: Optional[datetime] = None,
    page: int = 1,
    limit: int = 20,
):
    """
    Get all tasks for a user with optional filters and return both tasks and total count for pagination
    """
    user_uuid = uuid.UUID(user_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Build base query with selectinload for user relationship to prevent N+1
    base_query = select(Task).options(selectinload(Task.user)).where(Task.user_id == user_uuid)

    # Apply filters to base query
    if search:
        # Use case-insensitive search for better user experience
        search_lower = search.lower()
        base_query = base_query.where(
            (func.lower(Task.title).contains(search_lower)) | (func.lower(Task.description).contains(search_lower))
        )
    if priority:
        base_query = base_query.where(Task.priority == priority)
    if status_filter:
        if status_filter.lower() in ["complete", "completed", "true", "1"]:
            base_query = base_query.where(Task.status == True)
        elif status_filter.lower() in ["incomplete", "pending", "false", "0"]:
            base_query = base_query.where(Task.status == False)
    if timestamp_from:
        base_query = base_query.where(Task.timestamp >= timestamp_from)
    if timestamp_to:
        base_query = base_query.where(Task.timestamp <= timestamp_to)

    # Count total records for pagination
    count_query = select(func.count()).select_from(base_query.subquery())
    total_count = session.exec(count_query).one()

    # Apply pagination to the main query
    offset = (page - 1) * limit
    paginated_query = base_query.offset(offset).limit(limit)

    tasks = session.exec(paginated_query).all()

    return tasks, total_count


def get_task_by_id(session: Session, user_id: str, task_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a user
    """
    user_uuid = uuid.UUID(user_id)
    task_uuid = uuid.UUID(task_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get task and verify it belongs to the user using a single query
    query = select(Task).options(selectinload(Task.user)).where(
        Task.id == task_uuid,
        Task.user_id == user_uuid
    )
    task = session.exec(query).first()

    return task


def update_task(
    session: Session, user_id: str, task_id: str, task_data: TaskUpdate
) -> Optional[Task]:
    """
    Update a task for a user
    """
    user_uuid = uuid.UUID(user_id)
    task_uuid = uuid.UUID(task_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get task and verify it belongs to the user using a single query
    query = select(Task).options(selectinload(Task.user)).where(
        Task.id == task_uuid,
        Task.user_id == user_uuid
    )
    task = session.exec(query).first()

    if not task:
        return None

    # Update task with provided data
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, user_id: str, task_id: str) -> bool:
    """
    Delete a task for a user
    """
    user_uuid = uuid.UUID(user_id)
    task_uuid = uuid.UUID(task_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get task and verify it belongs to the user using a single query
    query = select(Task).where(
        Task.id == task_uuid,
        Task.user_id == user_uuid
    )
    task = session.exec(query).first()

    if not task:
        return False

    session.delete(task)
    session.commit()

    return True


def toggle_task_completion(
    session: Session, user_id: str, task_id: str, complete: bool
) -> Optional[Task]:
    """
    Toggle task completion status
    """
    user_uuid = uuid.UUID(user_id)
    task_uuid = uuid.UUID(task_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get task and verify it belongs to the user using a single query
    query = select(Task).options(selectinload(Task.user)).where(
        Task.id == task_uuid,
        Task.user_id == user_uuid
    )
    task = session.exec(query).first()

    if not task:
        return None

    # Update completion status
    task.status = complete
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return task
