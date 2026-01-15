# Repository Setup and Deployment Instructions

This document provides step-by-step instructions to set up the GitHub repository and deploy to both GitHub Pages and Hugging Face Spaces.

## Prerequisites

1. GitHub Personal Access Token with repository creation permissions
2. Hugging Face account and access token
3. GitHub CLI installed (`gh` command)
4. Git installed

## Step 1: GitHub Repository Setup

1. **Navigate to the project directory:**
   ```bash
   cd /mnt/d/Hackathon-2-all-five-phases
   ```

2. **Set your GitHub token as an environment variable:**
   ```bash
   export GITHUB_TOKEN=<your_github_personal_access_token>
   ```

3. **Run the setup script:**
   ```bash
   ./scripts/setup-deployment.sh
   ```

   When prompted, enter the name for your new GitHub repository.

## Step 2: Enable GitHub Pages

1. After the repository is created, go to your GitHub repository settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "Deploy from a branch"
4. Select "main" branch and "/root" folder
5. Click "Save"
6. GitHub Pages will automatically deploy the frontend from the `frontend/out` directory

## Step 3: Hugging Face Space Deployment

1. **Prepare the backend for deployment:**
   ```bash
   cd /mnt/d/Hackathon-2-all-five-phases
   ./scripts/hf-deployment.sh
   ```

2. **Using the Hugging Face MCP server, create a new Space:**
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose these settings:
     - SDK: Docker
     - Hardware: CPU (or appropriate option)
     - Visibility: Public or Private (as needed)

3. **Clone your new Space:**
   ```bash
   git clone https://huggingface.co/spaces/<your-username>/<your-space-name>
   cd <your-space-name>
   ```

4. **Copy the backend files:**
   ```bash
   # Copy all the prepared backend files from the temp directory mentioned in the hf-deployment.sh output
   cp -r /path/to/temp/dir/* .
   ```

5. **Commit and push to deploy:**
   ```bash
   git add .
   git commit -m "Deploy AIDO TODO backend"
   git push
   ```

6. **Configure Space secrets in the Hugging Face UI:**
   - Go to your Space settings
   - Navigate to "Secrets"
   - Add the following secrets:
     - `DATABASE_URL`: Your database connection string
     - `JWT_SECRET_KEY`: Secret key for JWT token generation
     - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Step 4: Configure Frontend to Backend Connection

1. **In your GitHub repository, go to Settings > Secrets and variables > Actions**
2. **Add a new secret:**
   - Name: `API_BASE_URL`
   - Value: The URL of your deployed Hugging Face Space (e.g., `https://your-username-huggingface-space.hf.space`)

## Step 5: Verification

1. **GitHub Pages URL:** `https://<your-username>.github.io/<repository-name>`
2. **Hugging Face Space URL:** `https://<your-username>-<space-name>.hf.space`

Both applications should now be deployed and communicating with each other.

## Troubleshooting

### GitHub Pages Issues:
- Ensure the frontend build generates files in the `out` directory
- Check that the `API_BASE_URL` secret is correctly set
- Verify CORS settings in the backend

### Hugging Face Space Issues:
- Make sure the Dockerfile is in the root of the Space repository
- Verify all required secrets are configured
- Check the Space logs for any build or runtime errors

### Connection Issues:
- Confirm the backend API is accessible from the frontend
- Check that the API endpoints are correctly configured
- Verify authentication tokens are properly handled