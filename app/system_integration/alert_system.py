import time
import json
from datetime import datetime
import threading
import uuid

class AlertSystem:
    """
    Alert system for monitoring predictions and notifying users when thresholds are crossed.
    Allows for custom alert configurations and integrates with the real-time updates system.
    """
    
    def __init__(self):
        """Initialize the alert system with default configurations"""
        self.alert_configurations = {}
        self.active_alerts = []
        self.alert_history = []
        
        # Default configuration
        self.default_config = {
            'threshold_checks': {
                'prediction_confidence': {
                    'min_threshold': 0.7,
                    'alert_level': 'warning'
                },
                'anomaly_score': {
                    'max_threshold': 0.8,
                    'alert_level': 'critical'
                },
                'data_staleness': {
                    'max_age_minutes': 30,
                    'alert_level': 'warning'
                }
            },
            'notification_channels': ['web', 'email'],
            'check_frequency_seconds': 60,
            'alert_grouping': True,
            'auto_resolve': True,
            'max_active_alerts': 100
        }
        
        # Load configuration
        self._load_configuration()
        
        # Start alert checking thread
        self.alert_check_active = True
        self.alert_thread = threading.Thread(target=self._alert_check_loop)
        self.alert_thread.daemon = True
        self.alert_thread.start()
    
    def _load_configuration(self):
        """Load alert configuration from storage or use defaults"""
        try:
            # This would normally load from a database or file
            # For now, just use the default configuration
            self.alert_configurations = {
                'default': self.default_config
            }
        except Exception as e:
            print(f"Error loading alert configuration: {e}")
            # Fall back to default config
            self.alert_configurations = {
                'default': self.default_config
            }
    
    def update_configuration(self, config_updates, config_id='default'):
        """Update the alert configuration"""
        if config_id in self.alert_configurations:
            # Update existing configuration
            current_config = self.alert_configurations[config_id]
            
            # Deep update the configuration
            self._deep_update(current_config, config_updates)
        else:
            # Create new configuration
            self.alert_configurations[config_id] = config_updates
        
        # Save the updated configuration
        self._save_configuration()
        
        return True
    
    def _deep_update(self, target, source):
        """Deep update a nested dictionary with another dictionary"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def _save_configuration(self):
        """Save the current configuration to storage"""
        # This would normally save to a database or file
        # For now, just print a message
        print(f"Alert configuration updated: {len(self.alert_configurations)} configurations")
    
    def check_thresholds(self, data_item, config_id='default'):
        """
        Check if a data item exceeds any configured thresholds.
        Returns a list of triggered alerts or an empty list.
        """
        if config_id not in self.alert_configurations:
            config_id = 'default'
            
        config = self.alert_configurations[config_id]
        triggered_alerts = []
        
        # Check various thresholds depending on data type
        for check_name, check_config in config['threshold_checks'].items():
            if check_name == 'prediction_confidence' and 'confidence' in data_item:
                confidence = data_item['confidence']
                min_threshold = check_config.get('min_threshold', 0.7)
                
                if confidence < min_threshold:
                    triggered_alerts.append({
                        'id': str(uuid.uuid4()),
                        'type': 'prediction_confidence',
                        'level': check_config.get('alert_level', 'warning'),
                        'message': f"Prediction confidence ({confidence:.2f}) below threshold ({min_threshold:.2f})",
                        'timestamp': datetime.now().isoformat(),
                        'data': {
                            'confidence': confidence,
                            'threshold': min_threshold,
                            'data_source': data_item.get('source', 'unknown')
                        }
                    })
            
            elif check_name == 'anomaly_score' and 'anomaly_score' in data_item:
                score = data_item['anomaly_score']
                max_threshold = check_config.get('max_threshold', 0.8)
                
                if score > max_threshold:
                    triggered_alerts.append({
                        'id': str(uuid.uuid4()),
                        'type': 'anomaly_score',
                        'level': check_config.get('alert_level', 'critical'),
                        'message': f"Anomaly score ({score:.2f}) above threshold ({max_threshold:.2f})",
                        'timestamp': datetime.now().isoformat(),
                        'data': {
                            'score': score,
                            'threshold': max_threshold,
                            'data_source': data_item.get('source', 'unknown')
                        }
                    })
        
        return triggered_alerts
    
    def _alert_check_loop(self):
        """Background thread that checks for alert conditions periodically"""
        while self.alert_check_active:
            try:
                # This would normally query the data pipeline for recent data
                # and check each item against thresholds
                # For demonstration, we'll add a simulated alert occasionally
                
                if len(self.active_alerts) < self.default_config['max_active_alerts'] and \
                   time.time() % 47 < 1:  # Just a way to occasionally trigger an alert
                    simulated_alert = {
                        'id': str(uuid.uuid4()),
                        'type': 'simulated',
                        'level': 'info',
                        'message': "Simulated periodic alert for demonstration",
                        'timestamp': datetime.now().isoformat(),
                        'data': {
                            'simulation': True
                        }
                    }
                    self.add_alert(simulated_alert)
                
                # Handle auto-resolution of alerts
                if self.default_config['auto_resolve']:
                    self._auto_resolve_alerts()
                
                # Sleep until next check
                check_frequency = self.default_config.get('check_frequency_seconds', 60)
                time.sleep(check_frequency)
                
            except Exception as e:
                print(f"Error in alert check loop: {e}")
                time.sleep(10)  # Sleep on error to avoid tight loop
    
    def _auto_resolve_alerts(self):
        """Automatically resolve alerts that have been active for too long"""
        current_time = time.time()
        resolved_alerts = []
        
        for alert in self.active_alerts:
            try:
                # Parse the alert timestamp
                alert_time = datetime.fromisoformat(alert['timestamp'])
                alert_age_seconds = (datetime.now() - alert_time).total_seconds()
                
                # Auto-resolve alerts older than 1 hour
                if alert_age_seconds > 3600:  # 1 hour in seconds
                    alert['resolved'] = True
                    alert['resolution_time'] = datetime.now().isoformat()
                    alert['resolution_reason'] = 'auto'
                    
                    # Move to history
                    self.alert_history.append(alert)
                    resolved_alerts.append(alert['id'])
            except Exception as e:
                print(f"Error auto-resolving alert {alert.get('id')}: {e}")
        
        # Remove resolved alerts from active list
        self.active_alerts = [a for a in self.active_alerts if a['id'] not in resolved_alerts]
    
    def add_alert(self, alert):
        """Add a new alert to the active alerts list"""
        # Add to active alerts
        self.active_alerts.append(alert)
        
        # Trim active alerts if necessary
        max_alerts = self.default_config.get('max_active_alerts', 100)
        if len(self.active_alerts) > max_alerts:
            # Move oldest alerts to history
            excess = len(self.active_alerts) - max_alerts
            for i in range(excess):
                oldest = self.active_alerts.pop(0)
                oldest['resolved'] = True
                oldest['resolution_reason'] = 'overflow'
                self.alert_history.append(oldest)
        
        # Emit alert via Flask-SocketIO
        # This would normally call the emit_alert function in routes.py
        # For now, just print the alert
        print(f"New alert: {alert['message']} ({alert['level']})")
        
        return alert['id']
    
    def resolve_alert(self, alert_id, resolution_note=None):
        """Resolve an active alert"""
        for alert in self.active_alerts:
            if alert['id'] == alert_id:
                alert['resolved'] = True
                alert['resolution_time'] = datetime.now().isoformat()
                alert['resolution_reason'] = 'manual'
                if resolution_note:
                    alert['resolution_note'] = resolution_note
                
                # Move to history
                self.alert_history.append(alert)
                self.active_alerts.remove(alert)
                return True
        
        return False
    
    def get_current_alerts(self, alert_level=None):
        """Get all current active alerts, optionally filtered by level"""
        if alert_level:
            return [a for a in self.active_alerts if a.get('level') == alert_level]
        return self.active_alerts
    
    def get_alert_history(self, limit=100, offset=0):
        """Get alert history with pagination"""
        return self.alert_history[offset:offset+limit]
    
    def get_configuration(self, config_id='default'):
        """Get the current alert configuration"""
        return self.alert_configurations.get(config_id, self.default_config)
    
    def shutdown(self):
        """Clean shutdown of the alert system"""
        self.alert_check_active = False
        if self.alert_thread.is_alive():
            self.alert_thread.join(timeout=5.0)