@echo off
echo 🚀 Import Dashboard all_4api_1 - Tổng quan 4 API Services
echo ============================================================

echo 🔍 Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)
echo ✅ Python found

echo 🔍 Checking Grafana...
curl -s http://localhost:3000/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Cannot connect to Grafana. Make sure it's running on http://localhost:3000
    pause
    exit /b 1
)
echo ✅ Grafana is running

echo 📊 Importing dashboard...
python k8s/monitoring/import-all-4api-1-dashboard.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Dashboard imported successfully!
    echo.
    echo 📋 Dashboard Features:
    echo    • 📊 Tổng số Services đang hoạt động
    echo    • 🖥️ CPU Usage trung bình và theo từng service
    echo    • 💾 Memory Usage tổng và theo từng service
    echo    • ⚠️ Tỷ lệ lỗi trung bình và theo từng service
    echo    • ⏱️ Response Time theo từng service
    echo    • 🚀 Request Rate theo từng service
    echo    • 📊 HTTP Methods (GET/POST) theo từng service
    echo.
    echo 🔗 Access your dashboard at: http://localhost:3000
    echo 👤 Login: admin / admin123
) else (
    echo ❌ Import failed!
    pause
    exit /b 1
)

pause
