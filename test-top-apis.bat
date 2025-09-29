@echo off
echo ========================================
echo Test Top APIs by Request Rate
echo Tạo dữ liệu ranking cho dashboard
echo ========================================
echo.

echo 🚀 Đang test phần "Top APIs by Request Rate"...
echo 💡 Tạo traffic với tần suất khác nhau để có ranking
echo 🔗 Dashboard: http://localhost:3000
echo 🔑 Login: admin / admin123
echo.

python test-top-apis-request-rate.py

echo.
echo 📊 Test hoàn thành!
echo 🎯 Kiểm tra dashboard để xem ranking:
echo    🥇 user-api (nhiều requests nhất)
echo    🥈 product-api (trung bình)
echo    🥉 order-api (ít hơn)
echo    🏅 payment-api (ít nhất)
echo.
pause
