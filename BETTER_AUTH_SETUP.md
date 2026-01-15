# Better Auth Integration

This project implements Better Auth for both frontend and backend authentication, with proper JWT token handling for user isolation.

## Architecture Overview

- **Frontend**: Next.js application with Better Auth for user authentication
- **Backend**: FastAPI application that receives authenticated requests from frontend
- **Authentication Flow**:
  1. Users authenticate via Better Auth in Next.js frontend
  2. Better Auth manages sessions and cookies
  3. Frontend communicates user identity to FastAPI backend using JWT tokens
  4. FastAPI validates tokens and enforces user isolation

## Configuration Files

### Frontend Configuration
- `frontend/src/lib/auth.ts`: Better Auth client configuration
- `frontend/src/components/AuthProviderWrapper.tsx`: React provider wrapper
- `frontend/src/app/api/auth/route.ts`: Better Auth API endpoints
- `frontend/src/lib/better-auth-integration.ts`: Integration service between frontend auth and backend

### Backend Configuration
- `backend/auth_config.py`: Better Auth backend configuration (placeholder)
- `backend/better_auth_integration.py`: Integration layer for FastAPI
- `backend/main.py`: FastAPI app with Better Auth middleware
- `backend/services/auth_service.py`: Authentication service with user isolation

## Environment Variables

### Frontend (.env.local)
```bash
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-better-auth-secret-change-in-production
```

### Backend (.env)
```bash
BETTER_AUTH_SECRET=your-better-auth-secret-change-in-production
JWT_SECRET_KEY=your-jwt-secret-change-in-production
DATABASE_URL=postgresql://...
```

## Key Features

1. **User Registration/Login**: Handled by Better Auth
2. **Session Management**: Automatic session handling by Better Auth
3. **User Isolation**: Each user can only access their own data
4. **JWT Token Handling**: Secure token-based communication between frontend and backend
5. **Security Features**: Password requirements, rate limiting, secure cookies

## API Endpoints

### Frontend Auth Endpoints
- `/api/auth/*` - Better Auth API routes
- `/auth/signin` - Login page
- `/auth/signup` - Registration page
- `/account` - Account management

### Backend API Endpoints
- `/api/auth/*` - Legacy auth endpoints (kept for compatibility)
- `/secure-test` - Example protected endpoint
- `/tasks/*` - User-isolated task endpoints

## Testing

To test the authentication flow:
1. Visit `/test-auth` page to verify session status
2. Use `/auth/signin` or `/auth/signup` to authenticate
3. Access protected backend endpoints with valid tokens

## Security Considerations

- Use strong secrets in production
- Enable HTTPS in production
- Implement proper rate limiting
- Validate all user inputs
- Follow security best practices for JWT handling