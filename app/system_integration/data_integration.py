"""
Data integration module for ETL processes and external data source integration.
"""

import pandas as pd
import numpy as np
import requests
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
import threading
import queue
import time
import csv
import hashlib
import sqlite3
from io import StringIO

# Configure logging
logger = logging.getLogger(__name__)

class DataSource:
    """Base class for all data sources."""
    
    def __init__(self, name, domain, config=None):
        """
        Initialize the data source.
        
        Args:
            name (str): Name of the data source
            domain (str): Domain this data source belongs to (e.g., weather, economic)
            config (dict, optional): Configuration for the data source
        """
        self.name = name
        self.domain = domain
        self.config = config or {}
        self.last_update = None
        self.is_connected = False
        self.error = None
        self.data_buffer = queue.Queue(maxsize=1000)
    
    def connect(self):
        """
        Connect to the data source.
        
        Returns:
            bool: Success status
        """
        self.is_connected = True
        return True
    
    def disconnect(self):
        """
        Disconnect from the data source.
        
        Returns:
            bool: Success status
        """
        self.is_connected = False
        return True
    
    def fetch_data(self):
        """
        Fetch data from the source.
        
        Returns:
            dict: Data from the source
        """
        raise NotImplementedError("Subclasses must implement fetch_data")
    
    def transform_data(self, data):
        """
        Transform data to the standard format.
        
        Args:
            data: Raw data from the source
            
        Returns:
            dict: Transformed data
        """
        # Default implementation just adds timestamp and domain
        transformed = {
            'timestamp': datetime.now().isoformat(),
            'domain': self.domain,
            'source': self.name
        }
        
        # Add data
        if isinstance(data, dict):
            transformed.update(data)
        
        return transformed
    
    def get_status(self):
        """
        Get the status of this data source.
        
        Returns:
            dict: Status information
        """
        return {
            'name': self.name,
            'domain': self.domain,
            'connected': self.is_connected,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'error': str(self.error) if self.error else None
        }
    
    def __str__(self):
        return f"DataSource({self.name}, {self.domain})"


class APIDataSource(DataSource):
    """Data source for API endpoints."""
    
    def __init__(self, name, domain, url, method='GET', headers=None, 
                 params=None, auth=None, data_path=None, config=None):
        """
        Initialize the API data source.
        
        Args:
            name (str): Name of the data source
            domain (str): Domain this data source belongs to
            url (str): API endpoint URL
            method (str): HTTP method (GET, POST, etc.)
            headers (dict, optional): HTTP headers
            params (dict, optional): Query parameters
            auth (tuple, optional): Authentication credentials (username, password)
            data_path (str, optional): JSON path to data (e.g., 'result.data')
            config (dict, optional): Additional configuration
        """
        super().__init__(name, domain, config)
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.params = params or {}
        self.auth = auth
        self.data_path = data_path
        self.session = requests.Session()
    
    def connect(self):
        """
        Connect to the API by validating the endpoint.
        
        Returns:
            bool: Success status
        """
        try:
            # Make a test request
            response = self.session.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                params=self.params,
                auth=self.auth,
                timeout=10
            )
            
            # Check if request was successful
            if response.status_code == 200:
                self.is_connected = True
                return True
            else:
                self.error = f"API returned status code: {response.status_code}"
                self.is_connected = False
                return False
        
        except Exception as e:
            self.error = str(e)
            self.is_connected = False
            return False
    
    def fetch_data(self):
        """
        Fetch data from the API.
        
        Returns:
            dict: Data from the API
        """
        if not self.is_connected:
            if not self.connect():
                raise ConnectionError(f"Could not connect to API: {self.error}")
        
        try:
            # Make request
            response = self.session.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                params=self.params,
                auth=self.auth,
                timeout=10
            )
            
            # Check if request was successful
            if response.status_code != 200:
                raise requests.HTTPError(f"API returned status code: {response.status_code}")
            
            # Parse JSON response
            data = response.json()
            
            # Extract data using path if provided
            if self.data_path:
                for key in self.data_path.split('.'):
                    if key in data:
                        data = data[key]
                    else:
                        raise KeyError(f"Key '{key}' not found in response data")
            
            # Update last update time
            self.last_update = datetime.now()
            
            return data
            
        except Exception as e:
            self.error = str(e)
            raise
    
    def transform_data(self, data):
        """
        Transform API data to the standard format.
        
        Args:
            data: Raw data from the API
            
        Returns:
            dict: Transformed data
        """
        # Start with basic transformation
        transformed = super().transform_data({})
        
        # Add raw data if it's a dictionary
        if isinstance(data, dict):
            for key, value in data.items():
                if key not in transformed and isinstance(value, (int, float, str, bool)):
                    transformed[key] = value
        
        # Add array data if applicable
        elif isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict):
                # Take first item if it's a list of dictionaries
                for key, value in data[0].items():
                    if key not in transformed and isinstance(value, (int, float, str, bool)):
                        transformed[key] = value
            elif isinstance(data[0], (int, float)):
                # If it's a list of numbers, add as 'values'
                transformed['values'] = data
        
        return transformed


