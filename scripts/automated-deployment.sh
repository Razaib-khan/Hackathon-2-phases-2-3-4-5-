#!/bin/bash

# Automated Deployment Script for AIDO TODO Application
# This script automates the deployment process to GitHub Pages and Hugging Face Spaces

set -e  # Exit immediately if a command exits with a non-zero status

echo "==========================================="
echo "AIDO TODO Application - Automated Deployment"
echo "==========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "Error: Not in the project root directory"
    exit 1
fi

echo "Step 1: Repository Preparation"
echo "==============================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git config user.name "${GITHUB_ACTOR:-$(git config --global user.name 2>/dev/null || echo 'Claude')}"
    git config user.email "${GITHUB_EMAIL:-$(git config --global user.email 2>/dev/null || echo 'claude@example.com')}"
    git commit -m "Initial commit for AIDO TODO application"
fi

echo "✓ Repository prepared"

echo ""
echo "Step 2: GitHub Repository Creation"
echo "=================================="

# Generate a unique repository name based on timestamp
TIMESTAMP=$(date +%s)
REPO_NAME="aido-todo-app-$TIMESTAMP"

echo "Creating GitHub repository: $REPO_NAME"
REPO_URL=$(gh repo create "$REPO_NAME" --public --clone 2>&1 || echo "FAILED")

if [[ "$REPO_URL" == *"FAILED"* ]]; then
    echo "✗ Failed to create repository"
    echo "Please check your GitHub CLI authentication and permissions"
    echo "Attempting to create repository without clone and then clone separately..."

    # Try creating repo without cloning
    gh repo create "$REPO_NAME" --public --remote=origin
    git remote add origin "https://github.com/$(gh api user --jq '.login')/$REPO_NAME.git"

    # Pull from remote to establish tracking
    git pull origin main --allow-unrelated-histories || echo "No main branch exists yet"
fi

# Set up the repository with our files
cd "$REPO_NAME" || cd ..

# If we're still in the original directory, copy files to the new repo
if [ -f "../CLAUDE.md" ]; then
    cd ..
    # Copy all files to the repository directory
    rsync -av --exclude='.git' --exclude="$REPO_NAME" . "$REPO_NAME/"
    cd "$REPO_NAME"

    # Add and commit all files
    git add .
    git status
    git commit -m "Initial commit for AIDO TODO application - Phase 2 deployment" || echo "No changes to commit"
fi

echo "✓ Repository created and files copied"

echo ""
echo "Step 3: Create and Deploy Phase-2 Branch"
echo "========================================"

# Create phase-2 branch
git checkout -b phase-2
git add .
git commit -m "Setup phase-2 branch with deployment configurations" || echo "No changes to commit"

# Push phase-2 branch
git push -u origin phase-2
echo "✓ Phase-2 branch created and pushed"

echo ""
echo "Step 4: Merge Phase-2 to Main"
echo "============================="

# Switch back to main and merge
git checkout main || git checkout -b main
git merge phase-2 -m "Merge phase-2 branch to main" || echo "Nothing to merge"
git push origin main
echo "✓ Phase-2 merged to main and pushed"

echo ""
echo "Step 5: GitHub Pages Configuration"
echo "=================================="

echo "GitHub Pages needs to be enabled manually:"
echo "1. Go to https://github.com/$(gh api user --jq '.login')/$REPO_NAME/settings"
echo "2. Scroll down to 'Pages' section"
echo "3. Under 'Source', select 'Deploy from a branch'"
echo "4. Select 'main' branch and '/root' folder"
echo "5. Click 'Save'"
echo ""

echo "Step 6: Hugging Face Space Preparation"
echo "====================================="

# Create temp directory for backend deployment
TEMP_DIR=$(mktemp -d -t hf-space-XXXXXX)
echo "Created temporary directory for backend: $TEMP_DIR"

