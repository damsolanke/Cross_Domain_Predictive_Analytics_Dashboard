"""
Natural Language Query Processor Module
Author: Ademola Solanke
Date: May 2025

This module handles the processing of natural language queries and 
conversion to structured operations for the Cross-Domain Analytics Dashboard.
"""

import re
import logging
from datetime import datetime, timedelta
import numpy as np
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
from app.system_integration.cross_domain_prediction import CrossDomainPredictor

logger = logging.getLogger(__name__)

class NaturalLanguageProcessor:
    """
    Processes natural language queries and converts them to structured operations.
    """
    
    def __init__(self, correlator=None, predictor=None):
        """
        Initialize the natural language processor.
        
        Args:
            correlator: CrossDomainCorrelator instance
            predictor: CrossDomainPredictor instance
        """
        self.correlator = correlator or CrossDomainCorrelator()
        self.predictor = predictor or CrossDomainPredictor(correlator=self.correlator)
        
        # Define query intent patterns
        self.intent_examples = {
            "simple_data": [
                "What's the current temperature?",
                "Show me today's traffic congestion",
                "What's the social media sentiment for the past week?",
                "Display economic indicators for last month"
            ],
            "correlation": [
                "How does temperature affect traffic congestion?",
                "Is there a relationship between market volatility and social media sentiment?",
                "What factors correlate with travel time?",
                "Show correlations between weather and transportation"
            ],
            "prediction": [
                "Predict tomorrow's traffic congestion",
                "What will social media sentiment be if market volatility increases?",
                "Forecast economic indicators for next week",
                "Which model best predicts transportation patterns?"
            ],
            "comparison": [
                "Compare weather patterns and traffic congestion",
                "Show the impact of weather on all other domains",
                "How do economic factors compare to social media trends?",
                "Compare last week's data with this week"
            ],
            "anomaly": [
                "Identify anomalies in cross-domain correlations",
                "Find unusual patterns in the data",
                "Show me outliers in transportation metrics",
                "Are there any unexpected correlations?"
            ]
        }
        
        # Domain keywords
        self.domain_keywords = {
            "weather": ["weather", "temperature", "humidity", "wind", "precipitation", "rain", "snow"],
            "economic": ["economic", "market", "stock", "finance", "trading", "volatility", "interest"],
            "transportation": ["transportation", "traffic", "congestion", "travel", "commute", "speed", "vehicle"],
            "social_media": ["social", "media", "sentiment", "twitter", "facebook", "post", "engagement"]
        }
        
        # Time expressions
        self.time_patterns = {
            "today": timedelta(days=0),
            "yesterday": timedelta(days=1),
            "last week": timedelta(days=7),
            "last month": timedelta(days=30),
            "past week": timedelta(days=7),
            "past month": timedelta(days=30),
            "tomorrow": timedelta(days=-1),
            "next week": timedelta(days=-7),
            "next month": timedelta(days=-30)
        }
    
    def process_query(self, query_text):
        """
        Process a natural language query.
        
        Args:
            query_text (str): The query text.
            
        Returns:
            dict: The query results including visualizations and explanations.
        """
        try:
            # Parse the query
            parsed_query = self._parse_query(query_text)
            
            # Execute the query based on intent
            if parsed_query['intent'] == 'simple_data':
                results = self._handle_simple_data_query(parsed_query)
            elif parsed_query['intent'] == 'correlation':
                results = self._handle_correlation_query(parsed_query)
            elif parsed_query['intent'] == 'prediction':
                results = self._handle_prediction_query(parsed_query)
            elif parsed_query['intent'] == 'comparison':
                results = self._handle_comparison_query(parsed_query)
            elif parsed_query['intent'] == 'anomaly':
                results = self._handle_anomaly_query(parsed_query)
            else:
                results = {
                    'error': 'Query intent not recognized',
                    'suggestion': 'Try asking about current data, correlations, or predictions.'
                }
            
            # Add query metadata
            results['query'] = query_text
            results['parsed'] = parsed_query
            results['timestamp'] = datetime.now().isoformat()
            
            return results
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'error': 'Failed to process query',
                'details': str(e),
                'query': query_text,
                'timestamp': datetime.now().isoformat()
            }
    
    def _parse_query(self, query_text):
        """
        Parse the query to determine intent, domains, and time ranges.
        
        Args:
            query_text (str): The query text.
            
        Returns:
            dict: Parsed query information.
        """
        # Preprocess query text
        query_text = query_text.lower().strip()
        if not query_text.endswith('?'):
            query_text += '?'
        
        # Determine intent by simple keyword matching and pattern recognition
        intent_scores = {}
        for intent, examples in self.intent_examples.items():
            score = 0
            for example in examples:
                # Calculate simple word overlap
                example_words = set(example.lower().split())
                query_words = set(query_text.lower().split())
                overlap = len(example_words.intersection(query_words))
                score += overlap / max(len(example_words), len(query_words))
            
            intent_scores[intent] = score / len(examples)
        
        # Find the intent with the highest score
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        intent = best_intent[0]
        confidence = best_intent[1]
        
        # Determine domains mentioned
        domains = []
        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword in query_text:
                    domains.append(domain)
                    break
        
        # Determine time frame
        time_range = self._extract_time_range(query_text)
        
        # Determine specific variables through simple keyword extraction
        variables = self._extract_variables(query_text)
        
        return {
            'intent': intent,
            'confidence': float(confidence),
            'domains': list(set(domains)),
            'variables': variables,
            'time_range': time_range
        }
    
    def _extract_time_range(self, query_text):
        """Extract time range from query text."""
        start_date = None
        end_date = None
        
        # Check for specific time expressions
        for expression, delta in self.time_patterns.items():
            if expression in query_text:
                if delta.days >= 0:  # Past
                    end_date = datetime.now()
                    start_date = end_date - delta
                else:  # Future
                    start_date = datetime.now()
                    end_date = start_date - delta
                break
        
        # Default to last 24 hours if no time specified
        if not start_date:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1)
        
        return {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
    
    def _extract_variables(self, query_text):
        """Extract specific variables from the query text."""
        # This is a simplified version - would be enhanced with NLP libraries
        variables = []
        common_vars = [
            "temperature", "humidity", "precipitation", 
            "congestion", "traffic", "speed", 
            "sentiment", "posts", "engagement",
            "volatility", "price", "volume"
        ]
        
        for var in common_vars:
            if var in query_text:
                variables.append(var)
        
        return list(set(variables))
    
    def _handle_simple_data_query(self, parsed_query):
        """Handle queries for simple data retrieval."""
        # Implementation will depend on data access methods
        # This is a placeholder
        results = {
            'type': 'simple_data',
            'data': [],
            'visualizations': []
        }
        
        # Get data for each mentioned domain
        for domain in parsed_query['domains']:
            # This would be replaced with actual data access
            domain_data = self._get_domain_data(domain, parsed_query)
            
            if domain_data:
                results['data'].append({
                    'domain': domain,
                    'values': domain_data
                })
                
                # Generate visualization for this domain data
                viz = self._generate_visualization(domain, domain_data)
                if viz:
                    results['visualizations'].append(viz)
        
        # If no specific domains mentioned, get overview data
        if not parsed_query['domains']:
            overview_data = self._get_overview_data(parsed_query)
            results['data'].append({
                'domain': 'overview',
                'values': overview_data
            })
            
            viz = self._generate_visualization('overview', overview_data)
            if viz:
                results['visualizations'].append(viz)
        
        # Generate explanation
        results['explanation'] = self._generate_explanation_for_data(results['data'])
        
        return results
    
    def _handle_correlation_query(self, parsed_query):
        """Handle queries about correlations between domains."""
        results = {
            'type': 'correlation',
            'correlations': [],
            'visualizations': []
        }
        
        # If specific domains mentioned, get correlations between them
        if len(parsed_query['domains']) >= 2:
            domain_pair = sorted(parsed_query['domains'][:2])
            pair_key = f"{domain_pair[0]}_vs_{domain_pair[1]}"
            
            # Calculate correlations using the correlator
            self.correlator.calculate_correlations()
            correlation_data = self.correlator.get_correlation_data_for_visualization()
            
            # Find the specific correlation data for these domains
            for matrix in correlation_data.get('correlation_matrices', []):
                if matrix['domain_pair'] == pair_key:
                    results['correlations'].append(matrix)
            
            # Find heatmap data
            for heatmap in correlation_data.get('heatmap_data', []):
                if heatmap['domain_pair'] == pair_key:
                    results['visualizations'].append({
                        'type': 'heatmap',
                        'title': f"Correlation between {domain_pair[0]} and {domain_pair[1]}",
                        'data': heatmap['data']
                    })
        
        # If only one domain or none mentioned, get all correlations for that domain
        else:
            # Calculate correlations using the correlator
            self.correlator.calculate_correlations()
            correlation_data = self.correlator.get_correlation_data_for_visualization()
            
            # Include all correlation matrices
            results['correlations'] = correlation_data.get('correlation_matrices', [])
            
            # Include network visualization
            results['visualizations'].append({
                'type': 'network',
                'title': 'Cross-Domain Correlation Network',
                'data': correlation_data.get('network_data', {})
            })
        
        # Generate insights
        insights = self.correlator.generate_insights()
        
        # Filter insights if specific domains mentioned
        if parsed_query['domains']:
            filtered_insights = []
            for insight in insights:
                if insight.get('domain1') in parsed_query['domains'] or insight.get('domain2') in parsed_query['domains']:
                    filtered_insights.append(insight)
            insights = filtered_insights
        
        results['insights'] = insights
        
        # Generate explanation
        results['explanation'] = self._generate_explanation_for_correlation(results['correlations'], insights)
        
        return results
    
    def _handle_prediction_query(self, parsed_query):
        """Handle queries about predictions."""
        results = {
            'type': 'prediction',
            'predictions': [],
            'visualizations': []
        }
        
        # If specific domains mentioned, get predictions for them
        if parsed_query['domains']:
            for domain in parsed_query['domains']:
                # Use the predictor to make predictions
                domain_predictions = self.predictor.predict_domain(domain)
                
                if domain_predictions:
                    results['predictions'].append({
                        'domain': domain,
                        'values': domain_predictions
                    })
                    
                    # Generate visualization for predictions
                    viz = self._generate_visualization(domain, domain_predictions, 'prediction')
                    if viz:
                        results['visualizations'].append(viz)
        
        # If no specific domains mentioned, get predictions for all domains
        else:
            for domain in self.domain_keywords.keys():
                domain_predictions = self.predictor.predict_domain(domain)
                
                if domain_predictions:
                    results['predictions'].append({
                        'domain': domain,
                        'values': domain_predictions
                    })
                    
                    # Generate visualization for predictions
                    viz = self._generate_visualization(domain, domain_predictions, 'prediction')
                    if viz:
                        results['visualizations'].append(viz)
        
        # Generate explanation
        results['explanation'] = self._generate_explanation_for_prediction(results['predictions'])
        
        return results
    
    def _handle_comparison_query(self, parsed_query):
        """Handle queries comparing domains or time periods."""
        results = {
            'type': 'comparison',
            'comparisons': [],
            'visualizations': []
        }
        
        # If multiple domains mentioned, compare them
        if len(parsed_query['domains']) >= 2:
            domains = parsed_query['domains']
            
            # This is a placeholder - would be replaced with actual implementation
            comparison_data = self._get_comparison_data(domains, parsed_query)
            
            results['comparisons'].append({
                'domains': domains,
                'data': comparison_data
            })
            
            # Generate visualization
            viz = self._generate_comparison_visualization(domains, comparison_data)
            if viz:
                results['visualizations'].append(viz)
        
        # If time comparison is implied, compare current with past
        elif any(term in parsed_query['query'].lower() for term in ['compare', 'difference', 'changed']):
            domain = parsed_query['domains'][0] if parsed_query['domains'] else 'overview'
            
            # This is a placeholder - would be replaced with actual implementation
            comparison_data = self._get_time_comparison_data(domain, parsed_query)
            
            results['comparisons'].append({
                'domain': domain,
                'time_comparison': True,
                'data': comparison_data
            })
            
            # Generate visualization
            viz = self._generate_time_comparison_visualization(domain, comparison_data)
            if viz:
                results['visualizations'].append(viz)
        
        # Generate explanation
        results['explanation'] = self._generate_explanation_for_comparison(results['comparisons'])
        
        return results
    
    def _handle_anomaly_query(self, parsed_query):
        """Handle queries about anomalies."""
        results = {
            'type': 'anomaly',
            'anomalies': [],
            'visualizations': []
        }
        
        # Detect anomalies using the correlator
        anomalies = self.correlator.detect_anomalies()
        
        # Filter anomalies if specific domains mentioned
        if parsed_query['domains']:
            filtered_anomalies = []
            for anomaly in anomalies:
                if anomaly.get('domain1') in parsed_query['domains'] or anomaly.get('domain2') in parsed_query['domains']:
                    filtered_anomalies.append(anomaly)
            anomalies = filtered_anomalies
        
        results['anomalies'] = anomalies
        
        # Generate visualization for anomalies
        if anomalies:
            results['visualizations'].append({
                'type': 'anomaly',
                'title': 'Anomaly Detection',
                'data': anomalies
            })
        
        # Generate explanation
        results['explanation'] = self._generate_explanation_for_anomaly(anomalies)
        
        return results
    
    def _get_domain_data(self, domain, parsed_query):
        """Get data for a specific domain (placeholder method)."""
        # This would be replaced with actual data access logic
        # For now, return demo data
        if domain == 'weather':
            return [
                {'variable': 'temperature', 'value': 22.5, 'unit': 'C', 'timestamp': datetime.now().isoformat()},
                {'variable': 'humidity', 'value': 65, 'unit': '%', 'timestamp': datetime.now().isoformat()},
                {'variable': 'wind_speed', 'value': 15, 'unit': 'km/h', 'timestamp': datetime.now().isoformat()}
            ]
        elif domain == 'transportation':
            return [
                {'variable': 'congestion', 'value': 75, 'unit': '%', 'timestamp': datetime.now().isoformat()},
                {'variable': 'average_speed', 'value': 25, 'unit': 'km/h', 'timestamp': datetime.now().isoformat()},
                {'variable': 'incidents', 'value': 3, 'unit': 'count', 'timestamp': datetime.now().isoformat()}
            ]
        elif domain == 'economic':
            return [
                {'variable': 'market_index', 'value': 320.5, 'unit': 'points', 'timestamp': datetime.now().isoformat()},
                {'variable': 'volatility', 'value': 2.1, 'unit': '%', 'timestamp': datetime.now().isoformat()},
                {'variable': 'volume', 'value': 1250000, 'unit': 'trades', 'timestamp': datetime.now().isoformat()}
            ]
        elif domain == 'social_media':
            return [
                {'variable': 'sentiment', 'value': 0.65, 'unit': 'index', 'timestamp': datetime.now().isoformat()},
                {'variable': 'post_volume', 'value': 12500, 'unit': 'posts', 'timestamp': datetime.now().isoformat()},
                {'variable': 'engagement', 'value': 3.2, 'unit': '%', 'timestamp': datetime.now().isoformat()}
            ]
        else:
            return []
    
    def _get_overview_data(self, parsed_query):
        """Get overview data across domains (placeholder method)."""
        # This would be replaced with actual data access logic
        return [
            {'domain': 'weather', 'key_metric': 'temperature', 'value': 22.5, 'unit': 'C'},
            {'domain': 'transportation', 'key_metric': 'congestion', 'value': 75, 'unit': '%'},
            {'domain': 'economic', 'key_metric': 'market_index', 'value': 320.5, 'unit': 'points'},
            {'domain': 'social_media', 'key_metric': 'sentiment', 'value': 0.65, 'unit': 'index'}
        ]
    
    def _get_comparison_data(self, domains, parsed_query):
        """Get comparison data between domains (placeholder method)."""
        # This would be replaced with actual implementation
        return [
            {'metric': 'correlation_strength', 'value': 0.72},
            {'metric': 'common_patterns', 'value': 3},
            {'metric': 'divergence_points', 'value': 2}
        ]
    
    def _get_time_comparison_data(self, domain, parsed_query):
        """Get time comparison data (placeholder method)."""
        # This would be replaced with actual implementation
        return [
            {'variable': 'temperature', 'current': 22.5, 'previous': 20.1, 'change': 2.4, 'change_percent': 12},
            {'variable': 'humidity', 'current': 65, 'previous': 70, 'change': -5, 'change_percent': -7.1},
            {'variable': 'wind_speed', 'current': 15, 'previous': 12, 'change': 3, 'change_percent': 25}
        ]
    
    def _generate_visualization(self, domain, data, viz_type='data'):
        """Generate visualization for domain data (placeholder method)."""
        # This would be replaced with actual visualization generation
        return {
            'type': viz_type,
            'domain': domain,
            'title': f"{domain.capitalize()} {viz_type.capitalize()}"
        }
    
    def _generate_comparison_visualization(self, domains, data):
        """Generate comparison visualization (placeholder method)."""
        # This would be replaced with actual visualization generation
        return {
            'type': 'comparison',
            'domains': domains,
            'title': f"Comparison between {' and '.join(domains)}"
        }
    
    def _generate_time_comparison_visualization(self, domain, data):
        """Generate time comparison visualization (placeholder method)."""
        # This would be replaced with actual visualization generation
        return {
            'type': 'time_comparison',
            'domain': domain,
            'title': f"Time Comparison for {domain}"
        }
    
    def _generate_explanation_for_data(self, data):
        """Generate natural language explanation for data."""
        if not data:
            return "No data available for the specified criteria."
        
        explanations = []
        for item in data:
            domain = item['domain']
            explanations.append(f"Showing current data for {domain}.")
        
        return " ".join(explanations)
    
    def _generate_explanation_for_correlation(self, correlations, insights):
        """Generate natural language explanation for correlations."""
        if not correlations and not insights:
            return "No significant correlations found for the specified criteria."
        
        if insights:
            # Focus on the strongest insights
            strongest = sorted(insights, key=lambda x: abs(x.get('correlation_value', 0)), reverse=True)[:3]
            
            explanations = []
            for insight in strongest:
                direction = insight.get('direction', 'unknown')
                value = insight.get('correlation_value', 0)
                var1 = insight.get('variable1', '')
                var2 = insight.get('variable2', '')
                dom1 = insight.get('domain1', '')
                dom2 = insight.get('domain2', '')
                
                explanations.append(
                    f"Found a strong {direction} correlation ({value:.2f}) between "
                    f"{dom1}'s {var1} and {dom2}'s {var2}."
                )
            
            return " ".join(explanations)
        
        return "Correlation analysis completed, but no strong relationships were identified."
    
    def _generate_explanation_for_prediction(self, predictions):
        """Generate natural language explanation for predictions."""
        if not predictions:
            return "No predictions available for the specified criteria."
        
        explanations = []
        for prediction in predictions:
            domain = prediction['domain']
            explanations.append(f"Showing predictions for {domain}.")
        
        return " ".join(explanations)
    
    def _generate_explanation_for_comparison(self, comparisons):
        """Generate natural language explanation for comparisons."""
        if not comparisons:
            return "No comparison data available for the specified criteria."
        
        explanations = []
        for comparison in comparisons:
            if 'domains' in comparison:
                domains = comparison['domains']
                explanations.append(f"Comparing data between {' and '.join(domains)}.")
            elif 'time_comparison' in comparison:
                domain = comparison['domain']
                explanations.append(f"Comparing current and historical data for {domain}.")
        
        return " ".join(explanations)
    
    def _generate_explanation_for_anomaly(self, anomalies):
        """Generate natural language explanation for anomalies."""
        if not anomalies:
            return "No anomalies detected for the specified criteria."
        
        if len(anomalies) == 1:
            anomaly = anomalies[0]
            dom1 = anomaly.get('domain1', '')
            dom2 = anomaly.get('domain2', '')
            var1 = anomaly.get('variable1', '')
            var2 = anomaly.get('variable2', '')
            
            return f"Detected an anomaly in the relationship between {dom1}'s {var1} and {dom2}'s {var2}."
        
        return f"Detected {len(anomalies)} anomalies in cross-domain relationships."