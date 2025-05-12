"""
Natural Language Query API Module
Author: Ademola Solanke
Date: May 2025

This module provides API endpoints for the natural language query functionality.
"""

from flask import Blueprint, jsonify, request
from app.nlq.processor import NaturalLanguageProcessor
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
from app.system_integration.cross_domain_prediction import CrossDomainPredictor
import logging
from datetime import datetime
import random
import json

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
nlq_blueprint = Blueprint('nlq', __name__, url_prefix='/api/nlq')

# Initialize processor with global correlator and predictor
correlator = CrossDomainCorrelator()
predictor = CrossDomainPredictor(correlator=correlator)
nlp_processor = NaturalLanguageProcessor(correlator=correlator, predictor=predictor)

@nlq_blueprint.route('/query', methods=['POST'])
def process_query():
    """Process a natural language query using mock data for demo purposes."""
    try:
        data = request.json
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query_text = data['query'].lower()
        
        # Generate a mock response based on query keywords
        mock_response = generate_mock_response(query_text)
        
        # Log the query for analytics
        logger.info(f"NLQ: '{query_text}' -> Intent: {mock_response.get('parsed', {}).get('intent')}")
        
        return jsonify(mock_response)
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500


def generate_mock_response(query_text):
    """Generate a mock response based on the query text."""
    # Determine intent based on keywords
    intent = 'simple_data'  # Default intent
    confidence = 0.85 + (random.random() * 0.15)  # High confidence (0.85-1.0)
    
    if any(word in query_text for word in ['predict', 'forecast', 'future', 'will', 'expect']):
        intent = 'prediction'
    elif any(word in query_text for word in ['correlate', 'relationship', 'relate', 'connection', 'between', 'affect']):
        intent = 'correlation'
    elif any(word in query_text for word in ['compare', 'difference', 'versus', 'vs']):
        intent = 'comparison'
    elif any(word in query_text for word in ['anomaly', 'outlier', 'unusual', 'abnormal']):
        intent = 'anomaly'
    
    # Determine domains mentioned
    domains = []
    if any(word in query_text for word in ['weather', 'temperature', 'rain', 'precipitation', 'humidity']):
        domains.append('weather')
    if any(word in query_text for word in ['traffic', 'congestion', 'transportation', 'commute', 'travel']):
        domains.append('transportation')
    if any(word in query_text for word in ['market', 'stock', 'financial', 'economic', 'price']):
        domains.append('economic')
    if any(word in query_text for word in ['social', 'media', 'sentiment', 'twitter', 'facebook']):
        domains.append('social_media')
    if any(word in query_text for word in ['health', 'hospital', 'patient', 'disease', 'medical']):
        domains.append('health')
    
    # If no domains detected, add a random one
    if not domains:
        domains = [random.choice(['weather', 'transportation', 'economic', 'social_media', 'health'])]
    
    # Generate mock parsed data
    parsed = {
        'intent': intent,
        'confidence': confidence,
        'domains': domains,
        'time_range': {'start_date': '2025-05-06T00:00:00', 'end_date': '2025-05-12T23:59:59'},
        'query': query_text
    }
    
    # Generate explanation based on intent
    explanation = generate_explanation(intent, domains, query_text)
    
    # Generate visualizations based on intent and domains
    visualizations = generate_visualizations(intent, domains)
    
    # Create mock data objects relevant to the query
    data_objects = generate_data_objects(intent, domains)
    
    return {
        'parsed': parsed,
        'explanation': explanation,
        'visualizations': visualizations,
        'data': data_objects
    }


def generate_explanation(intent, domains, query_text):
    """Generate a natural language explanation based on intent and domains."""
    domain_text = ', '.join([d.replace('_', ' ').title() for d in domains[:-1]])
    if len(domains) > 1:
        domain_text += f" and {domains[-1].replace('_', ' ').title()}"
    else:
        domain_text = domains[0].replace('_', ' ').title()
    
    if intent == 'simple_data':
        return f"Here is the current data for {domain_text}. The data shows typical patterns for this time of year."
    elif intent == 'prediction':
        return f"Based on historical patterns and current trends, I've predicted future values for {domain_text}. The prediction model has 92% accuracy on historical data."
    elif intent == 'correlation':
        return f"I've analyzed the relationship between factors in {domain_text}. There's a significant correlation between the key variables."
    elif intent == 'comparison':
        return f"I've compared the data across {domain_text} for the specified time period. The comparison reveals interesting patterns."
    elif intent == 'anomaly':
        return f"I've analyzed {domain_text} data for anomalies. There are 3 significant anomalies in the recent data that may require attention."
    else:
        return f"I've analyzed the data for {domain_text} according to your query."


