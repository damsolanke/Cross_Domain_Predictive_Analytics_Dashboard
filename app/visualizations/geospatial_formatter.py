"""
Geospatial data formatter for maps and location-based visualizations
"""
from typing import Dict, List, Any, Optional, Tuple, Union
from app.visualizations.base_formatter import BaseFormatter

class GeospatialFormatter(BaseFormatter):
    """Formatter for geospatial and location-based visualizations"""
    
    def __init__(self):
        """Initialize the geospatial formatter"""
        super().__init__(
            name="Geospatial Formatter",
            description="Formats data for geographic visualizations, including maps, heatmaps, and route displays",
            visualization_types=["map", "choropleth", "heatmap", "route", "scatter"],
            data_types=["weather", "economic", "transportation", "social-media", "location"]
        )
    
    def format(self, data: Dict[str, Any], visualization_type: str, 
              options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format data for geospatial visualizations
        
        Args:
            data: Input data to format
            visualization_type: Target visualization type
            options: Optional formatting options
            
        Returns:
            Formatted data ready for visualization
        """
        if options is None:
            options = {}
        
        # Detect data type if not specified
        data_type = options.get('data_type', self._detect_data_type(data))
        
        try:
            if data_type == "weather":
                return self._format_weather_maps(data, visualization_type, options)
            elif data_type == "economic":
                return self._format_economic_maps(data, visualization_type, options)
            elif data_type == "transportation":
                return self._format_transportation_maps(data, visualization_type, options)
            elif data_type == "social-media":
                return self._format_social_media_maps(data, visualization_type, options)
            else:
                return self._format_generic_geospatial(data, visualization_type, options)
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
        """Detect the type of data for geospatial visualization"""
        # Check for explicit type
        if 'data_type' in data:
            return data['data_type']
        
        # Check for signature fields
        if 'weather' in data or 'forecast' in data:
            return 'weather'
        elif 'economic' in data or 'indicators' in data:
            return 'economic'
        elif 'traffic' in data or 'transportation' in data or 'routes' in data:
            return 'transportation'
        elif 'social' in data or 'trends' in data:
            return 'social-media'
        elif 'locations' in data or 'coordinates' in data or 'geo' in data:
            return 'location'
        
        # Default
        return 'generic'
    
    def _format_weather_maps(self, data: Dict[str, Any], visualization_type: str, 
                           options: Dict[str, Any]) -> Dict[str, Any]:
        """Format weather data for map visualization"""
        result = {
            'data_type': 'weather',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Weather Map'),
            'data': []
        }
        
        # Get weather data and locations
        weather_data = []
        
        # Try multiple possible data structures
        if 'locations' in data and isinstance(data['locations'], list):
            # Format: list of locations with embedded weather data
            weather_data = data['locations']
        elif 'weather_data' in data and isinstance(data['weather_data'], list):
            # Format: list of weather data points with location information
            weather_data = data['weather_data']
        elif 'data' in data and isinstance(data['data'], list):
            # Generic format
            weather_data = data['data']
        
        if not weather_data:
            return result
        
        # Get the metric to display
        metric = options.get('metric', 'temperature')
        
        if visualization_type == 'map' or visualization_type == 'scatter':
            # Format for point-based map
            points = []
            
            for point in weather_data:
                # Extract location
                location = self._extract_location(point)
                if not location:
                    continue
                
                # Extract value for the selected metric
                value = self._extract_weather_value(point, metric)
                if value is None:
                    continue
                
                # Create point data
                points.append({
                    'lat': location[0],
                    'lon': location[1],
                    'value': value,
                    'name': point.get('name', point.get('location', '')),
                    'metric': metric
                })
            
            result['data'] = points
            result['metric'] = metric
            result['metric_label'] = self._get_weather_metric_label(metric)
            
        elif visualization_type == 'choropleth':
            # Format for area-based map
            regions = []
            
            for point in weather_data:
                # Extract location
                location = self._extract_location(point)
                if not location:
                    continue
                
                # Extract region code
                region_code = point.get('region_code', point.get('code', ''))
                if not region_code:
                    continue
                
                # Extract value for the selected metric
                value = self._extract_weather_value(point, metric)
                if value is None:
                    continue
                
                # Create region data
                regions.append({
                    'code': region_code,
                    'value': value,
                    'name': point.get('name', point.get('location', '')),
                    'metric': metric
                })
            
            result['data'] = regions
            result['metric'] = metric
            result['metric_label'] = self._get_weather_metric_label(metric)
            
        elif visualization_type == 'heatmap':
            # Format for heatmap
            points = []
            
            for point in weather_data:
                # Extract location
                location = self._extract_location(point)
                if not location:
                    continue
                
                # Extract value for the selected metric
                value = self._extract_weather_value(point, metric)
                if value is None:
                    continue
                
                # Create point data
                points.append({
                    'lat': location[0],
                    'lon': location[1],
                    'value': value,
                    'weight': self._get_heatmap_weight(value, metric)
                })
            
            result['data'] = points
            result['metric'] = metric
            result['metric_label'] = self._get_weather_metric_label(metric)
            
        return result
    
    def _format_economic_maps(self, data: Dict[str, Any], visualization_type: str, 
                            options: Dict[str, Any]) -> Dict[str, Any]:
        """Format economic data for map visualization"""
        result = {
            'data_type': 'economic',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Economic Map'),
            'data': []
        }
        
        # Get economic data by region
        economic_data = []
        
        # Try multiple possible data structures
        if 'regions' in data and isinstance(data['regions'], list):
            economic_data = data['regions']
        elif 'countries' in data and isinstance(data['countries'], list):
            economic_data = data['countries']
        elif 'indicators' in data and isinstance(data['indicators'], dict):
            # Convert dict of country -> value to list format
            for country, value in data['indicators'].items():
                economic_data.append({
                    'country': country,
                    'value': value
                })
        elif 'data' in data and isinstance(data['data'], list):
            economic_data = data['data']
        
        if not economic_data:
            return result
        
        # Get the indicator to display
        indicator = options.get('indicator', 'gdp')
        
        if visualization_type == 'choropleth':
            # Format for choropleth map (countries/regions)
            regions = []
            
            for item in economic_data:
                # Extract country/region code
                code = item.get('code', item.get('country_code', ''))
                if not code:
                    # Try to extract from country name
                    country = item.get('country', item.get('name', ''))
                    code = self._get_country_code(country)
                
                if not code:
                    continue
                
                # Extract value for the selected indicator
                value = self._extract_economic_value(item, indicator)
                if value is None:
                    continue
                
                # Create region data
                regions.append({
                    'code': code,
                    'value': value,
                    'name': item.get('name', item.get('country', '')),
                    'indicator': indicator
                })
            
            result['data'] = regions
            result['indicator'] = indicator
            result['indicator_label'] = self._get_economic_indicator_label(indicator)
            
        elif visualization_type == 'map' or visualization_type == 'scatter':
            # Format for point-based map (cities/locations)
            points = []
            
            for item in economic_data:
                # Extract location
                location = self._extract_location(item)
                if not location:
                    continue
                
                # Extract value for the selected indicator
                value = self._extract_economic_value(item, indicator)
                if value is None:
                    continue
                
                # Create point data
                points.append({
                    'lat': location[0],
                    'lon': location[1],
                    'value': value,
                    'name': item.get('name', item.get('city', item.get('location', ''))),
                    'indicator': indicator
                })
            
            result['data'] = points
            result['indicator'] = indicator
            result['indicator_label'] = self._get_economic_indicator_label(indicator)
            
        return result
    
    def _format_transportation_maps(self, data: Dict[str, Any], visualization_type: str, 
                                  options: Dict[str, Any]) -> Dict[str, Any]:
        """Format transportation data for map visualization"""
        result = {
            'data_type': 'transportation',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Transportation Map'),
            'data': []
        }
        
        # Get transportation data
        if 'routes' in data and isinstance(data['routes'], list):
            # Format for route visualization
            routes = []
            
            for route in data['routes']:
                # Extract route path
                path = route.get('path', route.get('coordinates', []))
                if not path:
                    continue
                
                # Create route data
                routes.append({
                    'path': path,
                    'name': route.get('name', ''),
                    'type': route.get('type', 'route'),
                    'color': route.get('color', ''),
                    'congestion': route.get('congestion', 0)
                })
            
            result['data'] = routes
            
        elif 'hotspots' in data and isinstance(data['hotspots'], list):
            # Format for traffic hotspots
            hotspots = []
            
            for hotspot in data['hotspots']:
                # Extract location
                location = self._extract_location(hotspot)
                if not location:
                    continue
                
                # Create hotspot data
                hotspots.append({
                    'lat': location[0],
                    'lon': location[1],
                    'name': hotspot.get('name', ''),
                    'congestion': hotspot.get('congestion_level', 0),
                    'delay': hotspot.get('delay_minutes', 0)
                })
            
            result['data'] = hotspots
            
        elif 'traffic_data' in data and isinstance(data['traffic_data'], list):
            # Format for general traffic data
            traffic_points = []
            
            for point in data['traffic_data']:
                # Extract location
                location = self._extract_location(point)
                if not location:
                    continue
                
                # Get congestion value
                congestion = point.get('congestion_level', 0)
                
                # Create traffic point data
                traffic_points.append({
                    'lat': location[0],
                    'lon': location[1],
                    'congestion': congestion,
                    'speed': point.get('avg_speed_mph', 0),
                    'incidents': len(point.get('incidents', []))
                })
            
            result['data'] = traffic_points
            
        return result
    
    def _format_social_media_maps(self, data: Dict[str, Any], visualization_type: str, 
                                options: Dict[str, Any]) -> Dict[str, Any]:
        """Format social media data for map visualization"""
        result = {
            'data_type': 'social-media',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Social Media Trends Map'),
            'data': []
        }
        
        # Get the metric to display
        metric = options.get('metric', 'trend_intensity')
        
        if 'trends_by_location' in data and isinstance(data['trends_by_location'], list):
            # Format for trends by location
            locations = []
            
            for location in data['trends_by_location']:
                # Extract coordinates
                coords = self._extract_location(location)
                if not coords:
                    continue
                
                # Get value for selected metric
                value = self._extract_social_media_value(location, metric)
                if value is None:
                    continue
                
                # Create location data
                locations.append({
                    'lat': coords[0],
                    'lon': coords[1],
                    'name': location.get('name', ''),
                    'value': value,
                    'topics': location.get('trending_topics', [])[:3]  # Top 3 topics
                })
            
            result['data'] = locations
            result['metric'] = metric
            
        elif 'regional_sentiment' in data and isinstance(data['regional_sentiment'], list):
            # Format for sentiment by region
            regions = []
            
            for region in data['regional_sentiment']:
                # Get region code
                code = region.get('code', region.get('region_code', ''))
                if not code:
                    country = region.get('country', region.get('name', ''))
                    code = self._get_country_code(country)
                
                if not code:
                    continue
                
                # Get sentiment value
                sentiment = region.get('sentiment', {})
                value = sentiment.get('positive', 0) - sentiment.get('negative', 0)
                
                # Create region data
                regions.append({
                    'code': code,
                    'value': value,
                    'name': region.get('name', ''),
                    'positive': sentiment.get('positive', 0),
                    'negative': sentiment.get('negative', 0)
                })
            
            result['data'] = regions
            result['metric'] = 'net_sentiment'
            
        return result
    
    def _format_generic_geospatial(self, data: Dict[str, Any], visualization_type: str, 
                                 options: Dict[str, Any]) -> Dict[str, Any]:
        """Format generic geospatial data"""
        result = {
            'data_type': 'generic',
            'visualization_type': visualization_type,
            'title': options.get('title', 'Geospatial Data'),
            'data': []
        }
        
        # Try to find location data
        locations = []
        
        if 'locations' in data and isinstance(data['locations'], list):
            locations = data['locations']
        elif 'points' in data and isinstance(data['points'], list):
            locations = data['points']
        elif 'data' in data and isinstance(data['data'], list):
            locations = data['data']
        
        if not locations:
            return result
        
        # Format based on visualization type
        if visualization_type in ['map', 'scatter', 'heatmap']:
            # Format for point-based visualization
            points = []
            
            for location in locations:
                # Extract coordinates
                coords = self._extract_location(location)
                if not coords:
                    continue
                
                # Get value (try common field names)
                value = None
                for field in ['value', 'weight', 'magnitude', 'size', 'intensity']:
                    if field in location:
                        value = location[field]
                        break
                
                # Create point data
                point_data = {
                    'lat': coords[0],
                    'lon': coords[1],
                    'name': location.get('name', '')
                }
                
                if value is not None:
                    point_data['value'] = value
                
                points.append(point_data)
            
            result['data'] = points
            
        elif visualization_type == 'choropleth':
            # Format for region-based visualization
            regions = []
            
            for location in locations:
                # Get region code
                code = location.get('code', location.get('region', ''))
                if not code:
                    continue
                
                # Get value
                value = None
                for field in ['value', 'weight', 'magnitude', 'size', 'intensity']:
                    if field in location:
                        value = location[field]
                        break
                
                if value is None:
                    continue
                
                # Create region data
                regions.append({
                    'code': code,
                    'value': value,
                    'name': location.get('name', '')
                })
            
            result['data'] = regions
            
        return result
    
    def _extract_location(self, data: Dict[str, Any]) -> Optional[Tuple[float, float]]:
        """Extract latitude and longitude from data"""
        # Check for explicit lat/lon fields
        if 'lat' in data and 'lon' in data:
            return (data['lat'], data['lon'])
        
        if 'latitude' in data and 'longitude' in data:
            return (data['latitude'], data['longitude'])
        
        # Check for coordinates array
        if 'coordinates' in data and isinstance(data['coordinates'], list) and len(data['coordinates']) >= 2:
            return (data['coordinates'][0], data['coordinates'][1])
        
        # Check for location object
        if 'location' in data and isinstance(data['location'], dict):
            location = data['location']
            if 'lat' in location and 'lon' in location:
                return (location['lat'], location['lon'])
            if 'latitude' in location and 'longitude' in location:
                return (location['latitude'], location['longitude'])
        
        # Check for position array
        if 'position' in data and isinstance(data['position'], list) and len(data['position']) >= 2:
            return (data['position'][0], data['position'][1])
        
        return None
    
    def _extract_weather_value(self, data: Dict[str, Any], metric: str) -> Optional[float]:
        """Extract weather metric value"""
        # Check for direct metric field
        if metric in data:
            return data[metric]
        
        # Check weather data structure
        if 'weather' in data and isinstance(data['weather'], dict):
            weather = data['weather']
            if metric in weather:
                return weather[metric]
        
        # Check current data structure
        if 'current' in data and isinstance(data['current'], dict):
            current = data['current']
            if metric in current:
                return current[metric]
            
            # Check nested temp structure
            if 'temp' in current and isinstance(current['temp'], dict) and metric in current['temp']:
                return current['temp'][metric]
        
        # Handle specific metrics
        if metric == 'temperature':
            return data.get('temp', data.get('temperature'))
        elif metric == 'precipitation':
            return data.get('precipitation', data.get('precipitation_chance', data.get('rain', 0)))
        elif metric == 'humidity':
            return data.get('humidity')
        elif metric == 'wind_speed':
            return data.get('wind_speed', data.get('wind', {}).get('speed'))
        
        # Try value field as fallback
        return data.get('value')
    
    def _extract_economic_value(self, data: Dict[str, Any], indicator: str) -> Optional[float]:
        """Extract economic indicator value"""
        # Check for direct indicator field
        if indicator in data:
            return data[indicator]
        
        # Check for value field
        if 'value' in data:
            return data['value']
        
        # Handle specific indicators
        if indicator == 'gdp':
            return data.get('gdp', data.get('gdp_growth'))
        elif indicator == 'inflation':
            return data.get('inflation', data.get('inflation_rate'))
        elif indicator == 'unemployment':
            return data.get('unemployment', data.get('unemployment_rate'))
        elif indicator == 'interest_rate':
            return data.get('interest_rate')
        
        return None
    
    def _extract_social_media_value(self, data: Dict[str, Any], metric: str) -> Optional[float]:
        """Extract social media metric value"""
        # Check for direct metric field
        if metric in data:
            return data[metric]
        
        # Handle specific metrics
        if metric == 'trend_intensity':
            return data.get('intensity', data.get('trending_score', data.get('trend_score')))
        elif metric == 'sentiment':
            sentiment = data.get('sentiment', {})
            if isinstance(sentiment, dict):
                return sentiment.get('positive', 0) - sentiment.get('negative', 0)
            return sentiment  # If it's a direct value
        elif metric == 'engagement':
            return data.get('engagement', data.get('engagement_rate'))
        
        # Try value field as fallback
        return data.get('value')
    
    def _get_weather_metric_label(self, metric: str) -> str:
        """Get human-readable label for weather metric"""
        if metric == 'temperature':
            return 'Temperature (°C)'
        elif metric == 'precipitation':
            return 'Precipitation (mm)'
        elif metric == 'humidity':
            return 'Humidity (%)'
        elif metric == 'wind_speed':
            return 'Wind Speed (km/h)'
        elif metric == 'pressure':
            return 'Pressure (hPa)'
        
        return metric.capitalize()
    
    def _get_economic_indicator_label(self, indicator: str) -> str:
        """Get human-readable label for economic indicator"""
        if indicator == 'gdp':
            return 'GDP Growth (%)'
        elif indicator == 'inflation':
            return 'Inflation Rate (%)'
        elif indicator == 'unemployment':
            return 'Unemployment Rate (%)'
        elif indicator == 'interest_rate':
            return 'Interest Rate (%)'
        elif indicator == 'stock_market':
            return 'Stock Market Index'
        
        return indicator.capitalize()
    
    def _get_heatmap_weight(self, value: float, metric: str) -> float:
        """Calculate appropriate heatmap weight based on metric and value"""
        # Scale weight based on metric type
        if metric == 'temperature':
            # Higher weight for extreme temperatures (hot or cold)
            return abs(value - 20) / 10  # Weight increases as temp deviates from 20°C
        elif metric == 'precipitation':
            # Higher weight for more precipitation
            return min(1.0, value / 25)  # Scale: 0-25mm maps to 0-1 weight
        elif metric == 'humidity':
            # Higher weight for extreme humidity (very high or very low)
            return abs(value - 50) / 50  # Weight increases as humidity deviates from 50%
        
        # Default: direct scaling between 0-1
        return min(1.0, max(0.0, value))
    
    def _get_country_code(self, country_name: str) -> str:
        """Get ISO country code from country name (simplified)"""
        # Very simplified mapping for common countries
        country_map = {
            'united states': 'US',
            'usa': 'US',
            'canada': 'CA',
            'united kingdom': 'GB',
            'uk': 'GB',
            'australia': 'AU',
            'germany': 'DE',
            'france': 'FR',
            'japan': 'JP',
            'china': 'CN',
            'india': 'IN',
            'brazil': 'BR',
            'mexico': 'MX',
            'russia': 'RU',
            'south africa': 'ZA',
            'italy': 'IT',
            'spain': 'ES'
        }
        
        if not country_name:
            return ''
        
        # Normalize and lookup
        normalized = country_name.lower().strip()
        return country_map.get(normalized, '')