class CSVDataSource(DataSource):
    """Data source for CSV files."""
    
    def __init__(self, name, domain, file_path, delimiter=',', 
                 columns=None, date_column=None, refresh_interval=3600, config=None):
        """
        Initialize the CSV data source.
        
        Args:
            name (str): Name of the data source
            domain (str): Domain this data source belongs to
            file_path (str): Path to the CSV file
            delimiter (str): CSV delimiter
            columns (list, optional): Columns to include (None for all)
            date_column (str, optional): Column containing dates
            refresh_interval (int): Seconds between refreshes
            config (dict, optional): Additional configuration
        """
        super().__init__(name, domain, config)
        self.file_path = file_path
        self.delimiter = delimiter
        self.columns = columns
        self.date_column = date_column
        self.refresh_interval = refresh_interval
        self.data_cache = None
        self.last_modified = None
    
    def connect(self):
        """
        Connect to the CSV file by checking if it exists.
        
        Returns:
            bool: Success status
        """
        try:
            # Check if file exists
            file_path = Path(self.file_path)
            if not file_path.exists():
                self.error = f"File not found: {self.file_path}"
                self.is_connected = False
                return False
            
            # Check if file can be read
            with open(file_path, 'r', encoding='utf-8') as f:
                # Read first line to check format
                header = f.readline().strip()
            
            # Update last modified time
            self.last_modified = file_path.stat().st_mtime
            
            self.is_connected = True
            return True
            
        except Exception as e:
            self.error = str(e)
            self.is_connected = False
            return False
    
    def fetch_data(self):
        """
        Fetch data from the CSV file.
        
        Returns:
            pandas.DataFrame: Data from the CSV file
        """
        if not self.is_connected:
            if not self.connect():
                raise ConnectionError(f"Could not connect to CSV file: {self.error}")
        
        try:
            file_path = Path(self.file_path)
            
            # Check if file has been modified
            current_mtime = file_path.stat().st_mtime
            if self.data_cache is not None and current_mtime == self.last_modified:
                # Use cached data if not modified
                return self.data_cache
            
            # Read CSV file
            df = pd.read_csv(
                file_path,
                delimiter=self.delimiter,
                usecols=self.columns
            )
            
            # Convert date column if specified
            if self.date_column and self.date_column in df.columns:
                df[self.date_column] = pd.to_datetime(df[self.date_column])
            
            # Update cache and metadata
            self.data_cache = df
            self.last_modified = current_mtime
            self.last_update = datetime.now()
            
            return df
            
        except Exception as e:
            self.error = str(e)
            raise
    
    def transform_data(self, data):
        """
        Transform CSV data to the standard format.
        
        Args:
            data (pandas.DataFrame): Raw data from the CSV
            
        Returns:
            dict: Transformed data
        """
        # Start with basic transformation
        transformed = super().transform_data({})
        
        # Add latest row as data
        if isinstance(data, pd.DataFrame) and not data.empty:
            # Get the latest row based on date column if available
            if self.date_column and self.date_column in data.columns:
                latest = data.sort_values(self.date_column).iloc[-1]
            else:
                latest = data.iloc[-1]
            
            # Add data from the row
            for column in latest.index:
                if column != self.date_column:
                    value = latest[column]
                    if pd.notna(value):
                        transformed[column] = value
        
        return transformed