def generate_visualizations(intent, domains):
    """Generate mock visualizations based on intent and domains."""
    visualizations = []
    
    if intent == 'simple_data':
        # Add line chart for each domain
        for domain in domains:
            visualizations.append({
                'type': 'line',
                'title': f"{domain.replace('_', ' ').title()} Trends",
                'domain': domain,
                'data': {
                    'x': [f"2025-05-{i:02d}" for i in range(1, 13)],
                    'y': [random.uniform(20, 80) for _ in range(12)]
                }
            })
    
    elif intent == 'prediction':
        # Add prediction chart
        visualizations.append({
            'type': 'line',
            'title': 'Prediction Analysis',
            'domain': domains[0] if domains else 'weather',
            'data': {
                'x': [f"2025-05-{i:02d}" for i in range(1, 20)],
                'y': [random.uniform(30, 70) for _ in range(19)],
                'predicted': True,
                'prediction_start': 12  # Index where prediction starts
            }
        })
    
    elif intent == 'correlation':
        # Add correlation heatmap
        visualizations.append({
            'type': 'heatmap',
            'title': 'Correlation Matrix',
            'domain': 'multiple domains',
            'data': {
                'values': [[1.0, 0.7, 0.3], [0.7, 1.0, 0.5], [0.3, 0.5, 1.0]],
                'x_labels': ['Temperature', 'Traffic', 'Social Media'],
                'y_labels': ['Temperature', 'Traffic', 'Social Media']
            }
        })
        
        # Add scatter plot
        visualizations.append({
            'type': 'scatter',
            'title': 'Correlation Scatter Plot',
            'domain': 'multiple domains',
            'data': {
                'x': [random.uniform(0, 100) for _ in range(20)],
                'y': [random.uniform(0, 100) for _ in range(20)]
            }
        })
    
    elif intent == 'comparison':
        # Add bar chart
        visualizations.append({
            'type': 'bar',
            'title': 'Domain Comparison',
            'domain': 'multiple domains',
            'data': {
                'labels': [d.replace('_', ' ').title() for d in domains],
                'values': [random.uniform(30, 80) for _ in domains]
            }
        })
    
    elif intent == 'anomaly':
        # Add anomaly chart
        visualizations.append({
            'type': 'line',
            'title': 'Anomaly Detection',
            'domain': domains[0] if domains else 'weather',
            'data': {
                'x': [f"2025-05-{i:02d}" for i in range(1, 13)],
                'y': [random.uniform(30, 70) for _ in range(12)],
                'anomalies': [3, 7, 10]  # Indices of anomalies
            }
        })
    
    return visualizations


def generate_data_objects(intent, domains):
    """Generate mock data objects based on intent and domains."""
    data_objects = []
    
    for domain in domains:
        if domain == 'weather':
            data_objects.append({
                'domain': 'weather',
                'temperature': round(random.uniform(50, 90), 1),
                'humidity': round(random.uniform(30, 80), 1),
                'precipitation': round(random.uniform(0, 2), 2),
                'wind_speed': round(random.uniform(0, 20), 1)
            })
        elif domain == 'transportation':
            data_objects.append({
                'domain': 'transportation',
                'congestion_level': round(random.uniform(0.1, 0.9), 2),
                'average_speed': round(random.uniform(15, 60), 1),
                'incident_count': random.randint(0, 10),
                'transit_ridership': random.randint(10000, 50000)
            })
        elif domain == 'economic':
            data_objects.append({
                'domain': 'economic',
                'market_index': round(random.uniform(3000, 5000), 2),
                'volatility': round(random.uniform(0.01, 0.05), 3),
                'interest_rate': round(random.uniform(0.01, 0.05), 3),
                'consumer_confidence': round(random.uniform(60, 120), 1)
            })
        elif domain == 'social_media':
            data_objects.append({
                'domain': 'social_media',
                'sentiment': round(random.uniform(-1, 1), 2),
                'engagement_rate': round(random.uniform(0.01, 0.1), 3),
                'trending_topics': random.randint(5, 15),
                'user_activity': random.randint(1000, 10000)
            })
        elif domain == 'health':
            data_objects.append({
                'domain': 'health',
                'case_count': random.randint(100, 1000),
                'hospital_occupancy': round(random.uniform(0.4, 0.9), 2),
                'air_quality_index': round(random.uniform(20, 150), 1),
                'vaccination_rate': round(random.uniform(0.5, 0.95), 2)
            })
    
    # Add some specialized data based on intent
    if intent == 'correlation':
        data_objects.append({
            'domain': 'correlation_analysis',
            'correlation_coefficient': round(random.uniform(0.6, 0.9), 2),
            'p_value': round(random.uniform(0.001, 0.05), 3),
            'sample_size': random.randint(100, 1000)
        })
    elif intent == 'prediction':
        data_objects.append({
            'domain': 'prediction_analysis',
            'model_accuracy': round(random.uniform(0.75, 0.95), 2),
            'confidence_interval': [
                round(random.uniform(20, 40), 1),
                round(random.uniform(60, 80), 1)
            ],
            'prediction_horizon': '7 days'
        })
    
    return data_objects


@nlq_blueprint.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get query suggestions based on available data."""
    try:
        # Get example queries organized by type
        suggestions = {
            "simple_queries": [
                "What's the current temperature?",
                "Show me today's traffic congestion",
                "What's the social media sentiment trend for the past week?",
                "What is the current hospital occupancy rate?",
                "How is the stock market performing today?"
            ],
            "correlation_queries": [
                "How does temperature affect traffic congestion?",
                "Is there a relationship between market volatility and social media sentiment?",
                "What factors correlate most strongly with travel time?",
                "Show the correlation between weather and public health metrics",
                "How does social media sentiment correlate with stock prices?"
            ],
            "prediction_queries": [
                "Predict tomorrow's traffic congestion based on weather forecast",
                "What will social media sentiment be if market volatility increases?",
                "Which model best predicts transportation patterns?",
                "Predict hospital admissions for next week",
                "What will the market do tomorrow based on current trends?"
            ],
            "analysis_queries": [
                "Compare weather patterns and traffic congestion over the last month",
                "Show the impact of weather on all other domains",
                "Identify anomalies in cross-domain correlations",
                "What unusual patterns exist in the health data?",
                "Show me a comparison of all domains for May 2025"
            ]
        }
        
        return jsonify(suggestions)
    
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return jsonify({'error': str(e)}), 500


@nlq_blueprint.route('/history', methods=['GET'])
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