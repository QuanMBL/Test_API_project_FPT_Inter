#!/usr/bin/env python3
"""
Script to install dependencies for all APIs
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies(api_dir, api_name):
    """Install dependencies for a specific API"""
    print(f"\n=== Installing dependencies for {api_name} ===")
    
    api_path = Path(api_dir)
    requirements_file = api_path / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ {api_name}: requirements.txt not found")
        return False
    
    try:
        # Install dependencies
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {api_name}: Dependencies installed successfully")
            return True
        else:
            print(f"❌ {api_name}: Failed to install dependencies")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {api_name}: Installation timed out")
        return False
    except Exception as e:
        print(f"❌ {api_name}: Installation error: {str(e)}")
        return False

def main():
    """Main function to install dependencies for all APIs"""
    print("🔍 Installing dependencies for all APIs...")
    
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
        if install_dependencies(api_dir, api_name):
            success_count += 1
    
    print(f"\n📊 Installation Results: {success_count}/{total_apis} APIs installed successfully")
    
    if success_count == total_apis:
        print("🎉 All dependencies installed successfully!")
        print("\nYou can now run: python test-mongodb-connection.py")
        return 0
    else:
        print("⚠️  Some APIs failed to install dependencies")
        return 1

if __name__ == "__main__":
    sys.exit(main())
