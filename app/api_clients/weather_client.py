"""
Weather API client for OpenWeatherMap integration.
Provides weather data retrieval and processing functionality.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from .base_client import BaseAPIClient

class WeatherAPIClient(BaseAPIClient):
    def __init__(self, api_key: str, cache_dir: str = "cache/weather"):
        """
        Initialize the Weather API client.
        
        Args:
            api_key (str): OpenWeatherMap API key
            cache_dir (str): Directory for caching weather data
        """
        super().__init__(
            base_url="https://api.openweathermap.org/data/2.5",
            api_key=api_key,
            cache_dir=cache_dir
        )
    
    def get_current_weather(self, city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current weather data for a city.
        
        Args:
            city (str): City name
            country_code (Optional[str]): Two-letter country code
            
        Returns:
            Dict[str, Any]: Current weather data
        """
        params = {
            'q': f"{city},{country_code}" if country_code else city,
            'units': 'metric',
            'appid': self.api_key
        }
        
        return self.get('weather', params=params)
    
    def get_forecast(self, city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Get 5-day weather forecast for a city.
        
        Args:
            city (str): City name
            country_code (Optional[str]): Two-letter country code
            
        Returns:
            Dict[str, Any]: 5-day forecast data
        """
        params = {
            'q': f"{city},{country_code}" if country_code else city,
            'units': 'metric',
            'appid': self.api_key
        }
        
        return self.get('forecast', params=params)
    
    def get_historical_weather(self, lat: float, lon: float, 
                             start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Get historical weather data for a location.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            start_date (datetime): Start date for historical data
            end_date (datetime): End date for historical data
            
        Returns:
            Dict[str, Any]: Historical weather data
        """
        params = {
            'lat': lat,
            'lon': lon,
            'start': int(start_date.timestamp()),
            'end': int(end_date.timestamp()),
            'appid': self.api_key
        }
        
        return self.get('onecall/timemachine', params=params)
    
    def process_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw weather data into a standardized format.
        
        Args:
            data (Dict[str, Any]): Raw weather data from API
            
        Returns:
            Dict[str, Any]: Processed weather data
        """
        if 'list' in data:  # Forecast data
            return {
                'forecast': [
                    {
                        'timestamp': item['dt'],
                        'temperature': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'pressure': item['main']['pressure'],
                        'description': item['weather'][0]['description'],
                        'wind_speed': item['wind']['speed'],
                        'clouds': item['clouds']['all']
                    }
                    for item in data['list']
                ]
            }
        else:  # Current weather data
            return {
                'current': {
                    'timestamp': data['dt'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'clouds': data['clouds']['all']
                }
            } 