#!/usr/bin/env python3
"""
Script để dọn dẹp các dashboard trùng lặp trong Grafana
Tìm và xóa các dashboard có tên giống nhau, chỉ giữ lại dashboard mới nhất
"""

import requests
import json
import sys
from collections import defaultdict
from datetime import datetime

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

def get_dashboard_details(dashboard_uid, auth_token):
    """Lấy thông tin chi tiết dashboard"""
    try:
        get_url = f"{GRAFANA_URL}/api/dashboards/uid/{dashboard_uid}"
        
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
        print(f"❌ Lỗi lấy chi tiết dashboard {dashboard_uid}: {e}")
        return None

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

def find_duplicate_dashboards(dashboards, auth_token):
    """Tìm các dashboard trùng lặp"""
    # Nhóm dashboard theo title
    title_groups = defaultdict(list)
    
    for dashboard in dashboards:
        title = dashboard.get('title', 'Unknown')
        title_groups[title].append(dashboard)
    
    duplicates = {}
    for title, dash_list in title_groups.items():
        if len(dash_list) > 1:
            # Lấy thông tin chi tiết để so sánh version và thời gian
            detailed_dashboards = []
            for dash in dash_list:
                details = get_dashboard_details(dash['uid'], auth_token)
                if details:
                    dash_info = details['dashboard']
                    detailed_dashboards.append({
                        'uid': dash['uid'],
                        'id': dash['id'],
                        'title': dash['title'],
                        'url': dash['url'],
                        'version': dash_info.get('version', 1),
                        'updated': dash_info.get('updated', ''),
                        'created': dash_info.get('created', ''),
                        'original': dash
                    })
            
            # Sắp xếp theo version (cao nhất) và thời gian cập nhật (mới nhất)
            detailed_dashboards.sort(key=lambda x: (x['version'], x['updated']), reverse=True)
            
            # Dashboard đầu tiên là mới nhất, các dashboard còn lại là trùng lặp
            duplicates[title] = {
                'keep': detailed_dashboards[0],
                'remove': detailed_dashboards[1:]
            }
    
    return duplicates

def cleanup_duplicates(auth_token, dry_run=True):
    """Dọn dẹp dashboard trùng lặp"""
    print("🔍 Tìm kiếm dashboard trùng lặp...")
    
    # Lấy tất cả dashboard
    dashboards = get_all_dashboards(auth_token)
    if not dashboards:
        print("❌ Không thể lấy danh sách dashboard")
        return False
    
    print(f"📊 Tìm thấy {len(dashboards)} dashboard")
    
    # Tìm dashboard trùng lặp
    duplicates = find_duplicate_dashboards(dashboards, auth_token)
    
    if not duplicates:
        print("✅ Không có dashboard trùng lặp")
        return True
    
    print(f"\n🔍 Tìm thấy {len(duplicates)} nhóm dashboard trùng lặp:")
    
    total_to_remove = 0
    for title, group in duplicates.items():
        print(f"\n📋 Dashboard: {title}")
        print(f"   ✅ Giữ lại: {group['keep']['title']} (ID: {group['keep']['id']}, Version: {group['keep']['version']})")
        print(f"   🗑️ Sẽ xóa {len(group['remove'])} dashboard:")
        
        for dash in group['remove']:
            print(f"      - {dash['title']} (ID: {dash['id']}, Version: {dash['version']})")
            total_to_remove += 1
    
    if dry_run:
        print(f"\n🔍 CHẠY THỬ - Sẽ xóa {total_to_remove} dashboard trùng lặp")
        print("💡 Để thực sự xóa, chạy script với --execute")
        return True
    
    # Xác nhận xóa
    print(f"\n⚠️ Bạn sắp xóa {total_to_remove} dashboard trùng lặp!")
    confirm = input("Bạn có chắc chắn muốn tiếp tục? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Hủy bỏ thao tác")
        return False
    
    # Thực hiện xóa
    removed_count = 0
    for title, group in duplicates.items():
        print(f"\n🗑️ Xóa dashboard trùng lặp: {title}")
        
        for dash in group['remove']:
            print(f"   Đang xóa: {dash['title']} (ID: {dash['id']})")
            if delete_dashboard(dash['uid'], auth_token):
                removed_count += 1
                print(f"   ✅ Đã xóa: {dash['title']}")
            else:
                print(f"   ❌ Lỗi xóa: {dash['title']}")
    
    print(f"\n📊 Kết quả: Đã xóa {removed_count}/{total_to_remove} dashboard trùng lặp")
    return removed_count == total_to_remove

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
    print("🧹 Script Dọn Dẹp Dashboard Trùng Lặp")
    print("=" * 50)
    
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
    
    # Dọn dẹp dashboard trùng lặp
    if cleanup_duplicates(auth_token, dry_run):
        if dry_run:
            print("\n✅ Chạy thử hoàn tất!")
            print("💡 Để thực sự xóa dashboard trùng lặp, chạy:")
            print("   python cleanup-duplicate-dashboards.py --execute")
        else:
            print("\n🎉 Dọn dẹp dashboard trùng lặp hoàn tất!")
    else:
        print("\n❌ Dọn dẹp dashboard trùng lặp thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main()