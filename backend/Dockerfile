# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy project requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for the AI agent and MCP
RUN pip install --no-cache-dir openai mcp-sdk python-multipart

# Copy the application files
COPY . .

# Expose port
EXPOSE 8000

# Run the application directly from the main module which handles PORT env var
CMD ["sh", "-c", "python -m src.mcp_server.server & python -c 'import uvicorn; import os; from src.main import app; port = int(os.environ.get(\"PORT\", 8000)); uvicorn.run(app, host=\"0.0.0.0\", port=port)'"]
