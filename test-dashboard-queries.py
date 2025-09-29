#!/usr/bin/env python3
"""
Script test queries của dashboard và tạo traffic mạnh hơn
"""

import requests
import time
import random
import json

def test_prometheus_query():
    """Test query trực tiếp với Prometheus"""
    print("🔍 Testing Prometheus queries...")
    
    queries = [
        "django_http_requests_total",
        "sum(rate(django_http_requests_total[1m])) by (job)",
        "topk(5, sum(rate(django_http_requests_total[1m])) by (job))",
        "up{job=~\"user-api|product-api|order-api|payment-api\"}"
    ]
    
    for query in queries:
        try:
            url = f"http://localhost:9090/api/v1/query?query={query}"
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == 'success' and data['data']['result']:
                print(f"✅ {query}: {len(data['data']['result'])} results")
                for result in data['data']['result'][:3]:  # Show first 3 results
                    print(f"   - {result['metric']}: {result['value']}")
            else:
                print(f"❌ {query}: No data")
                
        except Exception as e:
            print(f"❌ {query}: Error - {str(e)}")
        
        print()

def generate_heavy_traffic():
    """Tạo traffic mạnh hơn để có dữ liệu rõ ràng"""
    print("🚀 Generating heavy traffic...")
    
    apis = [
        'http://localhost:8000/api/users/',
        'http://localhost:8001/api/products/', 
        'http://localhost:8002/api/orders/',
        'http://localhost:8003/api/payments/'
    ]
    
    for i in range(100):  # 100 requests
        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=2)
                print(f"📊 {api_url}: {response.status_code}")
            except Exception as e:
                print(f"❌ {api_url}: {str(e)}")
            
            # Nghỉ ngắn
            time.sleep(0.1)
        
        if i % 20 == 0:
            print(f"🔄 Completed {i+1}/100 rounds...")
            time.sleep(1)

def main():
    print("🚀 Dashboard Query Tester")
    print("=" * 50)
    
    # Test queries trước
    test_prometheus_query()
    
    print("🚀 Generating heavy traffic...")
    generate_heavy_traffic()
    
    print("\n🔍 Testing queries after traffic...")
    test_prometheus_query()
    
    print("✅ Test completed!")
    print("🔗 Check dashboard: http://localhost:3000")
    print("🔑 Login: admin / admin123")

if __name__ == "__main__":
    main()
