"""
Economic data API connector
"""
import os
import time
import json
import hashlib
import random
import math
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from app.api.connectors.base_connector import BaseConnector

class EconomicConnector(BaseConnector):
    """Connector for economic data APIs"""
    
    def __init__(self):
        """Initialize the economic data connector"""
        super().__init__(
            name="Economic Indicators",
            description="Provides economic indicators such as inflation, stock indices, and currency exchange rates",
            cache_ttl=3600  # 1 hour cache
        )
        # API configuration
        self.api_key = os.environ.get('ECONOMIC_API_KEY', 'demo_key')
        self.base_url = "https://api.economicdata.org"  # Placeholder URL
        
        # Default country if none provided
        self.default_country = "US"
    
    def fetch_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch economic data based on parameters

        Args:
            params: Parameters for the economic data request
                - country: Country code (default: US)
                - indicator: Type of indicator (inflation, gdp, unemployment, stock_market, interest_rates, currency)
                - timeframe: Data timeframe (daily, weekly, monthly, quarterly, yearly)

        Returns:
            Dictionary of economic data
        """
        if params is None:
            params = {}

        # Get request parameters
        country = params.get('country', self.default_country)
        indicator = params.get('indicator', 'inflation')
        timeframe = params.get('timeframe', 'monthly')

        # Create cache key based on parameters
        cache_key = self._create_cache_key(country, indicator, timeframe)

        # Check cache first
        cached_data = self._check_cache(cache_key)
        if cached_data:
            return cached_data

        try:
            self._update_status("fetching")

            # Try to use real API data with fallback to simulated data
            if indicator == 'stock_market':
                # Use Alpha Vantage API for stock market data
                data = self._get_real_stock_market_data(country, timeframe)
            elif indicator == 'currency':
                # Use Alpha Vantage API for forex data
                data = self._get_real_currency_data(country, timeframe)
            else:
                # For other indicators, fallback to simulated data
                # These often require paid subscriptions or specialized APIs
                if indicator == 'inflation':
                    data = self._get_simulated_inflation_data(country, timeframe)
                elif indicator == 'gdp':
                    data = self._get_simulated_gdp_data(country, timeframe)
                elif indicator == 'unemployment':
                    data = self._get_simulated_unemployment_data(country, timeframe)
                elif indicator == 'interest_rates':
                    data = self._get_simulated_interest_rate_data(country, timeframe)
                else:
                    raise ValueError(f"Unsupported indicator: {indicator}")

            # Cache the results
            self._update_cache(cache_key, data)

            self._update_status("success")
            return data

        except Exception as e:
            self._update_status("error", e)
            print(f"Economic API error: {str(e)}")

            # Fallback to simulated data
            try:
                if indicator == 'inflation':
                    data = self._get_simulated_inflation_data(country, timeframe)
                elif indicator == 'gdp':
                    data = self._get_simulated_gdp_data(country, timeframe)
                elif indicator == 'unemployment':
                    data = self._get_simulated_unemployment_data(country, timeframe)
                elif indicator == 'stock_market':
                    data = self._get_simulated_stock_market_data(country, timeframe)
                elif indicator == 'interest_rates':
                    data = self._get_simulated_interest_rate_data(country, timeframe)
                elif indicator == 'currency':
                    data = self._get_simulated_currency_data(country, timeframe)
                else:
                    raise ValueError(f"Unsupported indicator: {indicator}")

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

    def _get_real_stock_market_data(self, country: str, timeframe: str) -> Dict[str, Any]:
        """Get real stock market data from Alpha Vantage API"""
        import requests

        # Map country to stock index/symbol
        symbol_mappings = {
            'US': 'SPY',  # S&P 500 ETF
            'UK': 'EZU',  # iShares MSCI Eurozone ETF
            'JP': 'EWJ',  # iShares MSCI Japan ETF
            'DE': 'EWG',  # iShares MSCI Germany ETF
            'FR': 'EWQ',  # iShares MSCI France ETF
            'CN': 'MCHI', # iShares MSCI China ETF
            'IN': 'INDA'  # iShares MSCI India ETF
        }

        # Get appropriate symbol
        symbol = symbol_mappings.get(country, 'SPY')

        # Map timeframe to API interval
        interval_mappings = {
            'daily': 'DAILY',
            'weekly': 'WEEKLY',
            'monthly': 'MONTHLY'
        }

        # Get appropriate interval
        interval = interval_mappings.get(timeframe, 'DAILY')

        try:
            # Make request to Alpha Vantage API - it's free but has usage limits
            api_key = self.api_key if self.api_key != 'demo_key' else 'demo'
            api_url = "https://www.alphavantage.co/query"

            response = requests.get(api_url, params={
                'function': f'TIME_SERIES_{interval}',
                'symbol': symbol,
                'apikey': api_key,
                'outputsize': 'compact'
            }, timeout=10)

            if response.status_code == 200:
                raw_data = response.json()

                # Check for API error messages
                if 'Error Message' in raw_data:
                    raise Exception(f"Alpha Vantage API error: {raw_data['Error Message']}")

                # Extract the time series data (different key based on interval)
                time_series_key = f"Time Series ({interval})"
                if 'Weekly' in interval:
                    time_series_key = "Weekly Time Series"
                elif 'Monthly' in interval:
                    time_series_key = "Monthly Time Series"

                # If the API is in demo mode or over rate limit, it may not return expected data
                if time_series_key not in raw_data:
                    raise Exception(f"Alpha Vantage API didn't return expected data. Keys: {list(raw_data.keys())}")

                time_series = raw_data[time_series_key]

                # Transform data into our standard format
                data_points = []

                # Sort dates (they come in reverse chronological order)
                sorted_dates = sorted(time_series.keys())

                for date_str in sorted_dates:
                    data = time_series[date_str]
                    data_points.append({
                        'date': date_str,
                        'value': float(data['4. close'])  # Use closing price
                    })

                # Map index name
                index_mappings = {
                    'US': 'S&P 500',
                    'UK': 'FTSE 100',
                    'JP': 'Nikkei 225',
                    'DE': 'DAX',
                    'FR': 'CAC 40',
                    'CN': 'Shanghai Composite',
                    'IN': 'BSE Sensex'
                }

                index_name = index_mappings.get(country, f"{country} Index")

                return {
                    'country': country,
                    'indicator': 'stock_market',
                    'index': index_name,
                    'unit': 'index_value',
                    'timeframe': timeframe,
                    'timestamp': datetime.now().isoformat(),
                    'data': data_points
                }
            else:
                raise Exception(f"Alpha Vantage API returned status code: {response.status_code}")

        except Exception as e:
            raise Exception(f"Stock market data fetch error: {str(e)}")

    def _get_real_currency_data(self, country: str, timeframe: str) -> Dict[str, Any]:
        """Get real currency exchange rate data from Alpha Vantage API"""
        import requests

        # Map country codes to currencies
        currency_mappings = {
            'US': 'USD',
            'JP': 'JPY',
            'UK': 'GBP',
            'EU': 'EUR',
            'CH': 'CHF',
            'CN': 'CNY',
            'CA': 'CAD',
            'AU': 'AUD'
        }

        # Get the currency code
        from_currency = currency_mappings.get(country, 'USD')
        to_currency = 'USD' if from_currency != 'USD' else 'EUR'  # If FROM is USD, use EUR as TO

        try:
            # Make request to Alpha Vantage FX API
            api_key = self.api_key if self.api_key != 'demo_key' else 'demo'
            api_url = "https://www.alphavantage.co/query"

            response = requests.get(api_url, params={
                'function': 'FX_DAILY',
                'from_symbol': from_currency,
                'to_symbol': to_currency,
                'apikey': api_key,
                'outputsize': 'compact'
            }, timeout=10)

            if response.status_code == 200:
                raw_data = response.json()

                # Check for API error messages
                if 'Error Message' in raw_data:
                    raise Exception(f"Alpha Vantage API error: {raw_data['Error Message']}")

                # If the API is in demo mode or over rate limit, it may not return expected data
                if 'Time Series FX (Daily)' not in raw_data:
                    raise Exception(f"Alpha Vantage API didn't return expected data. Keys: {list(raw_data.keys())}")

                time_series = raw_data['Time Series FX (Daily)']

                # Transform data into our standard format
                data_points = []

                # Sort dates (they come in reverse chronological order)
                sorted_dates = sorted(time_series.keys())

                for date_str in sorted_dates:
                    data = time_series[date_str]
                    data_points.append({
                        'date': date_str,
                        'value': float(data['4. close'])  # Use closing rate
                    })

                return {
                    'country': country,
                    'indicator': 'currency',
                    'currency': from_currency,
                    'against': to_currency,
                    'unit': 'exchange_rate',
                    'timeframe': timeframe,
                    'timestamp': datetime.now().isoformat(),
                    'data': data_points
                }
            else:
                raise Exception(f"Alpha Vantage API returned status code: {response.status_code}")

        except Exception as e:
            raise Exception(f"Currency data fetch error: {str(e)}")
    
    def _create_cache_key(self, country: str, indicator: str, timeframe: str) -> str:
        """Create a unique cache key based on request parameters"""
        params_str = f"{country}|{indicator}|{timeframe}"
        return f"economic_{hashlib.md5(params_str.encode()).hexdigest()}"
    
    def _get_simulated_inflation_data(self, country: str, timeframe: str) -> Dict[str, Any]:
        """Get simulated inflation data"""
        data_points = self._generate_time_series_data(
            base_value=3.0,  # Base inflation rate 
            volatility=0.5,  # Volatility of changes
            min_value=0.0,   # Minimum possible inflation
            max_value=10.0,  # Maximum possible inflation
            timeframe=timeframe,
            country_factor=self._get_country_factor(country)
        )
        
        return {
            'country': country,
            'indicator': 'inflation',
            'unit': 'percent',
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat(),
            'data': data_points
        }
    
    def _get_simulated_gdp_data(self, country: str, timeframe: str) -> Dict[str, Any]:
        """Get simulated GDP data"""
        # Base GDP growth around 2-3%
        country_factor = self._get_country_factor(country)
        base_value = 2.5 + (country_factor * 2)
        
        data_points = self._generate_time_series_data(
            base_value=base_value,
            volatility=0.7,
            min_value=-5.0,  # Allow for recessions
            max_value=10.0,  # Maximum growth
            timeframe=timeframe,
            country_factor=country_factor
        )
        
        return {
            'country': country,
            'indicator': 'gdp',
            'unit': 'percent_growth',
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat(),
            'data': data_points
        }
    
    def _get_simulated_unemployment_data(self, country: str, timeframe: str) -> Dict[str, Any]:
        """Get simulated unemployment data"""
        country_factor = self._get_country_factor(country)
        # Base unemployment rate - varies by country
        base_value = 5.0 + (country_factor * 3)
        
        data_points = self._generate_time_series_data(
            base_value=base_value,
            volatility=0.3,
            min_value=2.0,   # Minimum unemployment
            max_value=15.0,  # Maximum unemployment
            timeframe=timeframe,
            country_factor=country_factor
        )
        
        return {
            'country': country,
            'indicator': 'unemployment',
            'unit': 'percent',
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat(),
            'data': data_points
        }
    
    def _get_simulated_stock_market_data(self, country: str, timeframe: str) -> Dict[str, Any]:
        """Get simulated stock market data"""
        # Choose an index based on country
        index_mappings = {
            'US': 'S&P 500',
            'JP': 'Nikkei 225',
            'UK': 'FTSE 100',
            'DE': 'DAX',
            'FR': 'CAC 40',
            'CN': 'Shanghai Composite',
            'IN': 'BSE Sensex'
        }
        
        index_name = index_mappings.get(country, f"{country} Index")
        
        # Base value for the index - arbitrary starting point
        base_value = 1000 + (hash(country) % 3000)
        
        # Higher volatility for stock markets
        data_points = self._generate_time_series_data(
            base_value=base_value,
            volatility=2.0,
            min_value=base_value * 0.7,  # Allow for significant drops
            max_value=base_value * 1.3,  # And significant gains
            timeframe=timeframe,
            country_factor=self._get_country_factor(country),
            use_percentage=False  # Return absolute values
        )
        
        return {
            'country': country,
            'indicator': 'stock_market',
            'index': index_name,
            'unit': 'index_value',
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat(),
            'data': data_points
        }
    
    def _get_simulated_interest_rate_data(self, country: str, timeframe: str) -> Dict[str, Any]:
        """Get simulated interest rate data"""
        country_factor = self._get_country_factor(country)
        # Base interest rate - varies by country
        base_value = 2.0 + (country_factor * 2)
        
        data_points = self._generate_time_series_data(
            base_value=base_value,
            volatility=0.25,  # Interest rates change slowly
            min_value=0.0,    # Minimum rate (can't go below 0 historically)
            max_value=10.0,   # Maximum likely rate
            timeframe=timeframe,
            country_factor=country_factor
        )
        
        return {
            'country': country,
            'indicator': 'interest_rates',
            'unit': 'percent',
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat(),
            'data': data_points
        }
    
    def _get_simulated_currency_data(self, country: str, timeframe: str) -> Dict[str, Any]:
        """Get simulated currency exchange rate data"""
        # Map country codes to currencies
        currency_mappings = {
            'US': 'USD',
            'JP': 'JPY',
            'UK': 'GBP',
            'EU': 'EUR',
            'CH': 'CHF',
            'CN': 'CNY',
            'CA': 'CAD',
            'AU': 'AUD'
        }
        
        currency = currency_mappings.get(country, f"{country} Currency")
        
        # Generate exchange rates against USD
        base_rate = 1.0 if currency == 'USD' else 0.5 + (hash(currency) % 150) / 100
        
        data_points = self._generate_time_series_data(
            base_value=base_rate,
            volatility=0.01,  # Currency rates are often less volatile
            min_value=base_rate * 0.8,
            max_value=base_rate * 1.2,
            timeframe=timeframe,
            country_factor=self._get_country_factor(country),
            use_percentage=False  # Return absolute values
        )
        
        return {
            'country': country,
            'indicator': 'currency',
            'currency': currency,
            'against': 'USD',
            'unit': 'exchange_rate',
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat(),
            'data': data_points
        }
    
    def _get_country_factor(self, country: str) -> float:
        """
        Get a consistent factor for a country to ensure data is different but consistent.
        Returns a value between -0.5 and 0.5
        """
        # Use hash of country to get a consistent value
        return (hash(country) % 100) / 100 - 0.5
    
    def _generate_time_series_data(self, base_value: float, volatility: float, 
                                  min_value: float, max_value: float, timeframe: str,
                                  country_factor: float, use_percentage: bool = True) -> list:
        """
        Generate time series data with realistic patterns
        
        Args:
            base_value: Starting value for the time series
            volatility: How much the value can change between periods
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            timeframe: Type of time series (daily, weekly, monthly, etc.)
            country_factor: Factor to make data country-specific
            use_percentage: Whether to use percentage change or absolute values
            
        Returns:
            List of data points with timestamp and value
        """
        # Determine number of data points and time delta based on timeframe
        if timeframe == 'daily':
            num_points = 30  # 30 days
            delta = timedelta(days=1)
        elif timeframe == 'weekly':
            num_points = 52  # 1 year of weeks
            delta = timedelta(weeks=1)
        elif timeframe == 'monthly':
            num_points = 36  # 3 years of months
            delta = timedelta(days=30)
        elif timeframe == 'quarterly':
            num_points = 20  # 5 years of quarters
            delta = timedelta(days=91)
        elif timeframe == 'yearly':
            num_points = 10  # 10 years
            delta = timedelta(days=365)
        else:
            num_points = 12  # Default to monthly
            delta = timedelta(days=30)
        
        # Create data points
        data_points = []
        current_value = base_value
        end_date = datetime.now()
        
        # Seed the random generator based on country and timeframe for consistency
        random.seed(hash(f"{timeframe}_{country_factor}") % 1000000)
        
        for i in range(num_points):
            # Calculate the date, going backward from now
            point_date = end_date - (delta * (num_points - i - 1))
            
            # Add the data point
            data_points.append({
                'date': point_date.isoformat(),
                'value': round(current_value, 2)
            })
            
            # Update the value for the next point
            # Add some randomness but also a trend and seasonality
            trend = country_factor * 0.1  # Slight trend based on country
            seasonal = 0.2 * math.sin(i / (num_points / 2) * math.pi)  # Seasonal pattern
            random_change = (random.random() - 0.5) * volatility  # Random volatility
            
            if use_percentage:
                # For percentages, add the change
                change = trend + seasonal + random_change
                current_value += change
            else:
                # For absolute values, multiply by (1 + change)
                change = trend + seasonal + random_change
                current_value *= (1 + change / 100)
            
            # Ensure the value stays within bounds
            current_value = max(min_value, min(current_value, max_value))
        
        return data_points