#!/bin/bash

echo "Building Docker images..."

# Build Docker images
docker build -t user-api:latest ./api1
docker build -t product-api:latest ./api2
docker build -t order-api:latest ./api3
docker build -t payment-api:latest ./api4

echo "Docker images built successfully!"

echo "Deploying to Kubernetes..."

# Apply Kubernetes manifests
kubectl apply -f k8s/user-api-deployment.yaml
kubectl apply -f k8s/product-api-deployment.yaml
kubectl apply -f k8s/order-api-deployment.yaml
kubectl apply -f k8s/payment-api-deployment.yaml

echo "Deployment completed!"

echo "Checking pod status..."
kubectl get pods

echo "Checking services..."
kubectl get services
