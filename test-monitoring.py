#!/usr/bin/env python3
"""
Test script để kiểm tra Grafana monitoring setup
"""

import requests
import time
import json
from urllib.parse import urljoin

# Configuration
GRAFANA_URL = "http://localhost:3000"
PROMETHEUS_URL = "http://localhost:9090"
API_ENDPOINTS = [
    "http://localhost:8000",
    "http://localhost:8001", 
    "http://localhost:8002",
    "http://localhost:8003"
]

def test_prometheus():
    """Test Prometheus connectivity"""
    print("🔍 Testing Prometheus...")
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/targets", timeout=10)
        if response.status_code == 200:
            targets = response.json()
            active_targets = [t for t in targets['data']['activeTargets'] if t['health'] == 'up']
            print(f"✅ Prometheus is running - {len(active_targets)} targets active")
            return True
        else:
            print(f"❌ Prometheus returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Prometheus connection failed: {e}")
        return False

def test_grafana():
    """Test Grafana connectivity"""
    print("📊 Testing Grafana...")
    try:
        response = requests.get(f"{GRAFANA_URL}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Grafana is running")
            return True
        else:
            print(f"❌ Grafana returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Grafana connection failed: {e}")
        return False

def test_api_metrics():
    """Test API metrics endpoints"""
    print("🔧 Testing API metrics endpoints...")
    success_count = 0
    
    for i, api_url in enumerate(API_ENDPOINTS, 1):
        try:
            metrics_url = f"{api_url}/metrics"
            response = requests.get(metrics_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ API {i} metrics endpoint working")
                success_count += 1
            else:
                print(f"❌ API {i} metrics returned status {response.status_code}")
        except Exception as e:
            print(f"❌ API {i} metrics failed: {e}")
    
    return success_count == len(API_ENDPOINTS)

def test_api_endpoints():
    """Test basic API functionality"""
    print("🚀 Testing API endpoints...")
    success_count = 0
    
    # Test user API
    try:
        response = requests.get("http://localhost:8000/api/users/", timeout=5)
        if response.status_code in [200, 404]:  # 404 is ok if no users exist
            print("✅ User API responding")
            success_count += 1
        else:
            print(f"❌ User API returned status {response.status_code}")
    except Exception as e:
        print(f"❌ User API failed: {e}")
    
    # Test product API
    try:
        response = requests.get("http://localhost:8001/api/products/", timeout=5)
        if response.status_code in [200, 404]:  # 404 is ok if no products exist
            print("✅ Product API responding")
            success_count += 1
        else:
            print(f"❌ Product API returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Product API failed: {e}")
    
    return success_count >= 1

def generate_test_data():
    """Generate some test data to create metrics"""
    print("📝 Generating test data...")
    
    # Create a test user
    try:
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        response = requests.post("http://localhost:8000/api/users/", json=user_data, timeout=5)
        if response.status_code in [200, 201]:
            print("✅ Test user created")
        else:
            print(f"⚠️  User creation returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️  User creation failed: {e}")
    
    # Create a test product
    try:
        product_data = {
            "name": "Test Product",
            "description": "Test product for monitoring",
            "price": 99.99,
            "stock": 10
        }
        response = requests.post("http://localhost:8001/api/products/", json=product_data, timeout=5)
        if response.status_code in [200, 201]:
            print("✅ Test product created")
        else:
            print(f"⚠️  Product creation returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️  Product creation failed: {e}")
    
    # Make some API calls to generate metrics
    for _ in range(5):
        try:
            requests.get("http://localhost:8000/api/users/", timeout=2)
            requests.get("http://localhost:8001/api/products/", timeout=2)
        except:
            pass
        time.sleep(0.5)

def main():
    """Main test function"""
    print("🧪 Grafana Monitoring Test Suite")
    print("=" * 50)
    
    # Wait a bit for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(5)
    
    # Run tests
    tests = [
        ("Prometheus", test_prometheus),
        ("Grafana", test_grafana),
        ("API Metrics", test_api_metrics),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
        print()
    
    # Generate test data if APIs are working
    if results.get("API Endpoints", False):
        generate_test_data()
        print()
    
    # Summary
    print("📋 Test Summary:")
    print("=" * 50)
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:15} {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Monitoring setup is working correctly.")
        print("\n📊 Access your monitoring:")
        print(f"   Grafana:    {GRAFANA_URL} (admin/admin123)")
        print(f"   Prometheus: {PROMETHEUS_URL}")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure all containers are running: docker-compose ps")
        print("   2. Check container logs: docker-compose logs [service-name]")
        print("   3. Wait a bit longer for services to fully start")

if __name__ == "__main__":
    main()
