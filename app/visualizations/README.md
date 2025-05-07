# Cross-Domain Predictive Analytics Dashboard - Visualization Components

## Overview
This module provides visualization components for the Cross-Domain Predictive Analytics Dashboard. It includes specialized visualizations for different use cases and a comprehensive confidence scoring system.

## Components

### Use Case Visualizations (`use_case_visualizations.py`)

#### Supply Chain Optimization
- Real-time inventory level tracking
- Demand forecast comparison
- Safety stock level monitoring
- Interactive time series visualization

#### Public Health Response Planning
- Geographic health metric distribution
- Temporal trend analysis
- Location-based heatmaps
- Animated choropleth maps (when coordinates available)

#### Urban Infrastructure Management
- Infrastructure status overview
- Component usage metrics
- Status distribution visualization
- Multi-metric comparison

#### Financial Market Strategy
- Price and volume analysis
- OHLC candlestick charts
- Technical indicator integration
- Market trend visualization

### Confidence Scoring System (`confidence_scoring.py`)

#### Model Confidence Radar
- Multi-metric confidence visualization
- Threshold comparison
- Interactive polar chart
- Customizable metrics

#### Prediction Reliability Heatmap
- Probability calibration analysis
- Binned reliability assessment
- Density-based visualization
- Customizable bin size

#### Confidence Trend Visualization
- Temporal confidence tracking
- Moving average analysis
- Interactive time series
- Flexible window size

#### Cross-Domain Confidence Comparison
- Domain-wise metric comparison
- Grouped bar visualization
- Multiple metric support
- Interactive legend

## Usage Examples

### Supply Chain Visualization
```python
from app.visualizations.use_case_visualizations import UseCaseVisualizations

# Create supply chain visualization
fig = UseCaseVisualizations.create_supply_chain_visualization(
    inventory_data=inventory_df,
    demand_data=demand_df,
    time_col='date',
    inventory_col='stock_level',
    demand_col='forecast',
    title='Supply Chain Analysis'
)
```

### Confidence Scoring
```python
from app.visualizations.confidence_scoring import ConfidenceScoring

# Create confidence radar
metrics = {
    'Accuracy': 0.85,
    'Precision': 0.82,
    'Recall': 0.88,
    'F1': 0.84
}

fig = ConfidenceScoring.create_confidence_radar(
    metrics=metrics,
    title='Model Performance Metrics'
)
```

## Best Practices

### Data Preparation
1. Ensure data is properly cleaned and formatted
2. Handle missing values appropriately
3. Use consistent datetime formats
4. Normalize numerical values when necessary

### Visualization Design
1. Use appropriate color schemes for different metrics
2. Include clear titles and axis labels
3. Add interactive elements for better user experience
4. Implement proper error handling

### Performance Optimization
1. Limit data points for large datasets
2. Use efficient data structures
3. Implement caching when appropriate
4. Optimize figure updates

## Integration Guidelines

### Frontend Integration
1. Import required visualization components
2. Initialize with appropriate data
3. Update layouts as needed
4. Handle user interactions

### Backend Integration
1. Prepare data in required format
2. Handle API requests efficiently
3. Implement proper error handling
4. Cache results when appropriate

## Testing
All visualization components include comprehensive tests in the `tests` directory. Run tests using:
```bash
pytest app/visualizations/tests/
``` 