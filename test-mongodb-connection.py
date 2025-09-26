#!/usr/bin/env python3
"""
Script to test MongoDB connection for all APIs
"""

import os
import sys
import django
from pathlib import Path

def test_mongodb_connection(api_path, api_name):
    """Test MongoDB connection for a specific API"""
    print(f"\n=== Testing {api_name} MongoDB Connection ===")
    
    # Add the API path to Python path
    sys.path.insert(0, str(api_path))
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{api_name}.settings')
    
    try:
        # Setup Django
        django.setup()
        
        # Test MongoDB connection using mongoengine
        try:
            import mongoengine
            from mongoengine import connect, disconnect
        except ImportError:
            print(f"❌ {api_name}: mongoengine not installed")
            print(f"   Please install: pip install mongoengine==0.27.0")
            return False
        
        # Disconnect any existing connections first
        try:
            disconnect()  # Disconnect all connections
        except:
            pass  # Ignore if no connection exists
        
        # Get MongoDB host and port from environment
        mongodb_host = os.getenv('MONGODB_HOST', 'mongodb')
        mongodb_port = os.getenv('MONGODB_PORT', '27017')
        
        # Test connection
        db_name = f"{api_name.replace('api', '')}_db"
        connection_string = f"mongodb://{mongodb_host}:{mongodb_port}/"
        
        # Connect to MongoDB with unique alias
        connect(db=db_name, host=connection_string, alias=f"{api_name}_test")
        
        # Test with a simple operation
        from mongoengine import Document, StringField
        class TestDoc(Document):
            test_field = StringField()
            meta = {'collection': 'test_connection'}
        
        # Try to save and retrieve a test document
        test_doc = TestDoc(test_field="test")
        test_doc.save()
        test_doc.delete()
        
        print(f"✅ {api_name}: MongoDB connection successful")
        print(f"   Database: {db_name}")
        print(f"   Host: {connection_string}")
        
        # Disconnect using the specific alias
        disconnect(alias=f"{api_name}_test")
        
    except Exception as e:
        print(f"❌ {api_name}: MongoDB connection failed")
        print(f"   Error: {str(e)}")
        return False
    
    return True

def main():
    """Main function to test all APIs"""
    print("🔍 Testing MongoDB connections for all APIs...")
    
    # Define API configurations
    apis = [
        ("api1", "userapi"),
        ("api2", "productapi"), 
        ("api3", "orderapi"),
        ("api4", "paymentapi")
    ]
    
    success_count = 0
    total_apis = len(apis)
    
    for api_dir, api_name in apis:
        api_path = Path(api_dir)
        if api_path.exists():
            if test_mongodb_connection(api_path, api_name):
                success_count += 1
        else:
            print(f"❌ {api_name}: API directory not found")
    
    print(f"\n📊 Test Results: {success_count}/{total_apis} APIs connected successfully")
    
    if success_count == total_apis:
        print("🎉 All APIs are successfully connected to MongoDB!")
        return 0
    else:
        print("⚠️  Some APIs failed to connect to MongoDB")
        return 1

if __name__ == "__main__":
    sys.exit(main())
