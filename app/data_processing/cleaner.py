"""
Data cleaner class for handling data cleaning operations.
Provides methods for cleaning and normalizing data from various sources.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        """Initialize the data cleaner."""
        self.cleaning_history = []
    
    def clean_weather_data(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Clean weather data from OpenWeatherMap API.
        
        Args:
            data (Dict[str, Any]): Raw weather data
            
        Returns:
            pd.DataFrame: Cleaned weather data
        """
        try:
            if 'forecast' in data:
                df = pd.DataFrame(data['forecast'])
            else:
                df = pd.DataFrame([data['current']])
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            
            # Handle missing values
            df = df.fillna({
                'temperature': df['temperature'].mean(),
                'humidity': df['humidity'].mean(),
                'pressure': df['pressure'].mean(),
                'wind_speed': df['wind_speed'].mean(),
                'clouds': df['clouds'].mean()
            })
            
            # Remove outliers using IQR method
            numeric_columns = ['temperature', 'humidity', 'pressure', 'wind_speed', 'clouds']
            for col in numeric_columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
            
            self.cleaning_history.append({
                'timestamp': datetime.now(),
                'operation': 'clean_weather_data',
                'rows_processed': len(df)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning weather data: {str(e)}")
            raise
    
    def clean_economic_data(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Clean economic data from Alpha Vantage API.
        
        Args:
            data (Dict[str, Any]): Raw economic data
            
        Returns:
            pd.DataFrame: Cleaned economic data
        """
        try:
            # Convert data to DataFrame
            df = pd.DataFrame(data['data'])
            
            # Convert date to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Handle missing values
            df = df.fillna({
                'value': df['value'].mean(),
                'change': 0
            })
            
            # Remove outliers using IQR method
            Q1 = df['value'].quantile(0.25)
            Q3 = df['value'].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df['value'] < (Q1 - 1.5 * IQR)) | (df['value'] > (Q3 + 1.5 * IQR)))]
            
            self.cleaning_history.append({
                'timestamp': datetime.now(),
                'operation': 'clean_economic_data',
                'rows_processed': len(df)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning economic data: {str(e)}")
            raise
    
    def clean_social_data(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Clean social media data from Twitter API.
        
        Args:
            data (Dict[str, Any]): Raw social media data
            
        Returns:
            pd.DataFrame: Cleaned social media data
        """
        try:
            # Convert tweets to DataFrame
            df = pd.DataFrame(data['tweets'])
            
            # Convert created_at to datetime
            df['created_at'] = pd.to_datetime(df['created_at'])
            
            # Clean text data
            df['text'] = df['text'].str.replace(r'http\S+|www.\S+', '', regex=True)  # Remove URLs
            df['text'] = df['text'].str.replace(r'@\w+', '', regex=True)  # Remove mentions
            df['text'] = df['text'].str.replace(r'#\w+', '', regex=True)  # Remove hashtags
            df['text'] = df['text'].str.strip()
            
            # Handle missing values in metrics
            metrics_columns = ['retweet_count', 'reply_count', 'like_count', 'quote_count']
            for col in metrics_columns:
                if col in df.columns:
                    df[col] = df[col].fillna(0)
            
            self.cleaning_history.append({
                'timestamp': datetime.now(),
                'operation': 'clean_social_data',
                'rows_processed': len(df)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning social data: {str(e)}")
            raise
    
    def normalize_data(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Normalize specified columns in the DataFrame using min-max scaling.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): List of columns to normalize
            
        Returns:
            pd.DataFrame: DataFrame with normalized columns
        """
        try:
            df_normalized = df.copy()
            
            for col in columns:
                if col in df.columns:
                    min_val = df[col].min()
                    max_val = df[col].max()
                    if max_val != min_val:
                        df_normalized[col] = (df[col] - min_val) / (max_val - min_val)
            
            self.cleaning_history.append({
                'timestamp': datetime.now(),
                'operation': 'normalize_data',
                'columns_normalized': columns
            })
            
            return df_normalized
            
        except Exception as e:
            logger.error(f"Error normalizing data: {str(e)}")
            raise
    
    def get_cleaning_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of cleaning operations performed.
        
        Returns:
            List[Dict[str, Any]]: List of cleaning operations
        """
        return self.cleaning_history 