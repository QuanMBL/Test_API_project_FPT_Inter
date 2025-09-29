#!/usr/bin/env python3
"""
Script để import dashboard all_4api_1_v2_enhanced vào Grafana
Dashboard tổng quan cho 4 API Services với bảng dữ liệu ổn định
"""

import requests
import json
import os
import sys
from pathlib import Path

# Cấu hình Grafana
GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin123"

def get_grafana_auth():
    """Lấy token xác thực từ Grafana"""
    try:
        # Kiểm tra xác thực cơ bản
        response = requests.get(
            f"{GRAFANA_URL}/api/org",
            auth=(GRAFANA_USER, GRAFANA_PASSWORD),
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Sử dụng xác thực cơ bản")
            return "basic_auth"
        else:
            print(f"❌ Xác thực cơ bản thất bại: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Lỗi xác thực: {e}")
        return None

def import_dashboard():
    """Import dashboard all_4api_1_v2_enhanced vào Grafana"""
    
    # Lấy token xác thực
    auth_token = get_grafana_auth()
    if not auth_token:
        print("❌ Không thể lấy token xác thực")
        return False
    
    # Đọc file dashboard JSON
    dashboard_path = Path(__file__).parent.parent.parent / "monitoring" / "grafana" / "dashboards" / "all_4api_1_v2_enhanced_dashboard.json"
    
    if not dashboard_path.exists():
        print(f"❌ Không tìm thấy file dashboard: {dashboard_path}")
        return False
    
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        dashboard_data = json.load(f)
    
    # Chuẩn bị dữ liệu dashboard để import
    dashboard_payload = {
        "dashboard": dashboard_data,
        "overwrite": True,
        "inputs": []
    }
    
    # Import dashboard
    import_url = f"{GRAFANA_URL}/api/dashboards/import"
    
    try:
        if auth_token == "basic_auth":
            # Sử dụng xác thực cơ bản
            response = requests.post(
                import_url,
                json=dashboard_payload,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=30
            )
        else:
            # Sử dụng xác thực token
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            response = requests.post(
                import_url,
                json=dashboard_payload,
                headers=headers,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            if 'url' in result:
                dashboard_url = f"{GRAFANA_URL}{result['url']}"
                print(f"✅ Import dashboard thành công!")
                print(f"📊 URL Dashboard: {dashboard_url}")
            if 'id' in result:
                print(f"🆔 Dashboard ID: {result['id']}")
            return True
        else:
            print(f"❌ Import dashboard thất bại: {response.status_code}")
            print(f"Chi tiết: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi import dashboard: {e}")
        return False

def check_grafana_connection():
    """Kiểm tra kết nối đến Grafana"""
    try:
        response = requests.get(f"{GRAFANA_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Grafana đang hoạt động")
            return True
        else:
            print(f"❌ Kiểm tra sức khỏe Grafana thất bại: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối đến Grafana: {e}")
        print("Hãy đảm bảo Grafana đang chạy trên http://localhost:3000")
        return False

def check_prometheus_metrics():
    """Kiểm tra metrics từ Prometheus"""
    try:
        prometheus_url = "http://localhost:9090"
        response = requests.get(f"{prometheus_url}/api/v1/query?query=up", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success' and data['data']['result']:
                print("✅ Prometheus có dữ liệu metrics")
                return True
            else:
                print("⚠️ Prometheus chưa có dữ liệu metrics")
                return False
        else:
            print(f"❌ Không thể kết nối đến Prometheus: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Lỗi kiểm tra Prometheus: {e}")
        return False

def main():
    """Hàm chính"""
    print("🚀 Import Dashboard all_4api_1_v2_enhanced - Tổng quan 4 API Services với bảng dữ liệu")
    print("=" * 80)
    
    # Kiểm tra kết nối Grafana
    if not check_grafana_connection():
        sys.exit(1)
    
    # Kiểm tra Prometheus
    if not check_prometheus_metrics():
        print("⚠️ Cảnh báo: Prometheus có thể chưa có dữ liệu metrics")
        print("   Hãy đảm bảo các API services đang chạy và có metrics")
    
    # Import dashboard
    if import_dashboard():
        print("\n🎉 Import dashboard thành công!")
        print("\n📋 Tính năng Dashboard Enhanced:")
        print("   • 📊 Tổng số Services đang hoạt động")
        print("   • 🖥️ CPU Usage trung bình và theo từng service")
        print("   • 💾 Memory Usage tổng và theo từng service")
        print("   • ⚠️ Tỷ lệ lỗi trung bình và theo từng service")
        print("   • 📋 Bảng thông tin Services (ỔN ĐỊNH)")
        print("   • 📊 Bảng CPU Usage theo Service (ỔN ĐỊNH)")
        print("   • 💾 Bảng Memory Usage theo Service (ỔN ĐỊNH)")
        print("   • 🚀 Bảng Request Rate theo Service (ỔN ĐỊNH)")
        print("   • 📈 Biểu đồ CPU Usage theo thời gian")
        print("   • 💾 Biểu đồ Memory Usage theo thời gian")
        print("   • 📊 Bảng HTTP Status Codes (ỔN ĐỊNH)")
        print("   • ⏱️ Bảng Response Time trung bình (ỔN ĐỊNH)")
        print("\n🔗 Truy cập dashboard tại: http://localhost:3000")
        print("👤 Đăng nhập: admin / admin123")
        print("\n💡 Lưu ý: Các bảng dữ liệu sẽ hiển thị ổn định hơn biểu đồ")
    else:
        print("\n❌ Import dashboard thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main()
