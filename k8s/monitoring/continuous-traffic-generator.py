#!/usr/bin/env python3
"""
Script để tạo traffic liên tục cho các API services
Chạy trong background để dashboard có dữ liệu liên tục
"""

import requests
import time
import random
import threading
import signal
import sys
from datetime import datetime

# Cấu hình API endpoints
API_ENDPOINTS = {
    'user-api': {
        'base_url': 'http://localhost:8000',
        'endpoints': [
            '/api/users/',
            '/api/users/1/',
            '/api/users/2/',
            '/api/users/3/',
            '/api/users/4/',
            '/api/users/5/'
        ]
    },
    'product-api': {
        'base_url': 'http://localhost:8001',
        'endpoints': [
            '/api/products/',
            '/api/products/1/',
            '/api/products/2/',
            '/api/products/3/',
            '/api/products/4/',
            '/api/products/5/'
        ]
    },
    'order-api': {
        'base_url': 'http://localhost:8002',
        'endpoints': [
            '/api/orders/',
            '/api/orders/1/',
            '/api/orders/2/',
            '/api/orders/3/',
            '/api/orders/4/',
            '/api/orders/5/'
        ]
    },
    'payment-api': {
        'base_url': 'http://localhost:8003',
        'endpoints': [
            '/api/payments/',
            '/api/payments/1/',
            '/api/payments/2/',
            '/api/payments/3/',
            '/api/payments/4/',
            '/api/payments/5/'
        ]
    }
}

# Biến global để dừng traffic
stop_traffic = False
request_count = 0

def signal_handler(sig, frame):
    """Xử lý tín hiệu dừng"""
    global stop_traffic
    print(f"\n🛑 Nhận tín hiệu dừng...")
    stop_traffic = True

def make_request(api_name, base_url, endpoint):
    """Tạo một request đến API"""
    global request_count
    try:
        url = f"{base_url}{endpoint}"
        response = requests.get(url, timeout=5)
        request_count += 1
        
        if request_count % 50 == 0:  # Hiển thị mỗi 50 requests
            print(f"📊 Đã tạo {request_count} requests...")
        
        return True
    except Exception as e:
        return False

def generate_continuous_traffic():
    """Tạo traffic liên tục cho tất cả APIs"""
    global stop_traffic, request_count
    
    print("🚀 Bắt đầu tạo traffic liên tục...")
    print("💡 Nhấn Ctrl+C để dừng")
    print("🔗 Dashboard: http://localhost:3000")
    print("=" * 50)
    
    while not stop_traffic:
        # Tạo request cho mỗi API
        for api_name, config in API_ENDPOINTS.items():
            if stop_traffic:
                break
                
            # Chọn endpoint ngẫu nhiên
            endpoint = random.choice(config['endpoints'])
            
            # Tạo request
            make_request(api_name, config['base_url'], endpoint)
            
            # Nghỉ ngắn giữa các requests
            time.sleep(random.uniform(1, 2))
        
        # Nghỉ giữa các vòng lặp
        if not stop_traffic:
            time.sleep(random.uniform(5, 10))
    
    print(f"\n✅ Đã dừng traffic generator")
    print(f"📊 Tổng cộng: {request_count} requests")

def main():
    """Hàm chính"""
    global stop_traffic
    
    # Đăng ký signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Continuous Traffic Generator - Tạo traffic liên tục cho dashboard")
    print("=" * 70)
    print(f"⏰ Thời gian bắt đầu: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Kiểm tra kết nối
    print("🔍 Kiểm tra kết nối đến các APIs...")
    working_apis = []
    for api_name, config in API_ENDPOINTS.items():
        try:
            response = requests.get(f"{config['base_url']}/", timeout=5)
            if response.status_code in [200, 404, 405]:
                print(f"✅ {api_name}: Đang hoạt động")
                working_apis.append(api_name)
            else:
                print(f"⚠️ {api_name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {api_name}: {str(e)}")
    
    if not working_apis:
        print("\n❌ Không có API nào hoạt động!")
        return
    
    print(f"\n✅ Có {len(working_apis)} APIs đang hoạt động")
    print("🚀 Bắt đầu tạo traffic liên tục...")
    print("💡 Dashboard sẽ có dữ liệu real-time!")
    print("🛑 Nhấn Ctrl+C để dừng")
    print()
    
    # Bắt đầu tạo traffic
    try:
        generate_continuous_traffic()
    except KeyboardInterrupt:
        print(f"\n🛑 Dừng traffic generator...")
        stop_traffic = True
    
    print(f"\n🎉 Hoàn thành! Đã tạo {request_count} requests")
    print("📊 Dashboard bây giờ sẽ có dữ liệu!")

if __name__ == "__main__":
    main()
