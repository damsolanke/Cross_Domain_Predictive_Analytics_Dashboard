"""
API routes for the Cross-Domain Predictive Analytics Dashboard.
"""

from flask import jsonify, request
from . import api
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
import numpy as np
import random

# Initialize correlation analyzer
correlator = CrossDomainCorrelator()

@api.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'OK'})

@api.route('/correlation/analyze', methods=['POST'])
def analyze_correlation():
    """Analyze correlation between two domains/fields."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Get correlation parameters
        domain1 = data.get('domain1')
        field1 = data.get('field1')
        domain2 = data.get('domain2')
        field2 = data.get('field2')
        time_range = data.get('time_range', '30d')
        
        # Validate required parameters
        if not all([domain1, field1, domain2, field2]):
            return jsonify({'error': 'Missing required parameters'}), 400
            
        # For now, generate simulated data 
        # In a production environment, this would use the actual correlator class
        correlation_value = calculate_simulated_correlation(domain1, field1, domain2, field2)
        
        # Generate fake matrix data (would be real in production)
        matrix, labels = generate_matrix_data(domain1, field1, domain2, field2)
        
        # Generate scatter data
        scatter_data = generate_scatter_data(correlation_value)
        
        # Generate network data
        network_data = generate_network_data(domain1, domain2)
        
        # Return correlation results
        return jsonify({
            'correlation_value': correlation_value,
            'domain1': domain1,
            'field1': field1,
            'domain2': domain2,
            'field2': field2,
            'time_range': time_range,
            'matrix': matrix,
            'labels': labels,
            'scatter_data': scatter_data,
            'network': network_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def calculate_simulated_correlation(domain1, field1, domain2, field2):
    """
    Calculate a simulated correlation coefficient.
    In production, this would use real data from the correlator.
    """
    # Generate a consistent correlation value based on the inputs
    # This ensures the same domains/fields always give the same correlation
    seed_value = hash(f"{domain1}_{field1}_{domain2}_{field2}") % 10000
    random.seed(seed_value)
    
    # Generate a correlation between -1 and 1, with bias toward strong correlations
    # for more interesting demo results
    correlation = (random.random() * 1.6) - 0.8
    
    # Clamp between -1 and 1
    correlation = max(-0.99, min(0.99, correlation))
    
    return correlation


def generate_matrix_data(domain1, field1, domain2, field2):
    """Generate a correlation matrix for visualization."""
    # Create related domain fields
    domain1_fields = [f"{field1}_daily", field1, f"{field1}_max", f"{field1}_min", f"{field1}_trend"]
    domain2_fields = [f"{field2}_daily", field2, f"{field2}_max", f"{field2}_min", f"{field2}_trend"]
    
    # Create readable labels
    labels = [f.replace('_', ' ').capitalize() for f in domain1_fields + domain2_fields]
    
    # Create matrix size
    size = len(labels)
    matrix = np.zeros((size, size))
    
    # Set diagonal to 1.0 (self-correlation)
    for i in range(size):
        matrix[i, i] = 1.0
    
    # Fill with simulated correlations
    for i in range(size):
        for j in range(i+1, size):
            # Generate a correlation value between -1 and 1
            seed_value = hash(f"{labels[i]}_{labels[j]}") % 10000
            random.seed(seed_value)
            
            # Higher correlation for related fields
            if (i < len(domain1_fields) and j < len(domain1_fields)) or \
               (i >= len(domain1_fields) and j >= len(domain1_fields)):
                # Same domain, higher correlation
                corr = 0.5 + (random.random() * 0.5)
            else:
                # Different domains
                corr = (random.random() * 1.4) - 0.7
                
            # Clamp between -1 and 1
            corr = max(-0.99, min(0.99, corr))
            
            # Correlation matrix is symmetric
            matrix[i, j] = corr
            matrix[j, i] = corr
    
    return matrix.tolist(), labels


def generate_scatter_data(correlation):
    """Generate scatter plot data points."""
    points = 30
    x_data = np.linspace(10, 100, points).tolist()
    
    # Add noise but maintain the correlation
    noise = np.random.normal(0, 15, points)
    y_data = [(correlation * x) + noise[i] for i, x in enumerate(x_data)]
    
    return {
        'x': x_data,
        'y': y_data
    }


def generate_network_data(domain1, domain2):
    """Generate network graph data for visualization."""
    # Define domains to include
    domains = ['Weather', 'Energy', 'Economic', 'Transportation', 'Social Media', 'Health']
    
    # Convert input domains to proper format
    domain1_name = domain1.replace('-', ' ').title()
    domain2_name = domain2.replace('-', ' ').title()
    
    # Ensure our domains are in the list
    if domain1_name not in domains:
        domains[0] = domain1_name
    if domain2_name not in domains:
        domains[1] = domain2_name
    
    # Create nodes
    nodes = [{'id': domain, 'group': i+1} for i, domain in enumerate(domains)]
    
    # Create links
    links = []
    
    # Generate links with realistic weighting
    for i, source in enumerate(domains):
        # Each domain should connect to at least one other
        num_connections = random.randint(1, 3)
        connected = []
        
        # Always connect our two main domains
        if source == domain1_name and domain2_name not in connected:
            # Use the actual correlation value if available
            seed_value = hash(f"{domain1}_{domain2}") % 10000
            random.seed(seed_value)
            value = 0.5 + (random.random() * 0.5)  # Stronger correlation for selected domains
            links.append({
                'source': source,
                'target': domain2_name,
                'value': value
            })
            connected.append(domain2_name)
        
        # Add additional random connections
        while len(connected) < num_connections:
            target_idx = random.randint(0, len(domains)-1)
            target = domains[target_idx]
            
            if target != source and target not in connected:
                # Generate a correlation strength
                seed_value = hash(f"{source}_{target}") % 10000
                random.seed(seed_value)
                value = random.random() * 0.8
                
                links.append({
                    'source': source,
                    'target': target,
                    'value': value
                })
                connected.append(target)
    
    return {
        'nodes': nodes,
        'links': links
    }