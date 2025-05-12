import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional

class CoreVisualizations:
    """Core visualization components for the Cross-Domain Predictive Analytics Dashboard."""
    
    @staticmethod
    def create_advanced_time_series(
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: str,
        confidence_intervals: Optional[Dict[str, List[float]]] = None,
        annotations: Optional[List[Dict]] = None,
        secondary_y: Optional[Dict] = None
    ) -> go.Figure:
        """
        Create an advanced time series plot with multiple features.
        
        Args:
            data: DataFrame containing the time series data
            x_col: Column name for x-axis (time)
            y_col: Column name for y-axis (values)
            title: Plot title
            confidence_intervals: Optional dictionary with upper and lower confidence bounds
            annotations: Optional list of annotation dictionaries
            secondary_y: Optional dictionary for secondary y-axis data
        """
        fig = go.Figure()
        
        # Add main line with hover template
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode='lines',
            name='Actual',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>Time</b>: %{x}<br>' +
                         '<b>Value</b>: %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add confidence intervals if provided
        if confidence_intervals:
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=confidence_intervals['upper'],
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=confidence_intervals['lower'],
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor='rgba(31, 119, 180, 0.2)',
                name='Confidence Interval',
                hoverinfo='skip'
            ))
        
        # Add secondary y-axis if provided
        if secondary_y:
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[secondary_y['column']],
                mode='lines',
                name=secondary_y['name'],
                yaxis='y2',
                line=dict(color=secondary_y.get('color', '#ff7f0e'), 
                         dash=secondary_y.get('dash', 'dot'))
            ))
        
        # Add annotations if provided
        if annotations:
            for annotation in annotations:
                fig.add_annotation(
                    x=annotation['x'],
                    y=annotation['y'],
                    text=annotation['text'],
                    showarrow=annotation.get('showarrow', True),
                    arrowhead=annotation.get('arrowhead', 2),
                    ax=annotation.get('ax', 0),
                    ay=annotation.get('ay', -40)
                )
        
        # Update layout with advanced features
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                y=0.95
            ),
            xaxis=dict(
                title='Time',
                showgrid=True,
                gridcolor='lightgray',
                rangeslider=dict(visible=True)
            ),
            yaxis=dict(
                title='Value',
                showgrid=True,
                gridcolor='lightgray'
            ),
            hovermode='x unified',
            template='plotly_white',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Add secondary y-axis if provided
        if secondary_y:
            fig.update_layout(
                yaxis2=dict(
                    title=secondary_y.get('title', 'Secondary Value'),
                    overlaying='y',
                    side='right'
                )
            )
        
        return fig
    
    @staticmethod
    def create_advanced_correlation_matrix(
        data: pd.DataFrame,
        title: str,
        correlation_method: str = 'pearson',
        annotations: bool = True,
        cluster: bool = True
    ) -> go.Figure:
        """
        Create an advanced correlation matrix with clustering and annotations.
        
        Args:
            data: DataFrame containing the variables to correlate
            title: Plot title
            correlation_method: Correlation method ('pearson', 'spearman', or 'kendall')
            annotations: Whether to show correlation values
            cluster: Whether to cluster the correlation matrix
        """
        # Calculate correlation matrix
        corr_matrix = data.corr(method=correlation_method)
        
        # Apply clustering if requested
        if cluster:
            from scipy.cluster import hierarchy
            from scipy.spatial.distance import squareform
            
            # Convert correlation to distance
            dist_matrix = 1 - np.abs(corr_matrix)
            dist_array = squareform(dist_matrix)
            
            # Perform hierarchical clustering
            linkage_matrix = hierarchy.linkage(dist_array, method='complete')
            order = hierarchy.dendrogram(linkage_matrix, no_plot=True)['leaves']
            
            # Reorder correlation matrix
            corr_matrix = corr_matrix.iloc[order, order]
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.round(2) if annotations else None,
            texttemplate='%{text}' if annotations else None,
            textfont={"size": 10},
            colorbar=dict(
                title='Correlation',
                titleside='right'
            )
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                y=0.95
            ),
            xaxis=dict(
                title='Variables',
                tickangle=45
            ),
            yaxis=dict(
                title='Variables'
            ),
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_prediction_comparison(
        actual_data: pd.DataFrame,
        predicted_data: pd.DataFrame,
        x_col: str,
        actual_col: str,
        predicted_col: str,
        title: str,
        error_metrics: Optional[Dict[str, float]] = None
    ) -> go.Figure:
        """
        Create an advanced comparison plot between actual and predicted values.
        
        Args:
            actual_data: DataFrame containing actual values
            predicted_data: DataFrame containing predicted values
            x_col: Column name for x-axis
            actual_col: Column name for actual values
            predicted_col: Column name for predicted values
            title: Plot title
            error_metrics: Optional dictionary of error metrics to display
        """
        fig = go.Figure()
        
        # Add actual values
        fig.add_trace(go.Scatter(
            x=actual_data[x_col],
            y=actual_data[actual_col],
            mode='lines',
            name='Actual',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>Time</b>: %{x}<br>' +
                         '<b>Actual Value</b>: %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add predicted values
        fig.add_trace(go.Scatter(
            x=predicted_data[x_col],
            y=predicted_data[predicted_col],
            mode='lines',
            name='Predicted',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            hovertemplate='<b>Time</b>: %{x}<br>' +
                         '<b>Predicted Value</b>: %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add error metrics if provided
        if error_metrics:
            metrics_text = '<br>'.join([
                f"{metric}: {value:.3f}"
                for metric, value in error_metrics.items()
            ])
            
            fig.add_annotation(
                xref="paper",
                yref="paper",
                x=0.02,
                y=0.98,
                text=metrics_text,
                showarrow=False,
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="black",
                borderwidth=1,
                borderpad=4
            )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                y=0.95
            ),
            xaxis=dict(
                title='Time',
                showgrid=True,
                gridcolor='lightgray',
                rangeslider=dict(visible=True)
            ),
            yaxis=dict(
                title='Value',
                showgrid=True,
                gridcolor='lightgray'
            ),
            hovermode='x unified',
            template='plotly_white',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig 