from flask import render_template, request, jsonify, redirect, url_for
from . import main
from app.system_integration.integration import system_integrator
from app.demo.data_generator import demo_generator
from app.main.analytics_controller import analytics

@main.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', title='Cross-Domain Predictive Analytics Dashboard')

@main.route('/demo/control', methods=['GET', 'POST'])
def demo_control():
    """Control demo data generation"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'start':
            interval = int(request.form.get('interval', 30))
            scenario = request.form.get('scenario', 'baseline')
            demo_generator.start_generation(interval, scenario)
            return jsonify({'status': 'started', 'interval': interval, 'scenario': scenario})
        
        elif action == 'stop':
            demo_generator.stop_generation()
            return jsonify({'status': 'stopped'})
        
        elif action == 'scenario':
            scenario = request.form.get('scenario', 'baseline')
            demo_generator.set_scenario(scenario)
            return jsonify({'status': 'scenario_changed', 'scenario': scenario})
        
        elif action == 'generate':
            scenario = request.form.get('scenario')
            demo_generator.generate_single_update(scenario)
            return jsonify({'status': 'generated'})
    
    # GET request - show control panel
    scenarios = demo_generator.scenarios
    return render_template('demo_control.html', 
                         title='Demo Control',
                         scenarios=scenarios,
                         is_generating=demo_generator.is_generating,
                         active_scenario=demo_generator.active_scenario)

@main.route('/dashboard')
def dashboard():
    """Main dashboard view"""
    return render_template('dashboard.html', title='Analytics Dashboard')

@main.route('/nlq')
def natural_language_query():
    """Redirect to the dedicated NLQ module"""
    return redirect(url_for('nlq_routes.index'))

@main.route('/api/dashboard/data')
def dashboard_data():
    """API endpoint for dashboard data"""
    # Get processed data from the pipeline through the system integrator
    pipeline = system_integrator.data_pipeline
    processed_data = pipeline.get_processed_data(limit=50)
    
    # Organize by domain
    organized_data = {
        'weather': [],
        'economic': [],
        'transportation': [],
        'social-media': [],
        'cross-domain': []
    }
    
    for item in processed_data:
        source = item.get('source', '')
        if source in organized_data:
            organized_data[source].append(item)
    
    # Add system health information
    health = pipeline.check_system_health()
    
    return jsonify({
        'data': organized_data,
        'health': health,
        'timestamp': pipeline.get_current_timestamp()
    })