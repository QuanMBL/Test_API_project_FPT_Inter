@echo off
echo ========================================
echo FINAL FIX - Top APIs by Request Rate
echo Tạo dữ liệu thực sự cho dashboard
echo ========================================
echo.

echo 🚀 Đang tạo traffic mạnh...
echo 💡 Dashboard: http://localhost:3000
echo 🔑 Login: admin / admin123
echo 📊 Xem "Top APIs by Request Rate"
echo ⏰ Đợi 1-2 phút để có dữ liệu
echo 🛑 Nhấn Ctrl+C để dừng
echo.

python FINAL-FIX.py

echo.
echo 📊 FINAL FIX hoàn thành!
echo 🎯 Dashboard bây giờ sẽ có dữ liệu!
echo.
pause
