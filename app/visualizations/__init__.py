"""
Visualization components for the dashboard
"""
import importlib
import os
import pkgutil
from typing import Dict, List, Any, Optional
from flask import Blueprint, render_template, jsonify
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.ensemble import IsolationForest

# Create blueprint
visualization_bp = Blueprint('visualization', __name__)

# Dictionary to store visualization formatter instances
_formatters: Dict[str, Any] = {}

def register_formatter(formatter_id: str, formatter_instance: Any) -> None:
    """Register a visualization formatter with the system"""
    global _formatters
    _formatters[formatter_id] = formatter_instance

def get_formatter(formatter_id: str) -> Optional[Any]:
    """Get a registered formatter by ID"""
    return _formatters.get(formatter_id)

def list_formatters() -> List[Dict[str, Any]]:
    """List all registered formatters with their metadata"""
    return [
        {
            'id': formatter_id,
            'name': formatter.name,
            'description': formatter.description,
            'visualization_types': formatter.visualization_types,
            'data_types': formatter.data_types
        }
        for formatter_id, formatter in _formatters.items()
    ]

class BaseVisualization:
    def __init__(self):
        self.colors = px.colors.qualitative.Set3
        
    def to_json(self, fig):
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    def create_correlation_matrix(self, data, title="Cross-Domain Correlation Matrix"):
        """Create a correlation matrix heatmap for cross-domain data"""
        corr_matrix = data.corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))
        fig.update_layout(
            title=title,
            xaxis_title="Features",
            yaxis_title="Features"
        )
        return self.to_json(fig)
    
    def create_prediction_plot(self, actual_data, predicted_data, confidence_intervals=None, title="Prediction vs Actual"):
        """Create a line plot comparing actual vs predicted values with confidence intervals"""
        fig = go.Figure()
        
        # Add actual data
        fig.add_trace(go.Scatter(
            x=actual_data.index,
            y=actual_data.values,
            name='Actual',
            line=dict(color=self.colors[0])
        ))
        
        # Add predicted data
        fig.add_trace(go.Scatter(
            x=predicted_data.index,
            y=predicted_data.values,
            name='Predicted',
            line=dict(color=self.colors[1])
        ))
        
        # Add confidence intervals if provided
        if confidence_intervals is not None:
            fig.add_trace(go.Scatter(
                x=predicted_data.index,
                y=confidence_intervals['upper'],
                fill=None,
                mode='lines',
                line_color='rgba(0,100,80,0.2)',
                name='Upper Bound'
            ))
            fig.add_trace(go.Scatter(
                x=predicted_data.index,
                y=confidence_intervals['lower'],
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,100,80,0.2)',
                name='Lower Bound'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Value",
            hovermode='x unified'
        )
        return self.to_json(fig)
    
    def create_scatter_matrix(self, data, title="Cross-Domain Scatter Matrix"):
        """Create a scatter matrix for visualizing relationships between multiple variables"""
        fig = px.scatter_matrix(
            data,
            dimensions=data.columns,
            color=data.columns[0] if len(data.columns) > 0 else None,
            title=title
        )
        return self.to_json(fig)
    
    def create_confidence_visualization(self, predictions, confidence_scores, title="Prediction Confidence"):
        """Create a visualization showing prediction confidence levels"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=predictions.index,
            y=predictions.values,
            mode='lines+markers',
            name='Predictions',
            line=dict(color=self.colors[0])
        ))
        
        # Add confidence scores as error bars
        fig.add_trace(go.Scatter(
            x=predictions.index,
            y=predictions.values,
            mode='markers',
            marker=dict(
                size=confidence_scores * 10,  # Scale confidence to marker size
                color=confidence_scores,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Confidence')
            ),
            name='Confidence'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Predicted Value",
            showlegend=True
        )
        return self.to_json(fig)
    
    def create_time_series_decomposition(self, data, period=12, title="Time Series Decomposition"):
        """Create a time series decomposition plot showing trend, seasonal, and residual components"""
        decomposition = seasonal_decompose(data, period=period)
        
        fig = go.Figure()
        
        # Original data
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data.values,
            name='Original',
            line=dict(color=self.colors[0])
        ))
        
        # Trend
        fig.add_trace(go.Scatter(
            x=decomposition.trend.index,
            y=decomposition.trend.values,
            name='Trend',
            line=dict(color=self.colors[1])
        ))
        
        # Seasonal
        fig.add_trace(go.Scatter(
            x=decomposition.seasonal.index,
            y=decomposition.seasonal.values,
            name='Seasonal',
            line=dict(color=self.colors[2])
        ))
        
        # Residual
        fig.add_trace(go.Scatter(
            x=decomposition.resid.index,
            y=decomposition.resid.values,
            name='Residual',
            line=dict(color=self.colors[3])
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Value",
            hovermode='x unified'
        )
        return self.to_json(fig)
    
    def create_feature_importance(self, feature_names, importance_scores, title="Feature Importance"):
        """Create a horizontal bar chart showing feature importance"""
        fig = go.Figure()
        
        # Sort features by importance
        sorted_idx = np.argsort(importance_scores)
        pos = np.arange(sorted_idx.shape[0]) + .5
        
        fig.add_trace(go.Bar(
            y=[feature_names[i] for i in sorted_idx],
            x=importance_scores[sorted_idx],
            orientation='h',
            marker=dict(
                color=importance_scores[sorted_idx],
                colorscale='Viridis'
            )
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Importance Score",
            yaxis_title="Features",
            showlegend=False
        )
        return self.to_json(fig)
    
    def create_anomaly_detection(self, data, contamination=0.1, title="Anomaly Detection"):
        """Create a scatter plot showing normal points and anomalies"""
        # Fit isolation forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso_forest.fit_predict(data.values.reshape(-1, 1))
        
        # Create figure
        fig = go.Figure()
        
        # Normal points
        normal_mask = predictions == 1
        fig.add_trace(go.Scatter(
            x=data.index[normal_mask],
            y=data.values[normal_mask],
            mode='markers',
            name='Normal',
            marker=dict(
                color=self.colors[0],
                size=8
            )
        ))
        
        # Anomalies
        anomaly_mask = predictions == -1
        fig.add_trace(go.Scatter(
            x=data.index[anomaly_mask],
            y=data.values[anomaly_mask],
            mode='markers',
            name='Anomaly',
            marker=dict(
                color='red',
                size=12,
                symbol='x'
            )
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Value",
            showlegend=True
        )
        return self.to_json(fig)
    
    def create_comparison_view(self, datasets, title="Comparison View"):
        """Create a comparison view of multiple datasets"""
        fig = go.Figure()
        
        for i, (name, data) in enumerate(datasets.items()):
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data.values,
                name=name,
                line=dict(color=self.colors[i % len(self.colors)])
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Value",
            hovermode='x unified'
        )
        return self.to_json(fig)

# Initialize the visualization class
visualization = BaseVisualization()

# Import formatters explicitly
from app.visualizations.base_formatter import BaseFormatter
from app.visualizations.time_series_formatter import TimeSeriesFormatter
from app.visualizations.geospatial_formatter import GeospatialFormatter
from app.visualizations.correlation_formatter import CorrelationFormatter
from app.visualizations.dashboard_formatter import DashboardFormatter

# Register formatters
register_formatter('time-series', TimeSeriesFormatter())
register_formatter('geospatial', GeospatialFormatter())
register_formatter('correlation', CorrelationFormatter())
register_formatter('dashboard', DashboardFormatter())
