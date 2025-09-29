#!/usr/bin/env python3
"""
Script để import dashboard v4 với màu blue đã chỉnh sửa
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
    """Import dashboard v4 với màu blue"""
    
    # Lấy token xác thực
    auth_token = get_grafana_auth()
    if not auth_token:
        print("❌ Không thể lấy token xác thực")
        return False
    
    # Đọc file dashboard JSON
    dashboard_path = Path(__file__).parent.parent.parent / "monitoring" / "grafana" / "dashboards" / "all_4api_1_simple_dashboard.json"
    
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
            response = requests.post(
                import_url,
                json=dashboard_payload,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=30
            )
        else:
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
                print(f"✅ Import dashboard v4 thành công!")
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

def main():
    """Hàm chính"""
    print("🚀 Import Dashboard v4 - Màu blue đã chỉnh sửa")
    print("=" * 50)
    
    # Import dashboard
    if import_dashboard():
        print("\n🎉 Import dashboard v4 thành công!")
        print("🔗 Truy cập dashboard tại: http://localhost:3000")
        print("👤 Đăng nhập: admin / admin123")
        print("📊 Dashboard: all_4api_1_v4 - Dashboard tổng quan 4 API Services")
        print("🎨 Màu blue đã được áp dụng!")
    else:
        print("\n❌ Import dashboard thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main()

