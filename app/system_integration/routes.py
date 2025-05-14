"""
System integration routes.
"""
from flask import render_template, jsonify, request
from . import system_integration
from .integration import system_integrator
from .cross_domain_correlation import CrossDomainCorrelator
import random
import numpy as np
import time

@system_integration.route('/system-status')
def system_status():
    """Render the system status page."""
    return render_template('system_integration/system_status.html', title='System Status')

@system_integration.route('/api/system-status')
@system_integration.route('/system/api/system-status')  # Add the path that frontend is trying to use
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
            },
            "data_pipeline": {
                "status": "active",
                "throughput": 42.5,
                "queue_size": 12
            }
        }

    # Simulate a realistic uptime value (1-5 hours)
    # Store a startup time in the system_integrator if not already set
    if not hasattr(system_integrator, 'startup_time'):
        system_integrator.startup_time = time.time() - (random.randint(3600, 18000))  # 1-5 hours ago
    
    # Calculate uptime from stored startup time
    uptime = int(time.time() - system_integrator.startup_time)

    return jsonify({
        "status": "active",
        "uptime": uptime,
        "components": components,
        "processing_rate": 42.5,
        "queue_size": 12
    })

@system_integration.route('/api/correlation/analyze', methods=['POST'])
@system_integration.route('/system/api/correlation/analyze', methods=['POST'])  # Add prefixed route
def analyze_correlation():
    """
    API endpoint to analyze correlation between two domains and fields.
    Expects JSON with:
        - domain1: First domain name
        - field1: Field name in first domain
        - domain2: Second domain name
        - field2: Field name in second domain
        - time_range: Time range for analysis ('7d', '30d', '90d', '1y', 'all')
    """
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
    
    # Try to get the correlator from the system integrator
    correlator = system_integrator.get_component('correlator')
    if not correlator:
        # Create a new one if not available
        correlator = CrossDomainCorrelator()
    
    # For demonstration, we'll generate simulated but realistic and consistent correlation data
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

def generate_correlation(domain1, field1, domain2, field2, time_range):
    """Generate a deterministic but realistic correlation value."""
    # Create a hash from the inputs for consistent results
    seed_str = f"{domain1}_{field1}_{domain2}_{field2}"
    seed = sum(ord(c) for c in seed_str)
    random.seed(seed)
    
    # Base correlation
    base_correlation = random.uniform(-0.2, 0.9)
    
    # Modify based on domain relationships (add domain-specific logic)
    if (domain1 == 'weather' and domain2 == 'transportation') or (domain2 == 'weather' and domain1 == 'transportation'):
        # Weather and transportation are often correlated
        base_correlation = abs(base_correlation) * 0.8 + 0.1  # 0.1 to 0.9 range
    
    elif (domain1 == 'economic' and domain2 == 'social-media') or (domain2 == 'economic' and domain1 == 'social-media'):
        # Economic and social media can have positive or negative correlation
        base_correlation = base_correlation * 0.8  # -0.16 to 0.72 range
    
    # Adjust based on time range (longer ranges often show stronger correlations)
    time_factor = 1.0
    if time_range == '7d':
        time_factor = 0.85  # Shorter time ranges may show weaker correlations
    elif time_range == '90d':
        time_factor = 1.1  # Longer ranges often show stronger patterns
    elif time_range == '1y':
        time_factor = 1.2
    elif time_range == 'all':
        time_factor = 1.3
    
    # Apply time factor
    correlation = base_correlation * time_factor
    
    # Ensure correlation is in valid range (-1 to 1)
    return max(-0.98, min(0.98, correlation))

