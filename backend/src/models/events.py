"""
Event models for the Speckit Plus Todo Application
Defines event structures for the event-driven architecture
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel
import uuid


class EventTypeEnum(str, Enum):
    """
    Enum for different event types
    """
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_DELETED = "task.deleted"
    REMINDER_TRIGGERED = "reminder.triggered"
    RECURRING_TASK_GENERATED = "recurring_task.generated"


class BaseEvent(BaseModel):
    """
    Base event model with common fields
    """
    event_id: str
    event_type: EventTypeEnum
    timestamp: datetime
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    user_id: str
    data: Dict[str, Any]


class TaskCreatedEvent(BaseEvent):
    """
    Event for when a task is created
    """
    event_type: EventTypeEnum = EventTypeEnum.TASK_CREATED
    data: Dict[str, Any]  # Contains the task data


class TaskUpdatedEvent(BaseEvent):
    """
    Event for when a task is updated
    """
    event_type: EventTypeEnum = EventTypeEnum.TASK_UPDATED
    data: Dict[str, Any]  # Contains the updated task data and original data


class TaskCompletedEvent(BaseEvent):
    """
    Event for when a task is completed
    """
    event_type: EventTypeEnum = EventTypeEnum.TASK_COMPLETED
    data: Dict[str, Any]  # Contains the task data


class TaskDeletedEvent(BaseEvent):
    """
    Event for when a task is deleted
    """
    event_type: EventTypeEnum = EventTypeEnum.TASK_DELETED
    data: Dict[str, Any]  # Contains the task ID and metadata


class ReminderTriggeredEvent(BaseEvent):
    """
    Event for when a reminder is triggered
    """
    event_type: EventTypeEnum = EventTypeEnum.REMINDER_TRIGGERED
    data: Dict[str, Any]  # Contains reminder details and task info


class RecurringTaskGeneratedEvent(BaseEvent):
    """
    Event for when a recurring task generates a new occurrence
    """
    event_type: EventTypeEnum = EventTypeEnum.RECURRING_TASK_GENERATED
    data: Dict[str, Any]  # Contains the new task data and recurrence info


class EventFactory:
    """
    Factory class to create events based on event type
    """

    @staticmethod
    def create_event(event_type: EventTypeEnum, user_id: str, data: Dict[str, Any],
                    correlation_id: Optional[str] = None, causation_id: Optional[str] = None) -> BaseEvent:
        """
        Create an event instance based on the event type
        """
        event_id = str(uuid.uuid4())

        event_params = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp": datetime.utcnow(),
            "correlation_id": correlation_id,
            "causation_id": causation_id,
            "user_id": user_id,
            "data": data
        }

        if event_type == EventTypeEnum.TASK_CREATED:
            return TaskCreatedEvent(**event_params)
        elif event_type == EventTypeEnum.TASK_UPDATED:
            return TaskUpdatedEvent(**event_params)
        elif event_type == EventTypeEnum.TASK_COMPLETED:
            return TaskCompletedEvent(**event_params)
        elif event_type == EventTypeEnum.TASK_DELETED:
            return TaskDeletedEvent(**event_params)
        elif event_type == EventTypeEnum.REMINDER_TRIGGERED:
            return ReminderTriggeredEvent(**event_params)
        elif event_type == EventTypeEnum.RECURRING_TASK_GENERATED:
            return RecurringTaskGeneratedEvent(**event_params)
        else:
            raise ValueError(f"Unknown event type: {event_type}")


# Topic names for Kafka
TASK_EVENTS_TOPIC = "task-events"
REMINDERS_TOPIC = "reminders"
TASK_UPDATES_TOPIC = "task-updates"