---
name: yaml-workflow-manager
version: 1.0.0
type: skill
author: Claude
license: MIT
tags: [yaml, workflow, deployment, github-pages, hugging-face, ci-cd]
category: deployment
dependencies: []
---

# YAML Workflow Manager Skill

This skill manages YAML workflow configurations for deploying applications to GitHub Pages (frontend) and Hugging Face Spaces (backend). It provides capabilities to generate, validate, and manage CI/CD pipeline configurations for multi-platform deployments.

## Core Responsibilities

### 1. YAML Workflow Generation
Generate proper YAML configurations for deployment workflows:

```yaml
# Example GitHub Actions workflow for GitHub Pages deployment
name: Deploy Frontend to GitHub Pages

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Build frontend
      run: npm run build
      env:
        NEXT_PUBLIC_API_BASE_URL: ${{ secrets.API_BASE_URL }}

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./out
        cname: yourdomain.com  # Optional: for custom domain
```

### 2. Hugging Face Space Configuration
Manage Docker and Space configuration files for backend deployment:

```yaml
# .hf_space/config.yml
runtime:
  hardware: cpu-basic
  requirements:
    - python>=3.9
    - pip

  secrets:
    - DATABASE_URL
    - JWT_SECRET_KEY
    - BETTER_AUTH_SECRET
```

### 3. Workflow Validation
Validate YAML syntax and structure for deployment workflows:

```bash
# Validate GitHub Actions workflow
.github/workflows/deploy.yml

# Validate Hugging Face Space configuration
.hf_space/config.yml
Dockerfile
requirements.txt
```

### 4. Multi-Platform Coordination
Ensure coordinated deployments between frontend and backend platforms:

- GitHub Pages for frontend hosting
- Hugging Face Spaces for backend API
- Proper API endpoint configuration
- Cross-platform environment variable management

## Deployment Patterns

### 1. Frontend Deployment (GitHub Pages)
```yaml
# GitHub Actions workflow for Next.js static export
name: Deploy Frontend
on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build for GitHub Pages
        run: |
          npm run build
          npm run export  # This creates static files in 'out' directory

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./out
```

### 2. Backend Deployment (Hugging Face Spaces)
```dockerfile
# Dockerfile for Hugging Face Space
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Environment Configuration
Proper environment variable coordination between platforms:

```bash
# GitHub Actions secrets (for frontend build)
API_BASE_URL=https://username-reponame.hf.space  # Backend URL for frontend
NEXT_PUBLIC_API_BASE_URL=${{ secrets.API_BASE_URL }}

# Hugging Face Space secrets (for backend)
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret
BETTER_AUTH_SECRET=your_auth_secret
```

## Security Considerations

### 1. Secret Management
- Never hardcode secrets in workflow files
- Use GitHub Actions secrets and Hugging Face Space secrets
- Validate that sensitive information is properly masked

### 2. Access Control
- Limit workflow permissions to minimum required
- Use specific GitHub tokens with limited scope
- Validate repository access rights

### 3. Dependency Security
- Pin workflow action versions
- Validate Docker base images
- Scan for vulnerable dependencies

## Troubleshooting

### Common Issues

1. **Frontend Cannot Reach Backend**
   - Verify API_BASE_URL is correctly configured
   - Check CORS settings in backend
   - Confirm backend is publicly accessible

2. **Workflow Permissions Error**
   - Ensure GITHUB_TOKEN has proper permissions
   - Check repository settings for Actions access

3. **Docker Build Failures**
   - Verify Dockerfile syntax
   - Check that all required files are copied
   - Validate port exposure and CMD instruction

## Integration Patterns

### 1. API Endpoint Coordination
Ensure frontend knows where to find the backend API:

```typescript
// Frontend API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ||
                   'https://username-reponame.hf.space';  // Default to HF Space
```

### 2. Deployment Synchronization
Coordinate deployment timing between platforms:
- Deploy backend first to ensure API availability
- Update frontend with new backend endpoint if needed
- Monitor deployment status across platforms

## Verification

Run: `python3 scripts/verify-yaml-workflows.py`

Expected: `✓ yaml-workflow-manager skill ready`

## If Verification Fails

1. Check: YAML syntax validity using yamllint
2. **Stop and report** if validation errors persist

## Related Skills

- **building-nextjs-apps** - Frontend application structure and deployment
- **scaffolding-fastapi-dapr** - Backend service patterns
- **containerizing-applications** - Docker configuration for deployments
- **deploying-cloud-k8s** - Alternative deployment strategies

## References

- [references/github-actions-workflows.md](references/github-actions-workflows.md) - GitHub Actions best practices and patterns
- [references/hugging-face-spaces.md](references/hugging-face-spaces.md) - Hugging Face Spaces deployment configurations
- [references/ci-cd-best-practices.md](references/ci-cd-best-practices.md) - Continuous integration and deployment best practices