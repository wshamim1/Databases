# Database Examples

This folder contains practical examples demonstrating how to use the generic database framework with different database systems.

## 📚 Available Examples

### 1. **mysql_example.py**
Basic CRUD operations with MySQL
- Connect to MySQL
- Insert single and multiple records
- Query data
- Update records
- Delete records

**Run:**
```bash
python mysql_example.py
```

### 2. **mongodb_example.py**
Document operations with MongoDB
- Connect to MongoDB
- Insert documents with nested data
- Query collections
- Update documents
- Delete documents

**Run:**
```bash
python mongodb_example.py
```

### 3. **redis_example.py**
Key-value operations with Redis
- Connect to Redis
- String operations (SET/GET)
- Hash operations (HSET/HGET)
- List operations (LPUSH/RPUSH)
- Set operations (SADD/SMEMBERS)
- Counter operations (INCR)
- TTL and expiration

**Run:**
```bash
python redis_example.py
```

### 4. **postgresql_example.py**
Advanced SQL with PostgreSQL
- Connect to PostgreSQL
- CRUD operations
- Advanced features (JSONB support)
- Transaction handling

**Run:**
```bash
python postgresql_example.py
```

### 5. **multi_database_example.py**
Using multiple databases together
- MySQL for transactional data
- MongoDB for product catalog
- Redis for caching
- PostgreSQL for analytics
- Real-world e-commerce scenario

**Run:**
```bash
python multi_database_example.py
```

## 🚀 Prerequisites

### 1. Install Dependencies
```bash
cd ..
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp ../.env.example ../.env

# Edit with your database credentials
nano ../.env
```

### 3. Ensure Databases are Running

**MySQL:**
```bash
# Check if MySQL is running
mysql -u root -p
```

**MongoDB:**
```bash
# Check if MongoDB is running
mongosh
```

**Redis:**
```bash
# Check if Redis is running
redis-cli ping
```

**PostgreSQL:**
```bash
# Check if PostgreSQL is running
psql -U postgres
```

## 📖 Example Structure

Each example follows this pattern:

```python
# 1. Import framework
from generic_database_connector import GenericDatabaseConnector
from generic_database_manager import GenericDatabaseManager

# 2. Connect to database
with GenericDatabaseConnector("database_name") as db:
    if db.is_connected():
        manager = GenericDatabaseManager(db)
        
        # 3. Perform operations
        manager.insert_one("table", data)
        results = manager.find_all("table")
        manager.update_one("table", conditions, new_data)
        manager.delete_one("table", conditions)
```

## 🎯 Learning Path

### Beginners
1. Start with `mysql_example.py` - Learn basic CRUD
2. Try `mongodb_example.py` - Understand NoSQL
3. Explore `redis_example.py` - Learn caching

### Intermediate
4. Study `postgresql_example.py` - Advanced SQL
5. Run `multi_database_example.py` - Real-world patterns

## 💡 Tips

### Modify Examples
Feel free to modify these examples:
- Change table/collection names
- Add more fields
- Try different queries
- Experiment with data

### Error Handling
All examples include basic error handling:
```python
if not db.is_connected():
    logger.error("Failed to connect")
    return
```

### Logging
Examples use Python logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🔧 Troubleshooting

### Connection Failed
- Check if database server is running
- Verify credentials in `.env` file
- Check firewall settings
- Ensure correct port numbers

### Import Errors
```bash
# Make sure you're in the examples directory
cd examples

# Install missing packages
pip install package_name
```

### Database Not Found
- Create the database first
- Check database name in `.env`
- Verify user permissions

## 📝 Creating Your Own Examples

Template for new examples:

```python
"""
Your Database Example

Description of what this example demonstrates.
"""

import sys
sys.path.append('..')

from generic_database_connector import GenericDatabaseConnector
from generic_database_manager import GenericDatabaseManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Your example description."""
    
    with GenericDatabaseConnector("your_database") as db:
        if not db.is_connected():
            logger.error("Failed to connect")
            return
        
        logger.info("✅ Connected successfully!")
        manager = GenericDatabaseManager(db)
        
        # Your code here
        
        logger.info("✅ Example completed!")


if __name__ == "__main__":
    main()
```

## 🎓 Next Steps

After running these examples:

1. **Explore More Databases**
   - Try Elasticsearch for search
   - Use Neo4j for graph data
   - Test InfluxDB for time-series

2. **Build Real Applications**
   - Combine multiple databases
   - Add error handling
   - Implement business logic

3. **Optimize Performance**
   - Use connection pooling
   - Implement caching strategies
   - Add batch operations

## 📞 Support

- Check main README.md for framework documentation
- Review database_config.yaml for configuration options
- See .env.example for required environment variables

---

**Happy Coding!** 🚀