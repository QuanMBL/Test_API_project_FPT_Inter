#!/usr/bin/env python3
"""
Script xóa dashboard bằng cách sử dụng API khác
Thử nhiều phương pháp xóa dashboard
"""

import requests
import json
import sys

# Cấu hình Grafana
GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin123"

# Dashboard cần giữ lại
KEEP_DASHBOARD = "all_4api_1_v2 - Dashboard tổng quan 4 API Services"

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

def get_all_dashboards(auth_token):
    """Lấy tất cả dashboard từ Grafana"""
    try:
        search_url = f"{GRAFANA_URL}/api/search?type=dash-db"
        
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
            return response.json()
        else:
            print(f"❌ Lỗi lấy danh sách dashboard: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return []

def force_delete_dashboard(dashboard_id, dashboard_uid, auth_token):
    """Thử nhiều cách xóa dashboard"""
    print(f"   🔄 Thử xóa dashboard ID: {dashboard_id}, UID: {dashboard_uid}")
    
    # Phương pháp 1: Xóa bằng UID
    try:
        delete_url = f"{GRAFANA_URL}/api/dashboards/uid/{dashboard_uid}"
        
        if auth_token == "basic_auth":
            response = requests.delete(
                delete_url,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=10
            )
        else:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.delete(delete_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Xóa thành công bằng UID")
            return True
        else:
            print(f"   ❌ Lỗi xóa bằng UID: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Lỗi xóa bằng UID: {e}")
    
    # Phương pháp 2: Xóa bằng ID
    try:
        delete_url = f"{GRAFANA_URL}/api/dashboards/id/{dashboard_id}"
        
        if auth_token == "basic_auth":
            response = requests.delete(
                delete_url,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=10
            )
        else:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.delete(delete_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Xóa thành công bằng ID")
            return True
        else:
            print(f"   ❌ Lỗi xóa bằng ID: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Lỗi xóa bằng ID: {e}")
    
    # Phương pháp 3: Xóa bằng slug
    try:
        delete_url = f"{GRAFANA_URL}/api/dashboards/db/{dashboard_uid}"
        
        if auth_token == "basic_auth":
            response = requests.delete(
                delete_url,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=10
            )
        else:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.delete(delete_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Xóa thành công bằng slug")
            return True
        else:
            print(f"   ❌ Lỗi xóa bằng slug: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Lỗi xóa bằng slug: {e}")
    
    return False

def main():
    """Hàm chính"""
    print("🧹 Script Xóa Dashboard Bằng Nhiều Phương Pháp")
    print("=" * 60)
    
    # Kiểm tra kết nối Grafana
    try:
        response = requests.get(f"{GRAFANA_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ Grafana không hoạt động")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Không thể kết nối đến Grafana: {e}")
        sys.exit(1)
    
    # Lấy token xác thực
    auth_token = get_grafana_auth()
    if not auth_token:
        print("❌ Không thể lấy token xác thực")
        sys.exit(1)
    
    # Lấy tất cả dashboard
    dashboards = get_all_dashboards(auth_token)
    if not dashboards:
        print("❌ Không thể lấy danh sách dashboard")
        sys.exit(1)
    
    print(f"📊 Tìm thấy {len(dashboards)} dashboard")
    
    # Phân loại dashboard
    keep_dashboard = None
    delete_dashboards = []
    
    for dashboard in dashboards:
        title = dashboard.get('title', 'Unknown')
        if title == KEEP_DASHBOARD:
            keep_dashboard = dashboard
        else:
            delete_dashboards.append(dashboard)
    
    # Hiển thị kết quả
    if keep_dashboard:
        print(f"\n📋 Dashboard sẽ GIỮ LẠI (1):")
        print(f"   ✅ {keep_dashboard['title']} (ID: {keep_dashboard['id']})")
    else:
        print(f"\n⚠️ Không tìm thấy dashboard: {KEEP_DASHBOARD}")
    
    print(f"\n🗑️ Dashboard sẽ XÓA ({len(delete_dashboards)}):")
    for dash in delete_dashboards:
        print(f"   ❌ {dash['title']} (ID: {dash['id']})")
    
    # Xác nhận
    if not delete_dashboards:
        print("\n✅ Không có dashboard nào cần xóa!")
        return
    
    confirm = input(f"\nBạn có chắc chắn muốn xóa {len(delete_dashboards)} dashboard? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Hủy bỏ thao tác")
        return
    
    # Thực hiện xóa
    removed_count = 0
    print(f"\n🗑️ Đang xóa {len(delete_dashboards)} dashboard...")
    
    for dash in delete_dashboards:
        print(f"\n🔄 Xóa: {dash['title']} (ID: {dash['id']})")
        if force_delete_dashboard(dash['id'], dash['uid'], auth_token):
            removed_count += 1
            print(f"   ✅ Đã xóa: {dash['title']}")
        else:
            print(f"   ❌ Không thể xóa: {dash['title']}")
    
    print(f"\n📊 Kết quả: Đã xóa {removed_count}/{len(delete_dashboards)} dashboard")
    
    if keep_dashboard:
        print(f"✅ Giữ lại dashboard: {keep_dashboard['title']}")
    
    print("\n🔗 Truy cập Grafana: http://localhost:3000")
    print("👤 Đăng nhập: admin / admin123")

if __name__ == "__main__":
    main()
