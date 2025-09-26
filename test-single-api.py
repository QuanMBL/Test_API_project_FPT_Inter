#!/usr/bin/env python3
"""
Script to test MongoDB connection for a single API
Usage: python test-single-api.py <api_name>
Example: python test-single-api.py userapi
"""

import os
import sys
import django
from pathlib import Path

def test_single_api(api_name):
    """Test MongoDB connection for a single API"""
    print(f"🔍 Testing {api_name} MongoDB Connection...")
    
    # Map API names to directories
    api_dirs = {
        'userapi': 'api1',
        'productapi': 'api2', 
        'orderapi': 'api3',
        'paymentapi': 'api4'
    }
    
    if api_name not in api_dirs:
        print(f"❌ Unknown API: {api_name}")
        print(f"Available APIs: {', '.join(api_dirs.keys())}")
        return False
    
    api_dir = api_dirs[api_name]
    api_path = Path(api_dir)
    
    if not api_path.exists():
        print(f"❌ {api_name}: API directory not found")
        return False
    
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
            disconnect()
        except:
            pass  # Ignore if no connection exists
        
        # Get MongoDB host and port from environment
        mongodb_host = os.getenv('MONGODB_HOST', 'mongodb')
        mongodb_port = os.getenv('MONGODB_PORT', '27017')
        
        # Test connection
        db_name = f"{api_name.replace('api', '')}_db"
        connection_string = f"mongodb://{mongodb_host}:{mongodb_port}/"
        
        # Connect to MongoDB
        connect(db=db_name, host=connection_string)
        
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
        
        # Disconnect
        disconnect()
        
    except Exception as e:
        print(f"❌ {api_name}: MongoDB connection failed")
        print(f"   Error: {str(e)}")
        return False
    
    return True

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python test-single-api.py <api_name>")
        print("Available APIs: userapi, productapi, orderapi, paymentapi")
        return 1
    
    api_name = sys.argv[1]
    
    if test_single_api(api_name):
        print(f"\n🎉 {api_name} connected successfully!")
        return 0
    else:
        print(f"\n⚠️  {api_name} connection failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
