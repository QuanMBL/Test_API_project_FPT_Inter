#!/usr/bin/env python3
"""
Test MongoDB connection with localhost
"""

import os
import sys

def test_local_mongodb():
    """Test MongoDB connection with localhost"""
    print("🔍 Testing MongoDB connection with localhost...")
    
    try:
        import mongoengine
        from mongoengine import connect, disconnect
        print("✅ mongoengine imported successfully")
    except ImportError:
        print("❌ mongoengine not installed")
        print("   Please install: pip install mongoengine==0.27.0")
        return False
    
    # Disconnect any existing connections
    try:
        disconnect()
    except:
        pass
    
    # Use localhost for testing
    mongodb_host = "localhost"
    mongodb_port = "27017"
    
    connection_string = f"mongodb://{mongodb_host}:{mongodb_port}/"
    print(f"   Connecting to: {connection_string}")
    
    try:
        # Connect to MongoDB
        connect(db='test_db', host=connection_string)
        print(f"✅ MongoDB connection successful")
        
        # Test with a simple operation
        from mongoengine import Document, StringField
        class TestDoc(Document):
            test_field = StringField()
            meta = {'collection': 'test_connection'}
        
        # Try to save and retrieve a test document
        test_doc = TestDoc(test_field="test")
        test_doc.save()
        print("✅ Test document saved successfully")
        
        # Clean up
        test_doc.delete()
        print("✅ Test document deleted successfully")
        
        # Disconnect
        disconnect()
        print("✅ Disconnected successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed")
        print(f"   Error: {str(e)}")
        print(f"\nTroubleshooting:")
        print(f"1. Make sure MongoDB is running on localhost:27017")
        print(f"2. For Docker: docker-compose up -d mongodb")
        print(f"3. Check if port 27017 is accessible")
        return False

def main():
    """Main function"""
    print("🚀 Local MongoDB Connection Test")
    print("=" * 40)
    
    if test_local_mongodb():
        print("\n🎉 MongoDB connection test successful!")
        print("\nYou can now test your APIs:")
        print("MONGODB_HOST=localhost python test-single-api.py userapi")
        return 0
    else:
        print("\n⚠️  MongoDB connection test failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
