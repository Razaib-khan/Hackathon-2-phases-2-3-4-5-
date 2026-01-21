"""
MCP Tool for deleting tasks via AI agent
Implements the delete_tasks functionality for the AI agent to remove tasks
"""

from typing import Dict, List, Any, Optional
from uuid import UUID
import asyncio

from ...models.task import Task
from ...services.task_service import delete_tasks_batch
from ...database.database import engine
from sqlmodel import Session


async def delete_tasks(
    user_id: str,
    task_ids: List[str]
) -> Dict[str, Any]:
    """
    Delete one or multiple tasks for a user via the AI agent

    Args:
        user_id: The ID of the user deleting the tasks
        task_ids: List of task IDs to delete

    Returns:
        Dictionary with success status, number of deleted tasks, and any errors
    """
    try:
        # Validate input
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "deleted_count": 0,
                "errors": ["User ID is required"]
            }

        if not task_ids or not isinstance(task_ids, list):
            return {
                "success": False,
                "error": "Task IDs list is required",
                "deleted_count": 0,
                "errors": ["Task IDs list is required"]
            }

        # Validate task IDs
        errors = []
        valid_task_ids = []

        for i, task_id in enumerate(task_ids):
            if not isinstance(task_id, str):
                errors.append(f"Task ID {i}: Invalid format")
                continue

            try:
                # Validate UUID format
                UUID(task_id)
                valid_task_ids.append(task_id)
            except ValueError:
                errors.append(f"Task ID {i}: Invalid UUID format")

        if errors:
            return {
                "success": False,
                "error": "Some task IDs had validation errors",
                "deleted_count": 0,
                "errors": errors
            }

        # Delete tasks from database
        from concurrent.futures import ThreadPoolExecutor

        def _delete_tasks_sync():
            with Session(engine) as session:
                return delete_tasks_batch(session, user_id, valid_task_ids)

        loop = asyncio.get_event_loop()
        deleted_count = await loop.run_in_executor(None, _delete_tasks_sync)

        return {
            "success": True,
            "deleted_count": deleted_count,
            "errors": errors
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete tasks: {str(e)}",
            "deleted_count": 0,
            "errors": [f"Unexpected error: {str(e)}"]
        }