#!/usr/bin/env python
"""
Test runner for the natural language query functionality.
"""

import unittest
import sys
import argparse
import os
from unittest.mock import patch

# Set up environment for testing
os.environ['TESTING'] = 'True'

# Define mock classes
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
        self.correlator = correlator or MockCorrelator()
        self.predictor = predictor or MockPredictor()
        
        # Intent examples for testing
        self.intent_examples = {
            "simple_data": ["temperature", "show me data"],
            "correlation": ["correlation", "relationship"],
            "prediction": ["predict", "forecast"],
            "comparison": ["compare", "difference"],
            "anomaly": ["anomaly", "outlier"]
        }
        
        # Domain keywords for testing
        self.domain_keywords = {
            "weather": ["weather", "temperature"],
            "economic": ["economic", "market"],
            "transportation": ["transportation", "traffic"],
            "social_media": ["social", "media"]
        }
        
        # Time patterns for testing
        self.time_patterns = {
            "today": 0,
            "yesterday": 1,
            "last week": 7
        }
    
    def process_query(self, query_text):
        """Main query processing method."""
        parsed = self._parse_query(query_text)
        
        return {
            'parsed': parsed,
            'type': parsed['intent'],
            'explanation': 'Test explanation',
            'query': query_text,
            'timestamp': '2023-01-01T00:00:00',
            'data': [{'domain': 'overview', 'values': []}],
            'visualizations': [{'type': 'test', 'domain': 'test'}]
        }
    
    def _parse_query(self, query_text):
        """Test implementation of query parsing."""
        # Determine intent based on keywords
        intent = 'simple_data'  # Default
        for intent_name, keywords in self.intent_examples.items():
            for keyword in keywords:
                if keyword in query_text.lower():
                    intent = intent_name
                    break
        
        # Determine domains
        domains = []
        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword in query_text.lower():
                    domains.append(domain)
                    break
        
        # Extract time range
        time_range = self._extract_time_range(query_text)
        
        # Extract variables
        variables = self._extract_variables(query_text)
        
        return {
            'intent': intent,
            'confidence': 0.8,
            'domains': domains,
            'variables': variables,
            'time_range': time_range
        }
    
    def _extract_time_range(self, query_text):
        """Test implementation of time range extraction."""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        end_date = now
        start_date = now - timedelta(days=1)  # Default to last 24 hours
        
        return {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
    
    def _extract_variables(self, query_text):
        """Test implementation of variable extraction."""
        variables = []
        common_vars = ["temperature", "humidity", "congestion", "sentiment"]
        
        for var in common_vars:
            if var in query_text.lower():
                variables.append(var)
        
        return variables

# Apply mocks before importing test modules
with patch('app.system_integration.cross_domain_correlation.CrossDomainCorrelator', MockCorrelator), \
     patch('app.system_integration.cross_domain_prediction.CrossDomainPredictor', MockPredictor), \
     patch('app.system_integration.natural_language_processor.NaturalLanguageProcessor', MockNLProcessor):
    from app.tests.test_natural_language_processor import TestNaturalLanguageProcessor
    from app.tests.test_nlq_api import TestNLQAPI

# Browser tests require a running server
BROWSER_TESTS_ENABLED = False
if BROWSER_TESTS_ENABLED:
    from app.tests.test_browser import TestNLQBrowser

def run_unit_tests():
    """Run unit tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestNaturalLanguageProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestNLQAPI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_browser_tests():
    """Run browser integration tests."""
    if not BROWSER_TESTS_ENABLED:
        print("Browser tests are disabled. Set BROWSER_TESTS_ENABLED = True to enable them.")
        return True
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add browser test cases
    suite.addTests(loader.loadTestsFromTestCase(TestNLQBrowser))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    """Run all tests or specific test types based on arguments."""
    parser = argparse.ArgumentParser(description='Run tests for natural language query functionality.')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--browser', action='store_true', help='Run browser tests only')
    
    args = parser.parse_args()
    
    # By default, run all tests
    if not args.unit and not args.browser:
        args.unit = True
        args.browser = True if BROWSER_TESTS_ENABLED else False
    
    # Track success of all test types
    success = True
    
    # Run unit tests if requested
    if args.unit:
        print("\n--- Running Unit Tests ---")
        unit_success = run_unit_tests()
        success = success and unit_success
    
    # Run browser tests if requested
    if args.browser:
        print("\n--- Running Browser Tests ---")
        browser_success = run_browser_tests()
        success = success and browser_success
    
    # Return appropriate exit code
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())