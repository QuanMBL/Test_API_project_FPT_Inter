# MongoDB Setup Guide

Hướng dẫn kết nối 4 API với MongoDB.

## 🚀 Các thay đổi đã thực hiện

### 1. Dependencies
- Thêm `djongo==1.3.6` và `pymongo==4.6.0` vào tất cả `requirements.txt`

### 2. Database Configuration
- Cập nhật `settings.py` cho tất cả APIs để sử dụng MongoDB thay vì SQLite
- Sử dụng environment variables cho MongoDB host và port

### 3. Models Optimization
- Thêm indexes cho MongoDB để tối ưu hóa performance
- Các models hiện tại tương thích với MongoDB

### 4. Docker Configuration
- Thêm MongoDB service vào `docker-compose.yml`
- Cấu hình persistent volume cho MongoDB data
- Thêm dependencies cho tất cả API services

### 5. Kubernetes Configuration
- Tạo `mongodb-deployment.yaml` với PersistentVolumeClaim
- Cập nhật tất cả API deployments với MongoDB environment variables

## 🐳 Chạy với Docker Compose

```bash
# Build và start tất cả services
docker-compose up --build

# Chạy trong background
docker-compose up -d --build

# Xem logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☸️ Chạy với Kubernetes

```bash
# Deploy MongoDB trước
kubectl apply -f k8s/mongodb-deployment.yaml

# Deploy các APIs
kubectl apply -f k8s/user-api-deployment.yaml
kubectl apply -f k8s/product-api-deployment.yaml
kubectl apply -f k8s/order-api-deployment.yaml
kubectl apply -f k8s/payment-api-deployment.yaml

# Kiểm tra status
kubectl get pods
kubectl get services
```

## 📦 Install Dependencies

Trước khi test, cần cài đặt dependencies:

```bash
# Cài đặt dependencies toàn cục
python install-global-deps.py

# Hoặc cài đặt cho từng API
python install-dependencies.py
```

## 🧪 Test MongoDB Connection

```bash
# Kiểm tra trạng thái MongoDB
python check-mongodb.py

# Khởi động MongoDB và test
python start-mongodb.py

# Test kết nối MongoDB đơn giản (không cần Django)
python test-mongodb-simple.py

# Test kết nối MongoDB với localhost
python test-local-mongodb.py

# Test kết nối MongoDB cho tất cả APIs
python test-mongodb-connection.py

# Test kết nối cho một API cụ thể
python test-single-api.py userapi
```

## 📊 Database Information

### MongoDB Databases
- `userapi_db` - User API database
- `productapi_db` - Product API database  
- `orderapi_db` - Order API database
- `paymentapi_db` - Payment API database

### MongoDB Connection
- **Host**: `mongodb` (Docker) / `mongodb-service` (Kubernetes)
- **Port**: `27017`
- **Username**: `admin`
- **Password**: `password123`

## 🔧 Environment Variables

Các APIs sử dụng các environment variables sau:

```bash
MONGODB_HOST=mongodb  # hoặc mongodb-service cho Kubernetes
MONGODB_PORT=27017
```

## 📝 API Endpoints

Sau khi deploy, các APIs sẽ có sẵn tại:

- **User API**: http://localhost:8000
- **Product API**: http://localhost:8001  
- **Order API**: http://localhost:8002
- **Payment API**: http://localhost:8003

## 🗄️ MongoDB Collections

Mỗi API sẽ tạo các collections tương ứng:
- `users_user` - User data
- `products_product` - Product data
- `orders_order` - Order data
- `payments_payment` - Payment data

## 🔍 Monitoring

```bash
# Kiểm tra MongoDB logs
docker-compose logs mongodb

# Kết nối trực tiếp vào MongoDB
docker exec -it mongodb-container mongosh

# Trong MongoDB shell
use userapi_db
show collections
db.users_user.find()
```

## ⚠️ Lưu ý quan trọng

1. **Data Migration**: Dữ liệu SQLite hiện tại sẽ không tự động migrate sang MongoDB
2. **Indexes**: Các indexes đã được cấu hình để tối ưu hóa performance
3. **Backup**: Cần backup dữ liệu MongoDB thường xuyên
4. **Security**: Trong production, cần cấu hình authentication và authorization cho MongoDB

## 🚨 Troubleshooting

### Lỗi kết nối MongoDB
```bash
# Kiểm tra MongoDB container
docker-compose ps mongodb

# Restart MongoDB
docker-compose restart mongodb

# Xem MongoDB logs
docker-compose logs mongodb
```

### Lỗi API không kết nối được MongoDB
```bash
# Kiểm tra network
docker network ls
docker network inspect test_api_02_api-network

# Test kết nối từ API container
docker exec -it user-api-container ping mongodb
```
