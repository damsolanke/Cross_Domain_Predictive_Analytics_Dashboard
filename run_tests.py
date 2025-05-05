#!/usr/bin/env python
"""
Test runner for the natural language query functionality.
"""

import unittest
import sys
import argparse
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