#!/bin/bash

# Deployment script for Todo Chatbot on Kubernetes
# This script builds Docker images and deploys the application using Helm

set -e  # Exit on any error

echo "🚀 Starting deployment of Todo Chatbot to Kubernetes..."

# Check if required tools are available
command -v docker >/dev/null 2>&1 || { echo >&2 "❌ Docker is required but not installed. Aborting."; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo >&2 "❌ kubectl is required but not installed. Aborting."; exit 1; }
command -v helm >/dev/null 2>&1 || { echo >&2 "❌ Helm is required but not installed. Aborting."; exit 1; }

# Configuration
BACKEND_IMAGE_NAME="todo-chatbot-backend"
FRONTEND_IMAGE_NAME="todo-chatbot-frontend"
HELM_RELEASE_NAME="todo-chatbot"
NAMESPACE="todo-chatbot"

echo "🔧 Checking if Minikube is running..."
if ! minikube status >/dev/null 2>&1; then
    echo "💡 Minikube is not running. Starting Minikube with Docker driver..."
    minikube start --driver=docker --memory=3072 --cpus=2 --disk-size=10g
fi

echo "🐳 Setting Docker environment to Minikube..."
eval $(minikube docker-env)

echo "🏗️ Building backend Docker image..."
cd hf_space_cloned
docker build -t $BACKEND_IMAGE_NAME:latest .
cd ..

echo "🏗️ Building frontend Docker image..."
cd frontend
docker build -t $FRONTEND_IMAGE_NAME:latest .
cd ..

echo "_namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

echo "⎈ Installing/upgrading Helm release..."
helm upgrade --install $HELM_RELEASE_NAME charts/todo-chatbot \
    --namespace $NAMESPACE \
    --set backend.image.repository=$BACKEND_IMAGE_NAME \
    --set backend.image.tag=latest \
    --set backend.image.pullPolicy=Never \
    --set frontend.image.repository=$FRONTEND_IMAGE_NAME \
    --set frontend.image.tag=latest \
    --set frontend.image.pullPolicy=Never \
    --set env.backend.DATABASE_URL="${DATABASE_URL:-postgresql://user:password@neon-host:5432/dbname}" \
    --set env.backend.AUTH_SECRET="${AUTH_SECRET:-$(openssl rand -base64 32)}" \
    --set env.frontend.NEXT_PUBLIC_API_URL="http://$(minikube ip):30007" \
    --atomic \
    --timeout=20m

echo "✅ Deployment completed successfully!"

echo "🔗 Access the application:"
echo "  Frontend: http://$(minikube ip):30008"
echo "  Backend: http://$(minikube ip):30007"

echo "📊 Check deployment status:"
echo "  kubectl get pods -n $NAMESPACE"
echo "  kubectl get services -n $NAMESPACE"
echo "  kubectl get ingress -n $NAMESPACE"

echo "📝 To access application logs:"
echo "  kubectl logs -l app.kubernetes.io/name=todo-chatbot-backend -n $NAMESPACE"
echo "  kubectl logs -l app.kubernetes.io/name=todo-chatbot-frontend -n $NAMESPACE"

echo "🔄 To port forward for local access:"
echo "  kubectl port-forward -n $NAMESPACE svc/todo-chatbot-backend 8000:8000"
echo "  kubectl port-forward -n $NAMESPACE svc/todo-chatbot-frontend 3000:3000"

echo "🧹 To uninstall:"
echo "  helm uninstall $HELM_RELEASE_NAME -n $NAMESPACE"