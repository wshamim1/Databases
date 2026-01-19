# Building a Universal Database Framework: One API to Rule Them All

## The Problem

Modern applications often need multiple database systems—PostgreSQL for transactions, MongoDB for documents, Redis for caching, Elasticsearch for search. Each database has its own API, connection pattern, and quirks. This creates:

- **API Inconsistency**: Different code for each database
- **Steep Learning Curve**: Multiple APIs to master
- **Maintenance Overhead**: More code to maintain and test
- **Testing Complexity**: Managing multiple database servers

## The Solution

We built a configuration-driven Python framework that provides a **unified API for 25+ database systems**. Write once, use everywhere.

```python
# Same code works with ANY database!
with GenericDatabaseConnector("mysql") as db:  # or "mongodb", "redis", etc.
    manager = GenericDatabaseManager(db)
    manager.insert_one("users", {"name": "John", "age": 30})
    users = manager.find_all("users")
```

[**→ View Full Code on GitHub**](https://github.com/YOUR_USERNAME/YOUR_REPO)

## Supported Databases (25+)

**Relational**: MySQL, PostgreSQL, Oracle, SQL Server, MariaDB, SQLite, and more  
**NoSQL**: MongoDB, CouchDB, Firestore, ArangoDB  
**Key-Value**: Redis, DynamoDB  
**Graph**: Neo4j, ArangoDB  
**Search**: Elasticsearch  
**Time Series**: InfluxDB, TimescaleDB  
**And more**: Cassandra, ClickHouse, Milvus

## Architecture

### 1. Configuration Layer
All databases defined in YAML—no code changes needed:

```yaml
databases:
  mysql:
    type: "relational"
    driver: "mysql.connector"
    connection_params:
      host: "${DB_HOST}"
      user: "${DB_USER}"
      password: "${DB_PASSWORD}"
```

[**→ See Full Configuration**](https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/database_config.yaml)

### 2. Universal Connector
One connector for all databases:

```python
with GenericDatabaseConnector("postgresql") as db:
    if db.is_connected():
        # Work with any database
```

### 3. Unified Operations
Same methods everywhere:

```python
manager = GenericDatabaseManager(db)

# Works with MySQL, MongoDB, Redis, etc.
manager.insert_one("table", data)
manager.find_all("table", limit=10)
manager.update_one("table", conditions, new_data)
manager.delete_one("table", conditions)
```

## Real-World Example: E-Commerce Platform

### Traditional Approach (Different APIs)
```python
# MySQL
mysql_cursor.execute("INSERT INTO orders VALUES (%s, %s)", (1, "John"))

# MongoDB
mongo_db.products.insert_one({"name": "Laptop", "price": 999})

# Redis
redis_client.set("session:123", "user_data")
```

### With Our Framework (Unified API)
```python
# Same pattern for all databases
mysql_mgr.insert_one("orders", order_data)
mongo_mgr.insert_one("products", product_data)
redis_mgr.insert_one("sessions", session_data)
```

[**→ See Complete Example**](https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/examples/multi_database_example.py)

## Key Features

### 🚀 Rapid Development
Switch databases without rewriting code:

```python
def save_data(db_type: str, data: dict):
    with GenericDatabaseConnector(db_type) as db:
        manager = GenericDatabaseManager(db)
        manager.insert_one("data", data)

save_data("mysql", data)      # Works
save_data("mongodb", data)    # Works
save_data("redis", data)      # Works
```

### 🧪 Easy Testing
Start 11 databases with one command:

```bash
./start-databases.sh start
```

Automatically starts MySQL, PostgreSQL, MongoDB, Redis, and 7 others with proper configuration.

[**→ Podman Setup Guide**](https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/PODMAN_SETUP.md)

### 🔒 Security Built-In
- Environment variables for credentials
- Parameterized queries (SQL injection prevention)
- No hardcoded passwords

### 📝 Type-Safe
Complete type hints throughout:

```python
def insert_one(
    self,
    table_name: str,
    data: Dict[str, Any]
) -> Optional[Any]:
```

## Adding New Databases

Just add configuration—no code changes:

```yaml
databases:
  new_database:
    type: "relational"
    driver: "new_db_driver"
    connection_params:
      host: "${DB_HOST}"
```

[**→ Configuration Reference**](https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/database_config.yaml)

## Performance Tips

**Connection Pooling**: Enabled via configuration  
**Batch Operations**: Use `insert_many()` for bulk inserts  
**Caching**: Combine Redis with other databases

```python
# Check cache first
cached = redis_mgr.find_one("cache", {"key": "user:123"})
if not cached:
    data = mysql_mgr.find_one("users", {"id": 123})
    redis_mgr.insert_one("cache", {"key": "user:123", "value": data})
```

## Getting Started

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/YOUR_REPO
cd Databases
pip install -r requirements.txt

# Start databases
./start-databases.sh start

# Run examples
cd examples
python3 mysql_example.py
python3 multi_database_example.py
```

[**→ Full Documentation**](https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/README.md)

## Why This Matters

**For Developers**: Learn one API, use 25+ databases  
**For Teams**: Consistent patterns across projects  
**For Projects**: Easy database migration and testing  
**For Learning**: Experiment with different databases quickly

## What's Next?

We're working on:
- Database-agnostic query builder
- Data migration tools between databases
- Performance monitoring
- Schema versioning

## Try It Yourself

The framework is production-ready and open source. Get started in 3 commands:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO && cd Databases
pip install -r requirements.txt
./start-databases.sh start
```

## Resources

- [**GitHub Repository**](https://github.com/YOUR_USERNAME/YOUR_REPO)
- [**Examples**](https://github.com/YOUR_USERNAME/YOUR_REPO/tree/main/examples)
- [**Configuration Guide**](https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/database_config.yaml)
- [**Podman Setup**](https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/PODMAN_SETUP.md)

---

**Built with ❤️ for developers who work with multiple databases**

**Tags**: #Python #Databases #MySQL #PostgreSQL #MongoDB #Redis #DevOps #OpenSource

**Version**: 2.0.0 | **Published**: January 2026