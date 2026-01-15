# AIDO TODO Application Deployment Guide

This document outlines the deployment process for the AIDO TODO application, which consists of a frontend (deployed to GitHub Pages) and a backend (deployed to Hugging Face Spaces).

## Architecture Overview

- **Frontend**: Next.js application deployed to GitHub Pages
- **Backend**: FastAPI application deployed to Hugging Face Spaces
- **Database**: Neon PostgreSQL database (externally hosted)

## Prerequisites

### GitHub Pages Deployment
- GitHub repository with Pages enabled
- Repository secrets configured (see below)

### Hugging Face Spaces Deployment
- Hugging Face account
- Space created for the backend application
- API token for Hugging Face

## Deployment Configuration

### GitHub Repository Secrets (for frontend deployment)

Add these secrets to your GitHub repository:

- `API_BASE_URL`: The URL of your deployed backend (e.g., `https://your-space-name.hf.space`)

### Hugging Face Space Secrets

Configure these secrets in your Hugging Face Space:

- `DATABASE_URL`: PostgreSQL database connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `HF_TOKEN`: Hugging Face API token (if needed for API calls)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

## Deployment Process

### 1. Deploy Backend to Hugging Face

1. Create a new Space on Hugging Face
2. Connect your repository or upload the backend code
3. Configure the secrets in your Space settings
4. The Space will automatically build and deploy based on the `Dockerfile` and `config.yml`

### 2. Deploy Frontend to GitHub Pages

1. Enable GitHub Pages in your repository settings (under Settings > Pages)
2. Ensure the deployment workflow has the correct `API_BASE_URL` secret
3. The workflow will automatically deploy when changes are pushed to the `main` branch

## Local Development

To run the application locally:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Start both frontend and backend with Docker Compose
docker-compose up --build
```

The application will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Docker Configuration

### Backend Docker Configuration
The backend Dockerfile creates a lightweight Python environment and runs the FastAPI application.

### Frontend Docker Configuration
The frontend Dockerfile builds the Next.js application and serves it using the `serve` package.

### Docker Compose
The `docker-compose.yml` file orchestrates both services along with a PostgreSQL database for local development.

## Environment Variables

### Backend Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret for JWT generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Frontend Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for backend API calls

## Troubleshooting

### Frontend Deployment Issues
- Ensure the `API_BASE_URL` secret is correctly set in GitHub repository
- Verify that the backend is accessible from the frontend
- Check CORS configuration in the backend

### Backend Deployment Issues
- Verify that database connection string is correct
- Ensure all required secrets are configured in Hugging Face Space
- Check that the application starts correctly in the Space environment

### Common Issues
- Cross-Origin Resource Sharing (CORS) issues between frontend and backend
- Incorrect API URL configuration
- Database connection problems
- Missing environment variables or secrets

## Security Considerations

- Never hardcode secrets in configuration files
- Use environment variables and secrets management
- Ensure HTTPS is used for all API communications
- Regularly rotate secrets and API tokens
- Validate and sanitize all user inputs

## Scaling Considerations

### Frontend Scaling
- GitHub Pages automatically handles scaling for static content
- CDN is provided by GitHub

### Backend Scaling
- Hugging Face Spaces provide automatic scaling based on usage
- Monitor resource usage and upgrade hardware if needed
- Consider implementing caching for frequently accessed data

## Maintenance

Regular maintenance tasks include:
- Updating dependencies in both frontend and backend
- Rotating secrets and API tokens
- Monitoring application performance and errors
- Database maintenance and optimization
- Security updates