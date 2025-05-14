"""
API routes for the Cross-Domain Predictive Analytics Dashboard.
"""

from flask import jsonify, request
from . import api
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
import numpy as np
import random
import datetime

# Initialize correlation analyzer
correlator = CrossDomainCorrelator()

@api.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'OK'})

@api.route('/system-status')
def system_status():
    """System status endpoint for the API module.
    This is used as a fallback for the frontend JavaScript."""
    return jsonify({
        "status": "active",
        "uptime": __import__('time').time() - __import__('time').time() + 3600,  # Mock 1-hour uptime
        "components": {
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
        },
        "processing_rate": 42.5,
        "queue_size": 12
    })

@api.route('/analytics/reports/correlation')
def analytics_reports_correlation():
    """Generate correlation analysis report."""
    format_type = request.args.get('format', 'html')
    days = int(request.args.get('days', '7'))
    
    # Generate a mock correlation report
    report_data = {
        "title": "Cross-Domain Correlation Analysis Report",
        "generated_at": datetime.datetime.now().isoformat(),
        "time_range": f"Last {days} days",
        "correlations": [
            {
                "domain1": "Weather",
                "field1": "Temperature",
                "domain2": "Energy",
                "field2": "Consumption",
                "correlation": 0.78,
                "significance": "high",
                "description": "Strong positive correlation between temperature and energy consumption."
            },
            {
                "domain1": "Weather",
                "field1": "Precipitation",
                "domain2": "Transportation",
                "field2": "Traffic Delay",
                "correlation": 0.65,
                "significance": "medium",
                "description": "Moderate positive correlation between precipitation and traffic delays."
            },
            {
                "domain1": "Economic",
                "field1": "Market Index",
                "domain2": "Social Media",
                "field2": "Sentiment",
                "correlation": 0.48,
                "significance": "medium",
                "description": "Moderate positive correlation between market performance and social sentiment."
            }
        ],
        "insights": [
            "Weather factors show the strongest correlation with energy usage patterns",
            "Transportation metrics are moderately influenced by weather conditions",
            "Economic indicators have weaker but still significant correlations with social sentiment"
        ],
        "recommendations": [
            "Consider integrated forecasting models for energy demand based on weather predictions",
            "Develop predictive traffic management systems incorporating weather forecast data",
            "Monitor social media sentiment as a potential early indicator for economic trends"
        ]
    }
    
    if format_type == 'json':
        return jsonify(report_data)
    elif format_type == 'md':
        # Generate a simple markdown report
        markdown = f"""# {report_data['title']}

Generated: {report_data['generated_at']}
Time Range: {report_data['time_range']}

## Top Correlations

"""
        for corr in report_data['correlations']:
            markdown += f"### {corr['domain1']} ({corr['field1']}) × {corr['domain2']} ({corr['field2']})\n\n"
            markdown += f"**Correlation Coefficient:** {corr['correlation']}\n\n"
            markdown += f"**Significance:** {corr['significance']}\n\n"
            markdown += f"**Description:** {corr['description']}\n\n"
        
        markdown += "## Key Insights\n\n"
        for insight in report_data['insights']:
            markdown += f"* {insight}\n"
        
        markdown += "\n## Recommendations\n\n"
        for rec in report_data['recommendations']:
            markdown += f"* {rec}\n"
            
        return markdown
    else:
        # For HTML format, you would typically render a template
        # Since we're just adding a quick mock, we'll return HTML directly
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report_data['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .correlation {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 4px; }}
                .high {{ border-left: 5px solid #28a745; }}
                .medium {{ border-left: 5px solid #ffc107; }}
                .low {{ border-left: 5px solid #6c757d; }}
                h1, h2, h3 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>{report_data['title']}</h1>
            <p><strong>Generated:</strong> {report_data['generated_at']}</p>
            <p><strong>Time Range:</strong> {report_data['time_range']}</p>
            
            <h2>Top Correlations</h2>
        """
        
        for corr in report_data['correlations']:
            html += f"""
            <div class="correlation {corr['significance']}">
                <h3>{corr['domain1']} ({corr['field1']}) × {corr['domain2']} ({corr['field2']})</h3>
                <p><strong>Correlation Coefficient:</strong> {corr['correlation']}</p>
                <p><strong>Significance:</strong> {corr['significance']}</p>
                <p><strong>Description:</strong> {corr['description']}</p>
            </div>
            """
        
        html += "<h2>Key Insights</h2><ul>"
        for insight in report_data['insights']:
            html += f"<li>{insight}</li>"
        html += "</ul>"
        
        html += "<h2>Recommendations</h2><ul>"
        for rec in report_data['recommendations']:
            html += f"<li>{rec}</li>"
        html += "</ul>"
        
        html += "</body></html>"
        return html

@api.route('/analytics/reports/list')
def analytics_reports_list():
    """Return a list of available reports."""
    # Generate mock report list
    reports = [
        {
            "name": "Correlation Analysis Report",
            "path": "/api/analytics/reports/correlation?format=html&days=7",
            "format": "html",
            "size": 15240,
            "created": (datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat()
        },
        {
            "name": "Weather Insights Report",
            "path": "/api/analytics/reports/insights?format=html&days=7&domain=weather",
            "format": "html",
            "size": 12480,
            "created": (datetime.datetime.now() - datetime.timedelta(hours=5)).isoformat()
        },
        {
            "name": "Prediction Performance Report",
            "path": "/api/analytics/reports/prediction?format=json&days=30",
            "format": "json",
            "size": 8920,
            "created": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
        }
    ]
    
    return jsonify(reports)

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