@echo off
echo ========================================
echo Script Cap Nhat Dashboard - Khong Tao Trung Lap
echo ========================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python khong duoc cai dat hoac khong co trong PATH
    echo Hay cai dat Python va thu lai
    pause
    exit /b 1
)

REM Chay script cap nhat dashboard
echo 🚀 Dang cap nhat dashboard...
python k8s\monitoring\update-dashboard-script.py

if errorlevel 1 (
    echo.
    echo ❌ Cap nhat dashboard that bai!
    pause
    exit /b 1
)

echo.
echo ✅ Cap nhat dashboard thanh cong!
echo.
echo 📋 Cac buoc tiep theo:
echo    1. Kiem tra dashboard tai: http://localhost:3000
echo    2. Dang nhap voi: admin / admin123
echo    3. Neu co dashboard trung lap, chay: cleanup-dashboards.bat
echo.
pause
