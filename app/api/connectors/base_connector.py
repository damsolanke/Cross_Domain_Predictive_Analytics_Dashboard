"""
Base connector class for API data sources
"""
import time
import requests
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import threading
import logging

logger = logging.getLogger(__name__)

class BaseConnector(ABC):
    """
    Abstract base class for all API connectors.
    Provides common functionality for connecting to external APIs.
    """
    
    def __init__(self, name: str, description: str, cache_ttl: int = 300):
        """
        Initialize the connector
        
        Args:
            name: Human-readable name for this connector
            description: Description of the data source
            cache_ttl: Cache time-to-live in seconds (default: 5 minutes)
        """
        self.name = name
        self.description = description
        self.cache_ttl = cache_ttl
        self.last_update_timestamp = 0
        self.status = "initialized"
        self.error = None
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_lock = threading.RLock()
        
        # API rate limiting
        self.rate_limit = {
            'requests_per_minute': 60,
            'last_request_time': 0,
            'request_count': 0
        }
    
    @abstractmethod
    def fetch_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch data from the API
        
        Args:
            params: Optional parameters for the API request
            
        Returns:
            Dictionary of fetched data
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of this connector
        
        Returns:
            Status information dictionary
        """
        return {
            'status': self.status,
            'last_update': self.last_update_timestamp,
            'error': str(self.error) if self.error else None,
            'cache_entries': len(self.cache),
            'rate_limit': self.rate_limit['requests_per_minute']
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this connector
        
        Returns:
            Metadata dictionary
        """
        return {
            'name': self.name,
            'description': self.description,
            'cache_ttl': self.cache_ttl
        }
    
    def _update_status(self, status: str, error: Optional[Exception] = None) -> None:
        """
        Update connector status
        
        Args:
            status: New status string
            error: Optional exception if an error occurred
        """
        self.status = status
        self.error = error
        logger.info(f"Connector {self.name} status: {status}")
        if error:
            logger.error(f"Connector {self.name} error: {error}")
    
    def _check_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Check if data exists in cache and is still valid
        
        Args:
            cache_key: Cache key to check
            
        Returns:
            Cached data or None if not found/expired
        """
        with self.cache_lock:
            if cache_key in self.cache:
                timestamp = self.cache_timestamps.get(cache_key, 0)
                if time.time() - timestamp < self.cache_ttl:
                    logger.debug(f"Cache hit for {cache_key}")
                    return self.cache[cache_key]
                else:
                    logger.debug(f"Cache expired for {cache_key}")
        return None
    
    def _update_cache(self, cache_key: str, data: Dict[str, Any]) -> None:
        """
        Update the cache with new data
        
        Args:
            cache_key: Cache key to update
            data: Data to cache
        """
        with self.cache_lock:
            self.cache[cache_key] = data
            self.cache_timestamps[cache_key] = time.time()
            
        # Update last update timestamp
        self.last_update_timestamp = time.time()
    
    def _make_api_request(self, url: str, method: str = 'GET', params: Dict[str, Any] = None, 
                          headers: Dict[str, str] = None, json_data: Dict[str, Any] = None, 
                          timeout: int = 10) -> requests.Response:
        """
        Make an API request with rate limiting and error handling
        
        Args:
            url: URL to request
            method: HTTP method (GET, POST, etc.)
            params: URL parameters
            headers: HTTP headers
            json_data: JSON data for POST/PUT requests
            timeout: Request timeout in seconds
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If the request fails
        """
        # Check rate limiting
        current_time = time.time()
        time_diff = current_time - self.rate_limit['last_request_time']
        
        if time_diff < 60:  # Less than a minute since last reset
            if self.rate_limit['request_count'] >= self.rate_limit['requests_per_minute']:
                # Sleep until rate limit resets
                sleep_time = 60 - time_diff
                logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                # Reset counter
                self.rate_limit['last_request_time'] = time.time()
                self.rate_limit['request_count'] = 0
        else:
            # More than a minute has passed, reset counter
            self.rate_limit['last_request_time'] = current_time
            self.rate_limit['request_count'] = 0
        
        # Make the request
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=json_data,
                timeout=timeout
            )
            response.raise_for_status()
            
            # Increment request counter
            self.rate_limit['request_count'] += 1
            
            return response
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            self._update_status("error", e)
            raise