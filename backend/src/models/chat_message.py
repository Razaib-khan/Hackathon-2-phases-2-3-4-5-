from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from enum import Enum


class SenderType(str, Enum):
    user = "user"
    agent = "agent"


class ChatMessageBase(SQLModel):
    sender_type: SenderType = Field(nullable=False)
    content: str = Field(nullable=False)
    metadata: Optional[dict] = Field(default=None)


class ChatMessage(ChatMessageBase, table=True):
    """
    Represents individual messages in a chat session.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(nullable=False, foreign_key="chat_sessions.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    session: "ChatSession" = Relationship(back_populates="messages")


class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a new chat message."""
    sender_type: SenderType
    content: str


class ChatMessageRead(ChatMessageBase):
    """Schema for reading chat message data."""
    id: UUID
    session_id: UUID
    timestamp: datetime