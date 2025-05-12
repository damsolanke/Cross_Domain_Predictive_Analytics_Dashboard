"""
Visualization components for the dashboard
"""
import importlib
import os
import pkgutil
from typing import Dict, List, Any, Optional

# Dictionary to store visualization formatter instances
_formatters: Dict[str, Any] = {}

def register_formatter(formatter_id: str, formatter_instance: Any) -> None:
    """Register a visualization formatter with the system"""
    global _formatters
    _formatters[formatter_id] = formatter_instance

def get_formatter(formatter_id: str) -> Optional[Any]:
    """Get a registered formatter by ID"""
    return _formatters.get(formatter_id)

def list_formatters() -> List[Dict[str, Any]]:
    """List all registered formatters with their metadata"""
    return [
        {
            'id': formatter_id,
            'name': formatter.name,
            'description': formatter.description,
            'visualization_types': formatter.visualization_types,
            'data_types': formatter.data_types
        }
        for formatter_id, formatter in _formatters.items()
    ]

# Import formatters explicitly
from app.visualizations.base_formatter import BaseFormatter
from app.visualizations.time_series_formatter import TimeSeriesFormatter
from app.visualizations.geospatial_formatter import GeospatialFormatter
from app.visualizations.correlation_formatter import CorrelationFormatter
from app.visualizations.dashboard_formatter import DashboardFormatter

# Register formatters
register_formatter('time-series', TimeSeriesFormatter())
register_formatter('geospatial', GeospatialFormatter())
register_formatter('correlation', CorrelationFormatter())
register_formatter('dashboard', DashboardFormatter())