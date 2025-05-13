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
- **Socket.IO Client** - Real-time communications
- **localStorage API** - Client-side data persistence

### Backend
- **Python 3.9+** - Core programming language
- **Flask** - Web framework
- **Flask-SocketIO** - WebSocket implementation
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **scikit-learn** - Machine learning algorithms
- **Requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management for API keys

### Data Storage
- **In-memory storage** - Dictionary-based data caching in Python
- **File system storage** - JSON file storage for persistent data
- **Browser localStorage** - Client-side data persistence for offline capability

### DevOps & Infrastructure
- **Git** - Version control
- **Pytest** - Testing framework

### External Services
- **Weather API**: OpenWeatherMap API
- **Economic Data API**: Alpha Vantage API
- **News/Trends API**: News API
- **Transportation Data APIs**: TomTom Traffic API, TransitLand API, OpenStreetMap

## Key Features

- **Multi-Domain Data Integration**: Connect to public APIs to fetch data from different domains
- **Cross-Domain Correlation Analysis**: Identify relationships between datasets from different domains
- **Visualization Dashboard**: View data and correlations through an intuitive interface
- **API Fallback System**: Gracefully degrade to simulated data when APIs are unavailable
- **Customizable Time Ranges**: Analyze data across different time periods from 1 day to 1 year
- **Basic Caching**: Reduce API calls with a simple time-based cache
- **Use Case Templates**: Pre-built templates for common analytical scenarios

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
   - Web interface built with Flask templates, HTML5, CSS3, and JavaScript
   - Dashboard components with Chart.js visualizations
   - Simple query interface for data exploration
   - Form controls for selecting time periods and data filters

2. **Application Core Layer**
   - Basic system integration to coordinate components
   - Simple correlation calculation between data domains
   - Forecast generation for future data points
   - Data management services for organizing information flow

3. **Data Services Layer**
   - Basic data cleaning for handling missing values
   - Data transformation for consistent formats
   - Simple validation for data integrity

4. **Data Sources Layer**
   - API connectors for external data sources:
     - Weather data from OpenWeatherMap API
     - Economic data from Alpha Vantage API
     - News and trends from News API
     - Transportation data from TomTom Traffic API
   - Simple caching with time-based expiration
   - Fallback to simulated data when API connections fail

## Data Flow Process

The dashboard uses a straightforward flow to process data from external APIs:

```
┌────────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────┐
│ API        │    │ Basic         │    │ Memory      │    │ Correlation  │
│ Connectors │───▶│ Processing    │───▶│ Cache       │───▶│ Calculation  │
│            │    │               │    │             │    │              │
└────────────┘    └───────────────┘    └─────────────┘    └──────────────┘
                                                                  │
                                                                  ▼
┌────────────┐    ┌───────────────┐
│ Dashboard  │◀───│ Visualization │
│ UI         │    │ Component     │
│            │    │               │
└────────────┘    └───────────────┘
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
   - Basic caching system with TTL (Time-To-Live) settings:
     - Weather data: 30-minute cache
     - Economic data: 60-minute cache
     - News/social data: 15-minute cache
     - Transportation data: 10-minute cache
   - Browser localStorage for client-side persistence
   - API request throttling to stay within free tier limits

4. **Correlation Analysis**
   - Basic statistical methods to identify relationships between data sets
   - Simple confidence scoring for correlation strength
   - Visualization of correlation strengths between domains

5. **Prediction Engine**
   - Basic time-series forecasting for future data points
   - Cross-domain correlation analysis for trend identification
   - Confidence scores to indicate prediction reliability

6. **Visualization & Dashboard**
   - Chart-based data visualization
   - Interactive elements for timeframe selection
   - Basic WebSocket implementation for updates
   - Multiple chart types (bar charts, line charts, tables)

7. **Notification System**
   - Basic status notifications for data updates
   - Simple error messages for API failures

## Cross-Domain Correlation Approach

The system uses a basic approach to identify relationships between data from different domains:

```
┌─────────────────┐       ┌─────────────────┐
│                 │       │                 │
│  Data           │──────▶│  Correlation    │
│  Collection     │       │  Calculation    │
│                 │       │                 │
└─────────────────┘       └─────────────────┘
                                  │
                                  ▼
┌─────────────────┐       ┌─────────────────┐
│                 │       │                 │
│  Visualization  │◀──────│  Strength       │
│  Rendering      │       │  Classification │
│                 │       │                 │
└─────────────────┘       └─────────────────┘
```

### Correlation Features

- **Time Range Selection**: View correlations for different time periods
- **Correlation Strength Filtering**: Filter by strong, moderate, or weak correlations
- **Domain Filtering**: Focus on correlations from specific domains
- **Basic Visualizations**: View correlations as tables or simple charts

## Caching Implementation

The dashboard implements a simple caching system:

```
┌─────────────────────────────────────────────────────────┐
│                      Client Side                        │
│                                                         │
│  ┌─────────────────┐        ┌───────────────────────┐  │
│  │                 │        │                       │  │
│  │  Variable Cache │◀──────▶│  localStorage Cache   │  │
│  │  (In-memory)    │        │  (Browser Storage)    │  │
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
│  ┌─────────────────┐                                    │
│  │                 │                                    │
│  │  Dictionary     │                                    │
│  │  Cache          │                                    │
│  │                 │                                    │
│  └─────────────────┘                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Cache Features

- **Basic Time-based Expiration**: Cache entries expire based on data type:
  - Weather data: 30-minute expiration
  - Economic data: 60-minute expiration
  - News data: 15-minute expiration
  - Transportation data: 10-minute expiration

- **Simple Cache Invalidation**: Cache is cleared when:
  - User changes timeframe
  - Cache expiration time is reached

- **Basic Offline Support**: Some data persisted to localStorage

- **Fallback Mechanism**: If API calls fail, the system uses:
  1. Memory cache if available
  2. Generated demo data if no cache exists

## Natural Language Query Interface

The system provides a basic interface for entering natural language questions:

```
┌─────────────────┐     ┌────────────────┐     ┌────────────────┐
│                 │     │                │     │                │
│  User Query     │────▶│  Basic Parser  │────▶│  Result        │
│  Interface      │     │                │     │  Display       │
│                 │     │                │     │                │
└─────────────────┘     └────────────────┘     └────────────────┘
```

### NLQ Implementation

- **Basic Query Processing**: Simple parsing to identify metrics and domains
- **Query Visualization**: Display of basic results in appropriate formats
- **Input Interface**: User-friendly interface for entering natural language questions

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

## Performance Considerations

The dashboard includes basic performance optimizations:

1. **Caching**: Reduces API calls with time-based cache expiration
2. **Client-side Storage**: Uses localStorage for data persistence
3. **Throttled API Requests**: Stays within free tier API limits

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