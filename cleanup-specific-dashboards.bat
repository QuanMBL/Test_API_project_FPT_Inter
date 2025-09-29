@echo off
echo ========================================
echo Script Don Dep Dashboard Theo Yeu Cau
echo ========================================
echo.
echo 📋 Dashboard se GIU LAI:
echo    ✅ all_4api_1_v2 - Dashboard tong quan 4 API Services
echo    ✅ Dashboard Custom - Mau Blue
echo.
echo 🗑️ Tat ca dashboard khac se bi XOA
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
echo 💡 De thuc su xoa, chay: python k8s\monitoring\cleanup-specific-dashboards.py --execute
echo.

REM Chay script don dep dashboard (che do chay thu)
echo 🧹 Dang kiem tra dashboard...
python k8s\monitoring\cleanup-specific-dashboards.py

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
echo    1. Neu muon xoa thuc su, chay: python k8s\monitoring\cleanup-specific-dashboards.py --execute
echo    2. Kiem tra dashboard tai: http://localhost:3000
echo    3. Dang nhap voi: admin / admin123
echo.
pause
