"""
File storage class for handling file system operations.
Provides methods for storing and retrieving data from the file system.
"""

import pandas as pd
import json
import os
import pickle
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

class FileStorage:
    def __init__(self, base_dir: str = 'data'):
        """
        Initialize the file storage.
        
        Args:
            base_dir (str): Base directory for file storage
        """
        self.base_dir = Path(base_dir)
        self._create_directories()
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        try:
            # Create base directory
            self.base_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            (self.base_dir / 'raw').mkdir(exist_ok=True)
            (self.base_dir / 'processed').mkdir(exist_ok=True)
            (self.base_dir / 'cache').mkdir(exist_ok=True)
            (self.base_dir / 'backup').mkdir(exist_ok=True)
            
        except Exception as e:
            logger.error(f"Error creating directories: {str(e)}")
            raise
    
    def save_dataframe(self, df: pd.DataFrame, filename: str,
                      format: str = 'csv', subdir: str = 'processed') -> None:
        """
        Save DataFrame to file.
        
        Args:
            df (pd.DataFrame): DataFrame to save
            filename (str): Target filename
            format (str): File format ('csv', 'parquet', or 'pickle')
            subdir (str): Subdirectory to save in
        """
        try:
            filepath = self.base_dir / subdir / filename
            
            if format == 'csv':
                df.to_csv(filepath, index=False)
            elif format == 'parquet':
                df.to_parquet(filepath, index=False)
            elif format == 'pickle':
                df.to_pickle(filepath)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Saved DataFrame to: {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving DataFrame: {str(e)}")
            raise
    
    def load_dataframe(self, filename: str,
                      format: str = 'csv', subdir: str = 'processed') -> pd.DataFrame:
        """
        Load DataFrame from file.
        
        Args:
            filename (str): Source filename
            format (str): File format ('csv', 'parquet', or 'pickle')
            subdir (str): Subdirectory to load from
            
        Returns:
            pd.DataFrame: Loaded DataFrame
        """
        try:
            filepath = self.base_dir / subdir / filename
            
            if format == 'csv':
                return pd.read_csv(filepath)
            elif format == 'parquet':
                return pd.read_parquet(filepath)
            elif format == 'pickle':
                return pd.read_pickle(filepath)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
        except Exception as e:
            logger.error(f"Error loading DataFrame: {str(e)}")
            raise
    
    def save_json(self, data: Dict[str, Any], filename: str,
                 subdir: str = 'processed') -> None:
        """
        Save JSON data to file.
        
        Args:
            data (Dict[str, Any]): JSON data to save
            filename (str): Target filename
            subdir (str): Subdirectory to save in
        """
        try:
            filepath = self.base_dir / subdir / filename
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved JSON data to: {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving JSON data: {str(e)}")
            raise
    
    def load_json(self, filename: str,
                 subdir: str = 'processed') -> Dict[str, Any]:
        """
        Load JSON data from file.
        
        Args:
            filename (str): Source filename
            subdir (str): Subdirectory to load from
            
        Returns:
            Dict[str, Any]: Loaded JSON data
        """
        try:
            filepath = self.base_dir / subdir / filename
            
            with open(filepath, 'r') as f:
                return json.load(f)
            
        except Exception as e:
            logger.error(f"Error loading JSON data: {str(e)}")
            raise
    
    def save_object(self, obj: Any, filename: str,
                   subdir: str = 'processed') -> None:
        """
        Save Python object to file using pickle.
        
        Args:
            obj (Any): Object to save
            filename (str): Target filename
            subdir (str): Subdirectory to save in
        """
        try:
            filepath = self.base_dir / subdir / filename
            
            with open(filepath, 'wb') as f:
                pickle.dump(obj, f)
            
            logger.info(f"Saved object to: {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving object: {str(e)}")
            raise
    
    def load_object(self, filename: str,
                   subdir: str = 'processed') -> Any:
        """
        Load Python object from file using pickle.
        
        Args:
            filename (str): Source filename
            subdir (str): Subdirectory to load from
            
        Returns:
            Any: Loaded object
        """
        try:
            filepath = self.base_dir / subdir / filename
            
            with open(filepath, 'rb') as f:
                return pickle.load(f)
            
        except Exception as e:
            logger.error(f"Error loading object: {str(e)}")
            raise
    
    def create_backup(self, source_dir: str, backup_name: Optional[str] = None) -> None:
        """
        Create backup of a directory.
        
        Args:
            source_dir (str): Source directory to backup
            backup_name (Optional[str]): Name for backup directory
        """
        try:
            source_path = self.base_dir / source_dir
            if not backup_name:
                backup_name = f"{source_dir}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path = self.base_dir / 'backup' / backup_name
            
            shutil.copytree(source_path, backup_path)
            
            logger.info(f"Created backup: {backup_path}")
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            raise
    
    def restore_backup(self, backup_name: str, target_dir: str) -> None:
        """
        Restore from backup.
        
        Args:
            backup_name (str): Name of backup to restore
            target_dir (str): Target directory to restore to
        """
        try:
            backup_path = self.base_dir / 'backup' / backup_name
            target_path = self.base_dir / target_dir
            
            if target_path.exists():
                shutil.rmtree(target_path)
            
            shutil.copytree(backup_path, target_path)
            
            logger.info(f"Restored backup {backup_name} to: {target_path}")
            
        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
            raise
    
    def list_files(self, subdir: str = 'processed',
                  pattern: str = '*') -> List[str]:
        """
        List files in a directory.
        
        Args:
            subdir (str): Subdirectory to list
            pattern (str): File pattern to match
            
        Returns:
            List[str]: List of filenames
        """
        try:
            dir_path = self.base_dir / subdir
            return [f.name for f in dir_path.glob(pattern)]
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            raise
    
    def delete_file(self, filename: str,
                   subdir: str = 'processed') -> None:
        """
        Delete a file.
        
        Args:
            filename (str): Filename to delete
            subdir (str): Subdirectory containing the file
        """
        try:
            filepath = self.base_dir / subdir / filename
            
            if filepath.exists():
                filepath.unlink()
                logger.info(f"Deleted file: {filepath}")
            else:
                logger.warning(f"File not found: {filepath}")
            
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise 