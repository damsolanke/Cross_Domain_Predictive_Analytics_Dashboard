#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_socketio import SocketIO
import time
import random
import os

# Create a direct Flask application
app = Flask(__name__, 
            static_folder='app/static',
            template_folder='app/templates')

# Configure the app
app.config['SECRET_KEY'] = 'REDACTED'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Socket.IO event handlers
@socketio.on('connect', namespace='/system-updates')
def handle_connect():
    print("Client connected to system-updates namespace")
    socketio.emit('connection_response', {
        'status': 'connected',
        'message': 'Connected to system updates'
    }, namespace='/system-updates')

@socketio.on('subscribe_to_updates', namespace='/system-updates')
def handle_subscribe(data):
    print(f"Client subscribed to updates: {data}")
    socketio.emit('subscription_response', {
        'status': 'subscribed',
        'update_type': data.get('update_type', 'all')
    }, namespace='/system-updates')

@socketio.on('get_correlation_data', namespace='/system-updates')
def handle_get_correlation():
    # Send mock data for now
    mock_data = {
        'status': 'success',
        'data': {
            'domain_pair': 'weather_vs_economic',
            'heatmap_data': [{
                'domain_pair': 'weather_vs_economic',
                'data': [
                    {'x': 'Temperature', 'y': 'Stock Price', 'value': 0.65},
                    {'x': 'Rainfall', 'y': 'Consumer Spending', 'value': -0.32},
                    {'x': 'Humidity', 'y': 'Interest Rate', 'value': 0.18}
                ]
            }],
            'network_data': {
                'nodes': [
                    {'id': 'weather:temp', 'group': 'weather'},
                    {'id': 'weather:rain', 'group': 'weather'},
                    {'id': 'economic:gdp', 'group': 'economic'},
                    {'id': 'economic:stocks', 'group': 'economic'}
                ],
                'links': [
                    {'source': 'weather:temp', 'target': 'economic:stocks', 'value': 0.65, 'direction': 'positive'},
                    {'source': 'weather:rain', 'target': 'economic:gdp', 'value': 0.32, 'direction': 'negative'}
                ]
            }
        }
    }
    socketio.emit('correlation_data', mock_data, namespace='/system-updates')

@socketio.on('get_correlation_insights', namespace='/system-updates')
def handle_get_insights():
    # Send mock insights
    mock_insights = {
        'status': 'success',
        'data': [
            {
                'domain1': 'weather',
                'domain2': 'economic',
                'description': 'Strong correlation between temperature and stock market performance',
                'correlation_value': 0.65,
                'variable1': 'Temperature',
                'variable2': 'Stock Price',
                'timestamp': int(time.time() * 1000)
            },
            {
                'domain1': 'transportation',
                'domain2': 'economic',
                'description': 'Increased traffic congestion correlates with retail spending',
                'correlation_value': 0.58,
                'variable1': 'Congestion Level',
                'variable2': 'Retail Sales',
                'timestamp': int(time.time() * 1000)
            }
        ]
    }
    socketio.emit('correlation_insight', mock_insights, namespace='/system-updates')