# Copy backend files
mkdir -p "$TEMP_DIR/backend"
cp -r ../backend/* "$TEMP_DIR/backend/" 2>/dev/null || echo "Backend directory may not exist yet"

# Copy Dockerfile
if [ -f "../backend/Dockerfile" ]; then
    cp ../backend/Dockerfile "$TEMP_DIR/"
elif [ -f "backend/Dockerfile" ]; then
    cp backend/Dockerfile "$TEMP_DIR/"
else
    # Create a basic Dockerfile if none exists
    cat > "$TEMP_DIR/Dockerfile" << EOF
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
fi

# Copy Hugging Face Space configuration
if [ -d "../.hf_space" ]; then
    mkdir -p "$TEMP_DIR/.hf_space"
    cp -r ../.hf_space/* "$TEMP_DIR/.hf_space/" 2>/dev/null || echo "No .hf_space config found"
elif [ -d ".hf_space" ]; then
    mkdir -p "$TEMP_DIR/.hf_space"
    cp -r .hf_space/* "$TEMP_DIR/.hf_space/" 2>/dev/null || echo "No .hf_space config found"
else
    # Create a basic config if it doesn't exist
    mkdir -p "$TEMP_DIR/.hf_space"
    cat > "$TEMP_DIR/.hf_space/config.yml" << EOF
# Hugging Face Space Configuration for AIDO TODO Backend
runtime:
  hardware: cpu-basic
  requirements:
    - python>=3.9
    - pip
EOF
fi

echo "Backend files prepared in: $TEMP_DIR"

echo ""
echo "Step 7: Hugging Face Space Creation"
echo "=================================="

echo "The Hugging Face Space needs to be created manually:"
echo ""
echo "1. Go to https://huggingface.co/spaces"
echo "2. Click 'Create new Space'"
echo "3. Configure as follows:"
echo "   - Name: $REPO_NAME-backend (or your preferred name)"
echo "   - SDK: Docker"
echo "   - Hardware: cpu-basic (or appropriate option)"
echo "   - Visibility: Public"
echo ""
echo "4. After creating the Space, clone it:"
echo "   git clone https://huggingface.co/spaces/your-username/$REPO_NAME-backend"
echo "   cd $REPO_NAME-backend"
echo ""
echo "5. Copy the prepared backend files:"
echo "   cp -r $TEMP_DIR/* ."
echo ""
echo "6. Commit and push:"
echo "   git add ."
echo "   git commit -m 'Deploy AIDO TODO backend'"
echo "   git push"
echo ""
echo "7. Configure Space secrets in the Hugging Face UI:"
echo "   - DATABASE_URL: Your database connection string"
echo "   - JWT_SECRET_KEY: Secret key for JWT generation"
echo "   - ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time (default: 30)"
echo ""

echo "Step 8: GitHub Actions Configuration"
echo "==================================="

echo "Configure GitHub Actions secrets in your repository:"
echo "1. Go to Settings > Secrets and variables > Actions"
echo "2. Add the following secrets:"
echo "   - API_BASE_URL: Your Hugging Face Space URL (e.g., https://username-$REPO_NAME-backend.hf.space)"

echo ""
echo "==========================================="
echo "AUTOMATED DEPLOYMENT PROCESS COMPLETED"
echo "==========================================="
echo ""
echo "Repository: $REPO_NAME"
echo "Repository URL: https://github.com/$(gh api user --jq '.login')/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Complete the GitHub Pages setup (Step 5 above)"
echo "2. Complete the Hugging Face Space setup (Step 7 above)"
echo "3. Configure GitHub Actions secrets (Step 8 above)"
echo "4. The frontend will be available at: https://$(gh api user --jq '.login').github.io/$REPO_NAME"
echo "5. The backend will be available at: https://your-username-$REPO_NAME-backend.hf.space"
echo ""
echo "Temporary files are in: $TEMP_DIR"
echo "Remember to clean up the temporary directory when deployment is verified."