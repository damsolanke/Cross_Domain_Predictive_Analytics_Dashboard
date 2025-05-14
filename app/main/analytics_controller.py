"""
Controller for analytics related views.
"""

from flask import Blueprint, render_template

# Create a Blueprint for analytics views
analytics = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics.route('/models')
def models():
    """View for predictive models."""
    return render_template('analytics/models.html', title='Predictive Models')

@analytics.route('/reports')
def reports():
    """View for analytics reports."""
    return render_template('analytics/reports.html', title='Analytics Reports')