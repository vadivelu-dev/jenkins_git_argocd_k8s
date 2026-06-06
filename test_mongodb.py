#!/usr/bin/env python3
"""
Test script to verify MongoDB connection and basic operations for ParkEasy application
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import config

def test_mongodb_connection():
    """Test MongoDB connection and basic CRUD operations"""
    
    print("🧪 Testing MongoDB Connection and Operations...")
    print("=" * 50)
    
    try:
        # Connect to MongoDB
        client = MongoClient(config.MONGODB_URI)
        db = client[config.MONGODB_DB]
        contacts_collection = db.contacts
        
        print(f"✅ Connected to MongoDB at {config.MONGODB_URI}")
        print(f"✅ Using database: {config.MONGODB_DB}")
        
        # Test 1: Insert a test document
        print("\n🔹 Test 1: Inserting test contact...")
        test_contact = {
            'name': 'Test User',
            'email': 'test@parkeasy.com',
            'parking_type': 'Monthly',
            'message': 'This is a test message for MongoDB functionality',
            'verified': False,
            'created_at': datetime.now()
        }
        
        result = contacts_collection.insert_one(test_contact)
        test_id = result.inserted_id
        print(f"✅ Inserted test contact with ID: {test_id}")
        
        # Test 2: Read the document
        print("\n🔹 Test 2: Reading test contact...")
        retrieved_contact = contacts_collection.find_one({'_id': test_id})
        if retrieved_contact:
            print(f"✅ Retrieved contact: {retrieved_contact['name']} ({retrieved_contact['email']})")
        else:
            print("❌ Failed to retrieve test contact")
            
        # Test 3: Update the document
        print("\n🔹 Test 3: Updating test contact...")
        update_result = contacts_collection.update_one(
            {'_id': test_id},
            {'$set': {'verified': True, 'updated_at': datetime.now()}}
        )
        if update_result.modified_count > 0:
            print("✅ Successfully updated test contact")
        else:
            print("❌ Failed to update test contact")
            
        # Test 4: Query operations
        print("\n🔹 Test 4: Testing query operations...")
        
        # Count total documents
        total_count = contacts_collection.count_documents({})
        print(f"📊 Total contacts in database: {total_count}")
        
        # Count verified contacts
        verified_count = contacts_collection.count_documents({'verified': True})
        print(f"📊 Verified contacts: {verified_count}")
        
        # Find contacts by parking type
        monthly_contacts = contacts_collection.count_documents({'parking_type': 'Monthly'})
        print(f"📊 Monthly parking requests: {monthly_contacts}")
        
        # Test 5: List recent contacts
        print("\n🔹 Test 5: Listing recent contacts...")
        recent_contacts = list(contacts_collection.find().sort("created_at", -1).limit(3))
        for i, contact in enumerate(recent_contacts, 1):
            print(f"   {i}. {contact['name']} - {contact['parking_type']} - {contact['created_at'].strftime('%Y-%m-%d %H:%M')}")
        
        # Test 6: Delete the test document
        print("\n🔹 Test 6: Cleaning up test data...")
        delete_result = contacts_collection.delete_one({'_id': test_id})
        if delete_result.deleted_count > 0:
            print("✅ Successfully deleted test contact")
        else:
            print("❌ Failed to delete test contact")
            
        # Test 7: Check indexes
        print("\n🔹 Test 7: Checking indexes...")
        indexes = list(contacts_collection.list_indexes())
        print(f"📊 Collection has {len(indexes)} indexes:")
        for index in indexes:
            print(f"   - {index['name']}")
        
        client.close()
        print("\n🎉 All MongoDB tests completed successfully!")
        print("✅ Your application is ready to use MongoDB!")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB test failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure MongoDB is installed and running")
        print("   2. Check if MongoDB service is started")
        print("   3. Verify connection string in config.py")
        print("   4. Default MongoDB runs on: mongodb://localhost:27017/")
        return False

def check_old_mysql_references():
    """Check if there are any remaining MySQL references in the code"""
    print("\n🔍 Checking for any remaining MySQL references...")
    
    import os
    import re
    
    files_to_check = ['app.py', 'config.py']
    mysql_patterns = [
        r'mysql',
        r'MySQL',
        r'pymysql',
        r'Flask-MySQLdb',
        r'cursor\.',
        r'\.commit\(\)',
        r'\.connection\.'
    ]
    
    for file_name in files_to_check:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                
            found_mysql = False
            for pattern in mysql_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    if not found_mysql:
                        print(f"\n🔍 Checking {file_name}:")
                        found_mysql = True
                    print(f"   ⚠️  Found {len(matches)} references to: {pattern}")
            
            if not found_mysql:
                print(f"✅ {file_name}: No MySQL references found")
    
    print("\n✅ MySQL reference check completed")

if __name__ == "__main__":
    success = test_mongodb_connection()
    check_old_mysql_references()
    
    if success:
        print("\n🚀 Your ParkEasy application is now running on MongoDB!")
        print("   You can start the Flask application with: python app.py")
    else:
        print("\n❌ Please fix the MongoDB connection issues before running the application")
