@echo off
echo ========================================
echo Script Don Dep Dashboard Trung Lap
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

echo 🔍 Che do chay thu - Hien thi dashboard se bi xoa
echo 💡 De thuc su xoa, chay: python k8s\monitoring\cleanup-duplicate-dashboards.py --execute
echo.

REM Chay script don dep dashboard (che do chay thu)
echo 🧹 Dang kiem tra dashboard trung lap...
python k8s\monitoring\cleanup-duplicate-dashboards.py

if errorlevel 1 (
    echo.
    echo ❌ Kiem tra dashboard that bai!
    pause
    exit /b 1
)

echo.
echo ✅ Kiem tra dashboard hoan tat!
echo.
echo 📋 Cac buoc tiep theo:
echo    1. Neu co dashboard trung lap, chay: python k8s\monitoring\cleanup-duplicate-dashboards.py --execute
echo    2. Kiem tra dashboard tai: http://localhost:3000
echo    3. Dang nhap voi: admin / admin123
echo.
pause
