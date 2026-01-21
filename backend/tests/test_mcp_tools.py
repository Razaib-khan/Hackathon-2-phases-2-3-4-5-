"""
Unit tests for the MCP tools in the AIDO Todo application
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

from src.mcp_server.tools.create_tasks import create_tasks
from src.mcp_server.tools.read_tasks import read_tasks
from src.mcp_server.tools.update_tasks import update_tasks
from src.mcp_server.tools.delete_tasks import delete_tasks
from src.mcp_server.tools.update_tasks_status import update_tasks_status


@pytest.mark.asyncio
async def test_create_tasks_success():
    """Test successful creation of tasks via MCP tool"""
    user_id = "test-user-id"
    tasks_data = [
        {
            "title": "Test Task 1",
            "description": "Description 1",
            "priority": "High",
            "status": False
        },
        {
            "title": "Test Task 2",
            "description": "Description 2",
            "priority": "Medium",
            "status": True
        }
    ]

    # Mock the database operations
    mock_session = MagicMock()
    mock_created_task1 = MagicMock()
    mock_created_task1.dict.return_value = {
        "id": "task1-uuid",
        "title": "Test Task 1",
        "description": "Description 1",
        "priority": "High",
        "status": False,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    mock_created_task2 = MagicMock()
    mock_created_task2.dict.return_value = {
        "id": "task2-uuid",
        "title": "Test Task 2",
        "description": "Description 2",
        "priority": "Medium",
        "status": True,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    with patch('src.mcp_server.tools.create_tasks.Session') as mock_session_class, \
         patch('src.mcp_server.tools.create_tasks.create_tasks_batch') as mock_create_batch, \
         patch('src.mcp_server.tools.create_tasks.engine'):

        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_create_batch.return_value = [mock_created_task1, mock_created_task2]

        result = await create_tasks(user_id, tasks_data)

    assert result["success"] is True
    assert len(result["created_tasks"]) == 2
    assert result["errors"] == []


@pytest.mark.asyncio
async def test_create_tasks_missing_user_id():
    """Test creation of tasks with missing user ID"""
    tasks_data = [{"title": "Test Task"}]

    result = await create_tasks("", tasks_data)

    assert result["success"] is False
    assert "User ID is required" in result["error"]
    assert result["errors"] == ["User ID is required"]


@pytest.mark.asyncio
async def test_create_tasks_missing_tasks():
    """Test creation of tasks with missing tasks data"""
    user_id = "test-user-id"

    result = await create_tasks(user_id, [])

    assert result["success"] is False
    assert "Tasks list is required" in result["error"]


@pytest.mark.asyncio
async def test_create_tasks_invalid_data():
    """Test creation of tasks with invalid data"""
    user_id = "test-user-id"
    tasks_data = [
        {"description": "Missing title"},  # Missing required title
        {"title": "Valid task", "priority": "InvalidPriority"}  # Invalid priority
    ]

    result = await create_tasks(user_id, tasks_data)

    assert result["success"] is False
    assert "validation errors" in result["error"]
    assert len(result["errors"]) > 0


@pytest.mark.asyncio
async def test_read_tasks_success():
    """Test successful reading of tasks via MCP tool"""
    user_id = "test-user-id"
    task_ids = ["task1-uuid", "task2-uuid"]

    mock_session = MagicMock()
    mock_task1 = MagicMock()
    mock_task1.dict.return_value = {
        "id": "task1-uuid",
        "title": "Test Task 1",
        "description": "Description 1",
        "priority": "High",
        "status": False,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    mock_task2 = MagicMock()
    mock_task2.dict.return_value = {
        "id": "task2-uuid",
        "title": "Test Task 2",
        "description": "Description 2",
        "priority": "Medium",
        "status": True,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    with patch('src.mcp_server.tools.read_tasks.Session') as mock_session_class, \
         patch('src.mcp_server.tools.read_tasks.get_tasks_by_ids') as mock_get_tasks, \
         patch('src.mcp_server.tools.read_tasks.engine'):

        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_get_tasks.return_value = [mock_task1, mock_task2]

        result = await read_tasks(user_id, task_ids=task_ids)

    assert result["success"] is True
    assert len(result["tasks"]) == 2
    assert result["total_count"] == 2


@pytest.mark.asyncio
async def test_read_tasks_with_filters():
    """Test reading of tasks with filters"""
    user_id = "test-user-id"
    filters = {"priority": "High", "status": "incomplete"}

    mock_session = MagicMock()
    mock_task = MagicMock()
    mock_task.dict.return_value = {
        "id": "task1-uuid",
        "title": "Test Task 1",
        "description": "Description 1",
        "priority": "High",
        "status": False,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    with patch('src.mcp_server.tools.read_tasks.Session') as mock_session_class, \
         patch('src.mcp_server.tools.read_tasks.get_tasks_for_user') as mock_get_tasks, \
         patch('src.mcp_server.tools.read_tasks.engine'):

        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_get_tasks.return_value = ([mock_task], 1)  # (tasks, total_count)

        result = await read_tasks(user_id, filters=filters)

    assert result["success"] is True
    assert len(result["tasks"]) == 1
    assert result["total_count"] == 1


@pytest.mark.asyncio
async def test_update_tasks_success():
    """Test successful updating of tasks via MCP tool"""
    user_id = "test-user-id"
    task_updates = [
        {
            "id": "task1-uuid",
            "title": "Updated Title",
            "priority": "Low"
        }
    ]

    mock_session = MagicMock()
    mock_updated_task = MagicMock()
    mock_updated_task.dict.return_value = {
        "id": "task1-uuid",
        "title": "Updated Title",
        "description": "Original Description",
        "priority": "Low",
        "status": False,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    with patch('src.mcp_server.tools.update_tasks.Session') as mock_session_class, \
         patch('src.mcp_server.tools.update_tasks.update_tasks_batch') as mock_update_batch, \
         patch('src.mcp_server.tools.update_tasks.engine'):

        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_update_batch.return_value = [mock_updated_task]

        result = await update_tasks(user_id, task_updates)

    assert result["success"] is True
    assert len(result["updated_tasks"]) == 1
    assert result["errors"] == []


@pytest.mark.asyncio
async def test_update_tasks_invalid_data():
    """Test updating of tasks with invalid data"""
    user_id = "test-user-id"
    task_updates = [
        {
            "title": "Missing ID"  # Missing required ID
        },
        {
            "id": "invalid-uuid-format",
            "title": "Invalid UUID"
        }
    ]

    result = await update_tasks(user_id, task_updates)

    assert result["success"] is False
    assert "validation errors" in result["error"]
    assert len(result["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_tasks_success():
    """Test successful deletion of tasks via MCP tool"""
    user_id = "test-user-id"
    task_ids = ["task1-uuid", "task2-uuid"]

    with patch('src.mcp_server.tools.delete_tasks.Session') as mock_session_class, \
         patch('src.mcp_server.tools.delete_tasks.delete_tasks_batch') as mock_delete_batch, \
         patch('src.mcp_server.tools.delete_tasks.engine'):

        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_delete_batch.return_value = 2  # Number of deleted tasks

        result = await delete_tasks(user_id, task_ids)

    assert result["success"] is True
    assert result["deleted_count"] == 2
    assert result["errors"] == []


@pytest.mark.asyncio
async def test_delete_tasks_invalid_uuid():
    """Test deletion of tasks with invalid UUIDs"""
    user_id = "test-user-id"
    task_ids = ["invalid-uuid", "another-invalid"]

    result = await delete_tasks(user_id, task_ids)

    assert result["success"] is False
    assert "validation errors" in result["error"]


@pytest.mark.asyncio
async def test_update_tasks_status_success():
    """Test successful updating of task statuses via MCP tool"""
    user_id = "test-user-id"
    task_status_updates = [
        {
            "id": "task1-uuid",
            "status": True
        },
        {
            "id": "task2-uuid",
            "status": False
        }
    ]

    mock_session = MagicMock()
    mock_updated_task1 = MagicMock()
    mock_updated_task1.dict.return_value = {
        "id": "task1-uuid",
        "title": "Test Task 1",
        "status": True,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    mock_updated_task2 = MagicMock()
    mock_updated_task2.dict.return_value = {
        "id": "task2-uuid",
        "title": "Test Task 2",
        "status": False,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    with patch('src.mcp_server.tools.update_tasks_status.Session') as mock_session_class, \
         patch('src.mcp_server.tools.update_tasks_status.update_tasks_status_batch') as mock_update_status_batch, \
         patch('src.mcp_server.tools.update_tasks_status.engine'):

        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_update_status_batch.return_value = [mock_updated_task1, mock_updated_task2]

        result = await update_tasks_status(user_id, task_status_updates)

    assert result["success"] is True
    assert len(result["updated_tasks"]) == 2
    assert result["errors"] == []


@pytest.mark.asyncio
async def test_update_tasks_status_invalid_data():
    """Test updating of task statuses with invalid data"""
    user_id = "test-user-id"
    task_status_updates = [
        {
            "id": "task1-uuid"
            # Missing status
        },
        {
            "id": "invalid-uuid-format",
            "status": "invalid-status-type"
        }
    ]

    result = await update_tasks_status(user_id, task_status_updates)

    assert result["success"] is False
    assert "validation errors" in result["error"]
    assert len(result["errors"]) > 0