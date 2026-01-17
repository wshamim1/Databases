# Generic Database Framework

A unified, configuration-driven Python framework for connecting to and managing 25+ different database systems with a single codebase.

## 🎯 Overview

This framework provides a **universal interface** for all major database systems. Everything is managed through configuration, making it easy to work with multiple databases using the same API.

## ✨ Key Features

- **25+ Database Support** - One codebase for all databases
- **Configuration-Driven** - Add databases via YAML config
- **Unified API** - Same methods work everywhere
- **Production-Ready** - Full error handling and logging
- **Type-Safe** - Complete type hints throughout
- **Easy to Extend** - Add new databases in minutes

## 📦 Supported Databases (25+)

### Relational (10)
- MySQL, PostgreSQL, Oracle, DB2, SQL Server
- MariaDB, SQLite, CockroachDB, TimescaleDB, Netezza

### NoSQL Document (4)
- MongoDB, CouchDB, Firestore, ArangoDB

### Key-Value (2)
- Redis, DynamoDB

### Wide Column (2)
- Cassandra, ScyllaDB

### Graph (2)
- Neo4j, ArangoDB

### Search (1)
- Elasticsearch

### Time Series (2)
- InfluxDB, TimescaleDB

### Columnar (1)
- ClickHouse

### Vector (1)
- Milvus

## 🚀 Quick Start

### Installation

```bash
# Install core dependencies
pip install -r requirements.txt

# Or install specific database drivers
pip install mysql-connector-python  # MySQL
pip install pymongo                 # MongoDB
pip install redis                   # Redis
# ... etc
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### Basic Usage

```python
from generic_database_connector import GenericDatabaseConnector
from generic_database_manager import GenericDatabaseManager

# Connect to ANY database
with GenericDatabaseConnector("mysql") as db:  # or "mongodb", "redis", etc.
    if db.is_connected():
        manager = GenericDatabaseManager(db)
        
        # INSERT - same for all databases
        manager.insert_one("users", {"name": "John", "age": 30})
        
        # SELECT - same for all databases
        users = manager.find_all("users", limit=10)
        
        # UPDATE - same for all databases
        manager.update_one("users", {"name": "John"}, {"age": 31})
        
        # DELETE - same for all databases
        manager.delete_one("users", {"name": "John"})
```

## 📁 Project Structure

```
Databases/
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── database_config.yaml            # Database configurations (25+ databases)
├── generic_database_connector.py   # Universal connector
├── generic_database_manager.py     # Unified CRUD operations
├── README.md                       # This file
└── examples/                       # Practical examples
    ├── README.md                   # Examples documentation
    ├── mysql_example.py            # MySQL example
    ├── mongodb_example.py          # MongoDB example
    ├── redis_example.py            # Redis example
    ├── postgresql_example.py       # PostgreSQL example
    └── multi_database_example.py   # Multi-database example
```

## 🔧 Configuration

### database_config.yaml

All database configurations in one file:

```yaml
databases:
  mysql:
    type: "relational"
    driver: "mysql.connector"
    default_port: 3306
    connection_params:
      host: "${DB_HOST}"
      user: "${DB_USER}"
      password: "${DB_PASSWORD}"
      database: "${DB_NAME}"
      port: "${PORT}"
    features:
      - connection_pooling
      - transactions
    query_syntax:
      placeholder: "%s"
      identifier_quote: "`"
```

### .env

Environment variables for credentials:

```ini
# MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=your_database
PORT=3306

# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB_NAME=test_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 💡 Examples

### Switch Databases Easily

```python
# Same code works with different databases!
def process_data(db_type: str):
    with GenericDatabaseConnector(db_type) as db:
        if db.is_connected():
            manager = GenericDatabaseManager(db)
            manager.insert_one("data", {"value": 100})
            return manager.find_all("data")

# Use with MySQL
mysql_data = process_data("mysql")

# Use with MongoDB - same code!
mongo_data = process_data("mongodb")

# Use with Redis - same code!
redis_data = process_data("redis")
```

### Multiple Databases

```python
# Connect to multiple databases simultaneously
with GenericDatabaseConnector("mysql") as mysql_db, \
     GenericDatabaseConnector("mongodb") as mongo_db, \
     GenericDatabaseConnector("redis") as redis_db:
    
    mysql_mgr = GenericDatabaseManager(mysql_db)
    mongo_mgr = GenericDatabaseManager(mongo_db)
    redis_mgr = GenericDatabaseManager(redis_db)
    
    # Use all three databases together
    # ...
```

### Real-World Example

See `examples/multi_database_example.py` for a complete e-commerce application using:
- MySQL for transactional data
- MongoDB for product catalog
- Redis for caching
- PostgreSQL for analytics

## 🎯 Adding New Databases

Simply add configuration to `database_config.yaml`:

```yaml
databases:
  new_database:
    type: "relational"
    driver: "new_db_driver"
    default_port: 5000
    connection_params:
      host: "${DB_HOST}"
      # ... other params
    features:
      - feature1
      - feature2
    query_syntax:
      placeholder: "?"
      identifier_quote: "\""
```

No code changes needed!

## 🔒 Security

- ✅ Environment variables for credentials
- ✅ Parameterized queries (SQL injection prevention)
- ✅ No hardcoded passwords
- ✅ .gitignore for sensitive files

## 🧪 Testing

```bash
# Test connection to any database
python generic_database_connector.py

# Test CRUD operations
python generic_database_manager.py

# Run examples
cd examples
python mysql_example.py
python mongodb_example.py
python multi_database_example.py
```

## 📚 Documentation

### In-Code Documentation
- Comprehensive docstrings
- Type hints throughout
- Usage examples in main()

### Configuration Files
- `database_config.yaml` - All database configs
- `.env.example` - Environment variable template
- `requirements.txt` - Dependencies with versions
- `examples/README.md` - Examples documentation

## 🎓 Use Cases

- **Multi-Database Applications** - Use different databases for different purposes
- **Database Migration** - Easy switching between databases
- **Testing** - Test with SQLite, deploy with PostgreSQL
- **Microservices** - Each service uses appropriate database
- **Data Integration** - Connect multiple databases simultaneously

## 🤝 Contributing

To add a new database:

1. Add configuration to `database_config.yaml`
2. Add driver to `requirements.txt`
3. Add environment variables to `.env.example`
4. Test connection and CRUD operations
5. Create example in `examples/` folder

## 📝 License

MIT License

## 🏆 Features

### Universal Interface
- One connector for 25+ databases
- One manager for all CRUD operations
- Consistent API everywhere

### Configuration-Driven
- Add databases via YAML
- No code changes needed
- Environment variable support

### Production Quality
- Comprehensive error handling
- Structured logging
- Type hints throughout
- Context managers
- Security best practices

## 📞 Support

For issues or questions:
- Check `database_config.yaml` for configuration options
- Review `.env.example` for required environment variables
- See `examples/` folder for practical examples
- Read code docstrings for detailed API documentation

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Databases
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Run examples**
   ```bash
   cd examples
   python mysql_example.py
   ```

5. **Build your application**
   ```python
   from generic_database_connector import GenericDatabaseConnector
   from generic_database_manager import GenericDatabaseManager
   
   # Your code here
   ```

---

**Version**: 2.0.0  
**Last Updated**: 2026-01-17  
**Status**: Production Ready

**Built with ❤️ for developers who work with multiple databases**