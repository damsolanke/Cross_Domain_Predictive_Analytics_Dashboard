"""
API connector implementations for external data sources.
"""

import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from app.system_integration.data_integration import APIDataSource, DataIntegrator
from app.system_integration.integration import system_integrator

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
ECONOMIC_API_KEY = os.getenv('ECONOMIC_API_KEY')
SOCIAL_MEDIA_API_KEY = os.getenv('SOCIAL_MEDIA_API_KEY')
TRANSPORTATION_API_KEY = os.getenv('TRANSPORTATION_API_KEY')

# Create data integrator
data_integrator = DataIntegrator()

def init_api_connectors():
    """Initialize all API connectors and register them with the system integrator."""
    logger.info("Initializing API connectors...")
    
    # Register data integrator with system
    system_integrator.register_component('data_integrator', data_integrator)
    
    # Initialize API connectors if API keys are available
    init_weather_connector()
    init_economic_connector()
    init_social_media_connector()
    init_transportation_connector()
    
    # Start data processing
    data_integrator.start_processing()
    
    logger.info("API connectors initialized.")
    return data_integrator

def init_weather_connector():
    """Initialize weather data connector using OpenWeatherMap API."""
    if not WEATHER_API_KEY:
        logger.warning("Weather API key not found. Using fallback mock data.")
        return None
    
    try:
        # Create weather API connector
        # Using current weather data for a specific city (New York as default)
        weather_source = APIDataSource(
            name="openweathermap",
            domain="weather",
            url="https://api.openweathermap.org/data/2.5/weather",
            method="GET",
            params={
                "q": "New York,us",  # Can be parameterized later
                "appid": WEATHER_API_KEY,
                "units": "imperial"  # For Fahrenheit temperatures
            },
            data_path="",  # Root of response
            config={
                "update_interval": 1800  # Update every 30 minutes
            }
        )
        
        # Transform function to extract relevant weather data
        original_transform = weather_source.transform_data
        def weather_transform(data):
            base = original_transform(data)
            
            # Extract relevant fields from OpenWeatherMap response
            if 'main' in data and 'weather' in data and len(data['weather']) > 0:
                base.update({
                    'temperature': data['main'].get('temp'),
                    'humidity': data['main'].get('humidity'),
                    'pressure': data['main'].get('pressure'),
                    'condition': data['weather'][0].get('main'),
                    'description': data['weather'][0].get('description'),
                    'wind_speed': data.get('wind', {}).get('speed'),
                    'cloudiness': data.get('clouds', {}).get('all'),
                    'location': data.get('name')
                })
            
            return base
        
        # Replace transform method
        weather_source.transform_data = weather_transform
        
        # Register with data integrator
        data_integrator.register_data_source(weather_source)
        
        # Start collecting data
        data_integrator.start_source("openweathermap", interval=1800)
        
        logger.info("Weather API connector initialized successfully.")
        return weather_source
    
    except Exception as e:
        logger.error(f"Failed to initialize weather API connector: {e}")
        return None

def init_economic_connector():
    """Initialize economic data connector using Alpha Vantage API."""
    if not ECONOMIC_API_KEY:
        logger.warning("Economic API key not found. Using fallback mock data.")
        return None
    
    try:
        # Create economic API connector for GDP data
        economic_source = APIDataSource(
            name="alphavantage_gdp",
            domain="economic",
            url="https://www.alphavantage.co/query",
            method="GET",
            params={
                "function": "REAL_GDP",
                "interval": "quarterly",
                "apikey": ECONOMIC_API_KEY
            },
            data_path="data",  # Path to the data in the response
            config={
                "update_interval": 86400  # Update daily (economic data changes less frequently)
            }
        )
        
        # Transform function to extract relevant economic data
        original_transform = economic_source.transform_data
        def economic_transform(data):
            base = original_transform({})
            
            # Extract latest GDP data point
            if isinstance(data, list) and len(data) > 0:
                latest = data[0]  # Most recent data point
                base.update({
                    'gdp_value': latest.get('value'),
                    'gdp_date': latest.get('date'),
                    'indicator': 'REAL_GDP'
                })
            
            return base
        
        # Replace transform method
        economic_source.transform_data = economic_transform
        
        # Register with data integrator
        data_integrator.register_data_source(economic_source)
        
        # Start collecting data
        data_integrator.start_source("alphavantage_gdp", interval=86400)
        
        logger.info("Economic API connector initialized successfully.")
        return economic_source
    
    except Exception as e:
        logger.error(f"Failed to initialize economic API connector: {e}")
        return None

