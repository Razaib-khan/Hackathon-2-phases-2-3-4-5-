# Detailed Deployment Reference

## Dockerfile Best Practices

Discuss:
- Base image choice
- System dependencies
- Correct Uvicorn CMD binding
- Common failure modes

## Environment Variables

Explain:
- Required secrets
- SSL settings for Neon
- Using Hugging Face Secrets UI

## SQLAlchemy + Neon Config

- Connection string format
- Pool settings for serverless Postgres

## MCP SDK Integration

- Initialization after FastAPI startup
- Avoid blocking event loops
