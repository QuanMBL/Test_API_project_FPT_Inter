#!/usr/bin/env python3
"""
Script để dọn dẹp dashboard theo yêu cầu cụ thể
Giữ lại chỉ 2 dashboard:
- all_4api_1_v2 - Dashboard tổng quan 4 API Services  
- Dashboard Custom - Màu Blue
Xóa tất cả dashboard khác
"""

import requests
import json
import sys
from datetime import datetime

# Cấu hình Grafana
GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin123"

# Dashboard cần giữ lại
KEEP_DASHBOARDS = [
    "all_4api_1_v2 - Dashboard tổng quan 4 API Services",
    "Dashboard Custom - Màu Blue"
]

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

def delete_dashboard(dashboard_uid, auth_token):
    """Xóa dashboard"""
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
            return True
        else:
            print(f"❌ Lỗi xóa dashboard {dashboard_uid}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Lỗi xóa dashboard {dashboard_uid}: {e}")
        return False

def cleanup_specific_dashboards(auth_token, dry_run=True):
    """Dọn dẹp dashboard theo yêu cầu cụ thể"""
    print("🔍 Tìm kiếm dashboard...")
    
    # Lấy tất cả dashboard
    dashboards = get_all_dashboards(auth_token)
    if not dashboards:
        print("❌ Không thể lấy danh sách dashboard")
        return False
    
    print(f"📊 Tìm thấy {len(dashboards)} dashboard")
    
    # Phân loại dashboard
    keep_dashboards = []
    delete_dashboards = []
    
    for dashboard in dashboards:
        title = dashboard.get('title', 'Unknown')
        if title in KEEP_DASHBOARDS:
            keep_dashboards.append(dashboard)
        else:
            delete_dashboards.append(dashboard)
    
    # Hiển thị kết quả phân loại
    print(f"\n📋 Dashboard sẽ GIỮ LẠI ({len(keep_dashboards)}):")
    for dash in keep_dashboards:
        print(f"   ✅ {dash['title']} (ID: {dash['id']})")
    
    print(f"\n🗑️ Dashboard sẽ XÓA ({len(delete_dashboards)}):")
    for dash in delete_dashboards:
        print(f"   ❌ {dash['title']} (ID: {dash['id']})")
    
    if dry_run:
        print(f"\n🔍 CHẠY THỬ - Sẽ xóa {len(delete_dashboards)} dashboard")
        print("💡 Để thực sự xóa, chạy script với --execute")
        return True
    
    # Xác nhận xóa
    print(f"\n⚠️ Bạn sắp xóa {len(delete_dashboards)} dashboard!")
    print("📋 Dashboard sẽ được GIỮ LẠI:")
    for dash in keep_dashboards:
        print(f"   ✅ {dash['title']}")
    
    confirm = input("\nBạn có chắc chắn muốn tiếp tục? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Hủy bỏ thao tác")
        return False
    
    # Thực hiện xóa
    removed_count = 0
    print(f"\n🗑️ Đang xóa {len(delete_dashboards)} dashboard...")
    
    for dash in delete_dashboards:
        print(f"   Đang xóa: {dash['title']} (ID: {dash['id']})")
        if delete_dashboard(dash['uid'], auth_token):
            removed_count += 1
            print(f"   ✅ Đã xóa: {dash['title']}")
        else:
            print(f"   ❌ Lỗi xóa: {dash['title']}")
    
    print(f"\n📊 Kết quả: Đã xóa {removed_count}/{len(delete_dashboards)} dashboard")
    print(f"✅ Giữ lại {len(keep_dashboards)} dashboard quan trọng")
    
    return removed_count == len(delete_dashboards)

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
    print("🧹 Script Dọn Dẹp Dashboard Theo Yêu Cầu Cụ Thể")
    print("=" * 60)
    print("📋 Dashboard sẽ GIỮ LẠI:")
    for dash in KEEP_DASHBOARDS:
        print(f"   ✅ {dash}")
    print("=" * 60)
    
    # Kiểm tra tham số
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        dry_run = False
        print("⚠️ CHẾ ĐỘ THỰC THI - Sẽ xóa dashboard thật!")
    else:
        print("🔍 CHẾ ĐỘ CHẠY THỬ - Chỉ hiển thị dashboard sẽ bị xóa")
    
    # Kiểm tra kết nối Grafana
    if not check_grafana_connection():
        sys.exit(1)
    
    # Lấy token xác thực
    auth_token = get_grafana_auth()
    if not auth_token:
        print("❌ Không thể lấy token xác thực")
        sys.exit(1)
    
    # Dọn dẹp dashboard theo yêu cầu
    if cleanup_specific_dashboards(auth_token, dry_run):
        if dry_run:
            print("\n✅ Chạy thử hoàn tất!")
            print("💡 Để thực sự xóa dashboard, chạy:")
            print("   python k8s\\monitoring\\cleanup-specific-dashboards.py --execute")
        else:
            print("\n🎉 Dọn dẹp dashboard hoàn tất!")
            print("📋 Dashboard còn lại:")
            for dash in KEEP_DASHBOARDS:
                print(f"   ✅ {dash}")
            print("\n🔗 Truy cập Grafana: http://localhost:3000")
            print("👤 Đăng nhập: admin / admin123")
    else:
        print("\n❌ Dọn dẹp dashboard thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main()
