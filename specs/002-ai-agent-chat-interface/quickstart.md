# Quickstart: AI Agent Chat Interface for AIDO TODO Application

## Development Setup

### Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL-compatible database (Neon recommended)
- OpenAI API key
- OpenRouter API key

### Environment Configuration
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost:5432/aido_todo
JWT_SECRET_KEY=your-super-secret-jwt-key
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=...
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET_KEY=your-jwt-key
```

## Running the Application

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### MCP Server
```bash
cd backend/src/mcp_server
python server.py
```

## Key Integration Points

### 1. Chat Widget Integration
The floating chat widget is integrated into the main layout and can be accessed from any page. It communicates with the backend via the `/api/chat/*` endpoints.

### 2. AI Agent Task Operations
The AI agent connects to the existing task management system through the MCP server, which translates AI requests into appropriate backend API calls.

### 3. Authentication Flow
- Users authenticate through existing JWT-based system
- Chat sessions and task operations respect user isolation
- All AI agent operations are authenticated and authorized

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## API Endpoints

### Chat Interface
- `GET /api/chat/sessions` - Get user's chat sessions
- `GET /api/chat/sessions/{id}/messages` - Get messages for session
- `POST /api/chat/messages` - Send message to AI agent

### Task Operations (via AI Agent)
- MCP tools: `create_tasks`, `read_tasks`, `update_tasks`, `delete_tasks`, `update_tasks_status`

## Troubleshooting

### Common Issues
1. **Chat widget not appearing**: Check that the ChatWidget component is properly imported in the main layout
2. **AI agent not responding**: Verify MCP server is running and API keys are configured
3. **Authentication errors**: Ensure JWT tokens are being properly passed to all API calls

### Debugging AI Operations
- Check the task_operation_logs table for operation history
- Monitor the MCP server logs for communication issues
- Verify that all task operations respect user isolation

## Deployment

### Frontend
Deploy to GitHub Pages with proper environment configuration for production API endpoints.

### Backend
Deploy to Hugging Face Spaces with MCP server integration.

### Database
Use Neon Serverless PostgreSQL for scalable database hosting with proper security configurations.