#!/usr/bin/env python3
"""
Script FIX để tạo dữ liệu thực sự cho Top APIs by Request Rate
"""

import requests
import time
import threading
import random

def create_continuous_traffic():
    """Tạo traffic liên tục thực sự"""
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
                if count % 20 == 0:
                    print(f"📊 Đã tạo {count} requests - {api}: {response.status_code}")
            except:
                pass
        
        time.sleep(0.5)  # Nghỉ 0.5 giây

def main():
    print("🔧 FIX Dashboard Data - Top APIs by Request Rate")
    print("=" * 60)
    print("🚀 Tạo traffic liên tục để có dữ liệu thực tế...")
    print("💡 Dashboard: http://localhost:3000")
    print("🔑 Login: admin / admin123")
    print("📊 Xem 'Top APIs by Request Rate'")
    print("🛑 Nhấn Ctrl+C để dừng")
    print("=" * 60)
    
    try:
        create_continuous_traffic()
    except KeyboardInterrupt:
        print("\n✅ Traffic generation hoàn thành!")
        print("📊 Dashboard bây giờ sẽ có dữ liệu!")

if __name__ == "__main__":
    main()
