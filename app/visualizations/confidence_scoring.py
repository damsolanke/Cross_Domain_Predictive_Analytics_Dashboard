import plotly.graph_objects as go
import numpy as np
from typing import Dict, List, Optional, Union

class ConfidenceScoring:
    """Visualization components for model confidence scoring and reliability analysis."""
    
    @staticmethod
    def create_confidence_radar(
        metrics: Dict[str, float],
        thresholds: Optional[Dict[str, float]] = None,
        title: str = "Model Confidence Radar"
    ) -> go.Figure:
        """
        Create a radar chart showing different confidence metrics.
        
        Args:
            metrics: Dictionary of metric names and values
            thresholds: Optional dictionary of metric thresholds
            title: Plot title
        """
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        # Add first value again to close the polygon
        values.append(values[0])
        categories.append(categories[0])
        
        fig = go.Figure()
        
        # Add confidence metrics
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Confidence Metrics'
        ))
        
        # Add threshold reference if provided
        if thresholds:
            threshold_values = [thresholds[cat] for cat in categories[:-1]]
            threshold_values.append(threshold_values[0])
            
            fig.add_trace(go.Scatterpolar(
                r=threshold_values,
                theta=categories,
                fill='toself',
                name='Thresholds',
                line=dict(dash='dash')
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title=title
        )
        
        return fig
    
    @staticmethod
    def create_reliability_heatmap(
        predicted_probs: np.ndarray,
        actual_outcomes: np.ndarray,
        n_bins: int = 10,
        title: str = "Prediction Reliability Heatmap"
    ) -> go.Figure:
        """
        Create a heatmap showing prediction reliability across probability ranges.
        
        Args:
            predicted_probs: Array of predicted probabilities
            actual_outcomes: Array of actual outcomes
            n_bins: Number of probability bins
            title: Plot title
        """
        # Create probability bins
        bins = np.linspace(0, 1, n_bins + 1)
        bin_indices = np.digitize(predicted_probs, bins) - 1
        
        # Calculate reliability for each bin
        reliability_matrix = np.zeros((n_bins, n_bins))
        for i in range(n_bins):
            mask = bin_indices == i
            if np.any(mask):
                actual_in_bin = actual_outcomes[mask]
                reliability_matrix[i, :] = np.histogram(
                    actual_in_bin,
                    bins=bins,
                    density=True
                )[0]
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=reliability_matrix,
            x=np.round(bins[:-1], 2),
            y=np.round(bins[:-1], 2),
            colorscale='RdYlBu_r',
            colorbar=dict(title='Density')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Predicted Probability',
            yaxis_title='Actual Probability',
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_confidence_trend(
        timestamps: Union[List[str], np.ndarray],
        confidence_scores: Union[List[float], np.ndarray],
        window_size: Optional[int] = None,
        title: str = "Confidence Score Trend"
    ) -> go.Figure:
        """
        Create a trend visualization of confidence scores over time.
        
        Args:
            timestamps: List of timestamps
            confidence_scores: List of confidence scores
            window_size: Optional window size for moving average
            title: Plot title
        """
        fig = go.Figure()
        
        # Add raw confidence scores
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=confidence_scores,
            mode='lines',
            name='Raw Confidence',
            line=dict(color='blue', width=1)
        ))
        
        # Add moving average if window_size provided
        if window_size:
            moving_avg = np.convolve(
                confidence_scores,
                np.ones(window_size)/window_size,
                mode='valid'
            )
            
            fig.add_trace(go.Scatter(
                x=timestamps[window_size-1:],
                y=moving_avg,
                mode='lines',
                name=f'{window_size}-point Moving Average',
                line=dict(color='red', width=2)
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Confidence Score',
            template='plotly_white',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_cross_domain_confidence(
        domain_scores: Dict[str, Dict[str, float]],
        title: str = "Cross-Domain Confidence Comparison"
    ) -> go.Figure:
        """
        Create a visualization comparing confidence scores across different domains.
        
        Args:
            domain_scores: Dictionary of domains and their confidence metrics
            title: Plot title
        """
        # Prepare data
        domains = list(domain_scores.keys())
        metrics = list(set().union(*[set(scores.keys()) for scores in domain_scores.values()]))
        
        # Create traces for each metric
        fig = go.Figure()
        
        for metric in metrics:
            values = [domain_scores[domain].get(metric, 0) for domain in domains]
            
            fig.add_trace(go.Bar(
                name=metric,
                x=domains,
                y=values,
                text=np.round(values, 2),
                textposition='auto',
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Domain',
            yaxis_title='Confidence Score',
            template='plotly_white',
            barmode='group',
            showlegend=True
        )
        
        return fig 