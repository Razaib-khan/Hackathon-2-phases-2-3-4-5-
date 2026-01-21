"""
MCP Tool for reading tasks via AI agent
Implements the read_tasks functionality for the AI agent to retrieve tasks
"""

from typing import Dict, List, Any, Optional
from uuid import UUID
import asyncio

from ...models.task import Task
from ...services.task_service import get_tasks_by_ids, get_tasks_for_user
from ...database.database import engine
from sqlmodel import Session


async def read_tasks(
    user_id: str,
    task_ids: Optional[List[str]] = None,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Read one or multiple tasks for a user via the AI agent

    Args:
        user_id: The ID of the user reading the tasks
        task_ids: Optional list of specific task IDs to retrieve
        filters: Optional filters for broader task retrieval (priority, status, search, etc.)

    Returns:
        Dictionary with success status, tasks, and any errors
    """
    try:
        # Validate input
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "tasks": [],
                "total_count": 0
            }

        # If specific task IDs are provided, retrieve those
        if task_ids and isinstance(task_ids, list) and len(task_ids) > 0:
            # Get specific tasks by IDs
            from concurrent.futures import ThreadPoolExecutor

            def _get_tasks_by_ids_sync():
                with Session(engine) as session:
                    return get_tasks_by_ids(session, user_id, task_ids)

            loop = asyncio.get_event_loop()
            tasks = await loop.run_in_executor(None, _get_tasks_by_ids_sync)

            return {
                "success": True,
                "tasks": [task.dict() for task in tasks],
                "total_count": len(tasks)
            }

        # Otherwise, use filters for broader search
        filters = filters or {}

        # Extract filter parameters
        search = filters.get('search')
        priority = filters.get('priority')
        status = filters.get('status')
        # Add more filters as needed

        def _get_filtered_tasks_sync():
            with Session(engine) as session:
                # For this basic implementation, we'll use page 1 and default limit
                tasks, total_count = get_tasks_for_user(
                    session, user_id,
                    search=search,
                    priority=priority,
                    status_filter=status,
                    page=1,
                    limit=100  # Reasonable limit for AI agent
                )
                return tasks, total_count

        loop = asyncio.get_event_loop()
        tasks, total_count = await loop.run_in_executor(None, _get_filtered_tasks_sync)

        return {
            "success": True,
            "tasks": [task.dict() for task in tasks],
            "total_count": total_count
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to read tasks: {str(e)}",
            "tasks": [],
            "total_count": 0
        }