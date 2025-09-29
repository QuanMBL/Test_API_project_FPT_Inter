# Dashboard all_4api_1 - Tổng quan 4 API Services

## 📊 Tổng quan

Dashboard `all_4api_1` cung cấp cái nhìn tổng quan về hiệu suất và trạng thái của 4 API services trong hệ thống microservices của bạn.

## 🎯 Tính năng Dashboard

### 📈 Các Metrics Chính

#### 1. **Tổng số Services đang hoạt động**
- **Mô tả**: Hiển thị số lượng services đang hoạt động (tối đa 4)
- **Màu sắc**: 
  - 🟢 Xanh: 4/4 services hoạt động
  - 🔴 Đỏ: Có services bị lỗi
- **Công thức**: `sum(up{job=~"user-api|product-api|order-api|payment-api"})`

#### 2. **CPU Usage trung bình**
- **Mô tả**: CPU sử dụng trung bình của tất cả services
- **Đơn vị**: Phần trăm (%)
- **Ngưỡng cảnh báo**:
  - 🟢 Xanh: < 70%
  - 🟡 Vàng: 70-85%
  - 🔴 Đỏ: > 85%

#### 3. **Tổng Memory Usage**
- **Mô tả**: Tổng bộ nhớ RAM được sử dụng bởi tất cả services
- **Đơn vị**: Bytes (tự động chuyển đổi thành MB/GB)
- **Ngưỡng cảnh báo**:
  - 🟢 Xanh: < 100MB
  - 🟡 Vàng: 100-200MB
  - 🔴 Đỏ: > 200MB

#### 4. **Tỷ lệ lỗi trung bình**
- **Mô tả**: Tỷ lệ phần trăm các request bị lỗi (4xx, 5xx)
- **Đơn vị**: Phần trăm (%)
- **Ngưỡng cảnh báo**:
  - 🟢 Xanh: < 5%
  - 🟡 Vàng: 5-10%
  - 🔴 Đỏ: > 10%

### 📊 Biểu đồ Chi tiết

#### 1. **CPU Usage theo từng Service**
- **Mô tả**: Biểu đồ đường hiển thị CPU usage của từng service theo thời gian
- **Services**: User API, Product API, Order API, Payment API
- **Cập nhật**: Mỗi 5 giây

#### 2. **Memory Usage theo từng Service**
- **Mô tả**: Biểu đồ đường hiển thị memory usage của từng service
- **Đơn vị**: Bytes
- **Màu sắc**: Mỗi service có màu riêng biệt

#### 3. **Response Time theo từng Service**
- **Mô tả**: Thời gian phản hồi trung bình của từng service
- **Đơn vị**: Giây (s)
- **Ngưỡng cảnh báo**:
  - 🟢 Xanh: < 0.5s
  - 🟡 Vàng: 0.5-1.0s
  - 🔴 Đỏ: > 1.0s

#### 4. **Error Rate theo từng Service**
- **Mô tả**: Tỷ lệ lỗi của từng service theo thời gian
- **Đơn vị**: Phần trăm (%)
- **Màu sắc**: Mỗi service có màu riêng

#### 5. **Request Rate theo từng Service**
- **Mô tả**: Số lượng request mỗi giây của từng service
- **Đơn vị**: Requests per second (reqps)
- **Hiển thị**: Xu hướng traffic theo thời gian

#### 6. **HTTP Methods theo từng Service**
- **Mô tả**: Phân tích các phương thức HTTP (GET, POST) của từng service
- **Mục đích**: Hiểu rõ loại traffic và pattern sử dụng
- **Hiển thị**: Tổng số request theo method

## 🚀 Cách Sử dụng

### Import Dashboard

#### Phương pháp 1: PowerShell (Windows)
```powershell
.\import-all-4api-1-dashboard.ps1
```

#### Phương pháp 2: Python Script
```bash
python k8s/monitoring/import-all-4api-1-dashboard.py
```

#### Phương pháp 3: Import Thủ công
1. Mở Grafana tại `http://localhost:3000`
2. Đăng nhập với `admin` / `admin123`
3. Vào **Dashboards** → **Import**
4. Upload file `monitoring/grafana/dashboards/all_4api_1_dashboard.json`

### Truy cập Dashboard
- **URL**: `http://localhost:3000/d/all_4api_1`
- **Tên**: all_4api_1 - Dashboard tổng quan 4 API Services
- **Refresh**: Tự động mỗi 5 giây

## 📋 Giải thích Metrics

### CPU Usage
- **Ý nghĩa**: Phần trăm CPU được sử dụng bởi mỗi service
- **Công thức**: `rate(process_cpu_seconds_total[5m]) * 100`
- **Giám sát**: Quan trọng để phát hiện bottleneck

### Memory Usage
- **Ý nghĩa**: Bộ nhớ RAM được sử dụng bởi mỗi service
- **Công thức**: `process_resident_memory_bytes`
- **Giám sát**: Phát hiện memory leak hoặc sử dụng quá mức

