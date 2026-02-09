# Data Model: AI Agent Chat Interface for AIDO TODO Application

## Entity Definitions

### ChatSession
- **id**: UUID (Primary Key, Default: gen_random_uuid())
- **user_id**: UUID (Foreign Key → users.id, NOT NULL)
- **title**: VARCHAR(255) (NOT NULL)
- **created_at**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **updated_at**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **relationships**:
  - One-to-many with ChatMessage (one session has many messages)
  - Belongs to User (one user has many sessions)
- **Validation Rules**:
    - user_id must exist in users table (foreign key constraint)
    - title cannot be empty
    - user_id must match authenticated user for access (authorization check)

### ChatMessage
- **id**: UUID (Primary Key, Default: gen_random_uuid())
- **session_id**: UUID (Foreign Key → chat_sessions.id, NOT NULL)
- **sender_type**: VARCHAR(20) (NOT NULL, CHECK: 'user'/'agent')
- **content**: TEXT (NOT NULL)
- **timestamp**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **metadata**: JSONB (NULL) - For storing additional message context
- **relationships**:
  - Many-to-one with ChatSession (many messages belong to one session)
- **Validation Rules**:
    - session_id must exist in chat_sessions table (foreign key constraint)
    - sender_type must be either 'user' or 'agent'
    - content cannot be empty
    - session_id must belong to authenticated user (authorization check)

### TaskOperationLog
- **id**: UUID (Primary Key, Default: gen_random_uuid())
- **session_id**: UUID (Foreign Key → chat_sessions.id, NOT NULL)
- **operation_type**: VARCHAR(20) (NOT NULL, CHECK: 'create'/'read'/'update'/'delete'/'status_update')
- **task_ids**: TEXT[] (Array of task IDs involved in operation)
- **result**: JSONB (Result of the operation)
- **timestamp**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **relationships**:
  - Many-to-one with ChatSession (many logs belong to one session)
- **Validation Rules**:
    - session_id must exist in chat_sessions table (foreign key constraint)
    - operation_type must be one of the allowed values
    - session_id must belong to authenticated user (authorization check)

### Existing Task Model (Extended)
- **id**: UUID (Primary Key, Default: gen_random_uuid())
- **user_id**: UUID (Foreign Key → users.id, NOT NULL)
- **title**: VARCHAR(255) (NOT NULL)
- **description**: TEXT (NULL)
- **priority**: VARCHAR(20) (NOT NULL, CHECK: 'Critical'/'High'/'Medium'/'Low')
- **timestamp**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **status**: BOOLEAN (Default: FALSE)
- **created_at**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **updated_at**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **relationships**:
  - Belongs to User (many tasks belong to one user)
  - One-to-many with TaskOperationLog (one task can be involved in many operations)

### User Model (Existing)
- **id**: UUID (Primary Key, Default: gen_random_uuid())
- **first_name**: VARCHAR(100) (NOT NULL)
- **last_name**: VARCHAR(100) (NOT NULL)
- **email**: VARCHAR(255) (UNIQUE, NOT NULL)
- **password_hash**: TEXT (NOT NULL)
- **favorite_teacher**: TEXT (NOT NULL)
- **created_at**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **updated_at**: TIMESTAMP (Default: CURRENT_TIMESTAMP)
- **relationships**:
  - One-to-many with Task (one user has many tasks)
  - One-to-many with ChatSession (one user has many chat sessions)

## State Transitions

### ChatMessage
- Created when user or agent sends a message
- Remains immutable after creation

### TaskOperationLog
- Created when AI agent performs an operation on tasks
- Remains immutable after creation

## Indexing Strategy

### Database Indexes
- Index on `chat_sessions.user_id` for fast user session retrieval
- Composite index on `chat_sessions.user_id` and `chat_sessions.updated_at` for user session pagination
- Index on `chat_messages.session_id` for efficient message loading
- Index on `chat_messages.timestamp` for chronological ordering
- Composite index on `chat_messages.session_id` and `chat_messages.timestamp` for ordered message retrieval
- Index on `task_operation_logs.session_id` for operation history retrieval
- Index on `task_operation_logs.operation_type` for filtering by operation type
- Index on `task_operation_logs.timestamp` for chronological ordering

## Data Integrity Constraints

### User Isolation
- Users can only access their own chat sessions and messages
- Users can only access their own task operation logs
- All database queries must include user_id filter for proper isolation

### Referential Integrity
- All foreign key relationships must be maintained
- Cascade delete for chat sessions removes related messages and operation logs