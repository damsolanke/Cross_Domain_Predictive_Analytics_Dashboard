# External API Configuration Guide

This guide explains how to obtain and configure API keys for the external services integrated into the Cross-Domain Predictive Analytics Dashboard.

## Table of Contents
1. [OpenWeatherMap API](#openweathermap-api)
2. [Alpha Vantage API](#alpha-vantage-api)
3. [News API](#news-api)
4. [TomTom API](#tomtom-api)
5. [Configuring API Keys in the System](#configuring-api-keys-in-the-system)

## OpenWeatherMap API

### How to Obtain
1. Visit [OpenWeatherMap](https://openweathermap.org/) and create a free account
2. After signing up, go to your account page and navigate to the "API Keys" tab
3. Generate a new API key (or use the default one provided)

### Functionality
- Current weather data for cities worldwide
- 5-day weather forecasts
- Historical weather data (limited in free tier)

### Usage Limitations (Free Tier)
- 60 calls per minute
- 1,000,000 calls per month
- Limited historical data access
- Current weather and 5-day forecasts only
- No minute or hourly forecasts

## Alpha Vantage API

### How to Obtain
1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and register for a free API key
2. Complete the registration form
3. The API key will be displayed and emailed to you

### Functionality
- Economic indicators (GDP, inflation, unemployment)
- Interest rates data
- Retail sales data
- Financial market data

### Usage Limitations (Free Tier)
- 5 API calls per minute
- 500 API calls per day
- Limited to a subset of economic indicators
- Historical data limited to certain time periods

## News API

### How to Obtain
1. Visit [News API](https://newsapi.org/register) and create a free account
2. After registering, your API key will be displayed on your account page

### Functionality
- Access to trending news topics
- News sentiment analysis
- Multiple news sources worldwide
- Filtering by topics, countries, and sources

### Usage Limitations (Free Tier)
- 100 requests per day
- Limited to the previous month of articles
- No commercial usage allowed
- Search results limited to 100 articles per request
- Must attribute News API as the source

## TomTom API

### How to Obtain
1. Visit [TomTom Developer Portal](https://developer.tomtom.com/user/register) and create a free account
2. After registering, go to the Dashboard
3. Create a new project to generate an API key

### Functionality
- Real-time traffic data
- Traffic flow information
- Travel time estimates
- Traffic incidents and congestion levels

### Usage Limitations (Free Tier)
- 2,500 free daily requests
- Maximum of 5 requests per second
- Maps display requires attribution
- Limited historical data access
- Limited route planning capabilities

## Configuring API Keys in the System

There are two ways to configure API keys in the system:

### 1. Environment Variables (Recommended)

Set the following environment variables. All keys are read in one place,
`app/config.py`; each has a canonical name and a legacy alias (the generic name
the code used originally). The canonical name takes precedence when both are set.

```bash
# For OpenWeatherMap API (legacy alias: WEATHER_API_KEY)
export OPENWEATHER_API_KEY=your_openweathermap_api_key

# For Alpha Vantage API (legacy alias: ECONOMIC_API_KEY)
export ALPHAVANTAGE_API_KEY=your_alphavantage_api_key

# For News API, used for social media trends (legacy alias: SOCIAL_MEDIA_API_KEY)
export NEWSAPI_KEY=your_newsapi_key

# For TomTom API (legacy alias: TRANSPORTATION_API_KEY)
export TOMTOM_API_KEY=your_tomtom_api_key
```

For permanent configuration:
- Linux/macOS: Add the above commands to your `~/.bashrc` or `~/.zshrc` file
- Windows: Set through System Properties > Environment Variables

### 2. Configuration File (Alternative)

Copy `.env.example` to `.env` (which is git-ignored) and fill in the keys you have:

```
OPENWEATHER_API_KEY=your_openweathermap_api_key
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
NEWSAPI_KEY=your_newsapi_key
TOMTOM_API_KEY=your_tomtom_api_key
```

### Fallback Mechanism

If an API key is not provided (or is blank), the system logs a single warning for that service at startup and uses simulated data to demonstrate functionality. No request is sent to the external API without a key. In logs or the UI, you'll see an indication that fallback data is being used instead of real API data.

When using real API keys, the dashboard will automatically switch to using real data from the external services.