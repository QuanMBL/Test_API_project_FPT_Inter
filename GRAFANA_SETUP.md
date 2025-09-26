# Grafana Monitoring Setup

## Tổng quan
Dự án này đã được tích hợp với Grafana và Prometheus để monitoring các API services.

## Kiến trúc Monitoring

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Grafana   │◄───│ Prometheus  │◄───│   APIs      │
│  (Port 3000)│    │ (Port 9090) │    │ (8000-8003) │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Services được monitoring

1. **User API** (Port 8000) - http://localhost:8000/metrics
2. **Product API** (Port 8001) - http://localhost:8001/metrics
3. **Order API** (Port 8002) - http://localhost:8002/metrics
4. **Payment API** (Port 8003) - http://localhost:8003/metrics
5. **MongoDB** (Port 27017)

## Khởi động Monitoring

### Windows (PowerShell)
```powershell
.\start-monitoring.ps1
```

### Linux/Mac (Bash)
```bash
./start-monitoring.sh
```

### Thủ công
```bash
# Chỉ khởi động monitoring
docker-compose up -d prometheus grafana

# Hoặc khởi động tất cả services
docker-compose up -d
```

## Truy cập các services

### Grafana Dashboard
- **URL**: http://localhost:3000
- **Username**: admin
- **Password**: admin123

### Prometheus
- **URL**: http://localhost:9090

## Metrics được thu thập

### Django Metrics
- `django_http_requests_total` - Tổng số HTTP requests
- `django_http_request_duration_seconds` - Thời gian xử lý requests
- `django_db_connections` - Số kết nối database
- `django_cache_operations_total` - Số operations cache

### System Metrics
- `process_resident_memory_bytes` - Memory usage
- `process_cpu_seconds_total` - CPU usage
- `process_open_fds` - File descriptors

## Dashboard có sẵn

### API Services Monitoring Dashboard
- HTTP Request Rate
- HTTP Response Time
- HTTP Status Codes
- API Endpoints Performance
- Database Connections
- Memory Usage

## Cấu hình

### Prometheus Configuration
File: `monitoring/prometheus.yml`
- Scrape interval: 15s
- API metrics path: `/metrics`
- Retention time: 200h

### Grafana Configuration
- Datasource: Prometheus (http://prometheus:9090)
- Dashboard provisioning: `monitoring/grafana/provisioning/`
- Custom dashboards: `monitoring/grafana/dashboards/`

## Troubleshooting

### Kiểm tra services
```bash
docker-compose ps
```

### Xem logs
```bash
# Grafana logs
docker-compose logs grafana

# Prometheus logs
docker-compose logs prometheus

# API logs
docker-compose logs user-api
docker-compose logs product-api
docker-compose logs order-api
docker-compose logs payment-api
```

### Kiểm tra metrics endpoints
```bash
# Test metrics endpoint
curl http://localhost:8000/metrics
curl http://localhost:8001/metrics
curl http://localhost:8002/metrics
curl http://localhost:8003/metrics
```

### Restart services
```bash
# Restart monitoring only
docker-compose restart prometheus grafana

# Restart all services
docker-compose restart
```

## Thêm Dashboard mới

1. Tạo file JSON dashboard trong `monitoring/grafana/dashboards/`
2. Restart Grafana container
3. Dashboard sẽ tự động được load

## Custom Metrics

Để thêm custom metrics trong Django:

```python
from django_prometheus.models import Counter, Histogram

# Custom counter
custom_counter = Counter('my_app_custom_total', 'Custom counter')

# Custom histogram
custom_histogram = Histogram('my_app_duration_seconds', 'Custom timing')

# Sử dụng
custom_counter.inc()
custom_histogram.observe(0.5)
```

## Performance Tuning

### Prometheus
- Tăng `scrape_interval` nếu có quá nhiều metrics
- Điều chỉnh `retention.time` theo nhu cầu lưu trữ

### Grafana
- Tăng refresh interval cho dashboard nếu không cần real-time
- Sử dụng query optimization trong Prometheus

## Security Notes

- Đổi default password của Grafana trong production
- Sử dụng HTTPS cho production environment
- Cấu hình firewall để bảo vệ ports 3000 và 9090
