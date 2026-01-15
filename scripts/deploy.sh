#!/bin/bash

# Deployment script for AIDO TODO Application
# This script helps automate the deployment process for both frontend and backend

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment of AIDO TODO Application..."

# Function to deploy frontend to GitHub Pages
deploy_frontend() {
    echo "Deploying frontend to GitHub Pages..."
    cd frontend

    # Install dependencies
    echo "Installing frontend dependencies..."
    npm ci

    # Build the application
    echo "Building frontend application..."
    npm run build

    # Verify build succeeded
    if [ -d "out" ]; then
        echo "✓ Frontend build successful"
        echo "The build output is in the 'out' directory"
        echo "GitHub Actions will handle the actual deployment to GitHub Pages"
    else
        echo "✗ Frontend build failed"
        exit 1
    fi

    cd ..
}

# Function to prepare backend for Hugging Face
deploy_backend() {
    echo "Preparing backend for Hugging Face deployment..."
    cd backend

    # Verify Dockerfile exists
    if [ -f "Dockerfile" ]; then
        echo "✓ Dockerfile found"
    else
        echo "✗ Dockerfile not found"
        exit 1
    fi

    # Build Docker image (optional, for local testing)
    echo "Building Docker image for backend (optional)..."
    docker build . -t aido-todo-backend:latest || echo "Docker build failed - make sure Docker is running"

    echo "✓ Backend prepared for Hugging Face deployment"
    echo "Upload the backend code to your Hugging Face Space"
    echo "Configure the secrets in your Hugging Face Space settings"

    cd ..
}

# Function to run health checks
health_check() {
    echo "Running health checks..."

    # Check if frontend build directory exists
    if [ -d "frontend/out" ]; then
        echo "✓ Frontend build directory exists"
    else
        echo "⚠ Frontend build directory does not exist"
    fi

    # Check if backend Dockerfile exists
    if [ -f "backend/Dockerfile" ]; then
        echo "✓ Backend Dockerfile exists"
    else
        echo "✗ Backend Dockerfile does not exist"
        exit 1
    fi

    # Check if Hugging Face config exists
    if [ -f ".hf_space/config.yml" ]; then
        echo "✓ Hugging Face configuration exists"
    else
        echo "⚠ Hugging Face configuration does not exist"
    fi

    echo "✓ Health checks completed"
}

# Main execution
case "$1" in
    "frontend")
        deploy_frontend
        ;;
    "backend")
        deploy_backend
        ;;
    "health")
        health_check
        ;;
    "all")
        echo "Deploying both frontend and backend..."
        deploy_frontend
        deploy_backend
        health_check
        echo "✓ Deployment preparation completed for both frontend and backend"
        echo ""
        echo "Next steps:"
        echo "1. Push changes to GitHub for GitHub Actions to deploy frontend to GitHub Pages"
        echo "2. Upload backend code to your Hugging Face Space"
        echo "3. Configure secrets in GitHub repository and Hugging Face Space"
        ;;
    *)
        echo "Usage: $0 {frontend|backend|health|all}"
        echo "  frontend - Deploy frontend to GitHub Pages"
        echo "  backend  - Prepare backend for Hugging Face deployment"
        echo "  health   - Run health checks"
        echo "  all      - Deploy both frontend and backend"
        exit 1
        ;;
esac

echo "Deployment script completed successfully!"