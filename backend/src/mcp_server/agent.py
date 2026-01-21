"""
OpenAI Agent Configuration for AIDO Todo Application
Configures the AI agent to work with OpenRouter and connect to the MCP server
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
from openai import OpenAI
from mcp.client import ClientSession
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIDOTodoAgent:
    """
    AI Agent for the AIDO Todo application
    Connects to OpenRouter and uses MCP server for task operations
    """

    def __init__(self, openrouter_api_key: str = None, mcp_url: str = None):
        """
        Initialize the AIDO Todo Agent

        Args:
            openrouter_api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            mcp_url: URL for the MCP server (defaults to AIDO_MCP_URL env var)
        """
        self.openrouter_api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.openrouter_api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.")

        self.mcp_url = mcp_url or os.getenv("AIDO_MCP_URL", "stdio://")

        # Initialize OpenAI client with OpenRouter
        self.client = OpenAI(
            api_key=self.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )

        # Initialize MCP client session
        self.mcp_session = None

        # System prompt for the AI agent
        self.system_prompt = """
        You are an AI assistant for the AIDO Todo application. Your role is to help users manage their tasks using the available tools.

        Available capabilities:
        1. Create new tasks with titles, descriptions, priorities, and statuses
        2. Read existing tasks by ID or with filters (search, priority, status)
        3. Update existing tasks (title, description, priority, status)
        4. Delete tasks by ID
        5. Update task completion status (mark as complete/incomplete)

        Always confirm with the user before performing destructive operations like deleting tasks.
        When creating tasks, if the user doesn't specify a priority, default to "Medium".
        When updating tasks, only update the fields that the user specifically mentions.

        Be helpful, concise, and professional in your interactions.
        """

    async def connect_mcp_server(self):
        """Connect to the MCP server."""
        try:
            # For now, we'll simulate the connection - in a real implementation
            # this would establish a connection to the MCP server
            logger.info(f"Connecting to MCP server at {self.mcp_url}")

            # In a real implementation, you would do:
            # self.mcp_session = ClientSession()
            # await self.mcp_session.connect(self.mcp_url)

            logger.info("Connected to MCP server successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {str(e)}")
            raise

    async def disconnect_mcp_server(self):
        """Disconnect from the MCP server."""
        try:
            if self.mcp_session:
                # In a real implementation:
                # await self.mcp_session.close()
                logger.info("Disconnected from MCP server")
        except Exception as e:
            logger.error(f"Error disconnecting from MCP server: {str(e)}")

    async def create_tasks(self, user_id: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create tasks using the MCP server tool

        Args:
            user_id: The ID of the user creating the tasks
            tasks: List of task data to create

        Returns:
            Result from the MCP server
        """
        try:
            logger.info(f"Creating {len(tasks)} tasks for user {user_id}")

            # Simulate calling the MCP tool
            # In a real implementation, this would call the MCP server
            result = await self._call_mcp_tool("create-tasks", {
                "user_id": user_id,
                "tasks": tasks
            })

            return result
        except Exception as e:
            logger.error(f"Error creating tasks for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "created_tasks": [],
                "errors": [str(e)]
            }

    async def read_tasks(self, user_id: str, task_ids: List[str] = None, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Read tasks using the MCP server tool

        Args:
            user_id: The ID of the user reading the tasks
            task_ids: Optional list of specific task IDs to retrieve
            filters: Optional filters for broader task retrieval

        Returns:
            Result from the MCP server
        """
        try:
            logger.info(f"Reading tasks for user {user_id}")

            params = {
                "user_id": user_id
            }

            if task_ids is not None:
                params["task_ids"] = task_ids
            if filters is not None:
                params["filters"] = filters

            result = await self._call_mcp_tool("read-tasks", params)

            return result
        except Exception as e:
            logger.error(f"Error reading tasks for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tasks": [],
                "total_count": 0
            }

    async def update_tasks(self, user_id: str, task_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update tasks using the MCP server tool

        Args:
            user_id: The ID of the user updating the tasks
            task_updates: List of task updates to apply

        Returns:
            Result from the MCP server
        """
        try:
            logger.info(f"Updating {len(task_updates)} tasks for user {user_id}")

            result = await self._call_mcp_tool("update-tasks", {
                "user_id": user_id,
                "task_updates": task_updates
            })

            return result
        except Exception as e:
            logger.error(f"Error updating tasks for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "updated_tasks": [],
                "errors": [str(e)]
            }

    async def delete_tasks(self, user_id: str, task_ids: List[str]) -> Dict[str, Any]:
        """
        Delete tasks using the MCP server tool

        Args:
            user_id: The ID of the user deleting the tasks
            task_ids: List of task IDs to delete

        Returns:
            Result from the MCP server
        """
        try:
            logger.info(f"Deleting {len(task_ids)} tasks for user {user_id}")

            result = await self._call_mcp_tool("delete-tasks", {
                "user_id": user_id,
                "task_ids": task_ids
            })

            return result
        except Exception as e:
            logger.error(f"Error deleting tasks for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "deleted_count": 0,
                "errors": [str(e)]
            }

    async def update_tasks_status(self, user_id: str, task_status_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update task statuses using the MCP server tool

        Args:
            user_id: The ID of the user updating task statuses
            task_status_updates: List of task status updates to apply

        Returns:
            Result from the MCP server
        """
        try:
            logger.info(f"Updating {len(task_status_updates)} task statuses for user {user_id}")

            result = await self._call_mcp_tool("update-tasks-status", {
                "user_id": user_id,
                "task_status_updates": task_status_updates
            })

            return result
        except Exception as e:
            logger.error(f"Error updating task statuses for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "updated_tasks": [],
                "errors": [str(e)]
            }

    async def _call_mcp_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal method to call MCP tools
        This is a placeholder implementation - in a real scenario, this would call the actual MCP server

        Args:
            tool_name: Name of the MCP tool to call
            params: Parameters to pass to the tool

        Returns:
            Result from the MCP tool
        """
        # Placeholder implementation - in a real implementation, this would call the MCP server
        # For now, we'll return a mock response based on the tool
        logger.info(f"Calling MCP tool: {tool_name}")

        # This is where the actual MCP call would happen
        # return await self.mcp_session.call_tool(tool_name, params)

        # Mock implementation for demonstration
        if tool_name == "create-tasks":
            # Mock successful creation of tasks
            created_tasks = []
            for i, task in enumerate(params.get("tasks", [])):
                created_task = {
                    "id": f"mock-task-{i}-{hash(str(task))}",
                    "title": task.get("title", ""),
                    "description": task.get("description", ""),
                    "priority": task.get("priority", "Medium"),
                    "status": task.get("status", False),
                    "timestamp": "2024-01-01T00:00:00Z"
                }
                created_tasks.append(created_task)

            return {
                "success": True,
                "created_tasks": created_tasks,
                "errors": []
            }
        elif tool_name == "read-tasks":
            # Mock returning sample tasks
            return {
                "success": True,
                "tasks": [
                    {
                        "id": "mock-task-1",
                        "title": "Sample Task",
                        "description": "This is a sample task",
                        "priority": "Medium",
                        "status": False,
                        "timestamp": "2024-01-01T00:00:00Z"
                    }
                ],
                "total_count": 1
            }
        elif tool_name == "update-tasks":
            # Mock successful update
            return {
                "success": True,
                "updated_tasks": params.get("task_updates", []),
                "errors": []
            }
        elif tool_name == "delete-tasks":
            # Mock successful deletion
            return {
                "success": True,
                "deleted_count": len(params.get("task_ids", [])),
                "errors": []
            }
        elif tool_name == "update-tasks-status":
            # Mock successful status update
            return {
                "success": True,
                "updated_tasks": params.get("task_status_updates", []),
                "errors": []
            }
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "errors": [f"Unknown tool: {tool_name}"]
            }

    async def chat_completion(self, messages: List[Dict[str, str]], user_id: str) -> str:
        """
        Get a chat completion from the OpenAI-compatible API

        Args:
            messages: List of messages in the conversation
            user_id: ID of the user having the conversation

        Returns:
            The AI's response
        """
        try:
            # Add system message if not present
            if not any(msg.get("role") == "system" for msg in messages):
                messages = [{"role": "system", "content": self.system_prompt}] + messages

            # Add user ID context to the messages
            # This is where we'd typically enrich the context with user-specific information
            response = self.client.chat.completions.create(
                model="openrouter/auto",  # Auto-selects the best available model
                messages=messages,
                temperature=0.7,
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting chat completion: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"


# Example usage
async def main():
    """Example of how to use the AIDO Todo Agent."""
    # Initialize the agent
    agent = AIDOTodoAgent()

    try:
        # Connect to MCP server
        await agent.connect_mcp_server()

        # Example: Create a task
        user_id = "test-user-123"
        tasks_to_create = [{
            "title": "Buy groceries",
            "description": "Milk, bread, eggs",
            "priority": "High"
        }]

        result = await agent.create_tasks(user_id, tasks_to_create)
        print(f"Create tasks result: {result}")

        # Example: Read tasks
        read_result = await agent.read_tasks(user_id)
        print(f"Read tasks result: {read_result}")

    finally:
        # Disconnect from MCP server
        await agent.disconnect_mcp_server()


if __name__ == "__main__":
    asyncio.run(main())