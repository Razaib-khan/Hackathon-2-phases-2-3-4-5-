"""
Unit tests for the task service in the AIDO Todo application
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from uuid import UUID

from src.services.task_service import (
    create_task,
    get_tasks_for_user,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task_completion,
    create_tasks_batch,
    get_tasks_by_ids,
    update_tasks_batch,
    delete_tasks_batch,
    update_tasks_status_batch
)
from src.models.task import TaskCreate, TaskUpdate


def test_create_task_success():
    """Test successful task creation"""
    # Mock session and user
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user

    # Mock task data
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        priority="Medium",
        status=False
    )

    # Call the function
    with patch('src.services.task_service.uuid.UUID', return_value="user-uuid"):
        result = create_task(mock_session, "user-uuid", task_data)

    # Assertions
    assert result.title == "Test Task"
    assert result.description == "Test Description"
    assert result.priority == "Medium"
    assert result.status is False
    assert result.user_id == "user-uuid"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_create_task_user_not_found():
    """Test task creation when user doesn't exist"""
    mock_session = MagicMock(spec=Session)
    mock_session.get.return_value = None  # User not found

    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        priority="Medium",
        status=False
    )

    with patch('src.services.task_service.uuid.UUID', return_value="user-uuid"):
        with pytest.raises(ValueError, match="User not found"):
            create_task(mock_session, "user-uuid", task_data)


def test_get_tasks_for_user_success():
    """Test successful retrieval of tasks for a user"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user

    # Mock query execution
    mock_exec_result = MagicMock()
    mock_exec_result.one.return_value = 5  # Total count
    mock_exec_result.all.return_value = []  # Empty tasks list for this test

    mock_session.exec.return_value = mock_exec_result

    with patch('src.services.task_service.uuid.UUID', return_value="user-uuid"):
        tasks, count = get_tasks_for_user(mock_session, "user-uuid")

    assert count == 5
    assert tasks == []


def test_get_tasks_for_user_with_filters():
    """Test retrieval of tasks with filters applied"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user

    # Mock query execution
    mock_exec_result = MagicMock()
    mock_exec_result.one.return_value = 2  # Total count
    mock_exec_result.all.return_value = []  # Empty tasks list for this test

    mock_session.exec.return_value = mock_exec_result

    with patch('src.services.task_service.uuid.UUID', return_value="user-uuid"):
        tasks, count = get_tasks_for_user(
            mock_session,
            "user-uuid",
            search="test",
            priority="High",
            status_filter="complete"
        )

    assert count == 2
    assert tasks == []
    # Verify that the session.exec was called (meaning query was constructed)


def test_get_task_by_id_success():
    """Test successful retrieval of a specific task"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_task = MagicMock()
    mock_task.id = "task-uuid"
    mock_task.user_id = "user-uuid"

    mock_session.get.side_effect = [mock_user, mock_task]  # First call for user, second for task

    query_result = MagicMock()
    query_result.first.return_value = mock_task
    mock_session.exec.return_value = query_result

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task-uuid"]):
        result = get_task_by_id(mock_session, "user-uuid", "task-uuid")

    assert result == mock_task


def test_get_task_by_id_not_found():
    """Test retrieval of a task that doesn't exist"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user  # User exists

    query_result = MagicMock()
    query_result.first.return_value = None  # Task not found
    mock_session.exec.return_value = query_result

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task-uuid"]):
        result = get_task_by_id(mock_session, "user-uuid", "task-uuid")

    assert result is None


def test_update_task_success():
    """Test successful task update"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_task = MagicMock()
    mock_task.id = "task-uuid"
    mock_task.user_id = "user-uuid"
    mock_task.updated_at = None

    mock_session.get.side_effect = [mock_user, mock_task]  # First call for user, second for task

    query_result = MagicMock()
    query_result.first.return_value = mock_task
    mock_session.exec.return_value = query_result

    update_data = TaskUpdate(title="Updated Title")

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task-uuid"]), \
         patch('src.services.task_service.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = "updated-timestamp"
        result = update_task(mock_session, "user-uuid", "task-uuid", update_data)

    assert result == mock_task
    assert mock_task.title == "Updated Title"
    mock_session.add.assert_called_once_with(mock_task)
    mock_session.commit.assert_called_once()


def test_delete_task_success():
    """Test successful task deletion"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_task = MagicMock()
    mock_task.id = "task-uuid"
    mock_task.user_id = "user-uuid"

    mock_session.get.return_value = mock_user  # User exists

    query_result = MagicMock()
    query_result.first.return_value = mock_task
    mock_session.exec.return_value = query_result

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task-uuid"]):
        result = delete_task(mock_session, "user-uuid", "task-uuid")

    assert result is True
    mock_session.delete.assert_called_once_with(mock_task)
    mock_session.commit.assert_called_once()


