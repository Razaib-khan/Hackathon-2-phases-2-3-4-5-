# Quickstart Guide: Speckit Plus Phase II – Full-Stack Todo Application

## Development Environment Setup

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL (or Neon Serverless PostgreSQL)
- Git

### Clone and Initialize
```bash
git clone <repository-url>
cd <repository-name>
```

### Backend Setup
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and auth settings
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend  # From repository root
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit with your API endpoint
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Running the Application

### Development Mode
Both frontend and backend should be running simultaneously:
- Backend: `uvicorn src.main:app --reload` (port 8000 by default)
- Frontend: `npm run dev` (port 3000 by default)

### Accessing the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend docs: http://localhost:8000/docs

## Key Features Walkthrough

### User Registration and Authentication
**Note**: The authentication pages are not yet implemented in the frontend. The backend API supports authentication with the following endpoints:
- User registration: `POST /api/auth/signup`
- User login: `POST /api/auth/signin`
- User logout: `POST /api/auth/signout`

### Task Management
1. Navigate to `/tasks` to access the task management interface
2. Create tasks using the "Add New Task" button
3. Set title, description, and priority levels (Critical, High, Medium, Low)
4. Toggle completion status using the checkbox interface
5. View all tasks in the task list with sorting and filtering options

### Theme Switching
- Use the theme toggle (sun/moon icons) to switch between light and dark modes
- Preference is saved in browser storage

### Account Management
**Note**: Account management features are planned but not yet implemented in the frontend. The backend API supports:
- Changing password: `PUT /api/auth/password`
- Password recovery: `POST /api/auth/forgot-password`
- Account deletion: `DELETE /api/auth/account`

## API Endpoints Reference

### Task Operations
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout
- `PUT /api/auth/password` - Change password
- `POST /api/auth/forgot-password` - Password recovery
- `DELETE /api/auth/account` - Delete account

## Troubleshooting

### Common Issues
- **Database Connection**: Ensure PostgreSQL is running and credentials are correct in your `.env` file
- **Authentication**: The frontend currently uses mock authentication; real authentication requires implementing the auth pages
- **Frontend/Backend Communication**: Check that API endpoints are correctly configured and both servers are running

### Development Tips
- Use the backend API documentation at `http://localhost:8000/docs` for testing endpoints
- Check browser developer tools for frontend errors
- Enable logging in backend for debugging API issues
- Use the test page at `/test` to verify API connectivity