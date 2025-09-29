#!/usr/bin/env python3
"""
Script để tạo traffic cho các API services để test dashboard
"""

import requests
import time
import random
import threading
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

def make_request(api_name, base_url, endpoint):
    """Tạo một request đến API"""
    try:
        url = f"{base_url}{endpoint}"
        response = requests.get(url, timeout=5)
        
        print(f"✅ {api_name}: {endpoint} -> {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ {api_name}: {endpoint} -> Connection Error")
        return False
    except requests.exceptions.Timeout:
        print(f"⏰ {api_name}: {endpoint} -> Timeout")
        return False
    except Exception as e:
        print(f"❌ {api_name}: {endpoint} -> {str(e)}")
        return False

def generate_traffic_for_api(api_name, config, duration_minutes=5):
    """Tạo traffic cho một API trong thời gian nhất định"""
    print(f"🚀 Bắt đầu tạo traffic cho {api_name} trong {duration_minutes} phút...")
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    request_count = 0
    
    while time.time() < end_time:
        # Chọn endpoint ngẫu nhiên
        endpoint = random.choice(config['endpoints'])
        
        # Tạo request
        if make_request(api_name, config['base_url'], endpoint):
            request_count += 1
        
        # Nghỉ ngẫu nhiên từ 0.5 đến 2 giây
        time.sleep(random.uniform(0.5, 2.0))
    
    print(f"✅ {api_name}: Hoàn thành {request_count} requests")
    return request_count

def generate_traffic_parallel(duration_minutes=5):
    """Tạo traffic song song cho tất cả APIs"""
    print(f"🚀 Bắt đầu tạo traffic song song cho tất cả APIs trong {duration_minutes} phút...")
    print(f"⏰ Thời gian bắt đầu: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    threads = []
    results = {}
    
    # Tạo thread cho mỗi API
    for api_name, config in API_ENDPOINTS.items():
        thread = threading.Thread(
            target=lambda name=api_name, cfg=config: results.update({
                name: generate_traffic_for_api(name, cfg, duration_minutes)
            })
        )
        threads.append(thread)
        thread.start()
    
    # Đợi tất cả threads hoàn thành
    for thread in threads:
        thread.join()
    
    # Hiển thị kết quả
    print("\n" + "=" * 60)
    print("📊 KẾT QUẢ TRAFFIC GENERATION:")
    total_requests = 0
    for api_name, count in results.items():
        print(f"   {api_name}: {count} requests")
        total_requests += count
    
    print(f"\n🎉 Tổng cộng: {total_requests} requests")
    print(f"⏰ Thời gian kết thúc: {datetime.now().strftime('%H:%M:%S')}")
    
    return total_requests

def test_api_connectivity():
    """Kiểm tra kết nối đến các APIs"""
    print("🔍 Kiểm tra kết nối đến các APIs...")
    
    working_apis = []
    for api_name, config in API_ENDPOINTS.items():
        try:
            response = requests.get(f"{config['base_url']}/", timeout=5)
            if response.status_code in [200, 404, 405]:  # 404/405 cũng OK vì API đang chạy
                print(f"✅ {api_name}: Đang hoạt động")
                working_apis.append(api_name)
            else:
                print(f"⚠️ {api_name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {api_name}: {str(e)}")
    
    return working_apis

def main():
    """Hàm chính"""
    print("🚀 API Traffic Generator - Tạo traffic để test dashboard")
    print("=" * 60)
    
    # Kiểm tra kết nối
    working_apis = test_api_connectivity()
    
    if not working_apis:
        print("\n❌ Không có API nào hoạt động!")
        print("Hãy kiểm tra:")
        print("   • Docker containers: docker ps")
        print("   • API logs: docker logs user-api-container")
        return
    
    print(f"\n✅ Có {len(working_apis)} APIs đang hoạt động: {', '.join(working_apis)}")
    
    # Tạo traffic
    duration = 3  # 3 phút
    print(f"\n🚀 Bắt đầu tạo traffic trong {duration} phút...")
    print("💡 Hãy mở Grafana dashboard để xem dữ liệu real-time!")
    print("🔗 Grafana: http://localhost:3000")
    print("👤 Đăng nhập: admin / admin123")
    print()
    
    total_requests = generate_traffic_parallel(duration)
    
    print(f"\n🎉 Hoàn thành! Đã tạo {total_requests} requests")
    print("📊 Bây giờ hãy kiểm tra dashboard để xem dữ liệu!")

if __name__ == "__main__":
    main()
