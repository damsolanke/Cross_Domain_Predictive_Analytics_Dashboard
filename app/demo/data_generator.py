"""
Demo data generator for the Cross-Domain Predictive Analytics Dashboard
"""
import time
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
import threading

# Import API connectors to generate data
from app.api.connectors.weather_connector import WeatherConnector
from app.api.connectors.economic_connector import EconomicConnector
from app.api.connectors.transportation_connector import TransportationConnector
from app.api.connectors.social_media_connector import SocialMediaConnector

# Import ML models to generate predictions
from app.models.weather_prediction import WeatherPredictionModel
from app.models.economic_prediction import EconomicPredictionModel
from app.models.transportation_prediction import TransportationPredictionModel
from app.models.cross_domain_model import CrossDomainModel

# Import system integration components
from app.system_integration.pipeline import DataPipeline
from app.system_integration.alert_system import AlertSystem

class DemoDataGenerator:
    """
    Generates demo data for the dashboard by simulating API data sources,
    ML model predictions, and system integration.
    """
    
    def __init__(self):
        """Initialize the demo data generator"""
        # Create API connectors
        self.weather_connector = WeatherConnector()
        self.economic_connector = EconomicConnector()
        self.transportation_connector = TransportationConnector()
        self.social_media_connector = SocialMediaConnector()
        
        # Create ML models
        self.weather_model = WeatherPredictionModel()
        self.economic_model = EconomicPredictionModel()
        self.transportation_model = TransportationPredictionModel()
        self.cross_domain_model = CrossDomainModel()
        
        # Create system integration components
        self.data_pipeline = DataPipeline()
        self.alert_system = AlertSystem()
        
        # Data generation control
        self.is_generating = False
        self.generation_thread = None
        self.generation_interval = 30  # seconds
        
        # Use case scenarios
        self.active_scenario = None
        self.scenarios = [
            'baseline',
            'weather_event',
            'economic_volatility',
            'transportation_disruption',
            'social_media_trend'
        ]
        
        # Selected locations for demo
        self.locations = [
            'New York', 
            'Chicago', 
            'Los Angeles', 
            'Miami',
            'Seattle'
        ]
        
    def start_generation(self, interval: int = 30, scenario: str = 'baseline'):
        """
        Start generating demo data
        
        Args:
            interval: Time interval between data updates in seconds
            scenario: Active scenario to simulate
        """
        if self.is_generating:
            return False
        
        # Set parameters
        self.generation_interval = interval
        self.active_scenario = scenario
        
        # Start generation thread
        self.is_generating = True
        self.generation_thread = threading.Thread(target=self._generation_loop)
        self.generation_thread.daemon = True
        self.generation_thread.start()
        
        print(f"Demo data generation started with {interval}s interval using '{scenario}' scenario")
        return True
    
    def stop_generation(self):
        """Stop generating demo data"""
        if not self.is_generating:
            return False
        
        self.is_generating = False
        if self.generation_thread:
            self.generation_thread.join(timeout=5.0)
            self.generation_thread = None
        
        print("Demo data generation stopped")
        return True
    
    def set_scenario(self, scenario: str):
        """
        Set the active scenario
        
        Args:
            scenario: Scenario name to use
        """
        if scenario in self.scenarios:
            self.active_scenario = scenario
            print(f"Active scenario changed to '{scenario}'")
            return True
        
        return False
    
    def generate_single_update(self, scenario: Optional[str] = None):
        """
        Generate a single data update
        
        Args:
            scenario: Optional scenario to use (defaults to active scenario)
        """
        # Use specified scenario or active scenario
        scenario = scenario or self.active_scenario or 'baseline'
        
        # Generate data for each domain
        try:
            # Generate data for each location
            for location in self.locations:
                # Generate weather data
                weather_data = self._generate_weather_data(location, scenario)
                self.data_pipeline.submit_data('weather', weather_data)
                
                # Generate economic data
                economic_data = self._generate_economic_data('US', scenario)
                self.data_pipeline.submit_data('economic', economic_data)
                
                # Generate transportation data
                transportation_data = self._generate_transportation_data(location, scenario)
                self.data_pipeline.submit_data('transportation', transportation_data)
                
                # Generate social media data
                social_media_data = self._generate_social_media_data(location, scenario)
                self.data_pipeline.submit_data('social-media', social_media_data)
            
            # Generate cross-domain data periodically
            self._generate_cross_domain_data(scenario)
            
            print(f"Generated demo data update for scenario '{scenario}'")
            return True
            
        except Exception as e:
            print(f"Error generating demo data: {e}")
            return False
    
    def _generation_loop(self):
        """Background thread for generating periodic data updates"""
        while self.is_generating:
            try:
                # Generate data update
                self.generate_single_update()
                
                # Sleep until next update
                for _ in range(self.generation_interval):
                    if not self.is_generating:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Error in data generation loop: {e}")
                time.sleep(5)  # Sleep on error to avoid tight loop
    
    def _generate_weather_data(self, location: str, scenario: str) -> Dict[str, Any]:
        """
        Generate weather data for a specific location and scenario
        
        Args:
            location: Location name
            scenario: Active scenario
        
        Returns:
            Weather data dictionary
        """
        # Use the weather connector to generate baseline data
        weather_params = {
            'location': location,
            'units': 'metric',
            'type': 'current'
        }
        
        # Get baseline data from connector
        data = self.weather_connector.fetch_data(weather_params)
        
        # Apply scenario-specific modifications
        if scenario == 'weather_event':
            # Simulate extreme weather event
            data['current']['weather']['main'] = random.choice(['Thunderstorm', 'Snow', 'Rain'])
            data['current']['weather']['description'] = f"Severe {data['current']['weather']['main']}"
            
            # Adjust temperature and other metrics
            if data['current']['weather']['main'] == 'Thunderstorm':
                data['current']['temp'] -= 5  # Cooler during thunderstorms
                data['current']['humidity'] = min(100, data['current']['humidity'] + 30)
            elif data['current']['weather']['main'] == 'Snow':
                data['current']['temp'] = min(0, data['current']['temp'] - 10)  # Cold for snow
            else:  # Rain
                data['current']['humidity'] = min(100, data['current']['humidity'] + 20)
        
        # Generate prediction using the weather model
        prediction = self.weather_model.process(data)
        
        # Combine data and prediction
        data['prediction'] = prediction
        
        return data
    
    def _generate_economic_data(self, country: str, scenario: str) -> Dict[str, Any]:
        """
        Generate economic data for a specific country and scenario
        
        Args:
            country: Country code
            scenario: Active scenario
        
        Returns:
            Economic data dictionary
        """
        # Generate data for different economic indicators
        indicators = ['inflation', 'gdp', 'interest_rates', 'stock_market']
        
        # Select a random indicator each time
        indicator = random.choice(indicators)
        
        # Use the economic connector to generate baseline data
        economic_params = {
            'country': country,
            'indicator': indicator,
            'timeframe': 'monthly'
        }
        
        # Get baseline data from connector
        data = self.economic_connector.fetch_data(economic_params)
        
        # Apply scenario-specific modifications
        if scenario == 'economic_volatility':
            # Simulate economic volatility
            if indicator == 'inflation':
                # Increased inflation
                for point in data['data']:
                    point['value'] *= 1.5
            elif indicator == 'stock_market':
                # Market volatility - decrease values
                for point in data['data']:
                    point['value'] *= 0.85
            elif indicator == 'interest_rates':
                # Higher interest rates
                for point in data['data']:
                    point['value'] += 1.5
        
        # Generate prediction using the economic model
        prediction = self.economic_model.process(data)
        
        # Combine data and prediction
        data['prediction'] = prediction
        
        return data
    
    def _generate_transportation_data(self, city: str, scenario: str) -> Dict[str, Any]:
        """
        Generate transportation data for a specific city and scenario
        
        Args:
            city: City name
            scenario: Active scenario
        
        Returns:
            Transportation data dictionary
        """
        # Use the transportation connector to generate baseline data
        transportation_params = {
            'city': city,
            'data_type': 'traffic',
            'timeframe': 'day'
        }
        
        # Get baseline data from connector
        data = self.transportation_connector.fetch_data(transportation_params)
        
        # Apply scenario-specific modifications
        if scenario == 'transportation_disruption':
            # Simulate transportation disruption
            for point in data['traffic_data']:
                point['congestion_level'] = min(1.0, point['congestion_level'] * 1.7)
                point['avg_speed_mph'] *= 0.6
                
                # Add more incidents
                point['incidents'].extend([
                    {
                        'type': 'Road Closure',
                        'severity': 'High',
                        'expected_duration_minutes': 120,
                        'lanes_affected': 3
                    },
                    {
                        'type': 'Accident',
                        'severity': 'High',
                        'expected_duration_minutes': 90,
                        'lanes_affected': 2
                    }
                ])
        elif scenario == 'weather_event':
            # Weather affects transportation
            for point in data['traffic_data']:
                point['congestion_level'] = min(1.0, point['congestion_level'] * 1.4)
                point['avg_speed_mph'] *= 0.7
                
                # Add weather-related incident
                point['incidents'].append({
                    'type': 'Weather Hazard',
                    'severity': 'Medium',
                    'expected_duration_minutes': 180,
                    'lanes_affected': 'All'
                })
        
        # Generate prediction using the transportation model
        prediction = self.transportation_model.process(data)
        
        # Combine data and prediction
        data['prediction'] = prediction
        
        return data
    
    def _generate_social_media_data(self, location: str, scenario: str) -> Dict[str, Any]:
        """
        Generate social media data for a specific location and scenario
        
        Args:
            location: Location name
            scenario: Active scenario
        
        Returns:
            Social media data dictionary
        """
        # Use the social media connector to generate baseline data
        social_media_params = {
            'platform': 'twitter',
            'data_type': 'trends',
            'location': location,
            'timeframe': 'day'
        }
        
        # Get baseline data from connector
        data = self.social_media_connector.fetch_data(social_media_params)
        
        # Apply scenario-specific modifications
        if scenario == 'social_media_trend':
            # Simulate viral social media trend
            if 'trending_topics' in data and data['trending_topics']:
                # Make the top topic super viral
                data['trending_topics'][0]['growth_rate'] = 500
                data['trending_topics'][0]['volume'] *= 10
                
                # Add topic related to the scenario
                viral_topic = {
                    'topic': "#ViralChallenge",
                    'category': "Entertainment",
                    'volume': 500000,
                    'growth_rate': 800,
                    'rank': 1
                }
                
                # Insert at beginning and reorder ranks
                data['trending_topics'].insert(0, viral_topic)
                for i, topic in enumerate(data['trending_topics']):
                    topic['rank'] = i + 1
        
        elif scenario == 'weather_event':
            # Social media reacts to weather
            if 'trending_topics' in data and data['trending_topics']:
                # Add weather-related topics
                weather_topic = {
                    'topic': f"#Severe{random.choice(['Storm', 'Weather', 'Snow', 'Rain'])}",
                    'category': "News",
                    'volume': 250000,
                    'growth_rate': 400,
                    'rank': 1
                }
                
                # Insert at beginning and reorder ranks
                data['trending_topics'].insert(0, weather_topic)
                for i, topic in enumerate(data['trending_topics']):
                    topic['rank'] = i + 1
        
        elif scenario == 'transportation_disruption':
            # Social media reacts to transportation issues
            if 'trending_topics' in data and data['trending_topics']:
                # Add transportation-related topics
                topic = {
                    'topic': f"#{location.replace(' ', '')}Traffic",
                    'category': "Travel",
                    'volume': 150000,
                    'growth_rate': 350,
                    'rank': 1
                }
                
                # Insert at beginning and reorder ranks
                data['trending_topics'].insert(0, topic)
                for i, topic in enumerate(data['trending_topics']):
                    topic['rank'] = i + 1
        
        return data
    
    def _generate_cross_domain_data(self, scenario: str):
        """
        Generate cross-domain correlation data
        
        Args:
            scenario: Active scenario
        """
        # This method is called less frequently (not every update)
        if random.random() > 0.3:  # 30% chance of generating cross-domain data
            return
        
        try:
            # Get processed data from the pipeline
            processed_data = self.data_pipeline.get_processed_data(limit=20)
            
            if not processed_data:
                return
            
            # Extract metrics from each domain
            domain_metrics = {}
            
            for item in processed_data:
                source = item.get('source', '')
                
                if source == 'weather':
                    domain_metrics['weather'] = self._extract_weather_metrics(item)
                elif source == 'economic':
                    domain_metrics['economic'] = self._extract_economic_metrics(item)
                elif source == 'transportation':
                    domain_metrics['transportation'] = self._extract_transportation_metrics(item)
                elif source == 'social-media':
                    domain_metrics['social-media'] = self._extract_social_media_metrics(item)
            
            # Only proceed if we have data from multiple domains
            if len(domain_metrics) >= 2:
                # Generate cross-domain analysis
                cross_domain_data = self.cross_domain_model.process(domain_metrics)
                
                # Submit to pipeline
                self.data_pipeline.submit_data('cross-domain', cross_domain_data)
                
                # Check for significant correlations that might trigger alerts
                if 'correlations' in cross_domain_data:
                    for correlation in cross_domain_data['correlations']:
                        if abs(correlation.get('correlation', 0)) > 0.7:
                            # Create alert for strong correlation
                            alert = {
                                'type': 'cross_domain_correlation',
                                'level': 'info',
                                'domains': correlation['domains'],
                                'correlation': correlation['correlation'],
                                'message': f"Strong {correlation['direction']} correlation detected between {correlation['domains'][0]} and {correlation['domains'][1]}",
                                'timestamp': datetime.now().isoformat()
                            }
                            
                            self.alert_system.add_alert(alert)
                
                # Check for significant predictions that might trigger alerts
                if 'predictions' in cross_domain_data:
                    for horizon in ['short_term', 'medium_term', 'long_term']:
                        if horizon in cross_domain_data['predictions']:
                            horizon_preds = cross_domain_data['predictions'][horizon]
                            for pred in horizon_preds:
                                # Look for high-confidence predictions
                                if pred.get('confidence', 0) > 0.8:
                                    alert = {
                                        'type': 'cross_domain_prediction',
                                        'level': 'info',
                                        'domains': pred.get('domains', []),
                                        'prediction': pred.get('prediction', ''),
                                        'confidence': pred.get('confidence', 0),
                                        'message': f"High-confidence cross-domain prediction: {pred.get('prediction', '')}",
                                        'timestamp': datetime.now().isoformat()
                                    }
                                    
                                    self.alert_system.add_alert(alert)
            
        except Exception as e:
            print(f"Error generating cross-domain data: {e}")
    
    def _extract_weather_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from weather data"""
        metrics = {}
        
        # Try different data structures
        if 'payload' in data and 'current' in data['payload']:
            current = data['payload']['current']
            metrics['temperature'] = current.get('temp', 20)
            metrics['humidity'] = current.get('humidity', 50)
            
            if 'weather' in current and current['weather']:
                weather = current['weather'].get('main', '')
                metrics['extreme_weather'] = 1.0 if weather in ['Thunderstorm', 'Snow', 'Rain'] else 0.0
        
        elif 'original' in data and 'current' in data['original']:
            current = data['original']['current']
            metrics['temperature'] = current.get('temp', 20)
            metrics['humidity'] = current.get('humidity', 50)
            
            if 'weather' in current and current['weather']:
                weather = current['weather'].get('main', '')
                metrics['extreme_weather'] = 1.0 if weather in ['Thunderstorm', 'Snow', 'Rain'] else 0.0
        
        # Default values if not found
        if 'temperature' not in metrics:
            metrics['temperature'] = 20
        if 'humidity' not in metrics:
            metrics['humidity'] = 50
        if 'extreme_weather' not in metrics:
            metrics['extreme_weather'] = 0.0
        
        return metrics
    
    def _extract_economic_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from economic data"""
        metrics = {}
        
        # Try different data structures
        if 'payload' in data and 'indicator' in data['payload']:
            payload = data['payload']
            indicator = payload['indicator']
            
            if 'data' in payload and payload['data']:
                latest = payload['data'][-1]
                metrics[indicator] = latest.get('value', 0)
        
        elif 'original' in data and 'indicator' in data['original']:
            original = data['original']
            indicator = original['indicator']
            
            if 'data' in original and original['data']:
                latest = original['data'][-1]
                metrics[indicator] = latest.get('value', 0)
        
        # Default values
        if 'gdp_growth' not in metrics:
            metrics['gdp_growth'] = 2.5
        if 'inflation' not in metrics:
            metrics['inflation'] = 2.0
        if 'interest_rate' not in metrics:
            metrics['interest_rate'] = 3.0
        
        # Add volatility metric
        metrics['volatility'] = 0.3  # Default moderate volatility
        
        return metrics
    
    def _extract_transportation_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from transportation data"""
        metrics = {}
        
        # Try different data structures
        if 'payload' in data and 'traffic_data' in data['payload']:
            traffic_data = data['payload']['traffic_data']
            if traffic_data:
                latest = traffic_data[-1]
                metrics['congestion'] = latest.get('congestion_level', 0.4)
                metrics['speed'] = latest.get('avg_speed_mph', 30)
                metrics['incident_count'] = len(latest.get('incidents', []))
        
        elif 'original' in data and 'traffic_data' in data['original']:
            traffic_data = data['original']['traffic_data']
            if traffic_data:
                latest = traffic_data[-1]
                metrics['congestion'] = latest.get('congestion_level', 0.4)
                metrics['speed'] = latest.get('avg_speed_mph', 30)
                metrics['incident_count'] = len(latest.get('incidents', []))
        
        # Default values
        if 'congestion' not in metrics:
            metrics['congestion'] = 0.4
        if 'speed' not in metrics:
            metrics['speed'] = 30
        if 'incident_count' not in metrics:
            metrics['incident_count'] = 0
        
        return metrics
    
    def _extract_social_media_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from social media data"""
        metrics = {}
        
        # Try different data structures
        if 'payload' in data and 'trending_topics' in data['payload']:
            trending_topics = data['payload']['trending_topics']
            if trending_topics:
                # Average growth rate of top topics
                growth_rates = [topic.get('growth_rate', 0) for topic in trending_topics[:5]]
                if growth_rates:
                    metrics['trend_intensity'] = sum(growth_rates) / len(growth_rates) / 100
        
        elif 'original' in data and 'trending_topics' in data['original']:
            trending_topics = data['original']['trending_topics']
            if trending_topics:
                # Average growth rate of top topics
                growth_rates = [topic.get('growth_rate', 0) for topic in trending_topics[:5]]
                if growth_rates:
                    metrics['trend_intensity'] = sum(growth_rates) / len(growth_rates) / 100
        
        # Default sentiment values
        metrics['positive_sentiment'] = 0.5
        metrics['negative_sentiment'] = 0.2
        metrics['net_sentiment'] = metrics['positive_sentiment'] - metrics['negative_sentiment']
        
        # Default trend intensity if not calculated
        if 'trend_intensity' not in metrics:
            metrics['trend_intensity'] = 0.5
        
        return metrics


# Create singleton instance
demo_generator = DemoDataGenerator()