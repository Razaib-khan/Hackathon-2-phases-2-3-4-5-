# Data Model: Speckit Plus Phase II – Full-Stack Todo Application

## Entity Definitions

### User Entity
**Fields**:
- id: UUID (Primary Key)
- first_name: String (max 100, required)
- last_name: String (max 100, required)
- email: String (max 255, unique, required)
- password_hash: String (required)
- favorite_teacher: String (required)
- created_at: DateTime (default: current timestamp)
- updated_at: DateTime (default: current timestamp, auto-update)

**Relationships**:
- One-to-Many: User → Tasks (via user_id foreign key)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet strength requirements (uppercase, lowercase, number, special char, min 8 chars)
- Favorite teacher must be provided for password recovery

### Task Entity
**Fields**:
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key → User.id, required)
- title: String (max 255, required)
- description: Text (optional)
- priority: String (required, enum: 'Critical', 'High', 'Medium', 'Low')
- timestamp: DateTime (default: current timestamp)
- status: Boolean (default: false)
- created_at: DateTime (default: current timestamp)
- updated_at: DateTime (default: current timestamp, auto-update)

**Relationships**:
- Many-to-One: Task → User (via user_id foreign key)

**Validation Rules**:
- Title must not exceed 255 characters
- Status must be boolean value
- Priority must be one of the allowed values
- User can only access tasks with their user_id

## State Transitions

### Task State Transitions
- **Active** ↔ **Completed**: Toggled via checkbox interaction
  - Trigger: User clicks completion checkbox
  - Action: PATCH request to `/api/{user_id}/tasks/{id}/complete`
  - Result: Status field flips from true/false

### User Authentication States
- **Anonymous** → **Authenticated**: Via login process
- **Authenticated** → **Session Expired**: Via JWT expiration or logout
- **Authenticated** → **Password Change**: Via password update process

## Indexing Strategy

### Database Indexes
- Index on `users.email` for fast authentication lookups
- Index on `tasks.user_id` for efficient user task retrieval
- Index on `tasks.priority` for filtering performance
- Index on `tasks.status` for completion status filtering
- Index on `tasks.timestamp` for chronological sorting
- Composite index on `tasks.user_id` and `tasks.created_at` for user task pagination

## Data Integrity Constraints

### Referential Integrity
- Foreign key constraint on `tasks.user_id` referencing `users.id`
- Cascade delete: When user is deleted, all their tasks are deleted

### Data Validation
- Check constraint on `tasks.priority` to ensure only allowed values
- Unique constraint on `users.email`
- Not-null constraints on required fields