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


def create_tasks_batch(
    session: Session, user_id: str, tasks_data: List[TaskCreate]
) -> List[Task]:
    """
    Create multiple tasks for a user at once (for AI agent operations)
    """
    user_uuid = uuid.UUID(user_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    created_tasks = []
    for task_data in tasks_data:
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            timestamp=task_data.timestamp or datetime.utcnow(),
            status=task_data.status or False,
            user_id=user_uuid,
        )
        session.add(db_task)
        created_tasks.append(db_task)

    session.commit()

    # Refresh all created tasks to get their IDs
    for task in created_tasks:
        session.refresh(task)

    return created_tasks


def get_tasks_by_ids(
    session: Session, user_id: str, task_ids: List[str]
) -> List[Task]:
    """
    Get multiple tasks by their IDs for a user
    """
    user_uuid = uuid.UUID(user_id)
    task_uuids = [uuid.UUID(task_id) for task_id in task_ids]

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get tasks and verify they belong to the user
    query = select(Task).options(selectinload(Task.user)).where(
        Task.id.in_(task_uuids),
        Task.user_id == user_uuid
    )
    tasks = session.exec(query).all()

    return tasks


def update_tasks_batch(
    session: Session, user_id: str, task_updates: List[dict]
) -> List[Task]:
    """
    Update multiple tasks for a user at once (for AI agent operations)
    """
    user_uuid = uuid.UUID(user_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    updated_tasks = []
    for update_data in task_updates:
        task_id = update_data.get("id")
        if not task_id:
            continue

        task_uuid = uuid.UUID(task_id)

        # Get task and verify it belongs to the user
        query = select(Task).options(selectinload(Task.user)).where(
            Task.id == task_uuid,
            Task.user_id == user_uuid
        )
        task = session.exec(query).first()

        if not task:
            continue

        # Update task with provided data
        for field, value in update_data.items():
            if field != "id":  # Don't update the ID
                if hasattr(task, field):
                    setattr(task, field, value)
        task.updated_at = datetime.utcnow()

        session.add(task)
        updated_tasks.append(task)

    session.commit()

    # Refresh all updated tasks
    for task in updated_tasks:
        session.refresh(task)

    return updated_tasks


def delete_tasks_batch(
    session: Session, user_id: str, task_ids: List[str]
) -> int:
    """
    Delete multiple tasks for a user at once (for AI agent operations)
    """
    user_uuid = uuid.UUID(user_id)
    task_uuids = [uuid.UUID(task_id) for task_id in task_ids]

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get tasks and verify they belong to the user
    query = select(Task).where(
        Task.id.in_(task_uuids),
        Task.user_id == user_uuid
    )
    tasks = session.exec(query).all()

    deleted_count = 0
    for task in tasks:
        session.delete(task)
        deleted_count += 1

    session.commit()
    return deleted_count


def update_tasks_status_batch(
    session: Session, user_id: str, task_status_updates: List[dict]
) -> List[Task]:
    """
    Update status of multiple tasks for a user at once (for AI agent operations)
    """
    user_uuid = uuid.UUID(user_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    updated_tasks = []
    for update_data in task_status_updates:
        task_id = update_data.get("id")
        status = update_data.get("status")

        if not task_id or status is None:
            continue

        task_uuid = uuid.UUID(task_id)

        # Get task and verify it belongs to the user
        query = select(Task).options(selectinload(Task.user)).where(
            Task.id == task_uuid,
            Task.user_id == user_uuid
        )
        task = session.exec(query).first()

        if not task:
            continue

        # Update task status
        task.status = status
        task.updated_at = datetime.utcnow()

        session.add(task)
        updated_tasks.append(task)

    session.commit()

    # Refresh all updated tasks
    for task in updated_tasks:
        session.refresh(task)

    return updated_tasks