# Basic routes
@app.route('/')
def index():
    # Show the home page instead of redirecting to dashboard
    return render_template('index.html', title='Cross-Domain Predictive Analytics Dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='Analytics Dashboard')

@app.route('/nlq')
def nlq():
    """Natural language query interface"""
    return render_template('nlq.html', title='Natural Language Queries')

@app.route('/correlation')
def correlation():
    """Cross-domain correlation analysis page"""
    return render_template('correlation.html', title='Cross-Domain Correlation Analysis')

# Debug info will be printed in main block

# Use Case routes
@app.route('/use-cases/supply-chain')
def supply_chain_use_case():
    """Supply Chain Optimization use case page"""
    # Create mock data for the template
    mock_data = {
        'weather_forecast': {'condition': 'Partly Cloudy'},
        'economic_indicators': {'trend': 'improving'},
        'social_media_trends': {'sentiment': 'positive'},
        'inventory_insights': [
            {'product': 'Product A', 'current_stock': 120, 'predicted_demand': 180, 'confidence': 0.87, 'restock_recommendation': 60},
            {'product': 'Product B', 'current_stock': 75, 'predicted_demand': 50, 'confidence': 0.92, 'restock_recommendation': 0},
            {'product': 'Product C', 'current_stock': 30, 'predicted_demand': 90, 'confidence': 0.78, 'restock_recommendation': 60},
            {'product': 'Product D', 'current_stock': 200, 'predicted_demand': 140, 'confidence': 0.85, 'restock_recommendation': 0}
        ],
        'correlations': [
            {'factor1': 'Temperature', 'factor2': 'Ice Cream Sales', 'strength': 'strong', 'correlation': 0.87},
            {'factor1': 'Rainfall', 'factor2': 'Umbrella Sales', 'strength': 'strong', 'correlation': 0.79},
            {'factor1': 'Temperature', 'factor2': 'Rainfall', 'strength': 'medium', 'correlation': 0.45},
            {'factor1': 'Ice Cream Sales', 'factor2': 'Umbrella Sales', 'strength': 'weak', 'correlation': 0.32}
        ]
    }
    
    return render_template('use_cases/supply_chain.html', title='Supply Chain Optimization', data=mock_data)

@app.route('/use-cases/public-health')
def public_health_use_case():
    """Public Health Response Planning use case page"""
    # Create mock data for the template
    mock_data = {
        'outbreak_predictions': [
            {'region': 'North County', 'risk_level': 'high', 'confidence': 0.88},
            {'region': 'East District', 'risk_level': 'medium', 'confidence': 0.76},
            {'region': 'West Side', 'risk_level': 'low', 'confidence': 0.91},
            {'region': 'South Region', 'risk_level': 'medium', 'confidence': 0.82}
        ],
        'resource_recommendations': [
            {'resource': 'Testing Kits', 'current_stock': 5000, 'predicted_need': 7500, 'recommendation': 2500},
            {'resource': 'PPE Sets', 'current_stock': 2000, 'predicted_need': 3500, 'recommendation': 1500},
            {'resource': 'Ventilators', 'current_stock': 50, 'predicted_need': 45, 'recommendation': 0},
            {'resource': 'Hospital Beds', 'current_stock': 120, 'predicted_need': 95, 'recommendation': 0},
            {'resource': 'Medical Staff', 'current_staff': 75, 'recommended_staff': 95, 'additional_needed': 20},
            {'resource': 'Support Staff', 'current_staff': 45, 'recommended_staff': 65, 'additional_needed': 20},
            {'resource': 'Lab Technicians', 'current_staff': 15, 'recommended_staff': 20, 'additional_needed': 5}
        ],
        'correlations': [
            {'factor1': 'Temperature', 'factor2': 'Flu Cases', 'strength': 'strong', 'correlation': 0.76},
            {'factor1': 'Events', 'factor2': 'Transit Usage', 'strength': 'medium', 'correlation': 0.68},
            {'factor1': 'Temperature', 'factor2': 'Events', 'strength': 'medium', 'correlation': 0.42},
            {'factor1': 'Flu Cases', 'factor2': 'Transit Usage', 'strength': 'medium', 'correlation': 0.40}
        ]
    }
    
    return render_template('use_cases/public_health.html', title='Public Health Response Planning', data=mock_data)

@app.route('/use-cases/urban-infrastructure')
def urban_infrastructure_use_case():
    """Urban Infrastructure Management use case page"""
    # Create mock data for the template
    mock_data = {
        'weather_forecast': {'temperature': 75, 'condition': 'Rain Expected'},
        'traffic_data': {'congestion_level': 0.65, 'trend': 'increasing'},
        'event_calendar': {'upcoming_events': 3, 'largest_attendance': 25000},
        'infrastructure_alerts': [
            {'system': 'Storm Drains', 'status': 'warning', 'risk_level': 'high', 'confidence': 0.89},
            {'system': 'Power Grid', 'status': 'normal', 'risk_level': 'low', 'confidence': 0.92},
            {'system': 'Road Network', 'status': 'warning', 'risk_level': 'medium', 'confidence': 0.78},
            {'system': 'Public Transit', 'status': 'normal', 'risk_level': 'low', 'confidence': 0.85}
        ],
        'correlations': [
            {'factor1': 'Rainfall', 'factor2': 'Drain Capacity', 'strength': 'strong', 'correlation': 0.88},
            {'factor1': 'Events', 'factor2': 'Traffic Congestion', 'strength': 'strong', 'correlation': 0.82},
            {'factor1': 'Temperature', 'factor2': 'Power Usage', 'strength': 'medium', 'correlation': 0.68},
            {'factor1': 'Weekend', 'factor2': 'Transit Usage', 'strength': 'medium', 'correlation': 0.54}
        ]
    }
    
    return render_template('use_cases/urban_infrastructure.html', title='Urban Infrastructure Management', data=mock_data)

@app.route('/use-cases/financial-market')
def financial_market_use_case():
    """Financial Market Strategy use case page"""
    # Create mock data for the template
    mock_data = {
        'weather_data': {'temperature_anomaly': '+1.2°C', 'trend': 'warming'},
        'economic_indicators': {'trend': 'upward', 'gdp_growth': 2.8, 'inflation': 3.2},
        'market_indices': {'s_and_p': 4285, 'trend': 'upward'},
        'social_sentiment': {'overall': 0.65, 'trend': 'positive'},
        'investment_opportunities': [
            {'sector': 'Renewable Energy', 'signal': 'strong buy', 'confidence': 0.88, 'drivers': ['Weather Patterns', 'Policy Changes']},
            {'sector': 'Agriculture', 'signal': 'hold', 'confidence': 0.72, 'drivers': ['Weather Patterns', 'Supply Chain']},
            {'sector': 'Insurance', 'signal': 'buy', 'confidence': 0.81, 'drivers': ['Weather Patterns', 'Demographic Trends']},
            {'sector': 'Real Estate', 'signal': 'sell', 'confidence': 0.76, 'drivers': ['Interest Rates', 'Urban Migration']}
        ],
        'correlations': [
            {'factor1': 'Temperature Anomaly', 'factor2': 'Energy Demand', 'strength': 'strong', 'correlation': 0.85},
            {'factor1': 'Rainfall Patterns', 'factor2': 'Crop Yields', 'strength': 'strong', 'correlation': 0.79},
            {'factor1': 'Extreme Weather Events', 'factor2': 'Insurance Claims', 'strength': 'strong', 'correlation': 0.91},
            {'factor1': 'Social Sentiment', 'factor2': 'Market Volatility', 'strength': 'medium', 'correlation': 0.63}
        ]
    }
    
    return render_template('use_cases/financial_market.html', title='Financial Market Strategy', data=mock_data)

@app.route('/api/dashboard/data')
def dashboard_data():
    """API endpoint for dashboard data"""
    # Return mock data structure similar to what the real API would return
    return jsonify({
        'data': {
            'weather': [
                {
                    'type': 'forecast', 
                    'original': {'current': {'temp': 25, 'humidity': 65}},
                    'predictions': [
                        {'timestamp': int(time.time() * 1000), 'temperature': 25, 'humidity': 65},
                        {'timestamp': int(time.time() * 1000) + 3600000, 'temperature': 26, 'humidity': 62}
                    ]
                }
            ],
            'economic': [{'gdp_growth': 2.5, 'unemployment': 3.7}],
            'transportation': [{'congestion': 0.65, 'avg_speed': 35}],
            'social-media': [{'sentiment': 0.42, 'engagement': 2500}],
            'cross-domain': []
        },
        'health': {
            'uptime_seconds': 3600,
            'processing_rate': 12.5,
            'component_counts': {'api_connectors': 4, 'processors': 2},
            'queue_sizes': {'incoming': 5, 'processed': 0}
        },
        'timestamp': int(time.time())
    })

@app.route('/api/system/correlation/configure', methods=['POST'])
def configure_correlation():
    """API endpoint to configure correlation settings"""
    data = request.json
    # In a real implementation, this would update correlation settings
    return jsonify({
        'status': 'success',
        'message': 'Correlation settings updated successfully',
        'settings': data
    })

# Run the application directly
if __name__ == '__main__':
    print("Starting direct server for Cross-Domain Predictive Analytics Dashboard...")
    
    # Print template info
    print(f"Template folder: {app.template_folder}")
    print(f"Template folder exists: {os.path.exists(app.template_folder)}")
    use_cases_path = os.path.join(app.template_folder, 'use_cases')
    print(f"Use cases path: {use_cases_path}")
    print(f"Use cases path exists: {os.path.exists(use_cases_path)}")
    if os.path.exists(use_cases_path):
        print(f"Files in use_cases: {os.listdir(use_cases_path)}")
    
    # Print static file information
    print(f"Static folder: {app.static_folder}")
    print(f"Static folder exists: {os.path.exists(app.static_folder)}")
    img_path = os.path.join(app.static_folder, 'img')
    print(f"Images path: {img_path}")
    print(f"Images path exists: {os.path.exists(img_path)}")
    if os.path.exists(img_path):
        print(f"Files in img folder: {os.listdir(img_path)}")
        
    # Use socketio.run instead of app.run
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 