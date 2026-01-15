#!/bin/bash
# Simple script to test the backend API is running

echo "Testing backend API connection..."

# Check if backend is running on localhost:8000
if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✓ Backend API is accessible at http://localhost:8000"
else
    echo "✗ Backend API is not accessible at http://localhost:8000"
    echo "Please start the backend server with:"
    echo "cd /mnt/d/Hackathon-2-all-five-phases/backend"
    echo "uvicorn main:app --reload --port 8000"
fi

# Check if frontend dev server is running
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ Frontend is accessible at http://localhost:3000"
else
    echo "✗ Frontend is not accessible at http://localhost:3000"
    echo "To start the frontend development server:"
    echo "cd /mnt/d/Hackathon-2-all-five-phases/frontend"
    echo "npm run dev"
fi