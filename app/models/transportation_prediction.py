"""
Transportation prediction model for traffic and transit patterns
"""
import time
import random
import math
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from app.models.base_model import BaseModel

class TransportationPredictionModel(BaseModel):
    """Model for predicting transportation patterns and metrics"""
    
    def __init__(self):
        """Initialize the transportation prediction model"""
        super().__init__(
            name="Transportation Pattern Prediction",
            description="Predicts traffic conditions, congestion levels, and transit metrics",
            data_sources=["transportation"],
            prediction_types=["traffic", "transit", "congestion"]
        )
        # Initialize model-specific parameters
        self.weekly_patterns = {
            # Hour of day (0-23) by day of week (0=Monday, 6=Sunday)
            # Values represent typical congestion levels (0-1)
            0: [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.7, 0.8, 0.7, 0.6, 0.7, 0.7, 0.6, 0.7, 0.8, 0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1],  # Monday
            1: [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.7, 0.8, 0.7, 0.6, 0.7, 0.7, 0.6, 0.7, 0.8, 0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1],  # Tuesday
            2: [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.7, 0.8, 0.7, 0.6, 0.7, 0.7, 0.6, 0.7, 0.8, 0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1],  # Wednesday
            3: [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.7, 0.8, 0.7, 0.6, 0.7, 0.7, 0.6, 0.7, 0.8, 0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1],  # Thursday
            4: [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.7, 0.8, 0.7, 0.6, 0.7, 0.7, 0.6, 0.7, 0.8, 0.9, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2],  # Friday
            5: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.6, 0.6, 0.6, 0.5, 0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.2, 0.1],  # Saturday
            6: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1]   # Sunday
        }
        self.confidence_decay = 0.05  # Confidence reduction per hour
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process transportation data and generate predictions
        
        Args:
            data: Transportation data (traffic, transit, etc.)
            
        Returns:
            Dictionary with transportation predictions
        """
        start_time = time.time()
        
        try:
            self._update_status("processing")
            
            # Extract relevant data
            city = data.get('city', 'New York')
            data_type = data.get('data_type', 'traffic')
            
            # Different prediction methods based on data type
            if data_type == 'traffic':
                predictions = self._predict_traffic(data, city)
            elif data_type == 'transit':
                predictions = self._predict_transit(data, city)
            else:
                # Generic prediction for other types
                predictions = self._predict_generic(data, city, data_type)
            
            # Calculate prediction latency
            latency_ms = (time.time() - start_time) * 1000
            self._log_prediction(latency_ms)
            
            # Return predictions with metadata
            result = {
                'city': city,
                'data_type': data_type,
                'generated_at': datetime.now().isoformat(),
                'model_version': '1.0',
                'predictions': predictions
            }
            
            self._update_status("success")
            return result
            
        except Exception as e:
            self._update_status("error", e)
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def _predict_traffic(self, data: Dict[str, Any], city: str) -> Dict[str, Any]:
        """
        Predict traffic conditions
        
        Args:
            data: Traffic data
            city: City name
            
        Returns:
            Dictionary with traffic predictions
        """
        # Extract historical data if available
        traffic_data = []
        if 'traffic_data' in data and isinstance(data['traffic_data'], list):
            traffic_data = data['traffic_data']
        
        # Get current congestion level
        current_congestion = self._extract_current_congestion(data, traffic_data)
        
        # Generate prediction periods (24 hours ahead)
        prediction_periods = []
        now = datetime.now()
        for i in range(1, 25):
            prediction_periods.append(now + timedelta(hours=i))
        
        # Generate congestion predictions
        congestion_predictions = self._predict_congestion(current_congestion, prediction_periods, city)
        
        # Generate speed predictions based on congestion
        speed_predictions = self._predict_speeds(congestion_predictions)
        
        # Generate incident predictions
        incident_predictions = self._predict_incidents(congestion_predictions)
        
        # Combine predictions
        predictions = []
        for i, period in enumerate(prediction_periods):
            predictions.append({
                'timestamp': period.isoformat(),
                'congestion_level': round(congestion_predictions[i], 2),
                'avg_speed_mph': round(speed_predictions[i], 1),
                'incident_count': incident_predictions[i],
                'confidence': round(max(0.3, 0.9 - (i * self.confidence_decay)), 2)
            })
        
        return {
            'prediction_type': 'traffic',
            'periods': predictions,
            'hotspots': self._predict_hotspots(city, congestion_predictions)
        }
    
    def _predict_transit(self, data: Dict[str, Any], city: str) -> Dict[str, Any]:
        """
        Predict transit metrics
        
        Args:
            data: Transit data
            city: City name
            
        Returns:
            Dictionary with transit predictions
        """
        # Extract transit type
        transit_type = data.get('transit_type', 'all')
        
        # Extract current ridership if available
        current_ridership = 0
        if 'current_stats' in data and 'ridership' in data['current_stats']:
            current_ridership = data['current_stats']['ridership']
        else:
            # Estimate based on city size
            current_ridership = self._estimate_base_ridership(city)
        
        # Generate prediction periods (24 hours ahead)
        prediction_periods = []
        now = datetime.now()
        for i in range(1, 25):
            prediction_periods.append(now + timedelta(hours=i))
        
        # Generate ridership predictions
        ridership_predictions = self._predict_ridership(current_ridership, prediction_periods, city)
        
        # Generate on-time performance predictions
        ontime_predictions = self._predict_ontime_performance(prediction_periods)
        
        # Combine predictions
        predictions = []
        for i, period in enumerate(prediction_periods):
            predictions.append({
                'timestamp': period.isoformat(),
                'ridership': int(ridership_predictions[i]),
                'on_time_percentage': round(ontime_predictions[i], 1),
                'crowding_level': self._calculate_crowding_level(ridership_predictions[i], city),
                'confidence': round(max(0.3, 0.85 - (i * self.confidence_decay)), 2)
            })
        
        return {
            'prediction_type': 'transit',
            'transit_type': transit_type,
            'periods': predictions
        }
    
    def _predict_generic(self, data: Dict[str, Any], city: str, data_type: str) -> Dict[str, Any]:
        """
        Generic prediction method for other transportation data types
        
        Args:
            data: Input data
            city: City name
            data_type: Type of data
            
        Returns:
            Dictionary with predictions
        """
        # Generate prediction periods (24 hours ahead)
        prediction_periods = []
        now = datetime.now()
        for i in range(1, 25):
            prediction_periods.append(now + timedelta(hours=i))
        
        # Generate generic predictions
        predictions = []
        for i, period in enumerate(prediction_periods):
            # Create a prediction with random fluctuations
            predictions.append({
                'timestamp': period.isoformat(),
                'value': round(random.uniform(0.2, 0.8), 2),
                'confidence': round(max(0.3, 0.8 - (i * self.confidence_decay)), 2)
            })
        
        return {
            'prediction_type': data_type,
            'periods': predictions
        }
    
    def _extract_current_congestion(self, data: Dict[str, Any], traffic_data: List[Dict[str, Any]]) -> float:
        """
        Extract current congestion level from data
        
        Args:
            data: Traffic data
            traffic_data: Historical traffic data points
            
        Returns:
            Current congestion level (0-1)
        """
        # Try different paths to find congestion data
        if 'current_stats' in data and 'congestion_level' in data['current_stats']:
            return data['current_stats']['congestion_level']
        
        if traffic_data and 'congestion_level' in traffic_data[-1]:
            return traffic_data[-1]['congestion_level']
        
        # If not found, estimate based on time of day
        now = datetime.now()
        day_of_week = now.weekday()  # 0 = Monday, 6 = Sunday
        hour_of_day = now.hour
        
        # Get typical congestion for this time
        typical_congestion = self.weekly_patterns.get(day_of_week, self.weekly_patterns[0])[hour_of_day]
        
        # Add some randomness
        return min(1.0, max(0.1, typical_congestion + random.uniform(-0.1, 0.1)))
    
    def _predict_congestion(self, current_congestion: float, prediction_periods: List[datetime], 
                           city: str) -> List[float]:
        """
        Predict congestion levels for future periods
        
        Args:
            current_congestion: Current congestion level
            prediction_periods: List of prediction timestamps
            city: City name
            
        Returns:
            List of predicted congestion levels
        """
        predictions = []
        
        # City-specific factor (larger cities have higher base congestion)
        city_factor = self._get_city_congestion_factor(city)
        
        for period in prediction_periods:
            # Get day of week and hour
            day_of_week = period.weekday()
            hour_of_day = period.hour
            
            # Get typical congestion pattern for this time
            typical_congestion = self.weekly_patterns.get(day_of_week, self.weekly_patterns[0])[hour_of_day]
            
            # Adjust for city size
            city_adjusted = typical_congestion * city_factor
            
            # Blend current conditions with typical pattern
            # (current conditions have less influence as we look further ahead)
            hours_ahead = (period - datetime.now()).total_seconds() / 3600
            current_weight = max(0, 1.0 - (hours_ahead / 6))  # Current conditions matter for ~6 hours
            typical_weight = 1.0 - current_weight
            
            blended_congestion = (current_congestion * current_weight) + (city_adjusted * typical_weight)
            
            # Add some randomness (more for further predictions)
            randomness = 0.05 + (hours_ahead / 100)
            noise = random.uniform(-randomness, randomness)
            
            final_congestion = max(0.1, min(1.0, blended_congestion + noise))
            predictions.append(final_congestion)
        
        return predictions
    
    def _predict_speeds(self, congestion_levels: List[float]) -> List[float]:
        """
        Predict average speeds based on congestion levels
        
        Args:
            congestion_levels: List of congestion level predictions
            
        Returns:
            List of speed predictions (mph)
        """
        # Speed is inversely related to congestion
        # Assuming max speed of 65 mph in completely free-flowing traffic
        max_speed = 65.0
        
        speeds = []
        for congestion in congestion_levels:
            # Non-linear relationship between congestion and speed
            # Higher congestion has a more dramatic effect on speed
            speed = max_speed * (1 - congestion**1.5)
            
            # Add some noise
            noise = random.uniform(-3, 3)
            final_speed = max(5.0, speed + noise)  # At least 5 mph
            
            speeds.append(final_speed)
        
        return speeds
    
    def _predict_incidents(self, congestion_levels: List[float]) -> List[int]:
        """
        Predict number of traffic incidents based on congestion
        
        Args:
            congestion_levels: List of congestion level predictions
            
        Returns:
            List of incident count predictions
        """
        incidents = []
        
        for congestion in congestion_levels:
            # Higher congestion correlates with more incidents
            # Using a Poisson-like distribution based on congestion
            mean_incidents = congestion * 10  # Up to 10 incidents at max congestion
            
            # Generate a random count with appropriate distribution
            count = int(np.random.poisson(mean_incidents))
            incidents.append(count)
        
        return incidents
    
    def _predict_hotspots(self, city: str, congestion_predictions: List[float]) -> List[Dict[str, Any]]:
        """
        Predict traffic hotspots in the city
        
        Args:
            city: City name
            congestion_predictions: List of congestion predictions
            
        Returns:
            List of predicted hotspot dictionaries
        """
        # Number of hotspots depends on city size
        city_factor = self._get_city_congestion_factor(city)
        hotspot_count = int(3 + city_factor * 7)  # 3 to 10 hotspots
        
        # Generate consistent hotspot names for this city
        random.seed(hash(city))
        hotspot_names = [f"Hotspot {i+1}" for i in range(hotspot_count)]
        random.shuffle(hotspot_names)
        
        # Reset seed
        random.seed()
        
        # Choose a subset of hotspots that will be active
        active_count = int(hotspot_count * 0.6)  # 60% of hotspots active
        active_hotspots = []
        
        # Average of congestion predictions (weighting earlier predictions more)
        avg_congestion = sum(c * (1.0 - i*0.03) for i, c in enumerate(congestion_predictions[:10])) / sum((1.0 - i*0.03) for i in range(min(10, len(congestion_predictions))))
        
        for i in range(active_count):
            # Higher base congestion for early hotspots
            base_congestion = 0.7 + (0.3 * (active_count - i) / active_count)
            
            # Adjust congestion based on overall prediction
            hotspot_congestion = base_congestion * avg_congestion * random.uniform(0.9, 1.1)
            hotspot_congestion = min(1.0, hotspot_congestion)
            
            # Calculate average speed
            speed = 65.0 * (1 - hotspot_congestion**1.5)
            
            active_hotspots.append({
                'name': hotspot_names[i],
                'congestion_level': round(hotspot_congestion, 2),
                'avg_speed_mph': round(speed, 1),
                'delay_minutes': int(hotspot_congestion * 30)  # Up to 30 minutes delay
            })
        
        # Sort by congestion level
        active_hotspots.sort(key=lambda x: x['congestion_level'], reverse=True)
        
        return active_hotspots
    
    def _predict_ridership(self, current_ridership: int, prediction_periods: List[datetime], 
                          city: str) -> List[float]:
        """
        Predict transit ridership
        
        Args:
            current_ridership: Current ridership count
            prediction_periods: List of prediction timestamps
            city: City name
            
        Returns:
            List of ridership predictions
        """
        predictions = []
        
        # Get base ridership for this city
        base_ridership = self._estimate_base_ridership(city)
        
        # Adjust current ridership to a factor of the base
        current_factor = current_ridership / base_ridership if base_ridership > 0 else 1.0
        
        for period in prediction_periods:
            # Get day of week and hour
            day_of_week = period.weekday()
            hour_of_day = period.hour
            
            # Create ridership pattern similar to congestion but shifted
            # (transit ridership peaks slightly before traffic congestion in morning
            # and slightly after in evening)
            if day_of_week < 5:  # Weekday
                if 6 <= hour_of_day <= 9:  # Morning rush
                    time_factor = 0.7 + ((hour_of_day - 6) / 3) * 0.3  # Peaks at 9am
                elif 16 <= hour_of_day <= 19:  # Evening rush
                    time_factor = 0.7 + ((hour_of_day - 16) / 3) * 0.3  # Peaks at 7pm
                elif 10 <= hour_of_day <= 15:  # Midday
                    time_factor = 0.5
                else:  # Night
                    time_factor = 0.2
            else:  # Weekend
                if 10 <= hour_of_day <= 18:  # Daytime
                    time_factor = 0.4
                else:  # Night
                    time_factor = 0.2
            
            # Adjust for current conditions
            hours_ahead = (period - datetime.now()).total_seconds() / 3600
            current_weight = max(0, 1.0 - (hours_ahead / 4))  # Current conditions matter for ~4 hours
            pattern_weight = 1.0 - current_weight
            
            # Blend factors
            blended_factor = (current_factor * current_weight) + (time_factor * pattern_weight)
            
            # Calculate prediction with some noise
            noise = random.uniform(-0.05, 0.05)
            ridership = base_ridership * (blended_factor + noise)
            
            predictions.append(max(0, ridership))
        
        return predictions
    
    def _predict_ontime_performance(self, prediction_periods: List[datetime]) -> List[float]:
        """
        Predict on-time performance percentages
        
        Args:
            prediction_periods: List of prediction timestamps
            
        Returns:
            List of on-time percentage predictions
        """
        predictions = []
        
        # Base on-time percentage (typically high)
        base_ontime = 92.0
        
        for period in prediction_periods:
            # On-time performance is affected by time of day
            day_of_week = period.weekday()
            hour_of_day = period.hour
            
            # Adjust for rush hour
            if day_of_week < 5:  # Weekday
                if 7 <= hour_of_day <= 9 or 16 <= hour_of_day <= 18:  # Rush hours
                    time_factor = -3.0  # Lower on-time % during rush hour
                else:
                    time_factor = 0.0
            else:  # Weekend
                time_factor = 2.0  # Better on weekend
            
            # Weather can be a factor (would be incorporated here in a real model)
            
            # More uncertainty further in the future
            hours_ahead = (period - datetime.now()).total_seconds() / 3600
            uncertainty = min(5.0, hours_ahead / 10)  # Up to 5% uncertainty
            
            # Calculate with noise
            noise = random.uniform(-uncertainty, uncertainty)
            ontime = base_ontime + time_factor + noise
            
            # Ensure reasonable bounds
            ontime = max(70.0, min(99.9, ontime))
            
            predictions.append(ontime)
        
        return predictions
    
    def _calculate_crowding_level(self, ridership: float, city: str) -> str:
        """
        Calculate crowding level description based on ridership
        
        Args:
            ridership: Predicted ridership
            city: City name
            
        Returns:
            Crowding level description
        """
        # Get base ridership for this city
        base_ridership = self._estimate_base_ridership(city)
        
        # Calculate as a percentage of base
        if base_ridership > 0:
            percentage = ridership / base_ridership
        else:
            percentage = 0.5
        
        if percentage < 0.3:
            return "Light"
        elif percentage < 0.6:
            return "Moderate"
        elif percentage < 0.85:
            return "Heavy"
        else:
            return "Severe"
    
    def _get_city_congestion_factor(self, city: str) -> float:
        """
        Get congestion factor based on city (larger cities have higher congestion)
        
        Args:
            city: City name
            
        Returns:
            Congestion factor (0.5-1.5)
        """
        city_factors = {
            'New York': 1.5,
            'Los Angeles': 1.5,
            'Chicago': 1.3,
            'Houston': 1.2,
            'Phoenix': 1.0,
            'Philadelphia': 1.2,
            'San Antonio': 1.0,
            'San Diego': 1.1,
            'Dallas': 1.2,
            'San Jose': 1.2,
            'London': 1.4,
            'Paris': 1.3,
            'Tokyo': 1.5,
            'Berlin': 1.1,
            'Madrid': 1.2
        }
        
        return city_factors.get(city, 1.0)
    
    def _estimate_base_ridership(self, city: str) -> int:
        """
        Estimate base ridership based on city size
        
        Args:
            city: City name
            
        Returns:
            Base ridership estimate
        """
        city_factors = {
            'New York': 1000000,
            'Los Angeles': 500000,
            'Chicago': 750000,
            'Houston': 300000,
            'Phoenix': 200000,
            'Philadelphia': 400000,
            'San Antonio': 150000,
            'San Diego': 250000,
            'Dallas': 350000,
            'San Jose': 200000,
            'London': 950000,
            'Paris': 900000,
            'Tokyo': 1500000,
            'Berlin': 500000,
            'Madrid': 600000
        }
        
        return city_factors.get(city, 300000)