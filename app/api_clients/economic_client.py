"""
Economic indicators API client for Alpha Vantage integration.
Provides economic data retrieval and processing functionality.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from .base_client import BaseAPIClient

class EconomicAPIClient(BaseAPIClient):
    def __init__(self, api_key: str, cache_dir: str = "cache/economic"):
        """
        Initialize the Economic API client.
        
        Args:
            api_key (str): Alpha Vantage API key
            cache_dir (str): Directory for caching economic data
        """
        super().__init__(
            base_url="https://www.alphavantage.co/query",
            api_key=api_key,
            cache_dir=cache_dir
        )
    
    def get_gdp(self, interval: str = 'quarterly') -> Dict[str, Any]:
        """
        Get GDP data.
        
        Args:
            interval (str): Data interval ('quarterly' or 'annual')
            
        Returns:
            Dict[str, Any]: GDP data
        """
        params = {
            'function': 'REAL_GDP',
            'interval': interval,
            'apikey': self.api_key
        }
        
        return self.get('', params=params)
    
    def get_inflation(self) -> Dict[str, Any]:
        """
        Get inflation data.
        
        Returns:
            Dict[str, Any]: Inflation data
        """
        params = {
            'function': 'INFLATION',
            'apikey': self.api_key
        }
        
        return self.get('', params=params)
    
    def get_unemployment(self) -> Dict[str, Any]:
        """
        Get unemployment data.
        
        Returns:
            Dict[str, Any]: Unemployment data
        """
        params = {
            'function': 'UNEMPLOYMENT',
            'apikey': self.api_key
        }
        
        return self.get('', params=params)
    
    def get_interest_rates(self) -> Dict[str, Any]:
        """
        Get interest rates data.
        
        Returns:
            Dict[str, Any]: Interest rates data
        """
        params = {
            'function': 'FEDERAL_FUNDS_RATE',
            'interval': 'monthly',
            'apikey': self.api_key
        }
        
        return self.get('', params=params)
    
    def get_retail_sales(self) -> Dict[str, Any]:
        """
        Get retail sales data.
        
        Returns:
            Dict[str, Any]: Retail sales data
        """
        params = {
            'function': 'RETAIL_SALES',
            'apikey': self.api_key
        }
        
        return self.get('', params=params)
    
    def process_economic_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw economic data into a standardized format.
        
        Args:
            data (Dict[str, Any]): Raw economic data from API
            
        Returns:
            Dict[str, Any]: Processed economic data
        """
        if 'data' not in data:
            return data
        
        processed_data = {
            'indicator': data.get('name', ''),
            'unit': data.get('unit', ''),
            'data': []
        }
        
        for item in data['data']:
            processed_item = {
                'date': item.get('date', ''),
                'value': float(item.get('value', 0)),
                'change': float(item.get('change', 0)) if 'change' in item else None
            }
            processed_data['data'].append(processed_item)
        
        return processed_data
    
    def get_all_indicators(self) -> Dict[str, Any]:
        """
        Get all economic indicators.
        
        Returns:
            Dict[str, Any]: Combined economic indicators data
        """
        indicators = {
            'gdp': self.get_gdp(),
            'inflation': self.get_inflation(),
            'unemployment': self.get_unemployment(),
            'interest_rates': self.get_interest_rates(),
            'retail_sales': self.get_retail_sales()
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'indicators': {
                name: self.process_economic_data(data)
                for name, data in indicators.items()
            }
        } 