"""
Task Operations Handlers for AI Agent
Handles the processing of AI agent requests and connects them to the appropriate MCP tools
"""

import logging
from typing import Dict, Any, List, Optional
from .agent import AIDOTodoAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskOperationsHandler:
    """
    Handler for AI agent task operations
    Processes AI agent requests and connects them to the appropriate MCP tools
    """

    def __init__(self, agent: AIDOTodoAgent):
        """
        Initialize the task operations handler

        Args:
            agent: The AIDO Todo Agent instance
        """
        self.agent = agent

    async def handle_create_tasks_request(self, user_id: str, tasks_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle a request to create tasks

        Args:
            user_id: The ID of the user creating the tasks
            tasks_data: List of task data to create

        Returns:
            Result of the create operation
        """
        logger.info(f"Handling create tasks request for user {user_id}")

        try:
            result = await self.agent.create_tasks(user_id, tasks_data)
            logger.info(f"Create tasks request completed for user {user_id}: {len(result.get('created_tasks', []))} tasks created")
            return result
        except Exception as e:
            logger.error(f"Error handling create tasks request for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "created_tasks": [],
                "errors": [str(e)]
            }

    async def handle_read_tasks_request(self, user_id: str, task_ids: List[str] = None, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle a request to read tasks

        Args:
            user_id: The ID of the user reading the tasks
            task_ids: Optional list of specific task IDs to retrieve
            filters: Optional filters for broader task retrieval

        Returns:
            Result of the read operation
        """
        logger.info(f"Handling read tasks request for user {user_id}")

        try:
            result = await self.agent.read_tasks(user_id, task_ids, filters)
            logger.info(f"Read tasks request completed for user {user_id}: {result.get('total_count', 0)} tasks retrieved")
            return result
        except Exception as e:
            logger.error(f"Error handling read tasks request for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tasks": [],
                "total_count": 0
            }

    async def handle_update_tasks_request(self, user_id: str, task_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle a request to update tasks

        Args:
            user_id: The ID of the user updating the tasks
            task_updates: List of task updates to apply

        Returns:
            Result of the update operation
        """
        logger.info(f"Handling update tasks request for user {user_id}")

        try:
            result = await self.agent.update_tasks(user_id, task_updates)
            logger.info(f"Update tasks request completed for user {user_id}: {len(result.get('updated_tasks', []))} tasks updated")
            return result
        except Exception as e:
            logger.error(f"Error handling update tasks request for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "updated_tasks": [],
                "errors": [str(e)]
            }

    async def handle_delete_tasks_request(self, user_id: str, task_ids: List[str]) -> Dict[str, Any]:
        """
        Handle a request to delete tasks

        Args:
            user_id: The ID of the user deleting the tasks
            task_ids: List of task IDs to delete

        Returns:
            Result of the delete operation
        """
        logger.info(f"Handling delete tasks request for user {user_id}")

        try:
            result = await self.agent.delete_tasks(user_id, task_ids)
            logger.info(f"Delete tasks request completed for user {user_id}: {result.get('deleted_count', 0)} tasks deleted")
            return result
        except Exception as e:
            logger.error(f"Error handling delete tasks request for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "deleted_count": 0,
                "errors": [str(e)]
            }

    async def handle_update_tasks_status_request(self, user_id: str, task_status_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle a request to update task statuses

        Args:
            user_id: The ID of the user updating task statuses
            task_status_updates: List of task status updates to apply

        Returns:
            Result of the status update operation
        """
        logger.info(f"Handling update tasks status request for user {user_id}")

        try:
            result = await self.agent.update_tasks_status(user_id, task_status_updates)
            logger.info(f"Update tasks status request completed for user {user_id}: {len(result.get('updated_tasks', []))} tasks updated")
            return result
        except Exception as e:
            logger.error(f"Error handling update tasks status request for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "updated_tasks": [],
                "errors": [str(e)]
            }

    async def process_ai_request(self, user_id: str, operation: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a generic AI request based on the operation type

        Args:
            user_id: The ID of the user making the request
            operation: The type of operation (create, read, update, delete, update_status)
            data: The data for the operation

        Returns:
            Result of the operation
        """
        logger.info(f"Processing AI request for user {user_id}, operation: {operation}")

        if operation == "create":
            return await self.handle_create_tasks_request(user_id, data.get("tasks", []))
        elif operation == "read":
            return await self.handle_read_tasks_request(
                user_id,
                data.get("task_ids"),
                data.get("filters")
            )
        elif operation == "update":
            return await self.handle_update_tasks_request(user_id, data.get("task_updates", []))
        elif operation == "delete":
            return await self.handle_delete_tasks_request(user_id, data.get("task_ids", []))
        elif operation == "update_status":
            return await self.handle_update_tasks_status_request(user_id, data.get("task_status_updates", []))
        else:
            error_msg = f"Unknown operation: {operation}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "errors": [error_msg]
            }


# Example usage
async def main():
    """Example of how to use the Task Operations Handler."""
    # Initialize the agent
    agent = AIDOTodoAgent()

    # Connect to MCP server
    await agent.connect_mcp_server()

    # Initialize the handler
    handler = TaskOperationsHandler(agent)

    # Example: Process a create tasks request
    user_id = "test-user-123"
    create_result = await handler.process_ai_request(
        user_id,
        "create",
        {
            "tasks": [{
                "title": "Test task from handler",
                "description": "Created via task operations handler",
                "priority": "Medium"
            }]
        }
    )
    print(f"Create result: {create_result}")

    # Example: Process a read tasks request
    read_result = await handler.process_ai_request(
        user_id,
        "read",
        {}
    )
    print(f"Read result: {read_result}")

    # Disconnect from MCP server
    await agent.disconnect_mcp_server()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())