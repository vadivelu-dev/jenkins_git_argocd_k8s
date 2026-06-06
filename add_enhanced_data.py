#!/usr/bin/env python3
"""
Enhanced sample data script for better charts and analytics
"""

import pymysql
import config
from datetime import datetime, timedelta
import random

def add_enhanced_sample_data():
    """Add diverse sample contact submissions for better charts"""
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
        
        # Enhanced sample data with variety
        parking_types = ['Hourly Parking', 'Daily Parking', 'Monthly Parking', 'Weekly Parking', 'Event Parking', 'Valet Service']
        names = ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown', 'Frank Miller', 'Grace Lee', 'Henry Taylor']
        
        sample_contacts = []
        
        # Generate data for last 7 days
        for i in range(20):
            # Random date within last 7 days
            days_ago = random.randint(0, 6)
            created_date = datetime.now() - timedelta(days=days_ago)
            
            # Random verified status (70% verified)
            verified = random.choice([True, True, True, False])  # 75% chance of being verified
            
            contact = {
                'name': random.choice(names),
                'email': f"user{i+10}@example.com",
                'parking_type': random.choice(parking_types),
                'message': f"Sample message for {random.choice(parking_types).lower()} request. Looking for convenient parking options.",
                'verified': verified,
                'created_at': created_date
            }
            sample_contacts.append(contact)
        
        with connection.cursor() as cursor:
            for contact in sample_contacts:
                cursor.execute("""
                    INSERT INTO contacts (name, email, parking_type, message, verified, created_at) 
                    VALUES (%(name)s, %(email)s, %(parking_type)s, %(message)s, %(verified)s, %(created_at)s)
                """, contact)
            
            connection.commit()
            print(f"✅ Successfully added {len(sample_contacts)} enhanced sample contact submissions")
                
    except Exception as e:
        print(f"❌ Error adding sample contacts: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    print("🔄 Adding enhanced sample contact submissions for better charts...")
    add_enhanced_sample_data()
    print("✅ Enhanced sample data added! You can now see better charts at http://127.0.0.1:5000/admin/reports")
