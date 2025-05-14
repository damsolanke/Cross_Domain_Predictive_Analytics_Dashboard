"""
API endpoints for natural language query functionality.
"""

from flask import Blueprint, jsonify, request
from app.system_integration.natural_language_processor import NaturalLanguageProcessor
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
from app.system_integration.cross_domain_prediction import CrossDomainPredictor
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
nlq_api = Blueprint('nlq_api', __name__, url_prefix='/api/nlq')

# Initialize processor with global correlator and predictor
correlator = CrossDomainCorrelator()
predictor = CrossDomainPredictor(correlator=correlator)
nlp_processor = NaturalLanguageProcessor(correlator=correlator, predictor=predictor)

@nlq_api.route('/query', methods=['POST'])
def process_query():
    """Process a natural language query."""
    try:
        data = request.json
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query_text = data['query']
        
        # Process the query
        results = nlp_processor.process_query(query_text)
        
        # Log the query for analytics
        logger.info(f"NLQ: '{query_text}' -> Intent: {results.get('parsed', {}).get('intent')}")
        
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

@nlq_api.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get query suggestions based on available data."""
    try:
        # Get example queries organized by type
        suggestions = {
            "simple_queries": [
                "What's the current temperature?",
                "Show me today's traffic congestion",
                "What's the social media sentiment trend for the past week?"
            ],
            "correlation_queries": [
                "How does temperature affect traffic congestion?",
                "Is there a relationship between market volatility and social media sentiment?",
                "What factors correlate most strongly with travel time?"
            ],
            "prediction_queries": [
                "Predict tomorrow's traffic congestion based on weather forecast",
                "What will social media sentiment be if market volatility increases?",
                "Which model best predicts transportation patterns?"
            ],
            "analysis_queries": [
                "Compare weather patterns and traffic congestion over the last month",
                "Show the impact of weather on all other domains",
                "Identify anomalies in cross-domain correlations"
            ]
        }
        
        return jsonify(suggestions)
    
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return jsonify({'error': str(e)}), 500

@nlq_api.route('/history', methods=['GET'])
def get_query_history():
    """Get query history for the user."""
    try:
        # This would be replaced with actual query history retrieval
        # Placeholder implementation with some demo data
        history = [
            {
                "query": "What's the weather like today?",
                "timestamp": datetime.now().isoformat(),
                "intent": "simple_data"
            },
            {
                "query": "How does temperature affect traffic?",
                "timestamp": datetime.now().isoformat(),
                "intent": "correlation"
            },
            {
                "query": "Predict economic trends for next week",
                "timestamp": datetime.now().isoformat(),
                "intent": "prediction"
            },
            {
                "query": "Show anomalies in social media sentiment",
                "timestamp": datetime.now().isoformat(),
                "intent": "anomaly"
            }
        ]
        
        return jsonify(history)
    
    except Exception as e:
        logger.error(f"Error getting query history: {e}")
        return jsonify({'error': str(e)}), 500