"""
API Clients module for handling various external API integrations.
This module contains client classes for different data sources including:
- Weather data
- Economic indicators
- Social media trends
"""

from .base_client import BaseAPIClient
from .weather_client import WeatherAPIClient
from .economic_client import EconomicAPIClient
from .social_client import SocialMediaAPIClient

__all__ = [
    'BaseAPIClient',
    'WeatherAPIClient',
    'EconomicAPIClient',
    'SocialMediaAPIClient'
] 