"""
API module for the Cross-Domain Predictive Analytics Dashboard.
"""

from flask import Blueprint

api = Blueprint('api', __name__)

# Import routes after Blueprint is defined to avoid circular imports
from . import routes