"""
Base model class for ML models
"""
import time
import logging
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union

logger = logging.getLogger(__name__)

class BaseModel(ABC):
    """
    Abstract base class for all ML models.
    Provides common functionality for model integration.
    """
    component_type = 'ml_models'  # For system integration
    
    def __init__(self, name: str, description: str, 
                data_sources: List[str], prediction_types: List[str]):
        """
        Initialize the model
        
        Args:
            name: Human-readable name for this model
            description: Description of the model
            data_sources: List of data sources this model can process
            prediction_types: List of prediction types this model can generate
        """
        self.name = name
        self.description = description
        self.data_sources = data_sources
        self.prediction_types = prediction_types
        self.status = "initialized"
        self.error = None
        self.last_prediction_time = 0
        self.prediction_count = 0
        
        # Model performance metrics
        self.metrics = {
            'accuracy': 0.0,
            'mean_absolute_error': 0.0,
            'confidence_avg': 0.0,
            'prediction_latency_ms': 0.0
        }
    
    def can_process(self, data_source: str) -> bool:
        """
        Check if this model can process data from the given source
        
        Args:
            data_source: Source identifier
            
        Returns:
            True if this model can process the data source
        """
        return data_source in self.data_sources
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and generate predictions
        
        Args:
            data: Input data dictionary
            
        Returns:
            Dictionary containing predictions and metadata
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of this model
        
        Returns:
            Status information dictionary
        """
        return {
            'status': self.status,
            'metrics': self.metrics,
            'last_prediction': self.last_prediction_time,
            'prediction_count': self.prediction_count,
            'error': str(self.error) if self.error else None
        }
    
    def _update_status(self, status: str, error: Optional[Exception] = None) -> None:
        """
        Update model status
        
        Args:
            status: New status string
            error: Optional exception if an error occurred
        """
        self.status = status
        self.error = error
        logger.info(f"Model {self.name} status: {status}")
        if error:
            logger.error(f"Model {self.name} error: {error}")
    
    def _update_metrics(self, metrics_update: Dict[str, float]) -> None:
        """
        Update model performance metrics
        
        Args:
            metrics_update: Dictionary with metric updates
        """
        self.metrics.update(metrics_update)
    
    def _log_prediction(self, latency_ms: float) -> None:
        """
        Log a prediction event
        
        Args:
            latency_ms: Prediction latency in milliseconds
        """
        self.last_prediction_time = time.time()
        self.prediction_count += 1
        
        # Update latency metric with exponential moving average
        alpha = 0.1  # Smoothing factor
        old_latency = self.metrics.get('prediction_latency_ms', latency_ms)
        self.metrics['prediction_latency_ms'] = old_latency * (1 - alpha) + latency_ms * alpha
    
    def _calculate_confidence(self, prediction: Any, uncertainty: Optional[float] = None) -> float:
        """
        Calculate confidence score for a prediction
        
        Args:
            prediction: The prediction value
            uncertainty: Optional uncertainty measure
            
        Returns:
            Confidence score between 0 and 1
        """
        # Default implementation uses a fixed confidence or derives from uncertainty if provided
        if uncertainty is not None:
            # Convert uncertainty to confidence (higher uncertainty = lower confidence)
            return max(0.0, min(1.0, 1.0 - uncertainty))
        
        # Default confidence (could be overridden by subclasses)
        return 0.85