"""
MCP Tool for updating tasks via AI agent
Implements the update_tasks functionality for the AI agent to modify tasks
"""

from typing import Dict, List, Any, Optional
from uuid import UUID
import asyncio

from ...models.task import Task, TaskUpdate
from ...services.task_service import update_tasks_batch
from ...database.database import engine
from sqlmodel import Session
from ...utils.errors import (
    validate_required_fields,
    validate_field_length,
    validate_priority,
    validate_uuid_format,
    validate_boolean,
    handle_error,
    ValidationError
)


async def update_tasks(
    user_id: str,
    task_updates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update one or multiple tasks for a user via the AI agent

    Args:
        user_id: The ID of the user updating the tasks
        task_updates: List of dictionaries containing task IDs and the fields to update

    Returns:
        Dictionary with success status, updated tasks, and any errors
    """
    try:
        # Validate input
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "error_code": "VALIDATION_ERROR",
                "updated_tasks": [],
                "errors": ["User ID is required"]
            }

        if not task_updates or not isinstance(task_updates, list):
            return {
                "success": False,
                "error": "Task updates list is required",
                "error_code": "VALIDATION_ERROR",
                "updated_tasks": [],
                "errors": ["Task updates list is required"]
            }

        # Validate update data
        errors = []
        valid_updates = []

        for i, update_data in enumerate(task_updates):
            if not isinstance(update_data, dict):
                errors.append(f"Update {i}: Invalid data format")
                continue

            # Validate required fields
            missing_fields = validate_required_fields(update_data, ["id"])
            if missing_fields:
                errors.extend([f"Update {i}: {field} is required" for field in missing_fields])
                continue

            task_id = update_data.get('id')

            # Validate UUID format
            uuid_errors = validate_uuid_format(task_id, f"Update {i} task ID")
            if uuid_errors:
                errors.extend(uuid_errors)
                continue

            # Make sure we only allow valid fields to be updated
            valid_fields = {'id', 'title', 'description', 'priority', 'status', 'timestamp'}
            filtered_update = {}

            for k, v in update_data.items():
                if k not in valid_fields:
                    continue

                # Perform field-specific validation
                if k == 'title' and v is not None:
                    title_errors = validate_field_length(v, f"Update {i} title", min_length=1, max_length=200)
                    if title_errors:
                        errors.extend(title_errors)
                        continue
                    filtered_update[k] = v
                elif k == 'description' and v is not None:
                    desc_errors = validate_field_length(v, f"Update {i} description", max_length=1000)
                    if desc_errors:
                        errors.extend(desc_errors)
                        continue
                    filtered_update[k] = v
                elif k == 'priority' and v is not None:
                    priority_errors = validate_priority(v)
                    if priority_errors:
                        errors.extend([f"Update {i}: {error}" for error in priority_errors])
                        continue
                    filtered_update[k] = v
                elif k == 'status' and v is not None:
                    status_errors = validate_boolean(v, f"Update {i} status")
                    if status_errors:
                        errors.extend(status_errors)
                        continue
                    # Convert string boolean representations
                    if isinstance(v, str):
                        if v.lower() in ['true', '1', 'yes', 'on']:
                            filtered_update[k] = True
                        elif v.lower() in ['false', '0', 'no', 'off']:
                            filtered_update[k] = False
                    else:
                        filtered_update[k] = v
                elif k in {'id', 'timestamp'}:
                    filtered_update[k] = v

            if not filtered_update:
                errors.append(f"Update {i}: No valid fields to update")
                continue

            valid_updates.append(filtered_update)

        if errors:
            return {
                "success": False,
                "error": "Some updates had validation errors",
                "error_code": "VALIDATION_ERROR",
                "updated_tasks": [],
                "errors": errors
            }

        # Update tasks in database
        from concurrent.futures import ThreadPoolExecutor

        def _update_tasks_sync():
            with Session(engine) as session:
                return update_tasks_batch(session, user_id, valid_updates)

        loop = asyncio.get_event_loop()
        updated_tasks = await loop.run_in_executor(None, _update_tasks_sync)

        return {
            "success": True,
            "updated_tasks": [task.dict() for task in updated_tasks],
            "errors": errors
        }

    except Exception as e:
        return handle_error(e)