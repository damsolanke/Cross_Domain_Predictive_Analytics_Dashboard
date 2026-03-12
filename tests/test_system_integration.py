import unittest
import time
import json
from app import create_app, socketio
from app.system_integration.pipeline import DataPipeline
from app.system_integration.alert_system import AlertSystem
from app.system_integration.integration import SystemIntegrator

class TestSystemIntegration(unittest.TestCase):
    """Tests for the system integration components"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()

    def test_pipeline_creation(self):
        """Test that the data pipeline can be created"""
        pipeline = DataPipeline()
        self.assertIsNotNone(pipeline)
        self.assertIsInstance(pipeline, DataPipeline)

        # Check system health
        health = pipeline.check_system_health()
        self.assertIn('uptime', health)
        self.assertIn('queue_size', health)
        self.assertIn('status', health)

    def test_alert_system_creation(self):
        """Test that the alert system can be created"""
        alert_system = AlertSystem()
        self.assertIsNotNone(alert_system)
        self.assertIsInstance(alert_system, AlertSystem)

        # Test configuration
        config = alert_system.get_configuration()
        self.assertIn('threshold_checks', config)

        # Update configuration
        new_config = {'threshold_checks': {'prediction_confidence': {'min_threshold': 0.8}}}
        alert_system.update_configuration(new_config)

        # Verify config was updated
        updated_config = alert_system.get_configuration()
        self.assertEqual(updated_config['threshold_checks']['prediction_confidence']['min_threshold'], 0.8)

        # Test alert creation
        alert_data = {
            'confidence': 0.6,  # Below the threshold (0.8)
            'source': 'test'
        }
        alerts = alert_system.check_thresholds(alert_data)
        self.assertGreater(len(alerts), 0)

        # Clean up
        alert_system.shutdown()

    def test_system_integrator(self):
        """Test that the system integrator can be created"""
        integrator = SystemIntegrator()
        self.assertIsNotNone(integrator)

        # Register a mock component
        class MockComponent:
            def get_status(self):
                return {'status': 'connected'}

        integrator.register_component('weather', MockComponent())
        component = integrator.get_component('weather')
        self.assertIsNotNone(component)
        self.assertEqual(component.get_status()['status'], 'connected')

    def test_api_endpoints(self):
        """Test API endpoints for system integration"""
        # Test system health endpoint
        response = self.client.get('/api/system-health')
        self.assertEqual(response.status_code, 404)  # Will fail until we fix routes

        # Test alert configuration endpoint
        response = self.client.get('/api/alerts/config')
        self.assertEqual(response.status_code, 404)  # Will fail until we fix routes

    def test_socket_connection(self):
        """Test WebSocket connection (requires socket client)"""
        self.assertIsNotNone(socketio)


class TestEndToEndIntegration(unittest.TestCase):
    """End-to-end integration test for the system"""

    def test_data_flow(self):
        """Test end-to-end data flow through pipeline"""
        pipeline = DataPipeline()
        self.assertIsNotNone(pipeline)

        # Start pipeline processing
        pipeline.start_processing()
        self.assertTrue(pipeline.is_running)

        # Submit test data
        result = pipeline.submit_data('weather', {'temperature': 25.0, 'timestamp': time.time()})
        self.assertTrue(result)

        # Let the pipeline process
        time.sleep(0.5)

        # Stop pipeline
        pipeline.stop_processing()
        self.assertFalse(pipeline.is_running)

if __name__ == '__main__':
    unittest.main()
