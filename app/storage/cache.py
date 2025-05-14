"""
Cache manager class for handling data caching operations.
Provides methods for caching and retrieving data with expiration and invalidation.
"""

import json
import pickle
from typing import Any, Dict, Optional, Union
from datetime import datetime, timedelta
import logging
from pathlib import Path
import hashlib
import os

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, cache_dir: str = 'data/cache', max_size: int = 1000):
        """
        Initialize the cache manager.
        
        Args:
            cache_dir (str): Directory for cache storage
            max_size (int): Maximum number of cache entries
        """
        self.cache_dir = Path(cache_dir)
        self.max_size = max_size
        self._create_cache_dir()
        self._load_metadata()
    
    def _create_cache_dir(self) -> None:
        """Create cache directory if it doesn't exist."""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating cache directory: {str(e)}")
            raise
    
    def _load_metadata(self) -> None:
        """Load cache metadata from file."""
        self.metadata_file = self.cache_dir / 'metadata.json'
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                logger.error(f"Error loading cache metadata: {str(e)}")
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self) -> None:
        """Save cache metadata to file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache metadata: {str(e)}")
            raise
    
    def _generate_key(self, data: Any) -> str:
        """
        Generate a cache key from data.
        
        Args:
            data (Any): Data to generate key from
            
        Returns:
            str: Generated cache key
        """
        if isinstance(data, (str, int, float, bool)):
            key_data = str(data)
        else:
            key_data = pickle.dumps(data)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _cleanup_old_entries(self) -> None:
        """Remove expired and excess cache entries."""
        try:
            current_time = datetime.now()
            expired_keys = []
            
            # Find expired entries
            for key, metadata in self.metadata.items():
                if 'expires_at' in metadata:
                    expires_at = datetime.fromisoformat(metadata['expires_at'])
                    if current_time > expires_at:
                        expired_keys.append(key)
            
            # Remove expired entries
            for key in expired_keys:
                self._remove_entry(key)
            
            # Remove excess entries if needed
            while len(self.metadata) > self.max_size:
                oldest_key = min(self.metadata.items(),
                               key=lambda x: datetime.fromisoformat(x[1]['created_at']))[0]
                self._remove_entry(oldest_key)
                
        except Exception as e:
            logger.error(f"Error cleaning up cache: {str(e)}")
            raise
    
    def _remove_entry(self, key: str) -> None:
        """
        Remove a cache entry.
        
        Args:
            key (str): Cache key to remove
        """
        try:
            cache_file = self.cache_dir / f"{key}.cache"
            if cache_file.exists():
                cache_file.unlink()
            if key in self.metadata:
                del self.metadata[key]
            self._save_metadata()
        except Exception as e:
            logger.error(f"Error removing cache entry: {str(e)}")
            raise
    
    def set(self, key: str, value: Any,
            expires_in: Optional[timedelta] = None) -> None:
        """
        Set a value in the cache.
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
            expires_in (Optional[timedelta]): Time until expiration
        """
        try:
            self._cleanup_old_entries()
            
            cache_file = self.cache_dir / f"{key}.cache"
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
            
            metadata = {
                'created_at': datetime.now().isoformat(),
                'size': os.path.getsize(cache_file)
            }
            
            if expires_in:
                metadata['expires_at'] = (datetime.now() + expires_in).isoformat()
            
            self.metadata[key] = metadata
            self._save_metadata()
            
            logger.info(f"Cached value for key: {key}")
            
        except Exception as e:
            logger.error(f"Error setting cache value: {str(e)}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[Any]: Cached value if found and not expired
        """
        try:
            if key not in self.metadata:
                return None
            
            metadata = self.metadata[key]
            
            # Check expiration
            if 'expires_at' in metadata:
                expires_at = datetime.fromisoformat(metadata['expires_at'])
                if datetime.now() > expires_at:
                    self._remove_entry(key)
                    return None
            
            cache_file = self.cache_dir / f"{key}.cache"
            if not cache_file.exists():
                self._remove_entry(key)
                return None
            
            with open(cache_file, 'rb') as f:
                value = pickle.load(f)
            
            logger.info(f"Retrieved cached value for key: {key}")
            return value
            
        except Exception as e:
            logger.error(f"Error getting cache value: {str(e)}")
            raise
    
    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        Args:
            key (str): Cache key to delete
        """
        try:
            self._remove_entry(key)
            logger.info(f"Deleted cache entry for key: {key}")
        except Exception as e:
            logger.error(f"Error deleting cache entry: {str(e)}")
            raise
    
    def clear(self) -> None:
        """Clear all cache entries."""
        try:
            for file in self.cache_dir.glob('*.cache'):
                file.unlink()
            self.metadata = {}
            self._save_metadata()
            logger.info("Cleared all cache entries")
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        try:
            total_size = sum(metadata['size'] for metadata in self.metadata.values())
            return {
                'entry_count': len(self.metadata),
                'total_size': total_size,
                'max_size': self.max_size,
                'cache_dir': str(self.cache_dir)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            raise 