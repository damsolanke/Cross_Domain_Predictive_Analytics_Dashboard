from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from . import main
from app.system_integration.integration import system_integrator
from app.demo.data_generator import demo_generator
from app.main.analytics_controller import analytics
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
from app.system_integration.cross_domain_prediction import CrossDomainPredictor
import time

# Cache for dashboard data
dashboard_data_cache = {}
dashboard_cache_expires = 30  # seconds

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
def nlq():
    """Natural language query interface"""
    return render_template('nlq.html', title='Natural Language Queries')

@main.route('/correlation')
def correlation():
    """Cross-domain correlation analysis page"""
    return render_template('correlation.html', title='Cross-Domain Correlation Analysis')

@main.route('/use-cases/supply-chain')
def supply_chain():
    """Render the supply chain optimization use case."""
    # Get the correlator component
    correlator = system_integrator.get_component('correlator')
    predictor = system_integrator.get_component('predictor')
    
    # In a real application, we'd load actual data
    # For demo purposes, we'll use mock data
    mock_data = {
        'inventory_insights': [
            {'product': 'Refrigerated Food Storage Containers', 'current_stock': 2500, 'predicted_demand': 3800, 'restock_recommendation': 1300, 'confidence': 0.85},
            {'product': 'Industrial Packaging Materials', 'current_stock': 5200, 'predicted_demand': 4100, 'restock_recommendation': 0, 'confidence': 0.92},
            {'product': 'Temperature-Controlled Shipping Units', 'current_stock': 830, 'predicted_demand': 1200, 'restock_recommendation': 370, 'confidence': 0.78},
            {'product': 'Logistics Management Software Licenses', 'current_stock': 450, 'predicted_demand': 390, 'restock_recommendation': 0, 'confidence': 0.88},
        ],
        'correlations': [
            {'factor1': 'Extreme Heat Events', 'factor2': 'Cold Storage Demand', 'correlation': 0.87, 'strength': 'strong'},
            {'factor1': 'Seasonal Flooding', 'factor2': 'Transportation Delays', 'correlation': 0.79, 'strength': 'strong'},
            {'factor1': 'Holiday Season', 'factor2': 'Packaging Material Demand', 'correlation': 0.73, 'strength': 'strong'},
        ],
        'weather_forecast': {'temperature': 92, 'condition': 'Extreme Heat Warning', 'precipitation': 0},
        'economic_indicators': {'consumer_confidence': 112, 'trend': 'increasing'},
        'social_media_trends': {'buzz_factor': 87, 'sentiment': 'positive'},
        'logistics_data': {
            'shipping_delays': [
                {'route': 'North-South Corridor', 'delay_hours': 8.5, 'affected_products': 'Refrigerated Goods', 'cause': 'Weather Conditions'},
                {'route': 'East Port to Central Distribution', 'delay_hours': 3.2, 'affected_products': 'General Merchandise', 'cause': 'Traffic Congestion'},
                {'route': 'Cross-Country Route 5', 'delay_hours': 12.0, 'affected_products': 'All Categories', 'cause': 'Infrastructure Maintenance'}
            ],
            'warehouse_capacity': [
                {'location': 'North Regional Warehouse', 'capacity_used': 82, 'remaining_capacity': 18, 'optimization_suggestion': 'Redistribute to Southern Facility'},
                {'location': 'Central Distribution Hub', 'capacity_used': 65, 'remaining_capacity': 35, 'optimization_suggestion': 'No action needed'},
                {'location': 'East Coast Facility', 'capacity_used': 91, 'remaining_capacity': 9, 'optimization_suggestion': 'Urgent reallocation required'}
            ]
        }
    }
    
    return render_template('use_cases/supply_chain.html', title='Supply Chain Optimization', data=mock_data)

