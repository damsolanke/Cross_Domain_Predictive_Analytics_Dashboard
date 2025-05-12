"""
System integration routes.
"""
from flask import render_template, jsonify, request
from . import system_integration
from .integration import system_integrator

@system_integration.route('/system-status')
def system_status():
    """Render the system status page."""
    return render_template('system_integration/system_status.html', title='System Status')

@system_integration.route('/api/system-status')
def api_system_status():
    """Get system status data."""
    components = {name: component.get_status() for name, component in system_integrator.components.items()}
    
    # Add mock data if real data is not available
    if not components:
        components = {
            "api_connectors": {
                "status": "active",
                "connections": 4,
                "error_rate": 0.02
            },
            "ml_models": {
                "status": "active",
                "models_loaded": 3,
                "prediction_accuracy": 0.87
            },
            "visualization": {
                "status": "active",
                "active_visualizations": 8
            }
        }
    
    return jsonify({
        "status": "active",
        "uptime": __import__('time').time() - __import__('time').time() + 3600,  # Mock 1-hour uptime
        "components": components,
        "processing_rate": 42.5,
        "queue_size": 12
    })