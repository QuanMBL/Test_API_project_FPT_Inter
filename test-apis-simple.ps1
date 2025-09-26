# Simple PowerShell script to test APIs and generate data
Write-Host "🎯 Testing APIs and generating data..." -ForegroundColor Green

$apis = @(
    @{name="User API"; url="http://localhost:8000/api/users/"},
    @{name="Product API"; url="http://localhost:8001/api/products/"},
    @{name="Order API"; url="http://localhost:8002/api/orders/"},
    @{name="Payment API"; url="http://localhost:8003/api/payments/"}
)

$count = 0
while ($count -lt 50) {
    $count++
    Write-Host "🔄 Round $count - Testing all APIs..." -ForegroundColor Cyan
    
    foreach ($api in $apis) {
        try {
            # Test GET request
            $response = Invoke-WebRequest -Uri $api.url -UseBasicParsing -TimeoutSec 5
            Write-Host "✅ $($api.name): GET - Status $($response.StatusCode)" -ForegroundColor Green
            
            # Test POST request with random data
            $randomData = @{
                name = "Test Item $count"
                description = "Generated data for monitoring"
                value = Get-Random -Minimum 1 -Maximum 100
            }
            
            $postResponse = Invoke-WebRequest -Uri $api.url -Method POST -Body ($randomData | ConvertTo-Json) -ContentType "application/json" -UseBasicParsing -TimeoutSec 5
            Write-Host "✅ $($api.name): POST - Status $($postResponse.StatusCode)" -ForegroundColor Green
            
        } catch {
            Write-Host "❌ $($api.name): Error - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    Write-Host "⏳ Waiting 2 seconds before next round..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
}

Write-Host "Data generation completed! Check Grafana dashboard now." -ForegroundColor Green
Write-Host "Open Grafana: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Open Prometheus: http://localhost:9090" -ForegroundColor Cyan
