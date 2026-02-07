"""
Task service for the Speckit Plus Todo Application
Handles business logic for task operations
"""

import uuid
from typing import List, Optional
from datetime import datetime, timedelta
import json
import logging

from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.task import Task, TaskComplete, TaskCreate, TaskUpdate
from models.user import User
from models.recurrence_pattern import RecurrencePattern, RecurrencePatternCreate

# Import Dapr dependencies if available
try:
    from dapr.clients import DaprClient
    HAS_DAPR = True
except ImportError:
    HAS_DAPR = False
    logging.warning("Dapr not available for task service")

from .kafka_producer import publish_event, publish_task_created_event, publish_task_updated_event, publish_task_completed_event
from models.events import EventFactory, EventTypeEnum

# Import enhanced logging
from ..utils.logging import get_logger, log_to_external_system
logger = get_logger(__name__)


def create_task(session: Session, user_id: str, task_data: TaskCreate) -> Task:
    """
    Create a new task for a user
    """
    start_time = datetime.utcnow()

    # Validate user exists
    user = session.get(User, uuid.UUID(user_id))
    if not user:
        raise ValueError("User not found")

    # Create task object
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        timestamp=task_data.timestamp,
        status=task_data.status,
        user_id=uuid.UUID(user_id),
        due_date=getattr(task_data, 'due_date', None),
        reminder_time=getattr(task_data, 'reminder_time', None),
        is_recurring=getattr(task_data, 'is_recurring', False),
        recurrence_pattern=getattr(task_data, 'recurrence_pattern', None),
        next_occurrence=getattr(task_data, 'next_occurrence', None),
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Calculate operation duration
    duration = (datetime.utcnow() - start_time).total_seconds() * 1000  # in milliseconds

    # Log task creation
    logger.log_task_operation(
        operation="create",
        user_id=user_id,
        task_id=str(db_task.id),
        priority=db_task.priority.value if hasattr(db_task.priority, 'value') else db_task.priority,
        status=db_task.status,
        duration_ms=duration
    )

    # Publish event to Kafka if available
    try:
        from models.events import EventFactory, EventTypeEnum
        task_data_dict = db_task.dict()
        event = EventFactory.create_event(
            event_type=EventTypeEnum.TASK_CREATED,
            user_id=user_id,
            data=task_data_dict
        )
        from .kafka_producer import publish_event
        publish_event(event, user_id)

        # Log the event publishing
        logger.log_with_context(
            logging.INFO,
            "Task created event published to Kafka",
            context={
                "task_id": str(db_task.id),
                "user_id": user_id,
                "event_type": "task_created"
            }
        )
    except Exception as e:
        logger.log_with_context(
            logging.ERROR,
            "Failed to publish task created event",
            context={
                "task_id": str(db_task.id),
                "user_id": user_id,
                "error": str(e)
            }
        )

    # If Dapr is available, store task in state store
    if HAS_DAPR:
        try:
            with DaprClient() as dapr_client:
                # Save task to Dapr state store
                dapr_client.save_state(
                    store_name="postgresql-statestore",
                    key=f"task_{db_task.id}",
                    value=db_task.json()
                )

                # Log the Dapr state save
                logger.log_with_context(
                    logging.INFO,
                    "Task saved to Dapr state store",
                    context={
                        "task_id": str(db_task.id),
                        "dapr_store": "postgresql-statestore"
                    }
                )
        except Exception as e:
            logger.log_with_context(
                logging.ERROR,
                "Dapr state save failed",
                context={
                    "task_id": str(db_task.id),
                    "error": str(e)
                }
            )

    # Log to external systems
    log_to_external_system({
        "type": "task_operation",
        "operation": "create",
        "task_id": str(db_task.id),
        "user_id": user_id,
        "priority": db_task.priority.value if hasattr(db_task.priority, 'value') else db_task.priority,
        "status": db_task.status,
        "duration_ms": duration,
        "timestamp": datetime.utcnow().isoformat()
    })

    return db_task


