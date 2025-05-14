# System Integration & Real-Time Analytics

This module implements the system integration and real-time analytics components for the Cross-Domain Predictive Analytics Dashboard.

## Features

- **Data Pipeline**: Central integration for API data, ML models, and visualizations
- **Real-Time Updates**: WebSocket implementation for instant data updates
- **Alert System**: Customizable thresholds and notifications
- **System Status Dashboard**: Monitoring and visualization of system health
- **Component Integration**: Framework for easy integration of new components

## Components

1. **Data Pipeline** (`app/system_integration/pipeline.py`)
   - Manages data flow between system components
   - Queues for asynchronous processing
   - Health metrics and monitoring
   
2. **Alert System** (`app/system_integration/alert_system.py`)
   - Configurable alert thresholds
   - Multi-level alerts (info, warning, critical)
   - Alert history tracking
   
3. **System Integrator** (`app/system_integration/integration.py`)
   - Connects all system components
   - Dynamic component discovery and registration
   - System lifecycle management
   
4. **Real-Time Updates** (via Flask-SocketIO)
   - WebSocket connections for live updates
   - Event-based communication
   - Client subscription management

## API Endpoints

- `/system/system-status`: System status dashboard
- `/api/system-health`: API endpoint for system health metrics
- `/api/data-flow-status`: API endpoint for data flow information
- `/api/alerts/config`: Configuration endpoint for alerts
- `/api/alerts/current`: Current active alerts

## WebSocket Events

The system uses WebSockets for real-time updates:

- `data_update`: Real-time data updates
- `alert_notification`: Alert notifications
- `connection_response`: Connection confirmation
- `subscription_response`: Subscription confirmation

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python run.py
   ```

3. Visit the system status dashboard:
   ```
   http://localhost:5000/system/system-status
   ```

## Testing

Run the integration tests:
```
python -m unittest discover -s tests
```

## Architecture

For detailed system architecture documentation, see [system_architecture.md](system_architecture.md).