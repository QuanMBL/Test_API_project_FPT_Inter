#!/usr/bin/env python3
"""
Simple MongoDB connection test without Django
"""

import os
import sys

def test_mongodb_connection():
    """Test MongoDB connection directly"""
    print("🔍 Testing MongoDB connection...")
    
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
    
    # Get MongoDB host and port from environment
    mongodb_host = os.getenv('MONGODB_HOST', 'localhost')
    mongodb_port = os.getenv('MONGODB_PORT', '27017')
    
    print(f"   Connecting to: {mongodb_host}:{mongodb_port}")
    
    connection_string = f"mongodb://{mongodb_host}:{mongodb_port}/"
    
    try:
        # Connect to MongoDB
        connect(db='test_db', host=connection_string)
        print(f"✅ MongoDB connection successful")
        print(f"   Host: {connection_string}")
        
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
        return False

def main():
    """Main function"""
    print("🚀 Simple MongoDB Connection Test")
    print("=" * 40)
    
    if test_mongodb_connection():
        print("\n🎉 MongoDB connection test successful!")
        return 0
    else:
        print("\n⚠️  MongoDB connection test failed")
        print("\nTroubleshooting:")
        print("1. Make sure MongoDB is running")
        print("2. Check if mongoengine is installed: pip install mongoengine==0.27.0")
        print("3. For Docker: docker-compose up mongodb")
        return 1

if __name__ == "__main__":
    sys.exit(main())
