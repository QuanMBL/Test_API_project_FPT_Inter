#!/usr/bin/env python3
"""
Script đơn giản để test Top APIs by Request Rate
"""

import requests
import time
import random

def make_requests():
    """Tạo requests đơn giản"""
    apis = [
        'http://localhost:8000/api/users/',
        'http://localhost:8001/api/products/',
        'http://localhost:8002/api/orders/',
        'http://localhost:8003/api/payments/'
    ]
    
    for api in apis:
        try:
            response = requests.get(api, timeout=2)
            print(f"📊 {api}: {response.status_code}")
        except Exception as e:
            print(f"❌ {api}: {str(e)}")

def main():
    print("🚀 Simple Traffic Test for Top APIs")
    print("=" * 40)
    print("💡 Tạo traffic liên tục...")
    print("🔗 Dashboard: http://localhost:3000")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 40)
    
    count = 0
    while True:
        count += 1
        print(f"\n🔄 Round {count}")
        make_requests()
        
        if count % 10 == 0:
            print(f"📈 Đã tạo {count * 4} requests")
            print("💡 Kiểm tra dashboard: http://localhost:3000")
        
        time.sleep(2)  # Nghỉ 2 giây giữa các rounds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Dừng traffic test...")
        print("✅ Test hoàn thành!")
