"""
Cross-domain prediction model for analyzing correlations across different domains
"""
import time
import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from app.models.base_model import BaseModel

class CrossDomainModel(BaseModel):
    """Model for identifying and predicting cross-domain correlations"""
    
    def __init__(self):
        """Initialize the cross-domain prediction model"""
        super().__init__(
            name="Cross-Domain Correlation Model",
            description="Analyzes correlations between different data domains and generates predictions based on cross-domain patterns",
            data_sources=["weather", "economic", "transportation", "social-media"],
            prediction_types=["correlation", "impact", "scenario"]
        )
        # Domain correlation matrix (simulated)
        # Values represent correlation strength between domains
        self.domain_correlations = {
            'weather': {
                'economic': 0.3,
                'transportation': 0.7,
                'social-media': 0.4
            },
            'economic': {
                'weather': 0.3,
                'transportation': 0.5,
                'social-media': 0.6
            },
            'transportation': {
                'weather': 0.7,
                'economic': 0.5,
                'social-media': 0.4
            },
            'social-media': {
                'weather': 0.4,
                'economic': 0.6,
                'transportation': 0.4
            }
        }
        
        # Domain impact factors (how much one domain affects others)
        self.domain_impacts = {
            'weather': {
                'economic': {'strength': 0.4, 'lag': 3},  # Weather impacts economy with 3-day lag
                'transportation': {'strength': 0.8, 'lag': 0},  # Weather impacts transportation immediately
                'social-media': {'strength': 0.5, 'lag': 0}  # Weather impacts social media immediately
            },
            'economic': {
                'weather': {'strength': 0.1, 'lag': 30},  # Economy has minimal impact on weather (long-term)
                'transportation': {'strength': 0.6, 'lag': 7},  # Economy impacts transportation with 1-week lag
                'social-media': {'strength': 0.7, 'lag': 1}  # Economy impacts social media quickly
            },
            'transportation': {
                'weather': {'strength': 0.0, 'lag': 0},  # Transportation doesn't impact weather
                'economic': {'strength': 0.3, 'lag': 14},  # Transportation impacts economy with 2-week lag
                'social-media': {'strength': 0.5, 'lag': 0}  # Transportation impacts social media immediately
            },
            'social-media': {
                'weather': {'strength': 0.0, 'lag': 0},  # Social media doesn't impact weather
                'economic': {'strength': 0.2, 'lag': 3},  # Social media impacts economy with 3-day lag
                'transportation': {'strength': 0.3, 'lag': 1}  # Social media impacts transportation with 1-day lag
            }
        }
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process multi-domain data and generate cross-domain predictions
        
        Args:
            data: Dictionary containing data from multiple domains
            
        Returns:
            Dictionary with cross-domain analysis and predictions
        """
        start_time = time.time()
        
        try:
            self._update_status("processing")
            
            # Identify domains present in the data
            domains = self._identify_domains(data)
            
            # Extract key metrics for each domain
            domain_metrics = self._extract_domain_metrics(data, domains)
            
            # Analyze cross-domain correlations
            correlations = self._analyze_correlations(domain_metrics)
            
            # Generate cross-domain predictions
            predictions = self._generate_predictions(domain_metrics, correlations)
            
            # Calculate impact matrix
            impact_matrix = self._calculate_impact_matrix(domain_metrics, correlations)
            
            # Generate scenario analysis if requested
            scenarios = {}
            if 'scenario_params' in data:
                scenarios = self._generate_scenarios(domain_metrics, 
                                                   correlations, 
                                                   data['scenario_params'])
            
            # Calculate prediction latency
            latency_ms = (time.time() - start_time) * 1000
            self._log_prediction(latency_ms)
            
            # Return predictions with metadata
            result = {
                'generated_at': datetime.now().isoformat(),
                'model_version': '1.0',
                'domains_analyzed': domains,
                'correlations': correlations,
                'impact_matrix': impact_matrix,
                'predictions': predictions
            }
            
            if scenarios:
                result['scenarios'] = scenarios
            
            self._update_status("success")
            return result
            
        except Exception as e:
            self._update_status("error", e)
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def _identify_domains(self, data: Dict[str, Any]) -> List[str]:
        """
        Identify which domains are present in the data
        
        Args:
            data: Input data dictionary
            
        Returns:
            List of identified domains
        """
        domains = []
        
        # Check for domain-specific data
        if 'weather' in data or ('current' in data and 'temp' in data.get('current', {})):
            domains.append('weather')
        
        if 'economic' in data or 'indicator' in data:
            domains.append('economic')
        
        if 'transportation' in data or 'traffic_data' in data:
            domains.append('transportation')
        
        if 'social-media' in data or 'trending_topics' in data:
            domains.append('social-media')
        
        # If no specific domains found, check for explicit domain list
        if not domains and 'domains' in data and isinstance(data['domains'], list):
            domains = data['domains']
        
        # If still empty, default to all domains
        if not domains:
            domains = ['weather', 'economic', 'transportation', 'social-media']
        
        return domains
    
    def _extract_domain_metrics(self, data: Dict[str, Any], domains: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Extract key metrics for each domain
        
        Args:
            data: Input data dictionary
            domains: List of domains to extract metrics for
            
        Returns:
            Dictionary mapping domains to their key metrics
        """
        metrics = {}
        
        for domain in domains:
            domain_data = data.get(domain, {})
            
            if domain == 'weather':
                metrics[domain] = self._extract_weather_metrics(data, domain_data)
            elif domain == 'economic':
                metrics[domain] = self._extract_economic_metrics(data, domain_data)
            elif domain == 'transportation':
                metrics[domain] = self._extract_transportation_metrics(data, domain_data)
            elif domain == 'social-media':
                metrics[domain] = self._extract_social_media_metrics(data, domain_data)
        
        return metrics
    
    def _extract_weather_metrics(self, full_data: Dict[str, Any], domain_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from weather data"""
        metrics = {}
        
        # Try to find temperature
        if 'current' in full_data and 'temp' in full_data['current']:
            metrics['temperature'] = full_data['current']['temp']
        elif 'current' in domain_data and 'temp' in domain_data['current']:
            metrics['temperature'] = domain_data['current']['temp']
        else:
            metrics['temperature'] = 20.0  # Default
        
        # Try to find precipitation probability
        if 'current' in domain_data and 'precipitation_chance' in domain_data['current']:
            metrics['precipitation_chance'] = domain_data['current']['precipitation_chance']
        else:
            # Generate a reasonable value
            metrics['precipitation_chance'] = random.uniform(0.0, 0.5)
        
        # Extreme weather flag
        metrics['extreme_weather'] = 0.0
        weather_condition = "Clear"
        
        # Try to find weather condition
        if 'current' in domain_data and 'weather' in domain_data['current'] and 'main' in domain_data['current']['weather']:
            weather_condition = domain_data['current']['weather']['main']
        
        # Check for extreme weather
        if weather_condition in ['Thunderstorm', 'Tornado', 'Hurricane', 'Blizzard']:
            metrics['extreme_weather'] = 1.0
        elif weather_condition in ['Rain', 'Snow', 'Drizzle']:
            metrics['extreme_weather'] = 0.3
        
        return metrics
    
    def _extract_economic_metrics(self, full_data: Dict[str, Any], domain_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from economic data"""
        metrics = {}
        
        # Try to find economic indicators
        if 'indicator' in domain_data and domain_data['indicator'] == 'inflation' and 'data' in domain_data:
            # Get latest inflation value
            latest = domain_data['data'][-1] if isinstance(domain_data['data'], list) and domain_data['data'] else {'value': 2.0}
            metrics['inflation'] = latest.get('value', 2.0)
        else:
            metrics['inflation'] = 2.0  # Default inflation rate
        
        # Try to find GDP growth
        if 'indicator' in domain_data and domain_data['indicator'] == 'gdp' and 'data' in domain_data:
            # Get latest GDP value
            latest = domain_data['data'][-1] if isinstance(domain_data['data'], list) and domain_data['data'] else {'value': 2.5}
            metrics['gdp_growth'] = latest.get('value', 2.5)
        else:
            metrics['gdp_growth'] = 2.5  # Default GDP growth
        
        # Try to find interest rate
        if 'indicator' in domain_data and domain_data['indicator'] == 'interest_rates' and 'data' in domain_data:
            # Get latest interest rate value
            latest = domain_data['data'][-1] if isinstance(domain_data['data'], list) and domain_data['data'] else {'value': 3.0}
            metrics['interest_rate'] = latest.get('value', 3.0)
        else:
            metrics['interest_rate'] = 3.0  # Default interest rate
        
        # Economic volatility indicator
        metrics['volatility'] = 0.3  # Default moderate volatility
        
        return metrics
    
    def _extract_transportation_metrics(self, full_data: Dict[str, Any], domain_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from transportation data"""
        metrics = {}
        
        # Try to find congestion level
        if 'current_stats' in domain_data and 'congestion_level' in domain_data['current_stats']:
            metrics['congestion'] = domain_data['current_stats']['congestion_level']
        elif 'traffic_data' in domain_data and domain_data['traffic_data'] and 'congestion_level' in domain_data['traffic_data'][-1]:
            metrics['congestion'] = domain_data['traffic_data'][-1]['congestion_level']
        else:
            metrics['congestion'] = 0.4  # Default congestion
        
        # Try to find transit ridership (normalize to 0-1 range)
        if 'current_stats' in domain_data and 'ridership' in domain_data['current_stats']:
            # Normalize large ridership numbers to 0-1 range
            raw_ridership = domain_data['current_stats']['ridership']
            metrics['transit_usage'] = min(1.0, raw_ridership / 1000000)
        else:
            metrics['transit_usage'] = 0.5  # Default transit usage
        
        # Incident level (normalized count of incidents)
        if 'traffic_data' in domain_data and domain_data['traffic_data'] and 'incidents' in domain_data['traffic_data'][-1]:
            incidents = domain_data['traffic_data'][-1]['incidents']
            if isinstance(incidents, list):
                metrics['incident_level'] = min(1.0, len(incidents) / 10)
            else:
                metrics['incident_level'] = 0.2  # Default if structure is unexpected
        else:
            metrics['incident_level'] = 0.2  # Default incident level
        
        return metrics
    
    def _extract_social_media_metrics(self, full_data: Dict[str, Any], domain_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from social media data"""
        metrics = {}
        
        # Try to find sentiment levels
        if 'sentiment_data' in domain_data and domain_data['sentiment_data']:
            # Get latest sentiment data
            latest = domain_data['sentiment_data'][-1] if isinstance(domain_data['sentiment_data'], list) else domain_data['sentiment_data']
            
            if 'sentiment' in latest:
                sentiment = latest['sentiment']
                metrics['positive_sentiment'] = sentiment.get('positive', 0.5)
                metrics['negative_sentiment'] = sentiment.get('negative', 0.2)
            else:
                metrics['positive_sentiment'] = 0.5  # Default
                metrics['negative_sentiment'] = 0.2  # Default
        else:
            metrics['positive_sentiment'] = 0.5  # Default
            metrics['negative_sentiment'] = 0.2  # Default
        
        # Calculate net sentiment
        metrics['net_sentiment'] = metrics['positive_sentiment'] - metrics['negative_sentiment']
        
        # Trending topic intensity
        metrics['trend_intensity'] = 0.5  # Default
        if 'trending_topics' in domain_data and domain_data['trending_topics']:
            # Average growth rate of top trends
            top_trends = domain_data['trending_topics'][:5] if isinstance(domain_data['trending_topics'], list) else []
            if top_trends and 'growth_rate' in top_trends[0]:
                avg_growth = sum(t.get('growth_rate', 0) for t in top_trends) / len(top_trends)
                metrics['trend_intensity'] = min(1.0, avg_growth / 100)
        
        return metrics
    
    def _analyze_correlations(self, domain_metrics: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """
        Analyze cross-domain correlations
        
        Args:
            domain_metrics: Extracted metrics for each domain
            
        Returns:
            List of significant correlations between domains
        """
        correlations = []
        
        domains = list(domain_metrics.keys())
        
        # Analyze pairs of domains
        for i, domain1 in enumerate(domains):
            for domain2 in domains[i+1:]:
                # Get predefined correlation coefficient
                base_correlation = self.domain_correlations.get(domain1, {}).get(domain2, 0.0)
                
                # Adjust based on current metrics
                adjusted_correlation = self._calculate_adjusted_correlation(domain1, domain2, 
                                                                          domain_metrics[domain1], 
                                                                          domain_metrics[domain2],
                                                                          base_correlation)
                
                # Only include significant correlations
                if abs(adjusted_correlation) >= 0.3:
                    # Find specific metrics that correlate
                    correlated_metrics = self._find_correlated_metrics(domain1, domain2, 
                                                                     domain_metrics[domain1], 
                                                                     domain_metrics[domain2])
                    
                    correlations.append({
                        'domains': [domain1, domain2],
                        'correlation': round(adjusted_correlation, 2),
                        'direction': 'positive' if adjusted_correlation > 0 else 'negative',
                        'strength': self._correlation_strength_label(adjusted_correlation),
                        'metrics': correlated_metrics
                    })
        
        # Sort by correlation strength
        correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return correlations
    
    def _calculate_adjusted_correlation(self, domain1: str, domain2: str, 
                                      metrics1: Dict[str, float], metrics2: Dict[str, float],
                                      base_correlation: float) -> float:
        """
        Calculate adjusted correlation coefficient based on current metrics
        
        Args:
            domain1: First domain name
            domain2: Second domain name
            metrics1: Metrics for first domain
            metrics2: Metrics for second domain
            base_correlation: Base correlation coefficient
            
        Returns:
            Adjusted correlation coefficient
        """
        # Start with the base correlation
        adjusted = base_correlation
        
        # Apply domain-specific adjustments
        if domain1 == 'weather' and domain2 == 'transportation':
            # Weather impacts transportation more during extreme weather
            if metrics1.get('extreme_weather', 0) > 0:
                adjusted = min(1.0, adjusted + metrics1.get('extreme_weather', 0) * 0.3)
        
        elif domain1 == 'economic' and domain2 == 'transportation':
            # Economic volatility impacts transportation correlation
            adjusted = adjusted * (1 + metrics1.get('volatility', 0.3) * 0.5)
        
        elif domain1 == 'social-media' and domain2 == 'economic':
            # Extreme sentiment strengthens correlation
            sentiment_factor = abs(metrics1.get('net_sentiment', 0)) * 0.5
            adjusted = adjusted * (1 + sentiment_factor)
        
        # Add some randomness to simulate real-world variability
        noise = random.uniform(-0.1, 0.1)
        adjusted = max(-1.0, min(1.0, adjusted + noise))
        
        return adjusted
    
    def _find_correlated_metrics(self, domain1: str, domain2: str, 
                               metrics1: Dict[str, float], metrics2: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Find specific metrics that correlate between domains
        
        Args:
            domain1: First domain name
            domain2: Second domain name
            metrics1: Metrics for first domain
            metrics2: Metrics for second domain
            
        Returns:
            List of correlated metric pairs
        """
        correlated_pairs = []
        
        # Define potential correlations between domains
        potential_correlations = {
            ('weather', 'transportation'): [
                ('temperature', 'congestion', -0.4),  # Higher temp -> lower congestion
                ('precipitation_chance', 'congestion', 0.7),  # Higher rain chance -> higher congestion
                ('extreme_weather', 'incident_level', 0.8)  # Extreme weather -> more incidents
            ],
            ('weather', 'economic'): [
                ('extreme_weather', 'volatility', 0.6),  # Extreme weather -> higher economic volatility
                ('temperature', 'gdp_growth', 0.2)  # Temperature has mild effect on GDP
            ],
            ('weather', 'social-media'): [
                ('extreme_weather', 'trend_intensity', 0.7),  # Extreme weather drives social trends
                ('temperature', 'positive_sentiment', 0.3)  # Better weather -> more positive sentiment
            ],
            ('economic', 'transportation'): [
                ('gdp_growth', 'transit_usage', 0.5),  # Higher GDP -> more transit usage
                ('interest_rate', 'congestion', -0.3)  # Higher interest rates -> lower congestion
            ],
            ('economic', 'social-media'): [
                ('gdp_growth', 'positive_sentiment', 0.6),  # Higher GDP -> more positive sentiment
                ('volatility', 'trend_intensity', 0.4)  # Economic volatility drives social trends
            ],
            ('transportation', 'social-media'): [
                ('congestion', 'negative_sentiment', 0.5),  # More congestion -> more negative sentiment
                ('incident_level', 'trend_intensity', 0.6)  # More incidents drive social trends
            ]
        }
        
        # Order domains consistently for lookup
        domain_pair = (domain1, domain2) if domain1 < domain2 else (domain2, domain1)
        
        # Check for correlations between this domain pair
        for metric1, metric2, base_corr in potential_correlations.get(domain_pair, []):
            # Swap metrics if domains were swapped
            if domain_pair != (domain1, domain2):
                metric1, metric2 = metric2, metric1
            
            # Only include if both metrics exist
            if metric1 in metrics1 and metric2 in metrics2:
                # Calculate current correlation with some variance
                variance = random.uniform(-0.2, 0.2)
                current_corr = max(-1.0, min(1.0, base_corr + variance))
                
                # Only include significant correlations
                if abs(current_corr) >= 0.3:
                    correlated_pairs.append({
                        'metric1': {
                            'domain': domain1,
                            'metric': metric1,
                            'value': round(metrics1[metric1], 2)
                        },
                        'metric2': {
                            'domain': domain2,
                            'metric': metric2,
                            'value': round(metrics2[metric2], 2)
                        },
                        'correlation': round(current_corr, 2)
                    })
        
        return correlated_pairs
    
    def _correlation_strength_label(self, correlation: float) -> str:
        """Convert correlation coefficient to strength label"""
        abs_corr = abs(correlation)
        
        if abs_corr >= 0.8:
            return "Very Strong"
        elif abs_corr >= 0.6:
            return "Strong"
        elif abs_corr >= 0.4:
            return "Moderate"
        else:
            return "Weak"
    
    def _generate_predictions(self, domain_metrics: Dict[str, Dict[str, float]], 
                             correlations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate cross-domain predictions
        
        Args:
            domain_metrics: Extracted metrics for each domain
            correlations: List of identified correlations
            
        Returns:
            Dictionary of cross-domain predictions
        """
        predictions = {
            'short_term': self._generate_time_horizon_predictions(domain_metrics, correlations, 'short'),
            'medium_term': self._generate_time_horizon_predictions(domain_metrics, correlations, 'medium'),
            'long_term': self._generate_time_horizon_predictions(domain_metrics, correlations, 'long'),
            'key_insights': self._generate_key_insights(domain_metrics, correlations)
        }
        
        return predictions
    
    def _generate_time_horizon_predictions(self, domain_metrics: Dict[str, Dict[str, float]],
                                         correlations: List[Dict[str, Any]], 
                                         horizon: str) -> List[Dict[str, Any]]:
        """
        Generate predictions for a specific time horizon
        
        Args:
            domain_metrics: Extracted metrics for each domain
            correlations: List of identified correlations
            horizon: Time horizon (short, medium, long)
            
        Returns:
            List of predictions for the specified horizon
        """
        predictions = []
        
        # Define time horizons
        horizon_days = {
            'short': 3,    # 3 days
            'medium': 14,  # 2 weeks
            'long': 90     # 3 months
        }
        
        days = horizon_days.get(horizon, 7)
        confidence_factor = 0.9 if horizon == 'short' else 0.7 if horizon == 'medium' else 0.5
        
        # Sort correlations by strength
        strong_correlations = [c for c in correlations if abs(c['correlation']) >= 0.5]
        
        # Generate predictions based on strong correlations
        for correlation in strong_correlations:
            domains = correlation['domains']
            corr_value = correlation['correlation']
            
            # Find the domain that has more impact on the other
            impact_1_to_2 = self.domain_impacts.get(domains[0], {}).get(domains[1], {}).get('strength', 0)
            impact_2_to_1 = self.domain_impacts.get(domains[1], {}).get(domains[0], {}).get('strength', 0)
            
            # Primary domain is the one with more impact
            primary_idx = 0 if impact_1_to_2 >= impact_2_to_1 else 1
            secondary_idx = 1 - primary_idx
            
            primary_domain = domains[primary_idx]
            secondary_domain = domains[secondary_idx]
            
            # Generate a prediction
            prediction = self._create_cross_domain_prediction(
                primary_domain, 
                secondary_domain,
                domain_metrics[primary_domain],
                domain_metrics[secondary_domain],
                corr_value,
                confidence_factor,
                days
            )
            
            if prediction:
                predictions.append(prediction)
        
        # Add one overall prediction if we have multiple domains
        if len(domain_metrics) >= 3 and predictions:
            all_domains = sorted(domain_metrics.keys())
            overall = {
                'type': 'overall',
                'domains': all_domains,
                'prediction': self._generate_overall_prediction(domain_metrics, horizon),
                'confidence': round(confidence_factor * 0.9, 2),
                'timeframe': f"{days} days"
            }
            predictions.insert(0, overall)
        
        return predictions
    
    def _create_cross_domain_prediction(self, primary_domain: str, secondary_domain: str,
                                      primary_metrics: Dict[str, float], secondary_metrics: Dict[str, float],
                                      correlation: float, confidence_factor: float, days: int) -> Optional[Dict[str, Any]]:
        """
        Create a prediction between two domains
        
        Args:
            primary_domain: Domain with more impact
            secondary_domain: Domain with less impact
            primary_metrics: Metrics for primary domain
            secondary_metrics: Metrics for secondary domain
            correlation: Correlation coefficient
            confidence_factor: Base confidence factor
            days: Prediction timeframe in days
            
        Returns:
            Prediction dictionary or None if no significant prediction
        """
        # Generate prediction text based on domain pair
        prediction_text = ""
        metrics_pair = []
        
        # Weather -> Transportation
        if primary_domain == 'weather' and secondary_domain == 'transportation':
            if primary_metrics.get('extreme_weather', 0) > 0.5:
                prediction_text = f"Extreme weather conditions will lead to significant transportation disruptions with {int(correlation * 100)}% higher congestion and incident rates."
                metrics_pair = ["extreme_weather", "congestion"]
            elif primary_metrics.get('precipitation_chance', 0) > 0.6:
                prediction_text = f"High precipitation probability will result in {int(correlation * 60)}% increased transportation congestion and delays."
                metrics_pair = ["precipitation_chance", "congestion"]
            else:
                prediction_text = f"Weather conditions will have a {self._correlation_strength_label(correlation).lower()} impact on transportation efficiency."
                metrics_pair = ["temperature", "congestion"]
        
        # Weather -> Economic
        elif primary_domain == 'weather' and secondary_domain == 'economic':
            if primary_metrics.get('extreme_weather', 0) > 0.5:
                prediction_text = f"Extreme weather events will cause short-term economic volatility with up to {int(abs(correlation) * 3)}% fluctuation in affected sectors."
                metrics_pair = ["extreme_weather", "volatility"]
            else:
                prediction_text = f"Weather patterns will have a {self._correlation_strength_label(correlation).lower()} influence on economic indicators."
                metrics_pair = ["temperature", "gdp_growth"]
        
        # Economic -> Transportation
        elif primary_domain == 'economic' and secondary_domain == 'transportation':
            if primary_metrics.get('gdp_growth', 0) > 3.0:
                prediction_text = f"Strong economic growth will drive increased transportation usage by approximately {int(correlation * 15)}% across public transit systems."
                metrics_pair = ["gdp_growth", "transit_usage"]
            elif primary_metrics.get('volatility', 0) > 0.6:
                prediction_text = f"Economic volatility will create irregular transportation patterns with {int(correlation * 30)}% higher variability in congestion levels."
                metrics_pair = ["volatility", "congestion"]
            else:
                prediction_text = f"Economic indicators suggest a {self._correlation_strength_label(correlation).lower()} effect on transportation patterns."
                metrics_pair = ["gdp_growth", "transit_usage"]
        
        # Social Media -> Transportation/Economic
        elif primary_domain == 'social-media' and (secondary_domain == 'transportation' or secondary_domain == 'economic'):
            sentiment = primary_metrics.get('net_sentiment', 0)
            if abs(sentiment) > 0.3:
                sentiment_direction = "positive" if sentiment > 0 else "negative"
                impact_domain = "transportation demand" if secondary_domain == 'transportation' else "consumer behavior"
                prediction_text = f"Current {sentiment_direction} social sentiment will influence {impact_domain} with approximately {int(abs(correlation * sentiment * 20))}% effect."
                metrics_pair = ["net_sentiment", "transit_usage" if secondary_domain == 'transportation' else "gdp_growth"]
            else:
                prediction_text = f"Social media trends show a {self._correlation_strength_label(correlation).lower()} correlation with {secondary_domain} patterns."
                metrics_pair = ["trend_intensity", "congestion" if secondary_domain == 'transportation' else "volatility"]
        
        # If no specific prediction pattern matched
        if not prediction_text:
            return None
        
        # Adjust confidence based on correlation strength
        confidence = confidence_factor * abs(correlation)
        confidence = round(max(0.3, min(0.95, confidence)), 2)
        
        return {
            'type': 'cross_domain',
            'domains': [primary_domain, secondary_domain],
            'primary_domain': primary_domain,
            'related_metrics': metrics_pair,
            'prediction': prediction_text,
            'correlation': round(correlation, 2),
            'confidence': confidence,
            'timeframe': f"{days} days"
        }
    
    def _generate_overall_prediction(self, domain_metrics: Dict[str, Dict[str, float]], 
                                    horizon: str) -> str:
        """Generate an overall prediction across all domains"""
        # Analyze key factors across domains
        factors = []
        
        # Check for extreme weather
        if 'weather' in domain_metrics and domain_metrics['weather'].get('extreme_weather', 0) > 0.5:
            factors.append("extreme weather conditions")
        
        # Check for economic volatility
        if 'economic' in domain_metrics and domain_metrics['economic'].get('volatility', 0) > 0.6:
            factors.append("economic volatility")
        
        # Check for high transportation congestion
        if 'transportation' in domain_metrics and domain_metrics['transportation'].get('congestion', 0) > 0.7:
            factors.append("high transportation congestion")
        
        # Check for extreme social sentiment
        if 'social-media' in domain_metrics:
            sentiment = domain_metrics['social-media'].get('net_sentiment', 0)
            if abs(sentiment) > 0.4:
                sentiment_str = "strongly positive" if sentiment > 0 else "strongly negative"
                factors.append(f"{sentiment_str} social sentiment")
        
        # Generate prediction based on factors and horizon
        if horizon == 'short':
            if factors:
                return f"Cross-domain analysis indicates that {', '.join(factors)} will create significant interactions between domains over the next few days, requiring integrated monitoring and response."
            else:
                return "Short-term cross-domain effects show stable patterns with typical interactions between weather, transportation, and economic domains."
        
        elif horizon == 'medium':
            if factors:
                return f"Medium-term analysis shows that {', '.join(factors)} will drive cascading effects across domains, with potential second-order impacts emerging within 1-2 weeks."
            else:
                return "The medium-term cross-domain forecast shows gradually evolving relationships between domains with moderate interaction effects."
        
        else:  # long-term
            if factors:
                return f"Long-term cross-domain modeling indicates that current {', '.join(factors)} will establish new equilibrium patterns between domains over the next 2-3 months."
            else:
                return "Long-term cross-domain relationships will likely maintain their historical correlation patterns with seasonal variations being the primary influencing factor."
    
    def _generate_key_insights(self, domain_metrics: Dict[str, Dict[str, float]],
                             correlations: List[Dict[str, Any]]) -> List[str]:
        """
        Generate key insights from cross-domain analysis
        
        Args:
            domain_metrics: Extracted metrics for each domain
            correlations: List of identified correlations
            
        Returns:
            List of key insight statements
        """
        insights = []
        
        # Find strongest correlation
        strongest = next((c for c in correlations if abs(c['correlation']) >= 0.7), None)
        if strongest:
            domains = strongest['domains']
            corr = strongest['correlation']
            direction = "positive" if corr > 0 else "negative"
            insights.append(
                f"The strongest cross-domain relationship is a {direction} correlation of {abs(corr):.2f} " +
                f"between {domains[0]} and {domains[1]}."
            )
        
        # Insight about weather impact if applicable
        if 'weather' in domain_metrics:
            weather_metrics = domain_metrics['weather']
            weather_factor = ""
            
            if weather_metrics.get('extreme_weather', 0) > 0.5:
                weather_factor = "extreme weather events"
            elif weather_metrics.get('precipitation_chance', 0) > 0.7:
                weather_factor = "high precipitation probability"
            
            if weather_factor:
                impacts = []
                if 'transportation' in domain_metrics:
                    impacts.append(f"transportation delays of {int(0.7 * 40)}%")
                if 'economic' in domain_metrics:
                    impacts.append(f"short-term economic volatility of {int(0.5 * 5)}%")
                
                if impacts:
                    insights.append(
                        f"Current {weather_factor} are projected to cause {' and '.join(impacts)} " +
                        f"within the next 24-48 hours."
                    )
        
        # Insight about economic conditions if applicable
        if 'economic' in domain_metrics:
            econ_metrics = domain_metrics['economic']
            
            if 'gdp_growth' in econ_metrics and 'inflation' in econ_metrics:
                gdp = econ_metrics['gdp_growth']
                inflation = econ_metrics['inflation']
                
                if gdp > 3.0 and inflation < 3.0:
                    impacts = []
                    if 'transportation' in domain_metrics:
                        impacts.append(f"increased transportation demand ({int(gdp * 5)}%)")
                    
                    if impacts:
                        insights.append(
                            f"Favorable economic conditions (GDP growth: {gdp:.1f}%, Inflation: {inflation:.1f}%) " +
                            f"will likely drive {' and '.join(impacts)} over the next quarter."
                        )
        
        # Insight about unexpected correlation if found
        unexpected = next((c for c in correlations if 0.4 <= abs(c['correlation']) <= 0.6), None)
        if unexpected and len(insights) < 3:
            domains = unexpected['domains']
            corr = unexpected['correlation']
            insights.append(
                f"An emerging relationship between {domains[0]} and {domains[1]} " +
                f"(correlation: {corr:.2f}) suggests new cross-domain dynamics that may " +
                f"warrant further monitoring."
            )
        
        # Add general insight if needed
        if len(insights) < 2:
            domains_str = ", ".join(domain_metrics.keys())
            insights.append(
                f"Cross-domain analysis across {domains_str} reveals normal interaction patterns " +
                f"without significant anomalies or emerging threats."
            )
        
        return insights
    
    def _calculate_impact_matrix(self, domain_metrics: Dict[str, Dict[str, float]],
                               correlations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate impact matrix showing how domains affect each other
        
        Args:
            domain_metrics: Extracted metrics for each domain
            correlations: List of identified correlations
            
        Returns:
            Impact matrix dictionary
        """
        domains = sorted(domain_metrics.keys())
        
        # Initialize matrix
        matrix = {
            'domains': domains,
            'impacts': {}
        }
        
        # Calculate impacts between domains
        for source in domains:
            matrix['impacts'][source] = {}
            
            for target in domains:
                if source == target:
                    # No self-impact
                    matrix['impacts'][source][target] = 0.0
                    continue
                
                # Get base impact from predefined values
                base_impact = self.domain_impacts.get(source, {}).get(target, {}).get('strength', 0.0)
                
                # Find correlation between these domains if it exists
                correlation = 0.0
                for corr in correlations:
                    if source in corr['domains'] and target in corr['domains']:
                        correlation = corr['correlation']
                        break
                
                # Impact combines base impact and correlation
                impact = (base_impact + abs(correlation)) / 2
                
                # Adjust based on current metrics
                if source == 'weather' and 'extreme_weather' in domain_metrics[source]:
                    # Extreme weather increases impact
                    impact *= (1 + domain_metrics[source]['extreme_weather'])
                
                elif source == 'economic' and 'volatility' in domain_metrics[source]:
                    # Economic volatility increases impact
                    impact *= (1 + domain_metrics[source]['volatility'])
                
                # Ensure reasonable range
                impact = round(max(0.0, min(1.0, impact)), 2)
                matrix['impacts'][source][target] = impact
        
        return matrix
    
    def _generate_scenarios(self, domain_metrics: Dict[str, Dict[str, float]], 
                          correlations: List[Dict[str, Any]],
                          scenario_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate scenario analysis based on parameters
        
        Args:
            domain_metrics: Extracted metrics for each domain
            correlations: List of identified correlations
            scenario_params: Parameters for scenario generation
            
        Returns:
            Dictionary of scenarios
        """
        scenarios = {}
        
        # Get scenario type
        scenario_type = scenario_params.get('type', 'what_if')
        target_domain = scenario_params.get('target_domain')
        
        if scenario_type == 'what_if' and target_domain:
            # What-if scenario for specific domain
            scenarios = self._generate_what_if_scenario(domain_metrics, correlations, 
                                                      target_domain, scenario_params)
        
        elif scenario_type == 'extreme_events':
            # Extreme events scenario
            scenarios = self._generate_extreme_events_scenario(domain_metrics, correlations)
        
        elif scenario_type == 'optimization':
            # Optimization scenario
            target_metric = scenario_params.get('target_metric')
            scenarios = self._generate_optimization_scenario(domain_metrics, correlations, 
                                                          target_metric, scenario_params)
        
        return scenarios
    
    def _generate_what_if_scenario(self, domain_metrics: Dict[str, Dict[str, float]], 
                                 correlations: List[Dict[str, Any]],
                                 target_domain: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate what-if scenario analysis"""
        # Basic what-if scenario - not implemented in detail for this demo
        return {
            'type': 'what_if',
            'target_domain': target_domain,
            'description': f"What-if scenario analysis for {target_domain}",
            'results': [
                {
                    'condition': f"If {target_domain} metrics change by 20%",
                    'impact': f"Other domains would be affected by approximately 10-15%",
                    'confidence': 0.6
                }
            ]
        }
    
    def _generate_extreme_events_scenario(self, domain_metrics: Dict[str, Dict[str, float]], 
                                        correlations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate extreme events scenario analysis"""
        # Basic extreme events scenario - not implemented in detail for this demo
        return {
            'type': 'extreme_events',
            'description': "Analysis of potential extreme events across domains",
            'events': [
                {
                    'domain': 'weather',
                    'event': "Severe storm system",
                    'probability': 0.15,
                    'impacts': {
                        'transportation': "High congestion, 30% more incidents",
                        'economic': "Short-term 3% volatility increase"
                    }
                }
            ]
        }
    
    def _generate_optimization_scenario(self, domain_metrics: Dict[str, Dict[str, float]], 
                                      correlations: List[Dict[str, Any]],
                                      target_metric: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimization scenario analysis"""
        # Basic optimization scenario - not implemented in detail for this demo
        return {
            'type': 'optimization',
            'target_metric': target_metric,
            'description': f"Optimization scenario for {target_metric}",
            'recommendations': [
                {
                    'action': f"Optimize {target_metric} by adjusting related factors",
                    'expected_improvement': "15% improvement in target metric",
                    'confidence': 0.7
                }
            ]
        }