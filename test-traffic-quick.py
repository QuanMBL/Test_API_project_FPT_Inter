#!/usr/bin/env python3
"""
Script nhanh để test traffic và kiểm tra dashboard
"""

import requests
import time
import random
from datetime import datetime

# API endpoints
APIS = {
    'user-api': 'http://localhost:8000',
    'product-api': 'http://localhost:8001', 
    'order-api': 'http://localhost:8002',
    'payment-api': 'http://localhost:8003'
}

def test_api_traffic():
    """Test traffic cho tất cả APIs"""
    print("🚀 Bắt đầu test traffic...")
    print("=" * 50)
    
    for i in range(20):  # Tạo 20 requests cho mỗi API
        for api_name, base_url in APIS.items():
            try:
                # Test các endpoints khác nhau
                endpoints = ['/', '/api/', '/api/users/', '/api/products/', '/api/orders/', '/api/payments/']
                endpoint = random.choice(endpoints)
                url = f"{base_url}{endpoint}"
                
                response = requests.get(url, timeout=3)
                print(f"✅ {api_name}: {response.status_code} - {url}")
                
            except Exception as e:
                print(f"❌ {api_name}: {str(e)}")
            
            # Nghỉ ngắn giữa requests
            time.sleep(random.uniform(0.5, 1.5))
    
    print("\n🎉 Test traffic hoàn thành!")
    print("📊 Kiểm tra dashboard: http://localhost:3000")
    print("🔑 Login: admin / admin123")

if __name__ == "__main__":
    test_api_traffic()
