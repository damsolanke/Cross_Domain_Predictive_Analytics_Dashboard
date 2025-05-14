from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from . import main
from app.system_integration.integration import system_integrator
from app.demo.data_generator import demo_generator
from app.main.analytics_controller import analytics
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
from app.system_integration.cross_domain_prediction import CrossDomainPredictor
import time
import random

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

@main.route('/api/correlation/analyze', methods=['POST'])
def analyze_correlation():
    """API endpoint for correlation analysis"""
    from app.system_integration.routes import generate_correlation, generate_matrix, generate_scatter, generate_network
    import time
    
    # Check if request is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.json
    required_fields = ['domain1', 'field1', 'domain2', 'field2', 'time_range']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Extract parameters
    domain1 = data['domain1']
    field1 = data['field1']
    domain2 = data['domain2']
    field2 = data['field2']
    time_range = data['time_range']
    
    # Try to get the correlator
    correlator = system_integrator.get_component('correlator')
    
    # Generate correlation data
    try:
        # Generate a correlation value based on the inputs
        correlation_value = generate_correlation(domain1, field1, domain2, field2, time_range)
        
        # Generate matrix data for heatmap
        matrix, labels = generate_matrix(domain1, field1, domain2, field2)
        
        # Generate scatter data
        scatter_data = generate_scatter(correlation_value)
        
        # Generate network data
        network = generate_network(domain1, domain2)
        
        # Build the response
        response = {
            'domain1': domain1,
            'field1': field1,
            'domain2': domain2,
            'field2': field2,
            'time_range': time_range,
            'correlation_value': correlation_value,
            'matrix': matrix,
            'labels': labels,
            'scatter_data': scatter_data,
            'network': network,
            'analysis_timestamp': time.time()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/use-cases/supply-chain')
def supply_chain():
    """Render the supply chain optimization use case."""
    # Get the correlator component
    correlator = system_integrator.get_component('correlator')
    predictor = system_integrator.get_component('predictor')

    # Get the default data
    mock_data = _get_supply_chain_data()

    return render_template('use_cases/supply_chain.html', title='Supply Chain Optimization', data=mock_data)

@main.route('/use-cases/supply-chain/data')
def supply_chain_data():
    """API endpoint for supply chain data that respects timeframe."""
    time_range = request.args.get('timeRange', '1d')

    # Get data based on timeframe
    mock_data = _get_supply_chain_data(time_range)

    # Return as JSON
    return jsonify(mock_data)

def _get_supply_chain_data(time_range='1d'):
    """
    Generate supply chain data based on the selected time range.
    This function simulates different data for different time ranges.

    Args:
        time_range (str): The time range selected ('1d', '7d', '30d', '90d', '180d', '365d')

    Returns:
        dict: Supply chain data customized for the specified time range
    """
    # Base metrics that will be adjusted based on time range
    base_temperature = 92
    base_confidence = 112
    base_buzz = 87
    base_shipping_time = 3.8

    # Adjust metrics based on time range
    if time_range == '1d':
        # Default values for 1 day view (baseline)
        condition = 'Extreme Heat Warning'
        consumer_confidence = base_confidence
        buzz_factor = base_buzz
        shipping_time = base_shipping_time
        sentiment = 'positive'
        correlation_modifier = 0.0

    elif time_range == '7d':
        # Week view - slightly different conditions
        condition = 'Heat Advisory'
        consumer_confidence = base_confidence - 5
        buzz_factor = base_buzz - 10
        shipping_time = base_shipping_time + 0.6
        sentiment = 'neutral'
        correlation_modifier = -0.05

    elif time_range == '30d':
        # Month view - more significant differences
        condition = 'Variable Weather Patterns'
        consumer_confidence = base_confidence - 10
        buzz_factor = base_buzz - 15
        shipping_time = base_shipping_time + 1.2
        sentiment = 'cautious'
        correlation_modifier = -0.1

    elif time_range == '90d':
        # Quarter view
        condition = 'Seasonal Pattern Shift'
        consumer_confidence = base_confidence + 8
        buzz_factor = base_buzz + 5
        shipping_time = base_shipping_time - 0.4
        sentiment = 'optimistic'
        correlation_modifier = 0.08

    elif time_range == '180d':
        # Half year view
        condition = 'Multiple Weather Events'
        consumer_confidence = base_confidence + 15
        buzz_factor = base_buzz + 10
        shipping_time = base_shipping_time - 0.8
        sentiment = 'very positive'
        correlation_modifier = 0.15

    elif time_range == '365d':
        # Full year view
        condition = 'Yearly Climate Pattern'
        consumer_confidence = base_confidence + 20
        buzz_factor = base_buzz - 5
        shipping_time = base_shipping_time - 0.2
        sentiment = 'mixed'
        correlation_modifier = 0.05

    # Adjust temperature based on timeframe
    adjusted_temperature = base_temperature
    if time_range in ['90d', '180d', '365d']:
        adjusted_temperature = int(base_temperature * 0.85)  # Cooler for longer timeframes (seasonal averaging)

    # Generate shipping delays based on timeframe
    shipping_delays = []

    # Default delays for shorter timeframes
    if time_range in ['1d', '7d']:
        shipping_delays = [
            {'route': 'North-South Corridor', 'delay_hours': 8.5, 'affected_products': 'Refrigerated Goods', 'cause': 'Weather Conditions'},
            {'route': 'East Port to Central Distribution', 'delay_hours': 3.2, 'affected_products': 'General Merchandise', 'cause': 'Traffic Congestion'},
            {'route': 'Cross-Country Route 5', 'delay_hours': 12.0, 'affected_products': 'All Categories', 'cause': 'Infrastructure Maintenance'}
        ]
    # Mid-term delays
    elif time_range in ['30d', '90d']:
        shipping_delays = [
            {'route': 'North-South Corridor', 'delay_hours': 5.3, 'affected_products': 'Refrigerated Goods', 'cause': 'Weather Conditions'},
            {'route': 'International Shipping Lane', 'delay_hours': 36.0, 'affected_products': 'Import Products', 'cause': 'Port Congestion'},
            {'route': 'Cross-Country Route 5', 'delay_hours': 8.0, 'affected_products': 'All Categories', 'cause': 'Infrastructure Maintenance'}
        ]
    # Long-term patterns
    else:
        shipping_delays = [
            {'route': 'International Shipping Lane', 'delay_hours': 48.0, 'affected_products': 'Import Products', 'cause': 'Seasonal Congestion'},
            {'route': 'Southern Route', 'delay_hours': 16.5, 'affected_products': 'Agricultural Products', 'cause': 'Seasonal Weather'},
            {'route': 'Cross-Country Route 5', 'delay_hours': 24.0, 'affected_products': 'All Categories', 'cause': 'Yearly Maintenance'}
        ]

    # Adjust correlation data based on timeframe
    correlations = [
        {'factor1': 'Extreme Heat Events', 'factor2': 'Cold Storage Demand', 'correlation': 0.87 + correlation_modifier, 'strength': 'strong'},
        {'factor1': 'Seasonal Flooding', 'factor2': 'Transportation Delays', 'correlation': 0.79 + correlation_modifier, 'strength': 'strong'},
        {'factor1': 'Holiday Season', 'factor2': 'Packaging Material Demand', 'correlation': 0.73 + correlation_modifier, 'strength': 'strong'},
    ]

    # Adjust inventory insights based on timeframe
    if time_range in ['1d', '7d']:
        inventory_insights = [
            {'product': 'Refrigerated Food Storage Containers', 'current_stock': 2500, 'predicted_demand': 3800, 'restock_recommendation': 1300, 'confidence': 0.85},
            {'product': 'Industrial Packaging Materials', 'current_stock': 5200, 'predicted_demand': 4100, 'restock_recommendation': 0, 'confidence': 0.92},
            {'product': 'Temperature-Controlled Shipping Units', 'current_stock': 830, 'predicted_demand': 1200, 'restock_recommendation': 370, 'confidence': 0.78},
            {'product': 'Logistics Management Software Licenses', 'current_stock': 450, 'predicted_demand': 390, 'restock_recommendation': 0, 'confidence': 0.88},
        ]
    elif time_range in ['30d', '90d']:
        inventory_insights = [
            {'product': 'Refrigerated Food Storage Containers', 'current_stock': 2500, 'predicted_demand': 3200, 'restock_recommendation': 700, 'confidence': 0.82},
            {'product': 'Industrial Packaging Materials', 'current_stock': 5200, 'predicted_demand': 6500, 'restock_recommendation': 1300, 'confidence': 0.88},
            {'product': 'Sustainable Packaging Solutions', 'current_stock': 3400, 'predicted_demand': 4200, 'restock_recommendation': 800, 'confidence': 0.76},
            {'product': 'Emergency Power Generators', 'current_stock': 120, 'predicted_demand': 210, 'restock_recommendation': 90, 'confidence': 0.88},
        ]
    else:
        inventory_insights = [
            {'product': 'Sustainable Packaging Solutions', 'current_stock': 3400, 'predicted_demand': 8500, 'restock_recommendation': 5100, 'confidence': 0.92},
            {'product': 'Industrial Packaging Materials', 'current_stock': 5200, 'predicted_demand': 12000, 'restock_recommendation': 6800, 'confidence': 0.85},
            {'product': 'Emergency Power Generators', 'current_stock': 120, 'predicted_demand': 450, 'restock_recommendation': 330, 'confidence': 0.79},
            {'product': 'Temperature-Controlled Shipping Units', 'current_stock': 830, 'predicted_demand': 1900, 'restock_recommendation': 1070, 'confidence': 0.81},
        ]

    # Complete data structure
    data = {
        'inventory_insights': inventory_insights,
        'correlations': correlations,
        'weather_forecast': {'temperature': adjusted_temperature, 'condition': condition, 'precipitation': 0},
        'economic_indicators': {'consumer_confidence': consumer_confidence, 'trend': 'increasing' if consumer_confidence > base_confidence else 'decreasing'},
        'social_media_trends': {'buzz_factor': buzz_factor, 'sentiment': sentiment},
        'logistics_data': {
            'average_shipping_time': shipping_time,
            'shipping_delays': shipping_delays,
            'warehouse_capacity': [
                {'location': 'North Regional Warehouse', 'capacity_used': 82, 'remaining_capacity': 18, 'optimization_suggestion': 'Redistribute to Southern Facility'},
                {'location': 'Central Distribution Hub', 'capacity_used': 65, 'remaining_capacity': 35, 'optimization_suggestion': 'No action needed'},
                {'location': 'East Coast Facility', 'capacity_used': 91, 'remaining_capacity': 9, 'optimization_suggestion': 'Urgent reallocation required'}
            ]
        }
    }

    return data

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

@main.route('/api/correlations')
def correlations_data():
    """API endpoint for cross-domain correlations"""
    try:
        # Get time range from query parameters
        time_range = request.args.get('timeRange', '1d')
        resolution = request.args.get('resolution', 'daily')
        lag_window = int(request.args.get('lagWindow', 3))
        
        # Get correlator from system integrator
        correlator = system_integrator.get_component('correlator')
        
        # Generate some realistic correlation data
        correlations = []
        
        # Domain pairs to generate correlations for
        domain_pairs = [
            ('weather', 'temperature', 'economic', 'market_index', 0.68, 'moderate'),
            ('weather', 'temperature', 'transportation', 'congestion_level', 0.72, 'strong'),
            ('weather', 'precipitation', 'transportation', 'accident_count', 0.81, 'strong'),
            ('economic', 'market_index', 'social-media', 'sentiment', 0.65, 'moderate'),
            ('economic', 'consumer_confidence', 'social-media', 'engagement_rate', 0.58, 'moderate'),
            ('transportation', 'congestion_level', 'economic', 'retail_sales', -0.52, 'moderate'),
            ('social-media', 'sentiment', 'economic', 'market_volatility', 0.46, 'moderate'),
            ('social-media', 'mentions', 'economic', 'market_volatility', 0.53, 'moderate'),
            ('weather', 'wind_speed', 'transportation', 'accident_count', 0.47, 'moderate'),
            ('weather', 'temperature', 'social-media', 'sentiment', 0.32, 'weak')
        ]
        
        # Add some randomization based on time range for realistic data
        for pair in domain_pairs:
            domain1, metric1, domain2, metric2, base_correlation, strength = pair
            
            # Adjust correlation based on time range (longer ranges show stronger patterns)
            time_factor = 1.0
            if time_range == '7d':
                time_factor = 0.9
            elif time_range == '90d':
                time_factor = 1.1
            elif time_range == '1y':
                time_factor = 1.15
            
            # Add some random noise
            correlation = base_correlation * time_factor
            correlation += (random.random() - 0.5) * 0.1  # Add ±5% noise
            
            # Cap to valid range
            correlation = max(-1.0, min(1.0, correlation))
            
            # Adjust strength classification based on correlation value
            abs_corr = abs(correlation)
            if abs_corr > 0.7:
                strength = 'strong'
            elif abs_corr > 0.4:
                strength = 'moderate'
            else:
                strength = 'weak'
            
            # Calculate a confidence value (higher for strong correlations)
            confidence = 0.6 + (abs_corr * 0.3) + (random.random() * 0.1)
            
            # Generate lag value (0-3 days typically)
            lag = 0
            if random.random() < 0.4:  # 40% chance of lag
                lag = random.randint(1, lag_window)
            
            correlations.append({
                'domain1': domain1,
                'metric1': metric1,
                'domain2': domain2,
                'metric2': metric2,
                'correlation': correlation,
                'strength': strength,
                'confidence': confidence,
                'lag': lag
            })
        
        # Create summary data
        # Find strongest correlation (by absolute value)
        strongest = max(correlations, key=lambda c: abs(c['correlation']))
        
        # Find strongest negative correlation
        negatives = [c for c in correlations if c['correlation'] < 0]
        negative = min(negatives, key=lambda c: c['correlation']) if negatives else None
        
        # Create trending insight (correlation that's supposedly changing)
        trending = {
            'domain1': 'social-media',
            'metric1': 'sentiment',
            'domain2': 'economic',
            'metric2': 'market_index',
            'correlation_change': 0.15
        }
        
        summary = {
            'strongest': strongest,
            'negative': negative,
            'trending': trending,
            'timeRange': time_range
        }
        
        return jsonify({
            'correlations': correlations,
            'summary': summary,
            'timeRange': time_range,
            'resolution': resolution,
            'lagWindow': lag_window
        })
    except Exception as e:
        print(f"Error in correlations API: {e}")
        return jsonify({
            'error': str(e),
            'correlations': [],
            'summary': {},
            'timeRange': time_range
        }), 500

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