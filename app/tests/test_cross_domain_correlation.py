"""
Tests for the cross-domain correlation utilities.
"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator

class TestCrossDomainCorrelation(unittest.TestCase):
    """Tests for the CrossDomainCorrelator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.correlator = CrossDomainCorrelator()
        # Generate test data
        self.generate_test_data()
        
    def generate_test_data(self):
        """Generate test data for domains with known correlations."""
        # Generate timestamps for the last 24 hours
        now = datetime.now()
        timestamps = [(now - timedelta(hours=i)).isoformat() for i in range(24)]
        timestamps.reverse()  # Now in chronological order
        
        # Base temperature data (increases during the day)
        base_temperature = np.sin(np.linspace(0, 2*np.pi, 24)) * 10 + 20
        
        # Traffic congestion data (correlated with temperature)
        # Higher temperature -> more congestion (positive correlation)
        base_congestion = base_temperature / 40  # Scale to 0-1
        
        # Social media sentiment (negatively correlated with congestion)
        # More congestion -> negative sentiment
        base_sentiment = -base_congestion + np.random.normal(0, 0.1, 24)
        
        # Economic activity (weakly correlated with temperature)
        base_economic = base_temperature * 0.3 + np.random.normal(0, 5, 24)
        
        # Add some noise to all data
        temperature = base_temperature + np.random.normal(0, 1, 24)
        congestion = np.clip(base_congestion + np.random.normal(0, 0.05, 24), 0, 1)
        sentiment = np.clip(base_sentiment + np.random.normal(0, 0.1, 24), -1, 1)
        economic = base_economic + np.random.normal(0, 2, 24)
        
        # Create data for each domain
        for i in range(24):
            # Weather data
            self.correlator.add_data("weather", {
                "timestamp": timestamps[i],
                "temperature": temperature[i],
                "humidity": np.random.uniform(50, 90),
                "wind_speed": np.random.uniform(0, 15)
            })
            
            # Transportation data
            self.correlator.add_data("transportation", {
                "timestamp": timestamps[i],
                "congestion": congestion[i],
                "avg_speed": (1 - congestion[i]) * 60 + np.random.uniform(0, 10),
                "vehicle_count": int(congestion[i] * 1000 + np.random.uniform(0, 100))
            })
            
            # Social media data
            self.correlator.add_data("social_media", {
                "timestamp": timestamps[i],
                "sentiment": sentiment[i],
                "post_volume": int(np.random.uniform(500, 1500)),
                "engagement_rate": np.random.uniform(0.01, 0.1)
            })
            
            # Economic data
            self.correlator.add_data("economic", {
                "timestamp": timestamps[i],
                "index_value": economic[i],
                "volatility": np.random.uniform(0.01, 0.05),
                "transaction_volume": int(np.random.uniform(10000, 50000))
            })
    
    def test_correlation_calculation(self):
        """Test that correlations are calculated correctly."""
        # Calculate correlations
        correlations = self.correlator.calculate_correlations()
        
        # Verify correlation structure
        self.assertIsInstance(correlations, dict)
        self.assertTrue(len(correlations) > 0)
        
        # Check for expected domain pairs in correlations
        expected_pairs = [
            "weather_vs_transportation",
            "weather_vs_social_media",
            "weather_vs_economic",
            "transportation_vs_social_media",
            "transportation_vs_economic",
            "social_media_vs_economic"
        ]
        
        for pair in expected_pairs:
            self.assertIn(pair, correlations, f"Expected correlation pair {pair} not found")
            
        # Verify a specific correlation: temperature and congestion should be positively correlated
        weather_vs_transport = correlations.get("weather_vs_transportation", {})
        if "temperature" in weather_vs_transport and "congestion" in weather_vs_transport["temperature"]:
            temp_congestion_corr = weather_vs_transport["temperature"]["congestion"]
            self.assertGreater(temp_congestion_corr, 0.4, 
                              f"Expected positive correlation between temperature and congestion, got {temp_congestion_corr}")
    
    def test_insight_generation(self):
        """Test that insights are generated from correlations."""
        # Calculate correlations and generate insights
        self.correlator.calculate_correlations()
        insights = self.correlator.generate_insights()
        
        # Verify insights
        self.assertIsInstance(insights, list)
        
        # There should be some insights given our test data
        self.assertTrue(len(insights) > 0, "No insights were generated")
        
        # Verify structure of an insight
        if insights:
            insight = insights[0]
            required_fields = ["type", "domain1", "domain2", "variable1", "variable2", 
                              "correlation_value", "direction", "description", "timestamp"]
            for field in required_fields:
                self.assertIn(field, insight, f"Required field {field} missing from insight")
    
    def test_anomaly_detection(self):
        """Test anomaly detection."""
        anomalies = self.correlator.detect_anomalies()
        self.assertIsInstance(anomalies, list)
        
        # With our test data, we may or may not have anomalies
        # Just check the structure if there are any
        if anomalies:
            anomaly = anomalies[0]
            required_fields = ["type", "domain1", "domain2", "variable1", "variable2", 
                              "correlation_value", "description", "timestamp"]
            for field in required_fields:
                self.assertIn(field, anomaly, f"Required field {field} missing from anomaly")
    
    def test_visualization_data(self):
        """Test data formatting for visualization."""
        # Calculate correlations
        self.correlator.calculate_correlations()
        viz_data = self.correlator.get_correlation_data_for_visualization()
        
        # Verify visualization data
        self.assertIsInstance(viz_data, dict)
        required_sections = ["correlation_matrices", "heatmap_data", "network_data", "insights"]
        for section in required_sections:
            self.assertIn(section, viz_data, f"Required section {section} missing from visualization data")
        
        # Check network data
        network_data = viz_data["network_data"]
        self.assertIn("nodes", network_data)
        self.assertIn("links", network_data)
        self.assertTrue(len(network_data["nodes"]) > 0, "No nodes in network data")
    
    def test_time_window_setting(self):
        """Test setting the time window for correlation analysis."""
        # Initial time window is 24 hours
        self.assertEqual(self.correlator.time_window, timedelta(hours=24))
        
        # Set to 12 hours
        self.correlator.set_time_window(hours=12)
        self.assertEqual(self.correlator.time_window, timedelta(hours=12))
        
        # Set back to 24 hours
        self.correlator.set_time_window(hours=24)
        self.assertEqual(self.correlator.time_window, timedelta(hours=24))

if __name__ == '__main__':
    unittest.main()