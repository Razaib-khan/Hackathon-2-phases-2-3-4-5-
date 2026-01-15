#!/bin/bash

# Script to set up GitHub repository, create phase-2 branch, push code, and prepare for deployment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting up GitHub repository and deployment process..."

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "Error: Not in the project root directory"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for phase-2"
fi

# Get GitHub token from environment or prompt user
if [ -z "$GITHUB_TOKEN" ]; then
    read -p "Enter your GitHub personal access token: " GITHUB_TOKEN
    export GITHUB_TOKEN
fi

# Create a new repository using GitHub CLI
read -p "Enter the name for your new GitHub repository: " REPO_NAME

echo "Creating new GitHub repository: $REPO_NAME"
gh repo create "$REPO_NAME" --public --clone

# Navigate to the cloned repository
cd "$REPO_NAME"

# Copy all files from the parent directory
cp -r ../../* ./ 2>/dev/null || echo "Copying files..."

# Add all files to git
git add .

# Commit the changes
git config user.name "$(git config --global user.name)"
git config user.email "$(git config --global user.email)"
git commit -m "Initial setup for phase-2 deployment"

# Create phase-2 branch
git checkout -b phase-2

# Add and commit any potential changes
git add .
git commit -m "Prepare phase-2 branch" || echo "No changes to commit"

# Push phase-2 branch to remote
git push -u origin phase-2

# Switch back to main and merge phase-2
git checkout main
git merge phase-2
git push origin main

echo "Repository setup complete!"
echo "Repository: $REPO_NAME"
echo "Phase-2 branch created and merged to main"
echo ""
echo "Next steps:"
echo "1. GitHub Pages will be automatically deployed once you enable it in repository settings"
echo "2. For Hugging Face deployment, follow the instructions below"

# Instructions for Hugging Face deployment
echo ""
echo "=== HUGGING FACE DEPLOYMENT INSTRUCTIONS ==="
echo "1. Go to https://huggingface.co/spaces"
echo "2. Create a new Space with the following settings:"
echo "   - SDK: Docker"
echo "   - Hardware: CPU (or GPU if needed)"
echo "3. Once created, you can push the backend code to your Space using git:"
echo "   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME"
echo "   cd YOUR_SPACE_NAME"
echo "   # Copy backend files to this directory"
echo "   cp -r /path/to/your/backend/* ."
echo "   git add ."
echo "   git commit -m 'Initial backend deployment'"
echo "   git push"
echo ""
echo "4. Make sure to configure the secrets in your Space settings:"
echo "   - DATABASE_URL"
echo "   - JWT_SECRET_KEY"
echo "   - ACCESS_TOKEN_EXPIRE_MINUTES"
echo ""
echo "5. The Space will automatically build and deploy using the Dockerfile"