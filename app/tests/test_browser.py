"""
Browser integration tests for the NLQ functionality.

These tests require a running server and will be run with Selenium.
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class TestNLQBrowser(unittest.TestCase):
    """Browser integration tests for Natural Language Query functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up the browser before any tests."""
        # This would be updated with proper webdriver setup based on environment
        # For local testing, use:
        # cls.driver = webdriver.Chrome()  # or Firefox, etc.
        
        # For CI environment, might use headless mode:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=options)
        
        # Set implicit wait time
        cls.driver.implicitly_wait(10)
        
        # Set base URL (would be updated based on deployment)
        cls.base_url = "http://localhost:5000"

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests have run."""
        cls.driver.quit()

    def setUp(self):
        """Set up before each test."""
        self.driver.get(f"{self.base_url}/nlq")
        time.sleep(1)  # Give the page time to fully load

    def test_nlq_page_loads(self):
        """Test that the NLQ page loads correctly."""
        # Check title
        self.assertIn("Natural Language Queries", self.driver.title)
        
        # Check input box is present
        input_box = self.driver.find_element(By.ID, "nlq-input")
        self.assertTrue(input_box.is_displayed())
        
        # Check suggestion pills load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "suggestion-pill"))
        )
        suggestions = self.driver.find_elements(By.CLASS_NAME, "suggestion-pill")
        self.assertGreater(len(suggestions), 0)

    def test_simple_query(self):
        """Test submitting a simple query."""
        # Find the input box
        input_box = self.driver.find_element(By.ID, "nlq-input")
        
        # Type a query
        input_box.send_keys("What's the current temperature?")
        
        # Submit the query
        input_box.send_keys(Keys.RETURN)
        
        # Wait for results to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nlq-results"))
        )
        
        # Check that we have results
        results_element = self.driver.find_element(By.ID, "nlq-results")
        self.assertTrue(results_element.is_displayed())
        
        # Check the results title
        title_element = self.driver.find_element(By.ID, "nlq-results-title")
        self.assertEqual("Data Results", title_element.text)
        
        # Check explanation is present
        explanation = self.driver.find_element(By.ID, "nlq-explanation")
        self.assertNotEqual("", explanation.text)

    def test_suggestion_pills(self):
        """Test that clicking on suggestion pills works."""
        # Wait for pills to be loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "suggestion-pill"))
        )
        
        # Click on the first suggestion pill
        suggestions = self.driver.find_elements(By.CLASS_NAME, "suggestion-pill")
        first_suggestion_text = suggestions[0].text
        suggestions[0].click()
        
        # Wait for results to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nlq-results"))
        )
        
        # Check input box has suggestion text
        input_box = self.driver.find_element(By.ID, "nlq-input")
        self.assertEqual(first_suggestion_text, input_box.get_attribute("value"))

    def test_query_error_handling(self):
        """Test handling of empty queries."""
        # Find the input box
        input_box = self.driver.find_element(By.ID, "nlq-input")
        submit_button = self.driver.find_element(By.ID, "nlq-submit")
        
        # Submit an empty query
        input_box.send_keys("")
        submit_button.click()
        
        # Nothing should happen (no results should appear)
        time.sleep(1)  # Wait a bit
        results_elements = self.driver.find_elements(By.ID, "nlq-results")
        if results_elements:
            self.assertFalse(results_elements[0].is_displayed())

    def test_dashboard_integration(self):
        """Test NLQ integration on the main dashboard."""
        # Navigate to dashboard
        self.driver.get(f"{self.base_url}/dashboard")
        time.sleep(1)  # Give the page time to fully load
        
        # Find NLQ input
        input_box = self.driver.find_element(By.ID, "nlq-input")
        self.assertTrue(input_box.is_displayed())
        
        # Submit a query
        input_box.send_keys("Show correlation between weather and transportation")
        input_box.send_keys(Keys.RETURN)
        
        # Wait for results to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nlq-results"))
        )
        
        # Check that results row is visible
        results_row = self.driver.find_element(By.ID, "nlq-results-row")
        self.assertTrue(results_row.is_displayed())
        
        # Check results content
        title_element = self.driver.find_element(By.ID, "nlq-results-title")
        self.assertEqual("Correlation Analysis", title_element.text)


if __name__ == "__main__":
    unittest.main()