class DatabaseDataSource(DataSource):
    """Data source for SQL databases."""
    
    def __init__(self, name, domain, connection_string, query, 
                 parameters=None, config=None):
        """
        Initialize the database data source.
        
        Args:
            name (str): Name of the data source
            domain (str): Domain this data source belongs to
            connection_string (str): Database connection string
            query (str): SQL query to execute
            parameters (dict, optional): Query parameters
            config (dict, optional): Additional configuration
        """
        super().__init__(name, domain, config)
        self.connection_string = connection_string
        self.query = query
        self.parameters = parameters or {}
        self.connection = None
    
    def connect(self):
        """
        Connect to the database.
        
        Returns:
            bool: Success status
        """
        try:
            # Connect to database
            self.connection = sqlite3.connect(self.connection_string)
            
            # Test connection with a simple query
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            
            self.is_connected = True
            return True
            
        except Exception as e:
            self.error = str(e)
            self.is_connected = False
            return False
    
    def disconnect(self):
        """
        Disconnect from the database.
        
        Returns:
            bool: Success status
        """
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except Exception as e:
                self.error = str(e)
                return False
        
        self.is_connected = False
        return True
    
    def fetch_data(self):
        """
        Fetch data from the database.
        
        Returns:
            pandas.DataFrame: Data from the database
        """
        if not self.is_connected:
            if not self.connect():
                raise ConnectionError(f"Could not connect to database: {self.error}")
        
        try:
            # Execute query
            df = pd.read_sql_query(
                sql=self.query,
                con=self.connection,
                params=self.parameters
            )
            
            # Update last update time
            self.last_update = datetime.now()
            
            return df
            
        except Exception as e:
            self.error = str(e)
            raise
    
    def transform_data(self, data):
        """
        Transform database data to the standard format.
        
        Args:
            data (pandas.DataFrame): Raw data from the database
            
        Returns:
            dict: Transformed data
        """
        # Start with basic transformation
        transformed = super().transform_data({})
        
        # Add data from the first row
        if isinstance(data, pd.DataFrame) and not data.empty:
            row = data.iloc[0]
            
            for column in row.index:
                value = row[column]
                if pd.notna(value):
                    transformed[column] = value
        
        return transformed


