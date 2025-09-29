#!/usr/bin/env python3
"""
Script tạo dữ liệu liên tục cho dashboard - Top APIs by Request Rate
"""

import requests
import time
import random
import threading
from datetime import datetime

# API endpoints với các routes thực tế
APIS = {
    'user-api': {
        'base_url': 'http://localhost:8000',
        'endpoints': ['/api/users/', '/api/users/1/', '/api/users/2/']
    },
    'product-api': {
        'base_url': 'http://localhost:8001', 
        'endpoints': ['/api/products/', '/api/products/1/', '/api/products/2/']
    },
    'order-api': {
        'base_url': 'http://localhost:8002',
        'endpoints': ['/api/orders/', '/api/orders/1/', '/api/orders/2/']
    },
    'payment-api': {
        'base_url': 'http://localhost:8003',
        'endpoints': ['/api/payments/', '/api/payments/1/', '/api/payments/2/']
    }
}

def generate_traffic_for_api(api_name, config):
    """Tạo traffic cho một API cụ thể"""
    request_count = 0
    
    while True:
        try:
            # Chọn endpoint ngẫu nhiên
            endpoint = random.choice(config['endpoints'])
            url = f"{config['base_url']}{endpoint}"
            
            # Tạo request
            response = requests.get(url, timeout=5)
            request_count += 1
            
            if request_count % 10 == 0:
                print(f"📊 {api_name}: {request_count} requests - {response.status_code}")
            
            # Nghỉ ngẫu nhiên giữa requests (0.5-2 giây)
            time.sleep(random.uniform(0.5, 2.0))
            
        except Exception as e:
            print(f"❌ {api_name}: {str(e)}")
            time.sleep(1)

def main():
    """Chạy traffic generator cho tất cả APIs"""
    print("🚀 Dashboard Data Generator - Tạo dữ liệu cho Top APIs by Request Rate")
    print("=" * 70)
    print("💡 Dashboard: http://localhost:3000")
    print("🔑 Login: admin / admin123")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 70)
    
    # Tạo thread cho mỗi API
    threads = []
    
    for api_name, config in APIS.items():
        thread = threading.Thread(
            target=generate_traffic_for_api, 
            args=(api_name, config),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        print(f"✅ Đã khởi động traffic cho {api_name}")
    
    print(f"\n🎉 Đã khởi động {len(threads)} traffic generators!")
    print("📈 Dashboard sẽ có dữ liệu lên xuống liên tục!")
    print("🔗 Mở dashboard để xem: http://localhost:3000")
    print("\n🛑 Nhấn Ctrl+C để dừng tất cả...")
    
    try:
        # Giữ script chạy
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n🛑 Đang dừng tất cả traffic generators...")
        print("✅ Dashboard data generation hoàn thành!")

if __name__ == "__main__":
    main()
