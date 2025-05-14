"""
Economic prediction model for forecasting economic indicators
"""
import time
import random
import math
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from app.models.base_model import BaseModel

class EconomicPredictionModel(BaseModel):
    """Model for predicting economic indicators based on historical data"""
    
    def __init__(self):
        """Initialize the economic prediction model"""
        super().__init__(
            name="Economic Indicator Prediction",
            description="Predicts economic indicators including inflation, GDP, stock indices, and exchange rates",
            data_sources=["economic"],
            prediction_types=["inflation", "gdp", "stock_market", "interest_rates", "currency"]
        )
        # Initialize model-specific parameters
        self.model_coefficients = {
            'inflation': {
                'interest_rate_effect': 0.4,  # Higher rates -> lower inflation
                'gdp_effect': 0.3,  # Higher GDP -> higher inflation
                'unemployment_effect': -0.2,  # Higher unemployment -> lower inflation
                'momentum': 0.7  # Inflation persistence
            },
            'gdp': {
                'interest_rate_effect': -0.3,  # Higher rates -> lower GDP
                'inflation_effect': -0.2,  # Higher inflation -> lower GDP
                'global_economy_effect': 0.5,  # Global growth impacts local
                'momentum': 0.6  # GDP growth persistence
            },
            'stock_market': {
                'interest_rate_effect': -0.4,  # Higher rates -> lower stock prices
                'gdp_effect': 0.6,  # Higher GDP -> higher stock prices
                'earnings_effect': 0.7,  # Higher earnings -> higher stock prices
                'momentum': 0.3  # Stock market momentum factor
            }
        }
        
        # Confidence parameters
        self.base_confidence = 0.75
        self.confidence_decay = 0.1  # How much confidence decays per period
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process economic data and generate predictions
        
        Args:
            data: Economic data with historical patterns
            
        Returns:
            Dictionary with economic predictions
        """
        start_time = time.time()
        
        try:
            self._update_status("processing")
            
            # Extract relevant data
            indicator = data.get('indicator', 'inflation')
            country = data.get('country', 'US')
            
            # Extract historical data
            historical_data = self._extract_historical_data(data)
            
            # Get prediction periods
            prediction_periods = self._get_prediction_periods(indicator)
            
            # Generate predictions
            predictions = self._generate_predictions(indicator, historical_data, prediction_periods)
            
            # Calculate confidence scores
            confidence_scores = self._calculate_confidence_scores(indicator, len(prediction_periods))
            
            # Add confidence scores to predictions
            for i, prediction in enumerate(predictions):
                prediction['confidence'] = confidence_scores[i]
            
            # Calculate prediction latency
            latency_ms = (time.time() - start_time) * 1000
            self._log_prediction(latency_ms)
            
            # Return predictions with metadata
            result = {
                'country': country,
                'indicator': indicator,
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
    
    def _extract_historical_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract historical data from input data"""
        # Look for data in standard format
        if 'data' in data and isinstance(data['data'], list):
            return data['data']
        
        # If we can't find historical data, create a minimal placeholder
        return [
            {
                'date': (datetime.now() - timedelta(days=30)).isoformat(),
                'value': random.uniform(1.0, 5.0)
            },
            {
                'date': datetime.now().isoformat(),
                'value': random.uniform(1.0, 5.0)
            }
        ]
    
    def _get_prediction_periods(self, indicator: str) -> List[str]:
        """
        Determine appropriate prediction periods based on indicator type
        
        Args:
            indicator: Type of economic indicator
            
        Returns:
            List of prediction period timestamps
        """
        periods = []
        now = datetime.now()
        
        if indicator in ['inflation', 'gdp']:
            # Quarterly predictions for 2 years
            for i in range(1, 9):
                periods.append((now + timedelta(days=i*90)).isoformat())
        
        elif indicator in ['interest_rates']:
            # Monthly for 6 months, then quarterly
            for i in range(1, 7):
                periods.append((now + timedelta(days=i*30)).isoformat())
            for i in range(3, 9):
                periods.append((now + timedelta(days=i*90)).isoformat())
        
        elif indicator in ['stock_market', 'currency']:
            # Daily for 5 days, weekly for 4 weeks, monthly for 6 months
            for i in range(1, 6):
                periods.append((now + timedelta(days=i)).isoformat())
            for i in range(1, 5):
                periods.append((now + timedelta(weeks=i)).isoformat())
            for i in range(1, 7):
                periods.append((now + timedelta(days=i*30)).isoformat())
        
        else:
            # Default: monthly for a year
            for i in range(1, 13):
                periods.append((now + timedelta(days=i*30)).isoformat())
        
        return periods
    
    def _generate_predictions(self, indicator: str, historical_data: List[Dict[str, Any]], 
                             prediction_periods: List[str]) -> List[Dict[str, Any]]:
        """
        Generate predictions for the specified periods
        
        Args:
            indicator: Type of economic indicator
            historical_data: List of historical data points
            prediction_periods: List of prediction period timestamps
            
        Returns:
            List of prediction dictionaries
        """
        predictions = []
        
        # Get the most recent historical values
        latest_value = historical_data[-1]['value'] if historical_data else 2.0
        
        # Get prediction method based on indicator type
        if indicator == 'inflation':
            values = self._predict_inflation(latest_value, len(prediction_periods))
        elif indicator == 'gdp':
            values = self._predict_gdp(latest_value, len(prediction_periods))
        elif indicator == 'stock_market':
            values = self._predict_stock_market(latest_value, len(prediction_periods))
        elif indicator == 'interest_rates':
            values = self._predict_interest_rates(latest_value, len(prediction_periods))
        elif indicator == 'currency':
            values = self._predict_currency(latest_value, len(prediction_periods))
        else:
            # Default prediction method
            values = self._predict_generic(latest_value, len(prediction_periods))
        
        # Create prediction objects
        for i, period in enumerate(prediction_periods):
            predictions.append({
                'period': period,
                'value': round(values[i], 2)
            })
        
        return predictions
    
    def _predict_inflation(self, latest_value: float, periods: int) -> List[float]:
        """
        Predict inflation rates
        
        Args:
            latest_value: Most recent inflation rate
            periods: Number of periods to predict
            
        Returns:
            List of predicted inflation rates
        """
        predictions = []
        current = latest_value
        
        # Model coefficients
        momentum = self.model_coefficients['inflation']['momentum']
        noise_level = 0.3
        
        # Target inflation assuming central bank targets around 2%
        target_inflation = 2.0
        
        for i in range(periods):
            # Inflation tends to revert to target
            reversion_strength = 0.1 * (i + 1) / periods  # Stronger reversion over time
            target_pull = reversion_strength * (target_inflation - current)
            
            # Add some momentum (inflation persistence)
            momentum_effect = momentum * (current - latest_value)
            
            # Add random noise
            noise = random.uniform(-noise_level, noise_level)
            
            # Calculate new inflation value
            new_value = current + target_pull + momentum_effect + noise
            
            # Ensure inflation stays in reasonable bounds
            new_value = max(0.0, min(15.0, new_value))
            
            predictions.append(new_value)
            current = new_value
        
        return predictions
    
    def _predict_gdp(self, latest_value: float, periods: int) -> List[float]:
        """
        Predict GDP growth rates
        
        Args:
            latest_value: Most recent GDP growth rate
            periods: Number of periods to predict
            
        Returns:
            List of predicted GDP growth rates
        """
        predictions = []
        current = latest_value
        
        # Model coefficients
        momentum = self.model_coefficients['gdp']['momentum']
        noise_level = 0.4
        
        # Long-term growth trend around 2-3%
        trend_growth = 2.5
        
        for i in range(periods):
            # GDP growth tends to revert to trend
            reversion_strength = 0.15 * (i + 1) / periods  # Stronger reversion over time
            trend_pull = reversion_strength * (trend_growth - current)
            
            # Add some cyclicality (business cycle)
            cycle_position = (i % 20) / 20  # Position in a 5-year cycle
            cycle_effect = 1.0 * math.sin(2 * math.pi * cycle_position)
            
            # Add momentum
            momentum_effect = momentum * (current - latest_value)
            
            # Add random shocks
            shock = random.uniform(-noise_level, noise_level)
            
            # Calculate new GDP value
            new_value = current + trend_pull + cycle_effect * 0.2 + momentum_effect + shock
            
            # Ensure GDP stays in reasonable bounds
            new_value = max(-8.0, min(10.0, new_value))
            
            predictions.append(new_value)
            current = new_value
        
        return predictions
    
    def _predict_stock_market(self, latest_value: float, periods: int) -> List[float]:
        """
        Predict stock market index values
        
        Args:
            latest_value: Most recent index value
            periods: Number of periods to predict
            
        Returns:
            List of predicted index values
        """
        predictions = []
        current = latest_value
        
        # Assumptions for stock market model
        annual_growth_rate = 0.08  # 8% average annual return
        volatility = 0.02  # Initial volatility
        
        for i in range(periods):
            # Calculate period length in years (assuming periods are roughly equidistant)
            if periods <= 15:  # For short-term forecasts
                period_years = 1/252  # Daily (trading days per year)
            elif periods <= 25:
                period_years = 1/52  # Weekly
            else:
                period_years = 1/12  # Monthly
            
            # Expected return for this period
            expected_return = current * (math.pow(1 + annual_growth_rate, period_years) - 1)
            
            # Increasing volatility for further predictions
            period_volatility = volatility * math.sqrt(period_years) * (1 + i/10)
            
            # Lognormal random shock (common in stock price modeling)
            random_return = random.normalvariate(0, period_volatility) * current
            
            # Calculate new value
            new_value = current + expected_return + random_return
            
            # Ensure value stays positive
            new_value = max(0.1 * latest_value, new_value)
            
            predictions.append(new_value)
            current = new_value
        
        return predictions
    
    def _predict_interest_rates(self, latest_value: float, periods: int) -> List[float]:
        """
        Predict interest rates
        
        Args:
            latest_value: Most recent interest rate
            periods: Number of periods to predict
            
        Returns:
            List of predicted interest rates
        """
        predictions = []
        current = latest_value
        
        # Interest rate model parameters
        long_term_rate = 3.0  # Neutral rate assumption
        max_step = 0.25  # Maximum change per period
        volatility = 0.1  # Noise level
        
        for i in range(periods):
            # Interest rates tend to move in small steps
            # and revert to a long-term neutral rate
            reversion = 0.1 * (long_term_rate - current)
            
            # Add persistence (central banks move gradually)
            if i > 0:
                momentum = 0.3 * (predictions[i-1] - current)
            else:
                momentum = 0
            
            # Random component (economic surprises)
            noise = random.uniform(-volatility, volatility)
            
            # Calculate raw change
            rate_change = reversion + momentum + noise
            
            # Limit step size
            rate_change = max(-max_step, min(max_step, rate_change))
            
            # Calculate new rate
            new_rate = current + rate_change
            
            # Ensure rate stays non-negative and reasonable
            new_rate = max(0.0, min(15.0, new_rate))
            
            predictions.append(new_rate)
            current = new_rate
        
        return predictions
    
    def _predict_currency(self, latest_value: float, periods: int) -> List[float]:
        """
        Predict currency exchange rates
        
        Args:
            latest_value: Most recent exchange rate
            periods: Number of periods to predict
            
        Returns:
            List of predicted exchange rates
        """
        predictions = []
        current = latest_value
        
        # Currency model parameters
        volatility = 0.005  # Daily volatility
        annual_drift = 0.01  # Small drift (purchasing power parity)
        mean_reversion = 0.01  # Slow reversion to fundamentals
        
        # Find appropriate period length
        if periods <= 15:
            period_type = 'daily'
        elif periods <= 25:
            period_type = 'weekly'
        else:
            period_type = 'monthly'
        
        for i in range(periods):
            # Scale volatility by period length
            if period_type == 'daily':
                scaled_volatility = volatility
                period_drift = annual_drift / 252
            elif period_type == 'weekly':
                scaled_volatility = volatility * math.sqrt(5)
                period_drift = annual_drift / 52
            else:  # monthly
                scaled_volatility = volatility * math.sqrt(21)
                period_drift = annual_drift / 12
            
            # Add some mean reversion (currencies tend to revert to purchasing power parity)
            reversion = mean_reversion * (latest_value - current)
            
            # Random component (market surprises)
            noise = random.normalvariate(0, scaled_volatility) * current
            
            # Calculate new rate
            new_rate = current * (1 + period_drift) + reversion + noise
            
            # Ensure rate stays positive and reasonable
            new_rate = max(0.5 * latest_value, min(2.0 * latest_value, new_rate))
            
            predictions.append(new_rate)
            current = new_rate
        
        return predictions
    
    def _predict_generic(self, latest_value: float, periods: int) -> List[float]:
        """
        Generic prediction method for unsupported indicators
        
        Args:
            latest_value: Most recent value
            periods: Number of periods to predict
            
        Returns:
            List of predicted values
        """
        predictions = []
        current = latest_value
        
        for i in range(periods):
            # Simple random walk with slight upward bias
            change = random.normalvariate(0.01, 0.05) * current
            new_value = current + change
            
            # Ensure value stays positive
            new_value = max(0.1, new_value)
            
            predictions.append(new_value)
            current = new_value
        
        return predictions
    
    def _calculate_confidence_scores(self, indicator: str, periods: int) -> List[float]:
        """
        Calculate confidence scores for predictions
        
        Args:
            indicator: Type of economic indicator
            periods: Number of periods to predict
            
        Returns:
            List of confidence scores
        """
        confidence_scores = []
        
        # Different base confidence levels by indicator type
        if indicator in ['inflation', 'interest_rates']:
            base = 0.8  # Higher confidence (more stable indicators)
        elif indicator in ['gdp']:
            base = 0.75  # Medium confidence
        elif indicator in ['stock_market', 'currency']:
            base = 0.6  # Lower confidence (more volatile)
        else:
            base = 0.7  # Default
        
        # Confidence declines over time
        for i in range(periods):
            period_confidence = base - (self.confidence_decay * i / (periods / 2))
            
            # Ensure confidence stays within reasonable bounds
            confidence = max(0.3, min(0.95, period_confidence))
            confidence_scores.append(round(confidence, 2))
        
        return confidence_scores