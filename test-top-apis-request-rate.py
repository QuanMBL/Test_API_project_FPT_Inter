#!/usr/bin/env python3
"""
Script test phần "Top APIs by Request Rate" trong dashboard
Tạo traffic và kiểm tra dữ liệu hiển thị
"""

import requests
import time
import random
import json
from datetime import datetime

def test_prometheus_rate_query():
    """Test query rate trực tiếp"""
    print("🔍 Testing Top APIs by Request Rate query...")
    
    query = "topk(5, sum(rate(django_http_requests_total[1m])) by (job))"
    url = f"http://localhost:9090/api/v1/query?query={query}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'success' and data['data']['result']:
            print(f"✅ Query có dữ liệu: {len(data['data']['result'])} APIs")
            for result in data['data']['result']:
                job = result['metric']['job']
                rate = result['value'][1]
                print(f"   📊 {job}: {rate} requests/sec")
        else:
            print("❌ Query không có dữ liệu")
            
    except Exception as e:
        print(f"❌ Lỗi query: {str(e)}")

def generate_traffic_for_top_apis():
    """Tạo traffic để test Top APIs"""
    print("🚀 Tạo traffic cho Top APIs by Request Rate...")
    
    # APIs với tần suất khác nhau để tạo ranking
    apis = {
        'user-api': {
            'url': 'http://localhost:8000/api/users/',
            'weight': 4  # Nhiều requests nhất
        },
        'product-api': {
            'url': 'http://localhost:8001/api/products/',
            'weight': 3  # Trung bình
        },
        'order-api': {
            'url': 'http://localhost:8002/api/orders/',
            'weight': 2  # Ít hơn
        },
        'payment-api': {
            'url': 'http://localhost:8003/api/payments/',
            'weight': 1  # Ít nhất
        }
    }
    
    print("📊 Tạo traffic với tần suất khác nhau:")
    print("   🥇 user-api: 4x requests")
    print("   🥈 product-api: 3x requests") 
    print("   🥉 order-api: 2x requests")
    print("   🏅 payment-api: 1x requests")
    print()
    
    for round_num in range(50):  # 50 rounds
        for api_name, config in apis.items():
            # Tạo requests theo weight
            for _ in range(config['weight']):
                try:
                    response = requests.get(config['url'], timeout=2)
                    print(f"📈 {api_name}: {response.status_code}")
                except Exception as e:
                    print(f"❌ {api_name}: {str(e)}")
                
                time.sleep(0.1)  # Nghỉ ngắn
        
        if round_num % 10 == 0:
            print(f"🔄 Completed {round_num+1}/50 rounds...")
            # Test query sau mỗi 10 rounds
            test_prometheus_rate_query()
            print()

def main():
    print("🚀 Top APIs by Request Rate Tester")
    print("=" * 50)
    print("💡 Mục tiêu: Tạo ranking APIs theo request rate")
    print("🔗 Dashboard: http://localhost:3000")
    print("🔑 Login: admin / admin123")
    print("=" * 50)
    
    # Test query trước
    print("1️⃣ Testing query trước khi tạo traffic...")
    test_prometheus_rate_query()
    print()
    
    # Tạo traffic
    print("2️⃣ Tạo traffic với tần suất khác nhau...")
    generate_traffic_for_top_apis()
    
    # Test query sau
    print("3️⃣ Testing query sau khi tạo traffic...")
    test_prometheus_rate_query()
    
    print("\n✅ Test hoàn thành!")
    print("📊 Kiểm tra dashboard:")
    print("   🔗 http://localhost:3000")
    print("   📈 Xem 'Top APIs by Request Rate'")
    print("   🥇 user-api sẽ có rate cao nhất")
    print("   🥈 product-api sẽ có rate thứ 2")
    print("   🥉 order-api sẽ có rate thứ 3")
    print("   🏅 payment-api sẽ có rate thấp nhất")

if __name__ == "__main__":
    main()
