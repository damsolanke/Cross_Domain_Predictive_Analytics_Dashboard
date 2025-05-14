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

# Visualization Component Documentation

## Overview
The visualization component provides a comprehensive suite of interactive data visualizations for the Cross-Domain Predictive Analytics Dashboard. It includes various visualization types, export capabilities, and real-time updates.

## Available Visualizations

### 1. Correlation Matrix
- **Purpose**: Shows relationships between different features across domains
- **Features**:
  - Interactive heatmap
  - Color-coded correlation values
  - Hover tooltips with exact values
  - Export capabilities

### 2. Prediction vs Actual
- **Purpose**: Compares predicted values with actual values
- **Features**:
  - Line plot with actual and predicted values
  - Confidence intervals
  - Interactive zoom and pan
  - Export capabilities

### 3. Time Series Decomposition
- **Purpose**: Breaks down time series data into trend, seasonal, and residual components
- **Features**:
  - Multiple component visualization
  - Interactive controls
  - Export capabilities

### 4. Feature Importance
- **Purpose**: Shows the relative importance of different features
- **Features**:
  - Horizontal bar chart
  - Color-coded importance scores
  - Interactive sorting
  - Export capabilities

### 5. Anomaly Detection
- **Purpose**: Identifies and visualizes anomalies in the data
- **Features**:
  - Scatter plot with highlighted anomalies
  - Adjustable contamination parameter
  - Interactive filtering
  - Export capabilities

### 6. Comparison View
- **Purpose**: Compares multiple datasets side by side
- **Features**:
  - Multiple line plots
  - Interactive legend
  - Synchronized zooming
  - Export capabilities

## Interactive Features

### Time Range Selection
- Last 24 Hours
- Last Week
- Last Month
- Last 3 Months
- Last Year
- Custom Range

### Update Intervals
- 1 Minute
- 5 Minutes
- 15 Minutes
- 1 Hour

### Export Options
- CSV format
- JSON format
- Single visualization export
- Batch export of all visualizations

## API Endpoints

### Visualization Endpoints
- `/visualization/correlation-matrix`
- `/visualization/prediction-plot`
- `/visualization/time-series-decomposition`
- `/visualization/feature-importance`
- `/visualization/anomaly-detection`
- `/visualization/comparison-view`

### Export Endpoints
- `/visualization/export/<format>`
- `/visualization/batch-export`

## Usage Examples

### Basic Visualization
```python
from app.visualizations import visualization

# Create correlation matrix
data = pd.DataFrame(...)
correlation_viz = visualization.create_correlation_matrix(data)

# Create prediction plot
actual_data = pd.Series(...)
predicted_data = pd.Series(...)
prediction_viz = visualization.create_prediction_plot(actual_data, predicted_data)
```

### Export Data
```python
# Export single visualization
response = requests.post('/visualization/export/csv', json={'data': data})

# Batch export
response = requests.post('/visualization/batch-export', json={
    'format': 'csv',
    'visualizations': {
        'correlation-matrix': correlation_data,
        'prediction-plot': prediction_data
    }
})
```

## Best Practices

1. **Data Preparation**
   - Ensure data is properly formatted before visualization
   - Handle missing values appropriately
   - Normalize data when necessary

2. **Performance Optimization**
   - Use appropriate update intervals
   - Implement data caching when possible
   - Optimize large datasets before visualization

3. **User Experience**
   - Provide clear labels and titles
   - Include interactive tooltips
   - Enable easy export options

4. **Error Handling**
   - Implement proper error handling for data processing
   - Provide meaningful error messages
   - Include fallback options for failed visualizations

## Troubleshooting

### Common Issues

1. **Visualization Not Updating**
   - Check update interval settings
   - Verify data format
   - Check network connectivity

2. **Export Failures**
   - Verify data format
   - Check file permissions
   - Ensure sufficient memory

3. **Performance Issues**
   - Reduce update frequency
   - Optimize data size
   - Implement data sampling

## Contributing

1. Follow the project's coding standards
2. Add appropriate tests for new features
3. Update documentation for changes
4. Submit pull requests with clear descriptions

## Future Enhancements

1. Additional visualization types
2. More export formats
3. Enhanced interactivity
4. Advanced filtering options
5. Custom visualization templates 