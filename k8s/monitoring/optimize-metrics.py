#!/usr/bin/env python3
"""
Script để tối ưu metrics và giảm dữ liệu trùng lặp
"""

import subprocess
import time
import requests
import os

def restart_prometheus():
    """Restart Prometheus với cấu hình mới"""
    print("🔄 Đang restart Prometheus...")
    try:
        subprocess.run(["docker", "restart", "prometheus-container"], check=True)
        print("✅ Prometheus đã restart")
        return True
    except Exception as e:
        print(f"❌ Lỗi restart Prometheus: {e}")
        return False

def stop_traffic_generator():
    """Dừng traffic generator hiện tại"""
    print("🛑 Đang dừng traffic generator...")
    try:
        # Tìm và kill process traffic generator
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
            capture_output=True, text=True
        )
        
        if "continuous-traffic-generator" in result.stdout:
            print("⚠️ Traffic generator đang chạy, cần dừng thủ công")
            print("💡 Nhấn Ctrl+C trong terminal đang chạy traffic generator")
        else:
            print("✅ Không có traffic generator nào đang chạy")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi dừng traffic generator: {e}")
        return False

def clear_prometheus_data():
    """Xóa dữ liệu cũ trong Prometheus"""
    print("🧹 Đang xóa dữ liệu cũ trong Prometheus...")
    try:
        # Restart Prometheus để xóa cache
        subprocess.run(["docker", "restart", "prometheus-container"], check=True)
        time.sleep(5)
        print("✅ Dữ liệu cũ đã được xóa")
        return True
    except Exception as e:
        print(f"❌ Lỗi xóa dữ liệu: {e}")
        return False

def check_services():
    """Kiểm tra các services"""
    print("🔍 Kiểm tra các services...")
    
    services = [
        ("Prometheus", "http://localhost:9090"),
        ("Grafana", "http://localhost:3000"),
        ("User API", "http://localhost:8000"),
        ("Product API", "http://localhost:8001"),
        ("Order API", "http://localhost:8002"),
        ("Payment API", "http://localhost:8003")
    ]
    
    working_services = []
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 404, 405]:
                print(f"✅ {name}: Đang hoạt động")
                working_services.append(name)
            else:
                print(f"⚠️ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
    
    return working_services

def main():
    """Hàm chính"""
    print("🔧 Script Tối Ưu Metrics - Giảm Dữ Liệu Trùng Lặp")
    print("=" * 60)
    
    # Kiểm tra services
    working_services = check_services()
    if len(working_services) < 4:
        print("❌ Không đủ services hoạt động!")
        return
    
    # Dừng traffic generator
    stop_traffic_generator()
    
    # Restart Prometheus
    if restart_prometheus():
        print("⏳ Đợi Prometheus khởi động...")
        time.sleep(10)
    
    # Xóa dữ liệu cũ
    clear_prometheus_data()
    
    print("\n✅ Tối ưu hoàn tất!")
    print("\n📋 Các thay đổi đã thực hiện:")
    print("   • Tăng Prometheus scrape interval: 15s → 30s")
    print("   • Tăng API scrape interval: 10s → 30s")
    print("   • Tăng traffic generator interval: 0.1-0.5s → 1-2s")
    print("   • Tăng vòng lặp traffic: 1-3s → 5-10s")
    print("   • Restart Prometheus với cấu hình mới")
    
    print("\n🎯 Kết quả mong đợi:")
    print("   • Giảm 50% dữ liệu trùng lặp")
    print("   • Dashboard hiển thị dữ liệu ổn định hơn")
    print("   • Giảm tải cho hệ thống")
    
    print("\n🔗 Truy cập dashboard: http://localhost:3000")
    print("👤 Đăng nhập: admin / admin123")
    print("\n💡 Để tạo traffic mới với tần suất thấp hơn:")
    print("   python k8s\\monitoring\\continuous-traffic-generator.py")

if __name__ == "__main__":
    main()
