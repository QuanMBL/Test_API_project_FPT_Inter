@echo off
echo ========================================
echo WORKING TRAFFIC GENERATOR
echo Tạo dữ liệu thực sự cho Top APIs
echo ========================================
echo.

echo 🚀 Đang tạo traffic liên tục...
echo 💡 Dashboard: http://localhost:3000
echo 🔑 Login: admin / admin123
echo 📊 Xem "Top APIs by Request Rate"
echo ⏰ Đợi 2-3 phút để có dữ liệu
echo 🛑 Nhấn Ctrl+C để dừng
echo.

start /B python fix-dashboard-data.py

echo.
echo ⏳ Đợi 30 giây để có dữ liệu...
timeout /t 30 /nobreak

echo.
echo 🔍 Kiểm tra Prometheus metrics...
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:9090/api/v1/query?query=sum(rate(django_http_requests_total[5m])) by (job)' | Select-Object -ExpandProperty Content"

echo.
echo 📊 Traffic đang chạy!
echo 🎯 Mở dashboard để xem dữ liệu:
echo    🔗 http://localhost:3000
echo    📈 Top APIs by Request Rate
echo.
pause