class DataIntegrator:
    """
    Manages data sources and integration processes.
    """
    
    def __init__(self, data_dir=None):
        """
        Initialize the data integrator.
        
        Args:
            data_dir (str, optional): Directory for storing data
        """
        self.data_sources = {}
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Ensure data directory exists
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        
        self.active_processes = {}
        self.data_buffer = queue.Queue(maxsize=10000)
        self.is_running = False
        self.processing_thread = None
        self.cached_data = {}
    
    def register_data_source(self, source):
        """
        Register a data source.
        
        Args:
            source (DataSource): Data source to register
            
        Returns:
            bool: Success status
        """
        if source.name in self.data_sources:
            return False
        
        self.data_sources[source.name] = source
        return True
    
    def remove_data_source(self, source_name):
        """
        Remove a data source.
        
        Args:
            source_name (str): Name of the data source to remove
            
        Returns:
            bool: Success status
        """
        if source_name not in self.data_sources:
            return False
        
        # Stop any active processes for this source
        self.stop_source(source_name)
        
        # Remove the source
        del self.data_sources[source_name]
        return True
    
    def start_source(self, source_name, interval=60):
        """
        Start collecting data from a source.
        
        Args:
            source_name (str): Name of the data source
            interval (int): Interval between data collection in seconds
            
        Returns:
            bool: Success status
        """
        if source_name not in self.data_sources:
            return False
        
        # Check if source is already running
        if source_name in self.active_processes:
            return True
        
        # Start a new process for this source
        process_info = {
            'interval': interval,
            'running': True,
            'thread': threading.Thread(
                target=self._source_collection_loop,
                args=(source_name, interval),
                daemon=True
            ),
            'last_run': None,
            'error': None
        }
        
        process_info['thread'].start()
        self.active_processes[source_name] = process_info
        
        return True
    
    def stop_source(self, source_name):
        """
        Stop collecting data from a source.
        
        Args:
            source_name (str): Name of the data source
            
        Returns:
            bool: Success status
        """
        if source_name not in self.active_processes:
            return False
        
        # Signal the thread to stop
        self.active_processes[source_name]['running'] = False
        
        # Wait for thread to terminate (with timeout)
        thread = self.active_processes[source_name]['thread']
        if thread.is_alive():
            thread.join(timeout=5.0)
        
        # Remove from active processes
        del self.active_processes[source_name]
        
        return True
    
    def _source_collection_loop(self, source_name, interval):
        """
        Background loop for collecting data from a source.
        
        Args:
            source_name (str): Name of the data source
            interval (int): Interval between collections in seconds
        """
        try:
            source = self.data_sources[source_name]
            
            while self.active_processes.get(source_name, {}).get('running', False):
                try:
                    # Fetch and transform data
                    raw_data = source.fetch_data()
                    transformed_data = source.transform_data(raw_data)
                    
                    # Add to buffer
                    self.data_buffer.put(transformed_data, block=False)
                    
                    # Update process info
                    if source_name in self.active_processes:
                        self.active_processes[source_name]['last_run'] = datetime.now()
                        self.active_processes[source_name]['error'] = None
                    
                except Exception as e:
                    # Update error info
                    if source_name in self.active_processes:
                        self.active_processes[source_name]['error'] = str(e)
                    
                    logger.error(f"Error collecting data from {source_name}: {e}")
                
                # Sleep until next interval
                time.sleep(interval)
        
        except Exception as e:
            logger.error(f"Fatal error in collection loop for {source_name}: {e}")
    
    def start_processing(self):
        """
        Start processing collected data.
        
        Returns:
            bool: Success status
        """
        if self.is_running:
            return True
        
        # Start processing thread
        self.is_running = True
        self.processing_thread = threading.Thread(
            target=self._processing_loop,
            daemon=True
        )
        self.processing_thread.start()
        
        return True
    
    def stop_processing(self):
        """
        Stop processing collected data.
        
        Returns:
            bool: Success status
        """
        if not self.is_running:
            return True
        
        # Signal thread to stop
        self.is_running = False
        
        # Wait for thread to terminate (with timeout)
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=5.0)
        
        return True
    
    def _processing_loop(self):
        """Background loop for processing collected data."""
        try:
            while self.is_running:
                try:
                    # Get data from buffer (with timeout)
                    data = self.data_buffer.get(timeout=1.0)
                    
                    # Process data
                    processed_data = self._process_data(data)
                    
                    # Store in cache
                    self._cache_data(processed_data)
                    
                    # Store in file
                    self._store_data(processed_data)
                    
                    # Mark task as done
                    self.data_buffer.task_done()
                    
                except queue.Empty:
                    # No data available, just continue
                    pass
                
                except Exception as e:
                    logger.error(f"Error processing data: {e}")
        
        except Exception as e:
            logger.error(f"Fatal error in processing loop: {e}")
            self.is_running = False
    
    def _process_data(self, data):
        """
        Process raw data.
        
        Args:
            data (dict): Raw data to process
            
        Returns:
            dict: Processed data
        """
        # Basic processing - add any derived fields here
        processed = data.copy()
        
        # Add processing timestamp
        processed['processed_at'] = datetime.now().isoformat()
        
        return processed
    
    def _cache_data(self, data):
        """
        Cache data in memory.
        
        Args:
            data (dict): Data to cache
        """
        domain = data.get('domain')
        source = data.get('source')
        
        if not domain or not source:
            return
        
        # Cache by domain and source
        key = f"{domain}_{source}"
        
        # Initialize if needed
        if key not in self.cached_data:
            self.cached_data[key] = []
        
        # Add to cache and limit size
        self.cached_data[key].append(data)
        if len(self.cached_data[key]) > 100:
            self.cached_data[key] = self.cached_data[key][-100:]
    
    def _store_data(self, data):
        """
        Store data to disk.
        
        Args:
            data (dict): Data to store
        """
        domain = data.get('domain')
        source = data.get('source')
        
        if not domain or not source:
            return
        
        # Create file path
        today = datetime.now().strftime('%Y-%m-%d')
        file_name = f"{domain}_{source}_{today}.json"
        file_path = os.path.join(self.data_dir, file_name)
        
        # Append to file
        with open(file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def get_status(self):
        """
        Get the status of all data sources and processes.
        
        Returns:
            dict: Status information
        """
        return {
            'sources': {
                name: source.get_status() for name, source in self.data_sources.items()
            },
            'processes': {
                name: {
                    'interval': info['interval'],
                    'running': info['running'],
                    'last_run': info['last_run'].isoformat() if info['last_run'] else None,
                    'error': info['error']
                } for name, info in self.active_processes.items()
            },
            'processing': {
                'running': self.is_running,
                'buffer_size': self.data_buffer.qsize(),
                'cached_domains': list(self.cached_data.keys())
            }
        }
    
    def get_latest_data(self, domain=None, source=None, limit=10):
        """
        Get the latest data for a domain/source.
        
        Args:
            domain (str, optional): Domain to filter by
            source (str, optional): Source to filter by
            limit (int): Maximum number of items to return
            
        Returns:
            list: Latest data
        """
        result = []
        
        # Filter cache keys
        if domain and source:
            keys = [f"{domain}_{source}"]
        elif domain:
            keys = [k for k in self.cached_data.keys() if k.startswith(f"{domain}_")]
        elif source:
            keys = [k for k in self.cached_data.keys() if k.endswith(f"_{source}")]
        else:
            keys = list(self.cached_data.keys())
        
        # Collect data from each key
        for key in keys:
            result.extend(self.cached_data.get(key, []))
        
        # Sort by timestamp and limit
        result.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return result[:limit]


# Example usage
if __name__ == "__main__":
    # Create data integrator
    integrator = DataIntegrator()
    
    # Register data sources
    api_source = APIDataSource(
        name="weather_api",
        domain="weather",
        url="https://api.openweathermap.org/data/2.5/weather",
        params={"q": "London", "appid": "YOUR_API_KEY"}
    )
    
    csv_source = CSVDataSource(
        name="economic_data",
        domain="economic",
        file_path="economic_data.csv",
        date_column="date"
    )
    
    integrator.register_data_source(api_source)
    integrator.register_data_source(csv_source)
    
    # Start processing
    integrator.start_processing()
    
    # Start collecting data
    integrator.start_source("weather_api", interval=300)  # Every 5 minutes
    integrator.start_source("economic_data", interval=3600)  # Every hour
    
    # Print status
    print("Status:", integrator.get_status())
    
    # Run for a while
    time.sleep(60)
    
    # Stop everything
    integrator.stop_source("weather_api")
    integrator.stop_source("economic_data")
    integrator.stop_processing()