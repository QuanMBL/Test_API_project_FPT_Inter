@echo off
echo ========================================
echo Dashboard Traffic Generator
echo Tạo traffic và kiểm tra dashboard
echo ========================================
echo.

echo 🚀 Đang tạo traffic liên tục...
echo 💡 Mở dashboard: http://localhost:3000
echo 🔑 Login: admin / admin123
echo 📊 Xem "Top APIs by Request Rate" 
echo 🛑 Nhấn Ctrl+C để dừng
echo.

start python generate-dashboard-data.py

echo.
echo ⏳ Đợi 30 giây để có dữ liệu...
timeout /t 30 /nobreak

echo.
echo 🔍 Kiểm tra Prometheus metrics...
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:9090/api/v1/query?query=sum(rate(django_http_requests_total[1m])) by (job)' | Select-Object -ExpandProperty Content"

echo.
echo 📊 Traffic đang chạy! Kiểm tra dashboard:
echo 🔗 http://localhost:3000
echo.
pause
