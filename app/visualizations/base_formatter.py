"""
Base visualization formatter for converting data to visualization-ready formats
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseFormatter(ABC):
    """
    Abstract base class for all visualization formatters.
    """
    component_type = 'visualization_components'  # For system integration
    
    def __init__(self, name: str, description: str, 
                visualization_types: List[str], data_types: List[str]):
        """
        Initialize the formatter
        
        Args:
            name: Human-readable name for this formatter
            description: Description of the formatter
            visualization_types: List of visualization types this formatter supports
            data_types: List of data types this formatter can process
        """
        self.name = name
        self.description = description
        self.visualization_types = visualization_types
        self.data_types = data_types
        self.error = None
    
    def can_format(self, data_type: str, visualization_type: str) -> bool:
        """
        Check if this formatter can handle the given data and visualization types
        
        Args:
            data_type: Type of data to format
            visualization_type: Type of visualization to format for
            
        Returns:
            True if this formatter can handle the request
        """
        return data_type in self.data_types and visualization_type in self.visualization_types
    
    @abstractmethod
    def format(self, data: Dict[str, Any], visualization_type: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format data for visualization
        
        Args:
            data: Input data to format
            visualization_type: Target visualization type
            options: Optional formatting options
            
        Returns:
            Formatted data ready for visualization
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of this formatter
        
        Returns:
            Status information dictionary
        """
        return {
            'name': self.name,
            'visualization_types': self.visualization_types,
            'data_types': self.data_types,
            'error': str(self.error) if self.error else None
        }