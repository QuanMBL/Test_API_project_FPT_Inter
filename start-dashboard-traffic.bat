@echo off
echo ========================================
echo Dashboard Traffic Generator
echo Tạo dữ liệu lên xuống cho dashboard
echo ========================================
echo.

echo 🚀 Đang khởi động traffic generator...
echo 💡 Dashboard sẽ có dữ liệu real-time!
echo 🔗 Dashboard: http://localhost:3000
echo 🔑 Login: admin / admin123
echo 📊 Xem "Top APIs by Request Rate" để thấy dữ liệu lên xuống
echo.

python generate-dashboard-data.py

echo.
echo 📊 Traffic generation hoàn thành!
echo 🎉 Dashboard bây giờ sẽ có dữ liệu lên xuống!
echo.
pause
