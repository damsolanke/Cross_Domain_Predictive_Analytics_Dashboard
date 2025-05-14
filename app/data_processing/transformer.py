"""
Data transformer class for handling data transformation operations.
Provides methods for feature engineering and data transformation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import logging
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)

class DataTransformer:
    def __init__(self):
        """Initialize the data transformer."""
        self.transformation_history = []
        self.scalers = {}
        self.encoders = {}
    
    def create_time_features(self, df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
        """
        Create time-based features from timestamp column.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            timestamp_col (str): Name of timestamp column
            
        Returns:
            pd.DataFrame: DataFrame with additional time features
        """
        try:
            df_transformed = df.copy()
            df_transformed[timestamp_col] = pd.to_datetime(df_transformed[timestamp_col])
            
            # Extract time features
            df_transformed['hour'] = df_transformed[timestamp_col].dt.hour
            df_transformed['day_of_week'] = df_transformed[timestamp_col].dt.dayofweek
            df_transformed['month'] = df_transformed[timestamp_col].dt.month
            df_transformed['year'] = df_transformed[timestamp_col].dt.year
            df_transformed['is_weekend'] = df_transformed['day_of_week'].isin([5, 6]).astype(int)
            
            self.transformation_history.append({
                'timestamp': datetime.now(),
                'operation': 'create_time_features',
                'features_added': ['hour', 'day_of_week', 'month', 'year', 'is_weekend']
            })
            
            return df_transformed
            
        except Exception as e:
            logger.error(f"Error creating time features: {str(e)}")
            raise
    
    def create_lag_features(self, df: pd.DataFrame, columns: List[str], 
                          lags: List[int], group_by: Optional[str] = None) -> pd.DataFrame:
        """
        Create lag features for specified columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): Columns to create lag features for
            lags (List[int]): List of lag periods
            group_by (Optional[str]): Column to group by when creating lags
            
        Returns:
            pd.DataFrame: DataFrame with lag features
        """
        try:
            df_transformed = df.copy()
            
            for col in columns:
                if col in df.columns:
                    for lag in lags:
                        if group_by:
                            df_transformed[f'{col}_lag_{lag}'] = df_transformed.groupby(group_by)[col].shift(lag)
                        else:
                            df_transformed[f'{col}_lag_{lag}'] = df_transformed[col].shift(lag)
            
            self.transformation_history.append({
                'timestamp': datetime.now(),
                'operation': 'create_lag_features',
                'columns': columns,
                'lags': lags
            })
            
            return df_transformed
            
        except Exception as e:
            logger.error(f"Error creating lag features: {str(e)}")
            raise
    
    def create_rolling_features(self, df: pd.DataFrame, columns: List[str],
                              windows: List[int], group_by: Optional[str] = None) -> pd.DataFrame:
        """
        Create rolling window features for specified columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): Columns to create rolling features for
            windows (List[int]): List of window sizes
            group_by (Optional[str]): Column to group by when creating rolling features
            
        Returns:
            pd.DataFrame: DataFrame with rolling features
        """
        try:
            df_transformed = df.copy()
            
            for col in columns:
                if col in df.columns:
                    for window in windows:
                        if group_by:
                            df_transformed[f'{col}_rolling_mean_{window}'] = df_transformed.groupby(group_by)[col].transform(
                                lambda x: x.rolling(window=window, min_periods=1).mean()
                            )
                            df_transformed[f'{col}_rolling_std_{window}'] = df_transformed.groupby(group_by)[col].transform(
                                lambda x: x.rolling(window=window, min_periods=1).std()
                            )
                        else:
                            df_transformed[f'{col}_rolling_mean_{window}'] = df_transformed[col].rolling(
                                window=window, min_periods=1
                            ).mean()
                            df_transformed[f'{col}_rolling_std_{window}'] = df_transformed[col].rolling(
                                window=window, min_periods=1
                            ).std()
            
            self.transformation_history.append({
                'timestamp': datetime.now(),
                'operation': 'create_rolling_features',
                'columns': columns,
                'windows': windows
            })
            
            return df_transformed
            
        except Exception as e:
            logger.error(f"Error creating rolling features: {str(e)}")
            raise
    
    def encode_categorical_features(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Encode categorical features using one-hot encoding.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): Categorical columns to encode
            
        Returns:
            pd.DataFrame: DataFrame with encoded categorical features
        """
        try:
            df_transformed = df.copy()
            
            for col in columns:
                if col in df.columns:
                    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
                    encoded = encoder.fit_transform(df_transformed[[col]])
                    encoded_df = pd.DataFrame(
                        encoded,
                        columns=[f'{col}_{val}' for val in encoder.categories_[0]],
                        index=df_transformed.index
                    )
                    df_transformed = pd.concat([df_transformed, encoded_df], axis=1)
                    df_transformed = df_transformed.drop(col, axis=1)
                    self.encoders[col] = encoder
            
            self.transformation_history.append({
                'timestamp': datetime.now(),
                'operation': 'encode_categorical_features',
                'columns': columns
            })
            
            return df_transformed
            
        except Exception as e:
            logger.error(f"Error encoding categorical features: {str(e)}")
            raise
    
    def scale_numeric_features(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Scale numeric features using StandardScaler.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): Numeric columns to scale
            
        Returns:
            pd.DataFrame: DataFrame with scaled numeric features
        """
        try:
            df_transformed = df.copy()
            
            for col in columns:
                if col in df.columns:
                    scaler = StandardScaler()
                    df_transformed[col] = scaler.fit_transform(df_transformed[[col]])
                    self.scalers[col] = scaler
            
            self.transformation_history.append({
                'timestamp': datetime.now(),
                'operation': 'scale_numeric_features',
                'columns': columns
            })
            
            return df_transformed
            
        except Exception as e:
            logger.error(f"Error scaling numeric features: {str(e)}")
            raise
    
    def get_transformation_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of transformation operations performed.
        
        Returns:
            List[Dict[str, Any]]: List of transformation operations
        """
        return self.transformation_history 