# PowerShell script to start API data generation
Write-Host "🎯 Starting API Data Generation..." -ForegroundColor Green
Write-Host "This will generate continuous API requests to create monitoring data" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
Write-Host ""

# Check if Python is available
try {
    python --version | Out-Null
    Write-Host "✅ Python found" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if requests module is available
try {
    python -c "import requests" 2>$null
    Write-Host "✅ requests module found" -ForegroundColor Green
} catch {
    Write-Host "❌ requests module not found. Installing..." -ForegroundColor Yellow
    pip install requests
}

# Start the data generator
Write-Host "🚀 Starting data generator..." -ForegroundColor Cyan
python generate-api-data.py
