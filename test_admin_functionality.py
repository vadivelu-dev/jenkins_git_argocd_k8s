#!/usr/bin/env python3
"""
Test script to add sample contacts and test admin functionality
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import config
import random

def add_sample_contacts():
    """Add sample contact data for testing admin functionality"""
    
    client = MongoClient(config.MONGODB_URI)
    db = client[config.MONGODB_DB]
    contacts_collection = db.contacts
    
    print("🧪 Adding sample contact data for testing...")
    
    # Sample contact data
    sample_contacts = [
        {
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'parking_type': 'Monthly',
            'message': 'I need a monthly parking spot near downtown. Looking for secure parking for my sedan.',
            'verified': False,
            'created_at': datetime.now() - timedelta(days=3)
        },
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.j@email.com',
            'parking_type': 'Daily',
            'message': 'Looking for daily parking options near the shopping center. Need wheelchair accessible space.',
            'verified': True,
            'created_at': datetime.now() - timedelta(days=1)
        },
        {
            'name': 'Mike Wilson',
            'email': 'mike.wilson@email.com',
            'parking_type': 'Hourly',
            'message': 'Need hourly parking for my business meetings downtown. Preferably covered parking.',
            'verified': False,
            'created_at': datetime.now() - timedelta(hours=5)
        },
        {
            'name': 'Emily Davis',
            'email': 'emily.davis@email.com',
            'parking_type': 'Event',
            'message': 'Looking for event parking for the concert next week. Will need parking for 3-4 hours.',
            'verified': False,
            'created_at': datetime.now() - timedelta(hours=2)
        },
        {
            'name': 'Test User Delete Me',
            'email': 'test.delete@example.com',
            'parking_type': 'Monthly',
            'message': 'This is a test contact that can be safely deleted for testing purposes.',
            'verified': False,
            'created_at': datetime.now()
        }
    ]
    
    try:
        # Clear existing test data
        contacts_collection.delete_many({'email': {'$regex': 'test.*@example.com'}})
        
        # Insert sample data
        result = contacts_collection.insert_many(sample_contacts)
        
        print(f"✅ Successfully added {len(result.inserted_ids)} sample contacts")
        
        # Display the inserted contacts with their IDs
        print("\n📋 Sample contacts added:")
        for i, contact_id in enumerate(result.inserted_ids):
            contact = contacts_collection.find_one({'_id': contact_id})
            status = "✅ Verified" if contact['verified'] else "⏳ Pending"
            print(f"   {i+1}. {contact['name']} ({contact['parking_type']}) - {status}")
            print(f"      ID: {contact_id}")
            print(f"      Email: {contact['email']}")
            print(f"      Message: {contact['message'][:50]}...")
            print()
        
        # Show total count
        total_count = contacts_collection.count_documents({})
        print(f"📊 Total contacts in database: {total_count}")
        
        client.close()
        
        print("\n🎯 You can now test the admin functionality:")
        print("   1. Visit: http://localhost:5000/admin/contacts")
        print("   2. Try deleting the 'Test User Delete Me' contact")
        print("   3. Try verifying unverified contacts")
        print("   4. View contact details")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        client.close()
        return False

def test_admin_operations():
    """Test admin operations programmatically"""
    
    client = MongoClient(config.MONGODB_URI)
    db = client[config.MONGODB_DB]
    contacts_collection = db.contacts
    
    print("\n🧪 Testing admin operations programmatically...")
    
    try:
        # Find a test contact to work with
        test_contact = contacts_collection.find_one({'email': 'test.delete@example.com'})
        
        if test_contact:
            contact_id = test_contact['_id']
            print(f"Found test contact: {contact_id}")
            
            # Test 1: Verify contact
            print("\n🔹 Test 1: Verify contact...")
            result = contacts_collection.update_one(
                {'_id': contact_id},
                {'$set': {'verified': True}}
            )
            if result.modified_count > 0:
                print("✅ Contact verification successful")
            else:
                print("❌ Contact verification failed")
            
            # Test 2: Read contact details
            print("\n🔹 Test 2: Read contact details...")
            contact = contacts_collection.find_one({'_id': contact_id})
            if contact:
                print(f"✅ Retrieved contact: {contact['name']}")
                print(f"   Verified: {contact.get('verified', False)}")
            else:
                print("❌ Failed to retrieve contact")
            
            # Test 3: Delete contact
            print("\n🔹 Test 3: Delete contact...")
            result = contacts_collection.delete_one({'_id': contact_id})
            if result.deleted_count > 0:
                print("✅ Contact deletion successful")
            else:
                print("❌ Contact deletion failed")
            
            # Verify deletion
            deleted_contact = contacts_collection.find_one({'_id': contact_id})
            if deleted_contact is None:
                print("✅ Contact successfully removed from database")
            else:
                print("❌ Contact still exists in database")
                
        else:
            print("⚠️  No test contact found to test operations")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error during admin operations test: {e}")
        client.close()

if __name__ == "__main__":
    print("🚀 ParkEasy Admin Functionality Test")
    print("=" * 50)
    
    success = add_sample_contacts()
    
    if success:
        response = input("\n🤔 Run programmatic admin operations test? (y/N): ")
        if response.lower() in ['y', 'yes']:
            test_admin_operations()
    
    print("\n✅ Test completed. You can now test the web interface!")
