#!/usr/bin/env python3
"""
Script để kiểm tra sức khỏe metrics và sửa lỗi nếu cần
"""

import requests
import json
import time
from datetime import datetime

# Cấu hình
PROMETHEUS_URL = "http://localhost:9090"
GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin123"

def check_prometheus_connection():
    """Kiểm tra kết nối Prometheus"""
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query?query=up", timeout=10)
        if response.status_code == 200:
            print("✅ Prometheus đang hoạt động")
            return True
        else:
            print(f"❌ Prometheus không phản hồi: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối đến Prometheus: {e}")
        return False

def check_grafana_connection():
    """Kiểm tra kết nối Grafana"""
    try:
        response = requests.get(f"{GRAFANA_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Grafana đang hoạt động")
            return True
        else:
            print(f"❌ Grafana không phản hồi: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối đến Grafana: {e}")
        return False

def check_api_services_metrics():
    """Kiểm tra metrics từ các API services"""
    services = ['user-api', 'product-api', 'order-api', 'payment-api']
    working_services = []
    
    for service in services:
        try:
            # Kiểm tra metric up
            query = f"up{{job=\"{service}\"}}"
            response = requests.get(f"{PROMETHEUS_URL}/api/v1/query?query={query}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success' and data['data']['result']:
                    result = data['data']['result'][0]
                    if result['value'][1] == '1':
                        print(f"✅ {service}: Đang hoạt động")
                        working_services.append(service)
                    else:
                        print(f"❌ {service}: Không hoạt động")
                else:
                    print(f"⚠️ {service}: Không có dữ liệu metrics")
            else:
                print(f"❌ {service}: Lỗi query Prometheus")
                
        except Exception as e:
            print(f"❌ {service}: Lỗi kiểm tra - {e}")
    
    return working_services

def check_specific_metrics():
    """Kiểm tra các metrics cụ thể"""
    metrics_to_check = [
        "process_cpu_seconds_total",
        "process_resident_memory_bytes", 
        "django_http_requests_total",
        "django_http_request_duration_seconds_sum"
    ]
    
    print("\n🔍 Kiểm tra metrics cụ thể:")
    for metric in metrics_to_check:
        try:
            query = f"{metric}{{job=~\"user-api|product-api|order-api|payment-api\"}}"
            response = requests.get(f"{PROMETHEUS_URL}/api/v1/query?query={query}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success' and data['data']['result']:
                    count = len(data['data']['result'])
                    print(f"✅ {metric}: {count} series")
                else:
                    print(f"⚠️ {metric}: Không có dữ liệu")
            else:
                print(f"❌ {metric}: Lỗi query")
                
        except Exception as e:
            print(f"❌ {metric}: Lỗi - {e}")

def test_dashboard_queries():
    """Test các query được sử dụng trong dashboard"""
    print("\n🧪 Test các query dashboard:")
    
    test_queries = [
        ("Tổng services", "sum(up{job=~\"user-api|product-api|order-api|payment-api\"})"),
        ("CPU trung bình", "avg(rate(process_cpu_seconds_total{job=~\"user-api|product-api|order-api|payment-api\"}[5m]) * 100)"),
        ("Memory tổng", "sum(process_resident_memory_bytes{job=~\"user-api|product-api|order-api|payment-api\"})"),
        ("Error rate", "sum(rate(django_http_requests_total{job=~\"user-api|product-api|order-api|payment-api\",status=~\"4..|5..\"}[5m])) / sum(rate(django_http_requests_total{job=~\"user-api|product-api|order-api|payment-api\"}[5m])) * 100")
    ]
    
    for name, query in test_queries:
        try:
            response = requests.get(f"{PROMETHEUS_URL}/api/v1/query?query={query}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success' and data['data']['result']:
                    value = data['data']['result'][0]['value'][1]
                    print(f"✅ {name}: {value}")
                else:
                    print(f"⚠️ {name}: Không có dữ liệu")
            else:
                print(f"❌ {name}: Lỗi query")
        except Exception as e:
            print(f"❌ {name}: Lỗi - {e}")

def main():
    """Hàm chính"""
    print("🔍 Kiểm tra sức khỏe Metrics và Dashboard")
    print("=" * 50)
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Kiểm tra kết nối
    prometheus_ok = check_prometheus_connection()
    grafana_ok = check_grafana_connection()
    
    if not prometheus_ok:
        print("\n❌ Prometheus không hoạt động. Hãy kiểm tra:")
        print("   • Docker containers đang chạy: docker ps")
        print("   • Prometheus container: docker logs prometheus-container")
        return
    
    if not grafana_ok:
        print("\n❌ Grafana không hoạt động. Hãy kiểm tra:")
        print("   • Docker containers đang chạy: docker ps")
        print("   • Grafana container: docker logs grafana-container")
        return
    
    # Kiểm tra API services
    print("\n🔍 Kiểm tra API Services:")
    working_services = check_api_services_metrics()
    
    if not working_services:
        print("\n❌ Không có API service nào đang hoạt động!")
        print("   Hãy kiểm tra:")
        print("   • Docker containers: docker ps")
        print("   • API logs: docker logs user-api-container")
        print("   • API logs: docker logs product-api-container")
        print("   • API logs: docker logs order-api-container")
        print("   • API logs: docker logs payment-api-container")
        return
    
    print(f"\n✅ Có {len(working_services)} services đang hoạt động: {', '.join(working_services)}")
    
    # Kiểm tra metrics cụ thể
    check_specific_metrics()
    
    # Test dashboard queries
    test_dashboard_queries()
    
    print("\n🎉 Kiểm tra hoàn tất!")
    print("\n💡 Nếu dashboard vẫn không hiển thị dữ liệu:")
    print("   • Đợi 1-2 phút để metrics được thu thập")
    print("   • Refresh dashboard trong Grafana")
    print("   • Kiểm tra time range trong dashboard")
    print("   • Đảm bảo các API services đang nhận requests")

if __name__ == "__main__":
    main()
