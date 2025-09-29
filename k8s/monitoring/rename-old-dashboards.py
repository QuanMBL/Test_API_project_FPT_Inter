#!/usr/bin/env python3
"""
Script để đổi tên các dashboard cũ thay vì xóa
"""

import requests
import json
import sys

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

def get_dashboard_by_uid(uid):
    """Lấy thông tin dashboard theo UID"""
    try:
        response = requests.get(
            f"{GRAFANA_URL}/api/dashboards/uid/{uid}",
            auth=(GRAFANA_USER, GRAFANA_PASSWORD),
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Không thể lấy dashboard {uid}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Lỗi lấy dashboard {uid}: {e}")
        return None

def update_dashboard(uid, new_title):
    """Cập nhật tên dashboard"""
    try:
        # Lấy dashboard hiện tại
        dashboard_data = get_dashboard_by_uid(uid)
        if not dashboard_data:
            return False
        
        dashboard = dashboard_data.get("dashboard", {})
        dashboard["title"] = new_title
        
        # Cập nhật dashboard
        response = requests.post(
            f"{GRAFANA_URL}/api/dashboards/db",
            json={"dashboard": dashboard, "overwrite": True},
            auth=(GRAFANA_USER, GRAFANA_PASSWORD),
            timeout=30
        )
        
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Không thể cập nhật dashboard {uid}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Lỗi cập nhật dashboard {uid}: {e}")
        return False

def rename_old_dashboards():
    """Đổi tên các dashboard cũ"""
    print("🔄 Đổi tên các dashboard cũ...")
    
    # Danh sách dashboard cũ cần đổi tên
    old_dashboards = [
        {"uid": "all_4api_1", "new_title": "all_4api_1_OLD - Dashboard cũ (không sử dụng)"},
        {"uid": "all_4api_1_new", "new_title": "all_4api_1_OLD2 - Dashboard cũ (không sử dụng)"}
    ]
    
    updated_count = 0
    for dashboard_info in old_dashboards:
        uid = dashboard_info["uid"]
        new_title = dashboard_info["new_title"]
        
        print(f"🔄 Đang đổi tên dashboard {uid}...")
        if update_dashboard(uid, new_title):
            print(f"✅ Đã đổi tên: {new_title}")
            updated_count += 1
        else:
            print(f"❌ Không thể đổi tên dashboard {uid}")
    
    print(f"\n🎉 Hoàn thành! Đã đổi tên {updated_count} dashboard")
    print("✅ Dashboard chính: all_4api_1_v2 - Dashboard tổng quan 4 API Services")
    return True

def main():
    """Hàm chính"""
    print("🔄 Đổi tên Dashboards Cũ")
    print("=" * 30)
    
    # Kiểm tra kết nối Grafana
    auth_token = get_grafana_auth()
    if not auth_token:
        print("❌ Không thể kết nối đến Grafana")
        sys.exit(1)
    
    # Đổi tên dashboards cũ
    if rename_old_dashboards():
        print("\n🎉 Đổi tên hoàn tất!")
        print("🔗 Truy cập Grafana: http://localhost:3000")
        print("📝 Bây giờ chỉ có 1 dashboard chính: all_4api_1_v2")
    else:
        print("\n❌ Đổi tên thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main()
