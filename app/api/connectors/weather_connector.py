"""
Weather API connector
"""
import os
import time
import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from app.api.connectors.base_connector import BaseConnector

class WeatherConnector(BaseConnector):
    """Connector for weather data APIs"""
    
    def __init__(self):
        """Initialize the weather connector"""
        super().__init__(
            name="Weather Data",
            description="Provides weather forecasts and historical weather data",
            cache_ttl=1800  # 30 minutes cache
        )
        # API configuration
        self.api_key = os.environ.get('OPENWEATHER_API_KEY', 'demo_key')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # Default location if none provided
        self.default_location = "New York,US"
    
    def fetch_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch weather data based on parameters

        Args:
            params: Parameters for the weather data request
                - location: City name or coordinates (default: New York,US)
                - units: Units of measurement (metric, imperial, standard)
                - type: Type of data (current, forecast, historical)

        Returns:
            Dictionary of weather data
        """
        if params is None:
            params = {}

        # Get request parameters
        location = params.get('location', self.default_location)
        units = params.get('units', 'metric')
        data_type = params.get('type', 'current')

        # Create cache key based on parameters
        cache_key = self._create_cache_key(location, units, data_type)

        # Check cache first
        cached_data = self._check_cache(cache_key)
        if cached_data:
            return cached_data

        try:
            self._update_status("fetching")

            # Use real OpenWeatherMap API with fallback to simulated data
            import requests

            # Determine which API endpoint to use
            if data_type == 'current':
                # Current weather API endpoint
                api_url = f"{self.base_url}/weather"
                data = self._get_real_current_weather(api_url, location, units)
            elif data_type == 'forecast':
                # 5-day forecast API endpoint
                api_url = f"{self.base_url}/forecast"
                data = self._get_real_forecast(api_url, location, units)
            elif data_type == 'historical':
                # Historical data requires OneCall API subscription
                # Simulate this data since the free API doesn't have it
                data = self._get_simulated_historical_weather(location, units)
            else:
                raise ValueError(f"Unsupported data type: {data_type}")

            # Cache the results
            self._update_cache(cache_key, data)

            self._update_status("success")
            return data

        except Exception as e:
            self._update_status("error", e)
            print(f"Weather API error: {str(e)}")

            # Fallback to simulated data
            try:
                if data_type == 'current':
                    data = self._get_simulated_current_weather(location, units)
                elif data_type == 'forecast':
                    data = self._get_simulated_forecast(location, units)
                elif data_type == 'historical':
                    data = self._get_simulated_historical_weather(location, units)
                else:
                    raise ValueError(f"Unsupported data type: {data_type}")

                # Cache the fallback results
                self._update_cache(cache_key, data)

                self._update_status("using fallback data")
                return data
            except Exception as fallback_error:
                self._update_status("error", fallback_error)
                return {
                    'error': str(e),
                    'fallback_error': str(fallback_error),
                    'status': 'error'
                }

    def _get_real_current_weather(self, api_url: str, location: str, units: str) -> Dict[str, Any]:
        """Get real current weather data from OpenWeatherMap API"""
        import requests

        try:
            # Make the API request using the free OpenWeatherMap API
            response = requests.get(api_url, params={
                'q': location,
                'units': units,
                'appid': self.api_key
            }, timeout=5)

            # Check if the request was successful
            if response.status_code == 200:
                raw_data = response.json()

                # Transform raw API data into our standardized format
                return {
                    'location': location,
                    'timestamp': datetime.now().isoformat(),
                    'current': {
                        'temp': raw_data['main']['temp'],
                        'feels_like': raw_data['main']['feels_like'],
                        'temp_min': raw_data['main']['temp_min'],
                        'temp_max': raw_data['main']['temp_max'],
                        'humidity': raw_data['main']['humidity'],
                        'pressure': raw_data['main']['pressure'],
                        'wind_speed': raw_data['wind']['speed'],
                        'wind_direction': raw_data['wind']['deg'],
                        'clouds': raw_data['clouds']['all'],
                        'weather': {
                            'main': raw_data['weather'][0]['main'],
                            'description': raw_data['weather'][0]['description']
                        }
                    },
                    'units': units
                }
            else:
                # If API call fails, throw an error with the status code
                raise Exception(f"OpenWeatherMap API returned status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")

    def _get_real_forecast(self, api_url: str, location: str, units: str) -> Dict[str, Any]:
        """Get real forecast data from OpenWeatherMap API"""
        import requests

        try:
            # Make the API request using the free OpenWeatherMap API
            response = requests.get(api_url, params={
                'q': location,
                'units': units,
                'appid': self.api_key
            }, timeout=5)

            # Check if the request was successful
            if response.status_code == 200:
                raw_data = response.json()

                # Transform the 3-hour forecast into daily forecast
                forecast = []
                daily_data = {}

                for item in raw_data['list']:
                    # Extract date (ignoring time)
                    dt = datetime.fromtimestamp(item['dt'])
                    date_str = dt.strftime('%Y-%m-%d')

                    # Initialize day data if not exists
                    if date_str not in daily_data:
                        daily_data[date_str] = {
                            'temps': [],
                            'humidity': [],
                            'pressure': [],
                            'wind_speed': [],
                            'weather_main': [],
                            'weather_desc': [],
                            'precipitation_chance': []
                        }

                    # Add data points
                    daily_data[date_str]['temps'].append(item['main']['temp'])
                    daily_data[date_str]['humidity'].append(item['main']['humidity'])
                    daily_data[date_str]['pressure'].append(item['main']['pressure'])
                    daily_data[date_str]['wind_speed'].append(item['wind']['speed'])
                    daily_data[date_str]['weather_main'].append(item['weather'][0]['main'])
                    daily_data[date_str]['weather_desc'].append(item['weather'][0]['description'])
                    daily_data[date_str]['precipitation_chance'].append(item.get('pop', 0))

                # Calculate daily values
                for date_str, data in daily_data.items():
                    # Use most common weather condition
                    from collections import Counter
                    weather_main = Counter(data['weather_main']).most_common(1)[0][0]
                    weather_desc = Counter(data['weather_desc']).most_common(1)[0][0]

                    # Create forecast item
                    forecast.append({
                        'date': int(datetime.strptime(date_str, '%Y-%m-%d').timestamp()),
                        'temp': {
                            'day': sum(data['temps']) / len(data['temps']),
                            'min': min(data['temps']),
                            'max': max(data['temps']),
                            'night': data['temps'][-1] if len(data['temps']) > 0 else 0,
                        },
                        'humidity': sum(data['humidity']) / len(data['humidity']),
                        'pressure': sum(data['pressure']) / len(data['pressure']),
                        'wind_speed': sum(data['wind_speed']) / len(data['wind_speed']),
                        'weather': {
                            'main': weather_main,
                            'description': weather_desc
                        },
                        'precipitation_chance': max(data['precipitation_chance'])
                    })

                # Sort by date
                forecast.sort(key=lambda x: x['date'])

                # Return formatted result
                return {
                    'location': location,
                    'timestamp': datetime.now().isoformat(),
                    'forecast': forecast,
                    'units': units
                }
            else:
                # If API call fails, throw an error with the status code
                raise Exception(f"OpenWeatherMap API returned status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")
    
    def _create_cache_key(self, location: str, units: str, data_type: str) -> str:
        """Create a unique cache key based on request parameters"""
        params_str = f"{location}|{units}|{data_type}"
        return f"weather_{hashlib.md5(params_str.encode()).hexdigest()}"
    
    def _get_simulated_current_weather(self, location: str, units: str) -> Dict[str, Any]:
        """Get simulated current weather data"""
        # Create realistic but simulated weather data
        temp_base = 20 if units == 'metric' else 68
        temp_offset = hash(location + str(int(time.time() / 3600))) % 10
        
        return {
            'location': location,
            'timestamp': datetime.now().isoformat(),
            'current': {
                'temp': temp_base + temp_offset,
                'feels_like': temp_base + temp_offset - 2,
                'temp_min': temp_base + temp_offset - 5,
                'temp_max': temp_base + temp_offset + 5,
                'humidity': 60 + (hash(location) % 30),
                'pressure': 1015 + (hash(location) % 10),
                'wind_speed': 5 + (hash(location + 'wind') % 15),
                'wind_direction': hash(location + 'dir') % 360,
                'clouds': hash(location + 'clouds') % 100,
                'weather': {
                    'main': self._get_random_weather_condition(location),
                    'description': 'Simulated weather condition'
                }
            },
            'units': units
        }
    
    def _get_simulated_forecast(self, location: str, units: str) -> Dict[str, Any]:
        """Get simulated forecast weather data"""
        forecast = []
        temp_base = 20 if units == 'metric' else 68
        
        # Create a 5-day forecast
        for day in range(5):
            # Use day and location to create deterministic but varying values
            day_seed = hash(location + str(day) + str(int(time.time() / 86400)))
            temp_offset = day_seed % 15 - 5  # -5 to +10 range
            
            # Random weather condition that changes over time
            condition = self._get_random_weather_condition(location + str(day))
            
            forecast.append({
                'date': (datetime.now().replace(hour=12, minute=0, second=0, microsecond=0).timestamp() + day * 86400),
                'temp': {
                    'day': temp_base + temp_offset,
                    'min': temp_base + temp_offset - 5,
                    'max': temp_base + temp_offset + 5,
                    'night': temp_base + temp_offset - 8,
                },
                'humidity': 60 + (day_seed % 30),
                'pressure': 1015 + (day_seed % 10),
                'wind_speed': 5 + (day_seed % 15),
                'weather': {
                    'main': condition,
                    'description': f'Simulated {condition.lower()} conditions'
                },
                'precipitation_chance': day_seed % 100 / 100
            })
        
        return {
            'location': location,
            'timestamp': datetime.now().isoformat(),
            'forecast': forecast,
            'units': units
        }
    
    def _get_simulated_historical_weather(self, location: str, units: str) -> Dict[str, Any]:
        """Get simulated historical weather data"""
        # Similar to forecast but for past days
        historical = []
        temp_base = 20 if units == 'metric' else 68
        
        # 5-day historical data
        for day in range(1, 6):
            # Use day and location to create deterministic but varying values
            day_seed = hash(location + str(day) + str(int(time.time() / 86400)))
            temp_offset = day_seed % 15 - 5  # -5 to +10 range
            
            condition = self._get_random_weather_condition(location + str(day))
            
            historical.append({
                'date': (datetime.now().replace(hour=12, minute=0, second=0, microsecond=0).timestamp() - day * 86400),
                'temp': {
                    'avg': temp_base + temp_offset,
                    'min': temp_base + temp_offset - 5,
                    'max': temp_base + temp_offset + 5,
                },
                'humidity': 60 + (day_seed % 30),
                'pressure': 1015 + (day_seed % 10),
                'wind_speed': 5 + (day_seed % 15),
                'weather': {
                    'main': condition,
                    'description': f'Simulated {condition.lower()} conditions'
                },
                'precipitation': (day_seed % 20) / 10  # 0 to 2 cm
            })
        
        return {
            'location': location,
            'timestamp': datetime.now().isoformat(),
            'historical': historical,
            'units': units
        }
    
    def _get_random_weather_condition(self, seed: str) -> str:
        """Get a random weather condition based on a seed string"""
        conditions = ["Clear", "Clouds", "Rain", "Drizzle", "Thunderstorm", "Snow", "Mist", "Fog"]
        index = hash(seed + str(int(time.time() / 86400))) % len(conditions)
        return conditions[index]