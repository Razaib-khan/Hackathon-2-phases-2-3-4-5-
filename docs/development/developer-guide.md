# Developer Documentation

This document provides technical information for developers working on the Speckit Plus Todo Application, including architecture, setup, and development practices.

## Architecture Overview

### Technology Stack
- **Backend**: FastAPI (Python 3.9+)
- **Database**: SQLModel with SQLite (can be extended to PostgreSQL)
- **Frontend**: Next.js 14+ with TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: JWT tokens
- **Testing**: Pytest (backend), Jest (frontend)

### Project Structure
```
speckit-plus-todo/
├── backend/
│   ├── src/
│   │   ├── api/          # API route definitions
│   │   ├── models/       # Data models (SQLModel)
│   │   ├── services/     # Business logic
│   │   ├── database/     # Database configuration
│   │   └── main.py       # Application entry point
│   ├── requirements.txt
│   └── alembic/          # Database migrations
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js pages and routing
│   │   ├── components/   # Reusable UI components
│   │   ├── contexts/     # React contexts (AuthContext)
│   │   ├── services/     # API service layer
│   │   ├── styles/       # Global styles
│   │   └── utils/        # Utility functions
│   ├── package.json
│   └── tsconfig.json
├── docs/                 # Documentation
└── specs/                # Specification files
```

## Backend Development

### Setup Instructions

1. **Environment Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Variables**
Create a `.env` file in the backend root:
```
DATABASE_URL=sqlite:///./todo_app.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Run the Backend**
```bash
cd src
uvicorn main:app --reload --port 8000
```

### Key Components

#### API Layer (`/api/`)
- `auth.py`: Authentication endpoints
- `tasks.py`: Task management endpoints
- Each file contains route definitions with proper validation

#### Models (`/models/`)
- `user.py`: User entity with relationships
- `task.py`: Task entity with priority and status
- SQLModel-based models with validation

#### Services (`/services/`)
- `user_service.py`: User business logic
- `task_service.py`: Task business logic
- `auth_service.py`: Authentication utilities
- Separation of concerns between API and business logic

#### Database (`/database/`)
- `database.py`: Connection and initialization logic
- Uses SQLModel for ORM functionality
- SQLite by default with extensibility to other databases

### API Design Patterns

#### Response Models
```python
# All API endpoints return typed responses
@app.get("/users/{id}", response_model=UserRead)
def get_user(...):
    # Automatically validates response structure
```

#### Dependency Injection
```python
# Database session injected into endpoints
def get_user(session: Session = Depends(get_session)):
```

#### Error Handling
```python
# Standardized error responses
raise HTTPException(status_code=404, detail="User not found")
```

## Frontend Development

### Setup Instructions

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Environment Variables**
Create `.env.local` in the frontend root:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

3. **Run the Frontend**
```bash
npm run dev
```

### Key Components

#### Pages (`/app/`)
- `layout.tsx`: Root layout with theme support
- `page.tsx`: Home page
- `tasks/page.tsx`: Main task management page
- `test/page.tsx`: Testing page

#### Components (`/components/`)
- `Auth/`: Authentication-related components
- `TaskForm/`: Task creation/editing form
- `TaskItem/`: Individual task display
- `TaskList/`: Task listing with filtering
- `ThemeToggle/`: Dark/light mode toggle

#### Contexts (`/contexts/`)
- `AuthContext.tsx`: User authentication state management
- Global state for user session

#### Services (`/services/`)
- `api.ts`: API client with type safety
- Axios-based HTTP requests
- Type definitions for all API entities

### Component Architecture

#### Task Management Flow
```
TasksPage (Container)
├── TaskForm (Controlled component)
├── TaskList (Displays tasks)
└── TaskItem (Individual task UI)
```

#### State Management
- Local state for form inputs
- Context for authentication state
- API calls for persistence

## Database Schema

### Tables

#### Users Table
```
users
├── id: UUID (Primary Key)
├── first_name: VARCHAR(100)
├── last_name: VARCHAR(100)
├── email: VARCHAR(255) UNIQUE
├── password_hash: TEXT
├── favorite_teacher: TEXT
├── created_at: TIMESTAMP
└── updated_at: TIMESTAMP
```

#### Tasks Table
```
tasks
├── id: UUID (Primary Key)
├── user_id: UUID (Foreign Key → users.id)
├── title: VARCHAR(255)
├── description: TEXT
├── priority: ENUM('Critical', 'High', 'Medium', 'Low')
├── timestamp: TIMESTAMP
├── status: BOOLEAN (completion status)
├── created_at: TIMESTAMP
└── updated_at: TIMESTAMP
```

## API Integration

### Frontend API Calls
```typescript
// Example service call
import { createTask } from '@/src/services/api';

const newTask = await createTask(userId, {
  title: "New Task",
  description: "Task description",
  priority: "High"
});
```

### Error Handling
- Network error catching
- Status code checking
- User-friendly error messages
- Loading states

## Testing

### Backend Tests
Located in `/backend/tests/`
```bash
# Run backend tests
cd backend
pytest
```

### Frontend Tests
Located in `/frontend/`
```bash
# Run frontend tests
cd frontend
npm test
```

## Deployment

### Production Build
```bash
# Backend (Docker recommended)
docker build -t speckit-todo-backend .

# Frontend
cd frontend
npm run build
```

### Environment Configuration
- Separate configs for development/staging/production
- Secrets managed through environment variables
- Database URL configuration

## Development Best Practices

### Code Style
- Python: Black formatter, flake8 linting
- TypeScript: ESLint with Next.js recommended rules
- Consistent naming conventions
- Comprehensive docstrings

### Git Workflow
- Feature branches for new functionality
- Pull requests with code reviews
- Semantic versioning
- Commit message conventions

### API Design
- RESTful principles
- Consistent response formats
- Proper HTTP status codes
- Input validation
- Error handling

### Security
- Input sanitization
- Authentication for all sensitive endpoints
- Password hashing
- JWT token security
- SQL injection prevention

## Troubleshooting

### Common Issues
- Database connection problems
- CORS configuration
- Environment variable misconfiguration
- Type mismatch errors

### Debugging Tips
- Enable detailed logging in development
- Use browser dev tools for frontend debugging
- Check backend logs for API errors
- Verify environment variables

## Performance Considerations

### Backend Optimization
- Database indexing strategies
- Efficient query patterns
- Caching mechanisms
- Connection pooling

### Frontend Optimization
- Component lazy loading
- Image optimization
- Bundle size reduction
- API request caching