@main.route('/use-cases/public-health')
def public_health():
    """Render the public health response planning use case."""
    # For demo purposes, we'll use mock data
    mock_data = {
        'outbreak_predictions': [
            {'region': 'North County', 'risk_level': 'high', 'confidence': 0.88, 'contributing_factors': 'High population density, increased travel, seasonal patterns'},
            {'region': 'East District', 'risk_level': 'medium', 'confidence': 0.76, 'contributing_factors': 'Recent events, weather patterns'},
            {'region': 'West Side', 'risk_level': 'low', 'confidence': 0.91, 'contributing_factors': 'Lower population density, good vaccination coverage'},
            {'region': 'South Region', 'risk_level': 'medium', 'confidence': 0.82, 'contributing_factors': 'Weather patterns, community gatherings'},
        ],
        'resource_recommendations': [
            {'resource': 'Testing Kits', 'current_stock': 5000, 'predicted_need': 7500, 'recommendation': 2500},
            {'resource': 'Vaccines', 'current_stock': 10000, 'predicted_need': 8000, 'recommendation': 0},
            {'resource': 'PPE Sets', 'current_stock': 2000, 'predicted_need': 3500, 'recommendation': 1500},
            {'resource': 'Medical Staff', 'current_staff': 120, 'recommended_staff': 140, 'additional_needed': 20},
        ],
        'correlations': [
            {'factor1': 'Temperature Drop', 'factor2': 'Flu Cases', 'correlation': 0.76, 'strength': 'strong'},
            {'factor1': 'Community Events', 'factor2': 'Disease Spread', 'correlation': 0.68, 'strength': 'moderate'},
            {'factor1': 'Public Transportation Usage', 'factor2': 'Infection Rate', 'correlation': 0.72, 'strength': 'strong'},
        ]
    }
    
    return render_template('use_cases/public_health.html', title='Public Health Response Planning', data=mock_data)

@main.route('/use-cases/urban-infrastructure')
def urban_infrastructure():
    """Render the urban infrastructure management use case."""
    # For demo purposes, we'll use mock data
    mock_data = {
        'stress_points': [
            {'location': 'Downtown Bridge', 'risk_level': 'high', 'confidence': 0.89, 'recommendation': 'Schedule inspection within 7 days'},
            {'location': 'North Highway', 'risk_level': 'medium', 'confidence': 0.76, 'recommendation': 'Monitor traffic patterns'},
            {'location': 'West Side Power Grid', 'risk_level': 'high', 'confidence': 0.92, 'recommendation': 'Prepare backup generators'},
            {'location': 'South Water Main', 'risk_level': 'low', 'confidence': 0.85, 'recommendation': 'Routine maintenance sufficient'},
        ],
        'event_impacts': [
            {'event': 'Downtown Festival', 'date': '2023-05-15', 'predicted_impact': 'Significant traffic congestion, high power usage'},
            {'event': 'Sports Championship', 'date': '2023-05-22', 'predicted_impact': 'Public transit overload, cellular network strain'},
            {'event': 'State Conference', 'date': '2023-06-05', 'predicted_impact': 'Hotel capacity reached, moderate traffic increase'},
        ],
        'correlations': [
            {'factor1': 'Rainfall Intensity', 'factor2': 'Storm Drain Pressure', 'correlation': 0.83, 'strength': 'strong'},
            {'factor1': 'Temperature', 'factor2': 'Power Grid Load', 'correlation': 0.77, 'strength': 'strong'},
            {'factor1': 'Event Attendance', 'factor2': 'Traffic Congestion', 'correlation': 0.81, 'strength': 'strong'},
        ],
        'weather_forecast': {'temperature': 88, 'condition': 'Thunderstorms', 'precipitation': 60},
    }
    
    return render_template('use_cases/urban_infrastructure.html', title='Urban Infrastructure Management', data=mock_data)

