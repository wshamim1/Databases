"""
Generic Database Manager Module

This module provides unified CRUD operations that work across all database types
using the generic connector and configuration-driven approach.

Author: Database Team
Date: 2026-01-17
"""

import logging
from typing import Optional, List, Dict, Any, Tuple, Union
from generic_database_connector import GenericDatabaseConnector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GenericDatabaseManager:
    """
    Generic database manager providing unified CRUD operations.
    
    This class adapts operations to work with different database types
    (relational, document, search, etc.) using configuration-driven logic.
    
    Attributes:
        connector (GenericDatabaseConnector): Database connector instance
        db_type (str): Type of database
        syntax (Dict): Database-specific query syntax
    """
    
    def __init__(self, connector: GenericDatabaseConnector):
        """
        Initialize generic database manager.
        
        Args:
            connector (GenericDatabaseConnector): Database connector instance
        """
        self.connector = connector
        self.db_type = connector.db_type
        self.syntax = connector.get_query_syntax()
        self.features = connector.get_features()
        
        logger.info(f"GenericDatabaseManager initialized for {self.db_type}")
    
    # ==================== INSERT OPERATIONS ====================
    
    def insert_one(self, table_or_collection: str, data: Dict[str, Any]) -> Optional[Any]:
        """
        Insert a single record/document.
        
        Args:
            table_or_collection (str): Table name (SQL) or collection name (NoSQL)
            data (Dict[str, Any]): Data to insert
            
        Returns:
            Inserted ID or result, None if error
        """
        if not self.connector.is_connected():
            logger.error("No database connection available")
            return None
        
        try:
            if self.connector.config['type'] == 'relational':
                return self._insert_one_relational(table_or_collection, data)
            elif self.connector.config['type'] == 'nosql_document':
                return self._insert_one_document(table_or_collection, data)
            elif self.connector.config['type'] == 'nosql_search':
                return self._insert_one_search(table_or_collection, data)
            else:
                logger.error(f"Insert not implemented for {self.connector.config['type']}")
                return None
                
        except Exception as e:
            logger.error(f"Error inserting data: {e}")
            return None
    
    def _insert_one_relational(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """Insert into relational database."""
        columns = ', '.join([f"{self.syntax.get('identifier_quote', '')}{col}{self.syntax.get('identifier_quote', '')}" 
                            for col in data.keys()])
        placeholders = ', '.join([self.syntax.get('placeholder', '?')] * len(data))
        
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.connector.connection.cursor()
        cursor.execute(query, tuple(data.values()))
        self.connector.connection.commit()
        
        last_id = cursor.lastrowid if hasattr(cursor, 'lastrowid') else None
        cursor.close()
        
        logger.info(f"Inserted record into {table}")
        return last_id
    
    def _insert_one_document(self, collection: str, data: Dict[str, Any]) -> Optional[str]:
        """Insert into document database (MongoDB)."""
        db = self.connector.connection[self.connector.config['connection_params']['database']]
        result = db[collection].insert_one(data)
        logger.info(f"Inserted document into {collection}")
        return str(result.inserted_id)
    
    def _insert_one_search(self, index: str, data: Dict[str, Any]) -> Optional[str]:
        """Insert into search engine (Elasticsearch)."""
        result = self.connector.connection.index(index=index, document=data)
        logger.info(f"Indexed document in {index}")
        return result['_id']
    
    # ==================== SELECT/QUERY OPERATIONS ====================
    
    def find_all(self, table_or_collection: str, limit: int = 100) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve all records/documents with optional limit.
        
        Args:
            table_or_collection (str): Table/collection name
            limit (int): Maximum number of records to return
            
        Returns:
            List of records/documents, None if error
        """
        if not self.connector.is_connected():
            logger.error("No database connection available")
            return None
        
        try:
            if self.connector.config['type'] == 'relational':
                return self._find_all_relational(table_or_collection, limit)
            elif self.connector.config['type'] == 'nosql_document':
                return self._find_all_document(table_or_collection, limit)
            elif self.connector.config['type'] == 'nosql_search':
                return self._find_all_search(table_or_collection, limit)
            else:
                logger.error(f"Find not implemented for {self.connector.config['type']}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving data: {e}")
            return None
    
    def _find_all_relational(self, table: str, limit: int) -> List[Dict[str, Any]]:
        """Find all in relational database."""
        limit_clause = self.syntax.get('limit_clause', 'LIMIT {limit}').format(limit=limit, offset=0)
        query = f"SELECT * FROM {table} {limit_clause}"
        
        cursor = self.connector.connection.cursor()
        cursor.execute(query)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Fetch results
        rows = cursor.fetchall()
        cursor.close()
        
        # Convert to list of dicts
        results = [dict(zip(columns, row)) for row in rows]
        logger.info(f"Retrieved {len(results)} records from {table}")
        return results
    
    def _find_all_document(self, collection: str, limit: int) -> List[Dict[str, Any]]:
        """Find all in document database."""
        db = self.connector.connection[self.connector.config['connection_params']['database']]
        results = list(db[collection].find().limit(limit))
        
        # Convert ObjectId to string
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        
        logger.info(f"Retrieved {len(results)} documents from {collection}")
        return results
    
    def _find_all_search(self, index: str, limit: int) -> List[Dict[str, Any]]:
        """Find all in search engine."""
        result = self.connector.connection.search(
            index=index,
            body={"query": {"match_all": {}}, "size": limit}
        )
        
        documents = [hit['_source'] for hit in result['hits']['hits']]
        logger.info(f"Retrieved {len(documents)} documents from {index}")
        return documents
    
    # ==================== UPDATE OPERATIONS ====================
    
    def update_one(self, table_or_collection: str, 
                   conditions: Dict[str, Any], 
                   data: Dict[str, Any]) -> Optional[int]:
        """
        Update a single record/document.
        
        Args:
            table_or_collection (str): Table/collection name
            conditions (Dict): WHERE/filter conditions
            data (Dict): Data to update
            
        Returns:
            Number of records updated, None if error
        """
        if not self.connector.is_connected():
            logger.error("No database connection available")
            return None
        
        try:
            if self.connector.config['type'] == 'relational':
                return self._update_one_relational(table_or_collection, conditions, data)
            elif self.connector.config['type'] == 'nosql_document':
                return self._update_one_document(table_or_collection, conditions, data)
            elif self.connector.config['type'] == 'nosql_search':
                return self._update_one_search(table_or_collection, conditions, data)
            else:
                logger.error(f"Update not implemented for {self.connector.config['type']}")
                return None
                
        except Exception as e:
            logger.error(f"Error updating data: {e}")
            return None
    
    def _update_one_relational(self, table: str, conditions: Dict[str, Any], 
                              data: Dict[str, Any]) -> int:
        """Update in relational database."""
        set_clause = ', '.join([f"{col} = {self.syntax.get('placeholder', '?')}" 
                               for col in data.keys()])
        where_clause = ' AND '.join([f"{col} = {self.syntax.get('placeholder', '?')}" 
                                    for col in conditions.keys()])
        
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = tuple(list(data.values()) + list(conditions.values()))
        
        cursor = self.connector.connection.cursor()
        cursor.execute(query, params)
        self.connector.connection.commit()
        
        row_count = cursor.rowcount
        cursor.close()
        
        logger.info(f"Updated {row_count} record(s) in {table}")
        return row_count
    
    def _update_one_document(self, collection: str, conditions: Dict[str, Any], 
                            data: Dict[str, Any]) -> int:
        """Update in document database."""
        db = self.connector.connection[self.connector.config['connection_params']['database']]
        result = db[collection].update_one(conditions, {"$set": data})
        logger.info(f"Updated {result.modified_count} document(s) in {collection}")
        return result.modified_count
    
    def _update_one_search(self, index: str, conditions: Dict[str, Any], 
                          data: Dict[str, Any]) -> int:
        """Update in search engine."""
        # Elasticsearch update by query
        result = self.connector.connection.update_by_query(
            index=index,
            body={
                "query": {"match": conditions},
                "script": {
                    "source": " ".join([f"ctx._source.{k} = params.{k}" for k in data.keys()]),
                    "params": data
                }
            }
        )
        logger.info(f"Updated {result['updated']} document(s) in {index}")
        return result['updated']
    
    # ==================== DELETE OPERATIONS ====================
    
    def delete_one(self, table_or_collection: str, 
                   conditions: Dict[str, Any]) -> Optional[int]:
        """
        Delete a single record/document.
        
        Args:
            table_or_collection (str): Table/collection name
            conditions (Dict): WHERE/filter conditions
            
        Returns:
            Number of records deleted, None if error
        """
        if not self.connector.is_connected():
            logger.error("No database connection available")
            return None
        
        try:
            if self.connector.config['type'] == 'relational':
                return self._delete_one_relational(table_or_collection, conditions)
            elif self.connector.config['type'] == 'nosql_document':
                return self._delete_one_document(table_or_collection, conditions)
            elif self.connector.config['type'] == 'nosql_search':
                return self._delete_one_search(table_or_collection, conditions)
            else:
                logger.error(f"Delete not implemented for {self.connector.config['type']}")
                return None
                
        except Exception as e:
            logger.error(f"Error deleting data: {e}")
            return None
    
    def _delete_one_relational(self, table: str, conditions: Dict[str, Any]) -> int:
        """Delete from relational database."""
        where_clause = ' AND '.join([f"{col} = {self.syntax.get('placeholder', '?')}" 
                                    for col in conditions.keys()])
        
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        cursor = self.connector.connection.cursor()
        cursor.execute(query, tuple(conditions.values()))
        self.connector.connection.commit()
        
        row_count = cursor.rowcount
        cursor.close()
        
        logger.info(f"Deleted {row_count} record(s) from {table}")
        return row_count
    
    def _delete_one_document(self, collection: str, conditions: Dict[str, Any]) -> int:
        """Delete from document database."""
        db = self.connector.connection[self.connector.config['connection_params']['database']]
        result = db[collection].delete_one(conditions)
        logger.info(f"Deleted {result.deleted_count} document(s) from {collection}")
        return result.deleted_count
    
    def _delete_one_search(self, index: str, conditions: Dict[str, Any]) -> int:
        """Delete from search engine."""
        result = self.connector.connection.delete_by_query(
            index=index,
            body={"query": {"match": conditions}}
        )
        logger.info(f"Deleted {result['deleted']} document(s) from {index}")
        return result['deleted']


def main():
    """Example usage of GenericDatabaseManager."""
    # Example with MySQL
    print("\n=== Testing MySQL Operations ===")
    with GenericDatabaseConnector("mysql") as db:
        if db.is_connected():
            manager = GenericDatabaseManager(db)
            
            # Insert
            user_data = {"name": "John Doe", "age": 30, "email": "john@example.com"}
            user_id = manager.insert_one("users", user_data)
            logger.info(f"Inserted user with ID: {user_id}")
            
            # Find all
            users = manager.find_all("users", limit=10)
            logger.info(f"Found {len(users) if users else 0} users")
            
            # Update
            updated = manager.update_one("users", {"name": "John Doe"}, {"age": 31})
            logger.info(f"Updated {updated} user(s)")
    
    # Example with MongoDB
    print("\n=== Testing MongoDB Operations ===")
    with GenericDatabaseConnector("mongodb") as db:
        if db.is_connected():
            manager = GenericDatabaseManager(db)
            
            # Insert
            doc_data = {"name": "Jane Smith", "age": 25, "city": "New York"}
            doc_id = manager.insert_one("users", doc_data)
            logger.info(f"Inserted document with ID: {doc_id}")
            
            # Find all
            docs = manager.find_all("users", limit=10)
            logger.info(f"Found {len(docs) if docs else 0} documents")


if __name__ == "__main__":
    main()

# Made with Bob
