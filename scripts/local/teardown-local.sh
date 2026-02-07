#!/bin/bash

# Script to clean up local Minikube deployment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Cleaning up local Minikube deployment..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not available. Cannot proceed with cleanup."
    exit 1
fi

# Uninstall the application
NAMESPACE="todo-app"
echo "Uninstalling application..."
helm uninstall todo-chatbot --namespace $NAMESPACE || echo "Application was not installed or already uninstalled."

# Delete the namespace
echo "Deleting namespace..."
kubectl delete namespace $NAMESPACE --ignore-not-found=true

# Optionally stop minikube (uncomment if you want to stop minikube)
# echo "Stopping Minikube..."
# minikube stop

echo "Local deployment cleanup complete!"