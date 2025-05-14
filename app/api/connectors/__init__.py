"""
API Connectors for external data sources
"""
import importlib
import os
import pkgutil
from typing import Dict, List, Optional, Any

# Dictionary to store connector instances
_connectors: Dict[str, Any] = {}

def register_connector(connector_id: str, connector_instance: Any) -> None:
    """Register a connector with the system"""
    global _connectors
    _connectors[connector_id] = connector_instance

def get_connector(connector_id: str) -> Optional[Any]:
    """Get a registered connector by ID"""
    return _connectors.get(connector_id)

def list_connectors() -> List[Dict[str, Any]]:
    """List all registered connectors with their metadata"""
    return [
        {
            'id': connector_id,
            'name': connector.name,
            'description': connector.description,
            'status': connector.get_status(),
            'last_update': connector.last_update_timestamp
        }
        for connector_id, connector in _connectors.items()
    ]

# Auto-discover and register connectors
def _discover_connectors() -> None:
    """Discover and register connectors from the connectors package"""
    # Get the directory of this package
    package_dir = os.path.dirname(__file__)
    
    # Iterate through all modules in this package
    for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
        if not is_pkg and module_name != '__init__':
            try:
                # Import the module
                module = importlib.import_module(f'.{module_name}', __package__)
                
                # Look for connector classes
                for attr_name in dir(module):
                    if attr_name.endswith('Connector') and attr_name != 'BaseConnector':
                        connector_class = getattr(module, attr_name)
                        
                        # Create an instance and register it
                        connector_id = module_name.replace('_', '-')
                        connector = connector_class()
                        register_connector(connector_id, connector)
            except Exception as e:
                print(f"Error loading connector module {module_name}: {e}")

# Import connectors explicitly to ensure they're loaded
from app.api.connectors.base_connector import BaseConnector
from app.api.connectors.weather_connector import WeatherConnector
from app.api.connectors.economic_connector import EconomicConnector
from app.api.connectors.social_media_connector import SocialMediaConnector
from app.api.connectors.transportation_connector import TransportationConnector

# Register specific connectors
register_connector('weather', WeatherConnector())
register_connector('economic', EconomicConnector())
register_connector('social-media', SocialMediaConnector())
register_connector('transportation', TransportationConnector())