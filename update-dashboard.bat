@echo off
echo ========================================
echo Cập nhật Dashboard sau khi chỉnh sửa
echo ========================================
echo.

echo 🔄 Đang import lại dashboard...
python k8s\monitoring\import-all-4api-1-v2-enhanced-dashboard.py

echo.
echo ✅ Dashboard đã được cập nhật!
echo 🔗 Truy cập: http://localhost:3000
echo 👤 Đăng nhập: admin / admin123
echo.
pause
