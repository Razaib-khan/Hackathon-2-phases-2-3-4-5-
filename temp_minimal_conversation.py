# Minimal conversation history model for reset
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


class ConversationHistory(SQLModel, table=True):
    __tablename__ = "conversation_history"

    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str
    conversation_id: str
    message_content: str
    message_role: str
    timestamp: datetime
    is_summarized: bool = False
    summary_text: Optional[str] = None


class ConversationHistoryCreate(SQLModel):
    user_id: str
    conversation_id: str
    message_content: str
    message_role: str
    timestamp: datetime
    is_summarized: bool = False
    summary_text: Optional[str] = None


class ConversationHistoryRead(SQLModel):
    id: str
    user_id: str
    conversation_id: str
    message_content: str
    message_role: str
    timestamp: datetime
    is_summarized: bool
    summary_text: Optional[str]