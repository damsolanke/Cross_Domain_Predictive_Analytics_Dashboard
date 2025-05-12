import pytest
import pandas as pd
import numpy as np
from ..core_visualizations import CoreVisualizations

@pytest.fixture
def sample_time_series_data():
    """Create sample time series data for testing."""
    dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
    values = np.random.randn(10).cumsum()
    return pd.DataFrame({
        'date': dates,
        'value': values
    })

@pytest.fixture
def sample_correlation_data():
    """Create sample data for correlation testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'var1': np.random.randn(100),
        'var2': np.random.randn(100),
        'var3': np.random.randn(100)
    })

def test_advanced_time_series(sample_time_series_data):
    """Test advanced time series plot creation."""
    # Test basic plot
    fig = CoreVisualizations.create_advanced_time_series(
        data=sample_time_series_data,
        x_col='date',
        y_col='value',
        title='Test Time Series'
    )
    
    assert fig is not None
    assert len(fig.data) == 1  # Only main line
    assert fig.layout.title.text == 'Test Time Series'
    
    # Test with confidence intervals
    confidence_intervals = {
        'upper': sample_time_series_data['value'] + 1,
        'lower': sample_time_series_data['value'] - 1
    }
    
    fig = CoreVisualizations.create_advanced_time_series(
        data=sample_time_series_data,
        x_col='date',
        y_col='value',
        title='Test Time Series with Confidence',
        confidence_intervals=confidence_intervals
    )
    
    assert len(fig.data) == 3  # Main line + upper + lower bounds
    
    # Test with secondary y-axis
    secondary_y = {
        'column': 'value',
        'name': 'Secondary',
        'title': 'Secondary Value'
    }
    
    fig = CoreVisualizations.create_advanced_time_series(
        data=sample_time_series_data,
        x_col='date',
        y_col='value',
        title='Test Time Series with Secondary Y',
        secondary_y=secondary_y
    )
    
    assert len(fig.data) == 2  # Main line + secondary y-axis
    assert 'yaxis2' in fig.layout

def test_advanced_correlation_matrix(sample_correlation_data):
    """Test advanced correlation matrix creation."""
    # Test basic correlation matrix
    fig = CoreVisualizations.create_advanced_correlation_matrix(
        data=sample_correlation_data,
        title='Test Correlation'
    )
    
    assert fig is not None
    assert len(fig.data) == 1  # Single heatmap
    assert fig.layout.title.text == 'Test Correlation'
    
    # Test with clustering
    fig = CoreVisualizations.create_advanced_correlation_matrix(
        data=sample_correlation_data,
        title='Test Correlation with Clustering',
        cluster=True
    )
    
    assert fig is not None
    assert len(fig.data) == 1
    
    # Test without annotations
    fig = CoreVisualizations.create_advanced_correlation_matrix(
        data=sample_correlation_data,
        title='Test Correlation without Annotations',
        annotations=False
    )
    
    assert fig is not None
    assert fig.data[0].text is None

def test_prediction_comparison(sample_time_series_data):
    """Test prediction comparison plot creation."""
    # Create predicted data
    predicted_data = sample_time_series_data.copy()
    predicted_data['value'] = predicted_data['value'] * 1.1  # Simulate predictions
    
    # Test basic comparison
    fig = CoreVisualizations.create_prediction_comparison(
        actual_data=sample_time_series_data,
        predicted_data=predicted_data,
        x_col='date',
        actual_col='value',
        predicted_col='value',
        title='Test Prediction Comparison'
    )
    
    assert fig is not None
    assert len(fig.data) == 2  # Actual + predicted lines
    assert fig.layout.title.text == 'Test Prediction Comparison'
    
    # Test with error metrics
    error_metrics = {
        'RMSE': 0.5,
        'MAE': 0.4,
        'R2': 0.9
    }
    
    fig = CoreVisualizations.create_prediction_comparison(
        actual_data=sample_time_series_data,
        predicted_data=predicted_data,
        x_col='date',
        actual_col='value',
        predicted_col='value',
        title='Test Prediction Comparison with Metrics',
        error_metrics=error_metrics
    )
    
    assert fig is not None
    assert len(fig.layout.annotations) > 0  # Should have error metrics annotation 