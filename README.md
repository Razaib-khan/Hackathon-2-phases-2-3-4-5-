# AIDO TODO Application

A full-stack todo application with CRUD operations, authentication, and search/filter capabilities.

## Features

- **User Authentication**: Secure signup, signin, password recovery using security questions
- **Task Management**: Create, read, update, and delete tasks
- **Task Organization**: Mark tasks as complete/incomplete, assign priority levels
- **Search & Filter**: Find tasks by keywords and filter by priority, status, and timestamp
- **Theme Support**: Dark/light mode toggle with preference persistence
- **User Isolation**: Each user can only access their own tasks

## Tech Stack

- **Frontend**: Next.js 16.1.1
- **Backend**: FastAPI
- **Database**: SQLModel with Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Testing**: Jest (frontend), pytest (backend)

## API Endpoints

### Task Management
- `GET /api/{user_id}/tasks` - Retrieve user tasks with optional search/filter
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Retrieve specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout
- `PUT /api/auth/password` - Change password
- `POST /api/auth/forgot-password` - Password recovery
- `DELETE /api/auth/account` - Delete account

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env` file

4. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `JWT_ALGORITHM`: Algorithm for JWT token encoding
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time
- `NEON_DATABASE_URL`: Neon database connection string (if using Neon)

## Database Schema

### Users Table
- id: UUID (Primary Key)
- first_name: VARCHAR(100) (NOT NULL)
- last_name: VARCHAR(100) (NOT NULL)
- email: VARCHAR(255) (UNIQUE, NOT NULL)
- password_hash: TEXT (NOT NULL)
- favorite_teacher: TEXT (NOT NULL)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### Tasks Table
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key → users.id, NOT NULL)
- title: VARCHAR(255) (NOT NULL)
- description: TEXT (NULL)
- priority: VARCHAR(20) (NOT NULL, CHECK: 'Critical'/'High'/'Medium'/'Low')
- timestamp: TIMESTAMP
- status: BOOLEAN (Default: FALSE)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

## Security Features

- JWT-based authentication for all API calls
- User isolation - each user can only access their own tasks
- Password strength validation
- Rate limiting for authentication attempts
- SQL injection and XSS prevention