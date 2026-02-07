#!/bin/bash

# Script to deploy the AIDO TODO application to local Minikube

set -e  # Exit immediately if a command exits with a non-zero status

echo "Deploying AIDO TODO application to Minikube..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not available. Please ensure kubectl is installed and configured."
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "Helm is not available. Please ensure Helm is installed."
    exit 1
fi

# Create namespace if it doesn't exist
NAMESPACE="todo-app"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Install/upgrade the application using Helm
echo "Installing/upgrading the application..."
helm upgrade --install todo-chatbot ./charts/todo-chatbot \
    --namespace $NAMESPACE \
    --create-namespace \
    --values ./charts/todo-chatbot/values.yaml \
    --wait \
    --timeout=10m

# Wait for all pods to be ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pods -l app.kubernetes.io/name=todo-chatbot-backend -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=ready pods -l app.kubernetes.io/name=todo-chatbot-frontend -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=ready pods -l app.kubernetes.io/component=kafka -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=ready pods -l app.kubernetes.io/component=zookeeper -n $NAMESPACE --timeout=300s

# Get the service URLs
echo "Services deployed:"
kubectl get svc -n $NAMESPACE

# Get minikube IP for accessing the services
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: $MINIKUBE_IP"

echo "Application deployment complete!"
echo "Backend API should be available at: http://$MINIKUBE_IP:30080 (if using NodePort)"
echo "Frontend should be available at: http://$MINIKUBE_IP:30080 (if using NodePort)"
echo "You can also use 'minikube tunnel' to expose LoadBalancer services."