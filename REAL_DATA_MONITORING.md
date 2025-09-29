# 📊 Real Data Monitoring Setup

## 🎯 Mục tiêu
Cập nhật Grafana dashboard để hiển thị **dữ liệu thật** từ các API thay vì dữ liệu random/simulated.

## 🔧 Những thay đổi đã thực hiện

### 1. Cập nhật Middleware (Real System Metrics)
- **File**: `api1/users/middleware.py`, `api2/products/middleware.py`, `api3/orders/middleware.py`, `api4/payments/middleware.py`
- **Thay đổi**: 
  - Thay thế dữ liệu simulated bằng dữ liệu thật từ `psutil`
  - Thêm function `_update_system_metrics()` để lấy dữ liệu thật
  - Memory usage, CPU usage, file descriptors đều là dữ liệu thật

### 2. Cập nhật Requirements
- **File**: `api2/requirements.txt`, `api3/requirements.txt`, `api4/requirements.txt`
- **Thêm**: `psutil==5.9.0` để thu thập system metrics thật

### 3. Cập nhật Prometheus Configuration
- **File**: `monitoring/prometheus.yml`
- **Thay đổi**:
  - Tăng scrape_interval từ 1s lên 5s (tối ưu hơn)
  - Thêm scrape_timeout: 3s
  - Cải thiện reliability

### 4. Cập nhật Grafana Dashboard
- **File**: `monitoring/grafana/dashboards/custom_api_dashboard.json`
- **Thay đổi**:
  - Sửa title các panels cho rõ ràng hơn
  - Thêm panel "API Success Rate" mới
  - Cải thiện layout và thông tin hiển thị

## 🚀 Cách sử dụng

### 1. Khởi động hệ thống
```bash
# Khởi động tất cả services
docker-compose up -d

# Kiểm tra status
docker-compose ps
```

### 2. Tạo dữ liệu thật
```bash
# Chạy script tạo load test
python test_api_data.py
```

### 3. Kiểm tra metrics
```bash
# Kiểm tra metrics endpoints
python check_metrics.py
```

### 4. Xem dashboard
- Truy cập Grafana: http://localhost:3000
- Dashboard: "Custom API Dashboard - 4 Services Real Data"
- Tất cả dữ liệu hiển thị sẽ là dữ liệu thật từ hệ thống

## 📈 Metrics được thu thập

### HTTP Request Metrics (Thật)
- `django_http_requests_total`: Số lượng requests thật
- `django_http_request_duration_seconds`: Thời gian response thật
- Status codes: 200, 404, 500, etc. (thật)

### System Metrics (Thật)
- `process_resident_memory_bytes`: Memory usage thật từ psutil
- `process_cpu_seconds_total`: CPU usage thật từ psutil  
- `process_open_fds`: File descriptors thật từ psutil

### API Health (Thật)
- `up`: Service status thật
- Request rates: Thật từ middleware
- Error rates: Thật từ HTTP responses

## 🎯 Kết quả mong đợi

1. **Dữ liệu thật**: Không còn random/simulated data
2. **Real-time monitoring**: Dashboard cập nhật theo dữ liệu thật
3. **Accurate metrics**: CPU, Memory, Request rates đều chính xác
4. **Performance insights**: Hiểu được performance thật của hệ thống

## 🔍 Troubleshooting

### Nếu không thấy dữ liệu:
1. Kiểm tra containers đang chạy: `docker-compose ps`
2. Kiểm tra metrics endpoints: `curl http://localhost:8000/metrics`
3. Kiểm tra Prometheus: http://localhost:9090
4. Kiểm tra Grafana: http://localhost:3000

### Nếu có lỗi psutil:
- Đảm bảo đã cài đặt psutil trong requirements.txt
- Restart containers sau khi cập nhật requirements

## 📊 Dashboard Features

- **Real-time data**: Cập nhật mỗi 5 giây
- **Accurate metrics**: Dữ liệu thật từ hệ thống
- **Performance monitoring**: CPU, Memory, Request rates
- **Error tracking**: 4xx, 5xx errors thật
- **API health**: Service status thật
