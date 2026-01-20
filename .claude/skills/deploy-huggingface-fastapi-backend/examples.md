# Examples

## Dockerfile (Core Section)
Refer to [scripts/dockerfile-template.txt] for full content.

## Sample Commands

Build locally:
docker build -t fastapi-hf .
docker run -p 7860:7860 fastapi-hf

shell
Copy code

## Environment Setup
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DB?sslmode=require
MCP_SDK_KEY=xxx