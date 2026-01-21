"""
Integration Module for AI Agent and MCP Server
Handles the communication between the AI agent and MCP server tools
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager
from mcp.client import ClientSession
from .agent import AIDOTodoAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAgentMCPIntegration:
    """
    Integration layer between the AI Agent and MCP Server
    Manages the connection and communication between the AI agent and MCP tools
    """

    def __init__(self, agent: AIDOTodoAgent, mcp_url: str = None):
        """
        Initialize the AI Agent MCP Integration

        Args:
            agent: The AIDO Todo Agent instance
            mcp_url: URL for the MCP server (defaults to AIDO_MCP_URL env var)
        """
        self.agent = agent
        self.mcp_url = mcp_url or agent.mcp_url
        self.mcp_session: Optional[ClientSession] = None

    @asynccontextmanager
    async def mcp_connection(self):
        """
        Async context manager for MCP server connection
        """
        await self.connect()
        try:
            yield self
        finally:
            await self.disconnect()

    async def connect(self):
        """
        Establish connection to the MCP server
        """
        try:
            logger.info(f"Connecting to MCP server at {self.mcp_url}")

            # Initialize MCP client session
            self.mcp_session = ClientSession()

            # Connect to the MCP server
            # Note: The actual connection method depends on the MCP implementation
            # For stdio connections, this would be handled differently
            await self.mcp_session.initialize()

            logger.info("Successfully connected to MCP server")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {str(e)}")
            raise

    async def disconnect(self):
        """
        Close connection to the MCP server
        """
        try:
            if self.mcp_session:
                await self.mcp_session.shutdown()
                self.mcp_session = None
                logger.info("Disconnected from MCP server")
        except Exception as e:
            logger.error(f"Error disconnecting from MCP server: {str(e)}")

    async def call_mcp_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool with the given parameters

        Args:
            tool_name: Name of the MCP tool to call
            params: Parameters to pass to the tool

        Returns:
            Result from the MCP tool
        """
        if not self.mcp_session:
            raise RuntimeError("Not connected to MCP server. Call connect() first.")

        try:
            logger.info(f"Calling MCP tool: {tool_name}")

            # Call the MCP tool
            result = await self.mcp_session.call_tool(tool_name, params)

            logger.info(f"MCP tool {tool_name} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {str(e)}")
            raise

    async def create_tasks_via_mcp(self, user_id: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create tasks using the MCP server tool

        Args:
            user_id: The ID of the user creating the tasks
            tasks: List of task data to create

        Returns:
            Result from the MCP server
        """
        try:
            result = await self.call_mcp_tool("create-tasks", {
                "user_id": user_id,
                "tasks": tasks
            })
            return result
        except Exception as e:
            logger.error(f"Error creating tasks via MCP for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "created_tasks": [],
                "errors": [str(e)]
            }

    async def read_tasks_via_mcp(self, user_id: str, task_ids: List[str] = None, filters: Dict[str, Any] = None) -> Dict[str, Any]:
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
            params = {"user_id": user_id}
            if task_ids is not None:
                params["task_ids"] = task_ids
            if filters is not None:
                params["filters"] = filters

            result = await self.call_mcp_tool("read-tasks", params)
            return result
        except Exception as e:
            logger.error(f"Error reading tasks via MCP for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tasks": [],
                "total_count": 0
            }

    async def update_tasks_via_mcp(self, user_id: str, task_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update tasks using the MCP server tool

        Args:
            user_id: The ID of the user updating the tasks
            task_updates: List of task updates to apply

        Returns:
            Result from the MCP server
        """
        try:
            result = await self.call_mcp_tool("update-tasks", {
                "user_id": user_id,
                "task_updates": task_updates
            })
            return result
        except Exception as e:
            logger.error(f"Error updating tasks via MCP for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "updated_tasks": [],
                "errors": [str(e)]
            }

    async def delete_tasks_via_mcp(self, user_id: str, task_ids: List[str]) -> Dict[str, Any]:
        """
        Delete tasks using the MCP server tool

        Args:
            user_id: The ID of the user deleting the tasks
            task_ids: List of task IDs to delete

        Returns:
            Result from the MCP server
        """
        try:
            result = await self.call_mcp_tool("delete-tasks", {
                "user_id": user_id,
                "task_ids": task_ids
            })
            return result
        except Exception as e:
            logger.error(f"Error deleting tasks via MCP for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "deleted_count": 0,
                "errors": [str(e)]
            }

    async def update_tasks_status_via_mcp(self, user_id: str, task_status_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update task statuses using the MCP server tool

        Args:
            user_id: The ID of the user updating task statuses
            task_status_updates: List of task status updates to apply

        Returns:
            Result from the MCP server
        """
        try:
            result = await self.call_mcp_tool("update-tasks-status", {
                "user_id": user_id,
                "task_status_updates": task_status_updates
            })
            return result
        except Exception as e:
            logger.error(f"Error updating task statuses via MCP for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "updated_tasks": [],
                "errors": [str(e)]
            }

    async def run_ai_agent_with_mcp_integration(self, user_id: str, user_message: str) -> str:
        """
        Run the AI agent with full MCP integration

        Args:
            user_id: The ID of the user interacting with the agent
            user_message: The message from the user

        Returns:
            The AI agent's response
        """
        try:
            # For now, we'll use the agent's chat completion functionality
            # In a real implementation, this would involve:
            # 1. Processing the user's message to identify intent
            # 2. Determining if MCP tools need to be called
            # 3. Calling the appropriate MCP tools
            # 4. Generating a response based on the results

            # For demonstration, we'll simulate a simple interaction
            messages = [
                {"role": "user", "content": user_message}
            ]

            response = await self.agent.chat_completion(messages, user_id)
            return response
        except Exception as e:
            logger.error(f"Error running AI agent with MCP integration: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"


# Example usage
async def main():
    """Example of how to use the AI Agent MCP Integration."""
    # Initialize the agent
    agent = AIDOTodoAgent()

    # Initialize the integration
    integration = AIAgentMCPIntegration(agent)

    # Example: Use the integration to connect to MCP and perform operations
    async with integration.mcp_connection():
        user_id = "test-user-123"

        # Example: Create a task via MCP
        create_result = await integration.create_tasks_via_mcp(user_id, [{
            "title": "Test task via MCP integration",
            "description": "Created via AI Agent MCP integration",
            "priority": "Medium"
        }])
        print(f"Create result: {create_result}")

        # Example: Read tasks via MCP
        read_result = await integration.read_tasks_via_mcp(user_id)
        print(f"Read result: {read_result}")


if __name__ == "__main__":
    asyncio.run(main())