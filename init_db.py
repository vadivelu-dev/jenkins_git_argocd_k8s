"""
Database initialization script for ParkEasy
Run this script to set up the MySQL database and tables
"""

import pymysql
import config

def create_database():
    """Create the database and tables"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DB}")
        print(f"Database '{config.MYSQL_DB}' created successfully!")
        
        # Use the database
        cursor.execute(f"USE {config.MYSQL_DB}")
        
        # Create contacts table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            parking_type VARCHAR(50) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_sql)
        print("Contacts table created successfully!")
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON contacts(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON contacts(created_at)")
        print("Indexes created successfully!")
        
        connection.commit()
        
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    create_database()
