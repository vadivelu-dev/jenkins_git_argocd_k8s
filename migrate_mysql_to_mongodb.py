#!/usr/bin/env python3
"""
MySQL to MongoDB Migration Script for ParkEasy Application
This script migrates contact data from MySQL to MongoDB.
"""

import pymysql
from pymongo import MongoClient
from datetime import datetime
import config

def migrate_mysql_to_mongodb():
    """Migrate data from MySQL to MongoDB"""
    
    # MongoDB connection
    mongo_client = MongoClient(config.MONGODB_URI)
    mongo_db = mongo_client[config.MONGODB_DB]
    contacts_collection = mongo_db.contacts
    
    try:
        # MySQL connection (using old configuration)
        mysql_connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='parkeasy_db',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with mysql_connection.cursor() as cursor:
            # Fetch all contacts from MySQL
            cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
            mysql_contacts = cursor.fetchall()
            
            print(f"📋 Found {len(mysql_contacts)} contacts in MySQL database")
            
            if len(mysql_contacts) == 0:
                print("ℹ️  No data to migrate from MySQL")
                return
            
            # Prepare documents for MongoDB
            mongo_documents = []
            for contact in mysql_contacts:
                mongo_doc = {
                    'name': contact['name'],
                    'email': contact['email'],
                    'parking_type': contact['parking_type'],
                    'message': contact['message'],
                    'verified': bool(contact.get('verified', False)),
                    'created_at': contact.get('created_at', datetime.now()),
                    'migrated_from_mysql': True,
                    'mysql_id': contact['id']  # Keep reference to original MySQL ID
                }
                mongo_documents.append(mongo_doc)
            
            # Insert all documents into MongoDB
            if mongo_documents:
                result = contacts_collection.insert_many(mongo_documents)
                print(f"✅ Successfully migrated {len(result.inserted_ids)} contacts to MongoDB")
                
                # Verify migration
                mongo_count = contacts_collection.count_documents({})
                print(f"📊 Total documents in MongoDB: {mongo_count}")
                
            else:
                print("⚠️  No valid documents to migrate")
        
        mysql_connection.close()
        print("✅ Migration completed successfully!")
        
    except pymysql.Error as mysql_error:
        print(f"❌ MySQL connection error: {mysql_error}")
        print("💡 This is normal if you've already switched to MongoDB and MySQL is not running")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        
    finally:
        mongo_client.close()

def verify_migration():
    """Verify the migration by showing sample data"""
    try:
        mongo_client = MongoClient(config.MONGODB_URI)
        mongo_db = mongo_client[config.MONGODB_DB]
        contacts_collection = mongo_db.contacts
        
        total_contacts = contacts_collection.count_documents({})
        migrated_contacts = contacts_collection.count_documents({'migrated_from_mysql': True})
        
        print(f"\n📊 Migration Summary:")
        print(f"   - Total contacts in MongoDB: {total_contacts}")
        print(f"   - Migrated from MySQL: {migrated_contacts}")
        print(f"   - Created directly in MongoDB: {total_contacts - migrated_contacts}")
        
        # Show sample data
        sample_contact = contacts_collection.find_one()
        if sample_contact:
            print(f"\n📝 Sample contact:")
            print(f"   - Name: {sample_contact.get('name', 'N/A')}")
            print(f"   - Email: {sample_contact.get('email', 'N/A')}")
            print(f"   - Parking Type: {sample_contact.get('parking_type', 'N/A')}")
            print(f"   - Created: {sample_contact.get('created_at', 'N/A')}")
            print(f"   - Verified: {sample_contact.get('verified', False)}")
        
        mongo_client.close()
        
    except Exception as e:
        print(f"❌ Verification error: {e}")

if __name__ == "__main__":
    print("🔄 Starting MySQL to MongoDB Migration...")
    print("=" * 50)
    
    print("\n⚠️  IMPORTANT: Make sure both MySQL and MongoDB are running!")
    print("   - This script will copy data from MySQL to MongoDB")
    print("   - Original MySQL data will remain unchanged")
    print("   - You can safely run this script multiple times")
    
    response = input("\n🤔 Do you want to proceed with migration? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        migrate_mysql_to_mongodb()
        verify_migration()
    else:
        print("❌ Migration cancelled")
