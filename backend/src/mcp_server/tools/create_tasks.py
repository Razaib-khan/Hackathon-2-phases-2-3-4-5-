"""
MCP Tool for creating tasks via AI agent
Implements the create_tasks functionality for the AI agent to interact with the task system
"""

from typing import Dict, List, Any, Optional
from uuid import UUID
import asyncio
from contextlib import contextmanager

from ...models.task import TaskCreate
from ...services.task_service import create_tasks_batch
from ...database.database import engine
from sqlmodel import Session
from ...utils.errors import (
    validate_required_fields,
    validate_field_length,
    validate_priority,
    handle_error,
    ValidationError
)


async def create_tasks(
    user_id: str,
    tasks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create one or multiple tasks for a user via the AI agent

    Args:
        user_id: The ID of the user creating the tasks
        tasks: List of task data containing title, description, priority, etc.

    Returns:
        Dictionary with success status, created tasks, and any errors
    """
    try:
        # Validate input
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "error_code": "VALIDATION_ERROR",
                "created_tasks": [],
                "errors": ["User ID is required"]
            }

        if not tasks or not isinstance(tasks, list):
            return {
                "success": False,
                "error": "Tasks list is required",
                "error_code": "VALIDATION_ERROR",
                "created_tasks": [],
                "errors": ["Tasks list is required"]
            }

        # Prepare task objects
        task_objects = []
        errors = []

        for i, task_data in enumerate(tasks):
            try:
                if not isinstance(task_data, dict):
                    errors.append(f"Task {i}: Invalid data format")
                    continue

                # Validate required fields
                missing_fields = validate_required_fields(task_data, ["title"])
                if missing_fields:
                    errors.extend([f"Task {i}: {field} is required" for field in missing_fields])
                    continue

                # Validate field lengths
                title_errors = validate_field_length(task_data.get("title", ""), f"Task {i} title", min_length=1, max_length=200)
                description_errors = validate_field_length(task_data.get("description", ""), f"Task {i} description", max_length=1000)

                if title_errors or description_errors:
                    errors.extend(title_errors)
                    errors.extend(description_errors)
                    continue

                # Validate priority
                priority_errors = validate_priority(task_data.get("priority", "Medium"))
                if priority_errors:
                    errors.extend([f"Task {i}: {error}" for error in priority_errors])
                    continue

                # Validate status if provided
                status = task_data.get("status")
                if status is not None and not isinstance(status, bool):
                    # Try to convert common boolean representations
                    if isinstance(status, str):
                        if status.lower() in ['true', '1', 'yes', 'on']:
                            status = True
                        elif status.lower() in ['false', '0', 'no', 'off']:
                            status = False
                        else:
                            errors.append(f"Task {i}: Status must be a boolean value")
                            continue
                    else:
                        errors.append(f"Task {i}: Status must be a boolean value")
                        continue

                # Create TaskCreate object
                task_obj = TaskCreate(
                    title=task_data.get("title"),
                    description=task_data.get("description", ""),
                    priority=task_data.get("priority", "Medium"),
                    timestamp=task_data.get("timestamp"),
                    status=status if status is not None else False
                )
                task_objects.append(task_obj)

            except ValidationError as ve:
                errors.append(f"Task {i}: Validation error - {ve.message}")
            except Exception as e:
                errors.append(f"Task {i}: Invalid data - {str(e)}")

        if errors:
            return {
                "success": False,
                "error": "Some tasks had validation errors",
                "error_code": "VALIDATION_ERROR",
                "created_tasks": [],
                "errors": errors
            }

        # Create tasks in database
        # Since the function is async but the service is sync, we run it in a thread
        from concurrent.futures import ThreadPoolExecutor
        import asyncio

        def _create_tasks_sync():
            with Session(engine) as session:
                return create_tasks_batch(session, user_id, task_objects)

        loop = asyncio.get_event_loop()
        created_tasks = await loop.run_in_executor(None, _create_tasks_sync)

        return {
            "success": True,
            "created_tasks": [task.dict() for task in created_tasks],
            "errors": errors
        }

    except Exception as e:
        return handle_error(e)