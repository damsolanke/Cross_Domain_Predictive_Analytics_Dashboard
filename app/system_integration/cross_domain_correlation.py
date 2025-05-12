"""
Cross-domain correlation module.
"""
import numpy as np
from typing import Dict, List, Any, Optional

class CrossDomainCorrelator:
    """
    Analyzes correlations between different data domains.
    """
    
    def __init__(self):
        """Initialize the cross-domain correlator."""
        self.domain_data = {}
        self.correlation_cache = {}
        self.error = None
        
    def add_domain_data(self, domain: str, data: List[Dict[str, Any]]):
        """
        Add data for a specific domain.
        
        Args:
            domain: Domain name
            data: List of data points for the domain
        """
        self.domain_data[domain] = data
        # Invalidate cache when new data is added
        self.correlation_cache = {}
        
    def compute_correlation(self, domain1: str, field1: str, domain2: str, field2: str) -> Optional[float]:
        """
        Compute correlation between two domain fields.
        
        Args:
            domain1: First domain name
            field1: Field name in first domain
            domain2: Second domain name
            field2: Field name in second domain
            
        Returns:
            Pearson correlation coefficient or None if computation fails
        """
        cache_key = f"{domain1}.{field1}_{domain2}.{field2}"
        
        # Check cache first
        if cache_key in self.correlation_cache:
            return self.correlation_cache[cache_key]
            
        # Check if domains exist
        if domain1 not in self.domain_data or domain2 not in self.domain_data:
            self.error = f"Domain not found: {domain1 if domain1 not in self.domain_data else domain2}"
            return None
            
        try:
            # Extract data
            data1 = [item.get(field1) for item in self.domain_data[domain1] if field1 in item]
            data2 = [item.get(field2) for item in self.domain_data[domain2] if field2 in item]
            
            # Ensure equal length by truncating to shorter list
            min_len = min(len(data1), len(data2))
            if min_len < 2:
                self.error = f"Insufficient data points for correlation: {min_len}"
                return None
                
            data1 = data1[:min_len]
            data2 = data2[:min_len]
            
            # Compute correlation
            correlation = np.corrcoef(data1, data2)[0, 1]
            
            # Cache result
            self.correlation_cache[cache_key] = correlation
            
            return correlation
            
        except Exception as e:
            self.error = f"Error computing correlation: {str(e)}"
            return None
            
    def get_all_correlations(self) -> Dict[str, float]:
        """
        Get all possible correlations between domains.
        
        Returns:
            Dictionary mapping correlation keys to values
        """
        result = {}
        
        # Generate all combinations of domains and fields
        for domain1, data1 in self.domain_data.items():
            if not data1 or not isinstance(data1[0], dict):
                continue
                
            for field1 in data1[0].keys():
                for domain2, data2 in self.domain_data.items():
                    if not data2 or not isinstance(data2[0], dict):
                        continue
                        
                    for field2 in data2[0].keys():
                        # Skip self-correlations
                        if domain1 == domain2 and field1 == field2:
                            continue
                            
                        correlation = self.compute_correlation(domain1, field1, domain2, field2)
                        if correlation is not None:
                            key = f"{domain1}.{field1}_{domain2}.{field2}"
                            result[key] = correlation
                            
        return result
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of the correlator.
        
        Returns:
            Status information dictionary
        """
        return {
            'domains': list(self.domain_data.keys()),
            'correlation_count': len(self.correlation_cache),
            'error': self.error
        }
        
    def get_highest_correlations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get the highest absolute correlations.
        
        Args:
            limit: Maximum number of correlations to return
            
        Returns:
            List of correlation information dictionaries
        """
        # Compute all correlations if cache is empty
        if not self.correlation_cache:
            self.get_all_correlations()
            
        # Sort by absolute correlation value
        sorted_correlations = sorted(
            self.correlation_cache.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Format results
        result = []
        for key, value in sorted_correlations[:limit]:
            domain1_field, domain2_field = key.split('_')
            domain1, field1 = domain1_field.split('.')
            domain2, field2 = domain2_field.split('.')
            
            result.append({
                'correlation': value,
                'domain1': domain1,
                'field1': field1,
                'domain2': domain2,
                'field2': field2,
                'strength': self._interpret_correlation(value)
            })
            
        return result
        
    def _interpret_correlation(self, correlation: float) -> str:
        """
        Interpret the strength of a correlation coefficient.
        
        Args:
            correlation: Pearson correlation coefficient
            
        Returns:
            String describing correlation strength
        """
        abs_corr = abs(correlation)
        
        if abs_corr > 0.8:
            return 'very strong'
        elif abs_corr > 0.6:
            return 'strong'
        elif abs_corr > 0.4:
            return 'moderate'
        elif abs_corr > 0.2:
            return 'weak'
        else:
            return 'very weak'