# Test All APIs Script
Write-Host "Testing all 4 APIs..." -ForegroundColor Green

# Test User API (Port 8000)
Write-Host "`n=== Testing User API ===" -ForegroundColor Yellow
Write-Host "GET /api/users/"
try {
    $users = Invoke-RestMethod -Uri "http://localhost:8000/api/users/" -Method GET
    Write-Host "Response: $($users.message)" -ForegroundColor Green
    Write-Host "Data: $($users.data | ConvertTo-Json -Compress)"
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Product API (Port 8001)
Write-Host "`n=== Testing Product API ===" -ForegroundColor Yellow
Write-Host "GET /api/products/"
try {
    $products = Invoke-RestMethod -Uri "http://localhost:8001/api/products/" -Method GET
    Write-Host "Response: $($products.message)" -ForegroundColor Green
    Write-Host "Data: $($products.data | ConvertTo-Json -Compress)"
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Order API (Port 8002)
Write-Host "`n=== Testing Order API ===" -ForegroundColor Yellow
Write-Host "GET /api/orders/"
try {
    $orders = Invoke-RestMethod -Uri "http://localhost:8002/api/orders/" -Method GET
    Write-Host "Response: $($orders.message)" -ForegroundColor Green
    Write-Host "Data: $($orders.data | ConvertTo-Json -Compress)"
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Payment API (Port 8003)
Write-Host "`n=== Testing Payment API ===" -ForegroundColor Yellow
Write-Host "GET /api/payments/"
try {
    $payments = Invoke-RestMethod -Uri "http://localhost:8003/api/payments/" -Method GET
    Write-Host "Response: $($payments.message)" -ForegroundColor Green
    Write-Host "Data: $($payments.data | ConvertTo-Json -Compress)"
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Test completed ===" -ForegroundColor Green
