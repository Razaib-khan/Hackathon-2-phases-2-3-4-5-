# Deployment Tools Reference

## GitHub Actions Tools

### Core Actions
- `actions/checkout@v4` - Repository checkout
- `actions/setup-node@v4` - Node.js environment setup
- `actions/configure-pages@v4` - GitHub Pages configuration
- `actions/upload-pages-artifact@v3` - Upload static assets
- `actions/deploy-pages@v4` - Deploy to GitHub Pages

### Caching Actions
- `actions/cache@v4` - Dependency caching
- `actions/upload-artifact@v4` - Build artifact storage
- `actions/download-artifact@v4` - Download artifacts

### Environment Actions
- `actions/github-script@v7` - Custom GitHub API interactions
- `actions/stale@v9` - Issue/pr management

## Hugging Face Tools

### Space Runtime Configuration
- `runtime.hardware` - CPU/GPU selection
- `runtime.requirements` - Python dependencies
- `runtime.dockerfile` - Custom Docker configuration

### Space Secrets Management
- `${secret:SECRET_NAME}` - Secure secret references
- Space environment variables configuration

## YAML Validation Tools

### Linters
- `yamllint` - YAML syntax validation
- `prettier --parser yaml` - YAML formatting
- `actionlint` - GitHub Actions specific linting

### Schema Validators
- GitHub Actions schema validator
- Hugging Face configuration schema validator

## Deployment Verification Tools

### Health Checks
- `curl -f` - HTTP health check
- `wget --spider` - Resource availability check
- Custom health check scripts

### Status Monitoring
- GitHub Actions status API
- Hugging Face Space status monitoring
- Custom deployment verification scripts

## Security Tools

### Secret Scanning
- `truffleHog` - Secret leak detection
- `gitleaks` - Git repository secret scanning
- GitHub's secret scanning

### Permission Validation
- GitHub Actions permission validation
- Role-based access control verification