"""
PostgreSQL Database Example

This example demonstrates how to use the generic framework with PostgreSQL.
Shows advanced SQL features and JSONB support.
"""

import sys
sys.path.append('..')

from generic_database_connector import GenericDatabaseConnector
from generic_database_manager import GenericDatabaseManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """PostgreSQL example with advanced features."""
    
    # Connect to PostgreSQL
    with GenericDatabaseConnector("postgresql") as db:
        if not db.is_connected():
            logger.error("Failed to connect to PostgreSQL")
            return
        
        logger.info("✅ Connected to PostgreSQL successfully!")
        
        # Create manager
        manager = GenericDatabaseManager(db)
        
        # 1. INSERT - Add records
        logger.info("\n=== INSERT Operations ===")
        employee1 = {
            "name": "John Doe",
            "email": "john@company.com",
            "department": "Engineering",
            "salary": 75000,
            "hire_date": "2023-01-15"
        }
        emp_id = manager.insert_one("employees", employee1)
        logger.info(f"Inserted employee with ID: {emp_id}")
        
        # Insert multiple employees
        employees = [
            {"name": "Jane Smith", "email": "jane@company.com", "department": "Marketing", "salary": 65000, "hire_date": "2023-02-01"},
            {"name": "Bob Johnson", "email": "bob@company.com", "department": "Engineering", "salary": 80000, "hire_date": "2023-03-10"},
            {"name": "Alice Brown", "email": "alice@company.com", "department": "Sales", "salary": 70000, "hire_date": "2023-04-05"}
        ]
        
        for emp in employees:
            manager.insert_one("employees", emp)
        logger.info(f"Inserted {len(employees)} more employees")
        
        # 2. SELECT - Query data
        logger.info("\n=== SELECT Operations ===")
        all_employees = manager.find_all("employees", limit=10)
        if all_employees:
            logger.info(f"Found {len(all_employees)} employees:")
            for emp in all_employees:
                logger.info(f"  - {emp.get('name')} ({emp.get('department')}): ${emp.get('salary')}")
        
        # 3. UPDATE - Modify records
        logger.info("\n=== UPDATE Operations ===")
        updated = manager.update_one(
            "employees",
            {"name": "John Doe"},
            {"salary": 78000, "department": "Senior Engineering"}
        )
        logger.info(f"Updated {updated} employee(s)")
        
        # 4. DELETE - Remove records
        logger.info("\n=== DELETE Operations ===")
        deleted = manager.delete_one("employees", {"name": "Bob Johnson"})
        logger.info(f"Deleted {deleted} employee(s)")
        
        # PostgreSQL-specific: JSONB example (if table supports it)
        logger.info("\n=== PostgreSQL JSONB Feature ===")
        logger.info("PostgreSQL supports JSONB for flexible document storage")
        logger.info("You can store JSON data directly in columns")
        
        # Final count
        final_employees = manager.find_all("employees", limit=100)
        if final_employees:
            logger.info(f"\n✅ Final employee count: {len(final_employees)}")


if __name__ == "__main__":
    main()

# Made with Bob