def init_social_media_connector():
    """Initialize social media data connector using News API."""
    if not SOCIAL_MEDIA_API_KEY:
        logger.warning("Social Media API key not found. Using fallback mock data.")
        return None
    
    try:
        # Create social media API connector
        social_media_source = APIDataSource(
            name="newsapi",
            domain="social_media",
            url="https://newsapi.org/v2/top-headlines",
            method="GET",
            params={
                "country": "us",
                "apiKey": SOCIAL_MEDIA_API_KEY
            },
            data_path="articles",  # Path to the articles in the response
            config={
                "update_interval": 3600  # Update hourly
            }
        )
        
        # Transform function to extract relevant social media data
        original_transform = social_media_source.transform_data
        def social_media_transform(data):
            base = original_transform({})
            
            # Calculate basic sentiment and engagement metrics
            if isinstance(data, list):
                # Simple metric: count of articles
                article_count = len(data)
                
                # Extract topics (categories)
                topics = {}
                for article in data:
                    if 'title' in article:
                        # Simple naive sentiment calculation based on title
                        # (this would be replaced with proper NLP in production)
                        title = article.get('title', '')
                        sentiment = 0.5  # Neutral by default
                        
                        # Very simple sentiment adjustment based on keywords
                        positive_words = ['good', 'great', 'rise', 'growth', 'success', 'positive']
                        negative_words = ['bad', 'fail', 'drop', 'crisis', 'negative', 'fall']
                        
                        for word in positive_words:
                            if word in title.lower():
                                sentiment += 0.1
                        
                        for word in negative_words:
                            if word in title.lower():
                                sentiment -= 0.1
                        
                        sentiment = max(0, min(1, sentiment))  # Clamp to 0-1 range
                        
                        # Extract source
                        source = article.get('source', {}).get('name', 'Unknown')
                        
                        # Add to topics dict
                        if source not in topics:
                            topics[source] = {
                                'sentiment': sentiment,
                                'count': 1
                            }
                        else:
                            topics[source]['count'] += 1
                            topics[source]['sentiment'] = (topics[source]['sentiment'] + sentiment) / 2
                
                # Calculate average sentiment
                avg_sentiment = 0.5
                if topics:
                    total_sentiment = sum(t['sentiment'] for t in topics.values())
                    avg_sentiment = total_sentiment / len(topics)
                
                # Update base with calculated metrics
                base.update({
                    'trending_topics': [{'topic': k, 'sentiment': v['sentiment'], 'volume': v['count']} 
                                       for k, v in topics.items()],
                    'article_count': article_count,
                    'sentiment': avg_sentiment
                })
            
            return base
        
        # Replace transform method
        social_media_source.transform_data = social_media_transform
        
        # Register with data integrator
        data_integrator.register_data_source(social_media_source)
        
        # Start collecting data
        data_integrator.start_source("newsapi", interval=3600)
        
        logger.info("Social media API connector initialized successfully.")
        return social_media_source
    
    except Exception as e:
        logger.error(f"Failed to initialize social media API connector: {e}")
        return None

def init_transportation_connector():
    """Initialize transportation data connector using TomTom API."""
    if not TRANSPORTATION_API_KEY:
        logger.warning("Transportation API key not found. Using fallback mock data.")
        return None
    
    try:
        # Create transportation API connector for traffic flow data
        # Using New York as default location
        transportation_source = APIDataSource(
            name="tomtom_traffic",
            domain="transportation",
            url="https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json",
            method="GET",
            params={
                "point": "40.7128,-74.0060",  # New York coordinates
                "key": TRANSPORTATION_API_KEY
            },
            data_path="flowSegmentData",  # Path to the data in the response
            config={
                "update_interval": 900  # Update every 15 minutes
            }
        )
        
        # Transform function to extract relevant transportation data
        original_transform = transportation_source.transform_data
        def transportation_transform(data):
            base = original_transform({})
            
            # Extract relevant traffic flow data
            if isinstance(data, dict):
                base.update({
                    'average_speed': data.get('currentSpeed', 0),
                    'free_flow_speed': data.get('freeFlowSpeed', 0),
                    'current_travel_time': data.get('currentTravelTime', 0),
                    'free_flow_travel_time': data.get('freeFlowTravelTime', 0),
                    'confidence': data.get('confidence', 0),
                })
                
                # Calculate congestion level (as percentage of slowdown from free flow)
                if data.get('freeFlowSpeed', 0) > 0:
                    congestion = (1 - (data.get('currentSpeed', 0) / data.get('freeFlowSpeed', 1))) * 100
                    base['congestion_level'] = max(0, min(100, congestion))
                else:
                    base['congestion_level'] = 0
            
            return base
        
        # Replace transform method
        transportation_source.transform_data = transportation_transform
        
        # Register with data integrator
        data_integrator.register_data_source(transportation_source)
        
        # Start collecting data
        data_integrator.start_source("tomtom_traffic", interval=900)
        
        logger.info("Transportation API connector initialized successfully.")
        return transportation_source
    
    except Exception as e:
        logger.error(f"Failed to initialize transportation API connector: {e}")
        return None 