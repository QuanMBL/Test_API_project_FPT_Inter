# Script to generate traffic for APIs to populate dashboard data

Write-Host "Generating traffic for APIs..." -ForegroundColor Green

# Function to make HTTP requests
function Invoke-ApiRequest {
    param(
        [string]$Url,
        [string]$Method = "GET",
        [string]$Body = $null
    )
    
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Body $Body -ContentType "application/json"
        } else {
            $response = Invoke-RestMethod -Uri $Url -Method $Method
        }
        Write-Host "✓ $Method $Url - Success" -ForegroundColor Green
    } catch {
        Write-Host "✗ $Method $Url - Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Generate traffic for each API
Write-Host "`n=== Generating User API Traffic ===" -ForegroundColor Yellow
for ($i = 1; $i -le 10; $i++) {
    Invoke-ApiRequest -Url "http://localhost:8000/" -Method "GET"
    Start-Sleep -Milliseconds 100
}

Write-Host "`n=== Generating Product API Traffic ===" -ForegroundColor Yellow
for ($i = 1; $i -le 10; $i++) {
    Invoke-ApiRequest -Url "http://localhost:8001/" -Method "GET"
    Start-Sleep -Milliseconds 100
}

Write-Host "`n=== Generating Order API Traffic ===" -ForegroundColor Yellow
for ($i = 1; $i -le 10; $i++) {
    Invoke-ApiRequest -Url "http://localhost:8002/" -Method "GET"
    Start-Sleep -Milliseconds 100
}

Write-Host "`n=== Generating Payment API Traffic ===" -ForegroundColor Yellow
for ($i = 1; $i -le 10; $i++) {
    Invoke-ApiRequest -Url "http://localhost:8003/" -Method "GET"
    Start-Sleep -Milliseconds 100
}

Write-Host "`n=== Traffic Generation Complete! ===" -ForegroundColor Green
Write-Host "Check your dashboard at: http://localhost:3000/d/simple_api_dashboard/simple-api-dashboard" -ForegroundColor Cyan
