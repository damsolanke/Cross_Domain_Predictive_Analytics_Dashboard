"""
Demo data generator for cross-domain correlations.
"""

import numpy as np
from datetime import datetime, timedelta
import random
import time

class CrossDomainGenerator:
    """
    Generates demo data across multiple domains with configurable correlation patterns.
    This is useful for demonstrating and testing cross-domain correlation analysis.
    """
    
    def __init__(self, seed=None):
        """
        Initialize the cross-domain generator.
        
        Args:
            seed (int, optional): Random seed for reproducible generation.
        """
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        # Base signal parameters
        self.base_signals = {
            'daily_cycle': {
                'period': 24,  # Hours
                'amplitude': 1.0,
                'phase': 0
            },
            'weekly_cycle': {
                'period': 168,  # Hours (7 days)
                'amplitude': 0.5,
                'phase': 0
            },
            'trend': {
                'slope': 0.01,
                'baseline': 0
            },
            'noise': {
                'level': 0.1
            }
        }
        
        # Domain-specific parameters
        self.domain_params = {
            'weather': {
                'temperature': {
                    'daily_cycle': 0.8,
                    'weekly_cycle': 0.2,
                    'trend': 0.1,
                    'noise': 0.2,
                    'baseline': 20,
                    'scale': 15
                },
                'humidity': {
                    'daily_cycle': -0.5,  # Negatively correlated with temperature
                    'weekly_cycle': 0.2,
                    'trend': 0.0,
                    'noise': 0.3,
                    'baseline': 50,
                    'scale': 30
                },
                'wind_speed': {
                    'daily_cycle': 0.4,
                    'weekly_cycle': 0.3,
                    'trend': 0.0,
                    'noise': 0.5,
                    'baseline': 8,
                    'scale': 8
                }
            },
            'transportation': {
                'congestion': {
                    'daily_cycle': 0.7,  # Similar to temperature
                    'weekly_cycle': 0.6,  # Stronger weekly pattern
                    'trend': 0.05,
                    'noise': 0.15,
                    'baseline': 0.5,
                    'scale': 0.5
                },
                'avg_speed': {
                    'daily_cycle': -0.7,  # Inverse of congestion
                    'weekly_cycle': -0.6,
                    'trend': -0.05,
                    'noise': 0.15,
                    'baseline': 40,
                    'scale': 20
                },
                'vehicle_count': {
                    'daily_cycle': 0.8,
                    'weekly_cycle': 0.7,
                    'trend': 0.1,
                    'noise': 0.2,
                    'baseline': 500,
                    'scale': 500
                }
            },
            'economic': {
                'market_index': {
                    'daily_cycle': 0.3,  # Weaker daily cycle
                    'weekly_cycle': 0.5,
                    'trend': 0.2,  # Stronger upward trend
                    'noise': 0.4,  # More noise (volatility)
                    'baseline': 1000,
                    'scale': 200
                },
                'trading_volume': {
                    'daily_cycle': 0.6,
                    'weekly_cycle': 0.5,
                    'trend': 0.05,
                    'noise': 0.3,
                    'baseline': 10000,
                    'scale': 5000
                },
                'volatility': {
                    'daily_cycle': 0.2,
                    'weekly_cycle': 0.3,
                    'trend': 0.0,
                    'noise': 0.6,  # High noise
                    'baseline': 0.02,
                    'scale': 0.03
                }
            },
            'social_media': {
                'sentiment': {
                    'daily_cycle': 0.5,
                    'weekly_cycle': 0.4,
                    'trend': -0.05,  # Slight downward trend
                    'noise': 0.5,  # High variability
                    'baseline': 0.0,
                    'scale': 1.0
                },
                'post_volume': {
                    'daily_cycle': 0.7,
                    'weekly_cycle': 0.6,
                    'trend': 0.1,
                    'noise': 0.3,
                    'baseline': 1000,
                    'scale': 500
                },
                'engagement_rate': {
                    'daily_cycle': 0.6,
                    'weekly_cycle': 0.4,
                    'trend': 0.0,
                    'noise': 0.4,
                    'baseline': 0.05,
                    'scale': 0.05
                }
            }
        }
        
        # Special correlation effects
        self.correlation_effects = [
            {
                'name': 'hot_weather_affects_social',
                'trigger': {'domain': 'weather', 'variable': 'temperature', 'threshold': 30},
                'effect': {'domain': 'social_media', 'variable': 'sentiment', 'effect': -0.3},
                'description': 'Hot weather decreases social media sentiment'
            },
            {
                'name': 'congestion_affects_sentiment',
                'trigger': {'domain': 'transportation', 'variable': 'congestion', 'threshold': 0.8},
                'effect': {'domain': 'social_media', 'variable': 'sentiment', 'effect': -0.5},
                'description': 'High traffic congestion decreases social media sentiment'
            },
            {
                'name': 'market_volatility_affects_traffic',
                'trigger': {'domain': 'economic', 'variable': 'volatility', 'threshold': 0.04},
                'effect': {'domain': 'transportation', 'variable': 'congestion', 'effect': 0.2},
                'description': 'High market volatility increases traffic congestion'
            }
        ]
        
        # Events (anomalies)
        self.events = [
            {
                'name': 'sudden_temperature_drop',
                'domain': 'weather',
                'variables': {'temperature': -10, 'wind_speed': 5},
                'duration': 6,  # hours
                'probability': 0.01
            },
            {
                'name': 'market_crash',
                'domain': 'economic',
                'variables': {'market_index': -100, 'volatility': 0.05},
                'duration': 12,  # hours
                'probability': 0.005
            },
            {
                'name': 'traffic_incident',
                'domain': 'transportation',
                'variables': {'congestion': 0.3, 'avg_speed': -15},
                'duration': 3,  # hours
                'probability': 0.02
            },
            {
                'name': 'viral_content',
                'domain': 'social_media',
                'variables': {'post_volume': 1000, 'engagement_rate': 0.1},
                'duration': 8,  # hours
                'probability': 0.015
            }
        ]
        
        # Active events
        self.active_events = []
    
    def _generate_base_signal(self, timestamp, params, hours_offset=0):
        """
        Generate a base signal value at a given timestamp using the provided parameters.
        
        Args:
            timestamp (datetime): The timestamp to generate the signal for
            params (dict): Signal parameters
            hours_offset (int): Optional hour offset for phase shifting
            
        Returns:
            float: The generated signal value
        """
        # Convert timestamp to hours since epoch
        hours = timestamp.timestamp() / 3600 + hours_offset
        
        # Calculate components
        daily = params.get('daily_cycle', 0) * self.base_signals['daily_cycle']['amplitude'] * \
                np.sin(2 * np.pi * hours / self.base_signals['daily_cycle']['period'] + 
                       self.base_signals['daily_cycle']['phase'])
        
        weekly = params.get('weekly_cycle', 0) * self.base_signals['weekly_cycle']['amplitude'] * \
                 np.sin(2 * np.pi * hours / self.base_signals['weekly_cycle']['period'] + 
                        self.base_signals['weekly_cycle']['phase'])
        
        trend = params.get('trend', 0) * self.base_signals['trend']['slope'] * hours + \
                self.base_signals['trend']['baseline']
        
        noise = params.get('noise', 0) * self.base_signals['noise']['level'] * \
                np.random.normal(0, 1)
        
        # Combine components
        signal = daily + weekly + trend + noise
        
        # Apply baseline and scaling
        signal = params.get('baseline', 0) + params.get('scale', 1) * signal
        
        return signal
    
    def _apply_correlation_effects(self, data):
        """
        Apply special correlation effects based on triggers.
        
        Args:
            data (dict): Generated data for all domains
            
        Returns:
            dict: Data with correlation effects applied
        """
        # Check each correlation effect
        for effect in self.correlation_effects:
            trigger = effect['trigger']
            trigger_domain = trigger['domain']
            trigger_var = trigger['variable']
            threshold = trigger['threshold']
            
            # Check if trigger condition is met
            if (trigger_domain in data and 
                trigger_var in data[trigger_domain] and 
                data[trigger_domain][trigger_var] > threshold):
                
                # Apply effect
                effect_info = effect['effect']
                effect_domain = effect_info['domain']
                effect_var = effect_info['variable']
                effect_value = effect_info['effect']
                
                if effect_domain in data and effect_var in data[effect_domain]:
                    data[effect_domain][effect_var] += effect_value
        
        return data
    
    def _check_and_apply_events(self, timestamp, data):
        """
        Check for random events and update active events.
        
        Args:
            timestamp (datetime): Current timestamp
            data (dict): Generated data for all domains
            
        Returns:
            dict: Data with events applied
        """
        # Remove expired events
        current_events = []
        for event in self.active_events:
            if timestamp < event['end_time']:
                current_events.append(event)
        self.active_events = current_events
        
        # Check for new random events
        for event_def in self.events:
            if random.random() < event_def['probability']:
                # Create new event
                event = {
                    'name': event_def['name'],
                    'domain': event_def['domain'],
                    'variables': event_def['variables'].copy(),
                    'end_time': timestamp + timedelta(hours=event_def['duration']),
                    'start_time': timestamp
                }
                self.active_events.append(event)
        
        # Apply active events
        for event in self.active_events:
            domain = event['domain']
            if domain in data:
                for var, effect in event['variables'].items():
                    if var in data[domain]:
                        data[domain][var] += effect
        
        return data
    
    def generate_data(self, timestamp=None, apply_effects=True, apply_events=True):
        """
        Generate cross-domain data for a specific timestamp.
        
        Args:
            timestamp (datetime, optional): The timestamp to generate data for. Defaults to current time.
            apply_effects (bool): Whether to apply correlation effects
            apply_events (bool): Whether to apply random events
            
        Returns:
            dict: Generated data for all domains
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        data = {}
        
        # Generate data for each domain
        for domain, variables in self.domain_params.items():
            domain_data = {
                'timestamp': timestamp.isoformat()
            }
            
            # Generate each variable
            for var_name, params in variables.items():
                # Add some hour offset to create phase shifts between domains
                hours_offset = hash(domain + var_name) % 12
                value = self._generate_base_signal(timestamp, params, hours_offset)
                
                # Apply constraints based on variable type
                if var_name == 'congestion' or var_name == 'engagement_rate':
                    value = max(0, min(1, value))  # Clamp to 0-1
                elif var_name == 'humidity':
                    value = max(0, min(100, value))  # Clamp to 0-100
                elif var_name == 'temperature':
                    value = max(-20, min(45, value))  # Reasonable temperature range
                elif var_name == 'wind_speed' or var_name == 'avg_speed':
                    value = max(0, value)  # Non-negative
                
                domain_data[var_name] = value
            
            data[domain] = domain_data
        
        # Apply correlation effects if requested
        if apply_effects:
            data = self._apply_correlation_effects(data)
        
        # Apply events if requested
        if apply_events:
            data = self._check_and_apply_events(timestamp, data)
        
        return data
    
    def generate_time_series(self, start_time=None, duration_hours=24, interval_minutes=15):
        """
        Generate a time series of cross-domain data.
        
        Args:
            start_time (datetime, optional): Start time. Defaults to 24 hours ago.
            duration_hours (int): Duration in hours to generate data for
            interval_minutes (int): Interval between data points in minutes
            
        Returns:
            dict: Time series data for all domains
        """
        if start_time is None:
            start_time = datetime.now() - timedelta(hours=duration_hours)
        
        # Calculate number of data points
        num_points = int(duration_hours * 60 / interval_minutes)
        
        # Initialize result structure
        time_series = {domain: [] for domain in self.domain_params.keys()}
        
        # Generate data for each time point
        for i in range(num_points):
            timestamp = start_time + timedelta(minutes=i * interval_minutes)
            data = self.generate_data(timestamp)
            
            # Append to time series
            for domain, domain_data in data.items():
                time_series[domain].append(domain_data)
        
        return time_series
    
    def generate_and_stream(self, callback, interval_seconds=10, duration_hours=None):
        """
        Generate and stream real-time data.
        
        Args:
            callback (callable): Function to call with each data point
            interval_seconds (int): Interval between data points in seconds
            duration_hours (int, optional): Duration to generate data for. If None, runs indefinitely.
            
        Returns:
            None
        """
        start_time = datetime.now()
        iterations = float('inf') if duration_hours is None else int(duration_hours * 3600 / interval_seconds)
        
        for i in range(iterations):
            # Generate data for current time
            timestamp = datetime.now()
            data = self.generate_data(timestamp)
            
            # Call callback with generated data
            callback(data)
            
            # Sleep until next interval
            time.sleep(interval_seconds)
    
    def get_active_events(self):
        """
        Get information about currently active events.
        
        Returns:
            list: Active events
        """
        now = datetime.now()
        active = []
        
        for event in self.active_events:
            if now < event['end_time']:
                # Calculate remaining time
                remaining_seconds = (event['end_time'] - now).total_seconds()
                
                active.append({
                    'name': event['name'],
                    'domain': event['domain'],
                    'variables': event['variables'],
                    'start_time': event['start_time'].isoformat(),
                    'end_time': event['end_time'].isoformat(),
                    'remaining_seconds': remaining_seconds
                })
        
        return active
    
    def get_correlation_info(self):
        """
        Get information about the correlations in the generated data.
        
        Returns:
            dict: Correlation information
        """
        correlations = []
        
        # Extract correlations from parameters
        for domain1, vars1 in self.domain_params.items():
            for var1, params1 in vars1.items():
                for domain2, vars2 in self.domain_params.items():
                    if domain1 >= domain2:  # Skip duplicates and self
                        continue
                        
                    for var2, params2 in vars2.items():
                        # Estimate correlation based on signal parameters
                        dc1 = params1.get('daily_cycle', 0)
                        dc2 = params2.get('daily_cycle', 0)
                        wc1 = params1.get('weekly_cycle', 0)
                        wc2 = params2.get('weekly_cycle', 0)
                        t1 = params1.get('trend', 0)
                        t2 = params2.get('trend', 0)
                        
                        # Simplified correlation estimate
                        corr = (dc1 * dc2 + wc1 * wc2 + t1 * t2) / 3
                        
                        # Add if significant
                        if abs(corr) > 0.2:
                            correlations.append({
                                'domains': [domain1, domain2],
                                'variables': [var1, var2],
                                'correlation': corr,
                                'strength': self._correlation_strength(corr)
                            })
        
        # Add correlations from effects
        for effect in self.correlation_effects:
            trigger = effect['trigger']
            effect_info = effect['effect']
            
            correlations.append({
                'domains': [trigger['domain'], effect_info['domain']],
                'variables': [trigger['variable'], effect_info['variable']],
                'correlation': -1 if effect_info['effect'] < 0 else 1,  # Simplified
                'strength': 'Strong',
                'description': effect['description']
            })
        
        return {
            'correlations': correlations,
            'domains': list(self.domain_params.keys())
        }
    
    def _correlation_strength(self, corr):
        """
        Convert correlation coefficient to strength description.
        
        Args:
            corr (float): Correlation coefficient
            
        Returns:
            str: Strength description
        """
        abs_corr = abs(corr)
        if abs_corr > 0.8:
            return "Very Strong"
        elif abs_corr > 0.6:
            return "Strong"
        elif abs_corr > 0.4:
            return "Moderate"
        elif abs_corr > 0.2:
            return "Weak"
        else:
            return "Very Weak"


# Example usage
if __name__ == "__main__":
    generator = CrossDomainGenerator(seed=42)
    
    # Generate data for current time
    data = generator.generate_data()
    print("Current Data:")
    for domain, values in data.items():
        print(f"{domain}: {values}")
    
    # Get correlation information
    corr_info = generator.get_correlation_info()
    print("\nCorrelations:")
    for corr in corr_info['correlations']:
        print(f"{corr['domains'][0]}.{corr['variables'][0]} ↔ {corr['domains'][1]}.{corr['variables'][1]}: {corr['correlation']:.2f} ({corr['strength']})")
    
    # Stream data example (commented out for demonstration)
    # def print_data(data):
    #     print(f"[{datetime.now().isoformat()}] New data received:")
    #     for domain, values in data.items():
    #         print(f"  {domain}: {list(values.keys())}")
    # 
    # generator.generate_and_stream(print_data, interval_seconds=5, duration_hours=0.1)  # Run for 6 minutes