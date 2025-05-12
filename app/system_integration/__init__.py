"""
System Integration Module

This module is responsible for integrating all components of the system.
"""

from flask import Blueprint

system_integration = Blueprint('system_integration', __name__)

# Import routes after Blueprint is defined to avoid circular imports
from . import routes, integration, events