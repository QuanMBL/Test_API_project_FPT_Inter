#!/usr/bin/env python3
"""
Script cải tiến để cập nhật dashboard cũ thay vì tạo mới
Tìm kiếm dashboard theo title và cập nhật nếu tồn tại
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

def find_dashboard_by_title(title, auth_token):
    """Tìm dashboard theo title"""
    try:
        search_url = f"{GRAFANA_URL}/api/search?query={title}&type=dash-db"
        
        if auth_token == "basic_auth":
            response = requests.get(
                search_url,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=10
            )
        else:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dashboards = response.json()
            for dashboard in dashboards:
                if dashboard.get('title') == title:
                    return dashboard
        return None
    except Exception as e:
        print(f"❌ Lỗi tìm kiếm dashboard: {e}")
        return None

def get_dashboard_by_id(dashboard_id, auth_token):
    """Lấy thông tin chi tiết dashboard theo ID"""
    try:
        get_url = f"{GRAFANA_URL}/api/dashboards/uid/{dashboard_id}"
        
        if auth_token == "basic_auth":
            response = requests.get(
                get_url,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=10
            )
        else:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.get(get_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"❌ Lỗi lấy dashboard: {e}")
        return None

def update_dashboard(dashboard_data, auth_token, existing_dashboard=None):
    """Cập nhật dashboard cũ hoặc tạo mới"""
    
    # Chuẩn bị payload
    if existing_dashboard:
        # Cập nhật dashboard cũ
        dashboard_data['id'] = existing_dashboard['id']
        dashboard_data['uid'] = existing_dashboard['uid']
        dashboard_data['version'] = existing_dashboard.get('version', 1) + 1
        
        payload = {
            "dashboard": dashboard_data,
            "overwrite": True
        }
        
        # Sử dụng API update
        update_url = f"{GRAFANA_URL}/api/dashboards/db"
        print(f"🔄 Cập nhật dashboard cũ: {existing_dashboard['title']} (ID: {existing_dashboard['id']})")
        
    else:
        # Tạo dashboard mới
        payload = {
            "dashboard": dashboard_data,
            "overwrite": True
        }
        
        # Sử dụng API import
        update_url = f"{GRAFANA_URL}/api/dashboards/import"
        print(f"🆕 Tạo dashboard mới: {dashboard_data['title']}")
    
    try:
        if auth_token == "basic_auth":
            response = requests.post(
                update_url,
                json=payload,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=30
            )
        else:
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            response = requests.post(update_url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'url' in result:
                dashboard_url = f"{GRAFANA_URL}{result['url']}"
                print(f"✅ {'Cập nhật' if existing_dashboard else 'Tạo'} dashboard thành công!")
                print(f"📊 URL Dashboard: {dashboard_url}")
            if 'id' in result:
                print(f"🆔 Dashboard ID: {result['id']}")
            return True
        else:
            print(f"❌ {'Cập nhật' if existing_dashboard else 'Tạo'} dashboard thất bại: {response.status_code}")
            print(f"Chi tiết: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi {'cập nhật' if existing_dashboard else 'tạo'} dashboard: {e}")
        return False

def import_or_update_dashboard(dashboard_file_path, auth_token):
    """Import hoặc cập nhật dashboard"""
    
    # Đọc file dashboard
    if not dashboard_file_path.exists():
        print(f"❌ Không tìm thấy file dashboard: {dashboard_file_path}")
        return False
    
    with open(dashboard_file_path, 'r', encoding='utf-8') as f:
        dashboard_data = json.load(f)
    
    # Lấy thông tin dashboard
    dashboard_info = dashboard_data.get('dashboard', dashboard_data)
    dashboard_title = dashboard_info.get('title', 'Unknown')
    
    print(f"🔍 Tìm kiếm dashboard: {dashboard_title}")
    
    # Tìm dashboard cũ
    existing_dashboard = find_dashboard_by_title(dashboard_title, auth_token)
    
    if existing_dashboard:
        print(f"📋 Tìm thấy dashboard cũ: {existing_dashboard['title']} (ID: {existing_dashboard['id']})")
        # Lấy thông tin chi tiết để có version
        detailed_dashboard = get_dashboard_by_id(existing_dashboard['uid'], auth_token)
        if detailed_dashboard:
            existing_dashboard['version'] = detailed_dashboard['dashboard'].get('version', 1)
    else:
        print(f"📋 Không tìm thấy dashboard cũ, sẽ tạo mới")
    
    # Cập nhật hoặc tạo dashboard
    return update_dashboard(dashboard_info, auth_token, existing_dashboard)

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

def main():
    """Hàm chính"""
    print("🚀 Script Cập Nhật Dashboard - Không Tạo Dashboard Trùng Lặp")
    print("=" * 70)
    
    # Kiểm tra kết nối Grafana
    if not check_grafana_connection():
        sys.exit(1)
    
    # Lấy token xác thực
    auth_token = get_grafana_auth()
    if not auth_token:
        print("❌ Không thể lấy token xác thực")
        sys.exit(1)
    
    # Danh sách dashboard cần cập nhật
    dashboards = [
        {
            "name": "All 4 API Simple Dashboard",
            "file": "all_4api_1_simple_dashboard.json",
            "description": "Tổng quan 4 API Services cơ bản"
        },
        {
            "name": "All 4 API Enhanced Dashboard", 
            "file": "all_4api_1_v2_enhanced_dashboard.json",
            "description": "Tổng quan 4 API Services với bảng dữ liệu"
        },
        {
            "name": "CPU Resource Dashboard",
            "file": "comprehensive-cpu-resource-dashboard.json", 
            "description": "Giám sát CPU và tài nguyên chi tiết"
        },
        {
            "name": "Custom Blue Dashboard",
            "file": "custom_blue_dashboard.json",
            "description": "Dashboard tùy chỉnh màu xanh"
        }
    ]
    
    base_path = Path(__file__).parent.parent.parent / "monitoring" / "grafana" / "dashboards"
    
    success_count = 0
    total_count = len(dashboards)
    
    for dashboard in dashboards:
        print(f"\n{'='*50}")
        print(f"📊 Xử lý: {dashboard['name']}")
        print(f"📝 Mô tả: {dashboard['description']}")
        
        dashboard_path = base_path / dashboard['file']
        
        if import_or_update_dashboard(dashboard_path, auth_token):
            success_count += 1
            print(f"✅ Thành công: {dashboard['name']}")
        else:
            print(f"❌ Thất bại: {dashboard['name']}")
    
    print(f"\n{'='*70}")
    print(f"📊 Kết quả: {success_count}/{total_count} dashboard được xử lý thành công")
    
    if success_count == total_count:
        print("\n🎉 Tất cả dashboard đã được cập nhật thành công!")
        print("🔗 Truy cập Grafana tại: http://localhost:3000")
        print("👤 Đăng nhập: admin / admin123")
    else:
        print(f"\n⚠️ Có {total_count - success_count} dashboard thất bại")
        sys.exit(1)

if __name__ == "__main__":
    main()
