# PowerShell script to start Grafana Monitoring Stack

Write-Host "🚀 Starting Grafana Monitoring Stack..." -ForegroundColor Green

# Create monitoring directories if they don't exist
New-Item -ItemType Directory -Path "monitoring\grafana\provisioning\datasources" -Force | Out-Null
New-Item -ItemType Directory -Path "monitoring\grafana\provisioning\dashboards" -Force | Out-Null
New-Item -ItemType Directory -Path "monitoring\grafana\dashboards" -Force | Out-Null

Write-Host "📊 Starting Prometheus and Grafana..." -ForegroundColor Yellow
docker-compose up -d prometheus grafana

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "🔍 Checking service status..." -ForegroundColor Yellow
docker-compose ps prometheus grafana

Write-Host ""
Write-Host "✅ Monitoring services started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📈 Access URLs:" -ForegroundColor Cyan
Write-Host "   Prometheus: http://localhost:9090" -ForegroundColor White
Write-Host "   Grafana:    http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Grafana Credentials:" -ForegroundColor Cyan
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "💡 To start all APIs with monitoring:" -ForegroundColor Cyan
Write-Host "   docker-compose up -d" -ForegroundColor White
Write-Host ""
Write-Host "📊 To view metrics:" -ForegroundColor Cyan
Write-Host "   - User API:    http://localhost:8000/metrics" -ForegroundColor White
Write-Host "   - Product API: http://localhost:8001/metrics" -ForegroundColor White
Write-Host "   - Order API:   http://localhost:8002/metrics" -ForegroundColor White
Write-Host "   - Payment API: http://localhost:8003/metrics" -ForegroundColor White
