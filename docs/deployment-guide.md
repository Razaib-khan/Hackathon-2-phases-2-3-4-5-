# AIDO TODO Application - Deployment Guide

## Overview
This guide provides instructions for deploying the AIDO TODO application with advanced features including recurring tasks, due dates, reminders, Kafka event streaming, and Dapr integration.

## Architecture Components

### Core Services
- **Backend**: FastAPI application with task management, chat API, and MCP integration
- **Frontend**: Next.js application for user interface
- **Database**: PostgreSQL for persistent storage
- **Kafka**: Event streaming platform for task events and reminders
- **Dapr**: Distributed Application Runtime for service-to-service communication and state management

### Advanced Features
- **Recurring Tasks**: Tasks that automatically generate new instances based on patterns
- **Due Dates & Reminders**: Notifications sent at specified times
- **Event-Driven Architecture**: Asynchronous processing using Kafka

## Local Development Setup

### Prerequisites
- Docker and Docker Compose
- Minikube
- kubectl
- Helm
- Dapr CLI

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Setup Minikube with Dapr and Kafka**
   ```bash
   chmod +x scripts/local/setup-minikube.sh
   ./scripts/local/setup-minikube.sh
   ```

3. **Deploy the application**
   ```bash
   chmod +x scripts/local/deploy-local.sh
   ./scripts/local/deploy-local.sh
   ```

4. **Access the application**
   - Backend API: `http://<minikube-ip>:30080`
   - Frontend UI: `http://<minikube-ip>:30080`

### Teardown
To remove the local deployment:
```bash
chmod +x scripts/local/teardown-local.sh
./scripts/local/teardown-local.sh
```

## Cloud Deployment

### Azure AKS Deployment

1. **Initialize Terraform** (for new infrastructure)
   ```bash
   cd infrastructure/aks
   terraform init
   terraform plan -var="project_id=your-project-id"
   terraform apply -var="project_id=your-project-id"
   ```

2. **Deploy using Helm**
   ```bash
   kubectl config use-context <aks-cluster-context>
   helm upgrade --install todo-chatbot ./charts/todo-chatbot \
     --values ./charts/todo-chatbot/values-aks.yaml \
     --namespace todo-app \
     --create-namespace \
     --wait
   ```

### Google GKE Deployment

1. **Initialize Terraform** (for new infrastructure)
   ```bash
   cd infrastructure/gke
   terraform init
   terraform plan -var="project_id=your-project-id"
   terraform apply -var="project_id=your-project-id"
   ```

2. **Deploy using Helm**
   ```bash
   kubectl config use-context <gke-cluster-context>
   helm upgrade --install todo-chatbot ./charts/todo-chatbot \
     --values ./charts/todo-chatbot/values-gke.yaml \
     --namespace todo-app \
     --create-namespace \
     --wait
   ```

## Configuration

### Environment Variables
The application uses several environment variables for configuration:

#### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `AUTH_SECRET`: Secret for JWT authentication
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker addresses
- `KAFKA_TASK_EVENTS_TOPIC`: Topic name for task events
- `KAFKA_REMINDERS_TOPIC`: Topic name for reminder events

#### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_SSO_URL`: SSO service URL

### Dapr Configuration
The application uses Dapr for:
- Service-to-service invocation
- State management
- Pub/Sub messaging
- Secret management

## Monitoring and Observability

### Health Checks
The application provides several health check endpoints:
- `/health`: Overall health status
- `/ready`: Readiness probe
- `/metrics`: Application metrics

### Logging
Logs are structured in JSON format and include contextual information for easier analysis.

### Monitoring Stack
The deployment includes:
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Loki**: Log aggregation
- **Tempo**: Distributed tracing

## Troubleshooting

### Common Issues

1. **Kafka Connection Issues**
   - Verify Kafka pods are running: `kubectl get pods -l app.kubernetes.io/component=kafka`
   - Check Kafka logs: `kubectl logs -l app.kubernetes.io/component=kafka`

2. **Dapr Sidecar Issues**
   - Verify Dapr is installed: `dapr status -k`
   - Check Dapr logs: `kubectl logs -l app.kubernetes.io/name=dapr-placement-server -n dapr-system`

3. **Database Connection Issues**
   - Verify database is accessible
   - Check connection string configuration

### Diagnostic Commands
```bash
# Check all pods
kubectl get pods -n todo-app

# Check service status
kubectl get services -n todo-app

# View application logs
kubectl logs -l app.kubernetes.io/name=todo-chatbot-backend -n todo-app

# Check Dapr status
dapr status -k
```

## Scaling

### Horizontal Pod Autoscaling
The Helm charts include HPA configurations for automatic scaling based on CPU utilization.

### Manual Scaling
```bash
# Scale backend
kubectl scale deployment todo-chatbot-backend -n todo-app --replicas=3

# Scale frontend
kubectl scale deployment todo-chatbot-frontend -n todo-app --replicas=3
```

## Security Considerations

- All services should run with minimal required privileges
- Secrets should be stored in Kubernetes secrets or Dapr secret stores
- Network policies should restrict traffic between components
- TLS should be enabled for all external communications