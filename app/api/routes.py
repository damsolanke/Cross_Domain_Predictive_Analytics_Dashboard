"""
API routes for the Cross-Domain Predictive Analytics Dashboard.
"""

from flask import jsonify
from . import api

@api.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'OK'})