"""
Transportation data API connector
"""
import os
import time
import json
import hashlib
import random
import math
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from app.api.connectors.base_connector import BaseConnector

class TransportationConnector(BaseConnector):
    """Connector for transportation data APIs"""
    
    def __init__(self):
        """Initialize the transportation connector"""
        super().__init__(
            name="Transportation Data",
            description="Provides traffic patterns, public transit metrics, and transportation infrastructure data",
            cache_ttl=600  # 10 minutes cache
        )
        # API configuration
        self.api_key = os.environ.get('TRANSPORTATION_API_KEY', 'demo_key')
        self.base_url = "https://api.transportdata.io"  # Placeholder URL
        
        # Default city if none provided
        self.default_city = "New York"
    
    def fetch_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch transportation data based on parameters
        
        Args:
            params: Parameters for the transportation data request
                - city: City name (default: New York)
                - data_type: Type of data (traffic, transit, infrastructure)
                - transit_type: Type of transit (bus, subway, train, etc.)
                - timeframe: Time period (hour, day, week)
                
        Returns:
            Dictionary of transportation data
        """
        if params is None:
            params = {}
        
        # Get request parameters
        city = params.get('city', self.default_city)
        data_type = params.get('data_type', 'traffic')
        transit_type = params.get('transit_type', 'all')
        timeframe = params.get('timeframe', 'day')
        
        # Create cache key based on parameters
        cache_key = self._create_cache_key(city, data_type, transit_type, timeframe)
        
        # Check cache first
        cached_data = self._check_cache(cache_key)
        if cached_data:
            return cached_data
        
        try:
            self._update_status("fetching")
            
            # In a real implementation, we'd use the API key and make actual requests
            # For this demo, we'll use simulated data
            
            # Get data based on requested type
            if data_type == 'traffic':
                data = self._get_simulated_traffic_data(city, timeframe)
            elif data_type == 'transit':
                data = self._get_simulated_transit_data(city, transit_type, timeframe)
            elif data_type == 'infrastructure':
                data = self._get_simulated_infrastructure_data(city)
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
            
            # Cache the results
            self._update_cache(cache_key, data)
            
            self._update_status("success")
            return data
            
        except Exception as e:
            self._update_status("error", e)
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def _create_cache_key(self, city: str, data_type: str, transit_type: str, timeframe: str) -> str:
        """Create a unique cache key based on request parameters"""
        params_str = f"{city}|{data_type}|{transit_type}|{timeframe}"
        return f"transport_{hashlib.md5(params_str.encode()).hexdigest()}"
    
    def _get_simulated_traffic_data(self, city: str, timeframe: str) -> Dict[str, Any]:
        """Get simulated traffic data"""
        # Create seed for consistent results
        seed = f"{city}_traffic_{timeframe}_{int(time.time() / 3600)}"
        random.seed(hash(seed) % 1000000)
        
        # Generate traffic data over time
        traffic_data = []
        end_time = datetime.now()
        
        # Determine time interval based on timeframe
        if timeframe == 'hour':
            intervals = 12
            delta = timedelta(minutes=5)
        elif timeframe == 'day':
            intervals = 24
            delta = timedelta(hours=1)
        elif timeframe == 'week':
            intervals = 7
            delta = timedelta(days=1)
        else:
            intervals = 24
            delta = timedelta(hours=1)
        
        # Create time-based pattern with rush hours
        for i in range(intervals):
            point_time = end_time - delta * (intervals - i - 1)
            
            if timeframe == 'day':
                # Create rush hour pattern for daily data
                hour = point_time.hour
                
                # Morning rush (7-9 AM)
                if 7 <= hour <= 9:
                    congestion_base = random.uniform(0.7, 0.9)
                # Evening rush (4-7 PM)
                elif 16 <= hour <= 19:
                    congestion_base = random.uniform(0.8, 0.95)
                # Late night (11 PM - 5 AM)
                elif hour >= 23 or hour <= 5:
                    congestion_base = random.uniform(0.1, 0.3)
                # Other times
                else:
                    congestion_base = random.uniform(0.4, 0.6)
            else:
                # For weekly/hourly data, use simpler pattern
                congestion_base = random.uniform(0.3, 0.8)
            
            # Add some noise
            congestion = min(1.0, max(0.1, congestion_base + random.uniform(-0.1, 0.1)))
            
            # Calculate average speed based on congestion
            max_speed = 65  # mph
            avg_speed = max_speed * (1 - congestion**2)  # Non-linear relationship
            
            traffic_data.append({
                'timestamp': point_time.isoformat(),
                'congestion_level': round(congestion, 2),
                'avg_speed_mph': round(avg_speed, 1),
                'incidents': self._generate_traffic_incidents(congestion)
            })
        
        # Add hotspots
        hotspots = self._generate_traffic_hotspots(city)
        
        # Current overall stats
        current_congestion = traffic_data[-1]['congestion_level'] if traffic_data else 0.5
        
        return {
            'city': city,
            'timestamp': datetime.now().isoformat(),
            'timeframe': timeframe,
            'traffic_data': traffic_data,
            'hotspots': hotspots,
            'current_stats': {
                'congestion_level': current_congestion,
                'avg_commute_increase': f"{int(current_congestion * 100)}%",
                'incident_count': sum(len(d['incidents']) for d in traffic_data)
            }
        }
    
    def _get_simulated_transit_data(self, city: str, transit_type: str, timeframe: str) -> Dict[str, Any]:
        """Get simulated public transit data"""
        # Create seed for consistent results
        seed = f"{city}_{transit_type}_{timeframe}_{int(time.time() / 3600)}"
        random.seed(hash(seed) % 1000000)
        
        # Get list of transit types for this city
        if transit_type == 'all':
            transit_types = self._get_transit_types(city)
        else:
            transit_types = [transit_type]
        
        # Generate data for each transit type
        transit_data = {}
        for t_type in transit_types:
            transit_data[t_type] = self._generate_transit_type_data(city, t_type, timeframe)
        
        # Generate ridership data over time
        ridership_data = []
        end_time = datetime.now()
        
        # Determine time interval based on timeframe
        if timeframe == 'hour':
            intervals = 12
            delta = timedelta(minutes=5)
        elif timeframe == 'day':
            intervals = 24
            delta = timedelta(hours=1)
        elif timeframe == 'week':
            intervals = 7
            delta = timedelta(days=1)
        else:
            intervals = 24
            delta = timedelta(hours=1)
        
        for i in range(intervals):
            point_time = end_time - delta * (intervals - i - 1)
            
            # Create time-based patterns for ridership
            if timeframe == 'day':
                hour = point_time.hour
                # Rush hours have higher ridership
                if 7 <= hour <= 9 or 16 <= hour <= 19:
                    factor = random.uniform(0.8, 1.0)
                elif hour >= 23 or hour <= 5:
                    factor = random.uniform(0.1, 0.3)
                else:
                    factor = random.uniform(0.4, 0.7)
            elif timeframe == 'week':
                # Weekdays have higher ridership than weekends
                weekday = point_time.weekday()
                if weekday < 5:  # Monday-Friday
                    factor = random.uniform(0.7, 1.0)
                else:  # Weekend
                    factor = random.uniform(0.4, 0.7)
            else:
                factor = random.uniform(0.5, 1.0)
            
            # Base ridership depends on city size
            base_ridership = self._get_city_ridership_base(city)
            
            ridership = int(base_ridership * factor)
            
            ridership_data.append({
                'timestamp': point_time.isoformat(),
                'ridership': ridership,
                'on_time_percentage': round(random.uniform(70, 98), 1)
            })
        
        # Current statistics
        current_stats = {
            'ridership': ridership_data[-1]['ridership'] if ridership_data else 0,
            'on_time_percentage': ridership_data[-1]['on_time_percentage'] if ridership_data else 90.0,
            'active_lines': sum(len(td['lines']) for td in transit_data.values()),
            'active_vehicles': sum(td['active_vehicles'] for td in transit_data.values())
        }
        
        return {
            'city': city,
            'timestamp': datetime.now().isoformat(),
            'timeframe': timeframe,
            'transit_types': transit_types,
            'transit_data': transit_data,
            'ridership_data': ridership_data,
            'current_stats': current_stats
        }
    
    def _get_simulated_infrastructure_data(self, city: str) -> Dict[str, Any]:
        """Get simulated transportation infrastructure data"""
        # Create seed for consistent results
        seed = f"{city}_infrastructure_{int(time.time() / 86400)}"  # Daily seed
        random.seed(hash(seed) % 1000000)
        
        # Generate infrastructure elements
        road_stats = {
            'total_miles': int(random.uniform(2000, 10000)),
            'highways_miles': int(random.uniform(200, 1000)),
            'arterial_miles': int(random.uniform(500, 3000)),
            'bridges': int(random.uniform(50, 500)),
            'tunnels': int(random.uniform(5, 50)),
            'intersections': int(random.uniform(1000, 10000)),
            'traffic_signals': int(random.uniform(500, 5000))
        }
        
        # Maintenance stats
        maintenance_stats = {
            'road_condition_index': round(random.uniform(60, 95), 1),
            'bridge_health_index': round(random.uniform(70, 95), 1),
            'planned_projects': int(random.uniform(10, 100)),
            'ongoing_projects': int(random.uniform(5, 50)),
            'annual_maintenance_budget_M': int(random.uniform(50, 500))
        }
        
        # Public transport infrastructure
        transit_infrastructure = {}
        transit_types = self._get_transit_types(city)
        
        for t_type in transit_types:
            if t_type == 'subway':
                transit_infrastructure[t_type] = {
                    'lines': int(random.uniform(5, 25)),
                    'stations': int(random.uniform(50, 300)),
                    'track_miles': int(random.uniform(100, 600)),
                    'avg_station_age_years': int(random.uniform(20, 80))
                }
            elif t_type == 'bus':
                transit_infrastructure[t_type] = {
                    'routes': int(random.uniform(50, 300)),
                    'stops': int(random.uniform(1000, 8000)),
                    'dedicated_lanes_miles': int(random.uniform(10, 100)),
                    'terminals': int(random.uniform(3, 20))
                }
            elif t_type == 'train':
                transit_infrastructure[t_type] = {
                    'lines': int(random.uniform(3, 15)),
                    'stations': int(random.uniform(20, 150)),
                    'track_miles': int(random.uniform(200, 1000)),
                    'avg_station_age_years': int(random.uniform(30, 100))
                }
            elif t_type == 'ferry':
                transit_infrastructure[t_type] = {
                    'routes': int(random.uniform(2, 10)),
                    'terminals': int(random.uniform(2, 15)),
                    'vessels': int(random.uniform(5, 30))
                }
            elif t_type == 'tram':
                transit_infrastructure[t_type] = {
                    'lines': int(random.uniform(3, 12)),
                    'stops': int(random.uniform(30, 200)),
                    'track_miles': int(random.uniform(20, 150))
                }
        
        # Alternative transportation
        alternative_transport = {
            'bike_lanes_miles': int(random.uniform(10, 500)),
            'bike_share_stations': int(random.uniform(0, 300)),
            'bike_share_bikes': int(random.uniform(0, 5000)),
            'pedestrian_only_zones': int(random.uniform(0, 20)),
            'ev_charging_stations': int(random.uniform(10, 500))
        }
        
        return {
            'city': city,
            'timestamp': datetime.now().isoformat(),
            'road_stats': road_stats,
            'maintenance_stats': maintenance_stats,
            'transit_infrastructure': transit_infrastructure,
            'alternative_transport': alternative_transport,
            'investment_projects': self._generate_investment_projects(city)
        }
    
    def _generate_traffic_incidents(self, congestion_level: float) -> List[Dict[str, Any]]:
        """Generate simulated traffic incidents based on congestion level"""
        # Higher congestion means more incidents
        incident_count = round(random.triangular(0, 10, congestion_level * 10))
        
        incident_types = [
            'Accident', 'Construction', 'Disabled Vehicle', 'Road Closure',
            'Special Event', 'Hazard', 'Police Activity', 'Medical Emergency'
        ]
        
        severity_levels = ['Low', 'Medium', 'High', 'Critical']
        
        incidents = []
        for _ in range(incident_count):
            incident_type = random.choice(incident_types)
            
            # Critical incidents are rare
            if incident_type == 'Accident':
                severity_weights = [0.4, 0.3, 0.2, 0.1]  # Higher chance of serious accidents
            else:
                severity_weights = [0.6, 0.3, 0.08, 0.02]  # Other incidents usually less severe
                
            severity = random.choices(severity_levels, weights=severity_weights)[0]
            
            # Expected duration based on severity
            if severity == 'Low':
                duration_minutes = random.randint(15, 60)
            elif severity == 'Medium':
                duration_minutes = random.randint(30, 120)
            elif severity == 'High':
                duration_minutes = random.randint(60, 240)
            else:  # Critical
                duration_minutes = random.randint(120, 480)
            
            incidents.append({
                'type': incident_type,
                'severity': severity,
                'expected_duration_minutes': duration_minutes,
                'lanes_affected': random.randint(1, 4)
            })
        
        return incidents
    
    def _generate_traffic_hotspots(self, city: str) -> List[Dict[str, Any]]:
        """Generate simulated traffic hotspots for a city"""
        # Number of hotspots depends on city
        hotspot_count = self._get_city_size_factor(city)
        
        hotspots = []
        for i in range(hotspot_count):
            congestion = random.uniform(0.7, 1.0)  # Hotspots are by definition congested
            hotspots.append({
                'name': f"Hotspot {i+1}",
                'congestion_level': round(congestion, 2),
                'avg_speed_mph': round(65 * (1 - congestion**2), 1),
                'delay_minutes': round(congestion * 30)  # Up to 30 minute delay
            })
        
        # Sort by congestion level
        hotspots.sort(key=lambda x: x['congestion_level'], reverse=True)
        
        return hotspots
    
    def _get_transit_types(self, city: str) -> List[str]:
        """Get available transit types for a city"""
        # Different cities have different transit options
        transit_options = {
            'New York': ['subway', 'bus', 'train', 'ferry'],
            'Chicago': ['subway', 'bus', 'train'],
            'San Francisco': ['subway', 'bus', 'train', 'ferry', 'tram'],
            'Boston': ['subway', 'bus', 'train', 'ferry'],
            'Washington DC': ['subway', 'bus', 'train'],
            'Los Angeles': ['subway', 'bus', 'train'],
            'Seattle': ['bus', 'train', 'ferry', 'tram'],
            'Miami': ['bus', 'train', 'ferry'],
            'London': ['subway', 'bus', 'train', 'ferry', 'tram'],
            'Paris': ['subway', 'bus', 'train', 'tram'],
            'Tokyo': ['subway', 'bus', 'train'],
            'Beijing': ['subway', 'bus', 'train']
        }
        
        return transit_options.get(city, ['bus', 'train'])  # Default to bus and train
    
    def _generate_transit_type_data(self, city: str, transit_type: str, timeframe: str) -> Dict[str, Any]:
        """Generate data for a specific transit type"""
        # Create line names
        line_count = self._get_transit_line_count(city, transit_type)
        lines = []
        
        line_designations = {}
        line_designations['subway'] = list("123456789ABCDEFGJKLMNQRST")
        line_designations['bus'] = [f"{n}" for n in range(1, 100)]
        line_designations['train'] = [f"Line {c}" for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        line_designations['tram'] = [f"T{n}" for n in range(1, 20)]
        line_designations['ferry'] = [f"F{n}" for n in range(1, 10)]
        
        designations = line_designations.get(transit_type, [f"Route {n}" for n in range(1, 50)])
        
        for i in range(line_count):
            designation = designations[i % len(designations)]
            lines.append({
                'name': f"{designation}",
                'status': random.choice(['On Time', 'On Time', 'On Time', 'Delayed', 'Minor Delays']),
                'on_time_performance': round(random.uniform(80, 98), 1)
            })
        
        # Vehicle count based on city size and transit type
        city_factor = self._get_city_size_factor(city)
        
        if transit_type == 'subway':
            active_vehicles = int(city_factor * random.uniform(50, 200))
        elif transit_type == 'bus':
            active_vehicles = int(city_factor * random.uniform(100, 500))
        elif transit_type == 'train':
            active_vehicles = int(city_factor * random.uniform(20, 100))
        elif transit_type == 'ferry':
            active_vehicles = int(city_factor * random.uniform(5, 20))
        elif transit_type == 'tram':
            active_vehicles = int(city_factor * random.uniform(20, 80))
        else:
            active_vehicles = int(city_factor * random.uniform(10, 50))
        
        return {
            'lines': lines,
            'active_vehicles': active_vehicles,
            'avg_frequency_minutes': random.randint(5, 20),
            'accessibility_percentage': round(random.uniform(70, 100), 1)
        }
    
    def _get_transit_line_count(self, city: str, transit_type: str) -> int:
        """Get the number of transit lines for a city and transit type"""
        city_factor = self._get_city_size_factor(city)
        
        if transit_type == 'subway':
            return int(city_factor * random.uniform(5, 20))
        elif transit_type == 'bus':
            return int(city_factor * random.uniform(20, 100))
        elif transit_type == 'train':
            return int(city_factor * random.uniform(3, 15))
        elif transit_type == 'ferry':
            return int(city_factor * random.uniform(2, 8))
        elif transit_type == 'tram':
            return int(city_factor * random.uniform(3, 12))
        else:
            return int(city_factor * random.uniform(5, 20))
    
    def _get_city_size_factor(self, city: str) -> float:
        """Get a size factor for a city (1.0 = average)"""
        city_factors = {
            'New York': 2.0,
            'Chicago': 1.5,
            'Los Angeles': 1.8,
            'San Francisco': 1.2,
            'Boston': 1.1,
            'Washington DC': 1.3,
            'Seattle': 1.0,
            'Miami': 1.0,
            'London': 1.9,
            'Paris': 1.7,
            'Tokyo': 2.1,
            'Beijing': 2.0
        }
        
        return city_factors.get(city, 1.0)
    
    def _get_city_ridership_base(self, city: str) -> int:
        """Get base ridership for a city (daily)"""
        city_factor = self._get_city_size_factor(city)
        return int(1000000 * city_factor)
    
    def _generate_investment_projects(self, city: str) -> List[Dict[str, Any]]:
        """Generate simulated transportation investment projects"""
        city_factor = self._get_city_size_factor(city)
        project_count = int(city_factor * random.uniform(5, 15))
        
        project_types = [
            'Road Expansion', 'Bridge Replacement', 'Transit Expansion', 
            'Intersection Improvement', 'Pedestrian Infrastructure',
            'Bike Lane Network', 'Smart Traffic System', 'EV Infrastructure',
            'Transit Modernization', 'Accessibility Improvements'
        ]
        
        projects = []
        for i in range(project_count):
            project_type = random.choice(project_types)
            
            # Budget based on project type and city size
            if project_type in ['Road Expansion', 'Bridge Replacement', 'Transit Expansion']:
                budget = random.uniform(50, 500) * city_factor
            elif project_type in ['Transit Modernization', 'Smart Traffic System']:
                budget = random.uniform(20, 200) * city_factor
            else:
                budget = random.uniform(5, 100) * city_factor
            
            # Duration based on project type
            if project_type in ['Road Expansion', 'Bridge Replacement', 'Transit Expansion']:
                duration_months = random.randint(18, 60)
            elif project_type in ['Intersection Improvement', 'Smart Traffic System']:
                duration_months = random.randint(6, 24)
            else:
                duration_months = random.randint(3, 18)
            
            # Status
            status = random.choice(['Planned', 'Approved', 'In Progress', 'Completed', 'On Hold'])
            
            # Completion percentage
            if status == 'Planned' or status == 'Approved':
                completion = 0
            elif status == 'In Progress':
                completion = random.randint(10, 90)
            elif status == 'Completed':
                completion = 100
            else:  # On Hold
                completion = random.randint(10, 70)
            
            projects.append({
                'name': f"{project_type} Project {i+1}",
                'type': project_type,
                'budget_millions': round(budget, 1),
                'duration_months': duration_months,
                'status': status,
                'completion_percentage': completion,
                'impact_score': round(random.uniform(3, 10), 1)  # 1-10 impact score
            })
        
        return projects