#!/usr/bin/env python3
"""
Script to import the Comprehensive CPU & Resource Monitoring Dashboard
for 4 API Services into Grafana
"""

import requests
import json
import os
import sys
from pathlib import Path

# Grafana configuration
GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin123"

def get_grafana_auth():
    """Get Grafana authentication token"""
    # Try to get existing API key first
    auth_url = f"{GRAFANA_URL}/api/auth/keys"
    
    try:
        # Check if we can access with basic auth
        response = requests.get(
            f"{GRAFANA_URL}/api/org",
            auth=(GRAFANA_USER, GRAFANA_PASSWORD),
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Using basic authentication")
            return "basic_auth"
        else:
            print(f"Basic auth failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error with basic auth: {e}")
        return None

def import_dashboard():
    """Import the CPU Resource Dashboard into Grafana"""
    
    # Get authentication token
    auth_token = get_grafana_auth()
    if not auth_token:
        print("Failed to get authentication token")
        return False
    
    # Load dashboard JSON
    dashboard_path = Path(__file__).parent.parent.parent / "monitoring" / "grafana" / "dashboards" / "comprehensive-cpu-resource-dashboard.json"
    
    if not dashboard_path.exists():
        print(f"Dashboard file not found: {dashboard_path}")
        return False
    
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        dashboard_data = json.load(f)
    
    # Prepare dashboard for import
    dashboard_payload = {
        "dashboard": dashboard_data["dashboard"],
        "overwrite": True,
        "inputs": []
    }
    
    # Import dashboard
    import_url = f"{GRAFANA_URL}/api/dashboards/import"
    
    try:
        if auth_token == "basic_auth":
            # Use basic authentication
            response = requests.post(
                import_url,
                json=dashboard_payload,
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=30
            )
        else:
            # Use token authentication
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
                print(f"✅ Dashboard imported successfully!")
                print(f"📊 Dashboard URL: {dashboard_url}")
            if 'id' in result:
                print(f"🆔 Dashboard ID: {result['id']}")
            return True
        else:
            print(f"❌ Failed to import dashboard: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error importing dashboard: {e}")
        return False

def check_grafana_connection():
    """Check if Grafana is accessible"""
    try:
        response = requests.get(f"{GRAFANA_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Grafana is accessible")
            return True
        else:
            print(f"❌ Grafana health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Grafana: {e}")
        print("Make sure Grafana is running on http://localhost:3000")
        return False

def main():
    """Main function"""
    print("🚀 Importing Comprehensive CPU & Resource Monitoring Dashboard")
    print("=" * 60)
    
    # Check Grafana connection
    if not check_grafana_connection():
        sys.exit(1)
    
    # Import dashboard
    if import_dashboard():
        print("\n🎉 Dashboard import completed successfully!")
        print("\n📋 Dashboard Features:")
        print("   • CPU Usage overview for all 4 services")
        print("   • Memory usage trends")
        print("   • Detailed metrics tables for each service")
        print("   • Response time and latency monitoring")
        print("   • Error rate tracking")
        print("   • Service availability status")
        print("   • Request rate trends")
        print("\n🔗 Access your dashboard at: http://localhost:3000")
    else:
        print("\n❌ Dashboard import failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
