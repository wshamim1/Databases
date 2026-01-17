# Podman Database Setup Guide

This guide explains how to use Podman to run all supported databases locally for development and testing.

## Prerequisites

### Install Podman

**macOS:**
```bash
brew install podman
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install podman
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install podman
```

**Windows:**
Download from [https://podman.io/getting-started/installation](https://podman.io/getting-started/installation)

### Install podman-compose

```bash
pip install podman-compose
```

## Quick Start

### 1. Start All Databases

```bash
./start-databases.sh start
```

This will start all 11 database containers:
- MySQL
- PostgreSQL
- MongoDB
- Redis
- Elasticsearch
- Cassandra
- Neo4j
- InfluxDB
- MariaDB
- CouchDB
- Milvus (with etcd and MinIO)

### 2. Check Status

```bash
./start-databases.sh status
```

### 3. View Connection Information

```bash
./start-databases.sh info
```

### 4. Stop All Databases

```bash
./start-databases.sh stop
```

## Working with Specific Databases

### Start a Specific Database

```bash
# Start only MySQL
./start-databases.sh start mysql

# Start only MongoDB
./start-databases.sh start mongodb

# Start only Redis
./start-databases.sh start redis
```

### Stop a Specific Database

```bash
./start-databases.sh stop mysql
```

### Restart a Specific Database

```bash
./start-databases.sh restart postgresql
```

### View Logs

```bash
# View all logs
./start-databases.sh logs

# View specific database logs
./start-databases.sh logs mysql
```

## Database Connection Details

### MySQL
```
Host: localhost
Port: 3306
User: testuser
Password: testpassword
Database: testdb
Root Password: rootpassword
```

**Connection String:**
```python
mysql://testuser:testpassword@localhost:3306/testdb
```

### PostgreSQL
```
Host: localhost
Port: 5432
User: testuser
Password: testpassword
Database: testdb
```

**Connection String:**
```python
postgresql://testuser:testpassword@localhost:5432/testdb
```

### MongoDB
```
Host: localhost
Port: 27017
User: testuser
Password: testpassword
Database: testdb
```

**Connection String:**
```python
mongodb://testuser:testpassword@localhost:27017/testdb?authSource=admin
```

### Redis
```
Host: localhost
Port: 6379
Password: testpassword
```

**Connection String:**
```python
redis://:testpassword@localhost:6379/0
```

### Elasticsearch
```
Host: localhost
Port: 9200
No authentication (development mode)
```

**Connection String:**
```python
http://localhost:9200
```

### Cassandra
```
Host: localhost
Port: 9042
Cluster: TestCluster
Datacenter: datacenter1
```

**Connection String:**
```python
localhost:9042
```

### Neo4j
```
HTTP: http://localhost:7474
Bolt: bolt://localhost:7687
User: neo4j
Password: testpassword
```

**Connection String:**
```python
bolt://neo4j:testpassword@localhost:7687
```

### InfluxDB
```
Host: localhost
Port: 8086
User: testuser
Password: testpassword
Organization: testorg
Bucket: testbucket
Token: test-token-please-change-in-production
```

**Connection String:**
```python
http://localhost:8086
```

### MariaDB
```
Host: localhost
Port: 3307 (Note: Different from MySQL)
User: testuser
Password: testpassword
Database: testdb
Root Password: rootpassword
```

**Connection String:**
```python
mysql://testuser:testpassword@localhost:3307/testdb
```

### CouchDB
```
Host: localhost
Port: 5984
User: testuser
Password: testpassword
```

**Connection String:**
```python
http://testuser:testpassword@localhost:5984
```

### Milvus
```
Host: localhost
Port: 19530
```

**Connection String:**
```python
localhost:19530
```

## Using with the Generic Framework

### Update .env File

After starting the databases, update your `.env` file:

```bash
# Copy example file
cp .env.example .env

# Edit with your preferred editor
nano .env
```

Example `.env` configuration:
```env
# MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=testuser
DB_PASSWORD=testpassword
DB_NAME=testdb

# PostgreSQL
PG_HOST=localhost
PG_PORT=5432
PG_USER=testuser
PG_PASSWORD=testpassword
PG_DATABASE=testdb

# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=testuser
MONGO_PASSWORD=testpassword
MONGO_DATABASE=testdb

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=testpassword

# Elasticsearch
ES_HOST=localhost
ES_PORT=9200

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=testpassword

# InfluxDB
INFLUX_URL=http://localhost:8086
INFLUX_TOKEN=test-token-please-change-in-production
INFLUX_ORG=testorg
INFLUX_BUCKET=testbucket

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### Run Examples

```bash
cd examples

# Test MySQL
python mysql_example.py

# Test MongoDB
python mongodb_example.py

# Test Redis
python redis_example.py

# Test PostgreSQL
python postgresql_example.py

# Test multi-database application
python multi_database_example.py
```

## Advanced Usage

### Using podman-compose Directly

```bash
# Start all services
podman-compose up -d

# Start specific services
podman-compose up -d mysql mongodb redis

# Stop all services
podman-compose down

# View logs
podman-compose logs -f mysql

# Restart services
podman-compose restart

# Remove containers and volumes
podman-compose down -v
```

### Accessing Database Shells

**MySQL:**
```bash
podman exec -it generic-db-mysql mysql -u testuser -ptestpassword testdb
```

**PostgreSQL:**
```bash
podman exec -it generic-db-postgresql psql -U testuser -d testdb
```

**MongoDB:**
```bash
podman exec -it generic-db-mongodb mongosh -u testuser -p testpassword --authenticationDatabase admin testdb
```

**Redis:**
```bash
podman exec -it generic-db-redis redis-cli -a testpassword
```

**Cassandra:**
```bash
podman exec -it generic-db-cassandra cqlsh
```

**Neo4j:**
```bash
podman exec -it generic-db-neo4j cypher-shell -u neo4j -p testpassword
```

### Inspecting Containers

```bash
# List running containers
podman ps

# View container details
podman inspect generic-db-mysql

# View container logs
podman logs generic-db-mysql

# View container stats
podman stats
```

### Managing Volumes

```bash
# List volumes
podman volume ls

# Inspect a volume
podman volume inspect generic-db-mysql_data

# Remove unused volumes
podman volume prune
```

## Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

```bash
# Check what's using the port
lsof -i :3306  # For MySQL
lsof -i :5432  # For PostgreSQL

# Stop the conflicting service or change the port in podman-compose.yml
```

### Container Won't Start

```bash
# Check logs
./start-databases.sh logs mysql

# Or use podman directly
podman logs generic-db-mysql

# Remove and recreate
podman-compose down
podman-compose up -d
```

### Connection Refused

Wait for the database to fully initialize:

```bash
# Check health status
podman ps

# Wait for "healthy" status
# Some databases (like Cassandra) take 30-60 seconds to start
```

### Out of Memory

Some databases (Elasticsearch, Cassandra) require significant memory:

```bash
# Check available memory
free -h

# Reduce memory limits in podman-compose.yml if needed
# Edit ES_JAVA_OPTS for Elasticsearch
```

### Permission Issues

```bash
# On Linux, you may need to adjust SELinux settings
sudo setsebool -P container_manage_cgroup on

# Or run with --privileged flag (not recommended for production)
```

## Cleanup

### Remove All Containers and Volumes

```bash
./start-databases.sh cleanup
```

This will:
1. Stop all running containers
2. Remove all containers
3. Remove all volumes (⚠️ **Data will be lost!**)

### Selective Cleanup

```bash
# Stop and remove specific container
podman-compose stop mysql
podman-compose rm mysql

# Remove specific volume
podman volume rm generic-db-mysql_data
```

## Production Considerations

⚠️ **Important:** This setup is for **development and testing only**. For production:

1. **Change all default passwords**
2. **Enable authentication** on all databases
3. **Use proper SSL/TLS certificates**
4. **Configure proper backup strategies**
5. **Set appropriate resource limits**
6. **Use persistent volumes** with proper backup
7. **Enable monitoring and logging**
8. **Follow security best practices** for each database

## Performance Tuning

### Adjust Resource Limits

Edit `podman-compose.yml` to add resource constraints:

```yaml
services:
  mysql:
    # ... existing config
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Optimize for Development

For faster startup and lower resource usage:

1. Reduce memory limits for Java-based databases (Elasticsearch, Cassandra)
2. Disable unnecessary features
3. Use smaller Docker images (alpine variants)
4. Limit the number of running databases to only what you need

## Additional Resources

- [Podman Documentation](https://docs.podman.io/)
- [podman-compose Documentation](https://github.com/containers/podman-compose)
- [Docker Compose Specification](https://docs.docker.com/compose/compose-file/)
- Individual database documentation for configuration options

## Support

For issues or questions:
1. Check the logs: `./start-databases.sh logs [database]`
2. Review the troubleshooting section above
3. Consult the official database documentation
4. Check Podman/container runtime logs

---

**Happy Database Development! 🚀**