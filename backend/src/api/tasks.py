"""
Tasks API routes for the Speckit Plus Todo Application
Handles CRUD operations for tasks with user isolation
"""

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_session
from models.task import Task, TaskComplete, TaskCreate, TaskRead, TaskUpdate
from models.user import User
from services.task_service import (
    create_task,
    delete_task,
    get_task_by_id,
    get_tasks_for_user,
    toggle_task_completion,
    update_task,
)
from utils.validation import validate_user_id, validate_task_id
from utils.auth import get_current_user
from middleware.security import limiter

router = APIRouter()


from typing import Dict, Any

@router.get("/{user_id}/tasks", response_model=Dict[str, Any])
def get_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    search: Optional[str] = Query(
        None, description="Search keywords in title and description"
    ),
    priority: Optional[str] = Query(None, description="Filter by priority level"),
    status_filter: Optional[str] = Query(
        None, description="Filter by completion status"
    ),
    timestamp_from: Optional[datetime] = Query(
        None, description="Filter from timestamp"
    ),
    timestamp_to: Optional[datetime] = Query(None, description="Filter to timestamp"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """
    Retrieve all tasks for a user with optional search and filtering
    """
    # Validate user_id format
    user_uuid = validate_user_id(user_id)

    # Verify that the requested user_id matches the authenticated user
    if str(current_user.id) != str(user_uuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    # Get tasks using service
    try:
        tasks = get_tasks_for_user(
            session=session,
            user_id=str(user_uuid),
            search=search,
            priority=priority,
            status_filter=status_filter,
            timestamp_from=timestamp_from,
            timestamp_to=timestamp_to,
            page=page,
            limit=limit,
        )

        # Return response in format expected by frontend
        tasks_list, total_count = tasks
        return {
            "tasks": tasks_list,
            "total": total_count,
            "page": page,
            "limit": limit
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task_endpoint(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for a user
    """
    # Validate user_id format
    user_uuid = validate_user_id(user_id)

    # Verify that the requested user_id matches the authenticated user
    if str(current_user.id) != str(user_uuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create task using service
    try:
        task = create_task(session, str(user_uuid), task_data)
        return task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task for a user
    """
    # Validate user_id format
    user_uuid = validate_user_id(user_id)

    # Validate task_id format
    task_uuid = validate_task_id(task_id)

    # Verify that the requested user_id matches the authenticated user
    if str(current_user.id) != str(user_uuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    # Get task using service
    task = get_task_by_id(session, str(user_uuid), str(task_uuid))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a task for a user
    """
    # Validate user_id format
    user_uuid = validate_user_id(user_id)

    # Validate task_id format
    task_uuid = validate_task_id(task_id)

    # Verify that the requested user_id matches the authenticated user
    if str(current_user.id) != str(user_uuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    # Update task using service
    updated_task = update_task(session, str(user_uuid), str(task_uuid), task_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task_endpoint(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task for a user
    """
    # Validate user_id format
    user_uuid = validate_user_id(user_id)

    # Validate task_id format
    task_uuid = validate_task_id(task_id)

    # Verify that the requested user_id matches the authenticated user
    if str(current_user.id) != str(user_uuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user's tasks"
        )

    # Delete task using service
    success = delete_task(session, str(user_uuid), str(task_uuid))
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete")
def toggle_task_completion_endpoint(
    user_id: str,
    task_id: str,
    task_complete: TaskComplete,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status
    """
    # Validate user_id format
    user_uuid = validate_user_id(user_id)

    # Validate task_id format
    task_uuid = validate_task_id(task_id)

    # Verify that the requested user_id matches the authenticated user
    if str(current_user.id) != str(user_uuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this user's tasks"
        )

    # Toggle completion using service
    updated_task = toggle_task_completion(
        session, str(user_uuid), str(task_uuid), task_complete.complete
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task
