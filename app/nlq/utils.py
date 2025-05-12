"""
Natural Language Query Utilities
Author: Ademola Solanke
Date: May 2025

This module provides utility functions for the Natural Language Query functionality.
"""

from typing import Dict, List, Any
import logging
import datetime

logger = logging.getLogger(__name__)

def format_query_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the query results for presentation in the UI.
    
    Args:
        results: The raw query results
        
    Returns:
        Formatted results for the UI
    """
    # For demo purposes, we'll just pass the results as-is
    return results

def _get_title_from_intent(intent):
    """Get a display title based on the query intent."""
    titles = {
        'simple_data': 'Data Overview',
        'correlation': 'Correlation Analysis',
        'prediction': 'Prediction Results',
        'comparison': 'Comparison Results',
        'anomaly': 'Anomaly Detection'
    }
    return titles.get(intent, 'Query Results')

def is_valid_query(query):
    """Check if a query is valid and non-empty."""
    if not query or not isinstance(query, str):
        return False
    
    # Basic check for minimum length
    if len(query.strip()) < 3:
        return False
    
    return True

def get_sample_queries_by_category() -> Dict[str, List[str]]:
    """
    Get sample queries organized by category.
    
    Returns:
        Dictionary of query categories with example queries
    """
    return {
        "data_queries": [
            "What's the current temperature?", 
            "Show me today's traffic congestion",
            "What is the market sentiment today?",
            "Display the average temperature for the past week"
        ],
        "correlation_queries": [
            "How does temperature affect traffic congestion?",
            "Is there a relationship between market volatility and social media sentiment?",
            "What factors correlate with travel time?",
            "Show the correlation between weather and public health metrics"
        ],
        "prediction_queries": [
            "Predict tomorrow's traffic congestion",
            "What will social media sentiment be if market volatility increases?",
            "Forecast economic indicators for next week",
            "Which model best predicts transportation patterns?"
        ]
    }

def parse_date_range(date_range_str: str) -> Dict[str, datetime.datetime]:
    """
    Parse a date range string into start and end dates.
    
    Args:
        date_range_str: String representing a date range
        
    Returns:
        Dictionary with start_date and end_date
    """
    # Default to last 7 days
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)
    
    # Try to parse the date range string
    # This is a simplified implementation
    if date_range_str:
        if "yesterday" in date_range_str.lower():
            start_date = end_date - datetime.timedelta(days=1)
            end_date = start_date
        elif "last week" in date_range_str.lower():
            start_date = end_date - datetime.timedelta(days=7)
        elif "last month" in date_range_str.lower():
            start_date = end_date - datetime.timedelta(days=30)
        elif "this year" in date_range_str.lower():
            start_date = datetime.datetime(end_date.year, 1, 1)
        elif "tomorrow" in date_range_str.lower():
            start_date = end_date + datetime.timedelta(days=1)
            end_date = start_date
    
    return {
        "start_date": start_date,
        "end_date": end_date
    }

def extract_domains_from_query(query: str) -> List[str]:
    """
    Extract domain keywords from a query.
    
    Args:
        query: The natural language query
        
    Returns:
        List of domain names
    """
    domains = []
    query_lower = query.lower()
    
    # Check for weather-related terms
    if any(term in query_lower for term in ["weather", "temperature", "rain", "humidity"]):
        domains.append("weather")
    
    # Check for traffic-related terms
    if any(term in query_lower for term in ["traffic", "congestion", "transportation", "commute"]):
        domains.append("transportation")
    
    # Check for economic-related terms
    if any(term in query_lower for term in ["economy", "market", "stock", "financial", "price"]):
        domains.append("economic")
    
    # Check for social media-related terms
    if any(term in query_lower for term in ["social", "media", "sentiment", "twitter", "facebook"]):
        domains.append("social_media")
    
    return domains