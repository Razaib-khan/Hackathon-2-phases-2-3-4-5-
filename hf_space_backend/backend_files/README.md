# AIDO TODO Application Backend

This directory contains the FastAPI backend for the AIDO TODO Application.

## Dependencies

All Python dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

## Code Formatting and Linting

This project uses several tools to maintain code quality:

- **Black**: For automatic code formatting
- **isort**: For sorting imports
- **Flake8**: For linting
- **pytest**: For testing
- **mypy**: For type checking

### Using the tools

You can use the provided Makefile to run these tools:

```bash
# Format code with black and isort
make format

# Lint code with flake8
make lint

# Run tests
make test

# Run all checks (format, lint, test)
make check

# Run the application
make run
```

Alternatively, you can run the tools directly:

```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/

# Run type checking
mypy src/

# Run tests
pytest tests/ -v
```

## Deploying to Hugging Face Spaces

This backend can be deployed to Hugging Face Spaces. Here's how to configure it:

### Required Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
DATABASE_URL=your_postgresql_connection_string
JWT_SECRET_KEY=your_secure_jwt_secret
ALLOWED_ORIGINS=comma_separated_list_of_allowed_origins
```

### Secrets to Set in Hugging Face Space

In your Hugging Face Space repository settings, set these secrets:

1. `DATABASE_URL` - PostgreSQL database connection string
2. `JWT_SECRET_KEY` - Secure JWT secret key
3. `ALLOWED_ORIGINS` - Origins allowed to access the API (e.g., your GitHub Pages URL)

### Docker Configuration

The included Dockerfile is configured to run the FastAPI application on port 8000, which is what Hugging Face Spaces expects.

### Deployment Steps

1. Create a Hugging Face Space with Docker SDK
2. Add your secrets to the Space settings
3. Push this code to the Space repository
4. The application will automatically build and deploy

The API will be available at: `https://YOUR_HF_USERNAME-hf-space-YOUR_SPACE_NAME.hf.space`

## Project Structure

- `src/` - Main source code
  - `api/` - API route definitions
  - `database/` - Database configuration and models
  - `models/` - SQLModel data models
  - `services/` - Business logic
  - `main.py` - Application entry point
- `tests/` - Test files
- `alembic/` - Database migration files
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project configuration
- `Makefile` - Common development commands