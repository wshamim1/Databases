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

### Option 1: Podman Setup (Recommended)

Start all databases locally with one command:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start databases (auto-creates .env!)
./start-databases.sh start

# 3. Run examples
cd examples
python3 mysql_example.py
python3 multi_database_example.py
```

**That's it!** The script starts 11 databases and creates `.env` automatically.

### Option 2: Manual Setup

```bash
# 1. Install core dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with your credentials

# 3. Run examples
cd examples
python3 mysql_example.py
```

### Podman Commands

```bash
./start-databases.sh start      # Start all databases
./start-databases.sh stop       # Stop all databases
./start-databases.sh status     # Show container status
./start-databases.sh logs mysql # View logs
./start-databases.sh info       # Show connection info
./start-databases.sh env        # Create/update .env
./start-databases.sh cleanup    # Remove containers & volumes
```

See [PODMAN_SETUP.md](PODMAN_SETUP.md) for detailed Podman documentation.

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
├── BLOG_ARTICLE.md                 # Technical blog post
├── PODMAN_SETUP.md                 # Podman setup guide
├── podman-compose.yml              # Container definitions (11 databases)
├── start-databases.sh              # Database management script
└── examples/                       # Practical examples
    ├── README.md                   # Examples documentation
    ├── mysql_example.py            # MySQL example (with table creation)
    ├── mongodb_example.py          # MongoDB example
    ├── redis_example.py            # Redis example
    ├── postgresql_example.py       # PostgreSQL example (with table creation)
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

### With Podman (Recommended)

```bash
# Start databases
./start-databases.sh start

# Wait for databases to be healthy (30-60 seconds)
./start-databases.sh status

# Run examples (tables auto-create)
cd examples
python3 mysql_example.py
python3 mongodb_example.py
python3 postgresql_example.py
python3 redis_example.py
python3 multi_database_example.py
```

### Manual Testing

```bash
# Test connection to any database
python3 generic_database_connector.py

# Test CRUD operations
python3 generic_database_manager.py

# Run examples
cd examples
python3 mysql_example.py
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

### Quick Start (3 Commands)

```bash
git clone <repository-url> && cd Databases
pip install -r requirements.txt
./start-databases.sh start
```

### Detailed Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Databases
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install podman-compose  # For Podman support
   ```

3. **Start databases (Podman)**
   ```bash
   ./start-databases.sh start
   # This starts 11 databases and creates .env automatically
   ```

4. **Run examples**
   ```bash
   cd examples
   python3 mysql_example.py
   python3 multi_database_example.py
   ```

5. **Build your application**
   ```python
   from generic_database_connector import GenericDatabaseConnector
   from generic_database_manager import GenericDatabaseManager
   
   # Connect to any database
   with GenericDatabaseConnector("mysql") as db:
       manager = GenericDatabaseManager(db)
       # Your code here
   ```

### Available Databases (Podman)

When you run `./start-databases.sh start`, you get:
- MySQL (port 3306)
- PostgreSQL (port 5432)
- MongoDB (port 27017)
- Redis (port 6379)
- Elasticsearch (port 9200)
- Cassandra (port 9042)
- Neo4j (ports 7474, 7687)
- InfluxDB (port 8086)
- MariaDB (port 3307)
- CouchDB (port 5984)
- Milvus (port 19530)

---

**Version**: 2.0.0  
**Last Updated**: 2026-01-17  
**Status**: Production Ready

**Built with ❤️ for developers who work with multiple databases**