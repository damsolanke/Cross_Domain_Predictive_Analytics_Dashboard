"""
Cross-domain prediction module.
"""
import numpy as np
import time
from typing import Dict, List, Any, Optional, Tuple
from .cross_domain_correlation import CrossDomainCorrelator

class CrossDomainPredictor:
    """
    Makes predictions based on cross-domain correlations.
    """
    
    def __init__(self, correlator: CrossDomainCorrelator = None):
        """
        Initialize the cross-domain predictor.
        
        Args:
            correlator: Optional correlator instance
        """
        self.correlator = correlator or CrossDomainCorrelator()
        self.model_cache = {}
        self.predictor_fields_cache = {}  # Cache predictor fields by target
        self.prediction_cache = {}  # Cache for predictions
        self.cache_expiry = 60  # Cache expiry in seconds
        self.error = None
        
    def predict_target(self, target_domain: str, target_field: str, source_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Predict a target field based on source data from other domains.
        
        Args:
            target_domain: Domain to predict
            target_field: Field to predict
            source_data: Current data from other domains
            
        Returns:
            Dictionary with prediction information
        """
        # Check cache for recent prediction
        cache_key = (target_domain, target_field, self._get_source_data_hash(source_data))
        if cache_key in self.prediction_cache:
            timestamp, prediction = self.prediction_cache[cache_key]
            if time.time() - timestamp < self.cache_expiry:
                return prediction
                
        # Get high correlations to use as predictors
        try:
            # We need correlations to make predictions
            if not self.correlator.correlation_cache:
                self.error = "No correlation data available"
                return None
                
            # Find best predictor fields
            predictor_fields = self._find_predictor_fields(target_domain, target_field)
            if not predictor_fields:
                self.error = f"No suitable predictors found for {target_domain}.{target_field}"
                return None
                
            # Extract input values from source data
            input_values = []
            for domain, field in predictor_fields:
                if domain not in source_data or field not in source_data[domain]:
                    self.error = f"Missing predictor data: {domain}.{field}"
                    return None
                    
                input_values.append(source_data[domain][field])
                
            # Use a simple weighted average as prediction
            # In a real implementation, this would use a proper ML model
            weights = [abs(field_info['correlation']) for field_info in predictor_fields]
            weight_sum = sum(weights)
            
            if weight_sum == 0:
                normalized_weights = [1.0 / len(weights)] * len(weights)
            else:
                normalized_weights = [w / weight_sum for w in weights]
                
            prediction = sum(v * w for v, w in zip(input_values, normalized_weights))
            
            # Calculate confidence based on correlation strength
            confidence = min(0.95, sum(abs(field_info['correlation']) for field_info in predictor_fields) / len(predictor_fields))
            
            result = {
                'value': prediction,
                'confidence': confidence,
                'predictors': predictor_fields,
                'timestamp': time.time()
            }
            
            # Cache the prediction
            self.prediction_cache[cache_key] = (time.time(), result)
            
            return result
            
        except Exception as e:
            self.error = f"Prediction error: {str(e)}"
            return None
    
    def _get_source_data_hash(self, source_data: Dict[str, Any]) -> str:
        """Create a simple hash of source data for caching purposes"""
        hash_str = ""
        for domain in sorted(source_data.keys()):
            domain_data = source_data[domain]
            for field in sorted(domain_data.keys()):
                hash_str += f"{domain}-{field}-{domain_data[field]}|"
        return hash_str
            
    def _find_predictor_fields(self, target_domain: str, target_field: str) -> List[Dict[str, Any]]:
        """
        Find the best fields to use as predictors.
        
        Args:
            target_domain: Target domain name
            target_field: Target field name
            
        Returns:
            List of predictor field information
        """
        # Check cache first
        cache_key = (target_domain, target_field)
        if cache_key in self.predictor_fields_cache:
            timestamp, fields = self.predictor_fields_cache[cache_key]
            if time.time() - timestamp < self.cache_expiry:
                return fields
        
        # Look for fields with high correlation to target
        result = []
        
        for key, correlation in self.correlator.correlation_cache.items():
            # Parse the correlation key
            try:
                domain1_field, domain2_field = key.split('_')
                domain1, field1 = domain1_field.split('.')
                domain2, field2 = domain2_field.split('.')
                
                # Check if this correlation involves our target
                if (domain1 == target_domain and field1 == target_field):
                    result.append({
                        'domain': domain2,
                        'field': field2,
                        'correlation': correlation
                    })
                elif (domain2 == target_domain and field2 == target_field):
                    result.append({
                        'domain': domain1,
                        'field': field1,
                        'correlation': correlation
                    })
            except ValueError:
                # Skip malformed correlation keys
                continue
                
        # Sort by absolute correlation value
        result.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        # Take top 3 or fewer if not enough available
        final_result = result[:3]
        
        # Cache the result
        self.predictor_fields_cache[cache_key] = (time.time(), final_result)
        
        return final_result
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of the predictor.
        
        Returns:
            Status information dictionary
        """
        return {
            'model_count': len(self.model_cache),
            'prediction_cache_size': len(self.prediction_cache),
            'predictor_fields_cache_size': len(self.predictor_fields_cache),
            'correlator_status': self.correlator.get_status() if self.correlator else None,
            'error': self.error
        }
        
    def what_if_scenario(self, scenario_data: Dict[str, Dict[str, Any]], target_domain: str, target_field: str) -> Optional[Dict[str, Any]]:
        """
        Run a what-if scenario to predict outcomes with modified input data.
        
        Args:
            scenario_data: Modified domain data for the scenario
            target_domain: Domain to predict
            target_field: Field to predict
            
        Returns:
            Dictionary with prediction information
        """
        return self.predict_target(target_domain, target_field, scenario_data)
        
    def compare_scenarios(self, baseline_data: Dict[str, Dict[str, Any]], scenario_data: Dict[str, Dict[str, Any]], 
                          target_domain: str, target_field: str) -> Optional[Dict[str, Any]]:
        """
        Compare a what-if scenario to baseline data.
        
        Args:
            baseline_data: Current domain data
            scenario_data: Modified domain data for the scenario
            target_domain: Domain to predict
            target_field: Field to predict
            
        Returns:
            Dictionary with comparison information
        """
        baseline_prediction = self.predict_target(target_domain, target_field, baseline_data)
        scenario_prediction = self.predict_target(target_domain, target_field, scenario_data)
        
        if not baseline_prediction or not scenario_prediction:
            return None
            
        return {
            'baseline': baseline_prediction['value'],
            'scenario': scenario_prediction['value'],
            'difference': scenario_prediction['value'] - baseline_prediction['value'],
            'percent_change': (scenario_prediction['value'] - baseline_prediction['value']) / baseline_prediction['value'] * 100 if baseline_prediction['value'] != 0 else float('inf'),
            'confidence': min(baseline_prediction['confidence'], scenario_prediction['confidence']),
            'timestamp': time.time()
        }