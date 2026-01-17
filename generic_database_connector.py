"""
Generic Database Connector Module

This module provides a unified, configuration-driven interface for connecting
to multiple database systems using a YAML configuration file.

Author: Database Team
Date: 2026-01-17
"""

import logging
import os
import importlib
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class GenericDatabaseConnector:
    """
    Generic database connector that works with multiple database systems.
    
    This class uses a YAML configuration file to determine connection parameters
    and behavior for different database types.
    
    Attributes:
        db_type (str): Type of database (mysql, postgresql, mongodb, etc.)
        config (Dict): Database configuration from YAML
        connection: Active database connection
        driver_module: Imported database driver module
    """
    
    def __init__(self, db_type: str, config_file: str = "database_config.yaml"):
        """
        Initialize generic database connector.
        
        Args:
            db_type (str): Database type (mysql, postgresql, mongodb, etc.)
            config_file (str): Path to YAML configuration file
        """
        self.db_type = db_type.lower()
        self.config_file = config_file
        self.config: Optional[Dict[str, Any]] = None
        self.connection = None
        self.driver_module = None
        
        # Load configuration
        self._load_config()
        
        # Import appropriate driver
        self._import_driver()
        
        logger.info(f"Generic connector initialized for {self.db_type}")
    
    def _load_config(self) -> None:
        """Load database configuration from YAML file."""
        try:
            with open(self.config_file, 'r') as f:
                all_configs = yaml.safe_load(f)
            
            if self.db_type not in all_configs['databases']:
                raise ValueError(f"Database type '{self.db_type}' not found in config")
            
            self.config = all_configs['databases'][self.db_type]
            logger.info(f"Configuration loaded for {self.db_type}")
            
        except FileNotFoundError:
            logger.error(f"Configuration file '{self.config_file}' not found")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            raise
    
    def _import_driver(self) -> None:
        """Dynamically import the database driver module."""
        try:
            driver_name = self.config['driver']
            
            # Handle different import patterns
            if '.' in driver_name:
                # e.g., "mysql.connector"
                self.driver_module = importlib.import_module(driver_name)
            else:
                # e.g., "pymongo"
                self.driver_module = importlib.import_module(driver_name)
            
            logger.info(f"Driver '{driver_name}' imported successfully")
            
        except ImportError as e:
            logger.error(f"Failed to import driver '{self.config['driver']}': {e}")
            raise
    
    def _resolve_env_vars(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve environment variables in connection parameters.
        
        Args:
            params (Dict): Connection parameters with ${VAR} placeholders
            
        Returns:
            Dict: Parameters with resolved environment variables
        """
        resolved = {}
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                resolved[key] = os.getenv(env_var, "")
            elif isinstance(value, list):
                resolved[key] = [self._resolve_env_vars({"item": item})["item"] 
                               if isinstance(item, str) else item for item in value]
            else:
                resolved[key] = value
        return resolved
    
    def connect(self) -> bool:
        """
        Establish connection to the database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Resolve environment variables in connection params
            conn_params = self._resolve_env_vars(self.config['connection_params'])
            
            # Convert port to int if present and not empty
            if 'port' in conn_params and conn_params['port']:
                try:
                    conn_params['port'] = int(conn_params['port'])
                except (ValueError, TypeError) as e:
                    logger.error(f"Invalid port value '{conn_params['port']}': {e}")
                    # Use default port if conversion fails
                    if 'default_port' in self.config:
                        conn_params['port'] = self.config['default_port']
                        logger.info(f"Using default port: {conn_params['port']}")
                    else:
                        raise ValueError(f"Invalid port value and no default port configured")
            
            # Database-specific connection logic
            if self.config['type'] == 'relational':
                self.connection = self._connect_relational(conn_params)
            elif self.config['type'] == 'nosql_document':
                self.connection = self._connect_nosql_document(conn_params)
            elif self.config['type'] == 'nosql_search':
                self.connection = self._connect_nosql_search(conn_params)
            elif self.config['type'] == 'nosql_wide_column':
                self.connection = self._connect_nosql_wide_column(conn_params)
            elif self.config['type'] == 'vector_database':
                self.connection = self._connect_vector_db(conn_params)
            elif self.config['type'] == 'data_warehouse':
                self.connection = self._connect_data_warehouse(conn_params)
            else:
                raise ValueError(f"Unknown database type: {self.config['type']}")
            
            logger.info(f"Successfully connected to {self.db_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to {self.db_type}: {e}")
            self.connection = None
            return False
    
    def _connect_relational(self, params: Dict[str, Any]) -> Any:
        """Connect to relational database (MySQL, PostgreSQL, Oracle, etc.)."""
        if self.db_type == 'mysql':
            return self.driver_module.connect(**params)
        elif self.db_type == 'postgresql':
            return self.driver_module.connect(**params)
        elif self.db_type == 'oracle':
            return self.driver_module.connect(**params)
        elif self.db_type in ['db2', 'sqlserver', 'netezza']:
            # These use connection strings
            conn_str = self._build_connection_string(params)
            return self.driver_module.connect(conn_str)
        else:
            raise ValueError(f"Unsupported relational database: {self.db_type}")
    
    def _connect_nosql_document(self, params: Dict[str, Any]) -> Any:
        """Connect to document database (MongoDB)."""
        from pymongo import MongoClient
        
        if params.get('username') and params.get('password'):
            client = MongoClient(
                host=params['host'],
                port=params['port'],
                username=params['username'],
                password=params['password']
            )
        else:
            client = MongoClient(host=params['host'], port=params['port'])
        
        return client
    
    def _connect_nosql_search(self, params: Dict[str, Any]) -> Any:
        """Connect to search engine (Elasticsearch)."""
        from elasticsearch import Elasticsearch
        
        if params.get('http_auth'):
            return Elasticsearch(
                params['hosts'],
                http_auth=tuple(params['http_auth'])
            )
        else:
            return Elasticsearch(params['hosts'])
    
    def _connect_nosql_wide_column(self, params: Dict[str, Any]) -> Any:
        """Connect to wide-column store (Cassandra)."""
        from cassandra.cluster import Cluster
        
        cluster = Cluster(
            contact_points=params['contact_points'],
            port=params['port']
        )
        return cluster.connect()
    
    def _connect_vector_db(self, params: Dict[str, Any]) -> Any:
        """Connect to vector database (Milvus)."""
        from pymilvus import connections
        
        connections.connect(
            alias="default",
            host=params['host'],
            port=params['port']
        )
        return connections
    
    def _connect_data_warehouse(self, params: Dict[str, Any]) -> Any:
        """Connect to data warehouse (Netezza)."""
        conn_str = self._build_connection_string(params)
        return self.driver_module.connect(conn_str)
    
    def _build_connection_string(self, params: Dict[str, Any]) -> str:
        """Build connection string for ODBC-based connections."""
        parts = []
        for key, value in params.items():
            if value:
                parts.append(f"{key}={value}")
        return ";".join(parts)
    
    def disconnect(self) -> None:
        """Close the database connection."""
        if self.connection:
            try:
                if hasattr(self.connection, 'close'):
                    self.connection.close()
                elif hasattr(self.connection, 'disconnect'):
                    self.connection.disconnect()
                
                logger.info(f"{self.db_type} connection closed successfully")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
            finally:
                self.connection = None
    
    def is_connected(self) -> bool:
        """
        Check if database connection is active.
        
        Returns:
            bool: True if connected, False otherwise
        """
        if not self.connection:
            return False
        
        try:
            # Database-specific connection check
            if self.config['type'] == 'relational':
                if hasattr(self.connection, 'is_connected'):
                    return self.connection.is_connected()
                elif hasattr(self.connection, 'closed'):
                    return not self.connection.closed
            elif self.config['type'] == 'nosql_document':
                # MongoDB check
                self.connection.admin.command('ping')
                return True
            elif self.config['type'] == 'nosql_search':
                # Elasticsearch check
                return self.connection.ping()
            
            return True
            
        except Exception:
            return False
    
    def get_connection(self) -> Any:
        """
        Get the current database connection.
        
        Returns:
            Connection object or None if not connected
        """
        if not self.is_connected():
            logger.warning("No active connection. Call connect() first.")
            return None
        return self.connection
    
    def get_query_syntax(self) -> Dict[str, str]:
        """
        Get database-specific query syntax.
        
        Returns:
            Dict: Query syntax configuration
        """
        return self.config.get('query_syntax', {})
    
    def get_features(self) -> List[str]:
        """
        Get list of supported features for this database.
        
        Returns:
            List[str]: Supported features
        """
        return self.config.get('features', [])
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


def main():
    """Example usage of GenericDatabaseConnector."""
    # Test MySQL connection
    print("\n=== Testing MySQL ===")
    with GenericDatabaseConnector("mysql") as db:
        if db.is_connected():
            logger.info("MySQL connection successful!")
            logger.info(f"Features: {db.get_features()}")
            logger.info(f"Query syntax: {db.get_query_syntax()}")
    
    # Test MongoDB connection
    print("\n=== Testing MongoDB ===")
    with GenericDatabaseConnector("mongodb") as db:
        if db.is_connected():
            logger.info("MongoDB connection successful!")
            logger.info(f"Features: {db.get_features()}")
    
    # Test PostgreSQL connection
    print("\n=== Testing PostgreSQL ===")
    with GenericDatabaseConnector("postgresql") as db:
        if db.is_connected():
            logger.info("PostgreSQL connection successful!")
            logger.info(f"Features: {db.get_features()}")


if __name__ == "__main__":
    main()

# Made with Bob
