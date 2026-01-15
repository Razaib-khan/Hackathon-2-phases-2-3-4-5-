---
name: frontend-backend-alignment
description: |
  Align frontend and backend systems to ensure proper API integration. Use when coordinating
  frontend–backend API communication, debugging connection issues, verifying request/response
  contracts, or resolving integration problems between frontend components and backend services.
  Covers endpoint mapping, authentication flow, data validation, and error handling patterns.
  NOT when working on pure frontend UI or pure backend logic without integration concerns.
---

# Frontend-Backend Alignment

Ensure proper integration between frontend and backend systems with correct API communication patterns.

## Core Responsibilities

### 1. API Endpoint Verification
Verify all frontend API calls correctly map to existing backend endpoints:

```typescript
// CORRECT: Well-defined API contract
interface ApiContract {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  requestSchema: object;
  responseSchema: object;
  authRequired: boolean;
}

// Example: Task creation endpoint
const createTaskEndpoint: ApiContract = {
  path: '/api/{user_id}/tasks',
  method: 'POST',
  requestSchema: {
    title: string,
    description?: string,
    priority: 'Critical' | 'High' | 'Medium' | 'Low',
    timestamp?: string
  },
  responseSchema: {
    id: string,
    user_id: string,
    title: string,
    description?: string,
    priority: string,
    timestamp: string,
    status: boolean,
    created_at: string,
    updated_at: string
  },
  authRequired: true
};
```

### 2. Request Structure Validation
Ensure frontend requests match backend expectations:

```typescript
// CORRECT: Proper authentication header handling
class ApiService {
  private setupInterceptors() {
    this.axiosClient.interceptors.request.use(
      (config: any) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      }
    );
  }
}

// CORRECT: Proper error handling for different HTTP statuses
private handleError(error: any): void {
  if (error.response?.status === 401) {
    // Handle unauthorized access
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  } else if (error.response?.status === 404) {
    // Handle not found errors
    console.error('Endpoint not found:', error.response.config.url);
  } else if (error.request) {
    // Handle network errors
    console.error('Network error:', error.request);
  }
}
```

### 3. Authentication Flow Coordination
Ensure consistent authentication between frontend and backend:

```typescript
// CORRECT: Authentication flow with proper token handling
class AuthService {
  async login(credentials: { email: string, password: string }): Promise<AuthResponse> {
    try {
      // Call backend auth endpoint
      const response = await fetch('http://localhost:8000/api/auth/signin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      const { user_id, access_token } = data;

      // Store token and user data
      localStorage.setItem('access_token', access_token);

      return { user_id, access_token };
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  }
}
```

---

## Error Diagnosis & Resolution

### Common HTTP Error Patterns

#### 404 Not Found
**Symptoms**: Frontend request returns 404
**Diagnosis Steps**:
1. Verify the endpoint path matches exactly
2. Check if the backend server is running
3. Confirm HTTP method matches (GET vs POST vs PUT)
4. Ensure route parameters are correctly formatted

```bash
# Verify backend is running
curl http://localhost:8000/docs

# Check specific endpoint
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password"}'
```

#### 400 Bad Request
**Symptoms**: Request fails with validation errors
**Diagnosis Steps**:
1. Verify request payload structure matches backend expectation
2. Check data types (string vs number vs boolean)
3. Ensure required fields are present
4. Validate data formats (dates, emails, etc.)

#### 401 Unauthorized
**Symptoms**: Request fails due to authentication issues
**Diagnosis Steps**:
1. Verify JWT token is present in request headers
2. Check if token has expired
3. Ensure correct header format (`Authorization: Bearer <token>`)
4. Confirm token was issued by the same service

#### 500 Server Errors
**Symptoms**: Internal server errors
**Diagnosis Steps**:
1. Check backend logs for stack traces
2. Verify database connectivity
3. Confirm environment variables are set
4. Test with simpler requests to isolate the issue

---

## Integration Patterns

### 1. User Isolation Pattern
Ensure each user can only access their own data:

```typescript
// Frontend: Include user ID in all requests
async getUserTasks(userId: string) {
  const response = await fetch(`http://localhost:8000/api/${userId}/tasks`, {
    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
  });
  return response.json();
}

// Backend: Validate user ID matches authenticated user
@app.get("/api/{user_id}/tasks")
def get_tasks(user_id: str, current_user: User = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    # Return user's tasks
```

### 2. CORS Configuration
Ensure proper cross-origin communication:

```python
# Backend: Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend: Use absolute URLs to backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
```

### 3. Environment-Specific Configuration
Handle different environments consistently:

```typescript
// Frontend: Environment-based API URL
const getApiBaseUrl = () => {
  switch (process.env.NODE_ENV) {
    case 'development':
      return 'http://localhost:8000';
    case 'production':
      return process.env.REACT_APP_API_URL;
    default:
      return 'http://localhost:8000';
  }
};
```

---

## Debugging Workflow

### Phase 1: Request Verification
1. **Trace the request path**: From frontend call → network → backend endpoint
2. **Validate the contract**: Match request structure to backend expectation
3. **Check authentication**: Verify tokens and headers are properly set

### Phase 2: Response Analysis
1. **Inspect response**: Check status codes, headers, and body
2. **Validate parsing**: Ensure frontend correctly handles response format
3. **Error handling**: Verify error responses are properly caught and handled

### Phase 3: Integration Testing
1. **End-to-end flow**: Test complete user journeys
2. **Edge cases**: Test with invalid data, expired tokens, etc.
3. **Performance**: Monitor response times and connection stability

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ frontend-backend-alignment skill ready`

## If Verification Fails

1. Check: references/ folder has frontend-backend-contracts.md
2. **Stop and report** if still failing

## Related Skills

- **configuring-better-auth** - Advanced authentication patterns
- **building-nextjs-apps** - Frontend application structure
- **scaffolding-fastapi-dapr** - Backend service patterns

## References

- [references/frontend-backend-contracts.md](references/frontend-backend-contracts.md) - API contract patterns and validation
- [references/integration-testing.md](references/integration-testing.md) - End-to-end testing strategies for frontend-backend systems
- [references/error-handling-patterns.md](references/error-handling-patterns.md) - Comprehensive error handling between frontend and backend