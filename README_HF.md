---
title: AIDO TODO Backend
emoji: 🚀
colorFrom: purple
colorTo: yellow
sdk: docker
pinned: false
license: mit
---

# AIDO TODO Application Backend

This is the backend for the AIDO TODO Application, built with FastAPI and deployed on Hugging Face Spaces using Docker.

## Overview

This backend provides a complete API for the AIDO TODO application with features including:
- User authentication and management
- Task CRUD operations
- Search and filter capabilities
- Security measures including rate limiting and input sanitization

## Endpoints

The API provides the following main endpoints:
- `/api/auth/` - Authentication routes (signup, signin, password reset)
- `/api/tasks/` - Task management routes (create, read, update, delete)
- `/api/users/` - User management routes

## Environment Variables

This application requires the following environment variables to be set:
- `DATABASE_URL` - PostgreSQL database connection string
- `JWT_SECRET_KEY` - Secret key for JWT token signing
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins for CORS

## Usage

The backend is designed to work with the AIDO TODO frontend application. Once deployed, you can access the API documentation at `/docs` or `/redoc`.

## Architecture

Built with:
- FastAPI for the web framework
- SQLModel for database modeling
- PostgreSQL for the database (via Neon)
- Uvicorn for the ASGI server