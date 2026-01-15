#!/bin/bash

# Complete Deployment Script for AIDO TODO Application
# This script guides you through the complete deployment process to GitHub Pages and Hugging Face Spaces

set -e  # Exit immediately if a command exits with a non-zero status

echo "==========================================="
echo "AIDO TODO Application - Complete Deployment"
echo "==========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "Error: Not in the project root directory"
    exit 1
fi

echo "Step 1: Repository Preparation"
echo "==============================="

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git config user.name "${GITHUB_ACTOR:-$(git config --global user.name)}"
    git config user.email "${GITHUB_EMAIL:-$(git config --global user.email)}"
    git commit -m "Initial commit for AIDO TODO application"
fi

echo "✓ Repository prepared"

echo ""
echo "Step 2: GitHub Repository Creation"
echo "=================================="

echo "Before proceeding, please ensure you have:"
echo "- GitHub Personal Access Token with repo creation permissions"
echo "- GitHub CLI installed (gh command)"
echo ""

read -p "Do you have these prerequisites? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please set up the prerequisites before continuing."
    exit 1
fi

read -p "Enter your desired GitHub repository name: " REPO_NAME

echo "Creating GitHub repository: $REPO_NAME"
gh repo create "$REPO_NAME" --public --clone

if [ $? -eq 0 ]; then
    echo "✓ Repository created successfully"
else
    echo "✗ Failed to create repository"
    echo "Please check your GitHub CLI authentication and permissions"
    exit 1
fi

# Move to the new repository directory
cd "$REPO_NAME"

# Copy all project files to the new repository
echo "Copying project files..."
cp -r ../../* ./ 2>/dev/null || echo "Done copying files"

# Create a fresh git history for the new repo
git add .
git status
read -p "Press Enter to continue with the commit..."
git commit -m "Initial commit for AIDO TODO application - Phase 2 deployment"

echo "✓ Files copied and committed"

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
git checkout main
git merge phase-2 -m "Merge phase-2 branch to main"
git push origin main
echo "✓ Phase-2 merged to main and pushed"

echo ""
echo "Step 5: GitHub Pages Configuration"
echo "=================================="

echo "GitHub Pages needs to be enabled manually:"
echo "1. Go to https://github.com/your-username/$REPO_NAME/settings"
echo "2. Scroll down to 'Pages' section"
echo "3. Under 'Source', select 'Deploy from a branch'"
echo "4. Select 'main' branch and '/root' folder"
echo "5. Click 'Save'"
echo ""
echo "Also, configure the GitHub Actions secret:"
echo "1. Go to Settings > Secrets and variables > Actions"
echo "2. Click 'New repository secret'"
echo "3. Add the following secret:"
echo "   Name: API_BASE_URL"
echo "   Value: Your Hugging Face Space URL (will be created in next step)"
echo ""

echo "Step 6: Hugging Face Space Preparation"
echo "====================================="

# Create temp directory for backend deployment
TEMP_DIR=$(mktemp -d -t hf-space-XXXXXX)
echo "Created temporary directory for backend: $TEMP_DIR"

# Copy backend files
mkdir -p "$TEMP_DIR/backend"
cp -r ../backend/* "$TEMP_DIR/backend/"

# Copy Dockerfile
cp ../backend/Dockerfile "$TEMP_DIR/"

# Copy Hugging Face Space configuration
if [ -d "../.hf_space" ]; then
    mkdir -p "$TEMP_DIR/.hf_space"
    cp -r ../.hf_space/* "$TEMP_DIR/.hf_space/"
fi

echo "Backend files prepared in: $TEMP_DIR"

echo ""
echo "Step 7: Manual Hugging Face Space Creation"
echo "=========================================="

echo "You need to manually create and deploy the Hugging Face Space:"
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

echo "Step 8: Final Verification"
echo "=========================="

BACKEND_URL="https://$(echo $USER | tr '[:upper:]' '[:lower:]')-$REPO_NAME-backend.hf.space"
FRONTEND_URL="https://$(echo $USER | tr '[:upper:]' '[:lower:]').github.io/$REPO_NAME"

echo "Once both deployments are complete, verify:"
echo "Backend (API): $BACKEND_URL"
echo "Frontend (UI): $FRONTEND_URL"
echo ""
echo "The frontend should automatically connect to the backend using the API_BASE_URL configuration."

echo ""
echo "==========================================="
echo "DEPLOYMENT PROCESS COMPLETED"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Complete the GitHub Pages setup (Step 5 above)"
echo "2. Complete the Hugging Face Space setup (Step 7 above)"
echo "3. Update the API_BASE_URL secret in GitHub with your Space URL"
echo "4. Trigger a new GitHub Pages build by pushing an empty commit if needed:"
echo "   git commit --allow-empty -m 'Trigger GitHub Pages build'"
echo "   git push"
echo ""
echo "Temporary files are in: $TEMP_DIR"
echo "Remember to clean up the temporary directory when deployment is verified."