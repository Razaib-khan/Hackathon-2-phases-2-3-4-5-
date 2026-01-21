from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from enum import Enum
import json


class OperationType(str, Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"
    status_update = "status_update"


class TaskOperationLogBase(SQLModel):
    operation_type: OperationType = Field(nullable=False)
    task_ids: Optional[List[str]] = Field(default=None)
    result: Optional[dict] = Field(default=None)


class TaskOperationLog(TaskOperationLogBase, table=True):
    """
    Represents AI agent operations on tasks.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(nullable=False, foreign_key="chat_sessions.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    session: "ChatSession" = Relationship(back_populates="task_operations")

    # Custom serialization for the task_ids array and result JSON
    @classmethod
    def parse_obj(cls, obj):
        if isinstance(obj.get('task_ids'), str):
            obj['task_ids'] = json.loads(obj['task_ids'])
        if isinstance(obj.get('result'), str):
            obj['result'] = json.loads(obj['result'])
        return super().parse_obj(obj)


class TaskOperationLogCreate(TaskOperationLogBase):
    """Schema for creating a new task operation log."""
    operation_type: OperationType
    session_id: UUID


class TaskOperationLogRead(TaskOperationLogBase):
    """Schema for reading task operation log data."""
    id: UUID
    session_id: UUID
    timestamp: datetime