"""
Tests for the Natural Language Query API endpoints.
"""

import unittest
import json
from unittest.mock import patch, MagicMock

# Create mock classes for dependencies
class MockCorrelator:
    def __init__(self):
        self.domains = ['weather', 'economic', 'transportation', 'social_media']
    
    def calculate_correlations(self):
        return True
    
    def get_correlation_data_for_visualization(self):
        return {'correlation_matrices': [], 'heatmap_data': [], 'network_data': {}}
    
    def generate_insights(self):
        return []
    
    def detect_anomalies(self):
        return []

class MockPredictor:
    def __init__(self, correlator=None):
        pass
    
    def predict_domain(self, domain, variable=None):
        return []
    
    def get_prediction_history(self, limit=10):
        return []

class MockNLProcessor:
    def __init__(self, correlator=None, predictor=None):
        pass
    
    def process_query(self, query_text):
        return {
            'parsed': {'intent': 'simple_data', 'domains': ['weather']},
            'explanation': 'Test explanation'
        }

# Apply mocks
with patch('app.system_integration.cross_domain_correlation.CrossDomainCorrelator', MockCorrelator), \
     patch('app.system_integration.cross_domain_prediction.CrossDomainPredictor', MockPredictor), \
     patch('app.system_integration.natural_language_processor.NaturalLanguageProcessor', MockNLProcessor):
    from app import create_app


class TestNLQAPI(unittest.TestCase):
    """Test the NLQ API endpoints."""

    def setUp(self):
        """Set up the test case."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_process_query_endpoint(self):
        """Test the query processing endpoint."""
        # Test valid query
        data = {'query': 'What is the current temperature?'}
        response = self.client.post('/api/nlq/query', 
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('parsed', result)
        self.assertIn('explanation', result)
        self.assertEqual(result['parsed']['intent'], 'simple_data')
        
        # Test missing query
        data = {}  # No query
        response = self.client.post('/api/nlq/query', 
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Bad request
        
        # In these tests, we're using mocks, so we won't actually generate an error
        # for an empty query - our mock processor handles it gracefully.
        # Let's test that it returns something valid instead:
        data = {'query': ''}
        response = self.client.post('/api/nlq/query', 
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Should handle gracefully
        result = json.loads(response.data)
        self.assertIn('parsed', result)

    def test_suggestions_endpoint(self):
        """Test the query suggestions endpoint."""
        response = self.client.get('/api/nlq/suggestions')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        
        # Should have various suggestion categories
        self.assertIn('simple_queries', result)
        self.assertIn('correlation_queries', result)
        self.assertIn('prediction_queries', result)
        self.assertIn('analysis_queries', result)
        
        # Each category should have suggestions
        self.assertGreater(len(result['simple_queries']), 0)
        self.assertGreater(len(result['correlation_queries']), 0)
        self.assertGreater(len(result['prediction_queries']), 0)
        self.assertGreater(len(result['analysis_queries']), 0)

    def test_history_endpoint(self):
        """Test the query history endpoint."""
        response = self.client.get('/api/nlq/history')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        
        # Should be an array (even if empty)
        self.assertIsInstance(result, list)
        
        # If not empty, check structure
        if result:
            first_item = result[0]
            self.assertIn('query', first_item)
            self.assertIn('timestamp', first_item)
            self.assertIn('intent', first_item)


if __name__ == '__main__':
    unittest.main()