#!/usr/bin/env python3
"""
FINAL FIX - Tạo dữ liệu thực sự cho Top APIs by Request Rate
"""

import requests
import time
import threading
import json

def test_query():
    """Test query trực tiếp"""
    query = "sum(rate(django_http_requests_total[5m])) by (job)"
    url = f"http://localhost:9090/api/v1/query?query={query}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'success' and data['data']['result']:
            print("✅ Query có dữ liệu:")
            for result in data['data']['result']:
                job = result['metric']['job']
                rate = result['value'][1]
                print(f"   📊 {job}: {rate} requests/sec")
        else:
            print("❌ Query không có dữ liệu")
    except Exception as e:
        print(f"❌ Lỗi query: {str(e)}")

def create_heavy_traffic():
    """Tạo traffic mạnh"""
    apis = [
        'http://localhost:8000/api/users/',
        'http://localhost:8001/api/products/',
        'http://localhost:8002/api/orders/',
        'http://localhost:8003/api/payments/'
    ]
    
    count = 0
    while True:
        for api in apis:
            try:
                response = requests.get(api, timeout=1)
                count += 1
                if count % 50 == 0:
                    print(f"📊 Đã tạo {count} requests")
                    test_query()
            except:
                pass
        
        time.sleep(0.2)  # Nghỉ 0.2 giây

def main():
    print("🔧 FINAL FIX - Top APIs by Request Rate")
    print("=" * 50)
    print("🚀 Tạo traffic mạnh để có dữ liệu...")
    print("💡 Dashboard: http://localhost:3000")
    print("🔑 Login: admin / admin123")
    print("📊 Xem 'Top APIs by Request Rate'")
    print("⏰ Đợi 1-2 phút để có dữ liệu")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 50)
    
    # Test query trước
    print("1️⃣ Testing query trước...")
    test_query()
    print()
    
    # Tạo traffic
    print("2️⃣ Tạo traffic mạnh...")
    try:
        create_heavy_traffic()
    except KeyboardInterrupt:
        print("\n✅ Traffic generation hoàn thành!")
        print("📊 Dashboard bây giờ sẽ có dữ liệu!")

if __name__ == "__main__":
    main()
