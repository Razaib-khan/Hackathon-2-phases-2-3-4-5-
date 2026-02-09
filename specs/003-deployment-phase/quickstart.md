# Phase IV: Local Kubernetes Deployment

## Overview

This phase implements the deployment of the Todo Chatbot application on a local Kubernetes cluster using Minikube, Helm Charts, and AI-assisted tools. The deployment includes both frontend and backend applications with AI agent integration.

## Architecture

- **Frontend**: Next.js application (runs on port 3000)
- **Backend**: FastAPI application with MCP server for AI integration (runs on port 8000)
- **Database**: PostgreSQL (Neon or external connection)
- **Orchestration**: Kubernetes with Minikube
- **Packaging**: Helm Charts

## Components

### Docker Images
- `todo-chatbot-frontend`: Next.js application container
- `todo-chatbot-backend`: FastAPI application container with AI agent integration

### Kubernetes Resources
- Namespaces for isolation
- Deployments for application management
- Services for internal and external communication
- Secrets for sensitive configuration
- ConfigMaps for non-sensitive configuration
- Ingress for external access (optional)

### Helm Chart Structure
```
charts/todo-chatbot/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── templates/          # Kubernetes resource templates
│   ├── _helpers.tpl    # Template helper functions
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-secret.yaml
│   └── ingress.yaml
└── charts/             # Chart dependencies
```

## Prerequisites

- Docker (with WSL2 integration if on Windows)
- Minikube
- kubectl
- Helm 3
- At least 8GB RAM and 4 CPU cores available

## Quick Start

1. **Start Minikube:**
   ```bash
   minikube start --driver=docker --memory=8192 --cpus=4
   minikube addons enable ingress
   ```

2. **Deploy using the script:**
   ```bash
   ./scripts/deploy-k8s.sh
   ```

3. **Access the application:**
   - Frontend: `http://$(minikube ip):30008`
   - Backend: `http://$(minikube ip):30007`

## Deployment Script Features

The `scripts/deploy-k8s.sh` script automates:
- Docker image building
- Namespace creation
- Helm chart installation
- Configuration management
- Health checks

## Configuration

The deployment can be customized using Helm values. Create a custom `values.yaml` file to override defaults:

```bash
helm install todo-chatbot charts/todo-chatbot -f custom-values.yaml
```

## AI-Assisted Operations

This deployment supports AI-assisted operations using:
- **kubectl-ai**: For intelligent kubectl commands
- **kagent**: For cluster analysis and optimization
- **Docker AI Agent (Gordon)**: For intelligent Docker operations

Example kubectl-ai commands:
```bash
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "scale the backend to handle more load"
kubectl-ai "check why the pods are failing"
```

## Monitoring

Monitor the deployment with:
```bash
# Check pod status
kubectl get pods -n todo-chatbot

# View logs
kubectl logs -l app.kubernetes.io/name=todo-chatbot-backend -n todo-chatbot

# Monitor resources
kubectl top pods -n todo-chatbot
```

## Scaling

The application supports horizontal scaling:
```bash
# Scale backend
kubectl scale deployment todo-chatbot-backend -n todo-chatbot --replicas=3

# Scale frontend
kubectl scale deployment todo-chatbot-frontend -n todo-chatbot --replicas=3
```

## Cleanup

To remove the deployment:
```bash
helm uninstall todo-chatbot -n todo-chatbot
kubectl delete namespace todo-chatbot
```

## Documentation

For detailed information about the deployment process, see:
- `docs/kubernetes-deployment.md` - Full deployment guide
- `charts/todo-chatbot/` - Helm chart documentation

## Troubleshooting

Common issues and solutions:

1. **Docker build failures**: Ensure Docker is running and has sufficient resources
2. **Minikube startup issues**: Check system resources and virtualization settings
3. **Image pull issues**: Verify image names and tags match built images
4. **Service access**: Use `minikube tunnel` or port forwarding for external access