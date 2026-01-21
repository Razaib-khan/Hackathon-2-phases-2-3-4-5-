"""
MCP Tool for updating task statuses via AI agent
Implements the update_tasks_status functionality for the AI agent to modify task completion status
"""

from typing import Dict, List, Any, Optional
from uuid import UUID
import asyncio

from ...models.task import Task
from ...services.task_service import update_tasks_status_batch
from ...database.database import engine
from sqlmodel import Session


async def update_tasks_status(
    user_id: str,
    task_status_updates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update the status of one or multiple tasks for a user via the AI agent

    Args:
        user_id: The ID of the user updating the task statuses
        task_status_updates: List of dictionaries containing task IDs and their new status values

    Returns:
        Dictionary with success status, updated tasks, and any errors
    """
    try:
        # Validate input
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "updated_tasks": [],
                "errors": ["User ID is required"]
            }

        if not task_status_updates or not isinstance(task_status_updates, list):
            return {
                "success": False,
                "error": "Task status updates list is required",
                "updated_tasks": [],
                "errors": ["Task status updates list is required"]
            }

        # Validate update data
        errors = []
        valid_updates = []

        for i, update_data in enumerate(task_status_updates):
            if not isinstance(update_data, dict):
                errors.append(f"Update {i}: Invalid data format")
                continue

            task_id = update_data.get('id')
            status = update_data.get('status')

            if not task_id:
                errors.append(f"Update {i}: Task ID is required")
                continue

            if status is None:
                errors.append(f"Update {i}: Status is required")
                continue

            if not isinstance(status, bool):
                # Try to convert common boolean representations
                if isinstance(status, str):
                    if status.lower() in ['true', '1', 'yes', 'on']:
                        status = True
                    elif status.lower() in ['false', '0', 'no', 'off']:
                        status = False
                    else:
                        errors.append(f"Update {i}: Invalid status value '{status}'. Must be a boolean.")
                        continue
                else:
                    errors.append(f"Update {i}: Status must be a boolean value")
                    continue

            # Validate UUID format
            try:
                UUID(task_id)
            except ValueError:
                errors.append(f"Update {i}: Invalid UUID format for task ID")
                continue

            valid_updates.append({
                'id': task_id,
                'status': status
            })

        if errors:
            return {
                "success": False,
                "error": "Some updates had validation errors",
                "updated_tasks": [],
                "errors": errors
            }

        # Update task statuses in database
        from concurrent.futures import ThreadPoolExecutor

        def _update_tasks_status_sync():
            with Session(engine) as session:
                return update_tasks_status_batch(session, user_id, valid_updates)

        loop = asyncio.get_event_loop()
        updated_tasks = await loop.run_in_executor(None, _update_tasks_status_sync)

        return {
            "success": True,
            "updated_tasks": [task.dict() for task in updated_tasks],
            "errors": errors
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update task statuses: {str(e)}",
            "updated_tasks": [],
            "errors": [f"Unexpected error: {str(e)}"]
        }