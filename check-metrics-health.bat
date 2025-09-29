@echo off
echo ========================================
echo Kiểm tra sức khỏe Metrics và Dashboard
echo ========================================
echo.

echo 🔍 Đang kiểm tra metrics...
python k8s\monitoring\check-metrics-health.py

echo.
echo 💡 Nếu dashboard vẫn không hiển thị dữ liệu:
echo    • Đợi 1-2 phút để metrics được thu thập
echo    • Refresh dashboard trong Grafana
echo    • Kiểm tra time range trong dashboard
echo    • Đảm bảo các API services đang nhận requests
echo.
pause
