Write-Host "Generating traffic for APIs..." -ForegroundColor Green

# Generate traffic for each API
Write-Host "Generating User API Traffic..." -ForegroundColor Yellow
for ($i = 1; $i -le 5; $i++) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/" -Method "GET"
        Write-Host "User API request $i - Success" -ForegroundColor Green
    } catch {
        Write-Host "User API request $i - Error" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 200
}

Write-Host "Generating Product API Traffic..." -ForegroundColor Yellow
for ($i = 1; $i -le 5; $i++) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8001/" -Method "GET"
        Write-Host "Product API request $i - Success" -ForegroundColor Green
    } catch {
        Write-Host "Product API request $i - Error" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 200
}

Write-Host "Generating Order API Traffic..." -ForegroundColor Yellow
for ($i = 1; $i -le 5; $i++) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8002/" -Method "GET"
        Write-Host "Order API request $i - Success" -ForegroundColor Green
    } catch {
        Write-Host "Order API request $i - Error" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 200
}

Write-Host "Generating Payment API Traffic..." -ForegroundColor Yellow
for ($i = 1; $i -le 5; $i++) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8003/" -Method "GET"
        Write-Host "Payment API request $i - Success" -ForegroundColor Green
    } catch {
        Write-Host "Payment API request $i - Error" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 200
}

Write-Host "Traffic generation complete!" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:3000/d/simple_api_dashboard/simple-api-dashboard" -ForegroundColor Cyan