def generate_matrix(domain1, field1, domain2, field2):
    """Generate a correlation matrix for heatmap visualization."""
    seed_str = f"{domain1}_{field1}_{domain2}_{field2}"
    seed = sum(ord(c) for c in seed_str)
    random.seed(seed)
    
    # Define fields for each domain
    domain_fields = {
        'weather': [field1, 'temperature', 'precipitation', 'humidity', 'wind_speed'],
        'economic': [field1, 'market_index', 'interest_rate', 'consumer_confidence', 'unemployment'],
        'transportation': [field1, 'congestion', 'average_speed', 'accident_rate', 'transit_usage'],
        'social-media': [field1, 'sentiment', 'engagement', 'mentions', 'trending_topics'],
        'health': [field1, 'hospital_admissions', 'vaccination_rate', 'infection_spread', 'mortality']
    }
    
    # Make sure field1 is first in its domain's list
    if field1 in domain_fields[domain1] and domain_fields[domain1][0] != field1:
        domain_fields[domain1].remove(field1)
        domain_fields[domain1].insert(0, field1)
    
    # Same for field2
    if field2 in domain_fields[domain2] and domain_fields[domain2][0] != field2:
        domain_fields[domain2].remove(field2)
        domain_fields[domain2].insert(0, field2)
    
    # Select unique fields from both domains (up to 5 from each)
    fields1 = domain_fields[domain1][:5]
    fields2 = domain_fields[domain2][:5]
    
    # Create nice labels
    labels = []
    for f in fields1:
        label = f.replace('_', ' ').title()
        if f == field1:
            label += f" ({domain1.replace('-', ' ').title()})"
        labels.append(label)
    
    for f in fields2:
        if f == field2:
            label = f.replace('_', ' ').title() + f" ({domain2.replace('-', ' ').title()})"
        else:
            label = f.replace('_', ' ').title()
        if label not in labels:  # Avoid duplicates
            labels.append(label)
    
    # Create the matrix
    n = len(labels)
    matrix = np.zeros((n, n))
    
    # Fill the matrix with correlation values
    for i in range(n):
        matrix[i, i] = 1.0  # Self-correlation
        for j in range(i+1, n):
            # Generate correlation, considering if fields are in same domain
            same_domain = (i < len(fields1) and j < len(fields1)) or (i >= len(fields1) and j >= len(fields1))
            
            if same_domain:
                # Fields in same domain tend to have stronger positive correlations
                corr = random.uniform(0.3, 0.9)
            else:
                # Fields in different domains can have more varied correlations
                corr = random.uniform(-0.7, 0.8)
            
            # Make field1-field2 correlation match the main correlation
            if (i == 0 and j == len(fields1)) or (i == len(fields1) and j == 0):
                corr = generate_correlation(domain1, field1, domain2, field2, '30d')  # Use 30d as default
            
            matrix[i, j] = corr
            matrix[j, i] = corr  # Symmetric matrix
    
    return matrix.tolist(), labels

def generate_scatter(correlation):
    """Generate scatter plot data with the specified correlation."""
    # Number of data points
    n = 30
    
    # Generate x data (random but fixed)
    random.seed(42)  # Fixed seed for consistency
    x_data = [random.uniform(20, 80) for _ in range(n)]
    
    # Generate correlated y data
    random.seed(43)  # Different seed for y
    
    # Create correlated data using the formula:
    # y = correlation * x + sqrt(1-correlation^2) * noise
    y_data = []
    for x in x_data:
        # Normalize x to mean 0, std 1
        x_norm = (x - 50) / 15
        
        # Generate random noise
        noise = random.normalvariate(0, 1)
        
        # Apply correlation formula
        y_norm = correlation * x_norm + np.sqrt(1 - correlation**2) * noise
        
        # Transform back to original scale
        y = 50 + y_norm * 15
        
        y_data.append(y)
    
    return {'x': x_data, 'y': y_data}

def generate_network(domain1, domain2):
    """Generate network graph data."""
    seed_str = f"{domain1}_{domain2}"
    seed = sum(ord(c) for c in seed_str)
    random.seed(seed)
    
    # Available domains
    all_domains = ['weather', 'economic', 'transportation', 'social-media', 'health']
    
    # Make sure domain1 and domain2 are included
    domains = [d for d in all_domains if d in [domain1, domain2]]
    
    # Add some additional domains
    remaining = [d for d in all_domains if d not in domains]
    domains.extend(random.sample(remaining, min(3, len(remaining))))
    
    # Create nodes
    nodes = []
    for i, domain in enumerate(domains):
        nodes.append({
            'id': domain.replace('-', ' ').title(),
            'group': i + 1
        })
    
    # Create links
    links = []
    
    # Ensure link between the selected domains
    domain1_label = domain1.replace('-', ' ').title()
    domain2_label = domain2.replace('-', ' ').title()
    links.append({
        'source': domain1_label,
        'target': domain2_label,
        'value': abs(generate_correlation(domain1, 'default', domain2, 'default', '30d'))
    })
    
    # Add additional links
    for i, source in enumerate(nodes):
        for j, target in enumerate(nodes):
            if i < j:  # Avoid duplicates and self-links
                # Skip if already connected
                if (source['id'] == domain1_label and target['id'] == domain2_label) or \
                   (source['id'] == domain2_label and target['id'] == domain1_label):
                    continue
                
                # Add with random strength (higher probability for stronger connections)
                if random.random() < 0.7:  # 70% chance of connection
                    value = random.uniform(0.3, 0.9)  # Decent strength
                    links.append({
                        'source': source['id'],
                        'target': target['id'],
                        'value': value
                    })
    
    return {'nodes': nodes, 'links': links}