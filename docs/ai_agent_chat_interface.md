# AI Agent Chat Interface for AIDO Todo Application

## Overview
The AI Agent Chat Interface provides users with an intelligent assistant that can help manage their tasks through natural language interactions. The system integrates with OpenAI's platform through OpenRouter and connects to the backend via the Multi-Agent Communication Protocol (MCP).

## Architecture

### Backend Components
- **MCP Server**: Handles communication between the AI agent and the application's task management system
- **AI Agent**: Connects to OpenRouter and processes natural language requests
- **Task Service**: Enhanced with batch operations for AI agent efficiency
- **Chat Service**: Manages chat sessions and messages
- **Models**: Extended with chat-related entities (ChatSession, ChatMessage, TaskOperationLog)

### Frontend Components
- **ChatWidget**: Floating chat icon that appears at the bottom-right of the screen
- **ChatInterface**: Main chat interface with message history and input area
- **ChatContext**: React context for managing chat state
- **ToastNotifications**: Error and success message handling

## Features

### Task Operations
The AI agent can perform all standard task operations:
- Create new tasks with titles, descriptions, and priorities
- Read existing tasks with filtering capabilities
- Update task details (title, description, priority, status)
- Delete tasks
- Mark tasks as complete/incomplete

### Chat Functionality
- Persistent chat sessions with history
- User isolation (users only see their own conversations)
- Real-time message display
- Session management

## Security Considerations

### Authentication & Authorization
- All API endpoints require valid JWT authentication
- Users can only access their own data
- Role-based access controls prevent unauthorized operations

### Input Validation
- All user inputs are validated before processing
- SQL injection prevention through parameterized queries
- XSS prevention through proper output encoding

### Rate Limiting
- API rate limiting to prevent abuse
- MCP server connection limits

### Data Protection
- End-to-end encryption for sensitive data
- Secure storage of API keys and credentials
- Audit logging for all operations

## Installation & Setup

### Environment Variables
```bash
OPENROUTER_API_KEY=your_openrouter_api_key
AIDO_MCP_URL=stdio://  # Or your MCP server URL
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret
```

### Running the Application
1. Start the MCP server: `python -m src.mcp_server.server`
2. Start the backend: `uvicorn src.main:app --reload`
3. Start the frontend: `npm run dev`

## API Endpoints

### Chat Endpoints
- `GET /api/chat/sessions` - Retrieve user's chat sessions
- `POST /api/chat/sessions` - Create a new chat session
- `GET /api/chat/sessions/{session_id}/messages` - Get messages for a session
- `POST /api/chat/messages` - Send a message to the AI agent

### Task Endpoints (enhanced for AI operations)
- `POST /api/tasks/batch` - Create multiple tasks at once
- `GET /api/tasks/batch` - Retrieve multiple tasks by IDs
- `PUT /api/tasks/batch` - Update multiple tasks at once

## MCP Tools

The system implements the following MCP tools for AI agent operations:
- `create-tasks`: Create one or more tasks
- `read-tasks`: Read tasks with optional filtering
- `update-tasks`: Update one or more tasks
- `delete-tasks`: Delete one or more tasks
- `update-tasks-status`: Update status of one or more tasks

## Error Handling

The system implements comprehensive error handling:
- Centralized error utilities with standardized error responses
- Frontend toast notifications for user feedback
- Detailed logging for debugging
- Graceful degradation when services are unavailable

## Testing

Unit tests cover:
- Utility functions and error handling
- Task service operations
- MCP tool functionality
- Integration between components

Run tests with: `pytest`

## Future Enhancements

- Voice input capabilities
- Advanced natural language processing
- Task categorization and tagging
- Team collaboration features
- Offline functionality

## Troubleshooting

### Common Issues
1. **MCP Server Not Connecting**: Ensure the MCP server is running before starting the AI agent
2. **Authentication Failures**: Verify JWT tokens are properly configured
3. **API Limits**: Check OpenRouter quota and rate limits

### Support
For issues with the AI agent functionality, contact the development team or consult the logs in the backend service.