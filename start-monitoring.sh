#!/bin/bash

echo "🚀 Starting Grafana Monitoring Stack..."

# Create monitoring directories if they don't exist
mkdir -p monitoring/grafana/provisioning/datasources
mkdir -p monitoring/grafana/provisioning/dashboards
mkdir -p monitoring/grafana/dashboards

echo "📊 Starting Prometheus and Grafana..."
docker-compose up -d prometheus grafana

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Checking service status..."
docker-compose ps prometheus grafana

echo ""
echo "✅ Monitoring services started successfully!"
echo ""
echo "📈 Access URLs:"
echo "   Prometheus: http://localhost:9090"
echo "   Grafana:    http://localhost:3000"
echo ""
echo "🔑 Grafana Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "💡 To start all APIs with monitoring:"
echo "   docker-compose up -d"
echo ""
echo "📊 To view metrics:"
echo "   - User API:    http://localhost:8000/metrics"
echo "   - Product API: http://localhost:8001/metrics"
echo "   - Order API:   http://localhost:8002/metrics"
echo "   - Payment API: http://localhost:8003/metrics"
