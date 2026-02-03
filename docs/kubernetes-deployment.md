# Kubernetes Deployment Guide for Todo Chatbot

## Overview

This guide explains how to deploy the Todo Chatbot application to a local Kubernetes cluster using Minikube and Helm charts. The deployment consists of:
- Frontend: Next.js application
- Backend: FastAPI application with AI agent integration
- Database: PostgreSQL (Neon or external)

## Prerequisites

Before deploying, ensure you have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm 3](https://helm.sh/docs/intro/install/)

For Windows users with WSL2, make sure Docker Desktop is installed and WSL integration is enabled.

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Start Minikube

```bash
minikube start --driver=docker --memory=8192 --cpus=4
minikube addons enable ingress
```

### 3. Deploy the Application

Use the provided deployment script:

```bash
./scripts/deploy-k8s.sh
```

The script will:
- Build Docker images for frontend and backend
- Create a Kubernetes namespace
- Install the application using Helm

## Manual Deployment Steps

If you prefer to deploy manually:

### 1. Build Docker Images

```bash
# Set Docker environment to Minikube
eval $(minikube docker-env)

# Build backend image
cd backend
docker build -t todo-chatbot-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t todo-chatbot-frontend:latest .
cd ..
```

### 2. Install with Helm

```bash
# Create namespace
kubectl create namespace todo-chatbot

# Install the chart
helm install todo-chatbot charts/todo-chatbot \
    --namespace todo-chatbot \
    --set backend.image.repository=todo-chatbot-backend \
    --set backend.image.tag=latest \
    --set backend.image.pullPolicy=Never \
    --set frontend.image.repository=todo-chatbot-frontend \
    --set frontend.image.tag=latest \
    --set frontend.image.pullPolicy=Never \
    --set env.backend.DATABASE_URL="postgresql://user:password@host:5432/dbname" \
    --set env.backend.AUTH_SECRET="your-auth-secret" \
    --set env.frontend.NEXT_PUBLIC_API_URL="http://localhost:8000"
```

## Configuration

### Custom Values

You can customize the deployment by creating a `values.yaml` file:

```yaml
backend:
  replicaCount: 2
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 200m
      memory: 256Mi

frontend:
  replicaCount: 2
  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi

env:
  backend:
    DATABASE_URL: "postgresql://user:password@neon-host:5432/dbname"
    AUTH_SECRET: "your-secure-auth-secret"
  frontend:
    NEXT_PUBLIC_API_URL: "http://your-domain.com/api"
```

Then install with:

```bash
helm install todo-chatbot charts/todo-chatbot -f your-values.yaml
```

### Environment Variables

#### Backend Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `AUTH_SECRET`: Secret key for authentication
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `PORT`: Port number for the backend (default: 8000)

#### Frontend Environment Variables

- `NEXT_PUBLIC_API_URL`: URL of the backend API
- `NEXT_PUBLIC_SSO_URL`: URL for SSO if applicable

## Accessing the Application

### Using Minikube Tunnel

```bash
minikube tunnel
```

Then access the services using their LoadBalancer IPs:

```bash
kubectl get services --namespace todo-chatbot
```

### Using Port Forwarding

```bash
# Forward backend
kubectl port-forward -n todo-chatbot svc/todo-chatbot-backend 8000:8000

# Forward frontend
kubectl port-forward -n todo-chatbot svc/todo-chatbot-frontend 3000:3000
```

### Using Ingress

Enable ingress in your values file:

```yaml
backend:
  ingress:
    enabled: true
    hosts:
      - host: todo.local
        paths:
          - path: /
            pathType: Prefix
```

Add the host to your `/etc/hosts` file:

```bash
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
```

## Monitoring and Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n todo-chatbot
kubectl describe pod <pod-name> -n todo-chatbot
```

### View Logs

```bash
# Backend logs
kubectl logs -l app.kubernetes.io/name=todo-chatbot-backend -n todo-chatbot

# Frontend logs
kubectl logs -l app.kubernetes.io/name=todo-chatbot-frontend -n todo-chatbot

# Follow logs
kubectl logs -f -l app.kubernetes.io/name=todo-chatbot-backend -n todo-chatbot
```

### Check Services

```bash
kubectl get services -n todo-chatbot
```

### Check ConfigMaps and Secrets

```bash
kubectl get configmaps -n todo-chatbot
kubectl get secrets -n todo-chatbot
```

## Scaling

Scale deployments manually:

```bash
# Scale backend
kubectl scale deployment todo-chatbot-backend -n todo-chatbot --replicas=3

# Scale frontend
kubectl scale deployment todo-chatbot-frontend -n todo-chatbot --replicas=3
```

Or enable Horizontal Pod Autoscaler in your values file:

```yaml
backend:
  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 5
    targetCPUUtilizationPercentage: 80

frontend:
  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 3
    targetCPUUtilizationPercentage: 80
```

## Updating the Application

### Update with New Images

```bash
# Build new images
eval $(minikube docker-env)
cd backend && docker build -t todo-chatbot-backend:new-tag . && cd ..
cd frontend && docker build -t todo-chatbot-frontend:new-tag . && cd ..

# Upgrade the release
helm upgrade todo-chatbot charts/todo-chatbot \
    --namespace todo-chatbot \
    --set backend.image.tag=new-tag \
    --set frontend.image.tag=new-tag
```

### Update Configuration

```bash
helm upgrade todo-chatbot charts/todo-chatbot -f updated-values.yaml
```

## Uninstalling

Remove the application:

```bash
helm uninstall todo-chatbot -n todo-chatbot
kubectl delete namespace todo-chatbot
```

## Advanced Features

### AI Agent Integration

The backend includes MCP (Model Context Protocol) server for AI agent integration. Ensure that the AI agent services are properly configured and accessible within the cluster.

### Database Configuration

For production deployments, consider using a managed PostgreSQL service or deploying PostgreSQL in Kubernetes with proper backup and monitoring.

### SSL/TLS

Configure TLS certificates for secure communication:

```yaml
backend:
  ingress:
    enabled: true
    tls:
      - secretName: todo-backend-tls
        hosts:
          - api.todo.example.com
```

## Best Practices

1. **Security**: Always use secrets for sensitive data, not configmaps
2. **Resources**: Set appropriate resource limits and requests
3. **Health Checks**: Implement proper liveness and readiness probes
4. **Monitoring**: Set up monitoring and alerting for production deployments
5. **Backup**: Implement database backup strategies
6. **Networking**: Use proper network policies for security