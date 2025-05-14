"""
ML models package for the predictive analytics dashboard
"""
import importlib
import os
import pkgutil
from typing import Dict, List, Any, Optional

# Dictionary to store model instances
_models: Dict[str, Any] = {}

def register_model(model_id: str, model_instance: Any) -> None:
    """Register a model with the system"""
    global _models
    _models[model_id] = model_instance

def get_model(model_id: str) -> Optional[Any]:
    """Get a registered model by ID"""
    return _models.get(model_id)

def list_models() -> List[Dict[str, Any]]:
    """List all registered models with their metadata"""
    return [
        {
            'id': model_id,
            'name': model.name,
            'description': model.description,
            'data_sources': model.data_sources,
            'prediction_types': model.prediction_types
        }
        for model_id, model in _models.items()
    ]

# Import models explicitly
from app.models.base_model import BaseModel
from app.models.weather_prediction import WeatherPredictionModel
from app.models.economic_prediction import EconomicPredictionModel
from app.models.transportation_prediction import TransportationPredictionModel
from app.models.cross_domain_model import CrossDomainModel

# Register models
register_model('weather', WeatherPredictionModel())
register_model('economic', EconomicPredictionModel())
register_model('transportation', TransportationPredictionModel())
register_model('cross-domain', CrossDomainModel())