#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 10 21:31:18 2025

@author: mz
"""

import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error

# Prepare LSTM data
def prepare_lstm_data(data, time_step=10):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(np.array(data).reshape(-1, 1))
    
    X, y = [], []
    for i in range(len(scaled_data) - time_step):
        X.append(scaled_data[i:i + time_step, 0])
        y.append(scaled_data[i + time_step, 0])
    
    X = np.array(X)
    y = np.array(y)
    return X, y, scaler

# Create LSTM model
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=False, input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Forecast using LSTM
def forecast_lstm(model, scaler, last_data, time_step=10):
    last_data_scaled = scaler.transform(np.array(last_data).reshape(-1, 1))
    X_input = last_data_scaled[-time_step:].reshape(1, time_step, 1)
    prediction = model.predict(X_input)
    return scaler.inverse_transform(prediction)[0, 0]

# Training and forecasting for each domain (e.g., weather, market, etc.)
def train_forecast_model(data, domain_name, time_step=10):
    X, y, scaler = prepare_lstm_data(data)
    model = create_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=20, batch_size=8, verbose=0)  # Adjust epochs for performance
    forecast = forecast_lstm(model, scaler, data)
    return forecast, model, scaler

# Cross-domain correlation: Calculate correlations between domains (using Pearson correlation)
def calculate_cross_domain_correlation(data_dict):
    weather = np.array([item['temperature'] for item in data_dict['weather']])
    market = np.array([item['market'] for item in data_dict['economic']])
    traffic = np.array([item['traffic_speed'] for item in data_dict['transportation']])
    sentiment = np.array([item['social_sentiment'] for item in data_dict['social_media']])
    
    # Example: Pearson correlation between weather and market data
    weather_market_corr = np.corrcoef(weather, market)[0, 1]
    
    return {
        "weather_market_corr": weather_market_corr,
        # Add correlation for other domain pairs as needed
    }

# Confidence scoring: Using Mean Absolute Error as a confidence score proxy
def confidence_score(actual, forecast):
    return mean_absolute_error(actual, forecast)

# Scenario modeling: Adjust input and predict future outcomes
def what_if_scenario(model, scaler, last_data, change_factor=1.1, time_step=10):
    # Modify the last_data to simulate a "what-if" scenario
    modified_data = [x * change_factor for x in last_data]  # Example of modifying the last value
    return forecast_lstm(model, scaler, modified_data, time_step)

# Full workflow to train, forecast, and analyze cross-domain predictions
def forecast_all_domains(data):
    weather_data = [item['temperature'] for item in data['weather']]
    market_data = [item['market'] for item in data['economic']]
    
    # Train models for each domain
    weather_forecast, weather_model, weather_scaler = train_forecast_model(weather_data, 'weather')
    market_forecast, market_model, market_scaler = train_forecast_model(market_data, 'market')
    
    # Cross-domain correlation
    correlations = calculate_cross_domain_correlation(data)
    
    return {
        "weather_forecast": weather_forecast,
        "market_forecast": market_forecast,
        "cross_domain_correlations": correlations,
        "confidence_score_weather": confidence_score(weather_data[-1], weather_forecast),
        "confidence_score_market": confidence_score(market_data[-1], market_forecast),
    }