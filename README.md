# Cross-Domain Predictive Analytics Dashboard

An advanced web-based data analytics platform that integrates multiple domain-specific data sources and applies machine learning models to deliver predictive analytics, cross-domain correlations, and actionable insights across different domains.

![Cross-Domain Analytics Dashboard](https://i.ibb.co/4TyY9SZ/dashboard-preview.png)

## ✨ Key Features

- **Multi-Domain Data Integration**: Seamlessly connects weather, economic, transportation, and social media data
- **Intuitive Dashboard Interface**: Modern, responsive design with interactive data visualization
- **Cross-Domain Correlation Analysis**: Discover hidden relationships between different data domains
- **Natural Language Query Interface**: Ask questions in plain English and get visual answers
- **Real-time Data Processing**: Live data updates with intelligent caching and fallback mechanisms
- **Predictive Analytics**: Machine learning models forecast future trends based on cross-domain patterns
- **Resilient API Design**: Robust error handling with graceful degradation and fallback options

## Team Members

- **Ade Solanke** - Project Lead & System Integration
- **Chaozheng Zhang** - Machine Learning & Predictive Modeling
- **Emmanuel Jonathan** - Data Visualization
- **Julie Peter** - API Integration & Data Processing
- **Rujeko Macheka** - Frontend Development

## Project Overview

The Cross-Domain Predictive Analytics Dashboard integrates data from various domains (weather forecasts, economic indicators, social media trends, transportation metrics) and applies advanced analytics to identify patterns and correlations across these seemingly unrelated datasets. The system provides predictive analytics, correlation mapping, and actionable insights to support proactive decision-making across multiple domains.

![Dashboard Overview](https://i.ibb.co/VqRCGKB/dashboard-overview-diagram.png)

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

- **Multi-Domain Data Integration Framework**: Orchestrated connectivity to diverse public APIs for comprehensive data collection
- **Cross-Domain Correlation Analysis Engine**: Advanced pattern recognition across traditionally siloed datasets
- **Interactive Visualization Suite**: Rich, responsive interface for exploring complex data relationships
- **Resilient API Architecture**: Sophisticated fallback mechanisms ensuring continuous operation during API disruptions
- **Temporal Analysis Controls**: Flexible time horizon selection from 24 hours to annual perspectives
- **Multi-Tiered Caching System**: Domain-aware data persistence strategy optimizing performance and API usage
- **Domain-Specific Use Case Templates**: Pre-configured analytical environments for specialized business scenarios

## System Architecture

The application follows a layered, modular architecture with clean separation of concerns:

![System Architecture](https://i.ibb.co/QJnNM8n/system-architecture.png)

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
   - System integration to coordinate components
   - Cross-domain correlation calculation engine
   - Forecast generation for future data points
   - Data management services for organizing information flow

3. **Data Services Layer**
   - Comprehensive data cleaning for handling missing values
   - Data transformation for consistent formats
   - Validation services for data integrity

4. **Data Sources Layer**
   - API connectors for external data sources:
     - Weather data from OpenWeatherMap API
     - Economic data from Alpha Vantage API
     - News and trends from News API
     - Transportation data from TomTom Traffic API
   - Multi-level caching with time-based expiration
   - Fallback to simulated data when API connections fail

## Data Flow Architecture

The dashboard implements a comprehensive flow to process data from external APIs:

![Data Flow Diagram](https://i.ibb.co/s3JBYbz/data-flow-diagram.png)

```
┌────────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────┐
│ Domain     │    │ Data          │    │ Data        │    │ Correlation  │
│ API        │───▶│ Processing    │───▶│ Storage     │───▶│ Analysis     │
│ Connectors │    │ Pipeline      │    │ & Caching   │    │              │
└────────────┘    └───────────────┘    └─────────────┘    └──────────────┘
                                                                  │
                                                                  ▼
┌────────────┐    ┌───────────────┐
│ Dashboard  │◀───│ Visualization │
│ UI         │    │ Engine        │
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

2. **Data Processing Pipeline**
   - Raw data undergoes multi-stage transformation through cleaning, normalization, and enrichment phases
   - Missing data management with domain-appropriate interpolation strategies and confidence indicators
   - Metadata enrichment with contextual indicators and calculated derivative metrics
   - Structural validation ensuring data integrity throughout the processing pipeline

3. **Storage & Caching Architecture**
   - Domain-optimized caching system with strategic TTL (Time-To-Live) configuration:
     - Weather data: 30-minute TTL (optimized for meteorological update frequencies)
     - Economic data: 60-minute TTL (aligned with market data refresh patterns)
     - News/social data: 15-minute TTL (balancing trend detection with API efficiency)
     - Transportation data: 10-minute TTL (prioritizing real-time traffic conditions)
   - Progressive offline capability through browser localStorage persistence
   - API request governance with intelligent rate limiting and request batching

4. **Advanced Correlation Analysis**
   - Statistical modeling techniques for identifying non-obvious relationships between disparate data domains
   - Quantitative confidence scoring with adaptive thresholds for correlation reliability assessment
   - Multi-dimensional visualization of correlation patterns, strengths, and temporal consistency
   - Configurable significance filtering for focusing on high-value cross-domain insights

5. **Predictive Analytics Engine**
   - Time-series forecasting with domain-specific modeling parameters
   - Cross-domain correlation-based trend detection and projection
   - Confidence scoring system with quantitative reliability metrics
   - Dynamic prediction horizon adjustment based on data volatility

6. **Visualization Engine & Dashboard Interface**
   - Comprehensive data visualization library with context-aware chart selection
   - Interactive temporal controls for dynamic timeframe adjustment and analysis
   - Real-time updates through WebSocket communication architecture
   - Multi-format visualization suite including time-series charts, correlation matrices, and tabular data representations
   - Responsive design ensuring optimal display across device formats

7. **User Notification Framework**
   - Context-sensitive status notifications for data operations and system events
   - Graduated error messaging with appropriate severity levels and recovery suggestions
   - Toast-style interface elements ensuring minimally intrusive user experience
   - Event-driven notification architecture integrated with data refresh cycles

## Cross-Domain Correlation Framework

The system employs a multi-stage analytical process to identify and quantify relationships between diverse data domains:

![Correlation Framework](https://i.ibb.co/vHnPfB4/correlation-framework.png)

```
┌─────────────────┐       ┌─────────────────┐
│                 │       │                 │
│  Integrated     │──────▶│  Correlation    │
│  Data Pipeline  │       │  Analysis       │
│                 │       │                 │
└─────────────────┘       └─────────────────┘
                                  │
                                  ▼
┌─────────────────┐       ┌─────────────────┐
│                 │       │                 │
│  Visualization  │◀──────│  Relationship   │
│  Generator      │       │  Classification │
│                 │       │                 │
└─────────────────┘       └─────────────────┘
```

### Correlation Capabilities

- **Temporal Analysis Controls**: Examine correlation patterns across customizable time horizons
- **Strength-Based Classification**: Filter correlations by significance thresholds (strong, moderate, weak)
- **Domain-Specific Filtering**: Focus analysis on targeted domain combinations
- **Interactive Visualization Suite**: Explore correlations through multiple visual representations

## Multi-Tiered Caching Architecture

The dashboard implements a domain-aware, multi-tiered caching system:

![Caching Architecture](https://i.ibb.co/rMXszQn/caching-architecture.png)

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

### Caching Strategy

- **Domain-Specific TTL (Time-To-Live)**: Cache expiration periods optimized by data domain:
  - Weather data: 30-minute expiration (balances freshness with API rate limits)
  - Economic data: 60-minute expiration (optimized for market data update frequencies)
  - News data: 15-minute expiration (ensures trend data remains current)
  - Transportation data: 10-minute expiration (prioritizes real-time traffic conditions)

- **Strategic Cache Invalidation**: Cache is selectively cleared based on user interaction patterns:
  - Dynamic invalidation when timeframe parameters change
  - TTL-based automatic expiration
  - Selective refresh of affected data segments

- **Progressive Web Application Support**: Critical data persisted to localStorage for offline functionality

- **Graceful Degradation Pipeline**: If API calls fail, the system implements a cascading fallback strategy:
  1. Server memory cache retrieval
  2. Client-side localStorage retrieval
  3. Procedurally generated demonstration data with domain-appropriate patterns

## Natural Language Query Architecture

The system implements a comprehensive natural language interface for data exploration:

![NLQ System](https://i.ibb.co/T8Lr8js/nlq-system.png)

```
┌─────────────────┐     ┌────────────────┐     ┌────────────────┐
│                 │     │                │     │                │
│  Query Input    │────▶│  Processing    │────▶│  Visualization │
│  Interface      │     │  Engine        │     │  Engine        │
│                 │     │                │     │                │
└─────────────────┘     └────────────────┘     └────────────────┘
```

### NLQ Implementation

- **Query Processing Engine**: Pattern-based text processing to extract metrics, domains, and time references
- **Intelligent Visualization Selection**: Automatic selection of appropriate visualization formats based on query content
- **Intuitive Input Interface**: Streamlined interface for entering questions in natural language

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

The dashboard includes performance optimizations:

1. **Intelligent Caching**: Reduces API calls with domain-specific cache expiration
2. **Client-side Storage**: Uses localStorage for data persistence
3. **Throttled API Requests**: Stays within free tier API limits
4. **Lazy Loading**: Components load only when needed to improve initial render times
5. **Optimized Asset Delivery**: Minified CSS and JS for faster loading
6. **Connection Error Resilience**: Multiple fallback layers for handling API failures

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Recent Updates

### May 2024 - Major Dashboard Enhancement

![Dashboard UI Improvements](https://i.ibb.co/j8xmS5r/dashboard-ui-updates.png)

#### UI/UX Redesign
- **Modern Interface Overhaul**: Completely redesigned dashboard with clean, modern aesthetics
- **Color-Coded Domain Sections**: Each data domain has unique visual identity for better usability
- **Improved Card Components**: Enhanced card design with subtle shadows and rounded corners
- **Responsive Layout**: Optimized for all device sizes from mobile to large desktop displays
- **Interactive Elements**: Added hover effects and visual feedback for all interactive components
- **Typography Improvements**: Implemented Inter font family for better readability

#### Data Visualization Enhancements
- **Weather Visualizations**: Added dynamic weather icons that change based on conditions
- **Temperature Gauges**: Implemented color-gradient temperature scales for intuitive reading
- **Economic Indicators**: Enhanced economic data displays with trend indicators and color coding
- **Improved Charts**: Better designed time-series and bar charts with consistent styling
- **Loading States**: Added informative loading indicators with progress feedback

#### Reliability Improvements
- **Robust Error Handling**: Enhanced error detection and recovery for all API interactions
- **Graceful Degradation**: Implemented fallbacks to ensure dashboard always displays useful data
- **Multi-Tier Caching**: Improved caching architecture with domain-specific expiration policies
- **API Format Adaptability**: Added support for handling different API response formats
- **Error Notification System**: Better error messages with actionable information

![Dashboard Components](https://i.ibb.co/B4wQ9JG/dashboard-components.png)

#### Dashboard Component Architecture
- **Modular Component Design**: Each data domain now uses a unified component architecture for better consistency
- **Flexible Layout System**: Grid-based layout system that adapts to different screen sizes
- **Design System Implementation**: Comprehensive CSS variable system for consistent styling
- **Themeable Components**: All UI elements support light/dark mode through CSS variable swapping
- **Optimized Rendering**: Improved DOM manipulation for smoother updates and transitions

### API Integration (May 2024)
- **Integrated Domain-Specific APIs**: All data connectors now properly integrate with public APIs:
  - Weather data from OpenWeatherMap API
  - Economic data from Alpha Vantage API
  - News and trends from News API
  - Transportation data from TomTom Traffic API and TransitLand
- **Error Handling Framework**: Implemented comprehensive error detection, logging, and recovery
- **Multi-Level Caching**: Domain-optimized caching strategy with intelligent TTL configuration
- **API Documentation**: Created detailed guides for API configuration and usage

### System Improvements (May 2024)
- **Fixed System Status Page**: Resolved the 404 error by correcting route configuration
- **Timeframe Selector Enhancements**: Improved timeframe selection with proper data updates
- **Socket Connection Upgrades**: Enhanced error handling for WebSocket connections
- **Data Refresh Pipeline**: Implemented proper data refresh on timeframe changes
- **NLQ Visualization Selection**: Improved Natural Language Query with better visualization selection

### Cross-Domain Correlation Engine (May 2024)
![Correlation Analysis](https://i.ibb.co/vZnDbj2/correlation-analysis.png)

- **Enhanced Matrix Visualization**: Improved correlation matrix with better color coding and interaction
- **Network Graph Visualization**: Added force-directed graph for exploring correlation relationships
- **Confidence Scoring System**: Implemented advanced statistical significance testing for correlations
- **Temporal Correlation Analysis**: Added tools for tracking how correlations change over time
- **Strength-Based Filtering**: New filters for showing only strong, moderate, or weak correlations

![Error Handling Framework](https://i.ibb.co/PNqQRbp/error-handling-framework.png)

#### Error Handling Framework
- **Multi-Level Recovery Strategy**: Implemented graduated fallback mechanisms for API failures:
  1. Retry with exponential backoff
  2. Server-side cached data retrieval
  3. Client-side localStorage data retrieval
  4. Procedurally generated demo data
- **User-Friendly Error Messages**: Enhanced error displays with contextual information and recovery suggestions
- **Real-Time Error Logging**: Comprehensive error tracking for easier debugging and system monitoring
- **Data Validation Pipeline**: Robust validation at multiple stages to prevent invalid data propagation

## Acknowledgments

- **Team Members**: Ade Solanke, Chaozheng Zhang, Emmanuel Jonathan, Julie Peter, and Rujeko Macheka
- Faculty advisor: Dr. Sharma Rajinder
- Dallas Baptist University Department of Computer Science