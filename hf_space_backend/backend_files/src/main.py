"""
Main application entry point for the AIDO TODO Application
Sets up FastAPI app with routes and database configuration
"""

import uuid
import re
from contextlib import asynccontextmanager
from typing import List

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_db_and_tables()
    yield


app = FastAPI(
    title="AIDO TODO API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

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
from .api import auth, tasks

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
