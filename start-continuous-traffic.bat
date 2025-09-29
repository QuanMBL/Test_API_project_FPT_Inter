@echo off
echo ========================================
echo Continuous Traffic Generator
echo Tạo traffic liên tục cho dashboard
echo ========================================
echo.

echo 🚀 Đang tạo traffic liên tục...
echo 💡 Dashboard sẽ có dữ liệu real-time!
echo 🔗 Dashboard: http://localhost:3000
echo 👤 Đăng nhập: admin / admin123
echo 🛑 Nhấn Ctrl+C để dừng
echo.

python k8s\monitoring\continuous-traffic-generator.py

echo.
echo 📊 Traffic generation hoàn thành!
echo 🎉 Dashboard bây giờ sẽ có dữ liệu!
echo.
pause
