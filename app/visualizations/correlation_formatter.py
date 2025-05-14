"""
Correlation data formatter for visualizations
"""
from typing import Dict, List, Any, Optional, Tuple, Union
from app.visualizations.base_formatter import BaseFormatter

class CorrelationFormatter(BaseFormatter):
    """Formatter for correlation visualizations (heatmaps, networks, etc.)"""
    
    def __init__(self):
        """Initialize the correlation formatter"""
        super().__init__(
            name="Correlation Formatter",
            description="Formats correlation data for visualizations like heatmaps, network graphs, and bubble charts",
            visualization_types=["heatmap", "network", "bubble", "chord", "sankey"],
            data_types=["correlation", "cross-domain", "impact"]
        )
    
    def format(self, data: Dict[str, Any], visualization_type: str, 
              options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format correlation data for visualization
        
        Args:
            data: Input data to format
            visualization_type: Target visualization type
            options: Optional formatting options
            
        Returns:
            Formatted data ready for visualization
        """
        if options is None:
            options = {}
        
        # Detect data type and call appropriate formatter
        data_type = options.get('data_type', self._detect_data_type(data))
        
        try:
            if data_type == "correlation":
                # Standard correlation matrix
                return self._format_correlation_matrix(data, visualization_type, options)
            elif data_type == "cross-domain":
                # Cross-domain correlations
                return self._format_cross_domain(data, visualization_type, options)
            elif data_type == "impact":
                # Impact matrix/flow
                return self._format_impact_matrix(data, visualization_type, options)
            else:
                # Generic correlation data
                return self._format_generic_correlation(data, visualization_type, options)
        except Exception as e:
            self.error = e
            # Return a minimal working structure even on error
            return {
                'data_type': data_type,
                'visualization_type': visualization_type,
                'error': str(e),
                'data': []
            }
    
    def _detect_data_type(self, data: Dict[str, Any]) -> str:
        """Detect the type of correlation data"""
        if 'correlation_matrix' in data:
            return 'correlation'
        elif 'correlations' in data:
            return 'cross-domain'
        elif 'impact_matrix' in data:
            return 'impact'
        else:
            return 'generic'
    
    def _format_correlation_matrix(self, data: Dict[str, Any], visualization_type: str, 
                                 options: Dict[str, Any]) -> Dict[str, Any]:
        """Format correlation matrix data"""
        result = {
            'data_type': 'correlation',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Correlation Matrix'),
            'data': []
        }
        
        # Extract correlation matrix
        matrix = data.get('correlation_matrix', {})
        if not matrix:
            # Try alternate locations
            matrix = data.get('matrix', {})
        
        if not matrix:
            # Create empty result if no matrix found
            return result
        
        # Get variables/features
        variables = data.get('variables', list(matrix.keys()))
        
        if visualization_type == 'heatmap':
            # Format for heatmap
            heatmap_data = []
            for i, var1 in enumerate(variables):
                for j, var2 in enumerate(variables):
                    # Get correlation value
                    if var1 in matrix and var2 in matrix[var1]:
                        value = matrix[var1][var2]
                    else:
                        # Use symmetric property if value not found
                        value = matrix.get(var2, {}).get(var1, 0)
                    
                    heatmap_data.append([i, j, value])
            
            result['data'] = heatmap_data
            result['x_axis'] = variables
            result['y_axis'] = variables
            
        elif visualization_type == 'network':
            # Format for network graph
            nodes = []
            links = []
            
            # Create nodes
            for i, variable in enumerate(variables):
                nodes.append({
                    'id': variable,
                    'name': variable,
                    'group': options.get('groups', {}).get(variable, 1)
                })
            
            # Create links (edges)
            for i, var1 in enumerate(variables):
                for j, var2 in enumerate(variables):
                    if i >= j:  # Avoid duplicates
                        continue
                    
                    # Get correlation value
                    if var1 in matrix and var2 in matrix[var1]:
                        value = matrix[var1][var2]
                    else:
                        # Use symmetric property if value not found
                        value = matrix.get(var2, {}).get(var1, 0)
                    
                    # Only include significant correlations
                    if abs(value) >= options.get('threshold', 0.3):
                        links.append({
                            'source': var1,
                            'target': var2,
                            'value': abs(value),
                            'sign': 1 if value >= 0 else -1
                        })
            
            result['nodes'] = nodes
            result['links'] = links
            
        else:
            # Generic format (array of correlation values)
            formatted_data = []
            for var1 in variables:
                row = []
                for var2 in variables:
                    # Get correlation value
                    if var1 in matrix and var2 in matrix[var1]:
                        value = matrix[var1][var2]
                    else:
                        # Use symmetric property if value not found
                        value = matrix.get(var2, {}).get(var1, 0)
                    
                    row.append(value)
                formatted_data.append(row)
            
            result['data'] = formatted_data
            result['variables'] = variables
        
        return result
    
    def _format_cross_domain(self, data: Dict[str, Any], visualization_type: str, 
                           options: Dict[str, Any]) -> Dict[str, Any]:
        """Format cross-domain correlation data"""
        result = {
            'data_type': 'cross-domain',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Cross-Domain Correlations'),
            'data': []
        }
        
        # Extract correlations list
        correlations = data.get('correlations', [])
        
        if not correlations:
            # Try to find correlations in another location
            if 'data' in data and isinstance(data['data'], list):
                correlations = data['data']
        
        if not correlations:
            # Create empty result if no correlations found
            return result
        
        # Get all domains
        domains = set()
        for corr in correlations:
            if 'domains' in corr:
                domains.update(corr['domains'])
        
        domains = sorted(list(domains))
        
        if visualization_type == 'heatmap':
            # Create correlation matrix between domains
            matrix = []
            
            # Initialize empty matrix
            for i in range(len(domains)):
                row = [0] * len(domains)
                matrix.append(row)
            
            # Fill matrix with correlation values
            for corr in correlations:
                if 'domains' in corr and 'correlation' in corr:
                    domain1, domain2 = corr['domains'][0], corr['domains'][1]
                    value = corr['correlation']
                    
                    # Find indices
                    i = domains.index(domain1)
                    j = domains.index(domain2)
                    
                    # Update matrix (both directions for symmetric matrix)
                    matrix[i][j] = value
                    matrix[j][i] = value
            
            result['data'] = matrix
            result['x_axis'] = domains
            result['y_axis'] = domains
            
        elif visualization_type == 'network':
            # Format for network graph
            nodes = []
            links = []
            
            # Create nodes
            for domain in domains:
                nodes.append({
                    'id': domain,
                    'name': domain,
                    'group': options.get('domain_groups', {}).get(domain, 1)
                })
            
            # Create links
            for corr in correlations:
                if 'domains' in corr and 'correlation' in corr:
                    domain1, domain2 = corr['domains'][0], corr['domains'][1]
                    value = corr['correlation']
                    
                    # Only include significant correlations
                    if abs(value) >= options.get('threshold', 0.0):
                        links.append({
                            'source': domain1,
                            'target': domain2,
                            'value': abs(value),
                            'correlation': value,
                            'sign': 1 if value >= 0 else -1
                        })
            
            result['nodes'] = nodes
            result['links'] = links
            
        elif visualization_type == 'chord':
            # Format for chord diagram
            matrix = []
            
            # Initialize empty matrix
            for i in range(len(domains)):
                row = [0] * len(domains)
                matrix.append(row)
            
            # Fill matrix with correlation values (scaled for visualization)
            for corr in correlations:
                if 'domains' in corr and 'correlation' in corr:
                    domain1, domain2 = corr['domains'][0], corr['domains'][1]
                    value = abs(corr['correlation']) * 100  # Scale to 0-100
                    
                    # Find indices
                    i = domains.index(domain1)
                    j = domains.index(domain2)
                    
                    # Update matrix (both directions for chord diagram)
                    matrix[i][j] = value
                    matrix[j][i] = value
            
            result['matrix'] = matrix
            result['names'] = domains
            
        elif visualization_type == 'bubble':
            # Format for bubble chart
            bubbles = []
            
            for corr in correlations:
                if 'domains' in corr and 'correlation' in corr:
                    domain1, domain2 = corr['domains'][0], corr['domains'][1]
                    value = corr['correlation']
                    strength = corr.get('strength', self._get_correlation_strength(value))
                    
                    bubbles.append({
                        'x': domain1,
                        'y': domain2,
                        'z': abs(value),  # Bubble size
                        'name': f"{domain1}-{domain2}",
                        'correlation': value,
                        'strength': strength,
                        'color': value  # Color based on correlation value
                    })
            
            result['data'] = bubbles
            result['domains'] = domains
            
        else:
            # Default format (just pass correlations through)
            result['correlations'] = correlations
            result['domains'] = domains
        
        return result
    
    def _format_impact_matrix(self, data: Dict[str, Any], visualization_type: str, 
                            options: Dict[str, Any]) -> Dict[str, Any]:
        """Format impact matrix/flow data"""
        result = {
            'data_type': 'impact',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Impact Analysis'),
            'data': []
        }
        
        # Extract impact matrix
        impact_data = data.get('impact_matrix', {})
        if not impact_data:
            # Try alternate locations
            if 'impacts' in data:
                impact_data = {'impacts': data['impacts']}
        
        if not impact_data or 'impacts' not in impact_data:
            # Create empty result if no impact data found
            return result
        
        # Get domains
        domains = impact_data.get('domains', list(impact_data['impacts'].keys()))
        
        if visualization_type == 'heatmap':
            # Format for heatmap
            matrix = []
            
            # Convert impact data to matrix
            for source in domains:
                row = []
                for target in domains:
                    # Get impact value
                    value = impact_data['impacts'].get(source, {}).get(target, 0)
                    row.append(value)
                matrix.append(row)
            
            result['data'] = matrix
            result['x_axis'] = domains  # target domains
            result['y_axis'] = domains  # source domains
            
        elif visualization_type == 'network':
            # Format for network graph
            nodes = []
            links = []
            
            # Create nodes
            for domain in domains:
                nodes.append({
                    'id': domain,
                    'name': domain,
                    'group': options.get('domain_groups', {}).get(domain, 1)
                })
            
            # Create links based on impact
            for source in domains:
                for target in domains:
                    if source == target:
                        continue  # Skip self-impacts
                    
                    value = impact_data['impacts'].get(source, {}).get(target, 0)
                    
                    # Only include significant impacts
                    if value >= options.get('threshold', 0.2):
                        links.append({
                            'source': source,
                            'target': target,
                            'value': value,
                            'impact': value
                        })
            
            result['nodes'] = nodes
            result['links'] = links
            
        elif visualization_type == 'sankey':
            # Format for Sankey diagram
            nodes = []
            links = []
            
            # Create nodes
            for domain in domains:
                nodes.append({
                    'name': domain
                })
            
            # Create links based on impact
            for source in domains:
                for target in domains:
                    if source == target:
                        continue  # Skip self-impacts
                    
                    value = impact_data['impacts'].get(source, {}).get(target, 0)
                    
                    # Only include significant impacts
                    if value >= options.get('threshold', 0.2):
                        # Scale value for better visualization
                        scaled_value = value * 100  # Scale to 0-100
                        
                        links.append({
                            'source': domains.index(source),
                            'target': domains.index(target),
                            'value': scaled_value,
                            'unadjustedValue': value
                        })
            
            result['nodes'] = nodes
            result['links'] = links
            
        else:
            # Default format (just pass through)
            result['impacts'] = impact_data['impacts']
            result['domains'] = domains
        
        return result
    
    def _format_generic_correlation(self, data: Dict[str, Any], visualization_type: str, 
                                  options: Dict[str, Any]) -> Dict[str, Any]:
        """Format generic correlation data"""
        result = {
            'data_type': 'generic',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Correlation Analysis'),
            'data': []
        }
        
        # Try to find any correlation data
        correlation_data = None
        for key in ['data', 'correlations', 'matrix', 'relationships']:
            if key in data:
                correlation_data = data[key]
                break
        
        if not correlation_data:
            return result
        
        # Basic passthrough formatting
        result['data'] = correlation_data
        
        return result
    
    def _get_correlation_strength(self, value: float) -> str:
        """Get string description of correlation strength"""
        abs_val = abs(value)
        
        if abs_val >= 0.8:
            return "Very Strong"
        elif abs_val >= 0.6:
            return "Strong"
        elif abs_val >= 0.4:
            return "Moderate"
        elif abs_val >= 0.2:
            return "Weak"
        else:
            return "Very Weak"