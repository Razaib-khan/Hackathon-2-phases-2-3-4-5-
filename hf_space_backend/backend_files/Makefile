.PHONY: install format lint test run

# Install dependencies
install:
	pip install -r requirements.txt

# Format code with black and isort
format:
	black src/
	isort src/

# Lint code with flake8
lint:
	flake8 src/

# Run tests
test:
	pytest tests/ -v

# Run the application
run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Format, lint, and test
check: format lint test