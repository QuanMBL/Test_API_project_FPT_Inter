#!/usr/bin/env python3
"""
Script to install global dependencies needed for MongoDB integration
"""

import subprocess
import sys

def install_global_dependencies():
    """Install global dependencies"""
    print("🔍 Installing global dependencies...")
    
    dependencies = [
        "mongoengine==0.27.0",
        "pymongo==4.6.0",
        "Django==4.2.7",
        "djangorestframework==3.14.0",
        "django-cors-headers==4.3.1",
        "gunicorn==21.2.0"
    ]
    
    success_count = 0
    total_deps = len(dependencies)
    
    for dep in dependencies:
        print(f"\nInstalling {dep}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f"✅ {dep}: Installed successfully")
                success_count += 1
            else:
                print(f"❌ {dep}: Failed to install")
                print(f"   Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"❌ {dep}: Installation timed out")
        except Exception as e:
            print(f"❌ {dep}: Installation error: {str(e)}")
    
    print(f"\n📊 Installation Results: {success_count}/{total_deps} dependencies installed")
    
    if success_count == total_deps:
        print("🎉 All global dependencies installed successfully!")
        return 0
    else:
        print("⚠️  Some dependencies failed to install")
        return 1

if __name__ == "__main__":
    sys.exit(install_global_dependencies())
