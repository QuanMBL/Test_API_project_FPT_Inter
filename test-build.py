#!/usr/bin/env python3
"""
Script to test Docker build for all APIs
"""

import subprocess
import sys
import os
from pathlib import Path

def test_docker_build(api_dir, api_name):
    """Test Docker build for a specific API"""
    print(f"\n=== Testing {api_name} Docker Build ===")
    
    api_path = Path(api_dir)
    if not api_path.exists():
        print(f"❌ {api_name}: API directory not found")
        return False
    
    try:
        # Test Docker build
        cmd = ["docker", "build", "-t", f"{api_name}:test", str(api_path)]
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {api_name}: Docker build successful")
            return True
        else:
            print(f"❌ {api_name}: Docker build failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {api_name}: Docker build timed out")
        return False
    except Exception as e:
        print(f"❌ {api_name}: Docker build error: {str(e)}")
        return False

def main():
    """Main function to test all API builds"""
    print("🔍 Testing Docker builds for all APIs...")
    
    # Define API configurations
    apis = [
        ("api1", "user-api"),
        ("api2", "product-api"), 
        ("api3", "order-api"),
        ("api4", "payment-api")
    ]
    
    success_count = 0
    total_apis = len(apis)
    
    for api_dir, api_name in apis:
        if test_docker_build(api_dir, api_name):
            success_count += 1
    
    print(f"\n📊 Build Results: {success_count}/{total_apis} APIs built successfully")
    
    if success_count == total_apis:
        print("🎉 All APIs built successfully!")
        return 0
    else:
        print("⚠️  Some APIs failed to build")
        return 1

if __name__ == "__main__":
    sys.exit(main())
