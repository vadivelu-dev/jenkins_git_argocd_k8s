#!/usr/bin/env python3
"""
Database migration script to add the 'verified' column to existing contacts table.
Run this script to update your existing database with the new verify functionality.
"""

import pymysql
import config

def migrate_database():
    """Add verified column to contacts table if it doesn't exist"""
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
            # Check if verified column exists
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'contacts' 
                AND COLUMN_NAME = 'verified'
            """, (config.MYSQL_DB,))
            
            column_exists = cursor.fetchone()
            
            if not column_exists:
                # Add verified column
                cursor.execute("""
                    ALTER TABLE contacts 
                    ADD COLUMN verified BOOLEAN DEFAULT FALSE 
                    AFTER message
                """)
                connection.commit()
                print("✅ Successfully added 'verified' column to contacts table")
            else:
                print("ℹ️  'verified' column already exists in contacts table")
                
    except Exception as e:
        print(f"❌ Error migrating database: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    migrate_database()
    print("✅ Database migration completed!")
