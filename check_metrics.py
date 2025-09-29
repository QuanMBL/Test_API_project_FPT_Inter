#!/usr/bin/env python3
"""
Script để kiểm tra metrics endpoints của các API
"""

import requests
import time
import json

# API endpoints
APIS = {
    'user-api': 'http://localhost:8000',
    'product-api': 'http://localhost:8001', 
    'order-api': 'http://localhost:8002',
    'payment-api': 'http://localhost:8003'
}

def check_metrics(api_name, base_url):
    """Kiểm tra metrics endpoint của API"""
    try:
        metrics_url = f"{base_url}/metrics"
        response = requests.get(metrics_url, timeout=5)
        
        if response.status_code == 200:
            metrics_text = response.text
            lines = metrics_text.split('\n')
            
            # Parse metrics
            metrics = {}
            for line in lines:
                if line and not line.startswith('#'):
                    if ' ' in line:
                        metric_name, value = line.split(' ', 1)
                        try:
                            metrics[metric_name] = float(value)
                        except ValueError:
                            metrics[metric_name] = value
            
            return {
                'api': api_name,
                'status': 'success',
                'metrics_count': len(metrics),
                'sample_metrics': dict(list(metrics.items())[:5])  # First 5 metrics
            }
        else:
            return {
                'api': api_name,
                'status': 'error',
                'status_code': response.status_code,
                'error': f"HTTP {response.status_code}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'api': api_name,
            'status': 'error',
            'error': str(e)
        }

def main():
    """Kiểm tra tất cả metrics endpoints"""
    print("🔍 Kiểm tra metrics endpoints...")
    print("=" * 50)
    
    for api_name, base_url in APIS.items():
        print(f"\n📊 Checking {api_name} ({base_url})...")
        result = check_metrics(api_name, base_url)
        
        if result['status'] == 'success':
            print(f"  ✅ Metrics available: {result['metrics_count']} metrics")
            print(f"  📈 Sample metrics:")
            for metric, value in result['sample_metrics'].items():
                print(f"    - {metric}: {value}")
        else:
            print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print("🎯 Để xem dữ liệu thật, hãy:")
    print("1. Chạy các API containers")
    print("2. Chạy script test_api_data.py để tạo load")
    print("3. Kiểm tra Grafana dashboard")

if __name__ == "__main__":
    main()
