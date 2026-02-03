# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
RUN pip install uv
COPY requirements.txt .
RUN UV_HTTP_TIMEOUT=120 uv pip install --system --no-cache -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -u 1000 appuser && chown -R appuser /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1:8000/health || exit 1
CMD ["sh", "-c", "python -m src.mcp_server.server & python -c 'import uvicorn; import os; from src.main import app; port = int(os.environ.get(\"PORT\", 8000)); uvicorn.run(app, host=\"0.0.0.0\", port=port)'"]
