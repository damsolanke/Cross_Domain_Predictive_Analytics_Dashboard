"""
Data validator class for handling data validation operations.
Provides methods for validating data quality and consistency.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ValidationSeverity(Enum):
    """Enum for validation severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

@dataclass
class ValidationResult:
    """Class for storing validation results."""
    severity: ValidationSeverity
    message: str
    details: Optional[Dict[str, Any]] = None

class DataValidator:
    def __init__(self):
        """Initialize the data validator."""
        self.validation_history = []
    
    def validate_weather_data(self, df: pd.DataFrame) -> List[ValidationResult]:
        """
        Validate weather data quality and consistency.
        
        Args:
            df (pd.DataFrame): Weather data to validate
            
        Returns:
            List[ValidationResult]: List of validation results
        """
        results = []
        
        try:
            # Check for required columns
            required_columns = ['timestamp', 'temperature', 'humidity', 'pressure', 'wind_speed']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                results.append(ValidationResult(
                    severity=ValidationSeverity.ERROR,
                    message=f"Missing required columns: {missing_columns}",
                    details={'missing_columns': missing_columns}
                ))
            
            # Validate timestamp
            if 'timestamp' in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                    results.append(ValidationResult(
                        severity=ValidationSeverity.ERROR,
                        message="Timestamp column is not datetime type",
                        details={'column': 'timestamp', 'dtype': str(df['timestamp'].dtype)}
                    ))
            
            # Validate numeric ranges
            numeric_ranges = {
                'temperature': (-50, 50),  # Celsius
                'humidity': (0, 100),      # Percentage
                'pressure': (800, 1100),   # hPa
                'wind_speed': (0, 100)     # m/s
            }
            
            for col, (min_val, max_val) in numeric_ranges.items():
                if col in df.columns:
                    out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
                    if not out_of_range.empty:
                        results.append(ValidationResult(
                            severity=ValidationSeverity.WARNING,
                            message=f"Values out of range in {col}",
                            details={
                                'column': col,
                                'range': (min_val, max_val),
                                'out_of_range_count': len(out_of_range)
                            }
                        ))
            
            # Check for missing values
            missing_values = df.isnull().sum()
            if missing_values.any():
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    message="Missing values found",
                    details={'missing_counts': missing_values[missing_values > 0].to_dict()}
                ))
            
            # Check for duplicate timestamps
            if 'timestamp' in df.columns:
                duplicates = df[df['timestamp'].duplicated()]
                if not duplicates.empty:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.WARNING,
                        message="Duplicate timestamps found",
                        details={'duplicate_count': len(duplicates)}
                    ))
            
            self.validation_history.append({
                'timestamp': datetime.now(),
                'operation': 'validate_weather_data',
                'results': results
            })
            
            return results
            
        except Exception as e:
            logger.error(f"Error validating weather data: {str(e)}")
            raise
    
    def validate_economic_data(self, df: pd.DataFrame) -> List[ValidationResult]:
        """
        Validate economic data quality and consistency.
        
        Args:
            df (pd.DataFrame): Economic data to validate
            
        Returns:
            List[ValidationResult]: List of validation results
        """
        results = []
        
        try:
            # Check for required columns
            required_columns = ['date', 'value']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                results.append(ValidationResult(
                    severity=ValidationSeverity.ERROR,
                    message=f"Missing required columns: {missing_columns}",
                    details={'missing_columns': missing_columns}
                ))
            
            # Validate date
            if 'date' in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df['date']):
                    results.append(ValidationResult(
                        severity=ValidationSeverity.ERROR,
                        message="Date column is not datetime type",
                        details={'column': 'date', 'dtype': str(df['date'].dtype)}
                    ))
            
            # Validate value
            if 'value' in df.columns:
                if not pd.api.types.is_numeric_dtype(df['value']):
                    results.append(ValidationResult(
                        severity=ValidationSeverity.ERROR,
                        message="Value column is not numeric type",
                        details={'column': 'value', 'dtype': str(df['value'].dtype)}
                    ))
                
                # Check for negative values
                negative_values = df[df['value'] < 0]
                if not negative_values.empty:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.WARNING,
                        message="Negative values found in value column",
                        details={'negative_count': len(negative_values)}
                    ))
            
            # Check for missing values
            missing_values = df.isnull().sum()
            if missing_values.any():
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    message="Missing values found",
                    details={'missing_counts': missing_values[missing_values > 0].to_dict()}
                ))
            
            # Check for duplicate dates
            if 'date' in df.columns:
                duplicates = df[df['date'].duplicated()]
                if not duplicates.empty:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.WARNING,
                        message="Duplicate dates found",
                        details={'duplicate_count': len(duplicates)}
                    ))
            
            self.validation_history.append({
                'timestamp': datetime.now(),
                'operation': 'validate_economic_data',
                'results': results
            })
            
            return results
            
        except Exception as e:
            logger.error(f"Error validating economic data: {str(e)}")
            raise
    
    def validate_social_data(self, df: pd.DataFrame) -> List[ValidationResult]:
        """
        Validate social media data quality and consistency.
        
        Args:
            df (pd.DataFrame): Social media data to validate
            
        Returns:
            List[ValidationResult]: List of validation results
        """
        results = []
        
        try:
            # Check for required columns
            required_columns = ['created_at', 'text']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                results.append(ValidationResult(
                    severity=ValidationSeverity.ERROR,
                    message=f"Missing required columns: {missing_columns}",
                    details={'missing_columns': missing_columns}
                ))
            
            # Validate created_at
            if 'created_at' in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df['created_at']):
                    results.append(ValidationResult(
                        severity=ValidationSeverity.ERROR,
                        message="Created_at column is not datetime type",
                        details={'column': 'created_at', 'dtype': str(df['created_at'].dtype)}
                    ))
            
            # Validate text
            if 'text' in df.columns:
                # Check for empty text
                empty_text = df[df['text'].str.strip() == '']
                if not empty_text.empty:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.WARNING,
                        message="Empty text found",
                        details={'empty_count': len(empty_text)}
                    ))
                
                # Check text length
                long_text = df[df['text'].str.len() > 280]  # Twitter's character limit
                if not long_text.empty:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.WARNING,
                        message="Text exceeds character limit",
                        details={'long_text_count': len(long_text)}
                    ))
            
            # Check for missing values
            missing_values = df.isnull().sum()
            if missing_values.any():
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    message="Missing values found",
                    details={'missing_counts': missing_values[missing_values > 0].to_dict()}
                ))
            
            # Check for duplicate tweets
            if 'text' in df.columns:
                duplicates = df[df['text'].duplicated()]
                if not duplicates.empty:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.WARNING,
                        message="Duplicate tweets found",
                        details={'duplicate_count': len(duplicates)}
                    ))
            
            self.validation_history.append({
                'timestamp': datetime.now(),
                'operation': 'validate_social_data',
                'results': results
            })
            
            return results
            
        except Exception as e:
            logger.error(f"Error validating social data: {str(e)}")
            raise
    
    def get_validation_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of validation operations performed.
        
        Returns:
            List[Dict[str, Any]]: List of validation operations
        """
        return self.validation_history 