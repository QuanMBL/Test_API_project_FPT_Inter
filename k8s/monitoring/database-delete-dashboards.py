#!/usr/bin/env python3
"""
Script xóa dashboard trực tiếp từ database Grafana
"""

import sqlite3
import os
import sys
import subprocess

# Cấu hình
GRAFANA_DB_PATH = "/var/lib/grafana/grafana.db"
KEEP_DASHBOARD = "all_4api_1_v2 - Dashboard tổng quan 4 API Services"

def get_database_connection():
    """Lấy kết nối database từ container"""
    try:
        # Copy database từ container về local
        subprocess.run([
            "docker", "cp", 
            "grafana-container:/var/lib/grafana/grafana.db", 
            "grafana_temp.db"
        ], check=True)
        
        # Kết nối database local
        conn = sqlite3.connect("grafana_temp.db")
        return conn
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        return None

def list_dashboards(conn):
    """Liệt kê tất cả dashboard"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, uid, created, updated 
            FROM dashboard 
            ORDER BY id
        """)
        
        dashboards = cursor.fetchall()
        return dashboards
    except Exception as e:
        print(f"❌ Lỗi lấy danh sách dashboard: {e}")
        return []

def delete_dashboard_from_db(conn, dashboard_id):
    """Xóa dashboard từ database"""
    try:
        cursor = conn.cursor()
        
        # Xóa dashboard
        cursor.execute("DELETE FROM dashboard WHERE id = ?", (dashboard_id,))
        
        # Xóa các bảng liên quan
        cursor.execute("DELETE FROM dashboard_version WHERE dashboard_id = ?", (dashboard_id,))
        cursor.execute("DELETE FROM dashboard_acl WHERE dashboard_id = ?", (dashboard_id,))
        cursor.execute("DELETE FROM dashboard_tag WHERE dashboard_id = ?", (dashboard_id,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Lỗi xóa dashboard {dashboard_id}: {e}")
        return False

def copy_database_back():
    """Copy database trở lại container"""
    try:
        subprocess.run([
            "docker", "cp", 
            "grafana_temp.db",
            "grafana-container:/var/lib/grafana/grafana.db"
        ], check=True)
        
        # Restart Grafana để áp dụng thay đổi
        subprocess.run([
            "docker", "restart", "grafana-container"
        ], check=True)
        
        return True
    except Exception as e:
        print(f"❌ Lỗi copy database: {e}")
        return False

def main():
    """Hàm chính"""
    print("🧹 Script Xóa Dashboard Từ Database")
    print("=" * 50)
    
    # Lấy kết nối database
    conn = get_database_connection()
    if not conn:
        print("❌ Không thể kết nối database")
        sys.exit(1)
    
    # Lấy danh sách dashboard
    dashboards = list_dashboards(conn)
    if not dashboards:
        print("❌ Không có dashboard nào")
        conn.close()
        return
    
    print(f"📊 Tìm thấy {len(dashboards)} dashboard trong database:")
    
    # Phân loại dashboard
    keep_dashboards = []
    delete_dashboards = []
    
    for dash in dashboards:
        dashboard_id, title, uid, created, updated = dash
        if KEEP_DASHBOARD in title:
            keep_dashboards.append(dash)
        else:
            delete_dashboards.append(dash)
    
    # Hiển thị kết quả
    if keep_dashboards:
        print(f"\n📋 Dashboard sẽ GIỮ LẠI ({len(keep_dashboards)}):")
        for dash in keep_dashboards:
            print(f"   ✅ {dash[1]} (ID: {dash[0]}, UID: {dash[2]})")
    
    print(f"\n🗑️ Dashboard sẽ XÓA ({len(delete_dashboards)}):")
    for dash in delete_dashboards:
        print(f"   ❌ {dash[1]} (ID: {dash[0]}, UID: {dash[2]})")
    
    if not delete_dashboards:
        print("\n✅ Không có dashboard nào cần xóa!")
        conn.close()
        return
    
    # Xác nhận
    confirm = input(f"\nBạn có chắc chắn muốn xóa {len(delete_dashboards)} dashboard từ database? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Hủy bỏ thao tác")
        conn.close()
        return
    
    # Thực hiện xóa
    removed_count = 0
    print(f"\n🗑️ Đang xóa {len(delete_dashboards)} dashboard từ database...")
    
    for dash in delete_dashboards:
        dashboard_id, title, uid = dash[0], dash[1], dash[2]
        print(f"\n🔄 Xóa: {title} (ID: {dashboard_id})")
        
        if delete_dashboard_from_db(conn, dashboard_id):
            removed_count += 1
            print(f"   ✅ Đã xóa: {title}")
        else:
            print(f"   ❌ Không thể xóa: {title}")
    
    conn.close()
    
    print(f"\n📊 Kết quả: Đã xóa {removed_count}/{len(delete_dashboards)} dashboard từ database")
    
    if removed_count > 0:
        print("\n🔄 Đang copy database trở lại container...")
        if copy_database_back():
            print("✅ Database đã được cập nhật và Grafana đã restart")
            print("🔗 Truy cập Grafana: http://localhost:3000")
            print("👤 Đăng nhập: admin / admin123")
        else:
            print("❌ Lỗi copy database trở lại container")
    else:
        print("⚠️ Không có dashboard nào được xóa")
    
    # Dọn dẹp file tạm
    try:
        os.remove("grafana_temp.db")
    except:
        pass

if __name__ == "__main__":
    main()
