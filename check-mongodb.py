#!/usr/bin/env python3
"""
Script to check MongoDB status
"""

import subprocess
import sys

def check_mongodb_status():
    """Check MongoDB container status"""
    print("🔍 Checking MongoDB status...")
    
    try:
        # Check if MongoDB container is running
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=mongodb-container", "--format", "table {{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if "mongodb-container" in output:
                print("✅ MongoDB container is running")
                print(output)
                return True
            else:
                print("❌ MongoDB container is not running")
                return False
        else:
            print("❌ Failed to check container status")
            return False
            
    except Exception as e:
        print(f"❌ Error checking MongoDB status: {str(e)}")
        return False

def check_mongodb_connection():
    """Check MongoDB connection"""
    print("🔍 Checking MongoDB connection...")
    
    try:
        # Try to connect to MongoDB
        result = subprocess.run(
            ["docker", "exec", "mongodb-container", "mongosh", "--eval", "db.runCommand('ping')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ MongoDB connection successful")
            return True
        else:
            print("❌ MongoDB connection failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ MongoDB connection timed out")
        return False
    except Exception as e:
        print(f"❌ MongoDB connection error: {str(e)}")
        return False

def show_mongodb_logs():
    """Show MongoDB logs"""
    print("📋 MongoDB logs (last 10 lines):")
    
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", "10", "mongodb-container"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("❌ Failed to get MongoDB logs")
            
    except Exception as e:
        print(f"❌ Error getting logs: {str(e)}")

def main():
    """Main function"""
    print("🔍 MongoDB Status Check")
    print("=" * 30)
    
    # Check container status
    container_running = check_mongodb_status()
    
    if not container_running:
        print("\n❌ MongoDB container is not running")
        print("\nTo start MongoDB:")
        print("1. Run: python start-mongodb.py")
        print("2. Or run: docker-compose up -d mongodb")
        return 1
    
    # Check connection
    connection_ok = check_mongodb_connection()
    
    if not connection_ok:
        print("\n❌ MongoDB connection failed")
        show_mongodb_logs()
        return 1
    
    print("\n✅ MongoDB is running and accessible!")
    print("\nYou can now test your APIs:")
    print("python test-single-api.py userapi")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
