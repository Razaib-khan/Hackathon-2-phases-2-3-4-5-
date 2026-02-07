"""
Main application entry point for the AIDO TODO Application
Sets up FastAPI app with routes and database configuration
"""

import uuid
import re
from contextlib import asynccontextmanager
from typing import List
import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import create_db_and_tables, get_session
from models.task import Task, TaskComplete, TaskCreate, TaskRead, TaskUpdate
from models.user import User, UserCreate, UserRead, UserUpdate
from middleware.security import register_security_middleware, sanitize_input
from config.security import SecurityConfig
from security.middleware import (
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    InputValidationMiddleware,
    SecurityLoggerMiddleware
)

# Import Dapr dependencies if available
try:
    import dapr.ext.fastapi as dapr_ext
    from dapr.clients import DaprClient
    HAS_DAPR = True
except ImportError:
    HAS_DAPR = False
    logging.warning("Dapr not available, running without Dapr integration")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_db_and_tables()

    # Initialize Dapr if available
    if HAS_DAPR:
        # Initialize Dapr extension for FastAPI
        dapr_ext.AsgiDaprApp(app, dapr_http_port=3500)

        # Set up Dapr client for service invocation and other operations
        app.state.dapr_client = DaprClient()

    yield


app = FastAPI(
    title="AIDO TODO API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add security middleware in order of importance
app.add_middleware(SecurityLoggerMiddleware)
app.add_middleware(InputValidationMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=SecurityConfig.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register security middleware
register_security_middleware(app)


@app.get("/")
def read_root():
    return {"message": "Welcome to AIDO TODO API"}


# Include API routes
from .api import auth, tasks, chat

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

# Health check endpoints
@app.get("/health", tags=["health"])
def health_check():
    from .services.health_check import get_health_status
    return get_health_status()

@app.get("/metrics", tags=["health"])
def metrics():
    from .services.health_check import get_application_metrics
    return get_application_metrics()

@app.get("/ready", tags=["health"])
def readiness_check():
    from .services.health_check import is_healthy
    if is_healthy():
        return {"status": "ready"}
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Service not ready")

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