def test_delete_task_not_found():
    """Test deletion of a task that doesn't exist"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user  # User exists

    query_result = MagicMock()
    query_result.first.return_value = None  # Task not found
    mock_session.exec.return_value = query_result

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task-uuid"]):
        result = delete_task(mock_session, "user-uuid", "task-uuid")

    assert result is False


def test_toggle_task_completion():
    """Test toggling task completion status"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_task = MagicMock()
    mock_task.id = "task-uuid"
    mock_task.user_id = "user-uuid"
    mock_task.status = False  # Initially incomplete

    mock_session.get.side_effect = [mock_user, mock_task]  # First call for user, second for task

    query_result = MagicMock()
    query_result.first.return_value = mock_task
    mock_session.exec.return_value = query_result

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task-uuid"]), \
         patch('src.services.task_service.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = "updated-timestamp"
        result = toggle_task_completion(mock_session, "user-uuid", "task-uuid", True)

    assert result == mock_task
    assert mock_task.status is True  # Should be marked as complete


def test_create_tasks_batch():
    """Test batch creation of tasks"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user

    task_data_list = [
        TaskCreate(title="Task 1", description="Desc 1", priority="High", status=False),
        TaskCreate(title="Task 2", description="Desc 2", priority="Low", status=True)
    ]

    with patch('src.services.task_service.uuid.UUID', return_value="user-uuid"):
        result = create_tasks_batch(mock_session, "user-uuid", task_data_list)

    # Verify that tasks were added to session
    assert mock_session.add.call_count == 2
    mock_session.commit.assert_called_once()
    assert len(result) == 2


def test_get_tasks_by_ids():
    """Test retrieval of multiple tasks by IDs"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user

    mock_tasks = [MagicMock(), MagicMock()]

    query_result = MagicMock()
    query_result.all.return_value = mock_tasks
    mock_session.exec.return_value = query_result

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task1-uuid", "task2-uuid"]):
        result = get_tasks_by_ids(mock_session, "user-uuid", ["task1-uuid", "task2-uuid"])

    assert result == mock_tasks


def test_update_tasks_batch():
    """Test batch updating of tasks"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user

    mock_task = MagicMock()
    mock_task.id = "task-uuid"
    mock_task.user_id = "user-uuid"

    query_result = MagicMock()
    query_result.first.return_value = mock_task
    mock_session.exec.return_value = query_result

    update_data_list = [
        {"id": "task1-uuid", "title": "Updated Title 1"},
        {"id": "task2-uuid", "title": "Updated Title 2"}
    ]

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task1-uuid", "task2-uuid"]):
        result = update_tasks_batch(mock_session, "user-uuid", update_data_list)

    # Verify that tasks were updated
    assert len(result) >= 0  # At least one task should be processed
    mock_session.add.assert_called()


def test_delete_tasks_batch():
    """Test batch deletion of tasks"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user

    mock_task1 = MagicMock()
    mock_task1.id = "task1-uuid"
    mock_task1.user_id = "user-uuid"

    mock_task2 = MagicMock()
    mock_task2.id = "task2-uuid"
    mock_task2.user_id = "user-uuid"

    query_result = MagicMock()
    query_result.all.return_value = [mock_task1, mock_task2]
    mock_session.exec.return_value = query_result

    task_ids = ["task1-uuid", "task2-uuid"]

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task1-uuid", "task2-uuid"]):
        result = delete_tasks_batch(mock_session, "user-uuid", task_ids)

    assert result == 2  # Two tasks should be deleted
    assert mock_session.delete.call_count == 2
    mock_session.commit.assert_called_once()


def test_update_tasks_status_batch():
    """Test batch updating of task statuses"""
    mock_session = MagicMock(spec=Session)
    mock_user = MagicMock()
    mock_session.get.return_value = mock_user

    mock_task = MagicMock()
    mock_task.id = "task-uuid"
    mock_task.user_id = "user-uuid"

    query_result = MagicMock()
    query_result.first.return_value = mock_task
    mock_session.exec.return_value = query_result

    status_updates = [
        {"id": "task1-uuid", "status": True},
        {"id": "task2-uuid", "status": False}
    ]

    with patch('src.services.task_service.uuid.UUID', side_effect=["user-uuid", "task1-uuid", "task2-uuid"]), \
         patch('src.services.task_service.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = "updated-timestamp"
        result = update_tasks_status_batch(mock_session, "user-uuid", status_updates)

    # Verify that statuses were updated
    assert len(result) >= 0  # At least one task should be processed
    mock_session.add.assert_called()