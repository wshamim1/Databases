"""
MySQL Database Example

This example demonstrates how to use the generic framework with MySQL.
Shows basic CRUD operations and common patterns.
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generic_database_connector import GenericDatabaseConnector
from generic_database_manager import GenericDatabaseManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """MySQL example with CRUD operations."""
    
    # Connect to MySQL
    with GenericDatabaseConnector("mysql") as db:
        if not db.is_connected():
            logger.error("Failed to connect to MySQL")
            return
        
        logger.info("✅ Connected to MySQL successfully!")
        
        # Create manager
        manager = GenericDatabaseManager(db)
        
        # Create users table if it doesn't exist
        logger.info("\n=== Creating Table ===")
        cursor = db.get_connection().cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age INT,
                city VARCHAR(255)
            )
        """)
        db.get_connection().commit()
        cursor.close()
        logger.info("✅ Users table ready")
        
        # 1. INSERT - Add new users
        logger.info("\n=== INSERT Operations ===")
        user1 = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "city": "New York"
        }
        user_id = manager.insert_one("users", user1)
        logger.info(f"Inserted user with ID: {user_id}")
        
        # Insert multiple users
        users = [
            {"name": "Jane Smith", "email": "jane@example.com", "age": 25, "city": "Boston"},
            {"name": "Bob Johnson", "email": "bob@example.com", "age": 35, "city": "Chicago"},
            {"name": "Alice Brown", "email": "alice@example.com", "age": 28, "city": "Seattle"}
        ]
        
        for user in users:
            manager.insert_one("users", user)
        logger.info(f"Inserted {len(users)} more users")
        
        # 2. SELECT - Retrieve data
        logger.info("\n=== SELECT Operations ===")
        all_users = manager.find_all("users", limit=10)
        if all_users:
            logger.info(f"Found {len(all_users)} users:")
            for user in all_users:
                logger.info(f"  - {user.get('name')} ({user.get('email')})")
        else:
            logger.info("No users found")
        
        # 3. UPDATE - Modify data
        logger.info("\n=== UPDATE Operations ===")
        updated = manager.update_one(
            "users",
            {"name": "John Doe"},  # condition
            {"age": 31, "city": "San Francisco"}  # new data
        )
        logger.info(f"Updated {updated} user(s)")
        
        # 4. DELETE - Remove data
        logger.info("\n=== DELETE Operations ===")
        deleted = manager.delete_one("users", {"name": "Bob Johnson"})
        logger.info(f"Deleted {deleted} user(s)")
        
        # Final count
        final_users = manager.find_all("users", limit=100)
        if final_users:
            logger.info(f"\n✅ Final user count: {len(final_users)}")
        else:
            logger.info(f"\n✅ Final user count: 0")


if __name__ == "__main__":
    main()

# Made with Bob
