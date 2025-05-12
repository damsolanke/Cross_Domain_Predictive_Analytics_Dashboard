"""
Weather prediction model for forecasting weather conditions
"""
import time
import random
import math
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from app.models.base_model import BaseModel

class WeatherPredictionModel(BaseModel):
    """Model for predicting weather conditions based on historical data"""
    
    def __init__(self):
        """Initialize the weather prediction model"""
        super().__init__(
            name="Weather Prediction Model",
            description="Predicts weather conditions based on historical patterns and current data",
            data_sources=["weather"],
            prediction_types=["temperature", "precipitation", "wind", "humidity"]
        )
        # Initialize model-specific parameters
        self.temperature_seasonality = 0.8  # Strength of seasonal patterns
        self.precipitation_randomness = 0.4  # How random precipitation is
        self.confidence_bounds = {
            'hours_1_12': 0.9,
            'hours_13_24': 0.85,
            'hours_25_48': 0.75,
            'hours_49_72': 0.65,
            'days_4_7': 0.55
        }
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process weather data and generate predictions
        
        Args:
            data: Weather data with historical patterns
            
        Returns:
            Dictionary with weather predictions
        """
        start_time = time.time()
        
        try:
            self._update_status("processing")
            
            # Extract relevant data
            location = data.get('location', 'unknown')
            current_temp = self._extract_temperature(data)
            current_conditions = self._extract_conditions(data)
            
            # Get timestamps for predictions
            prediction_timestamps = self._get_prediction_timestamps()
            
            # Generate predictions for different time horizons
            temperature_predictions = self._predict_temperature(current_temp, prediction_timestamps)
            precipitation_predictions = self._predict_precipitation(current_conditions, prediction_timestamps)
            
            # Calculate confidence scores
            confidence_scores = self._get_confidence_scores(prediction_timestamps)
            
            # Combine predictions
            predictions = []
            for i, timestamp in enumerate(prediction_timestamps):
                predictions.append({
                    'timestamp': timestamp,
                    'temperature': round(temperature_predictions[i], 1),
                    'precipitation_chance': round(precipitation_predictions[i], 2),
                    'conditions': self._predict_conditions(current_conditions, precipitation_predictions[i]),
                    'confidence': round(confidence_scores[i], 2)
                })
            
            # Calculate prediction latency
            latency_ms = (time.time() - start_time) * 1000
            self._log_prediction(latency_ms)
            
            # Return predictions with metadata
            result = {
                'location': location,
                'generated_at': datetime.now().isoformat(),
                'model_version': '1.0',
                'predictions': predictions,
                'overall_confidence': round(sum(confidence_scores) / len(confidence_scores), 2)
            }
            
            self._update_status("success")
            return result
            
        except Exception as e:
            self._update_status("error", e)
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def _extract_temperature(self, data: Dict[str, Any]) -> float:
        """Extract current temperature from data"""
        # Try to find temperature in different data structures
        if 'current' in data and 'temp' in data['current']:
            return data['current']['temp']
        elif 'temperature' in data:
            return data['temperature']
        elif 'temp' in data:
            return data['temp']
        
        # Default fallback temperature
        return 20.0  # Celsius
    
    def _extract_conditions(self, data: Dict[str, Any]) -> str:
        """Extract current weather conditions from data"""
        # Try to find conditions in different data structures
        if 'current' in data and 'weather' in data['current'] and 'main' in data['current']['weather']:
            return data['current']['weather']['main']
        elif 'weather' in data and 'main' in data['weather']:
            return data['weather']['main']
        elif 'conditions' in data:
            return data['conditions']
        
        # Default fallback condition
        return "Clear"
    
    def _get_prediction_timestamps(self) -> List[str]:
        """Generate timestamps for prediction horizons"""
        timestamps = []
        now = datetime.now()
        
        # Hourly for first 24 hours
        for i in range(1, 25):
            timestamps.append((now + timedelta(hours=i)).isoformat())
        
        # Every 6 hours for days 2-3
        for i in range(4, 13):
            timestamps.append((now + timedelta(hours=i*6)).isoformat())
        
        # Daily for days 4-7
        for i in range(4, 8):
            timestamps.append((now + timedelta(days=i)).isoformat())
        
        return timestamps
    
    def _predict_temperature(self, current_temp: float, timestamps: List[str]) -> List[float]:
        """
        Predict temperatures for given timestamps
        
        Args:
            current_temp: Current temperature
            timestamps: List of prediction timestamps
            
        Returns:
            List of predicted temperatures
        """
        predictions = []
        
        # Convert timestamps to datetime objects
        datetimes = [datetime.fromisoformat(ts) for ts in timestamps]
        
        # Get base temperature for this time of year
        base_temp = self._get_seasonal_base_temp(datetimes[0])
        
        # Generate predictions with trending towards seasonal average
        for dt in datetimes:
            # Calculate hours from now
            hours_ahead = (dt - datetime.now()).total_seconds() / 3600
            
            # Weight between current temperature and seasonal baseline
            # The further ahead, the more we rely on seasonal patterns
            seasonal_weight = min(1.0, hours_ahead / 120)  # Full seasonal weight after 5 days
            current_weight = 1.0 - seasonal_weight
            
            # Calculate target temperature
            target_temp = current_temp * current_weight + base_temp * seasonal_weight
            
            # Add time-of-day variation (cooler at night, warmer in afternoon)
            hour_of_day = dt.hour
            time_of_day_offset = self._get_time_of_day_offset(hour_of_day)
            
            # Add noise that increases with forecast distance
            noise_amplitude = min(5.0, hours_ahead / 24)  # Up to 5 degrees of noise
            noise = random.uniform(-noise_amplitude, noise_amplitude)
            
            # Combine all factors
            predicted_temp = target_temp + time_of_day_offset + noise
            
            predictions.append(predicted_temp)
        
        return predictions
    
    def _get_seasonal_base_temp(self, dt: datetime) -> float:
        """
        Get the baseline temperature for a given time of year
        
        Args:
            dt: Datetime object
            
        Returns:
            Baseline temperature for this time of year
        """
        # This is a simplified model that assumes temperature follows a sinusoidal pattern throughout the year
        # A more realistic model would use historical data for the specific location
        
        # Day of year from 0 to 1
        day_of_year = (dt.timetuple().tm_yday - 1) / 365
        
        # Northern hemisphere (adjust for southern hemisphere if needed)
        # Peak in summer (day 172, ~June 21), trough in winter (day 355, ~Dec 21)
        seasonal_factor = math.sin(2 * math.pi * (day_of_year - 0.5))
        
        # Temperature varies between 0°C and 30°C by default
        return 15 + 15 * seasonal_factor * self.temperature_seasonality
    
    def _get_time_of_day_offset(self, hour: int) -> float:
        """
        Get temperature offset based on time of day
        
        Args:
            hour: Hour of day (0-23)
            
        Returns:
            Temperature offset
        """
        # Simple model: coldest at 4am, warmest at 2pm
        phase_shift = (hour - 4) % 24  # Hours since coldest time
        normalized_phase = phase_shift / 24
        
        # Sinusoidal pattern with 10 degree amplitude
        return 5 * math.sin(2 * math.pi * normalized_phase)
    
    def _predict_precipitation(self, current_conditions: str, timestamps: List[str]) -> List[float]:
        """
        Predict precipitation probability for given timestamps
        
        Args:
            current_conditions: Current weather conditions
            timestamps: List of prediction timestamps
            
        Returns:
            List of precipitation probabilities (0-1)
        """
        predictions = []
        
        # Convert timestamps to datetime objects
        datetimes = [datetime.fromisoformat(ts) for ts in timestamps]
        
        # Base precipitation probability depends on current conditions
        if 'Rain' in current_conditions or 'Drizzle' in current_conditions:
            base_prob = 0.7
        elif 'Thunderstorm' in current_conditions:
            base_prob = 0.8
        elif 'Snow' in current_conditions:
            base_prob = 0.6
        elif 'Clouds' in current_conditions:
            base_prob = 0.4
        elif 'Mist' in current_conditions or 'Fog' in current_conditions:
            base_prob = 0.3
        else:  # Clear
            base_prob = 0.1
        
        # Generate predictions
        for dt in datetimes:
            # Calculate hours from now
            hours_ahead = (dt - datetime.now()).total_seconds() / 3600
            
            # Precipitation probability tends toward climatological average as we go further out
            climatological_avg = 0.3  # Average precipitation chance
            forecasting_horizon = min(1.0, hours_ahead / 120)  # Full weight after 5 days
            
            # Blend current-based probability with climatological average
            blended_prob = base_prob * (1 - forecasting_horizon) + climatological_avg * forecasting_horizon
            
            # Add randomness that increases with time
            randomness = min(0.5, self.precipitation_randomness * hours_ahead / 48)
            random_factor = random.uniform(-randomness, randomness)
            
            # Combine factors and ensure probability is between 0 and 1
            prob = max(0.0, min(1.0, blended_prob + random_factor))
            
            predictions.append(prob)
        
        return predictions
    
    def _predict_conditions(self, current_conditions: str, precipitation_prob: float) -> str:
        """
        Predict weather conditions based on precipitation probability
        
        Args:
            current_conditions: Current weather conditions
            precipitation_prob: Precipitation probability
            
        Returns:
            Predicted weather conditions
        """
        if precipitation_prob > 0.7:
            if random.random() > 0.7:
                return "Thunderstorm"
            else:
                return "Rain"
        elif precipitation_prob > 0.4:
            if "Snow" in current_conditions and random.random() > 0.5:
                return "Snow"
            else:
                return "Rain"
        elif precipitation_prob > 0.3:
            return "Drizzle"
        elif precipitation_prob > 0.2:
            return "Clouds"
        elif random.random() > 0.8:
            return "Mist"
        else:
            return "Clear"
    
    def _get_confidence_scores(self, timestamps: List[str]) -> List[float]:
        """
        Calculate confidence scores for each prediction timestamp
        
        Args:
            timestamps: List of prediction timestamps
            
        Returns:
            List of confidence scores (0-1)
        """
        confidence_scores = []
        
        # Convert timestamps to datetime objects
        datetimes = [datetime.fromisoformat(ts) for ts in timestamps]
        
        for dt in datetimes:
            # Calculate hours from now
            hours_ahead = (dt - datetime.now()).total_seconds() / 3600
            
            # Assign confidence based on prediction horizon
            if hours_ahead <= 12:
                confidence = self.confidence_bounds['hours_1_12']
            elif hours_ahead <= 24:
                confidence = self.confidence_bounds['hours_13_24']
            elif hours_ahead <= 48:
                confidence = self.confidence_bounds['hours_25_48']
            elif hours_ahead <= 72:
                confidence = self.confidence_bounds['hours_49_72']
            else:
                confidence = self.confidence_bounds['days_4_7']
            
            # Add small random variation
            confidence += random.uniform(-0.05, 0.05)
            confidence = max(0.0, min(1.0, confidence))
            
            confidence_scores.append(confidence)
        
        return confidence_scores