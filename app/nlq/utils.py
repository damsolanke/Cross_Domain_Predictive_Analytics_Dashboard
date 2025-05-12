"""
Natural Language Query Utilities Module
Author: Ademola Solanke
Date: May 2025

This module provides utility functions for the NLQ functionality.
"""

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def format_query_results(results):
    """
    Format query results for display.
    
    Args:
        results (dict): The raw query results.
        
    Returns:
        dict: Formatted results for display.
    """
    formatted = {
        'title': _get_title_from_intent(results.get('parsed', {}).get('intent', 'unknown')),
        'explanation': results.get('explanation', 'No explanation available.'),
        'visualizations': results.get('visualizations', []),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return formatted

def _get_title_from_intent(intent):
    """Get a display title based on query intent."""
    titles = {
        'simple_data': 'Data Results',
        'correlation': 'Correlation Analysis',
        'prediction': 'Prediction Results',
        'comparison': 'Comparison Results',
        'anomaly': 'Anomaly Detection',
        'unknown': 'Query Results'
    }
    
    return titles.get(intent, 'Query Results')

def log_query_to_history(query_text, results):
    """
    Log a query to the user's history.
    
    Args:
        query_text (str): The original query text.
        results (dict): The query results.
        
    Returns:
        bool: True if successfully logged, False otherwise.
    """
    try:
        # This would be replaced with actual history storage
        # E.g., database entry, file logging, etc.
        logger.info(f"Query logged: {query_text}")
        return True
    except Exception as e:
        logger.error(f"Error logging query to history: {e}")
        return False

def get_sample_queries_by_category():
    """
    Get sample queries organized by category.
    
    Returns:
        dict: Categories of sample queries.
    """
    return {
        "data": [
            "What's the current temperature?",
            "Show me today's traffic congestion",
            "What's the social media sentiment like?"
        ],
        "correlations": [
            "How does temperature affect traffic congestion?",
            "Is there a relationship between market volatility and social media sentiment?",
            "What factors correlate with travel time?"
        ],
        "predictions": [
            "Predict tomorrow's traffic congestion",
            "What will social media sentiment be next week?",
            "Forecast economic indicators for next month"
        ],
        "anomalies": [
            "Find unusual patterns in transportation data",
            "Identify anomalies in cross-domain correlations",
            "Show me outliers in weather-traffic relationships"
        ]
    }