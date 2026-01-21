from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4


class ChatSessionBase(SQLModel):
    title: str = Field(max_length=255, nullable=False)


class ChatSession(ChatSessionBase, table=True):
    """
    Represents a conversation session between user and AI agent.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(nullable=False, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["ChatMessage"] = Relationship(back_populates="session")

    # Update the updated_at timestamp automatically
    def __setattr__(self, name, value):
        if name == 'updated_at':
            super().__setattr__('updated_at', datetime.utcnow())
        super().__setattr__(name, value)


class ChatSessionCreate(ChatSessionBase):
    """Schema for creating a new chat session."""
    title: str


class ChatSessionRead(ChatSessionBase):
    """Schema for reading chat session data."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime