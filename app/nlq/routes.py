"""
Natural Language Query Routes Module
Author: Ademola Solanke
Date: May 2025

This module defines the routes for the NLQ web interface.
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.nlq.utils import format_query_results, get_sample_queries_by_category

# Create Blueprint
nlq_routes = Blueprint('nlq_routes', __name__, url_prefix='/nlq')

@nlq_routes.route('/')
def index():
    """Natural Language Query main page."""
    return render_template('nlq/index.html', title='Natural Language Queries')

@nlq_routes.route('/dashboard')
def dashboard_integration():
    """NLQ integration for the dashboard."""
    # This route provides a compact version of the NLQ interface for embedding in dashboards
    return render_template('nlq/dashboard_integration.html', title='Dashboard NLQ')

@nlq_routes.route('/examples')
def examples():
    """NLQ examples page."""
    sample_queries = get_sample_queries_by_category()
    return render_template('nlq/examples.html', 
                          title='NLQ Examples',
                          sample_queries=sample_queries)

@nlq_routes.route('/help')
def help_page():
    """NLQ help and documentation page."""
    return render_template('nlq/help.html', title='NLQ Help')