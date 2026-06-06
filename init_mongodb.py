#!/usr/bin/env python3
"""
MongoDB Database Initialization Script for ParkEasy Application
This script creates the necessary database and collections for the ParkEasy parking application.
"""

from pymongo import MongoClient
from datetime import datetime
import config

def init_mongodb():
    """Initialize MongoDB database and collections"""
    try:
        # Connect to MongoDB
        client = MongoClient(config.MONGODB_URI)
        
        # Create database
        db = client[config.MONGODB_DB]
        
        # Create contacts collection with indexes for better performance
        contacts_collection = db.contacts
        
        # Create indexes for better query performance
        contacts_collection.create_index("email")
        contacts_collection.create_index("created_at")
        contacts_collection.create_index("parking_type")
        contacts_collection.create_index("verified")
        
        print(f"✅ Successfully connected to MongoDB at {config.MONGODB_URI}")
        print(f"✅ Database '{config.MONGODB_DB}' is ready")
        print(f"✅ Collection 'contacts' created with indexes")
        
        # Test the connection by inserting a sample document (optional)
        test_doc = {
            'name': 'Test User',
            'email': 'test@example.com',
            'parking_type': 'Monthly',
            'message': 'This is a test message for MongoDB connection',
            'verified': False,
            'created_at': datetime.now()
        }
        
        # Insert and then immediately delete the test document
        result = contacts_collection.insert_one(test_doc)
        contacts_collection.delete_one({'_id': result.inserted_id})
        
        print("✅ MongoDB connection test successful")
        print("\n🎉 MongoDB database is ready for your ParkEasy application!")
        
        # Display collection stats
        stats = db.command("collstats", "contacts")
        print(f"\n📊 Collection stats:")
        print(f"   - Documents: {stats.get('count', 0)}")
        print(f"   - Storage size: {stats.get('storageSize', 0)} bytes")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error initializing MongoDB: {e}")
        print("\n💡 Make sure MongoDB is running on your system:")
        print("   - Download MongoDB Community Server from: https://www.mongodb.com/try/download/community")
        print("   - Start MongoDB service")
        print("   - Default connection: mongodb://localhost:27017/")

if __name__ == "__main__":
    print("🚀 Initializing MongoDB for ParkEasy Application...")
    print("=" * 50)
    init_mongodb()
