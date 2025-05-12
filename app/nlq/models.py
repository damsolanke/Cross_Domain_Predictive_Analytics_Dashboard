"""
Natural Language Query Models Module
Author: Ademola Solanke
Date: May 2025

This module defines data models for natural language queries.
"""

from datetime import datetime

class QueryRecord:
    """Class representing a saved query record."""
    
    def __init__(self, query_text, intent, results=None):
        """
        Initialize a query record.
        
        Args:
            query_text (str): The original query text.
            intent (str): The detected intent of the query.
            results (dict, optional): The query results.
        """
        self.query_text = query_text
        self.intent = intent
        self.results = results or {}
        self.timestamp = datetime.now()
        self.id = None  # Would be set when saved to database
    
    def to_dict(self):
        """Convert the query record to a dictionary."""
        return {
            'id': self.id,
            'query': self.query_text,
            'intent': self.intent,
            'timestamp': self.timestamp.isoformat(),
            'has_results': bool(self.results)
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a QueryRecord from a dictionary."""
        record = cls(
            query_text=data.get('query', ''),
            intent=data.get('intent', 'unknown'),
            results=data.get('results', {})
        )
        
        # Set other attributes if available
        if 'id' in data:
            record.id = data['id']
        
        if 'timestamp' in data:
            try:
                record.timestamp = datetime.fromisoformat(data['timestamp'])
            except (ValueError, TypeError):
                record.timestamp = datetime.now()
        
        return record


class QueryHistoryManager:
    """Class for managing query history."""
    
    def __init__(self, max_history=100):
        """
        Initialize the history manager.
        
        Args:
            max_history (int): Maximum number of history entries to keep.
        """
        self.max_history = max_history
        self.history = []
    
    def add_query(self, query_record):
        """
        Add a query to the history.
        
        Args:
            query_record (QueryRecord): The query record to add.
            
        Returns:
            QueryRecord: The added record with updated ID.
        """
        # Assign an ID
        query_record.id = self._generate_id()
        
        # Add to history
        self.history.append(query_record)
        
        # Trim history if needed
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        return query_record
    
    def get_history(self, limit=None):
        """
        Get query history.
        
        Args:
            limit (int, optional): Maximum number of history items to return.
            
        Returns:
            list: Query history items as dictionaries.
        """
        history = sorted(self.history, key=lambda x: x.timestamp, reverse=True)
        
        if limit and limit > 0:
            history = history[:limit]
        
        return [item.to_dict() for item in history]
    
    def clear_history(self):
        """Clear the query history."""
        self.history = []
    
    def _generate_id(self):
        """Generate a unique ID for a query record."""
        if not self.history:
            return 1
        
        return max(record.id or 0 for record in self.history) + 1