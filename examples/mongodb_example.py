"""
MongoDB Database Example

This example demonstrates how to use the generic framework with MongoDB.
Shows document operations and NoSQL patterns.
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
    """MongoDB example with document operations."""
    
    # Connect to MongoDB
    with GenericDatabaseConnector("mongodb") as db:
        if not db.is_connected():
            logger.error("Failed to connect to MongoDB")
            return
        
        logger.info("✅ Connected to MongoDB successfully!")
        
        # Create manager
        manager = GenericDatabaseManager(db)
        
        # 1. INSERT - Add documents
        logger.info("\n=== INSERT Operations ===")
        product1 = {
            "name": "Laptop",
            "category": "Electronics",
            "price": 999.99,
            "specs": {
                "cpu": "Intel i7",
                "ram": "16GB",
                "storage": "512GB SSD"
            },
            "tags": ["computer", "portable", "work"]
        }
        product_id = manager.insert_one("products", product1)
        logger.info(f"Inserted product with ID: {product_id}")
        
        # Insert multiple products
        products = [
            {
                "name": "Mouse",
                "category": "Accessories",
                "price": 29.99,
                "tags": ["peripheral", "wireless"]
            },
            {
                "name": "Keyboard",
                "category": "Accessories",
                "price": 79.99,
                "tags": ["peripheral", "mechanical"]
            },
            {
                "name": "Monitor",
                "category": "Electronics",
                "price": 299.99,
                "specs": {"size": "27 inch", "resolution": "4K"},
                "tags": ["display", "4k"]
            }
        ]
        
        for product in products:
            manager.insert_one("products", product)
        logger.info(f"Inserted {len(products)} more products")
        
        # 2. FIND - Query documents
        logger.info("\n=== FIND Operations ===")
        all_products = manager.find_all("products", limit=10)
        if all_products:
            logger.info(f"Found {len(all_products)} products:")
            for product in all_products:
                logger.info(f"  - {product.get('name')}: ${product.get('price')}")
        
        # 3. UPDATE - Modify documents
        logger.info("\n=== UPDATE Operations ===")
        updated = manager.update_one(
            "products",
            {"name": "Laptop"},  # filter
            {"price": 899.99, "on_sale": True}  # update
        )
        logger.info(f"Updated {updated} product(s)")
        
        # 4. DELETE - Remove documents
        logger.info("\n=== DELETE Operations ===")
        deleted = manager.delete_one("products", {"name": "Mouse"})
        logger.info(f"Deleted {deleted} product(s)")
        
        # Final count
        final_products = manager.find_all("products", limit=100)
        if final_products:
            logger.info(f"\n✅ Final product count: {len(final_products)}")


if __name__ == "__main__":
    main()

# Made with Bob
