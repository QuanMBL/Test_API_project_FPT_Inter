# 🔄 Hướng Dẫn Cập Nhật Dashboard - Không Tạo Trùng Lặp

## 🎯 Vấn Đề Đã Giải Quyết

Trước đây, mỗi lần chạy script import dashboard đều tạo ra dashboard mới, dẫn đến nhiều dashboard trùng lặp. Bây giờ đã có giải pháp:

- ✅ **Cập nhật dashboard cũ** thay vì tạo mới
- ✅ **Tìm kiếm dashboard theo tên** trước khi import
- ✅ **Dọn dẹp dashboard trùng lặp** hiện có
- ✅ **Script tổng hợp** để quản lý tất cả dashboard

## 📋 Các Script Mới

### 1. 🚀 Cập Nhật Dashboard (Không Tạo Trùng Lặp)
```bash
# Chạy script cập nhật tất cả dashboard
update-dashboards.bat

# Hoặc chạy trực tiếp Python
python k8s\monitoring\update-dashboard-script.py
```

**Tính năng:**
- Tìm kiếm dashboard cũ theo tên
- Cập nhật dashboard cũ nếu tồn tại
- Tạo dashboard mới nếu chưa có
- Không tạo dashboard trùng lặp

### 2. 🧹 Dọn Dẹp Dashboard Trùng Lặp
```bash
# Chạy thử (chỉ hiển thị dashboard sẽ bị xóa)
cleanup-dashboards.bat

# Thực sự xóa dashboard trùng lặp
python k8s\monitoring\cleanup-duplicate-dashboards.py --execute
```

**Tính năng:**
- Tìm tất cả dashboard trùng lặp
- Giữ lại dashboard mới nhất (version cao nhất)
- Xóa các dashboard cũ trùng lặp
- Chế độ chạy thử an toàn

## 🔧 Cách Sử Dụng

### Bước 1: Cập Nhật Dashboard
```bash
# Chạy script cập nhật
update-dashboards.bat
```

Script sẽ:
1. ✅ Kiểm tra kết nối Grafana
2. 🔍 Tìm kiếm dashboard cũ theo tên
3. 🔄 Cập nhật dashboard cũ nếu tồn tại
4. 🆕 Tạo dashboard mới nếu chưa có
5. 📊 Hiển thị kết quả

### Bước 2: Dọn Dẹp Dashboard Trùng Lặp (Nếu Cần)
```bash
# Chạy thử trước
cleanup-dashboards.bat

# Nếu có dashboard trùng lặp, thực sự xóa
python k8s\monitoring\cleanup-duplicate-dashboards.py --execute
```

## 📊 Dashboard Được Quản Lý

Script sẽ cập nhật các dashboard sau:

1. **All 4 API Simple Dashboard** - Tổng quan 4 API Services cơ bản
2. **All 4 API Enhanced Dashboard** - Tổng quan với bảng dữ liệu
3. **CPU Resource Dashboard** - Giám sát CPU và tài nguyên chi tiết
4. **Custom Blue Dashboard** - Dashboard tùy chỉnh màu xanh

## 🛡️ An Toàn

- ✅ **Chế độ chạy thử** cho script dọn dẹp
- ✅ **Xác nhận trước khi xóa** dashboard
- ✅ **Giữ lại dashboard mới nhất** (version cao nhất)
- ✅ **Backup tự động** thông tin dashboard

## 🔗 Truy Cập Dashboard

Sau khi cập nhật:
- 🌐 **URL:** http://localhost:3000
- 👤 **Đăng nhập:** admin / admin123
- 📊 **Dashboard chính:** Tìm theo tên dashboard đã cập nhật

## 🚨 Lưu Ý Quan Trọng

1. **Luôn chạy thử trước** khi dọn dẹp dashboard
2. **Kiểm tra Grafana đang chạy** trước khi thực hiện
3. **Backup dashboard quan trọng** nếu cần
4. **Sử dụng script cập nhật** thay vì import trực tiếp

## 🔧 Troubleshooting

### Lỗi: "Không thể kết nối đến Grafana"
```bash
# Kiểm tra Grafana có đang chạy không
curl http://localhost:3000/api/health

# Khởi động Grafana nếu cần
docker-compose up -d grafana
```

### Lỗi: "Python không được cài đặt"
```bash
# Cài đặt Python từ python.org
# Hoặc sử dụng Anaconda/Miniconda
```

### Lỗi: "Không tìm thấy file dashboard"
```bash
# Kiểm tra đường dẫn file dashboard
# Đảm bảo chạy script từ thư mục gốc project
```

## 📈 Kết Quả Mong Đợi

Sau khi sử dụng script mới:
- ✅ **Không còn dashboard trùng lặp**
- ✅ **Dashboard được cập nhật** thay vì tạo mới
- ✅ **Quản lý dashboard dễ dàng** hơn
- ✅ **Tiết kiệm không gian** Grafana

## 🎉 Kết Luận

Bây giờ bạn có thể:
1. **Cập nhật dashboard** mà không lo tạo trùng lặp
2. **Dọn dẹp dashboard cũ** một cách an toàn
3. **Quản lý dashboard** hiệu quả hơn

Chỉ cần chạy `update-dashboards.bat` mỗi khi cần cập nhật dashboard!
