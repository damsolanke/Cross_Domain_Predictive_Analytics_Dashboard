"""
Dashboard formatter for combining multiple visualizations
"""
from typing import Dict, List, Any, Optional
from app.visualizations.base_formatter import BaseFormatter
from app.visualizations.time_series_formatter import TimeSeriesFormatter
from app.visualizations.correlation_formatter import CorrelationFormatter
from app.visualizations.geospatial_formatter import GeospatialFormatter

class DashboardFormatter(BaseFormatter):
    """Formatter for creating dashboard layouts with multiple visualizations"""
    
    def __init__(self):
        """Initialize the dashboard formatter"""
        super().__init__(
            name="Dashboard Formatter",
            description="Formats data for complete dashboards with multiple visualization components",
            visualization_types=["dashboard", "grid", "tabs", "composite"],
            data_types=["multi-domain", "cross-domain", "summary"]
        )
        
        # Initialize component formatters
        self.time_series_formatter = TimeSeriesFormatter()
        self.correlation_formatter = CorrelationFormatter()
        self.geospatial_formatter = GeospatialFormatter()
    
    def format(self, data: Dict[str, Any], visualization_type: str, 
              options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format data for dashboard visualization
        
        Args:
            data: Input data to format
            visualization_type: Target visualization type
            options: Optional formatting options
            
        Returns:
            Formatted data ready for visualization
        """
        if options is None:
            options = {}
        
        # Initialize result structure
        result = {
            'data_type': 'dashboard',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Analytics Dashboard'),
            'layout': options.get('layout', 'grid'),
            'components': []
        }
        
        try:
            # Detect data organization
            if 'domains' in data and isinstance(data['domains'], dict):
                # Format is { "domain1": {...}, "domain2": {...} }
                return self._format_domain_organized(data, visualization_type, options)
            elif 'components' in data and isinstance(data['components'], list):
                # Format is { "components": [{...}, {...}] }
                return self._format_component_organized(data, visualization_type, options)
            elif 'sections' in data and isinstance(data['sections'], list):
                # Format is { "sections": [{...}, {...}] }
                return self._format_section_organized(data, visualization_type, options)
            else:
                # Try to auto-detect structure and create appropriate components
                return self._format_auto_detect(data, visualization_type, options)
                
        except Exception as e:
            self.error = e
            # Return minimal working structure
            result['error'] = str(e)
            return result
    
    def _format_domain_organized(self, data: Dict[str, Any], visualization_type: str, 
                               options: Dict[str, Any]) -> Dict[str, Any]:
        """Format data organized by domains"""
        result = {
            'data_type': 'dashboard',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Cross-Domain Analytics Dashboard'),
            'layout': options.get('layout', 'grid'),
            'components': []
        }
        
        # Get domains data
        domains_data = data.get('domains', {})
        
        # Get layout configuration
        layout = options.get('layout', 'grid')
        layout_config = options.get('layout_config', {})
        
        # Process each domain
        for domain_name, domain_data in domains_data.items():
            # Create component for this domain
            component = self._create_domain_component(domain_name, domain_data, options)
            if component:
                result['components'].append(component)
        
        # Add cross-domain components if available
        if 'cross_domain' in data:
            cross_domain_components = self._create_cross_domain_components(
                data['cross_domain'], options)
            result['components'].extend(cross_domain_components)
        
        return result
    
    def _format_component_organized(self, data: Dict[str, Any], visualization_type: str, 
                                  options: Dict[str, Any]) -> Dict[str, Any]:
        """Format data organized by components"""
        result = {
            'data_type': 'dashboard',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Analytics Dashboard'),
            'layout': options.get('layout', 'grid'),
            'components': []
        }
        
        # Get components data
        components_data = data.get('components', [])
        
        # Process each component
        for component_data in components_data:
            component_type = component_data.get('type')
            component_options = component_data.get('options', {})
            
            # Create formatted component
            formatted_component = self._format_component(
                component_data.get('data', {}),
                component_type,
                component_options
            )
            
            # Add component metadata
            formatted_component.update({
                'id': component_data.get('id', f"component_{len(result['components'])}"),
                'title': component_data.get('title', ''),
                'width': component_data.get('width', 1),
                'height': component_data.get('height', 1),
                'position': component_data.get('position', {})
            })
            
            result['components'].append(formatted_component)
        
        return result
    
    def _format_section_organized(self, data: Dict[str, Any], visualization_type: str, 
                                options: Dict[str, Any]) -> Dict[str, Any]:
        """Format data organized by sections"""
        result = {
            'data_type': 'dashboard',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Analytics Dashboard'),
            'layout': options.get('layout', 'tabs'),  # Default to tabs for sections
            'sections': []
        }
        
        # Get sections data
        sections_data = data.get('sections', [])
        
        # Process each section
        for section_data in sections_data:
            section = {
                'id': section_data.get('id', f"section_{len(result['sections'])}"),
                'title': section_data.get('title', ''),
                'components': []
            }
            
            # Process components in this section
            for component_data in section_data.get('components', []):
                component_type = component_data.get('type')
                component_options = component_data.get('options', {})
                
                # Create formatted component
                formatted_component = self._format_component(
                    component_data.get('data', {}),
                    component_type,
                    component_options
                )
                
                # Add component metadata
                formatted_component.update({
                    'id': component_data.get('id', f"component_{len(section['components'])}"),
                    'title': component_data.get('title', ''),
                    'width': component_data.get('width', 1),
                    'height': component_data.get('height', 1),
                    'position': component_data.get('position', {})
                })
                
                section['components'].append(formatted_component)
            
            result['sections'].append(section)
        
        return result
    
    def _format_auto_detect(self, data: Dict[str, Any], visualization_type: str, 
                          options: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-detect data structure and create components"""
        result = {
            'data_type': 'dashboard',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Analytics Dashboard'),
            'layout': options.get('layout', 'grid'),
            'components': []
        }
        
        # Check for domain-specific data
        domains_to_check = ['weather', 'economic', 'transportation', 'social-media']
        
        for domain in domains_to_check:
            if domain in data:
                component = self._create_domain_component(domain, data[domain], options)
                if component:
                    result['components'].append(component)
        
        # Check for cross-domain correlations
        if 'correlations' in data or 'cross_domain' in data:
            cross_domain_data = data.get('cross_domain', data)
            cross_domain_components = self._create_cross_domain_components(cross_domain_data, options)
            result['components'].extend(cross_domain_components)
        
        # Check for predictions
        if 'predictions' in data:
            prediction_component = self._create_prediction_component(data, options)
            if prediction_component:
                result['components'].append(prediction_component)
        
        # If no components were created, try to create a generic component
        if not result['components']:
            generic_component = self._create_generic_component(data, options)
            if generic_component:
                result['components'].append(generic_component)
        
        return result
    
    def _create_domain_component(self, domain: str, domain_data: Dict[str, Any],
                               options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a dashboard component for a specific domain"""
        if not domain_data:
            return None
        
        # Initialize component
        component = {
            'id': f"{domain}_component",
            'title': self._get_domain_title(domain),
            'domain': domain,
            'type': 'composite',
            'width': options.get('domain_width', 1),
            'height': options.get('domain_height', 1),
            'subcomponents': []
        }
        
        # Detect time series data
        time_series_data = self._extract_time_series_data(domain_data)
        if time_series_data:
            time_series = self.time_series_formatter.format(
                time_series_data,
                'line',
                {'data_type': domain}
            )
            component['subcomponents'].append({
                'id': f"{domain}_timeseries",
                'title': 'Time Series',
                'visualization_type': 'line',
                'data': time_series
            })
        
        # Detect geospatial data
        geospatial_data = self._extract_geospatial_data(domain_data)
        if geospatial_data:
            # Determine map type based on data
            map_type = 'map'
            if 'regions' in geospatial_data or 'countries' in geospatial_data:
                map_type = 'choropleth'
            
            geospatial = self.geospatial_formatter.format(
                geospatial_data,
                map_type,
                {'data_type': domain}
            )
            component['subcomponents'].append({
                'id': f"{domain}_map",
                'title': 'Geographic Distribution',
                'visualization_type': map_type,
                'data': geospatial
            })
        
        # If no subcomponents were created, return None
        if not component['subcomponents']:
            return None
        
        return component
    
    def _create_cross_domain_components(self, data: Dict[str, Any], 
                                     options: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create components for cross-domain analysis"""
        components = []
        
        # Check for correlations
        if 'correlations' in data:
            # Format correlation data
            correlation_data = self.correlation_formatter.format(
                data,
                'heatmap',
                {'data_type': 'cross-domain'}
            )
            
            components.append({
                'id': 'cross_domain_correlation',
                'title': 'Cross-Domain Correlations',
                'visualization_type': 'heatmap',
                'data': correlation_data,
                'width': options.get('correlation_width', 1),
                'height': options.get('correlation_height', 1)
            })
            
            # Also add network visualization if there are sufficient correlations
            if len(data.get('correlations', [])) >= 3:
                network_data = self.correlation_formatter.format(
                    data,
                    'network',
                    {'data_type': 'cross-domain'}
                )
                
                components.append({
                    'id': 'cross_domain_network',
                    'title': 'Cross-Domain Relationship Network',
                    'visualization_type': 'network',
                    'data': network_data,
                    'width': options.get('network_width', 1),
                    'height': options.get('network_height', 1)
                })
        
        # Check for impact matrix
        if 'impact_matrix' in data:
            # Format impact data
            impact_data = self.correlation_formatter.format(
                data,
                'heatmap',
                {'data_type': 'impact'}
            )
            
            components.append({
                'id': 'domain_impact_matrix',
                'title': 'Domain Impact Analysis',
                'visualization_type': 'heatmap',
                'data': impact_data,
                'width': options.get('impact_width', 1),
                'height': options.get('impact_height', 1)
            })
        
        # Check for key insights
        if 'key_insights' in data.get('predictions', {}):
            insights = data['predictions']['key_insights']
            
            components.append({
                'id': 'key_insights',
                'title': 'Key Cross-Domain Insights',
                'visualization_type': 'text',
                'data': {
                    'insights': insights
                },
                'width': options.get('insights_width', 1),
                'height': options.get('insights_height', 1)
            })
        
        return components
    
    def _create_prediction_component(self, data: Dict[str, Any], 
                                  options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a component for predictions"""
        predictions = data.get('predictions', {})
        if not predictions:
            return None
        
        # Create component based on prediction structure
        component = {
            'id': 'predictions_component',
            'title': 'Cross-Domain Predictions',
            'type': 'composite',
            'width': options.get('prediction_width', 2),
            'height': options.get('prediction_height', 1),
            'subcomponents': []
        }
        
        # Check for time horizons
        horizons = ['short_term', 'medium_term', 'long_term']
        has_horizons = any(horizon in predictions for horizon in horizons)
        
        if has_horizons:
            # Create a subcomponent for each time horizon
            for horizon in horizons:
                if horizon in predictions:
                    horizon_preds = predictions[horizon]
                    
                    # Format for appropriate visualization
                    if isinstance(horizon_preds, list):
                        # Create a table or list view
                        component['subcomponents'].append({
                            'id': f"predictions_{horizon}",
                            'title': self._get_horizon_title(horizon),
                            'visualization_type': 'list',
                            'data': {
                                'predictions': horizon_preds,
                                'horizon': horizon
                            }
                        })
        else:
            # Try to format as time series
            time_series_data = self._extract_time_series_data(predictions)
            if time_series_data:
                time_series = self.time_series_formatter.format(
                    predictions,
                    'line',
                    {'data_type': 'prediction', 'include_confidence': True}
                )
                component['subcomponents'].append({
                    'id': 'predictions_timeseries',
                    'title': 'Prediction Time Series',
                    'visualization_type': 'line',
                    'data': time_series
                })
        
        # If no subcomponents were created, return None
        if not component['subcomponents']:
            return None
        
        return component
    
    def _create_generic_component(self, data: Dict[str, Any], 
                               options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a generic component when structure can't be determined"""
        # Try to create a simple visualization based on available data
        component = {
            'id': 'generic_component',
            'title': options.get('title', 'Data Overview'),
            'width': options.get('width', 1),
            'height': options.get('height', 1)
        }
        
        # Look for arrays of data that might be visualizable
        for key, value in data.items():
            if isinstance(value, list) and value:
                if all(isinstance(item, dict) for item in value):
                    # This might be time series or tabular data
                    if any('timestamp' in item or 'date' in item for item in value):
                        # Looks like time series
                        time_series = self.time_series_formatter.format(
                            {key: value},
                            'line',
                            {}
                        )
                        component['visualization_type'] = 'line'
                        component['data'] = time_series
                        return component
                    else:
                        # Looks like tabular data
                        component['visualization_type'] = 'table'
                        component['data'] = {
                            'columns': list(value[0].keys()),
                            'data': value
                        }
                        return component
        
        # If nothing visualizable was found
        return None
    
    def _format_component(self, data: Dict[str, Any], component_type: str, 
                        options: Dict[str, Any]) -> Dict[str, Any]:
        """Format a single component based on its type"""
        if not component_type:
            # Try to detect component type
            component_type = self._detect_component_type(data)
        
        # Use appropriate formatter based on component type
        if component_type in ['line', 'area', 'bar', 'candlestick', 'heatmap']:
            return {
                'visualization_type': component_type,
                'data': self.time_series_formatter.format(data, component_type, options)
            }
        elif component_type in ['heatmap', 'network', 'chord', 'bubble']:
            return {
                'visualization_type': component_type,
                'data': self.correlation_formatter.format(data, component_type, options)
            }
        elif component_type in ['map', 'choropleth', 'scatter', 'route']:
            return {
                'visualization_type': component_type,
                'data': self.geospatial_formatter.format(data, component_type, options)
            }
        else:
            # Default: pass through data
            return {
                'visualization_type': component_type,
                'data': data
            }
    
    def _detect_component_type(self, data: Dict[str, Any]) -> str:
        """Detect the appropriate visualization type for the data"""
        # Check for time series data
        if self._extract_time_series_data(data):
            return 'line'  # Default to line chart for time series
        
        # Check for correlation data
        if 'correlations' in data or 'correlation_matrix' in data:
            return 'heatmap'  # Default to heatmap for correlations
        
        # Check for geospatial data
        if self._extract_geospatial_data(data):
            # Determine appropriate map type
            if 'regions' in data or 'countries' in data:
                return 'choropleth'
            else:
                return 'map'
        
        # Default
        return 'table'
    
    def _extract_time_series_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract time series data from a data structure"""
        # Check for common time series fields
        time_series_fields = ['time_series', 'timeseries', 'series', 'data', 'values']
        for field in time_series_fields:
            if field in data and isinstance(data[field], list):
                items = data[field]
                if items and isinstance(items[0], dict):
                    # Check if items have timestamp/date fields
                    if any('timestamp' in item or 'date' in item or 'time' in item 
                          for item in items[:min(len(items), 3)]):
                        return {field: items}
        
        # Check for domain-specific time series
        if 'forecast' in data:
            return {'forecast': data['forecast']}
        if 'historical' in data:
            return {'historical': data['historical']}
        if 'traffic_data' in data:
            return {'traffic_data': data['traffic_data']}
        if 'sentiment_data' in data:
            return {'sentiment_data': data['sentiment_data']}
        
        return None
    
    def _extract_geospatial_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract geospatial data from a data structure"""
        # Check for common geospatial fields
        geospatial_fields = ['locations', 'points', 'coordinates', 'regions', 'countries']
        for field in geospatial_fields:
            if field in data and isinstance(data[field], list):
                items = data[field]
                if items and isinstance(items[0], dict):
                    # Check if items have location information
                    if any('lat' in item or 'latitude' in item or 'coordinates' in item 
                          or 'code' in item for item in items[:min(len(items), 3)]):
                        return {field: items}
        
        # Check for domain-specific geospatial data
        if 'hotspots' in data:
            return {'hotspots': data['hotspots']}
        if 'routes' in data:
            return {'routes': data['routes']}
        
        return None
    
    def _get_domain_title(self, domain: str) -> str:
        """Get human-readable title for a domain"""
        if domain == 'weather':
            return 'Weather Analysis'
        elif domain == 'economic':
            return 'Economic Indicators'
        elif domain == 'transportation':
            return 'Transportation Metrics'
        elif domain == 'social-media':
            return 'Social Media Trends'
        
        return domain.replace('_', ' ').title()
    
    def _get_horizon_title(self, horizon: str) -> str:
        """Get human-readable title for a time horizon"""
        if horizon == 'short_term':
            return 'Short-Term Predictions (1-3 days)'
        elif horizon == 'medium_term':
            return 'Medium-Term Predictions (1-2 weeks)'
        elif horizon == 'long_term':
            return 'Long-Term Predictions (1-3 months)'
        
        return horizon.replace('_', ' ').title()