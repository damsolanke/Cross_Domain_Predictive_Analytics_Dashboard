# Cross-Domain Predictive Analytics Dashboard

An advanced web-based data analytics platform that integrates multiple domain-specific data sources and applies machine learning models to deliver predictive analytics, cross-domain correlations, and actionable insights across different domains.

![Cross-Domain Analytics Dashboard](https://via.placeholder.com/1200x600?text=Cross-Domain+Predictive+Analytics+Dashboard)

## Team Members

- **Ade Solanke** - Project Lead & System Integration
- **Chaozheng Zhang** - Machine Learning & Predictive Modeling
- **Emmanuel Jonathan** - Data Visualization
- **Julie Peter** - API Integration & Data Processing
- **Rujeko Macheka** - Frontend Development

## Project Overview

The Cross-Domain Predictive Analytics Dashboard integrates data from various domains (weather forecasts, economic indicators, social media trends, transportation metrics) and applies advanced analytics to identify patterns and correlations across these seemingly unrelated datasets. The system provides predictive analytics, correlation mapping, and actionable insights to support proactive decision-making across multiple domains.

## Technology Stack

### Frontend
- **HTML5/CSS3/JavaScript** - Core web technologies
- **Bootstrap 5** - Responsive UI framework
- **Chart.js** - Interactive data visualization
- **D3.js** - Advanced custom visualizations 
- **Plotly.js** - Scientific and statistical charts
- **Socket.IO Client** - Real-time communications
- **jQuery** - DOM manipulation and Ajax requests
- **localStorage API** - Client-side data persistence

### Backend
- **Python 3.9+** - Core programming language
- **Flask** - Web framework
- **Flask-SocketIO** - WebSocket implementation
- **SQLAlchemy** - ORM for database operations
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **SciPy** - Statistical analysis
- **scikit-learn** - Machine learning algorithms
- **TensorFlow/Keras** - Deep learning for time series prediction
- **NLTK/spaCy** - Natural language processing
- **Redis** - In-memory data store for caching
- **Celery** - Task queue for background processing

### Data Storage
- **SQLite** - Development database
- **PostgreSQL** - Production database
- **MongoDB** - Unstructured data storage
- **Redis** - Caching and session management

### DevOps & Infrastructure
- **Docker** - Containerization
- **Git** - Version control
- **GitHub Actions** - CI/CD pipeline
- **Pytest** - Testing framework
- **Nginx** - Web server (production)
- **Gunicorn** - WSGI server (production)

### External Services
- **Weather API**: OpenWeatherMap API
- **Economic Data API**: Alpha Vantage API
- **News/Trends API**: News API
- **Transportation Data APIs**: TomTom Traffic API, TransitLand API, OpenStreetMap

## Key Features

- **Multi-Domain Data Integration**: Seamlessly connect to diverse public APIs to fetch real-time data across different domains
- **Advanced Predictive Modeling**: Implement machine learning algorithms to analyze historical patterns and generate forecasts
- **Cross-Domain Correlation Analysis**: Discover and visualize non-obvious correlations between datasets from different domains
- **Real-Time Analytics**: Process and visualize data updates in real-time through WebSocket connections
- **Natural Language Queries (NLQ)**: Ask questions in plain English to explore the data and get visualized answers
- **Customizable Dashboard**: Tailor the dashboard to focus on specific domains or metrics
- **Year-Long Data Analysis**: Analyze correlations and trends across time ranges from hours to a full year
- **Intelligent Caching**: Optimize performance with multi-tiered caching system and local storage persistence
- **Adaptive Visualizations**: Dynamic visualization components that adapt to different data types and patterns

## System Architecture

The application follows a layered, modular architecture with clean separation of concerns:

```
┌───────────────────────────────────────────────────────────┐
│                      User Interface                       │
│                                                           │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │ Dashboards   │  │ NLQ Interface│  │ Visualization│   │
│   └──────────────┘  └──────────────┘  └──────────────┘   │
└───────────────────────────────────────────────────────────┘
                           ▲
                           │
                           ▼
┌───────────────────────────────────────────────────────────┐
│                    Application Core                       │
│                                                           │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │ System       │  │ Correlation  │  │ Prediction   │   │
│   │ Integration  │  │ Engine       │  │ Engine       │   │
│   └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                           │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │ NL Processor │  │ Alert System │  │ Data Pipeline│   │
│   └──────────────┘  └──────────────┘  └──────────────┘   │
└───────────────────────────────────────────────────────────┘
                           ▲
                           │
                           ▼
┌───────────────────────────────────────────────────────────┐
│                     Data Services                         │
│                                                           │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │ Data         │  │ Validation   │  │ Transformation│   │
│   │ Cleaning     │  │ Services     │  │ Services     │   │
│   └──────────────┘  └──────────────┘  └──────────────┘   │
└───────────────────────────────────────────────────────────┘
                           ▲
                           │
                           ▼
┌───────────────────────────────────────────────────────────┐
│                     Data Sources                          │
│                                                           │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │ Weather API  │  │ Economic API │  │ Social API   │   │
│   └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                           │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │Transport API │  │  Cache       │  │Local Storage │   │
│   └──────────────┘  └──────────────┘  └──────────────┘   │
└───────────────────────────────────────────────────────────┘
```

### Architectural Components

1. **User Interface Layer**
   - Responsive web interface built with Flask templates, HTML5, CSS3, and modern JavaScript
   - Real-time dashboard components with dynamic updates
   - Natural Language Query interface for intuitive data exploration
   - Interactive visualization components supporting various chart types

2. **Application Core Layer**
   - System Integration module for coordinating all components
   - Correlation Engine for identifying cross-domain relationships
   - Prediction Engine using machine learning models for forecasting
   - Natural Language Processing for understanding user queries
   - Alert System for monitoring and notifying based on thresholds
   - Data Pipeline for managing data flow through the system

3. **Data Services Layer**
   - Data Cleaning services to handle missing values and outliers
   - Validation Services to ensure data integrity and quality
   - Transformation Services to normalize and prepare data for analysis

4. **Data Sources Layer**
   - Domain-specific API connectors with rate limiting and authentication:
     - Weather data from OpenWeatherMap API
     - Economic data from Alpha Vantage API
     - News and trends from News API
     - Transportation data from TomTom Traffic API, TransitLand API, and OpenStreetMap
   - Multi-level caching system with configurable expiration times
   - Local storage for offline support and performance optimization
   - Intelligent fallback to simulated data when API connections fail

## Data Flow and Processing

The Cross-Domain Analytics Dashboard uses a sophisticated data flow architecture to process incoming data from various domains:

```
┌────────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────┐
│ Domain     │    │ Data          │    │ Data        │    │ Correlation  │
│ API        │───▶│ Processing    │───▶│ Storage     │───▶│ Analysis     │
│ Connectors │    │ Pipeline      │    │ & Caching   │    │              │
└────────────┘    └───────────────┘    └─────────────┘    └──────────────┘
                                                                  │
                                                                  ▼
┌────────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────┐
│ Dashboard  │    │ Visualization │    │ Prediction  │    │ Alert        │
│ UI         │◀───│ Engine        │◀───│ Engine      │◀───│ System       │
│            │    │               │    │             │    │              │
└────────────┘    └───────────────┘    └─────────────┘    └──────────────┘
```

### Process Steps

1. **Data Collection**
   - Domain-specific API connectors fetch data from external public APIs:
     - OpenWeatherMap API for weather data (current conditions and forecasts)
     - Alpha Vantage API for economic indicators and financial markets data
     - News API for trending topics and sentiment analysis
     - TomTom Traffic API and TransitLand API for transportation metrics
   - API calls are optimized with rate limiting and batching where possible
   - Data is validated for format compliance and completeness
   - Graceful fallback to simulated data when API access fails

2. **Data Processing**
   - Raw data is cleaned, normalized and transformed for analysis
   - Missing values are handled with appropriate strategies (interpolation, defaults)
   - Data is enriched with calculated fields and metadata

3. **Storage & Caching**
   - Multi-tiered caching system with configurable expiration times based on data type and source:
     - Weather data: 30-minute TTL (Time-To-Live)
     - Economic data: 60-minute TTL
     - News/social data: 15-minute TTL
     - Transportation data: 10-minute TTL
   - Intelligent caching with localStorage persistence for offline access
   - Cache size management to prevent memory issues while maintaining performance
   - API-specific rate limiting management to stay within free tier constraints

4. **Correlation Analysis**
   - Pearson and Spearman correlation methods applied to identify relationships
   - Lag analysis to detect time-delayed correlations between domains
   - Seasonal pattern detection and adjustment
   - Confidence scoring to measure reliability of detected correlations

5. **Prediction Engine**
   - Time-series forecasting using ARIMA, LSTM, and ensemble models
   - Cross-domain factor analysis to improve prediction accuracy
   - Automated hyperparameter tuning for model optimization
   - Confidence intervals calculated for all predictions

6. **Visualization & Dashboard**
   - Dynamic rendering based on data characteristics
   - Interactive elements for data exploration
   - Real-time updates via WebSocket connections
   - Multiple visualization formats (heatmaps, networks, time-series, etc.)

7. **Alert System**
   - Threshold-based alerting with configurable rules
   - Anomaly detection for unusual patterns
   - User-defined alert priorities and notification methods

## Cross-Domain Correlation System

The correlation system is a key component that analyzes relationships between data from different domains:

```
┌───────────────────────┐        ┌──────────────────────┐
│                       │        │                      │
│   Time-Series         │───────▶│   Correlation        │
│   Alignment           │        │   Calculation        │
│                       │        │                      │
└───────────────────────┘        └──────────────────────┘
                                           │
                                           ▼
┌───────────────────────┐        ┌──────────────────────┐
│                       │        │                      │
│   Lag Detection       │◀──────▶│   Significance       │
│   Analysis            │        │   Testing            │
│                       │        │                      │
└───────────────────────┘        └──────────────────────┘
                                           │
                                           ▼
┌───────────────────────┐        ┌──────────────────────┐
│                       │        │                      │
│   Visualization       │◀──────▶│   Insight            │
│   Rendering           │        │   Generation         │
│                       │        │                      │
└───────────────────────┘        └──────────────────────┘
```

### Key Correlation Features

- **Multi-resolution Analysis**: Analyze correlations at different time resolutions (hourly, daily, weekly, monthly)
- **Lag Window Analysis**: Detect time-delayed correlations with configurable lag windows
- **Correlation Strength Filtering**: Focus on strong, moderate, or weak correlations as needed
- **Domain-specific Filtering**: Isolate correlations involving specific domains
- **Historical Correlation Trending**: Track how correlations change over time
- **Visualization Options**: View correlations as heatmaps, network graphs, or tabular data
- **Confidence Scoring**: Each correlation includes a confidence score based on data quality and volume

## Caching Architecture

The dashboard implements a sophisticated multi-tiered caching system for optimal performance:

```
┌─────────────────────────────────────────────────────────┐
│                      Client Side                        │
│                                                         │
│  ┌─────────────────┐        ┌───────────────────────┐  │
│  │                 │        │                       │  │
│  │  Memory Cache   │◀──────▶│  localStorage Cache   │  │
│  │  (Short-term)   │        │  (Persistent)         │  │
│  │                 │        │                       │  │
│  └─────────────────┘        └───────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                      Server Side                        │
│                                                         │
│  ┌─────────────────┐        ┌───────────────────────┐  │
│  │                 │        │                       │  │
│  │  Memory Cache   │◀──────▶│  Database Cache       │  │
│  │  (Short-term)   │        │  (Long-term)          │  │
│  │                 │        │                       │  │
│  └─────────────────┘        └───────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Cache Features

- **Time-based Expiration**: Different expiration times based on time range and data type
  - Short time ranges (1h, 6h): 15-30 seconds
  - Medium time ranges (1d, 7d): 1-5 minutes
  - Long time ranges (30d, 90d): 15-30 minutes
  - Very long time ranges (180d, 365d): 1-2 hours

- **Intelligent Cache Invalidation**: Cache is selectively invalidated when:
  - User changes view parameters
  - New data is received that affects existing cached results
  - Server indicates data is stale

- **Offline Support**: Critical data is persisted to localStorage with:
  - Size management to prevent browser storage limits
  - Age-based pruning for older cache items
  - Metadata to verify cache validity

- **Progressive Loading**: UI shows immediately with cached data while fresh data loads in background

- **Fallback System**: If API calls fail, the system falls back to:
  1. In-memory cache
  2. localStorage cache
  3. Generated demo data if no cache exists

## Natural Language Query System

The NLQ system allows users to ask questions in plain English and receive visualized answers:

```
┌─────────────────┐     ┌────────────────┐     ┌────────────────┐
│                 │     │                │     │                │
│  User Query     │────▶│  NLQ Parser    │────▶│  Intent        │
│  Interface      │     │                │     │  Classification│
│                 │     │                │     │                │
└─────────────────┘     └────────────────┘     └────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐     ┌────────────────┐     ┌────────────────┐
│                 │     │                │     │                │
│  Visualization  │◀────│  Query         │◀────│  Domain & Field│
│  Selection      │     │  Execution     │     │  Extraction    │
│                 │     │                │     │                │
└─────────────────┘     └────────────────┘     └────────────────┘
```

### NLQ Features

- **Query Understanding**: Parse natural language to identify query intent, domains, and metrics
- **Intelligent Fallbacks**: Client-side processing if server-side NLQ fails
- **Context Awareness**: Maintain context for follow-up questions
- **Visualization Matching**: Automatically select appropriate visualization for the query
- **Query Suggestions**: Offer relevant query suggestions based on available data
- **History Tracking**: Save and recall previous queries

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/damolasolanke/Cross_Domain_Predictive_Analytics_Dashboard.git
   cd Cross_Domain_Predictive_Analytics_Dashboard
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the setup script to ensure all necessary directories exist:
   ```
   python setup.py
   ```

5. Configure API keys for external services (optional but recommended for real data):
   - Set environment variables for your API keys:
     ```
     export OPENWEATHER_API_KEY=your_openweathermap_api_key
     export ECONOMIC_API_KEY=your_alphavantage_api_key
     export SOCIAL_MEDIA_API_KEY=your_newsapi_key
     export TRANSPORTATION_API_KEY=your_tomtom_api_key
     ```
   - Alternatively, create a `.env` file in the project root with these keys
   - See `docs/api_configuration_guide.md` for detailed instructions on obtaining free API keys

   Note: If no API keys are provided, the system will use simulated data with realistic patterns.

## Running the Application

Start the application with:
```
python run.py
```

The application will be available at [http://localhost:5000](http://localhost:5000)

### Running on Windows

For Windows-specific environments:
```
python run.py --host=0.0.0.0
```

This ensures the server binds to all network interfaces.

## Advanced Features and How to Use Them

### Time Range Selection

The dashboard supports various time ranges for analysis:
- Short-term: 1 hour, 6 hours, 24 hours
- Medium-term: 7 days, 30 days
- Long-term: 90 days, 180 days, 365 days (1 year)

Time ranges can be selected from the dropdown in the dashboard controls.

### Correlation Analysis

To use the correlation analysis features:
1. Navigate to the Cross-Domain tab in the dashboard
2. Select your preferred correlation strength filter (strong, moderate, weak, or all)
3. Choose a specific domain to focus on (optional)
4. View correlations in heatmap or table format using the view toggle
5. Explore the network visualization to see relationships between domains

### Natural Language Queries

To use the NLQ system:
1. Type your question in the query input box
2. Click Submit or press Enter
3. View the visualized results
4. Explore suggested follow-up questions

Example queries:
- "How is the stock market performing today?"
- "Show the relationship between temperature and energy consumption"
- "Predict traffic congestion for tomorrow based on weather"
- "Compare social media sentiment with market trends over the last 30 days"

## Use Cases

The dashboard supports multiple use cases:

### Supply Chain Optimization
- **Challenge**: Anticipate supply chain disruptions and optimize inventory levels
- **Solution**: Analyze correlations between weather events, transportation metrics, and economic indicators
- **Key Metrics**: Delivery times, inventory costs, weather-related delays, economic indices

### Public Health Response Planning
- **Challenge**: Optimize resource allocation for public health events
- **Solution**: Correlate weather data, mobility patterns, and social media health discussions
- **Key Metrics**: Population movement patterns, temperature trends, social media health sentiment

### Urban Infrastructure Management
- **Challenge**: Anticipate infrastructure stress points and plan maintenance
- **Solution**: Analyze relationships between weather, transportation, and infrastructure usage
- **Key Metrics**: Traffic density, weather conditions, maintenance requests

### Financial Market Strategy
- **Challenge**: Identify emerging market trends and opportunities
- **Solution**: Correlate economic indicators with social media sentiment and news analysis
- **Key Metrics**: Market indices, social sentiment scores, keyword trend analysis

## Project Structure

```
Cross_Domain_Predictive_Analytics_Dashboard/
├── app/                       # Main application package
│   ├── api/                   # API integration components
│   │   ├── routes.py          # API routes
│   │   ├── advanced_analytics.py # Advanced analytics functions
│   │   └── connectors/        # API connectors for different domains
│   │       ├── base_connector.py
│   │       ├── economic_connector.py
│   │       ├── social_media_connector.py
│   │       ├── transportation_connector.py
│   │       └── weather_connector.py
│   ├── data_processing/       # Data processing components
│   │   ├── cleaner.py
│   │   ├── correlator.py      # Cross-domain correlation logic
│   │   ├── transformer.py
│   │   └── validator.py
│   ├── main/                  # Main application routes
│   │   ├── routes.py
│   │   └── analytics_controller.py
│   ├── models/                # Machine learning models
│   │   ├── base_model.py
│   │   ├── cross_domain_model.py
│   │   ├── economic_prediction.py
│   │   ├── transportation_prediction.py
│   │   └── weather_prediction.py
│   ├── nlq/                   # Natural language query processing
│   │   ├── api.py
│   │   ├── models.py
│   │   ├── processor.py
│   │   └── routes.py
│   ├── static/                # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   │       ├── dashboard.js   # Main dashboard JavaScript
│   │       └── nlq.js         # NLQ interface JavaScript
│   ├── system_integration/    # System integration components
│   │   ├── integration.py     # Main integration module
│   │   ├── pipeline.py        # Data pipeline logic
│   │   ├── cross_domain_correlation.py # Correlation system
│   │   └── cross_domain_prediction.py  # Prediction system
│   ├── templates/             # HTML templates
│   │   ├── dashboard.html     # Main dashboard template
│   │   ├── nlq.html           # NLQ interface template
│   │   └── correlation.html   # Correlation analysis template
│   └── visualizations/        # Data visualization components
│       ├── core_visualizations.py
│       ├── correlation_formatter.py
│       ├── dashboard_formatter.py
│       └── time_series_formatter.py
├── docs/                      # Documentation files
│   └── system_architecture.md # Detailed architecture documentation
├── tests/                     # Unit and integration tests
├── run.py                     # Application entry point
├── setup.py                   # Setup script
└── requirements.txt           # Project dependencies
```

## Development

### Adding New Data Sources

To add a new data source:

1. Create a new connector in `app/api/connectors/`
2. Extend the `BaseConnector` class
3. Implement required methods (`fetch_data`, `process_data`)
4. Register the connector in `app/api/routes.py`
5. Add corresponding visualization support

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Performance Optimization

The dashboard includes several performance optimizations:

1. **Lazy Loading**: Components are loaded as needed rather than all at once
2. **Multi-tiered Caching**: Reduces API calls and database queries
3. **Parallel Data Fetching**: Multiple data sources are queried simultaneously
4. **Client-side Processing**: Reduces server load for simple operations
5. **Data Compression**: Minimizes network transfer sizes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Recent Updates

### API Integration (May 2024)
- Integrated all data connectors with real public APIs:
  - Weather data from OpenWeatherMap API
  - Economic data from Alpha Vantage API
  - News and trends from News API
  - Transportation data from TomTom Traffic API and TransitLand
- Implemented robust error handling and fallback to simulated data when API requests fail
- Added multi-level caching to optimize API usage and improve performance
- Created comprehensive documentation for API configuration

### UI Improvements (May 2024)
- Fixed the system status page 404 error
- Improved timeframe selection to properly update all visualizations
- Enhanced error handling for socket connections
- Implemented proper data refresh on timeframe changes for all use cases
- Added better feedback for data loading and API connections

## Acknowledgments

- **Team Members**: Ade Solanke, Chaozheng Zhang, Emmanuel Jonathan, Julie Peter, and Rujeko Macheka
- Faculty advisor: Dr. Sharma Rajinder
- Dallas Baptist University Department of Computer Science