### Response Time
- **Ý nghĩa**: Thời gian trung bình để xử lý một request
- **Công thức**: `avg(django_http_request_duration_seconds_sum / django_http_request_duration_seconds_count)`
- **Giám sát**: Đảm bảo hiệu suất tốt cho người dùng

### Error Rate
- **Ý nghĩa**: Tỷ lệ request bị lỗi (4xx, 5xx)
- **Công thức**: `sum(rate(django_http_requests_total{status=~"4..|5.."}[5m])) / sum(rate(django_http_requests_total[5m])) * 100`
- **Giám sát**: Phát hiện sớm các vấn đề trong hệ thống

### Request Rate
- **Ý nghĩa**: Số lượng request mỗi giây
- **Công thức**: `rate(django_http_requests_total[5m])`
- **Giám sát**: Hiểu rõ traffic pattern và load

## 🎨 Tính năng Giao diện

### Màu sắc
- **🟢 Xanh**: Trạng thái tốt, hoạt động bình thường
- **🟡 Vàng**: Cảnh báo, cần theo dõi
- **🔴 Đỏ**: Nguy hiểm, cần xử lý ngay

### Tự động cập nhật
- **Refresh Rate**: 5 giây
- **Time Range**: 1 giờ qua (có thể điều chỉnh)
- **Timezone**: Theo múi giờ trình duyệt

### Responsive Design
- **Layout**: Tự động điều chỉnh theo kích thước màn hình
- **Panels**: Có thể di chuyển và thay đổi kích thước
- **Dark Theme**: Giao diện tối dễ nhìn

## 🔧 Cấu hình

### Prometheus Queries
```promql
# CPU Usage
rate(process_cpu_seconds_total{job="service-name"}[5m]) * 100

# Memory Usage
process_resident_memory_bytes{job="service-name"}

# Request Rate
rate(django_http_requests_total{job="service-name"}[5m])

# Response Time
avg(django_http_request_duration_seconds_sum{job="service-name"} / django_http_request_duration_seconds_count{job="service-name"})

# Error Rate
sum(rate(django_http_requests_total{job="service-name",status=~"4..|5.."}[5m])) / sum(rate(django_http_requests_total{job="service-name"}[5m])) * 100
```

### Service Names
- `user-api`: User Management API
- `product-api`: Product Catalog API
- `order-api`: Order Processing API
- `payment-api`: Payment Processing API

## 🚨 Cảnh báo Khuyến nghị

### CPU Alerts
- **Cảnh báo**: CPU > 70% trong 5 phút
- **Nguy hiểm**: CPU > 85% trong 2 phút

### Memory Alerts
- **Cảnh báo**: Memory > 100MB trong 5 phút
- **Nguy hiểm**: Memory > 200MB trong 2 phút

### Response Time Alerts
- **Cảnh báo**: Response time > 0.5s trong 5 phút
- **Nguy hiểm**: Response time > 1.0s trong 2 phút

### Error Rate Alerts
- **Cảnh báo**: Error rate > 5% trong 5 phút
- **Nguy hiểm**: Error rate > 10% trong 2 phút

## 🔍 Xử lý Sự cố

### Không có dữ liệu
1. Kiểm tra Prometheus có đang chạy không
2. Xác minh các service metrics endpoints
3. Kiểm tra cấu hình service discovery

### Dashboard không load
1. Xác minh Grafana đang chạy trên port 3000
2. Kiểm tra thông tin đăng nhập
3. Đảm bảo file JSON hợp lệ

### Metrics bị thiếu
1. Xác minh services đang expose metrics trên `/metrics`
2. Kiểm tra Prometheus targets đang UP
3. Xác minh tên metrics khớp với queries

## 📈 Tối ưu Hiệu suất

### Dashboard Performance
- **Refresh Rate**: 5 giây (có thể điều chỉnh)
- **Time Range**: 1 giờ (có thể mở rộng)
- **Query Optimization**: Sử dụng time range phù hợp

### Resource Usage
- **CPU**: Giám sát CPU usage của dashboard
- **Memory**: Kiểm tra memory consumption của Grafana
- **Network**: Giám sát data transfer rates

## 🔄 Bảo trì

### Công việc Thường xuyên
1. **Hàng tuần**: Xem xét hiệu suất dashboard
2. **Hàng tháng**: Cập nhật thresholds dựa trên usage patterns
3. **Hàng quý**: Xem xét và tối ưu queries

### Cập nhật
- **Dashboard version**: 1.0
- **Tương thích**: Grafana 8.0+
- **Yêu cầu**: Prometheus metrics

## 📞 Hỗ trợ

Để giải quyết vấn đề:
1. Kiểm tra phần xử lý sự cố
2. Xác minh tất cả prerequisites
3. Xem lại logs của Prometheus và Grafana
4. Test các metric queries riêng lẻ

---

**Dashboard Version**: 1.0  
**Cập nhật lần cuối**: $(Get-Date -Format "yyyy-MM-dd")  
**Tương thích**: Grafana 8.0+, Prometheus 2.0+
