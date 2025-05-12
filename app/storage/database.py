"""
Database manager class for handling database operations.
Provides methods for storing and retrieving data from SQLite/PostgreSQL databases.
"""

import pandas as pd
import sqlite3
import psycopg2
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_type: str = 'sqlite', db_name: str = 'data.db',
                 host: Optional[str] = None, port: Optional[int] = None,
                 user: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the database manager.
        
        Args:
            db_type (str): Database type ('sqlite' or 'postgresql')
            db_name (str): Database name or file path
            host (Optional[str]): Database host (for PostgreSQL)
            port (Optional[int]): Database port (for PostgreSQL)
            user (Optional[str]): Database user (for PostgreSQL)
            password (Optional[str]): Database password (for PostgreSQL)
        """
        self.db_type = db_type
        self.db_name = db_name
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.engine = self._create_engine()
    
    def _create_engine(self) -> Engine:
        """
        Create SQLAlchemy engine based on database type.
        
        Returns:
            Engine: SQLAlchemy engine
        """
        try:
            if self.db_type == 'sqlite':
                return create_engine(f'sqlite:///{self.db_name}')
            elif self.db_type == 'postgresql':
                return create_engine(
                    f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
                )
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            logger.error(f"Error creating database engine: {str(e)}")
            raise
    
    def create_tables(self, schema: Dict[str, str]) -> None:
        """
        Create database tables based on schema.
        
        Args:
            schema (Dict[str, str]): Dictionary mapping table names to CREATE TABLE statements
        """
        try:
            with self.engine.connect() as conn:
                for table_name, create_stmt in schema.items():
                    conn.execute(text(create_stmt))
                    conn.commit()
            
            logger.info(f"Created tables: {list(schema.keys())}")
            
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise
    
    def store_dataframe(self, df: pd.DataFrame, table_name: str,
                       if_exists: str = 'replace') -> None:
        """
        Store DataFrame in database table.
        
        Args:
            df (pd.DataFrame): DataFrame to store
            table_name (str): Target table name
            if_exists (str): How to behave if table exists ('fail', 'replace', or 'append')
        """
        try:
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False
            )
            
            logger.info(f"Stored DataFrame in table: {table_name}")
            
        except Exception as e:
            logger.error(f"Error storing DataFrame: {str(e)}")
            raise
    
    def read_dataframe(self, table_name: str,
                      query: Optional[str] = None) -> pd.DataFrame:
        """
        Read DataFrame from database table.
        
        Args:
            table_name (str): Source table name
            query (Optional[str]): Custom SQL query
            
        Returns:
            pd.DataFrame: Retrieved DataFrame
        """
        try:
            if query:
                return pd.read_sql(query, self.engine)
            else:
                return pd.read_sql_table(table_name, self.engine)
            
        except Exception as e:
            logger.error(f"Error reading DataFrame: {str(e)}")
            raise
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute custom SQL query.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Dict[str, Any]]): Query parameters
            
        Returns:
            Any: Query result
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                return result.fetchall()
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def store_json(self, data: Dict[str, Any], table_name: str,
                  key_column: str = 'id') -> None:
        """
        Store JSON data in database table.
        
        Args:
            data (Dict[str, Any]): JSON data to store
            table_name (str): Target table name
            key_column (str): Column name for the key
        """
        try:
            # Convert JSON to DataFrame
            df = pd.DataFrame([{
                key_column: k,
                'data': json.dumps(v)
            } for k, v in data.items()])
            
            # Store in database
            self.store_dataframe(df, table_name)
            
            logger.info(f"Stored JSON data in table: {table_name}")
            
        except Exception as e:
            logger.error(f"Error storing JSON data: {str(e)}")
            raise
    
    def read_json(self, table_name: str,
                 key_column: str = 'id') -> Dict[str, Any]:
        """
        Read JSON data from database table.
        
        Args:
            table_name (str): Source table name
            key_column (str): Column name for the key
            
        Returns:
            Dict[str, Any]: Retrieved JSON data
        """
        try:
            # Read from database
            df = self.read_dataframe(table_name)
            
            # Convert to dictionary
            return {
                row[key_column]: json.loads(row['data'])
                for _, row in df.iterrows()
            }
            
        except Exception as e:
            logger.error(f"Error reading JSON data: {str(e)}")
            raise
    
    def backup_database(self, backup_path: str) -> None:
        """
        Create database backup.
        
        Args:
            backup_path (str): Path to store backup
        """
        try:
            if self.db_type == 'sqlite':
                # SQLite backup
                with sqlite3.connect(self.db_name) as src:
                    with sqlite3.connect(backup_path) as dst:
                        src.backup(dst)
            elif self.db_type == 'postgresql':
                # PostgreSQL backup
                with psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.db_name,
                    user=self.user,
                    password=self.password
                ) as conn:
                    with open(backup_path, 'w') as f:
                        conn.cursor().copy_to(f, 'SELECT * FROM pg_dump')
            
            logger.info(f"Created database backup: {backup_path}")
            
        except Exception as e:
            logger.error(f"Error creating database backup: {str(e)}")
            raise 