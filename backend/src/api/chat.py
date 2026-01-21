"""
Chat API routes for the AI Agent Chat Interface
Handles chat sessions, messages, and AI agent integration
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from uuid import UUID

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_session
from models.chat_session import ChatSession, ChatSessionCreate, ChatSessionRead
from models.chat_message import ChatMessage, ChatMessageCreate, ChatMessageRead
from models.user import User
from services.chat_service import (
    create_chat_session,
    get_user_sessions,
    get_session_messages,
    save_message,
    get_session_by_id
)
from utils.validation import validate_user_id
from utils.auth import get_current_user
from middleware.security import limiter

router = APIRouter()


@router.get("/chat/sessions", response_model=dict)
def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Items per page")
):
    """
    Retrieve user's chat sessions with pagination
    """
    user_sessions = get_user_sessions(
        session=session,
        user_id=str(current_user.id),
        page=page,
        limit=limit
    )

    return {
        "sessions": user_sessions,
        "total": len(user_sessions),
        "page": page,
        "limit": limit
    }


@router.post("/chat/sessions", response_model=ChatSessionRead)
def create_chat_session_endpoint(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new chat session
    """
    chat_session = create_chat_session(
        session=session,
        user_id=str(current_user.id),
        title=session_data.title
    )

    return chat_session


@router.get("/chat/sessions/{session_id}/messages", response_model=dict)
def get_chat_messages(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Retrieve messages for a specific chat session
    """
    # Verify user has access to this session
    chat_session = get_session_by_id(session, str(session_id))
    if not chat_session or str(chat_session.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this session")

    messages = get_session_messages(
        session=session,
        session_id=str(session_id),
        page=page,
        limit=limit
    )

    return {
        "messages": messages,
        "total": len(messages),
        "page": page,
        "limit": limit
    }


@router.post("/chat/messages", response_model=dict)
def send_message(
    message_data: dict,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI agent
    """
    session_id = message_data.get("session_id")
    content = message_data.get("content")

    if not content:
        raise HTTPException(status_code=400, detail="Content is required")

    # If no session_id provided, create a new session
    if not session_id:
        chat_session = create_chat_session(
            session=session,
            user_id=str(current_user.id),
            title="New Conversation"
        )
        session_id = chat_session.id

    # Verify user has access to this session
    chat_session = get_session_by_id(session, str(session_id))
    if not chat_session or str(chat_session.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this session")

    # Save user message
    user_message = save_message(
        session=session,
        session_id=str(session_id),
        sender_type="user",
        content=content
    )

    # TODO: Here would be the integration with the AI agent and MCP server
    # For now, returning the user message and a placeholder response
    agent_response = save_message(
        session=session,
        session_id=str(session_id),
        sender_type="agent",
        content="This is a placeholder response. The AI agent integration will be implemented in the next phase."
    )

    return {
        "user_message": user_message,
        "agent_response": agent_response
    }