#!/usr/bin/env python3
"""
Complete setup script for MongoDB integration
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {description}: Success")
            return True
        else:
            print(f"❌ {description}: Failed")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ {description}: Timed out")
        return False
    except Exception as e:
        print(f"❌ {description}: Error - {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up MongoDB integration for all APIs...")
    
    steps = [
        ("python install-global-deps.py", "Install global dependencies"),
        ("python test-mongodb-connection.py", "Test MongoDB connections"),
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for cmd, description in steps:
        if run_command(cmd, description):
            success_count += 1
        else:
            print(f"\n⚠️  Step failed: {description}")
            print("You may need to install dependencies manually:")
            print("pip install mongoengine==0.27.0 pymongo==4.6.0")
            break
    
    print(f"\n📊 Setup Results: {success_count}/{total_steps} steps completed")
    
    if success_count == total_steps:
        print("🎉 MongoDB integration setup completed successfully!")
        print("\nNext steps:")
        print("1. Start MongoDB: docker-compose up mongodb")
        print("2. Start APIs: docker-compose up --build")
        print("3. Test APIs: python test-mongodb-connection.py")
        return 0
    else:
        print("⚠️  Setup incomplete. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
