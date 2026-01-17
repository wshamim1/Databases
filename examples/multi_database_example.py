"""
Multi-Database Example

This example demonstrates how to use multiple databases simultaneously
in a single application using the generic framework.
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
    """Example using multiple databases together."""
    
    logger.info("=== Multi-Database Application Example ===\n")
    
    # Scenario: E-commerce application using different databases for different purposes
    
    # 1. MySQL for transactional data (orders, customers)
    logger.info("1. Using MySQL for transactional data...")
    with GenericDatabaseConnector("mysql") as mysql_db:
        if mysql_db.is_connected():
            mysql_mgr = GenericDatabaseManager(mysql_db)
            
            # Store order
            order = {
                "order_id": "ORD-001",
                "customer_id": "CUST-123",
                "total": 299.99,
                "status": "pending"
            }
            mysql_mgr.insert_one("orders", order)
            logger.info(f"✅ Stored order in MySQL: {order['order_id']}")
    
    # 2. MongoDB for product catalog (flexible schema)
    logger.info("\n2. Using MongoDB for product catalog...")
    with GenericDatabaseConnector("mongodb") as mongo_db:
        if mongo_db.is_connected():
            mongo_mgr = GenericDatabaseManager(mongo_db)
            
            # Store product with flexible attributes
            product = {
                "sku": "LAPTOP-001",
                "name": "Gaming Laptop",
                "price": 1299.99,
                "specs": {
                    "cpu": "Intel i9",
                    "gpu": "RTX 4080",
                    "ram": "32GB"
                },
                "tags": ["gaming", "high-performance"],
                "reviews": []
            }
            mongo_mgr.insert_one("products", product)
            logger.info(f"✅ Stored product in MongoDB: {product['sku']}")
    
    # 3. Redis for caching and sessions
    logger.info("\n3. Using Redis for caching...")
    with GenericDatabaseConnector("redis") as redis_db:
        if redis_db.is_connected():
            redis_conn = redis_db.get_connection()
            
            # Cache user session
            redis_conn.setex("session:user123", 3600, "active")
            
            # Cache frequently accessed data
            redis_conn.set("product:LAPTOP-001:views", 0)
            redis_conn.incr("product:LAPTOP-001:views")
            
            views = redis_conn.get("product:LAPTOP-001:views")
            logger.info(f"✅ Cached session and product views in Redis: {views} views")
    
    # 4. PostgreSQL for analytics (with JSONB support)
    logger.info("\n4. Using PostgreSQL for analytics...")
    with GenericDatabaseConnector("postgresql") as pg_db:
        if pg_db.is_connected():
            pg_mgr = GenericDatabaseManager(pg_db)
            
            # Store analytics event
            event = {
                "event_type": "page_view",
                "user_id": "CUST-123",
                "page": "/product/LAPTOP-001",
                "timestamp": "2024-01-17T10:30:00"
            }
            pg_mgr.insert_one("analytics_events", event)
            logger.info(f"✅ Stored analytics event in PostgreSQL")
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("✅ Multi-Database Application Complete!")
    logger.info("="*50)
    logger.info("\nDatabase Usage Summary:")
    logger.info("  • MySQL      → Transactional data (orders, customers)")
    logger.info("  • MongoDB    → Product catalog (flexible schema)")
    logger.info("  • Redis      → Caching & sessions (fast access)")
    logger.info("  • PostgreSQL → Analytics (complex queries)")
    logger.info("\nAll using the SAME generic framework! 🎉")


if __name__ == "__main__":
    main()

# Made with Bob
