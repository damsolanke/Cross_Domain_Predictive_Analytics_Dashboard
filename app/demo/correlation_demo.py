"""
Demo controller for cross-domain correlation visualization.
"""

from flask import Blueprint, render_template, jsonify, request
from datetime import datetime, timedelta
import threading
import time

from app.demo.cross_domain_generator import CrossDomainGenerator
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
from app.system_integration.routes import emit_data_update, emit_alert

# Create Blueprint
correlation_demo = Blueprint('correlation_demo', __name__, url_prefix='/demo/correlation')

# Global objects
generator = CrossDomainGenerator(seed=42)
correlator = CrossDomainCorrelator()
demo_thread = None
demo_running = False

@correlation_demo.route('/')
def index():
    """Render the correlation demo page."""
    return render_template('demo/correlation_demo.html', title='Cross-Domain Correlation Demo')

@correlation_demo.route('/start', methods=['POST'])
def start_demo():
    """Start the correlation demo."""
    global demo_thread, demo_running
    
    if demo_running:
        return jsonify({'status': 'error', 'message': 'Demo already running'})
    
    # Get parameters from request
    data = request.json or {}
    interval_seconds = data.get('interval_seconds', 5)
    
    # Start demo thread
    demo_running = True
    demo_thread = threading.Thread(target=run_demo, args=(interval_seconds,))
    demo_thread.daemon = True
    demo_thread.start()
    
    return jsonify({'status': 'success', 'message': 'Demo started'})

@correlation_demo.route('/stop', methods=['POST'])
def stop_demo():
    """Stop the correlation demo."""
    global demo_running
    
    if not demo_running:
        return jsonify({'status': 'error', 'message': 'Demo not running'})
    
    # Stop demo thread
    demo_running = False
    
    return jsonify({'status': 'success', 'message': 'Demo stopping, please wait...'})

@correlation_demo.route('/status')
def demo_status():
    """Get demo status."""
    return jsonify({
        'running': demo_running,
        'generator': {
            'active_events': generator.get_active_events(),
            'correlation_info': generator.get_correlation_info()
        },
        'correlator': {
            'insight_count': len(correlator.insights),
            'time_window_hours': correlator.time_window.total_seconds() // 3600
        }
    })

@correlation_demo.route('/force_event', methods=['POST'])
def force_event():
    """Force a specific event to occur."""
    data = request.json or {}
    event_name = data.get('event_name')
    
    if not event_name:
        return jsonify({'status': 'error', 'message': 'Event name required'})
    
    # Find the event definition
    event_def = None
    for event in generator.events:
        if event['name'] == event_name:
            event_def = event
            break
    
    if not event_def:
        return jsonify({'status': 'error', 'message': f'Event "{event_name}" not found'})
    
    # Create and add the event
    now = datetime.now()
    event = {
        'name': event_def['name'],
        'domain': event_def['domain'],
        'variables': event_def['variables'].copy(),
        'end_time': now + timedelta(hours=event_def['duration']),
        'start_time': now
    }
    generator.active_events.append(event)
    
    return jsonify({
        'status': 'success', 
        'message': f'Event "{event_name}" triggered',
        'event': {
            'name': event['name'],
            'domain': event['domain'],
            'variables': event['variables'],
            'duration_hours': event_def['duration']
        }
    })

@correlation_demo.route('/set_time_window', methods=['POST'])
def set_time_window():
    """Set the correlation time window."""
    data = request.json or {}
    hours = data.get('hours', 24)
    
    try:
        hours = int(hours)
        if hours < 1 or hours > 168:  # 1 hour to 7 days
            return jsonify({'status': 'error', 'message': 'Hours must be between 1 and 168'})
        
        correlator.set_time_window(hours=hours)
        return jsonify({'status': 'success', 'message': f'Time window set to {hours} hours'})
    
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid hours value'})

def process_data(data):
    """
    Process generated data and feed to correlator.
    
    Args:
        data (dict): Generated data for all domains
    """
    # Process each domain
    for domain, domain_data in data.items():
        # Extract timestamp
        timestamp_str = domain_data.get('timestamp')
        
        # Send data to correlator
        correlator.add_data(domain, domain_data)
        
        # Emit real-time update to clients
        emit_data_update('domain_data', {
            'domain': domain,
            'data': domain_data,
            'timestamp': timestamp_str
        })
    
    # Periodically calculate correlations and generate insights
    current_time = time.time()
    if current_time % 30 < 5:  # About every 30 seconds
        # Calculate correlations
        correlator.calculate_correlations()
        
        # Generate insights
        insights = correlator.generate_insights()
        
        # Detect anomalies
        anomalies = correlator.detect_anomalies()
        
        # Emit correlation data
        viz_data = correlator.get_correlation_data_for_visualization()
        emit_data_update('correlation_data', viz_data)
        
        # Emit insights
        for insight in insights:
            if 'correlation_value' in insight and abs(insight['correlation_value']) > 0.7:
                # Create alert for significant insights
                alert = {
                    'type': 'correlation_insight',
                    'level': 'info',
                    'message': insight['description'],
                    'data': insight,
                    'timestamp': datetime.now().isoformat()
                }
                emit_alert(alert)
            
            # Emit insight update
            emit_data_update('correlation_insight', insight)
        
        # Emit anomalies
        for anomaly in anomalies:
            # Create alert for anomalies
            alert = {
                'type': 'correlation_anomaly',
                'level': 'warning',
                'message': anomaly['description'],
                'data': anomaly,
                'timestamp': datetime.now().isoformat()
            }
            emit_alert(alert)
            
            # Emit anomaly update
            emit_data_update('correlation_anomaly', anomaly)

def run_demo(interval_seconds=5):
    """
    Run the correlation demo.
    
    Args:
        interval_seconds (int): Interval between data points in seconds
    """
    global demo_running
    
    print(f"Starting correlation demo with interval={interval_seconds}s")
    
    try:
        while demo_running:
            # Generate data
            data = generator.generate_data()
            
            # Process data
            process_data(data)
            
            # Sleep until next interval
            time.sleep(interval_seconds)
    
    except Exception as e:
        print(f"Error in correlation demo: {e}")
    
    finally:
        demo_running = False
        print("Correlation demo stopped")