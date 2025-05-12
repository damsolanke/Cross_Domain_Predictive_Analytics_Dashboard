"""
Routes for the system integration module.
"""

from flask import jsonify
from . import system_integration

@system_integration.route('/system-status')
def system_status():
    """Get system status information."""
    from app.system_integration.integration import system_integrator
    
    pipeline = system_integrator.data_pipeline
    health = pipeline.check_system_health() if pipeline else {'status': 'not_initialized'}
    
    return jsonify({
        'status': 'operational',
        'health': health,
        'timestamp': pipeline.get_current_timestamp() if pipeline else None
    })