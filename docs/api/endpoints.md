# API Endpoints Documentation

This document provides detailed information about the REST API endpoints available in the Speckit Plus Todo Application.

## Authentication Endpoints

### POST `/api/auth/signup`
Create a new user account.

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "password": "string (min 8 chars)",
  "favorite_teacher": "string"
}
```

**Response:**
- Status: 200 OK
- Body: User object with the created user details

**Errors:**
- 409 Conflict: Email already registered

---

### POST `/api/auth/signin`
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
- Status: 200 OK
- Body:
```json
{
  "access_token": "JWT token string",
  "token_type": "bearer",
  "user_id": "UUID string"
}
```

**Errors:**
- 401 Unauthorized: Invalid credentials

---

### POST `/api/auth/signout`
Logout user and invalidate session.

**Response:**
- Status: 200 OK
- Body: `{"message": "Logout successful"}`

---

### PUT `/api/auth/password`
Change user password.

**Request Body:**
```json
{
  "old_password": "string",
  "new_password": "string"
}
```

**Response:**
- Status: 200 OK
- Body: `{"message": "Password changed successfully"}`

---

### POST `/api/auth/forgot-password`
Handle password recovery using security question.

**Request Body:**
```json
{
  "email": "string",
  "favorite_teacher_answer": "string"
}
```

**Response:**
- Status: 200 OK
- Body: `{"message": "Password recovery successful"}`
- 404 Not Found: User not found
- 400 Bad Request: Incorrect security answer

---

### DELETE `/api/auth/account`
Delete user account and all associated data.

**Response:**
- Status: 200 OK
- Body: `{"message": "Account deleted successfully"}`

---

## Task Management Endpoints

### GET `/api/{user_id}/tasks`
Retrieve all tasks for a user with optional search and filtering.

**Path Parameters:**
- `user_id`: UUID string of the user

**Query Parameters:**
- `search`: Search keywords in title and description
- `priority`: Filter by priority level (Critical, High, Medium, Low)
- `status_filter`: Filter by completion status
- `timestamp_from`: Filter from timestamp
- `timestamp_to`: Filter to timestamp
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response:**
- Status: 200 OK
- Body: Array of Task objects

**Errors:**
- 400 Bad Request: Invalid user ID format
- 404 Not Found: User not found

---

### POST `/api/{user_id}/tasks`
Create a new task for a user.

**Path Parameters:**
- `user_id`: UUID string of the user

**Request Body:**
```json
{
  "title": "string",
  "description": "string (optional)",
  "priority": "Critical | High | Medium | Low (default: Medium)",
  "timestamp": "datetime (default: now)"
}
```

**Response:**
- Status: 200 OK
- Body: Created Task object

**Errors:**
- 400 Bad Request: Invalid user ID format
- 404 Not Found: User not found

---

### GET `/api/{user_id}/tasks/{task_id}`
Retrieve a specific task for a user.

**Path Parameters:**
- `user_id`: UUID string of the user
- `task_id`: UUID string of the task

**Response:**
- Status: 200 OK
- Body: Task object

**Errors:**
- 400 Bad Request: Invalid user ID or task ID format
- 404 Not Found: Task not found

---

### PUT `/api/{user_id}/tasks/{task_id}`
Update a task for a user.

**Path Parameters:**
- `user_id`: UUID string of the user
- `task_id`: UUID string of the task

**Request Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "priority": "Critical | High | Medium | Low (optional)",
  "status": "boolean (optional)",
  "timestamp": "datetime (optional)"
}
```

**Response:**
- Status: 200 OK
- Body: Updated Task object

**Errors:**
- 400 Bad Request: Invalid user ID or task ID format
- 404 Not Found: Task not found

---

### DELETE `/api/{user_id}/tasks/{task_id}`
Delete a task for a user.

**Path Parameters:**
- `user_id`: UUID string of the user
- `task_id`: UUID string of the task

**Response:**
- Status: 200 OK
- Body: `{"message": "Task deleted successfully"}`

**Errors:**
- 400 Bad Request: Invalid user ID or task ID format
- 404 Not Found: Task not found

---

### PATCH `/api/{user_id}/tasks/{task_id}/complete`
Toggle task completion status.

**Path Parameters:**
- `user_id`: UUID string of the user
- `task_id`: UUID string of the task

**Request Body:**
```json
{
  "complete": "boolean"
}
```

**Response:**
- Status: 200 OK
- Body: Updated Task object

**Errors:**
- 400 Bad Request: Invalid user ID or task ID format
- 404 Not Found: Task not found

---

## Data Models

### User Model
```typescript
interface User {
  id: string;           // UUID
  first_name: string;
  last_name: string;
  email: string;
  favorite_teacher: string;
  created_at: Date;
  updated_at: Date;
}
```

### Task Model
```typescript
interface Task {
  id: string;           // UUID
  user_id: string;      // UUID
  title: string;
  description: string | null;
  priority: "Critical" | "High" | "Medium" | "Low";
  timestamp: Date;
  status: boolean;      // completion status
  created_at: Date;
  updated_at: Date;
}
```