---
name: deploy-huggingface-fastapi-backend
description: Guide deployment of a FastAPI backend with Neon PostgreSQL, SQL models, Uvicorn, and MCP SDK to Hugging Face Spaces using Docker. Use when the user asks about deployment configuration, building, environment variables, database connections, or troubleshooting deployment errors.
---

# Deploy FastAPI Backend to Hugging Face Spaces

This Skill teaches how to configure, package, and deploy a FastAPI backend using:

- FastAPI framework
- SQLAlchemy models connected to a Neon PostgreSQL database
- Uvicorn as the ASGI server
- MCP SDK Python
- Docker for deployment on Hugging Face Spaces

## Instructions

1. **Set up the repository.**
   Ensure the root contains:
   - `Dockerfile`
   - `requirements.txt`
   - FastAPI code (application folder)
   - database and MCP initialization files

2. **Define environment variables.**
   Store secrets (e.g., `DATABASE_URL`, `MCP_SDK_KEY`) in Hugging Face Spaces Secrets.

3. **Use the Dockerfile template.**
   See [dockerfile-template.txt](scripts/dockerfile-template.txt) for a working example.

4. **Configure SQLAlchemy for Neon.**
   Use SSL and correct connection pooling patterns.

5. **Expose Uvicorn on port 7860.**
   Required by Hugging Face Spaces for deployment.

6. **Test locally in Docker.**
   Validate build and exposed endpoints.

7. **Push and deploy the Space.**
   Hugging Face will auto-build and serve the FastAPI app.

## Detailed Reference

For deeper configuration details and pitfalls, see [reference.md](reference.md).

## Examples

Sample Dockerfile, environment settings, and command usage are provided in [examples.md](examples.md).
