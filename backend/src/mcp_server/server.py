"""
MCP Server for AI Agent Task Management
Implements the MCP protocol to connect the AI agent with task management operations
"""

import asyncio
import json
from typing import Dict, Any, List
from mcp.server import Server
from mcp.server.exceptions import McpError
from pydantic import AnyUrl
import logging

# Import the task operation tools
from .tools.create_tasks import create_tasks
from .tools.read_tasks import read_tasks
from .tools.update_tasks import update_tasks
from .tools.delete_tasks import delete_tasks
from .tools.update_tasks_status import update_tasks_status

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
server = Server("aido-todo-ai-agent")


@server.after_connect
async def setup_logging(context):
    """Set up logging after connection is established."""
    logger.info("MCP server connected and ready for task operations")


# Tool for creating tasks
@server.tool("create-tasks")
def create_tasks_tool(
    user_id: str,
    tasks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create one or multiple tasks for a user

    Args:
        user_id: The ID of the user creating the tasks
        tasks: List of task data containing title, description, priority, etc.

    Returns:
        Dictionary with success status, created tasks, and any errors
    """
    logger.info(f"Creating tasks for user {user_id}")

    try:
        # Run the async function synchronously for the tool
        import asyncio
        import threading

        # Create a new event loop if none exists in this thread
        try:
            loop = asyncio.get_running_loop()
            # If we're already in a loop, run in executor
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, create_tasks(user_id, tasks))
                result = future.result()
        except RuntimeError:
            # No event loop, safe to run
            result = asyncio.run(create_tasks(user_id, tasks))

        logger.info(f"Successfully created tasks for user {user_id}: {len(result.get('created_tasks', []))} created")
        return result
    except Exception as e:
        logger.error(f"Error creating tasks for user {user_id}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to create tasks: {str(e)}",
            "created_tasks": [],
            "errors": [f"Unexpected error: {str(e)}"]
        }


# Tool for reading tasks
@server.tool("read-tasks")
def read_tasks_tool(
    user_id: str,
    task_ids: List[str] = None,
    filters: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Read one or multiple tasks for a user

    Args:
        user_id: The ID of the user reading the tasks
        task_ids: Optional list of specific task IDs to retrieve
        filters: Optional filters for broader task retrieval (priority, status, search, etc.)

    Returns:
        Dictionary with success status, tasks, and any errors
    """
    logger.info(f"Reading tasks for user {user_id}")

    try:
        # Run the async function synchronously for the tool
        import asyncio
        import threading

        # Create a new event loop if none exists in this thread
        try:
            loop = asyncio.get_running_loop()
            # If we're already in a loop, run in executor
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, read_tasks(user_id, task_ids, filters))
                result = future.result()
        except RuntimeError:
            # No event loop, safe to run
            result = asyncio.run(read_tasks(user_id, task_ids, filters))

        logger.info(f"Successfully read tasks for user {user_id}: {result.get('total_count', 0)} tasks retrieved")
        return result
    except Exception as e:
        logger.error(f"Error reading tasks for user {user_id}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to read tasks: {str(e)}",
            "tasks": [],
            "total_count": 0
        }


# Tool for updating tasks
@server.tool("update-tasks")
def update_tasks_tool(
    user_id: str,
    task_updates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update one or multiple tasks for a user

    Args:
        user_id: The ID of the user updating the tasks
        task_updates: List of dictionaries containing task IDs and the fields to update

    Returns:
        Dictionary with success status, updated tasks, and any errors
    """
    logger.info(f"Updating tasks for user {user_id}")

    try:
        # Run the async function synchronously for the tool
        import asyncio
        import threading

        # Create a new event loop if none exists in this thread
        try:
            loop = asyncio.get_running_loop()
            # If we're already in a loop, run in executor
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, update_tasks(user_id, task_updates))
                result = future.result()
        except RuntimeError:
            # No event loop, safe to run
            result = asyncio.run(update_tasks(user_id, task_updates))

        logger.info(f"Successfully updated tasks for user {user_id}: {len(result.get('updated_tasks', []))} updated")
        return result
    except Exception as e:
        logger.error(f"Error updating tasks for user {user_id}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to update tasks: {str(e)}",
            "updated_tasks": [],
            "errors": [f"Unexpected error: {str(e)}"]
        }


# Tool for deleting tasks
@server.tool("delete-tasks")
def delete_tasks_tool(
    user_id: str,
    task_ids: List[str]
) -> Dict[str, Any]:
    """
    Delete one or multiple tasks for a user

    Args:
        user_id: The ID of the user deleting the tasks
        task_ids: List of task IDs to delete

    Returns:
        Dictionary with success status, number of deleted tasks, and any errors
    """
    logger.info(f"Deleting tasks for user {user_id}")

    try:
        # Run the async function synchronously for the tool
        import asyncio
        import threading

        # Create a new event loop if none exists in this thread
        try:
            loop = asyncio.get_running_loop()
            # If we're already in a loop, run in executor
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, delete_tasks(user_id, task_ids))
                result = future.result()
        except RuntimeError:
            # No event loop, safe to run
            result = asyncio.run(delete_tasks(user_id, task_ids))

        logger.info(f"Successfully deleted tasks for user {user_id}: {result.get('deleted_count', 0)} deleted")
        return result
    except Exception as e:
        logger.error(f"Error deleting tasks for user {user_id}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to delete tasks: {str(e)}",
            "deleted_count": 0,
            "errors": [f"Unexpected error: {str(e)}"]
        }


# Tool for updating task statuses
@server.tool("update-tasks-status")
def update_tasks_status_tool(
    user_id: str,
    task_status_updates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update the status of one or multiple tasks for a user

    Args:
        user_id: The ID of the user updating the task statuses
        task_status_updates: List of dictionaries containing task IDs and their new status values

    Returns:
        Dictionary with success status, updated tasks, and any errors
    """
    logger.info(f"Updating task statuses for user {user_id}")

    try:
        # Run the async function synchronously for the tool
        import asyncio
        import threading

        # Create a new event loop if none exists in this thread
        try:
            loop = asyncio.get_running_loop()
            # If we're already in a loop, run in executor
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, update_tasks_status(user_id, task_status_updates))
                result = future.result()
        except RuntimeError:
            # No event loop, safe to run
            result = asyncio.run(update_tasks_status(user_id, task_status_updates))

        logger.info(f"Successfully updated task statuses for user {user_id}: {len(result.get('updated_tasks', []))} updated")
        return result
    except Exception as e:
        logger.error(f"Error updating task statuses for user {user_id}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to update task statuses: {str(e)}",
            "updated_tasks": [],
            "errors": [f"Unexpected error: {str(e)}"]
        }


async def main():
    """Main entry point for the MCP server."""
    import stdio
    from mcp.shared.stdio import run_stdio_server

    # Run the server using stdin/stdout
    async with run_stdio_server(server) as shutdown:
        logger.info("AIDO Todo AI Agent MCP Server is running...")
        logger.info("Ready to handle AI agent task operations")
        await shutdown


if __name__ == "__main__":
    asyncio.run(main())