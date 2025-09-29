@echo off
echo ========================================
echo Import Dashboard all_4api_1_v2_enhanced
echo Dashboard tổng quan 4 API Services với bảng dữ liệu ổn định
echo ========================================
echo.

echo 🚀 Đang import dashboard enhanced...
python k8s\monitoring\import-all-4api-1-v2-enhanced-dashboard.py

echo.
echo 📋 Dashboard Enhanced Features:
echo    • 📊 Tổng số Services đang hoạt động
echo    • 🖥️ CPU Usage trung bình và theo từng service
echo    • 💾 Memory Usage tổng và theo từng service
echo    • ⚠️ Tỷ lệ lỗi trung bình và theo từng service
echo    • 📋 Bảng thông tin Services (ỔN ĐỊNH)
echo    • 📊 Bảng CPU Usage theo Service (ỔN ĐỊNH)
echo    • 💾 Bảng Memory Usage theo Service (ỔN ĐỊNH)
echo    • 🚀 Bảng Request Rate theo Service (ỔN ĐỊNH)
echo    • 📈 Biểu đồ CPU Usage theo thời gian
echo    • 💾 Biểu đồ Memory Usage theo thời gian
echo    • 📊 Bảng HTTP Status Codes (ỔN ĐỊNH)
echo    • ⏱️ Bảng Response Time trung bình (ỔN ĐỊNH)
echo.
echo 🔗 Truy cập dashboard tại: http://localhost:3000
echo 👤 Đăng nhập: admin / admin123
echo.
echo 💡 Lưu ý: Các bảng dữ liệu sẽ hiển thị ổn định hơn biểu đồ
echo.
pause
