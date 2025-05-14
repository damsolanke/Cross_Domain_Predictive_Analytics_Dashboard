# Cross-Domain Correlation Utilities

The cross-domain correlation utilities are designed to analyze relationships between different data domains in the Cross-Domain Predictive Analytics Dashboard. These utilities help identify correlations, generate insights, and detect anomalies in real-time data.

## Overview

The cross-domain correlation system consists of the following components:

1. **CrossDomainCorrelator**: The core class that manages correlation data and analysis.
2. **System Integration**: Integration with the SystemIntegrator to process data in real-time.
3. **API Endpoints**: REST endpoints for accessing correlation data and insights.
4. **Frontend Visualization**: Interactive visualization of correlation data in the dashboard.

## Using the CrossDomainCorrelator

The `CrossDomainCorrelator` class provides methods for analyzing relationships between different data domains and generating insights.

### Initialization

```python
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator

# Initialize with default domains
correlator = CrossDomainCorrelator()

# Or specify domains to monitor
correlator = CrossDomainCorrelator(domains=["weather", "economic", "transportation", "social_media"])
```

### Adding Data

To add data for correlation analysis:

```python
# Add weather data
correlator.add_data("weather", {
    "timestamp": "2023-09-15T14:30:00",
    "temperature": 25.5,
    "humidity": 60,
    "wind_speed": 5.2
})

# Add transportation data
correlator.add_data("transportation", {
    "timestamp": "2023-09-15T14:30:00",
    "congestion": 0.65,
    "avg_speed": 35.2,
    "vehicle_count": 850
})
```

### Calculating Correlations

To calculate correlations between domains:

```python
# Calculate correlations
correlations = correlator.calculate_correlations()

# Access specific correlations
weather_vs_transport = correlations.get("weather_vs_transportation", {})
if "temperature" in weather_vs_transport and "congestion" in weather_vs_transport["temperature"]:
    temp_congestion_corr = weather_vs_transport["temperature"]["congestion"]
    print(f"Correlation between temperature and congestion: {temp_congestion_corr}")
```

### Generating Insights

To generate insights from correlations:

```python
# Generate insights
insights = correlator.generate_insights()

# Print insights
for insight in insights:
    print(f"{insight['domain1']} vs {insight['domain2']}: {insight['description']}")
```

### Detecting Anomalies

To detect anomalies in cross-domain relationships:

```python
# Detect anomalies
anomalies = correlator.detect_anomalies()

# Print anomalies
for anomaly in anomalies:
    print(f"ANOMALY: {anomaly['description']}")
```

### Getting Visualization Data

To prepare correlation data for visualization:

```python
# Get visualization data
viz_data = correlator.get_correlation_data_for_visualization()

# Access different visualization components
heatmap_data = viz_data["heatmap_data"]
network_data = viz_data["network_data"]
insights = viz_data["insights"]
```

### Configuring Time Window

To adjust the time window for correlation analysis:

```python
# Set time window to 12 hours
correlator.set_time_window(hours=12)

# Set time window to 7 days
correlator.set_time_window(hours=7*24)
```

## API Endpoints

The following API endpoints are available for accessing correlation data:

### GET /api/correlation/data

Returns the current correlation data formatted for visualization.

**Example Response:**
```json
{
  "correlation_matrices": [...],
  "heatmap_data": [...],
  "network_data": {
    "nodes": [...],
    "links": [...]
  },
  "insights": [...]
}
```

### GET /api/correlation/insights

Returns insights generated from cross-domain correlations.

**Example Response:**
```json
[
  {
    "type": "correlation",
    "domain1": "weather",
    "domain2": "transportation",
    "variable1": "temperature",
    "variable2": "congestion",
    "correlation_value": 0.85,
    "direction": "positive",
    "description": "Strong positive correlation (0.85) between weather's temperature and transportation's congestion",
    "timestamp": "2023-09-15T15:00:00"
  }
]
```

### POST /api/correlation/configure

Configures correlation parameters.

**Request Body:**
```json
{
  "time_window_hours": 24
}
```

**Example Response:**
```json
{
  "status": "success",
  "message": "Correlation time window set to 24 hours"
}
```

## WebSocket Events

The following WebSocket events are available for real-time updates:

### correlation_data

Emitted when new correlation data is available.

### correlation_insight

Emitted when a new correlation insight is discovered.

### correlation_anomaly

Emitted when a correlation anomaly is detected.

## Using in the Dashboard

The dashboard provides interactive visualizations for correlation data:

1. **Correlation Heatmap**: Visualizes the strength of correlations between variables from different domains.
2. **Correlation Network**: Displays significant relationships as a network graph.
3. **Correlation Insights**: Shows key insights derived from correlations.
4. **Correlation Settings**: Allows configuring parameters like time window.

## Use Cases

1. **Cross-Domain Impact Analysis**: Identify how changes in one domain affect others.
2. **Anomaly Detection**: Detect unusual patterns in cross-domain relationships.
3. **Predictive Analysis**: Use correlations to improve prediction accuracy.
4. **Insight Generation**: Automatically generate insights from data relationships.

## Implementation Details

The cross-domain correlation system uses:

- **Pandas** for data manipulation and correlation calculations
- **NumPy** for numerical operations
- **Threading** for concurrent processing
- **Visualization Libraries** (Highcharts, D3.js) for interactive visualizations