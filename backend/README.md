# Backend Setup

This directory contains the FastAPI backend for the Speckit Plus Todo Application.

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