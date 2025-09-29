#!/usr/bin/env python3
"""
Script xóa dashboard với headers đầy đủ
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

def get_all_dashboards():
    """Lấy tất cả dashboard"""
    try:
        response = requests.get(
            f"{GRAFANA_URL}/api/search?type=dash-db",
            auth=(GRAFANA_USER, GRAFANA_PASSWORD),
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Lỗi lấy danh sách dashboard: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return []

def delete_dashboard_with_headers(dashboard_uid, dashboard_id):
    """Xóa dashboard với headers đầy đủ"""
    try:
        # Thử nhiều cách xóa
        methods = [
            {
                "name": "UID API",
                "url": f"{GRAFANA_URL}/api/dashboards/uid/{dashboard_uid}",
                "method": "DELETE"
            },
            {
                "name": "ID API", 
                "url": f"{GRAFANA_URL}/api/dashboards/id/{dashboard_id}",
                "method": "DELETE"
            },
            {
                "name": "DB API",
                "url": f"{GRAFANA_URL}/api/dashboards/db/{dashboard_uid}",
                "method": "DELETE"
            }
        ]
        
        for method in methods:
            print(f"   🔄 Thử {method['name']}: {method['url']}")
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            if method['method'] == 'DELETE':
                response = requests.delete(
                    method['url'],
                    auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                    headers=headers,
                    timeout=10
                )
            else:
                response = requests.post(
                    method['url'],
                    auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                    headers=headers,
                    timeout=10
                )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Thành công với {method['name']}")
                return True
            else:
                print(f"   ❌ Thất bại: {response.text[:100]}")
        
        return False
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        return False

def main():
    """Hàm chính"""
    print("🧹 Script Xóa Dashboard Với Headers Đầy Đủ")
    print("=" * 60)
    
    # Lấy tất cả dashboard
    dashboards = get_all_dashboards()
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
        print(f"   ❌ {dash['title']} (ID: {dash['id']}, UID: {dash['uid']})")
    
    if not delete_dashboards:
        print("\n✅ Không có dashboard nào cần xóa!")
        return
    
    # Xác nhận
    confirm = input(f"\nBạn có chắc chắn muốn xóa {len(delete_dashboards)} dashboard? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Hủy bỏ thao tác")
        return
    
    # Thực hiện xóa
    removed_count = 0
    print(f"\n🗑️ Đang xóa {len(delete_dashboards)} dashboard...")
    
    for dash in delete_dashboards:
        print(f"\n🔄 Xóa: {dash['title']} (ID: {dash['id']}, UID: {dash['uid']})")
        if delete_dashboard_with_headers(dash['uid'], dash['id']):
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
