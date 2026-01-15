#!/bin/bash

# Script to create and deploy to Hugging Face Space using MCP server

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting up Hugging Face Space deployment..."

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "Error: Not in the project root directory"
    exit 1
fi

# Create a temporary directory for the backend deployment
TEMP_DIR=$(mktemp -d)
echo "Creating temporary directory: $TEMP_DIR"

# Copy only the backend files to the temporary directory
mkdir -p "$TEMP_DIR"/backend
cp -r backend/* "$TEMP_DIR"/backend/

# Add the Hugging Face Space configuration
mkdir -p "$TEMP_DIR"/.hf_space
cp -r .hf_space/* "$TEMP_DIR"/.hf_space/ 2>/dev/null || echo "No .hf_space directory found, creating basic config..."

# Create a basic config if it doesn't exist
if [ ! -f "$TEMP_DIR/.hf_space/config.yml" ]; then
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

# Copy the Dockerfile to the temp directory root (Hugging Face expects it in the root of the space)
cp backend/Dockerfile "$TEMP_DIR/"

# Display instructions for creating the space using MCP server
echo "=== HUGGING FACE SPACE CREATION INSTRUCTIONS ==="
echo "The backend code is prepared in: $TEMP_DIR"
echo ""
echo "To create and deploy to Hugging Face Space using the MCP server:"
echo ""
echo "1. Using the Hugging Face MCP server, create a new space with these parameters:"
echo "   - Space name: Choose a unique name for your space"
echo "   - SDK: Docker (since we have a Dockerfile)"
echo "   - Hardware: cpu-basic (adjust as needed)"
echo ""
echo "2. After creating the space, you can clone it and push the backend code:"
echo "   cd $TEMP_DIR"
echo "   git clone https://huggingface.co/spaces/[YOUR_USERNAME]/[YOUR_SPACE_NAME] ."
echo "   # The code is already prepared in the temp directory"
echo "   git add ."
echo "   git commit -m 'Deploy AIDO TODO backend'"
echo "   git push"
echo ""
echo "3. Configure the secrets in your Space settings via the Hugging Face UI:"
echo "   - DATABASE_URL: Your database connection string"
echo "   - JWT_SECRET_KEY: Secret key for JWT token generation"
echo "   - ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time (default: 30)"
echo ""
echo "4. The Space will automatically build and deploy using the Dockerfile"
echo ""
echo "Temporary directory location: $TEMP_DIR"
echo "Note: You will need to manually clean up this directory when deployment is complete."