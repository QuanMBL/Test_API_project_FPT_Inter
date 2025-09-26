#!/usr/bin/env python3
"""
Script to start MongoDB and test connection
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_docker():
    """Check if Docker is running"""
    print("🔍 Checking Docker...")
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
        else:
            print("❌ Docker not available")
            return False
    except FileNotFoundError:
        print("❌ Docker not found")
        return False

def start_mongodb():
    """Start MongoDB using Docker Compose"""
    print("🚀 Starting MongoDB...")
    
    try:
        # Start MongoDB service
        result = subprocess.run(
            ["docker-compose", "up", "-d", "mongodb"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ MongoDB started successfully")
            return True
        else:
            print("❌ Failed to start MongoDB")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ MongoDB startup timed out")
        return False
    except Exception as e:
        print(f"❌ Error starting MongoDB: {str(e)}")
        return False

def wait_for_mongodb():
    """Wait for MongoDB to be ready"""
    print("⏳ Waiting for MongoDB to be ready...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            # Try to connect to MongoDB
            result = subprocess.run(
                ["docker", "exec", "mongodb-container", "mongosh", "--eval", "db.runCommand('ping')"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✅ MongoDB is ready")
                return True
                
        except subprocess.TimeoutExpired:
            pass
        except Exception:
            pass
        
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ MongoDB not ready after 60 seconds")
    return False

def test_connection():
    """Test MongoDB connection"""
    print("🧪 Testing MongoDB connection...")
    
    try:
        result = subprocess.run(
            ["python", "test-mongodb-simple.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ MongoDB connection test successful")
            print(result.stdout)
            return True
        else:
            print("❌ MongoDB connection test failed")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Connection test timed out")
        return False
    except Exception as e:
        print(f"❌ Connection test error: {str(e)}")
        return False

def main():
    """Main function"""
    print("🚀 MongoDB Setup and Test")
    print("=" * 40)
    
    # Check Docker
    if not check_docker():
        print("\n❌ Docker is not available")
        print("Please install Docker Desktop and try again")
        return 1
    
    # Start MongoDB
    if not start_mongodb():
        print("\n❌ Failed to start MongoDB")
        return 1
    
    # Wait for MongoDB to be ready
    if not wait_for_mongodb():
        print("\n❌ MongoDB is not ready")
        return 1
    
    # Test connection
    if not test_connection():
        print("\n❌ MongoDB connection test failed")
        return 1
    
    print("\n🎉 MongoDB is running and ready!")
    print("\nNext steps:")
    print("1. Test APIs: python test-single-api.py userapi")
    print("2. Start all services: docker-compose up --build")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
