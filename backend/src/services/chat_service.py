"""
Chat service layer for the AI Agent Chat Interface
Handles business logic for chat sessions and messages
"""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select, func
from uuid import UUID, uuid4

from models.chat_session import ChatSession, ChatSessionCreate
from models.chat_message import ChatMessage, ChatMessageCreate, SenderType
from models.task_operation_log import TaskOperationLog, OperationType


def create_chat_session(session: Session, user_id: str, title: str) -> ChatSession:
    """
    Create a new chat session for a user
    """
    chat_session = ChatSession(
        user_id=user_id,
        title=title
    )
    session.add(chat_session)
    session.commit()
    session.refresh(chat_session)
    return chat_session


def get_user_sessions(
    session: Session,
    user_id: str,
    page: int = 1,
    limit: int = 10
) -> List[ChatSession]:
    """
    Get chat sessions for a specific user with pagination
    """
    offset = (page - 1) * limit

    stmt = (
        select(ChatSession)
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )

    chat_sessions = session.exec(stmt).all()
    return chat_sessions


def get_session_by_id(session: Session, session_id: str) -> Optional[ChatSession]:
    """
    Get a specific chat session by its ID
    """
    stmt = select(ChatSession).where(ChatSession.id == session_id)
    chat_session = session.exec(stmt).first()
    return chat_session


def get_session_messages(
    session: Session,
    session_id: str,
    page: int = 1,
    limit: int = 20
) -> List[ChatMessage]:
    """
    Get messages for a specific session with pagination
    """
    offset = (page - 1) * limit

    stmt = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.timestamp.asc())
        .offset(offset)
        .limit(limit)
    )

    messages = session.exec(stmt).all()
    return messages


def save_message(
    session: Session,
    session_id: str,
    sender_type: str,
    content: str,
    metadata: Optional[dict] = None
) -> ChatMessage:
    """
    Save a message to a chat session
    """
    message = ChatMessage(
        session_id=session_id,
        sender_type=sender_type,
        content=content,
        metadata=metadata
    )

    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def create_task_operation_log(
    session: Session,
    session_id: str,
    operation_type: OperationType,
    task_ids: List[str],
    result: dict
) -> TaskOperationLog:
    """
    Create a log entry for a task operation performed by the AI agent
    """
    operation_log = TaskOperationLog(
        session_id=session_id,
        operation_type=operation_type,
        task_ids=task_ids,
        result=result
    )

    session.add(operation_log)
    session.commit()
    session.refresh(operation_log)
    return operation_log


def get_session_operation_logs(
    session: Session,
    session_id: str
) -> List[TaskOperationLog]:
    """
    Get all task operation logs for a specific session
    """
    stmt = (
        select(TaskOperationLog)
        .where(TaskOperationLog.session_id == session_id)
        .order_by(TaskOperationLog.timestamp.desc())
    )

    operation_logs = session.exec(stmt).all()
    return operation_logs