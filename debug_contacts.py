#!/usr/bin/env python3
"""
Debug script to check contact data structure and identify issues
"""

import pymysql
import config

def debug_contacts():
    """Check the structure of contact data"""
    try:
        # Connect to database
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Get table structure
            cursor.execute("DESCRIBE contacts")
            columns = cursor.fetchall()
            print("📋 Table Structure:")
            for col in columns:
                print(f"  - {col['Field']}: {col['Type']} ({col['Null']}, {col['Key']}, {col['Default']})")
            
            print("\n" + "="*50)
            
            # Get sample data
            cursor.execute("SELECT * FROM contacts LIMIT 3")
            contacts = cursor.fetchall()
            
            print(f"\n📊 Sample Data ({len(contacts)} records):")
            for i, contact in enumerate(contacts, 1):
                print(f"\nContact {i}:")
                for key, value in contact.items():
                    print(f"  {key}: {value} ({type(value).__name__})")
                    
        print("\n✅ Debug completed successfully!")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    debug_contacts()
