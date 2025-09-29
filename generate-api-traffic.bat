@echo off
echo ========================================
echo API Traffic Generator
echo Tạo traffic để test dashboard
echo ========================================
echo.

echo 🚀 Đang tạo traffic cho các API services...
echo 💡 Hãy mở Grafana dashboard để xem dữ liệu real-time!
echo 🔗 Grafana: http://localhost:3000
echo 👤 Đăng nhập: admin / admin123
echo.

python k8s\monitoring\generate-api-traffic.py

echo.
echo 📊 Traffic generation hoàn thành!
echo 🎉 Bây giờ hãy kiểm tra dashboard để xem dữ liệu!
echo.
pause
