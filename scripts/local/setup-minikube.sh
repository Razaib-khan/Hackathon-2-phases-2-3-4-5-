#!/bin/bash

# Script to setup Minikube with Dapr and Kafka for local development

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting up Minikube for AIDO TODO application..."

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Minikube is not installed. Please install minikube first."
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Start minikube with sufficient resources
echo "Starting Minikube..."
minikube start --memory=4096 --cpus=2

# Enable required addons
echo "Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable registry

# Install Dapr
echo "Installing Dapr..."
helm repo add dapr https://dapr.github.io/helm-charts
helm repo update
helm upgrade --install dapr dapr/dapr --namespace dapr-system --create-namespace --wait

# Wait for Dapr to be ready
echo "Waiting for Dapr to be ready..."
kubectl wait --for=condition=ready pods -l app.kubernetes.io/name=dapr-placement-server -n dapr-system --timeout=300s

echo "Minikube setup complete!"
echo "Dapr has been installed and is running."
echo "You can now deploy the application using: helm install todo ./charts/todo-chatbot"