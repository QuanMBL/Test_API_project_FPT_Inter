#!/usr/bin/env python3
"""
Script để tạo CPU load thật cho testing
"""

import requests
import time
import threading
import random

def cpu_intensive_request(api_url):
    """Tạo request có CPU intensive"""
    try:
        # Tạo request với data lớn để tăng CPU usage
        large_data = {
            'name': 'test_' + 'x' * 1000,  # Data lớn
            'description': 'CPU test ' + 'y' * 2000,  # Data rất lớn
            'items': [{'id': i, 'value': f'item_{i}' * 100} for i in range(100)]  # Array lớn
        }
        
        # POST request với data lớn
        response = requests.post(f"{api_url}/", json=large_data, timeout=10)
        return response.status_code
    except Exception as e:
        return f"Error: {e}"

def create_cpu_load():
    """Tạo CPU load cho tất cả APIs"""
    apis = [
        'http://localhost:8000',  # user-api
        'http://localhost:8001',  # product-api  
        'http://localhost:8002',  # order-api
        'http://localhost:8003'   # payment-api
    ]
    
    print("🔥 Bắt đầu tạo CPU load...")
    
    # Tạo nhiều threads để tăng CPU usage
    threads = []
    for i in range(50):  # 50 concurrent requests
        for api in apis:
            thread = threading.Thread(target=cpu_intensive_request, args=(api,))
            threads.append(thread)
            thread.start()
            time.sleep(0.1)  # Nghỉ 0.1s giữa các requests
    
    # Chờ tất cả threads hoàn thành
    for thread in threads:
        thread.join()
    
    print("✅ CPU load test hoàn thành!")

if __name__ == "__main__":
    create_cpu_load()