def get_tasks_for_user(
    session: Session,
    user_id: str,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    status_filter: Optional[str] = None,
    timestamp_from: Optional[datetime] = None,
    timestamp_to: Optional[datetime] = None,
    page: int = 1,
    limit: int = 20,
):
    """
    Get all tasks for a user with optional filters and return both tasks and total count for pagination
    """
    user_uuid = uuid.UUID(user_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Build base query with selectinload for user relationship to prevent N+1
    base_query = select(Task).options(selectinload(Task.user)).where(Task.user_id == user_uuid)

    # Apply filters to base query
    if search:
        # Use case-insensitive search for better user experience
        search_lower = search.lower()
        base_query = base_query.where(
            (func.lower(Task.title).contains(search_lower)) | (func.lower(Task.description).contains(search_lower))
        )
    if priority:
        base_query = base_query.where(Task.priority == priority)
    if status_filter:
        if status_filter.lower() in ["complete", "completed", "true", "1"]:
            base_query = base_query.where(Task.status == True)
        elif status_filter.lower() in ["incomplete", "pending", "false", "0"]:
            base_query = base_query.where(Task.status == False)
    if timestamp_from:
        base_query = base_query.where(Task.timestamp >= timestamp_from)
    if timestamp_to:
        base_query = base_query.where(Task.timestamp <= timestamp_to)

    # Count total records for pagination
    count_query = select(func.count()).select_from(base_query.subquery())
    total_count = session.exec(count_query).one()

    # Apply pagination to the main query
    offset = (page - 1) * limit
    paginated_query = base_query.offset(offset).limit(limit)

    tasks = session.exec(paginated_query).all()

    return tasks, total_count


def get_task_by_id(session: Session, user_id: str, task_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a user
    """
    user_uuid = uuid.UUID(user_id)
    task_uuid = uuid.UUID(task_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get task and verify it belongs to the user using a single query
    query = select(Task).options(selectinload(Task.user)).where(
        Task.id == task_uuid,
        Task.user_id == user_uuid
    )
    task = session.exec(query).first()

    return task


def update_task(
    session: Session, user_id: str, task_id: str, task_data: TaskUpdate
) -> Optional[Task]:
    """
    Update a task for a user
    """
    user_uuid = uuid.UUID(user_id)
    task_uuid = uuid.UUID(task_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get task and verify it belongs to the user using a single query
    query = select(Task).options(selectinload(Task.user)).where(
        Task.id == task_uuid,
        Task.user_id == user_uuid
    )
    task = session.exec(query).first()

    if not task:
        return None

    # Store original task data for event
    original_task_data = task.dict()

    # Update task with provided data
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    # Publish event to Kafka if available
    try:
        from models.events import EventFactory, EventTypeEnum
        event_data = {
            "original": original_task_data,
            "updated": task.dict()
        }
        event = EventFactory.create_event(
            event_type=EventTypeEnum.TASK_UPDATED,
            user_id=user_id,
            data=event_data
        )
        from .kafka_producer import publish_event
        publish_event(event, user_id)
    except Exception as e:
        logging.error(f"Failed to publish task updated event: {str(e)}")

    # If Dapr is available, update task in state store
    if HAS_DAPR:
        try:
            with DaprClient() as dapr_client:
                # Update task in Dapr state store
                dapr_client.save_state(
                    store_name="postgresql-statestore",
                    key=f"task_{task.id}",
                    value=task.json()
                )
        except Exception as e:
            logging.error(f"Dapr state update failed: {str(e)}")

    return task


def delete_task(session: Session, user_id: str, task_id: str) -> bool:
    """
    Delete a task for a user
    """
    user_uuid = uuid.UUID(user_id)
    task_uuid = uuid.UUID(task_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get task and verify it belongs to the user using a single query
    query = select(Task).where(
        Task.id == task_uuid,
        Task.user_id == user_uuid
    )
    task = session.exec(query).first()

    if not task:
        return False

    session.delete(task)
    session.commit()

    return True


def toggle_task_completion(
    session: Session, user_id: str, task_id: str, complete: bool
) -> Optional[Task]:
    """
    Toggle task completion status
    """
    user_uuid = uuid.UUID(user_id)
    task_uuid = uuid.UUID(task_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get task and verify it belongs to the user using a single query
    query = select(Task).options(selectinload(Task.user)).where(
        Task.id == task_uuid,
        Task.user_id == user_uuid
    )
    task = session.exec(query).first()

    if not task:
        return None

    # Store original status for event
    original_status = task.status

    # Update completion status
    task.status = complete
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    # Publish event to Kafka if available
    try:
        from models.events import EventFactory, EventTypeEnum
        event_data = {
            "task_id": str(task.id),
            "original_status": original_status,
            "new_status": complete,
            "task_details": task.dict()
        }
        event = EventFactory.create_event(
            event_type=EventTypeEnum.TASK_COMPLETED if complete else EventTypeEnum.TASK_UPDATED,
            user_id=user_id,
            data=event_data
        )
        from .kafka_producer import publish_event
        publish_event(event, user_id)
    except Exception as e:
        logging.error(f"Failed to publish task completion event: {str(e)}")

    # If Dapr is available, update task in state store
    if HAS_DAPR:
        try:
            with DaprClient() as dapr_client:
                # Update task in Dapr state store
                dapr_client.save_state(
                    store_name="postgresql-statestore",
                    key=f"task_{task.id}",
                    value=task.json()
                )
        except Exception as e:
            logging.error(f"Dapr state update failed: {str(e)}")

    # If task is completed and it's recurring, generate next occurrence
    if complete and task.is_recurring and task.recurrence_pattern:
        from .task_scheduler import generate_next_occurrence
        generate_next_occurrence(session, task)

    return task


def create_tasks_batch(
    session: Session, user_id: str, tasks_data: List[TaskCreate]
) -> List[Task]:
    """
    Create multiple tasks for a user at once (for AI agent operations)
    """
    user_uuid = uuid.UUID(user_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    created_tasks = []
    for task_data in tasks_data:
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            timestamp=task_data.timestamp or datetime.utcnow(),
            status=task_data.status or False,
            user_id=user_uuid,
        )
        session.add(db_task)
        created_tasks.append(db_task)

    session.commit()

    # Refresh all created tasks to get their IDs
    for task in created_tasks:
        session.refresh(task)

    return created_tasks


def get_tasks_by_ids(
    session: Session, user_id: str, task_ids: List[str]
) -> List[Task]:
    """
    Get multiple tasks by their IDs for a user
    """
    user_uuid = uuid.UUID(user_id)
    task_uuids = [uuid.UUID(task_id) for task_id in task_ids]

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get tasks and verify they belong to the user
    query = select(Task).options(selectinload(Task.user)).where(
        Task.id.in_(task_uuids),
        Task.user_id == user_uuid
    )
    tasks = session.exec(query).all()

    return tasks


def update_tasks_batch(
    session: Session, user_id: str, task_updates: List[dict]
) -> List[Task]:
    """
    Update multiple tasks for a user at once (for AI agent operations)
    """
    user_uuid = uuid.UUID(user_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    updated_tasks = []
    for update_data in task_updates:
        task_id = update_data.get("id")
        if not task_id:
            continue

        task_uuid = uuid.UUID(task_id)

        # Get task and verify it belongs to the user
        query = select(Task).options(selectinload(Task.user)).where(
            Task.id == task_uuid,
            Task.user_id == user_uuid
        )
        task = session.exec(query).first()

        if not task:
            continue

        # Update task with provided data
        for field, value in update_data.items():
            if field != "id":  # Don't update the ID
                if hasattr(task, field):
                    setattr(task, field, value)
        task.updated_at = datetime.utcnow()

        session.add(task)
        updated_tasks.append(task)

    session.commit()

    # Refresh all updated tasks
    for task in updated_tasks:
        session.refresh(task)

    return updated_tasks


def delete_tasks_batch(
    session: Session, user_id: str, task_ids: List[str]
) -> int:
    """
    Delete multiple tasks for a user at once (for AI agent operations)
    """
    user_uuid = uuid.UUID(user_id)
    task_uuids = [uuid.UUID(task_id) for task_id in task_ids]

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Get tasks and verify they belong to the user
    query = select(Task).where(
        Task.id.in_(task_uuids),
        Task.user_id == user_uuid
    )
    tasks = session.exec(query).all()

    deleted_count = 0
    for task in tasks:
        session.delete(task)
        deleted_count += 1

    session.commit()
    return deleted_count


def update_tasks_status_batch(
    session: Session, user_id: str, task_status_updates: List[dict]
) -> List[Task]:
    """
    Update status of multiple tasks for a user at once (for AI agent operations)
    """
    user_uuid = uuid.UUID(user_id)

    # Verify user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    updated_tasks = []
    for update_data in task_status_updates:
        task_id = update_data.get("id")
        status = update_data.get("status")

        if not task_id or status is None:
            continue

        task_uuid = uuid.UUID(task_id)

        # Get task and verify it belongs to the user
        query = select(Task).options(selectinload(Task.user)).where(
            Task.id == task_uuid,
            Task.user_id == user_uuid
        )
        task = session.exec(query).first()

        if not task:
            continue

        # Update task status
        task.status = status
        task.updated_at = datetime.utcnow()

        session.add(task)
        updated_tasks.append(task)

    session.commit()

    # Refresh all updated tasks
    for task in updated_tasks:
        session.refresh(task)

    return updated_tasks


def create_recurring_task(session: Session, user_id: str, task_data: TaskCreate, recurrence_pattern: dict) -> Task:
    """
    Create a new recurring task for a user with specified recurrence pattern
    """
    # Validate user exists
    user = session.get(User, uuid.UUID(user_id))
    if not user:
        raise ValueError("User not found")

    # Create task object with recurrence properties
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        timestamp=task_data.timestamp,
        status=task_data.status,
        user_id=uuid.UUID(user_id),
        is_recurring=True,
        recurrence_pattern=recurrence_pattern,
        due_date=getattr(task_data, 'due_date', None),
        reminder_time=getattr(task_data, 'reminder_time', None),
        next_occurrence=_calculate_next_occurrence(recurrence_pattern, datetime.utcnow())
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def _calculate_next_occurrence(recurrence_pattern: dict, current_datetime: datetime) -> Optional[datetime]:
    """
    Calculate the next occurrence for a recurring task based on its recurrence pattern
    """
    if not recurrence_pattern or not isinstance(recurrence_pattern, dict):
        return None

    frequency = recurrence_pattern.get('frequency', 'daily')
    interval = recurrence_pattern.get('interval', 1)

    # Handle different frequencies
    if frequency == 'daily':
        next_dt = current_datetime + timedelta(days=interval)
    elif frequency == 'weekly':
        next_dt = current_datetime + timedelta(weeks=interval)
    elif frequency == 'monthly':
        # Add months by calculating the next month
        import calendar
        year = current_datetime.year
        month = current_datetime.month + interval

        # Handle year overflow
        while month > 12:
            year += 1
            month -= 12

        # Get the last day of the target month to handle months with fewer days
        max_day = calendar.monthrange(year, month)[1]
        day = min(current_datetime.day, max_day)

        next_dt = current_datetime.replace(year=year, month=month, day=day)
    elif frequency == 'yearly':
        next_dt = current_datetime.replace(year=current_datetime.year + interval)
    else:  # custom frequency
        # For custom patterns, default to daily for now
        next_dt = current_datetime + timedelta(days=interval)

    return next_dt


def generate_next_occurrence(session: Session, task: Task) -> Optional[Task]:
    """
    Generate the next occurrence of a recurring task
    """
    if not task.is_recurring or not task.recurrence_pattern:
        return None

    # Check if task has reached its end condition
    if _has_reached_end_condition(task):
        return None

    # Create a new task instance with the same properties but a new ID
    next_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        user_id=task.user_id,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern,
        due_date=task.due_date,
        reminder_time=task.reminder_time,
        next_occurrence=_calculate_next_occurrence(task.recurrence_pattern, datetime.utcnow())
    )

    # Add the new occurrence to the database
    session.add(next_task)
    session.commit()
    session.refresh(next_task)

    # Update the original task's next occurrence
    task.next_occurrence = _calculate_next_occurrence(task.recurrence_pattern, datetime.utcnow())
    session.add(task)
    session.commit()

    return next_task


def _has_reached_end_condition(task: Task) -> bool:
    """
    Check if a recurring task has reached its end condition
    """
    if not task.recurrence_pattern:
        return False

    end_condition = task.recurrence_pattern.get('end_condition')
    end_value = task.recurrence_pattern.get('end_value')

    if not end_condition or not end_value:
        return False

    if end_condition == 'count':
        # Check if the task has been completed enough times
        # This would require tracking completion count, which is not implemented yet
        # For now, we'll return False to indicate no end condition reached
        return False
    elif end_condition == 'date':
        # Check if the current date has passed the end date
        try:
            end_date = datetime.fromisoformat(str(end_value))
            return datetime.utcnow() >= end_date
        except:
            return False

    return False


def handle_due_dates_and_reminders(session: Session) -> List[Task]:
    """
    Process tasks that have due dates or reminders that need attention
    """
    # Get tasks that have due dates or reminders scheduled for now or in the past
    current_time = datetime.utcnow()

    query = select(Task).where(
        (Task.due_date.is_not(None) & (Task.due_date <= current_time)) |
        (Task.reminder_time.is_not(None) & (Task.reminder_time <= current_time)) &
        (Task.status == False)  # Only non-completed tasks
    )

    tasks_needing_attention = session.exec(query).all()

    # Process each task that needs attention
    for task in tasks_needing_attention:
        # Here we would typically trigger notifications or other actions
        # For now, we just return the list of tasks that need attention
        pass

    return tasks_needing_attention
