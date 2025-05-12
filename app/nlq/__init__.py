"""
Natural Language Query (NLQ) Package
Author: Ademola Solanke
Date: May 2025

This package contains the components for the natural language query functionality
of the Cross-Domain Predictive Analytics Dashboard.
"""

from app.nlq.processor import NaturalLanguageProcessor
from app.nlq.api import nlq_blueprint

# Export public interfaces only
__all__ = ['NaturalLanguageProcessor', 'nlq_blueprint']
