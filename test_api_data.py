#!/usr/bin/env python3
"""
Script để test các API và tạo dữ liệu thật cho monitoring
"""

import requests
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor

# API endpoints
APIS = {
    'user-api': 'http://localhost:8000',
    'product-api': 'http://localhost:8001', 
    'order-api': 'http://localhost:8002',
    'payment-api': 'http://localhost:8003'
}

def make_request(api_name, base_url):
    """Tạo request đến API và trả về kết quả"""
    try:
        # Random endpoint selection
        endpoints = [
            '/',  # Health check
            '/users/',  # User endpoints
            '/products/',  # Product endpoints  
            '/orders/',  # Order endpoints
            '/payments/',  # Payment endpoints
        ]
        
        endpoint = random.choice(endpoints)
        url = f"{base_url}{endpoint}"
        
        # Random HTTP method
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        method = random.choice(methods)
        
        # Random data for POST/PUT
        data = {}
        if method in ['POST', 'PUT']:
            data = {
                'name': f'test_{random.randint(1, 1000)}',
                'description': f'Test data {random.randint(1, 1000)}'
            }
        
        # Make request
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=data, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=5)
            
        return {
            'api': api_name,
            'method': method,
            'endpoint': endpoint,
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'success': 200 <= response.status_code < 300
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'api': api_name,
            'method': method if 'method' in locals() else 'UNKNOWN',
            'endpoint': endpoint if 'endpoint' in locals() else '/',
            'status_code': 0,
            'response_time': 0,
            'success': False,
            'error': str(e)
        }

def generate_load():
    """Tạo load test cho các API"""
    print("🚀 Bắt đầu tạo dữ liệu thật cho monitoring...")
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        while True:
            # Tạo batch requests
            futures = []
            for api_name, base_url in APIS.items():
                # Tạo 5-10 requests mỗi API
                for _ in range(random.randint(5, 10)):
                    future = executor.submit(make_request, api_name, base_url)
                    futures.append(future)
            
            # Chờ tất cả requests hoàn thành
            results = []
            for future in futures:
                try:
                    result = future.result(timeout=10)
                    results.append(result)
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            # Log kết quả
            success_count = sum(1 for r in results if r['success'])
            total_count = len(results)
            print(f"📊 Batch completed: {success_count}/{total_count} successful requests")
            
            # Hiển thị chi tiết một số requests
            for result in results[:3]:  # Chỉ hiển thị 3 requests đầu
                status_emoji = "✅" if result['success'] else "❌"
                print(f"  {status_emoji} {result['api']} {result['method']} {result['endpoint']} -> {result['status_code']} ({result['response_time']:.3f}s)")
            
            # Nghỉ một chút trước batch tiếp theo
            time.sleep(random.uniform(2, 5))

if __name__ == "__main__":
    try:
        generate_load()
    except KeyboardInterrupt:
        print("\n🛑 Stopping load generation...")
    except Exception as e:
        print(f"❌ Error: {e}")
