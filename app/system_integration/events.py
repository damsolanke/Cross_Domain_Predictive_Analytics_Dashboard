"""
Event handling for the system integration module.

This module provides functions for emitting events to WebSocket clients
and handles event-related functionality.
"""

from app import socketio

def emit_data_update(domain, data):
    """
    Emit a data update event to connected clients.
    
    Args:
        domain: Domain name (e.g., 'weather', 'economic', etc.)
        data: Data to emit
    """
    event_name = f"{domain}_update"
    socketio.emit(event_name, data)

def emit_alert(alert_type, data):
    """
    Emit an alert event to connected clients.
    
    Args:
        alert_type: Type of alert (e.g., 'threshold', 'anomaly', etc.)
        data: Alert data
    """
    socketio.emit('alert', {
        'type': alert_type,
        'data': data,
        'timestamp': __import__('time').time()
    })