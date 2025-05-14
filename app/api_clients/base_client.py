"""
Base API client class that provides common functionality for all API clients.
Includes retry logic, error handling, and caching mechanisms.
"""

import requests
import logging
from functools import wraps
import time
from typing import Any, Dict, Optional
import json
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BaseAPIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, cache_dir: str = "cache"):
        """
        Initialize the base API client.
        
        Args:
            base_url (str): Base URL for the API
            api_key (Optional[str]): API key for authentication
            cache_dir (str): Directory for caching API responses
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.cache_dir = cache_dir
        self.session = requests.Session()
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Configure session headers
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def _get_cache_path(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate cache file path based on endpoint and parameters."""
        cache_key = f"{endpoint}_{hash(frozenset(params.items()))}"
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def _is_cache_valid(self, cache_path: str, max_age_minutes: int = 60) -> bool:
        """Check if cached data is still valid based on age."""
        if not os.path.exists(cache_path):
            return False
        
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_path))
        return file_age < timedelta(minutes=max_age_minutes)
    
    def _load_from_cache(self, cache_path: str) -> Optional[Dict[str, Any]]:
        """Load data from cache file."""
        try:
            with open(cache_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def _save_to_cache(self, cache_path: str, data: Dict[str, Any]) -> None:
        """Save data to cache file."""
        with open(cache_path, 'w') as f:
            json.dump(data, f)
    
    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None,
                     max_retries: int = 3, retry_delay: int = 1,
                     use_cache: bool = True, cache_max_age: int = 60) -> Dict[str, Any]:
        """
        Make an API request with retry logic and caching.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (Dict[str, Any]): Request parameters
            max_retries (int): Maximum number of retry attempts
            retry_delay (int): Delay between retries in seconds
            use_cache (bool): Whether to use caching
            cache_max_age (int): Maximum age of cache in minutes
            
        Returns:
            Dict[str, Any]: API response data
            
        Raises:
            requests.exceptions.RequestException: If all retry attempts fail
        """
        params = params or {}
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Check cache if enabled
        if use_cache:
            cache_path = self._get_cache_path(endpoint, params)
            if self._is_cache_valid(cache_path, cache_max_age):
                cached_data = self._load_from_cache(cache_path)
                if cached_data:
                    logger.info(f"Using cached data for {endpoint}")
                    return cached_data
        
        # Make request with retries
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Cache successful response
                if use_cache:
                    self._save_to_cache(cache_path, data)
                
                return data
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    logger.error(f"API request failed after {max_retries} attempts: {str(e)}")
                    raise
                logger.warning(f"API request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
    
    def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Make a GET request to the API."""
        return self._make_request('GET', endpoint, params, **kwargs)
    
    def post(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Make a POST request to the API."""
        return self._make_request('POST', endpoint, params, **kwargs) 