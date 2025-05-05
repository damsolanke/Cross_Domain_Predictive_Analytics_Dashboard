"""
System integration module for the Cross-Domain Predictive Analytics Dashboard.
"""

from flask import Blueprint

system_integration = Blueprint('system_integration', __name__)

# Import routes after Blueprint is defined to avoid circular imports
from . import routes