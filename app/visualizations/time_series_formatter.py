"""
Time series data formatter for visualizations
"""
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from app.visualizations.base_formatter import BaseFormatter

class TimeSeriesFormatter(BaseFormatter):
    """Formatter for time series visualizations"""
    
    def __init__(self):
        """Initialize the time series formatter"""
        super().__init__(
            name="Time Series Formatter",
            description="Formats data for time series visualizations, including line charts, area charts, and bar charts",
            visualization_types=["line", "area", "bar", "candlestick", "heatmap"],
            data_types=["weather", "economic", "transportation", "social-media", "prediction"]
        )
    
    def format(self, data: Dict[str, Any], visualization_type: str, 
              options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format data for time series visualizations
        
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
        data_type = self._detect_data_type(data)
        
        try:
            if data_type == "weather":
                return self._format_weather_data(data, visualization_type, options)
            elif data_type == "economic":
                return self._format_economic_data(data, visualization_type, options)
            elif data_type == "transportation":
                return self._format_transportation_data(data, visualization_type, options)
            elif data_type == "social-media":
                return self._format_social_media_data(data, visualization_type, options)
            elif data_type == "prediction":
                return self._format_prediction_data(data, visualization_type, options)
            else:
                return self._format_generic_time_series(data, visualization_type, options)
        except Exception as e:
            self.error = e
            # Return a minimal working structure even on error
            return {
                'data_type': data_type,
                'visualization_type': visualization_type,
                'error': str(e),
                'x_axis': {
                    'type': 'time',
                    'label': 'Time'
                },
                'y_axis': {
                    'type': 'linear',
                    'label': 'Value'
                },
                'series': []
            }
    
    def _detect_data_type(self, data: Dict[str, Any]) -> str:
        """Detect the type of data being formatted"""
        # Check for explicit data type
        if 'data_type' in data:
            return data['data_type']
        
        # Look for signature fields
        if 'current' in data and ('temp' in data.get('current', {}) or 'weather' in data.get('current', {})):
            return 'weather'
        elif 'indicator' in data and data['indicator'] in ['inflation', 'gdp', 'stock_market', 'interest_rates']:
            return 'economic'
        elif 'traffic_data' in data or 'congestion' in data.get('current_stats', {}):
            return 'transportation'
        elif 'trending_topics' in data or 'sentiment_data' in data:
            return 'social-media'
        elif 'predictions' in data or 'confidence' in data:
            return 'prediction'
        
        # Default
        return 'generic'
    
    def _format_weather_data(self, data: Dict[str, Any], visualization_type: str, 
                           options: Dict[str, Any]) -> Dict[str, Any]:
        """Format weather data for time series visualization"""
        result = {
            'data_type': 'weather',
            'visualization_type': visualization_type,
            'x_axis': {
                'type': 'time',
                'label': 'Time'
            },
            'y_axis': {
                'type': 'linear',
                'label': self._get_weather_metric_label(options)
            },
            'series': []
        }
        
        # Find time series data in different possible locations
        time_series_data = None
        if 'forecast' in data:
            time_series_data = data['forecast']
        elif 'historical' in data:
            time_series_data = data['historical']
        elif 'data' in data and isinstance(data['data'], list):
            time_series_data = data['data']
        elif 'weather_data' in data and isinstance(data['weather_data'], list):
            time_series_data = data['weather_data']
        
        if not time_series_data:
            # Return empty result if no time series data found
            return result
        
        # Get selected metric or default to temperature
        metric = options.get('metric', 'temperature')
        
        # Create series data
        series = {
            'name': self._get_weather_metric_label({'metric': metric}),
            'data': []
        }
        
        # Process data points
        for point in time_series_data:
            # Extract time
            timestamp = self._extract_timestamp(point)
            
            # Extract value based on metric
            value = self._extract_weather_metric(point, metric)
            
            if timestamp and value is not None:
                series['data'].append({
                    'x': timestamp,
                    'y': value
                })
        
        # Add series to result
        result['series'].append(series)
        
        # Add additional series if requested
        if options.get('include_min_max', False) and metric == 'temperature':
            # Add min/max temperature series
            min_series = {
                'name': 'Min Temperature',
                'data': []
            }
            max_series = {
                'name': 'Max Temperature',
                'data': []
            }
            
            for point in time_series_data:
                timestamp = self._extract_timestamp(point)
                min_temp = self._extract_weather_metric(point, 'min_temperature')
                max_temp = self._extract_weather_metric(point, 'max_temperature')
                
                if timestamp:
                    if min_temp is not None:
                        min_series['data'].append({
                            'x': timestamp,
                            'y': min_temp
                        })
                    
                    if max_temp is not None:
                        max_series['data'].append({
                            'x': timestamp,
                            'y': max_temp
                        })
            
            # Add series if they have data
            if min_series['data']:
                result['series'].append(min_series)
            if max_series['data']:
                result['series'].append(max_series)
        
        return result
    
    def _format_economic_data(self, data: Dict[str, Any], visualization_type: str, 
                            options: Dict[str, Any]) -> Dict[str, Any]:
        """Format economic data for time series visualization"""
        result = {
            'data_type': 'economic',
            'visualization_type': visualization_type,
            'x_axis': {
                'type': 'time',
                'label': 'Time'
            },
            'y_axis': {
                'type': 'linear',
                'label': self._get_economic_metric_label(options)
            },
            'series': []
        }
        
        # Find time series data
        time_series_data = None
        if 'data' in data and isinstance(data['data'], list):
            time_series_data = data['data']
        elif 'economic_data' in data and isinstance(data['economic_data'], list):
            time_series_data = data['economic_data']
        
        if not time_series_data:
            # Return empty result if no time series data found
            return result
        
        # Get indicator type
        indicator = data.get('indicator', options.get('indicator', 'inflation'))
        
        # Create series data
        series = {
            'name': self._get_economic_indicator_name(indicator),
            'data': []
        }
        
        # Process data points
        for point in time_series_data:
            # Extract time
            timestamp = self._extract_timestamp(point)
            
            # Extract value
            value = point.get('value')
            
            if timestamp and value is not None:
                series['data'].append({
                    'x': timestamp,
                    'y': value
                })
        
        # Add series to result
        result['series'].append(series)
        
        # Add confidence bands if available and requested
        if options.get('include_confidence', False) and 'confidence' in time_series_data[0]:
            upper_series = {
                'name': 'Upper Confidence',
                'data': [],
                'type': 'area',
                'fillOpacity': 0.2
            }
            
            lower_series = {
                'name': 'Lower Confidence',
                'data': [],
                'type': 'area',
                'fillOpacity': 0.2
            }
            
            for point in time_series_data:
                timestamp = self._extract_timestamp(point)
                value = point.get('value', 0)
                confidence = point.get('confidence', 0.5)
                
                # Calculate confidence band (±2σ)
                confidence_range = value * (1 - confidence)
                
                if timestamp:
                    upper_series['data'].append({
                        'x': timestamp,
                        'y': value + confidence_range
                    })
                    
                    lower_series['data'].append({
                        'x': timestamp,
                        'y': max(0, value - confidence_range)
                    })
            
            if upper_series['data']:
                result['series'].append(upper_series)
            if lower_series['data']:
                result['series'].append(lower_series)
        
        return result
    
    def _format_transportation_data(self, data: Dict[str, Any], visualization_type: str, 
                                  options: Dict[str, Any]) -> Dict[str, Any]:
        """Format transportation data for time series visualization"""
        result = {
            'data_type': 'transportation',
            'visualization_type': visualization_type,
            'x_axis': {
                'type': 'time',
                'label': 'Time'
            },
            'y_axis': {
                'type': 'linear',
                'label': self._get_transportation_metric_label(options)
            },
            'series': []
        }
        
        # Find time series data
        time_series_data = None
        if 'traffic_data' in data and isinstance(data['traffic_data'], list):
            time_series_data = data['traffic_data']
        elif 'ridership_data' in data and isinstance(data['ridership_data'], list):
            time_series_data = data['ridership_data']
        elif 'data' in data and isinstance(data['data'], list):
            time_series_data = data['data']
        
        if not time_series_data:
            # Return empty result if no time series data found
            return result
        
        # Get selected metric or default to congestion
        metric = options.get('metric', 'congestion')
        
        # Create series data
        series = {
            'name': self._get_transportation_metric_label({'metric': metric}),
            'data': []
        }
        
        # Process data points
        for point in time_series_data:
            # Extract time
            timestamp = self._extract_timestamp(point)
            
            # Extract value based on metric
            value = self._extract_transportation_metric(point, metric)
            
            if timestamp and value is not None:
                series['data'].append({
                    'x': timestamp,
                    'y': value
                })
        
        # Add series to result
        result['series'].append(series)
        
        # Add related series if requested and available
        if options.get('include_related', False):
            # For congestion, also show avg_speed
            if metric == 'congestion' and 'avg_speed_mph' in time_series_data[0]:
                speed_series = {
                    'name': 'Average Speed (mph)',
                    'data': [],
                    'yAxis': 1  # Use secondary axis
                }
                
                for point in time_series_data:
                    timestamp = self._extract_timestamp(point)
                    speed = point.get('avg_speed_mph')
                    
                    if timestamp and speed is not None:
                        speed_series['data'].append({
                            'x': timestamp,
                            'y': speed
                        })
                
                if speed_series['data']:
                    # Add secondary y-axis
                    result['y_axis_secondary'] = {
                        'type': 'linear',
                        'label': 'Speed (mph)',
                        'opposite': True
                    }
                    result['series'].append(speed_series)
        
        return result
    
    def _format_social_media_data(self, data: Dict[str, Any], visualization_type: str, 
                                options: Dict[str, Any]) -> Dict[str, Any]:
        """Format social media data for time series visualization"""
        result = {
            'data_type': 'social-media',
            'visualization_type': visualization_type,
            'x_axis': {
                'type': 'time',
                'label': 'Time'
            },
            'y_axis': {
                'type': 'linear',
                'label': self._get_social_media_metric_label(options)
            },
            'series': []
        }
        
        # Find time series data
        time_series_data = None
        if 'sentiment_data' in data and isinstance(data['sentiment_data'], list):
            time_series_data = data['sentiment_data']
        elif 'engagement_timeline' in data and isinstance(data['engagement_timeline'], list):
            time_series_data = data['engagement_timeline']
        elif 'data' in data and isinstance(data['data'], list):
            time_series_data = data['data']
        
        if not time_series_data:
            # Return empty result if no time series data found
            return result
        
        # Get selected metric or default to sentiment
        data_type = options.get('data_type', 'sentiment')
        
        if data_type == 'sentiment':
            # Create sentiment series
            positive_series = {
                'name': 'Positive Sentiment',
                'data': []
            }
            
            negative_series = {
                'name': 'Negative Sentiment',
                'data': []
            }
            
            neutral_series = {
                'name': 'Neutral Sentiment',
                'data': []
            }
            
            # Process data points
            for point in time_series_data:
                # Extract time
                timestamp = self._extract_timestamp(point)
                
                # Extract sentiment values
                sentiment = point.get('sentiment', {})
                
                if timestamp and sentiment:
                    positive = sentiment.get('positive')
                    if positive is not None:
                        positive_series['data'].append({
                            'x': timestamp,
                            'y': positive
                        })
                    
                    negative = sentiment.get('negative')
                    if negative is not None:
                        negative_series['data'].append({
                            'x': timestamp,
                            'y': negative
                        })
                    
                    neutral = sentiment.get('neutral')
                    if neutral is not None:
                        neutral_series['data'].append({
                            'x': timestamp,
                            'y': neutral
                        })
            
            # Add series to result
            if positive_series['data']:
                result['series'].append(positive_series)
            if negative_series['data']:
                result['series'].append(negative_series)
            if neutral_series['data']:
                result['series'].append(neutral_series)
                
        elif data_type == 'engagement':
            # Create engagement series
            likes_series = {
                'name': 'Likes',
                'data': []
            }
            
            shares_series = {
                'name': 'Shares',
                'data': []
            }
            
            comments_series = {
                'name': 'Comments',
                'data': []
            }
            
            # Process data points
            for point in time_series_data:
                # Extract time
                timestamp = self._extract_timestamp(point)
                
                if timestamp:
                    likes = point.get('likes')
                    if likes is not None:
                        likes_series['data'].append({
                            'x': timestamp,
                            'y': likes
                        })
                    
                    shares = point.get('shares')
                    if shares is not None:
                        shares_series['data'].append({
                            'x': timestamp,
                            'y': shares
                        })
                    
                    comments = point.get('comments')
                    if comments is not None:
                        comments_series['data'].append({
                            'x': timestamp,
                            'y': comments
                        })
            
            # Add series to result
            if likes_series['data']:
                result['series'].append(likes_series)
            if shares_series['data']:
                result['series'].append(shares_series)
            if comments_series['data']:
                result['series'].append(comments_series)
        
        return result
    
    def _format_prediction_data(self, data: Dict[str, Any], visualization_type: str, 
                              options: Dict[str, Any]) -> Dict[str, Any]:
        """Format prediction data for time series visualization"""
        result = {
            'data_type': 'prediction',
            'visualization_type': visualization_type,
            'x_axis': {
                'type': 'time',
                'label': 'Time'
            },
            'y_axis': {
                'type': 'linear',
                'label': self._get_prediction_metric_label(options)
            },
            'series': []
        }
        
        # Find prediction data
        predictions = None
        if 'predictions' in data and isinstance(data['predictions'], list):
            predictions = data['predictions']
        elif 'periods' in data and isinstance(data['periods'], list):
            predictions = data['periods']
        
        if not predictions:
            # Return empty result if no predictions found
            return result
        
        # Get prediction metric
        metric = options.get('metric', self._detect_prediction_metric(predictions[0]))
        
        # Create prediction series
        prediction_series = {
            'name': self._get_prediction_metric_label({'metric': metric}),
            'data': []
        }
        
        # Process predictions
        for point in predictions:
            # Extract time
            timestamp = self._extract_timestamp(point)
            
            # Extract value
            value = self._extract_prediction_metric(point, metric)
            
            if timestamp and value is not None:
                prediction_series['data'].append({
                    'x': timestamp,
                    'y': value
                })
        
        # Add series to result
        result['series'].append(prediction_series)
        
        # Add confidence bands if requested and available
        if options.get('include_confidence', True) and 'confidence' in predictions[0]:
            confidence_positive = {
                'name': 'Upper Confidence',
                'data': [],
                'type': 'arearange' if visualization_type == 'arearange' else 'line',
                'dashStyle': 'dash',
                'lineWidth': 1,
                'color': 'rgba(0, 0, 200, 0.2)',
                'fillOpacity': 0.2
            }
            
            confidence_negative = {
                'name': 'Lower Confidence',
                'data': [],
                'type': 'arearange' if visualization_type == 'arearange' else 'line',
                'dashStyle': 'dash',
                'lineWidth': 1,
                'color': 'rgba(0, 0, 200, 0.2)',
                'fillOpacity': 0.2
            }
            
            # For specialized range visualization
            confidence_range = {
                'name': 'Confidence Range',
                'data': [],
                'type': 'arearange',
                'color': 'rgba(0, 0, 200, 0.2)',
                'fillOpacity': 0.2
            }
            
            for point in predictions:
                timestamp = self._extract_timestamp(point)
                value = self._extract_prediction_metric(point, metric)
                confidence = point.get('confidence', 0.8)
                
                if timestamp and value is not None:
                    # Calculate confidence interval based on confidence level
                    # Higher confidence = narrower band
                    range_size = value * (1 - confidence) * 2
                    upper = value + range_size / 2
                    lower = max(0, value - range_size / 2)
                    
                    confidence_positive['data'].append({
                        'x': timestamp,
                        'y': upper
                    })
                    
                    confidence_negative['data'].append({
                        'x': timestamp,
                        'y': lower
                    })
                    
                    confidence_range['data'].append({
                        'x': timestamp,
                        'low': lower,
                        'high': upper
                    })
            
            # Add appropriate confidence visualization
            if visualization_type == 'arearange' and confidence_range['data']:
                result['series'].append(confidence_range)
            elif confidence_positive['data'] and confidence_negative['data']:
                result['series'].append(confidence_positive)
                result['series'].append(confidence_negative)
        
        # Add historical data if available
        if 'historical' in data and isinstance(data['historical'], list):
            historical_series = {
                'name': 'Historical',
                'data': [],
                'dashStyle': 'solid',
                'lineWidth': 2,
                'color': 'rgba(0, 0, 0, 0.8)'
            }
            
            for point in data['historical']:
                timestamp = self._extract_timestamp(point)
                value = self._extract_prediction_metric(point, metric)
                
                if timestamp and value is not None:
                    historical_series['data'].append({
                        'x': timestamp,
                        'y': value
                    })
            
            if historical_series['data']:
                # Insert historical data at beginning
                result['series'].insert(0, historical_series)
        
        return result
    
    def _format_generic_time_series(self, data: Dict[str, Any], visualization_type: str, 
                                  options: Dict[str, Any]) -> Dict[str, Any]:
        """Format generic time series data"""
        result = {
            'data_type': 'generic',
            'visualization_type': visualization_type,
            'x_axis': {
                'type': 'time',
                'label': options.get('x_label', 'Time')
            },
            'y_axis': {
                'type': 'linear',
                'label': options.get('y_label', 'Value')
            },
            'series': []
        }
        
        # Try to find time series data
        time_series_data = None
        for key in ['data', 'time_series', 'values', 'points']:
            if key in data and isinstance(data[key], list) and data[key]:
                time_series_data = data[key]
                break
        
        if not time_series_data:
            # Return empty result if no time series data found
            return result
        
        # Create series data
        series = {
            'name': options.get('series_name', 'Data'),
            'data': []
        }
        
        # Look for x and y fields
        x_field = options.get('x_field', self._detect_time_field(time_series_data[0]))
        y_field = options.get('y_field', self._detect_value_field(time_series_data[0]))
        
        # Process data points
        for point in time_series_data:
            x_value = point.get(x_field)
            y_value = point.get(y_field)
            
            if x_value is not None and y_value is not None:
                # Convert to timestamp if it's a date
                if isinstance(x_value, str) and self._is_timestamp(x_value):
                    x_value = self._parse_timestamp(x_value)
                
                series['data'].append({
                    'x': x_value,
                    'y': y_value
                })
        
        # Add series to result
        result['series'].append(series)
        
        return result
    
    def _extract_timestamp(self, data_point: Dict[str, Any]) -> Optional[str]:
        """Extract timestamp from a data point"""
        # Check common timestamp fields
        for field in ['timestamp', 'date', 'time', 'datetime', 'period']:
            if field in data_point:
                value = data_point[field]
                if isinstance(value, str) and self._is_timestamp(value):
                    return value
                return value
        
        return None
    
    def _is_timestamp(self, value: str) -> bool:
        """Check if a string is a timestamp"""
        # Check for ISO format (simplistic)
        if re.match(r'\d{4}-\d{2}-\d{2}', value):
            return True
        # Check for Unix timestamp
        if value.isdigit() and len(value) >= 10:
            return True
        return False
    
    def _parse_timestamp(self, timestamp: str) -> str:
        """Parse a timestamp string to standard format"""
        try:
            # If it's already an ISO timestamp
            if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', timestamp):
                return timestamp
            
            # If it's a date only
            if re.match(r'\d{4}-\d{2}-\d{2}$', timestamp):
                return f"{timestamp}T00:00:00Z"
            
            # If it's a Unix timestamp
            if timestamp.isdigit():
                return datetime.fromtimestamp(int(timestamp)).isoformat()
            
            # Try to parse as datetime
            return datetime.fromisoformat(timestamp).isoformat()
        except:
            # Return original on error
            return timestamp
    
    def _extract_weather_metric(self, data_point: Dict[str, Any], metric: str) -> Optional[float]:
        """Extract weather metric from a data point"""
        if metric == 'temperature':
            # Check different possible locations
            if 'temp' in data_point:
                return data_point['temp']
            elif 'temperature' in data_point:
                return data_point['temperature']
            elif 'temp' in data_point.get('temp', {}):
                return data_point['temp']['day']
        
        elif metric == 'min_temperature':
            if 'temp_min' in data_point:
                return data_point['temp_min']
            elif 'min' in data_point.get('temp', {}):
                return data_point['temp']['min']
        
        elif metric == 'max_temperature':
            if 'temp_max' in data_point:
                return data_point['temp_max']
            elif 'max' in data_point.get('temp', {}):
                return data_point['temp']['max']
        
        elif metric == 'humidity':
            return data_point.get('humidity')
        
        elif metric == 'precipitation_chance':
            return data_point.get('precipitation_chance')
        
        # Try generic 'value' field
        return data_point.get('value')
    
    def _extract_transportation_metric(self, data_point: Dict[str, Any], metric: str) -> Optional[float]:
        """Extract transportation metric from a data point"""
        if metric == 'congestion':
            return data_point.get('congestion_level')
        elif metric == 'speed':
            return data_point.get('avg_speed_mph')
        elif metric == 'ridership':
            return data_point.get('ridership')
        elif metric == 'on_time':
            return data_point.get('on_time_percentage')
        
        # Try generic 'value' field
        return data_point.get('value')
    
    def _extract_prediction_metric(self, data_point: Dict[str, Any], metric: str) -> Optional[float]:
        """Extract prediction metric from a data point"""
        # Check for the metric directly
        if metric in data_point:
            return data_point[metric]
        
        # Check for 'value' field
        if 'value' in data_point:
            return data_point['value']
        
        # If no metric specified, try to find any numeric value
        for key, value in data_point.items():
            if isinstance(value, (int, float)) and key not in ['confidence', 'timestamp', 'date', 'time']:
                return value
        
        return None
    
    def _detect_prediction_metric(self, data_point: Dict[str, Any]) -> str:
        """Detect the main metric in a prediction data point"""
        # Check common metrics
        for key in ['temperature', 'precipitation', 'congestion', 'gdp_growth', 'inflation', 'ridership']:
            if key in data_point:
                return key
        
        # Check for 'value' field
        if 'value' in data_point:
            return 'value'
        
        # Default
        return 'prediction'
    
    def _detect_time_field(self, data_point: Dict[str, Any]) -> str:
        """Detect the field containing time information"""
        for key in ['timestamp', 'date', 'time', 'datetime', 'x']:
            if key in data_point:
                return key
        return 'x'
    
    def _detect_value_field(self, data_point: Dict[str, Any]) -> str:
        """Detect the field containing value information"""
        for key in ['value', 'y', 'data']:
            if key in data_point:
                return key
        
        # Try to find a numeric value
        for key, value in data_point.items():
            if isinstance(value, (int, float)) and key not in ['timestamp', 'date', 'time', 'x']:
                return key
        
        return 'y'
    
    def _get_weather_metric_label(self, options: Dict[str, Any]) -> str:
        """Get label for weather metric"""
        metric = options.get('metric', 'temperature')
        units = options.get('units', 'metric')
        
        if metric == 'temperature':
            if units == 'metric':
                return 'Temperature (°C)'
            else:
                return 'Temperature (°F)'
        elif metric == 'min_temperature':
            if units == 'metric':
                return 'Min Temperature (°C)'
            else:
                return 'Min Temperature (°F)'
        elif metric == 'max_temperature':
            if units == 'metric':
                return 'Max Temperature (°C)'
            else:
                return 'Max Temperature (°F)'
        elif metric == 'humidity':
            return 'Humidity (%)'
        elif metric == 'precipitation_chance':
            return 'Precipitation Probability (%)'
        
        return 'Value'
    
    def _get_economic_metric_label(self, options: Dict[str, Any]) -> str:
        """Get label for economic metric"""
        indicator = options.get('indicator', 'generic')
        
        if indicator == 'inflation':
            return 'Inflation Rate (%)'
        elif indicator == 'gdp':
            return 'GDP Growth (%)'
        elif indicator == 'stock_market':
            return 'Index Value'
        elif indicator == 'interest_rates':
            return 'Interest Rate (%)'
        elif indicator == 'currency':
            return 'Exchange Rate'
        
        return 'Value'
    
    def _get_economic_indicator_name(self, indicator: str) -> str:
        """Get human-readable name for economic indicator"""
        if indicator == 'inflation':
            return 'Inflation Rate'
        elif indicator == 'gdp':
            return 'GDP Growth'
        elif indicator == 'stock_market':
            return 'Stock Market Index'
        elif indicator == 'interest_rates':
            return 'Interest Rate'
        elif indicator == 'currency':
            return 'Currency Exchange Rate'
        
        return indicator.capitalize()
    
    def _get_transportation_metric_label(self, options: Dict[str, Any]) -> str:
        """Get label for transportation metric"""
        metric = options.get('metric', 'congestion')
        
        if metric == 'congestion':
            return 'Congestion Level'
        elif metric == 'speed':
            return 'Average Speed (mph)'
        elif metric == 'ridership':
            return 'Ridership'
        elif metric == 'on_time':
            return 'On-Time Performance (%)'
        
        return 'Value'
    
    def _get_social_media_metric_label(self, options: Dict[str, Any]) -> str:
        """Get label for social media metric"""
        data_type = options.get('data_type', 'sentiment')
        
        if data_type == 'sentiment':
            return 'Sentiment'
        elif data_type == 'engagement':
            return 'Engagement'
        
        return 'Value'
    
    def _get_prediction_metric_label(self, options: Dict[str, Any]) -> str:
        """Get label for prediction metric"""
        metric = options.get('metric', 'prediction')
        
        if metric == 'temperature':
            return 'Predicted Temperature'
        elif metric == 'precipitation':
            return 'Predicted Precipitation'
        elif metric == 'congestion':
            return 'Predicted Congestion'
        elif metric == 'gdp_growth':
            return 'Predicted GDP Growth (%)'
        elif metric == 'inflation':
            return 'Predicted Inflation Rate (%)'
        elif metric == 'ridership':
            return 'Predicted Ridership'
        
        return 'Predicted Value'