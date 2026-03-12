# Cross-Domain Predictive Analytics Dashboard

[![CI](https://github.com/damsolanke/Cross_Domain_Predictive_Analytics_Dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/damsolanke/Cross_Domain_Predictive_Analytics_Dashboard/actions/workflows/ci.yml)

Real-time predictive analytics platform that correlates data across four public API domains — weather, economic indicators, news sentiment, and transportation — to surface cross-domain insights via an interactive Flask dashboard with WebSocket updates.

## Architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#E3F2FD', 'primaryTextColor': '#1565C0', 'primaryBorderColor': '#1565C0', 'lineColor': '#555', 'secondaryColor': '#FFF3E0', 'tertiaryColor': '#F3E5F5', 'fontSize': '14px'}}}%%
flowchart LR
    subgraph SRC["Data Sources"]
        W[OpenWeatherMap]
        E[Alpha Vantage]
        N[News API]
        T[TomTom Traffic]
    end

    subgraph PROC["Processing Layer"]
        CL[Data Cleaning<br/>& Validation]
        TR[Normalization<br/>& Transformation]
        CA[Domain-Aware<br/>Caching]
    end

    subgraph CORE["Analytics Core"]
        CO[Correlation<br/>Engine]
        PR[Prediction<br/>Engine]
        NL[Natural Language<br/>Query Processor]
    end

    subgraph UI["Dashboard · Flask + Socket.IO"]
        DA[Interactive<br/>Dashboards]
        VZ[Visualization<br/>Suite]
        RT[Real-Time<br/>Updates]
    end

    W & E & N & T --> CL --> TR --> CA --> CO & PR & NL --> DA & VZ & RT

    style SRC fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    style PROC fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    style CORE fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    style UI fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#4A148C
```

### Data Domains

| Domain | Source | Cache TTL | What it provides |
|--------|--------|-----------|------------------|
| **Weather** | OpenWeatherMap API | 30 min | Current conditions, 5-day forecasts, temperature trends |
| **Economic** | Alpha Vantage API | 60 min | Market indices, exchange rates, sector performance |
| **News/Social** | News API | 15 min | Trending topics, sentiment scores, keyword frequency |
| **Transportation** | TomTom Traffic API | 10 min | Traffic density, congestion indices, transit metrics |

### Data Flow

```mermaid
sequenceDiagram
    autonumber
    participant API as Domain APIs
    participant CON as API Connectors
    participant PIPE as Processing Pipeline
    participant CACHE as Cache Layer
    participant ML as Analytics Engine
    participant WS as Socket.IO
    participant UI as Dashboard

    API->>CON: Raw domain data
    CON->>PIPE: Validated payloads
    PIPE->>CACHE: Cleaned & normalized

    alt Cache Hit
        CACHE-->>ML: Cached data (within TTL)
    else Cache Miss
        CON->>API: Refresh from source
    end

    ML->>ML: Cross-domain correlation
    ML->>ML: Trend prediction
    ML->>WS: Updated insights
    WS->>UI: Real-time push
    UI-->>API: User-triggered refresh
```

## Key Capabilities

| Capability | Implementation | Detail |
|-----------|---------------|--------|
| **Cross-domain correlation** | Pearson + rolling window | Identifies non-obvious relationships between weather, markets, traffic, and news |
| **Natural language queries** | Intent classification + entity extraction | Ask "How does temperature affect traffic congestion?" and get visual answers |
| **Real-time updates** | Flask-SocketIO with WebSocket fallback | Dashboard refreshes without page reload when new data arrives |
| **Predictive analytics** | scikit-learn time-series models | Forecasts future trends using cross-domain feature combinations |
| **Graceful degradation** | 3-tier fallback: API → cache → demo data | System stays operational even when all external APIs are down |
| **Use case templates** | 4 pre-built analytical environments | Supply chain, public health, urban infrastructure, financial strategy |

## Quick Start

```bash
git clone https://github.com/damsolanke/Cross_Domain_Predictive_Analytics_Dashboard.git
cd Cross_Domain_Predictive_Analytics_Dashboard
pip install -r requirements.txt
```

```bash
# Configure API keys (optional — runs with demo data without them)
cp .env.example .env
# Edit .env with your API keys

# Start the dashboard
python run.py
# → http://localhost:5000
```

The system works without API keys — it falls back to generated demo data with realistic domain patterns.

## Design Decisions

| Decision | Why | Tradeoff |
|----------|-----|----------|
| **Flask over FastAPI** | Jinja templates for server-rendered dashboards, mature SocketIO integration | No async by default; mitigated by eventlet/gevent |
| **Socket.IO for real-time** | Bidirectional communication, automatic reconnection, room-based broadcasts | Additional server process; simpler than polling |
| **Demo data fallback** | Portfolio reviewers can evaluate the full system without obtaining 4 API keys | Demo patterns are synthetic; real API keys unlock live data |
| **Domain-specific cache TTLs** | Weather changes faster than economic indicators — cache durations reflect real-world update frequencies | More complex invalidation logic |
| **In-memory storage** | No database setup required for reviewers; caching layer handles persistence | Data lost on restart; acceptable for analytics dashboard |
| **Multi-domain correlation engine** | Cross-domain insights are the differentiator — weather×traffic, sentiment×markets | Correlation ≠ causation; confidence scoring helps |

## Project Structure

```
├── app/                          # Main application package
│   ├── api/                      #   API routes + domain connectors
│   │   └── connectors/           #   weather, economic, social, transport
│   ├── data_processing/          #   cleaner, correlator, transformer, validator
│   ├── models/                   #   ML prediction models (weather, economic, transport)
│   ├── nlq/                      #   Natural language query processor + routes
│   ├── system_integration/       #   Pipeline orchestration, socket events, correlation engine
│   ├── visualizations/           #   Chart formatters (time-series, correlation, dashboard)
│   ├── static/                   #   CSS, JavaScript, images
│   └── templates/                #   Jinja2 HTML templates
├── tests/                        #   Integration tests
├── app/tests/                    #   Unit tests (NLP, API, correlation)
├── docs/                         #   Architecture + API configuration guides
├── .github/workflows/ci.yml      #   CI pipeline
├── run.py                        #   Entry point (calls create_app factory)
├── requirements.txt              #   Python dependencies
├── .env.example                  #   Required environment variables
└── LICENSE                       #   MIT
```

## Testing

```bash
# Run all tests
python -m pytest tests/ app/tests/ -v

# Unit tests only (NLP processor, correlation engine, NLQ API)
python -m pytest app/tests/ -v --ignore=app/tests/test_browser.py

# Integration tests (system integration, pipeline, alerts)
python -m pytest tests/ -v
```

## Use Cases

| Use Case | Challenge | Cross-Domain Approach |
|----------|-----------|----------------------|
| **Supply Chain** | Anticipate disruptions | Weather events × transportation delays × economic indicators |
| **Public Health** | Optimize resource allocation | Weather patterns × mobility data × social media health sentiment |
| **Urban Infrastructure** | Plan maintenance proactively | Traffic density × weather conditions × infrastructure usage |
| **Financial Strategy** | Identify emerging trends | Economic indicators × news sentiment × social media momentum |

## License

MIT — see [LICENSE](LICENSE).
