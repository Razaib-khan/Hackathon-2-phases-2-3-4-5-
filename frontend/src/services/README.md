# API Service Documentation

The API service in `frontend/src/services/api.ts` handles communication with the backend API endpoints for tasks. It provides functions for getting, creating, updating, and deleting tasks using the API endpoints defined in the spec.

## Features

- **TypeScript Support**: Full TypeScript typing with interfaces for all API objects
- **Authentication**: Automatic JWT token handling via interceptors
- **Error Handling**: Comprehensive error handling with logging
- **Environment Configuration**: Configurable API base URL via environment variables
- **Browser Compatibility**: Interceptors only set up in browser environments

## Available Methods

### `getTasks(userId, params?)`
- Retrieves all tasks for a user
- Optional filters: search, priority, status, timestamps, pagination

### `getTask(userId, taskId)`
- Retrieves a specific task by ID

### `createTask(userId, taskData)`
- Creates a new task
- Requires: title, priority

### `updateTask(userId, taskId, taskData)`
- Updates an existing task
- Partial updates supported

### `deleteTask(userId, taskId)`
- Deletes a task

### `toggleTaskCompletion(userId, taskId, complete)`
- Toggles the completion status of a task

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the API (defaults to http://localhost:8000)

## Usage Example

```typescript
import { getTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '@/src/services/api';

// Get all tasks for a user
const tasks = await getTasks('user-123');

// Create a new task
const newTask = await createTask('user-123', {
  title: 'New Task',
  priority: 'High',
  description: 'Task description'
});

// Update a task
const updatedTask = await updateTask('user-123', 'task-456', {
  title: 'Updated Title',
  status: true
});

// Delete a task
await deleteTask('user-123', 'task-456');

// Toggle task completion
const toggledTask = await toggleTaskCompletion('user-123', 'task-456', true);
```

## Security

- Automatically includes Authorization header with JWT token from localStorage
- Handles 401 errors by removing the token and redirecting to login
- Secure by design with proper error handling