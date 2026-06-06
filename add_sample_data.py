#!/usr/bin/env python3
"""
Test script to add sample contact data for demonstrating the verify/delete functionality.
"""

import pymysql
import config
from datetime import datetime

def add_sample_contacts():
    """Add sample contact submissions for testing"""
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
        
        sample_contacts = [
            {
                'name': 'John Smith',
                'email': 'john.smith@email.com',
                'parking_type': 'Monthly Parking',
                'message': 'Hi, I am looking for a monthly parking spot near my office in Whitefield. Could you please provide me with available options and pricing details? I need a secure parking space for my sedan.',
                'verified': False
            },
            {
                'name': 'Sarah Wilson',
                'email': 'sarah.wilson@email.com',
                'parking_type': 'Hourly Parking',
                'message': 'I need hourly parking for tomorrow evening. Will be visiting a friend and need parking for about 3-4 hours near Koramangala. Please let me know availability.',
                'verified': True
            },
            {
                'name': 'Mike Johnson',
                'email': 'mike.j@email.com',
                'parking_type': 'Event Parking',
                'message': 'Looking for event parking for a wedding at Palace Grounds. Need parking for approximately 100 guests. The event is scheduled for next month on the 15th.',
                'verified': False
            },
            {
                'name': 'Lisa Brown',
                'email': 'lisa.brown@email.com',
                'parking_type': 'Valet Service',
                'message': 'Interested in your valet parking service for a corporate event. We are expecting about 50 executives and would like premium parking arrangement.',
                'verified': True
            }
        ]
        
        with connection.cursor() as cursor:
            for contact in sample_contacts:
                cursor.execute("""
                    INSERT INTO contacts (name, email, parking_type, message, verified) 
                    VALUES (%(name)s, %(email)s, %(parking_type)s, %(message)s, %(verified)s)
                """, contact)
            
            connection.commit()
            print(f"✅ Successfully added {len(sample_contacts)} sample contact submissions")
                
    except Exception as e:
        print(f"❌ Error adding sample contacts: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    print("🔄 Adding sample contact submissions...")
    add_sample_contacts()
    print("✅ Sample data added! You can now test the admin functionality at http://127.0.0.1:5000/admin/contacts")