@main.route('/use-cases/financial-market')
def financial_market():
    """Render the financial market strategy use case."""
    # For demo purposes, we'll use mock data
    mock_data = {
        'market_predictions': [
            {'market': 'Technology Sector', 'trend': 'upward', 'confidence': 0.82, 'key_factors': 'Product launches, positive consumer sentiment'},
            {'market': 'Energy Commodities', 'trend': 'downward', 'confidence': 0.78, 'key_factors': 'Weather patterns, transportation disruptions'},
            {'market': 'Consumer Goods', 'trend': 'stable', 'confidence': 0.91, 'key_factors': 'Economic indicators, steady demand'},
            {'market': 'Financial Services', 'trend': 'upward', 'confidence': 0.73, 'key_factors': 'Interest rate projections, market sentiment'},
        ],
        'opportunity_alerts': [
            {'asset': 'Renewable Energy ETF', 'signal': 'buy', 'confidence': 0.85, 'reasoning': 'Weather pattern shifts, policy changes'},
            {'asset': 'Agricultural Futures', 'signal': 'sell', 'confidence': 0.79, 'reasoning': 'Improved weather forecast for growing regions'},
            {'asset': 'Tech Sector Leaders', 'signal': 'hold', 'confidence': 0.82, 'reasoning': 'Strong social media sentiment balanced with economic concerns'},
        ],
        'correlations': [
            {'factor1': 'Weather Severity', 'factor2': 'Energy Prices', 'correlation': 0.84, 'strength': 'strong'},
            {'factor1': 'Social Media Sentiment', 'factor2': 'Stock Performance', 'correlation': 0.68, 'strength': 'moderate'},
            {'factor1': 'Transportation Disruptions', 'factor2': 'Supply Chain Costs', 'correlation': 0.79, 'strength': 'strong'},
        ],
        'economic_indicators': {'gdp_growth': 2.3, 'trend': 'stable'},
        'social_sentiment': {'overall': 'positive', 'trend': 'improving'}
    }
    
    return render_template('use_cases/financial_market.html', title='Financial Market Strategy', data=mock_data)

@main.route('/api/dashboard/data')
def dashboard_data():
    """API endpoint for dashboard data"""
    # Check cache first
    cache_key = 'dashboard_data'
    if cache_key in dashboard_data_cache:
        cached_time, cached_data = dashboard_data_cache[cache_key]
        if time.time() - cached_time < dashboard_cache_expires:
            return jsonify(cached_data)
    
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
    
    result = {
        'data': organized_data,
        'health': health,
        'timestamp': pipeline.get_current_timestamp()
    }
    
    # Cache the result
    dashboard_data_cache[cache_key] = (time.time(), result)
    
    return jsonify(result)

@main.route('/api/dashboard-data')
def dashboard_data_new():
    """API endpoint to get dashboard data."""
    # Check cache first
    cache_key = 'dashboard_data_new'
    if cache_key in dashboard_data_cache:
        cached_time, cached_data = dashboard_data_cache[cache_key]
        if time.time() - cached_time < dashboard_cache_expires:
            return jsonify(cached_data)
            
    # In a real application, this would fetch data from the database
    # For demo purposes, we'll return mock data
    result = {
        'weather': {
            'temperature': 78,
            'condition': 'Partly Cloudy',
            'forecast': [
                {'day': 'Today', 'high': 78, 'low': 65, 'condition': 'Partly Cloudy'},
                {'day': 'Tomorrow', 'high': 82, 'low': 68, 'condition': 'Sunny'},
                {'day': 'Wednesday', 'high': 85, 'low': 70, 'condition': 'Sunny'},
                {'day': 'Thursday', 'high': 79, 'low': 68, 'condition': 'Cloudy'},
                {'day': 'Friday', 'high': 76, 'low': 64, 'condition': 'Rainy'}
            ]
        },
        'economic': {
            'market_index': 32415,
            'change_percent': 0.5,
            'consumer_confidence': 110,
            'indicators': [
                {'name': 'GDP Growth', 'value': 2.3, 'trend': 'stable'},
                {'name': 'Unemployment', 'value': 3.6, 'trend': 'decreasing'},
                {'name': 'Inflation', 'value': 2.1, 'trend': 'increasing'},
                {'name': 'Interest Rate', 'value': 1.5, 'trend': 'stable'}
            ]
        },
        'transportation': {
            'congestion_level': 65,
            'average_speed': 35,
            'hotspots': [
                {'location': 'Downtown', 'level': 85, 'trend': 'increasing'},
                {'location': 'Highway 101', 'level': 70, 'trend': 'stable'},
                {'location': 'East Bridge', 'level': 90, 'trend': 'increasing'},
                {'location': 'North Exit', 'level': 45, 'trend': 'decreasing'}
            ]
        },
        'social_media': {
            'sentiment': 72,
            'trending_topics': [
                {'topic': 'New Product Launch', 'sentiment': 85, 'volume': 12500},
                {'topic': 'Weather Concerns', 'sentiment': 45, 'volume': 8300},
                {'topic': 'Traffic Conditions', 'sentiment': 30, 'volume': 7200},
                {'topic': 'Economic News', 'sentiment': 65, 'volume': 6100}
            ]
        }
    }
    
    # Cache the result
    dashboard_data_cache[cache_key] = (time.time(), result)
    
    return jsonify(result)