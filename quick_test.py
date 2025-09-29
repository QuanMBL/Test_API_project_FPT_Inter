#!/usr/bin/env python3
"""
Script nhanh để test API và tạo dữ liệu thật
"""

import requests
import time
import random

def test_api():
    """Test một API và tạo dữ liệu thật"""
    apis = [
        'http://localhost:8000',  # user-api
        'http://localhost:8001',  # product-api  
        'http://localhost:8002',  # order-api
        'http://localhost:8003'   # payment-api
    ]
    
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    endpoints = ['/', '/users/', '/products/', '/orders/', '/payments/']
    
    print("🚀 Bắt đầu test API...")
    
    for i in range(20):  # 20 requests
        try:
            api = random.choice(apis)
            method = random.choice(methods)
            endpoint = random.choice(endpoints)
            url = f"{api}{endpoint}"
            
            print(f"📡 {method} {url}")
            
            if method == 'GET':
                response = requests.get(url, timeout=3)
            elif method == 'POST':
                response = requests.post(url, json={'name': f'test_{i}'}, timeout=3)
            elif method == 'PUT':
                response = requests.put(url, json={'name': f'test_{i}'}, timeout=3)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=3)
            
            print(f"  ✅ {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        time.sleep(0.5)  # Nghỉ 0.5 giây
    
    print("✅ Hoàn thành test!")

if __name__ == "__main__":
    test_api()
