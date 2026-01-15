---
name: deployment-yaml-workflows
description: |
  YAML workflow configuration for deploying frontend to GitHub Pages and backend to Hugging Face Spaces.
  Generate, validate, and manage deployment configurations for multi-environment deployments.
  Use when tasks involve CI/CD pipeline setup, GitHub Actions workflows, or deployment automation.
---

# Deployment YAML Workflows

Configure and manage deployment workflows for frontend (GitHub Pages) and backend (Hugging Face Spaces) deployments.

## Core Responsibilities

- Generate GitHub Actions workflows for GitHub Pages frontend deployment
- Create Hugging Face Space configuration files
- Validate YAML syntax and deployment configurations
- Set up environment-specific variables and secrets
- Coordinate multi-stage deployments with proper dependencies

## GitHub Pages Deployment Workflow

### Workflow Structure
```yaml
name: Deploy Frontend to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_API_BASE_URL: ${{ secrets.API_BASE_URL }}

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./out

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Required Secrets
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL for frontend configuration

## Hugging Face Spaces Deployment

### Space Configuration
```yaml
# .hf_space/config.yml
runtime:
  hardware: cpu
  requirements:
    - python>=3.8
    - pip
  secrets:
    - name: DATABASE_URL
      description: Database connection string
    - name: JWT_SECRET_KEY
      description: JWT secret key
    - name: HF_TOKEN
      description: Hugging Face API token
```

### Space Environment Variables
```yaml
# .hf_space/app.env
DATABASE_URL=${secret:DATABASE_URL}
JWT_SECRET_KEY=${secret:JWT_SECRET_KEY}
HF_TOKEN=${secret:HF_TOKEN}
```

## Deployment Coordination

### Multi-Stage Deployment Sequence
1. **Backend Deployment**: Deploy backend to Hugging Face first
2. **Health Check**: Verify backend is operational
3. **Frontend Configuration**: Update frontend with backend URL
4. **Frontend Deployment**: Deploy frontend to GitHub Pages

### Health Check Workflow
```yaml
- name: Verify Backend Health
  run: |
    curl -f ${{ secrets.BACKEND_URL }}/health || exit 1
    sleep 10  # Allow backend to fully initialize
```

## YAML Validation

### Syntax Validation
- Validate YAML syntax using yamlfmt or similar tools
- Check for proper indentation and structure
- Verify GitHub Actions and Hugging Face configuration schemas

### Security Validation
- Ensure secrets are properly referenced, not hardcoded
- Validate permission scopes for GitHub Actions
- Check for exposed sensitive information

## Environment Configuration

### Production Environment
```yaml
# GitHub Pages environment
environment:
  name: github-pages
  url: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}

# Hugging Face environment
runtime:
  hardware: gpu-t4-medium  # Adjust based on requirements
  requirements:
    - python>=3.9
    - torch>=1.13.0
    - fastapi>=0.100.0
```

### Staging Environment
```yaml
# Separate staging workflow for testing
name: Deploy Staging

on:
  push:
    branches: [ develop ]

# Similar structure but with staging-specific configurations
```

## Best Practices

### GitHub Actions Optimization
- Use caching for dependencies (`actions/cache`)
- Limit workflow concurrency to prevent conflicts
- Use appropriate runner sizes for build times
- Implement proper error handling and notifications

### Hugging Face Optimization
- Choose appropriate hardware tier for workload
- Use Docker if complex dependencies are required
- Implement proper logging and monitoring
- Set up automatic scaling if needed

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Frontend can't reach backend | Verify API URL configuration and CORS settings |
| Build failures | Check Node.js version and dependency compatibility |
| Permission errors | Ensure proper GitHub Actions permissions are set |
| Slow deployments | Optimize build caching and asset compression |
| Secrets not loading | Verify secret names and access scopes |

## Verification

Run: `bash scripts/verify-deployment-workflow.sh`

Expected: `✓ Deployment workflows configured successfully`

## If Verification Fails

1. Check: YAML syntax with `yamllint` or similar tool
2. Validate: GitHub Actions schema against GitHub's requirements
3. Verify: Secret references match repository settings
4. Test: Individual workflow steps in isolation
5. **Stop and report** if validation continues failing

## Tool Reference

See [references/deployment-tools.md](references/deployment-tools.md) for complete deployment tool documentation.

## Troubleshooting

For deployment issues, follow this sequence:
1. Verify YAML syntax
2. Check environment configurations
3. Validate secret availability
4. Test backend health independently
5. Review CORS and network configurations