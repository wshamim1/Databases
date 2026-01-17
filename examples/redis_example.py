"""
Redis Database Example

This example demonstrates how to use the generic framework with Redis.
Shows key-value operations and caching patterns.
"""

import sys
sys.path.append('..')

from generic_database_connector import GenericDatabaseConnector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Redis example with key-value operations."""
    
    # Connect to Redis
    with GenericDatabaseConnector("redis") as db:
        if not db.is_connected():
            logger.error("Failed to connect to Redis")
            return
        
        logger.info("✅ Connected to Redis successfully!")
        
        # Get Redis connection
        redis_conn = db.get_connection()
        
        # 1. SET - Store values
        logger.info("\n=== SET Operations ===")
        redis_conn.set("user:1:name", "John Doe")
        redis_conn.set("user:1:email", "john@example.com")
        redis_conn.set("user:1:age", 30)
        logger.info("Stored user data in Redis")
        
        # Set with expiration (TTL)
        redis_conn.setex("session:abc123", 3600, "user_session_data")
        logger.info("Stored session with 1 hour expiration")
        
        # 2. GET - Retrieve values
        logger.info("\n=== GET Operations ===")
        name = redis_conn.get("user:1:name")
        email = redis_conn.get("user:1:email")
        age = redis_conn.get("user:1:age")
        logger.info(f"Retrieved user: {name}, {email}, age {age}")
        
        # 3. Hash operations
        logger.info("\n=== HASH Operations ===")
        redis_conn.hset("user:2", mapping={
            "name": "Jane Smith",
            "email": "jane@example.com",
            "age": "25"
        })
        logger.info("Stored user as hash")
        
        user2 = redis_conn.hgetall("user:2")
        logger.info(f"Retrieved hash: {user2}")
        
        # 4. List operations
        logger.info("\n=== LIST Operations ===")
        redis_conn.rpush("tasks", "task1", "task2", "task3")
        logger.info("Added tasks to list")
        
        task = redis_conn.lpop("tasks")
        logger.info(f"Popped task: {task}")
        
        # 5. Set operations
        logger.info("\n=== SET Operations ===")
        redis_conn.sadd("tags", "python", "redis", "database")
        logger.info("Added tags to set")
        
        tags = redis_conn.smembers("tags")
        logger.info(f"Tags: {tags}")
        
        # 6. Counter operations
        logger.info("\n=== COUNTER Operations ===")
        redis_conn.set("page:views", 0)
        redis_conn.incr("page:views")
        redis_conn.incr("page:views")
        redis_conn.incr("page:views")
        views = redis_conn.get("page:views")
        logger.info(f"Page views: {views}")
        
        # 7. Check existence
        logger.info("\n=== EXISTS Operations ===")
        exists = redis_conn.exists("user:1:name")
        logger.info(f"Key exists: {exists}")
        
        # 8. Delete keys
        logger.info("\n=== DELETE Operations ===")
        deleted = redis_conn.delete("user:1:name", "user:1:email", "user:1:age")
        logger.info(f"Deleted {deleted} keys")
        
        logger.info("\n✅ Redis operations completed!")


if __name__ == "__main__":
    main()

# Made with Bob
