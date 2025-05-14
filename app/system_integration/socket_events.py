"""
Socket.IO event handlers for system integration WebSocket connections.

This module defines handlers for WebSocket events, particularly for the /system-updates namespace
used by the dashboard and system status pages.
"""

from flask_socketio import emit, join_room
from app import socketio
from app.system_integration.integration import system_integrator

@socketio.on('connect', namespace='/system-updates')
def handle_system_updates_connect():
    """Handle connection to the system-updates namespace."""
    # Log connection
    print("Client connected to system-updates namespace")
    
    # Send initial connection response
    emit('connection_response', {
        'status': 'connected',
        'message': 'Connected to system updates'
    })

@socketio.on('disconnect', namespace='/system-updates')
def handle_system_updates_disconnect():
    """Handle disconnection from the system-updates namespace."""
    print("Client disconnected from system-updates namespace")

@socketio.on('subscribe_to_updates', namespace='/system-updates')
def handle_subscribe_to_updates(data):
    """
    Handle subscription requests to various update types.
    
    Args:
        data: Dictionary containing subscription details.
              Expected to have an 'update_type' key.
    """
    update_type = data.get('update_type', 'all')
    
    if update_type == 'all':
        # Subscribe to all update types
        join_room('system_metrics')
        join_room('processed_data')
        join_room('alerts')
        join_room('correlations')
    else:
        # Subscribe to specific update type
        join_room(update_type)
    
    # Send confirmation
    emit('subscription_response', {
        'status': 'subscribed',
        'update_type': update_type
    })

@socketio.on('get_correlation_data', namespace='/system-updates')
def handle_get_correlation_data():
    """Handle requests for correlation data."""
    # Get correlator from system integrator
    correlator = system_integrator.get_component('correlator')
    
    # If there's no correlator, send an empty response
    if not correlator:
        emit('correlation_data', {
            'status': 'error',
            'message': 'Correlator component not available'
        })
        return
    
    # Get correlation data
    correlation_data = correlator.get_latest_correlations()
    
    # Send data to client
    emit('correlation_data', {
        'status': 'success',
        'data': correlation_data
    })

@socketio.on('get_correlation_insights', namespace='/system-updates')
def handle_get_correlation_insights():
    """Handle requests for correlation insights."""
    # Get correlator from system integrator
    correlator = system_integrator.get_component('correlator')
    
    # If there's no correlator, send an empty response
    if not correlator:
        emit('correlation_insight', {
            'status': 'error',
            'message': 'Correlator component not available'
        })
        return
    
    # Get correlation insights
    insights = correlator.get_insights()
    
    # Send data to client
    emit('correlation_insight', {
        'status': 'success',
        'data': insights
    }) 