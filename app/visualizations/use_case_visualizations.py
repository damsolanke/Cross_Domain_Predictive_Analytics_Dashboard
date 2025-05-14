import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class UseCaseVisualizations:
    """Visualization components for specific use cases in the Cross-Domain Analytics Dashboard."""
    
    @staticmethod
    def create_supply_chain_visualization(
        inventory_data: pd.DataFrame,
        demand_data: pd.DataFrame,
        time_col: str,
        inventory_col: str,
        demand_col: str,
        title: str = "Supply Chain Analysis"
    ) -> go.Figure:
        """
        Create supply chain optimization visualization.
        
        Args:
            inventory_data: DataFrame with inventory levels
            demand_data: DataFrame with demand forecasts
            time_col: Column name for time axis
            inventory_col: Column name for inventory levels
            demand_col: Column name for demand values
            title: Plot title
        """
        fig = go.Figure()
        
        # Add inventory levels
        fig.add_trace(go.Scatter(
            x=inventory_data[time_col],
            y=inventory_data[inventory_col],
            name='Inventory Level',
            mode='lines',
            line=dict(color='blue', width=2)
        ))
        
        # Add demand forecast
        fig.add_trace(go.Scatter(
            x=demand_data[time_col],
            y=demand_data[demand_col],
            name='Demand Forecast',
            mode='lines',
            line=dict(color='red', dash='dash')
        ))
        
        # Add safety stock level if available
        if 'safety_stock' in inventory_data.columns:
            fig.add_trace(go.Scatter(
                x=inventory_data[time_col],
                y=inventory_data['safety_stock'],
                name='Safety Stock Level',
                mode='lines',
                line=dict(color='green', dash='dot')
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Units',
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_health_response_visualization(
        health_data: pd.DataFrame,
        location_col: str,
        metric_col: str,
        time_col: str,
        title: str = "Public Health Response Analysis"
    ) -> go.Figure:
        """
        Create public health response planning visualization.
        
        Args:
            health_data: DataFrame with health metrics
            location_col: Column name for locations
            metric_col: Column name for health metric
            time_col: Column name for time
            title: Plot title
        """
        # Create animated choropleth if coordinates available
        if all(col in health_data.columns for col in ['latitude', 'longitude']):
            fig = px.scatter_mapbox(
                health_data,
                lat='latitude',
                lon='longitude',
                color=metric_col,
                size=metric_col,
                animation_frame=time_col,
                hover_name=location_col,
                title=title
            )
            fig.update_layout(mapbox_style="carto-positron")
        else:
            # Create heatmap of health metrics by location and time
            pivot_data = health_data.pivot(
                index=location_col,
                columns=time_col,
                values=metric_col
            )
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='RdYlBu_r'
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title='Time',
                yaxis_title='Location',
                template='plotly_white'
            )
        
        return fig
    
    @staticmethod
    def create_urban_infrastructure_visualization(
        infrastructure_data: pd.DataFrame,
        component_col: str,
        status_col: str,
        usage_col: Optional[str] = None,
        title: str = "Urban Infrastructure Status"
    ) -> go.Figure:
        """
        Create urban infrastructure management visualization.
        
        Args:
            infrastructure_data: DataFrame with infrastructure components and their status
            component_col: Column name for infrastructure components
            status_col: Column name for status indicators
            usage_col: Optional column name for usage metrics
            title: Plot title
        """
        fig = go.Figure()
        
        # Create status overview
        status_counts = infrastructure_data[status_col].value_counts()
        
        # Create donut chart for status distribution
        fig.add_trace(go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.4,
            name='Status Distribution'
        ))
        
        # Add usage metrics if available
        if usage_col:
            fig.add_trace(go.Bar(
                x=infrastructure_data[component_col],
                y=infrastructure_data[usage_col],
                name='Usage Metrics',
                yaxis='y2'
            ))
            
            fig.update_layout(
                yaxis2=dict(
                    title='Usage',
                    overlaying='y',
                    side='right'
                )
            )
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_financial_market_visualization(
        market_data: pd.DataFrame,
        time_col: str,
        price_col: str,
        volume_col: Optional[str] = None,
        indicators: Optional[Dict[str, List[float]]] = None,
        title: str = "Financial Market Analysis"
    ) -> go.Figure:
        """
        Create financial market strategy visualization.
        
        Args:
            market_data: DataFrame with market data
            time_col: Column name for time
            price_col: Column name for price data
            volume_col: Optional column name for volume data
            indicators: Optional dictionary of technical indicators
            title: Plot title
        """
        fig = go.Figure()
        
        # Add price candlesticks if OHLC data available
        if all(col in market_data.columns for col in ['open', 'high', 'low', 'close']):
            fig.add_trace(go.Candlestick(
                x=market_data[time_col],
                open=market_data['open'],
                high=market_data['high'],
                low=market_data['low'],
                close=market_data['close'],
                name='OHLC'
            ))
        else:
            # Add line plot for price
            fig.add_trace(go.Scatter(
                x=market_data[time_col],
                y=market_data[price_col],
                name='Price',
                line=dict(color='blue')
            ))
        
        # Add volume if available
        if volume_col:
            fig.add_trace(go.Bar(
                x=market_data[time_col],
                y=market_data[volume_col],
                name='Volume',
                yaxis='y2',
                opacity=0.3
            ))
        
        # Add technical indicators if provided
        if indicators:
            for name, values in indicators.items():
                fig.add_trace(go.Scatter(
                    x=market_data[time_col],
                    y=values,
                    name=name,
                    line=dict(dash='dash')
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Price',
            template='plotly_white',
            yaxis2=dict(
                title='Volume',
                overlaying='y',
                side='right'
            ) if volume_col else None
        )
        
        return fig 