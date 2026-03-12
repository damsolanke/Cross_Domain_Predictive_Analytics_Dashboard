"""
Tests for the cross-domain correlation utilities.
"""
import unittest
import numpy as np
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator

class TestCrossDomainCorrelation(unittest.TestCase):
    """Tests for the CrossDomainCorrelator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.correlator = CrossDomainCorrelator()
        self.generate_test_data()

    def generate_test_data(self):
        """Generate test data for domains with known correlations."""
        np.random.seed(42)

        # Base temperature data (sinusoidal pattern)
        base_temperature = np.sin(np.linspace(0, 2 * np.pi, 24)) * 10 + 20

        # Traffic congestion: positively correlated with temperature
        base_congestion = base_temperature / 40

        # Social media sentiment: negatively correlated with congestion
        base_sentiment = -base_congestion + np.random.normal(0, 0.1, 24)

        # Economic activity: weakly correlated with temperature
        base_economic = base_temperature * 0.3 + np.random.normal(0, 5, 24)

        # Build domain data as lists of dicts (what add_domain_data expects)
        weather_data = [
            {"temperature": float(base_temperature[i]), "humidity": float(np.random.uniform(50, 90))}
            for i in range(24)
        ]
        transport_data = [
            {"congestion": float(base_congestion[i]), "avg_speed": float((1 - base_congestion[i]) * 60)}
            for i in range(24)
        ]
        social_data = [
            {"sentiment": float(base_sentiment[i]), "post_volume": int(np.random.uniform(500, 1500))}
            for i in range(24)
        ]
        economic_data = [
            {"index_value": float(base_economic[i]), "volatility": float(np.random.uniform(0.01, 0.05))}
            for i in range(24)
        ]

        self.correlator.add_domain_data("weather", weather_data)
        self.correlator.add_domain_data("transportation", transport_data)
        self.correlator.add_domain_data("social_media", social_data)
        self.correlator.add_domain_data("economic", economic_data)

    def test_correlation_calculation(self):
        """Test that correlations are calculated correctly."""
        # Temperature and congestion are positively correlated by construction
        corr = self.correlator.compute_correlation("weather", "temperature", "transportation", "congestion")
        self.assertIsNotNone(corr)
        self.assertGreater(corr, 0.9, f"Expected strong positive correlation, got {corr}")

    def test_get_all_correlations(self):
        """Test computing all pairwise correlations."""
        all_corr = self.correlator.get_all_correlations()
        self.assertIsInstance(all_corr, dict)
        self.assertGreater(len(all_corr), 0)

    def test_highest_correlations(self):
        """Test getting highest correlations."""
        top = self.correlator.get_highest_correlations(limit=3)
        self.assertIsInstance(top, list)
        self.assertLessEqual(len(top), 3)

        if top:
            entry = top[0]
            self.assertIn('correlation', entry)
            self.assertIn('domain1', entry)
            self.assertIn('domain2', entry)
            self.assertIn('strength', entry)

    def test_status(self):
        """Test correlator status reporting."""
        status = self.correlator.get_status()
        self.assertIn('domains', status)
        self.assertEqual(len(status['domains']), 4)
        self.assertIsNone(status['error'])

    def test_missing_domain(self):
        """Test behavior when domain is not found."""
        result = self.correlator.compute_correlation("missing", "field", "weather", "temperature")
        self.assertIsNone(result)
        self.assertIsNotNone(self.correlator.error)

if __name__ == '__main__':
    unittest.main()
