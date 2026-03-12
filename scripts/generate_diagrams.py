#!/usr/bin/env python3
"""Generate architecture diagrams for the Cross-Domain Predictive Analytics Dashboard."""

import os

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python
from diagrams.saas.chat import Slack
from diagrams.generic.compute import Rack
from diagrams.generic.database import SQL
from diagrams.generic.network import Firewall
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "images")

CLUSTER_FONT = "Helvetica Neue Bold"
FONT = "Helvetica Neue"


def architecture_diagram():
    """Main system architecture — data sources to dashboard."""
    with Diagram(
        "",
        filename=os.path.join(OUTPUT_DIR, "architecture"),
        outformat="png",
        show=False,
        direction="LR",
        graph_attr={
            "fontsize": "11",
            "fontname": FONT,
            "bgcolor": "#ffffff",
            "pad": "0.6",
            "nodesep": "0.5",
            "ranksep": "0.8",
            "dpi": "150",
        },
        node_attr={"fontsize": "10", "fontname": FONT},
        edge_attr={"fontsize": "8", "fontname": FONT, "color": "#666666"},
    ):
        # --- Data Sources ---
        with Cluster(
            "Data Sources  ·  4 Domain APIs",
            graph_attr={
                "bgcolor": "#E8F5E9",
                "style": "rounded",
                "fontsize": "11",
                "fontname": CLUSTER_FONT,
                "pencolor": "#2E7D32",
                "penwidth": "2.0",
            },
        ):
            weather = Server("OpenWeatherMap\nweather · forecasts")
            economic = Server("Alpha Vantage\nmarkets · indices")
            news = Server("News API\nsentiment · trends")
            transport = Server("TomTom Traffic\ncongestion · transit")

        # --- Processing Pipeline ---
        with Cluster(
            "Processing Pipeline  ·  Python",
            graph_attr={
                "bgcolor": "#FFF3E0",
                "style": "rounded",
                "fontsize": "11",
                "fontname": CLUSTER_FONT,
                "pencolor": "#E65100",
                "penwidth": "2.0",
            },
        ):
            connectors = Python("API Connectors\nvalidation · rate limiting")
            cleaning = Python("Data Cleaning\nnormalization · enrichment")
            cache = Redis("Domain Cache\nTTL: 10-60 min")

        # --- Analytics Core ---
        with Cluster(
            "Analytics Core  ·  scikit-learn",
            graph_attr={
                "bgcolor": "#E3F2FD",
                "style": "rounded",
                "fontsize": "11",
                "fontname": CLUSTER_FONT,
                "pencolor": "#1565C0",
                "penwidth": "2.0",
            },
        ):
            correlation = Python("Correlation Engine\nPearson · rolling window")
            prediction = Python("Prediction Engine\ntime-series forecasting")
            nlq = Python("NLQ Processor\nintent · entity extraction")

        # --- Dashboard ---
        with Cluster(
            "Dashboard  ·  Flask + Socket.IO",
            graph_attr={
                "bgcolor": "#F3E5F5",
                "style": "rounded",
                "fontsize": "11",
                "fontname": CLUSTER_FONT,
                "pencolor": "#6A1B9A",
                "penwidth": "2.0",
            },
        ):
            flask_app = Flask("Flask App\nblueprints · templates")
            socketio = Rack("Socket.IO\nreal-time push")
            ui = Client("Dashboard UI\nChart.js · Bootstrap")

        # --- Edges: data sources to processing ---
        weather >> Edge(label="30min TTL", color="#2E7D32", penwidth="1.5") >> connectors
        economic >> Edge(label="60min TTL", color="#2E7D32", penwidth="1.5") >> connectors
        news >> Edge(label="15min TTL", color="#2E7D32", penwidth="1.5") >> connectors
        transport >> Edge(label="10min TTL", color="#2E7D32", penwidth="1.5") >> connectors

        # --- Edges: processing ---
        connectors >> Edge(color="#E65100", penwidth="2.0") >> cleaning
        cleaning >> Edge(color="#E65100", penwidth="1.5") >> cache

        # --- Edges: cache to analytics ---
        cache >> Edge(color="#1565C0", penwidth="2.0") >> correlation
        cache >> Edge(color="#1565C0", penwidth="2.0") >> prediction
        cache >> Edge(color="#1565C0", penwidth="1.5") >> nlq

        # --- Edges: analytics to dashboard ---
        correlation >> Edge(color="#6A1B9A", penwidth="2.0") >> flask_app
        prediction >> Edge(color="#6A1B9A", penwidth="2.0") >> flask_app
        nlq >> Edge(color="#6A1B9A", penwidth="1.5") >> flask_app
        flask_app >> Edge(color="#6A1B9A", penwidth="1.5") >> socketio
        socketio >> Edge(label="WebSocket", color="#6A1B9A", penwidth="2.0") >> ui


def data_flow_diagram():
    """Data flow showing fallback strategy."""
    with Diagram(
        "",
        filename=os.path.join(OUTPUT_DIR, "data-flow"),
        outformat="png",
        show=False,
        direction="LR",
        graph_attr={
            "fontsize": "11",
            "fontname": FONT,
            "bgcolor": "#ffffff",
            "pad": "0.6",
            "nodesep": "0.7",
            "ranksep": "0.9",
            "dpi": "150",
        },
        node_attr={"fontsize": "10", "fontname": FONT},
        edge_attr={"fontsize": "8", "fontname": FONT, "color": "#666666"},
    ):
        # API layer
        with Cluster(
            "External APIs",
            graph_attr={
                "bgcolor": "#E8F5E9",
                "style": "rounded",
                "fontsize": "10",
                "fontname": CLUSTER_FONT,
                "pencolor": "#2E7D32",
                "penwidth": "2.0",
            },
        ):
            api = Server("Domain APIs\nweather · economic\nnews · transport")

        # Processing
        connectors = Python("API Connectors\nvalidate · transform")
        cache = Redis("Server Cache\nTTL per domain")

        # Analytics
        with Cluster(
            "Analytics",
            graph_attr={
                "bgcolor": "#E3F2FD",
                "style": "rounded",
                "fontsize": "10",
                "fontname": CLUSTER_FONT,
                "pencolor": "#1565C0",
                "penwidth": "2.0",
            },
        ):
            corr = Python("Cross-Domain\nCorrelation")
            pred = Python("Predictive\nModels")

        # Dashboard
        dashboard = Client("Dashboard\nreal-time updates")

        # Fallback
        demo = SQL("Demo Data\ngenerated patterns")

        # --- Happy path ---
        api >> Edge(label="live data", color="#2E7D32", penwidth="2.5") >> connectors
        connectors >> Edge(color="#E65100", penwidth="2.0") >> cache
        cache >> Edge(color="#1565C0", penwidth="2.0") >> corr
        cache >> Edge(color="#1565C0", penwidth="2.0") >> pred
        corr >> Edge(color="#6A1B9A", penwidth="2.0") >> dashboard
        pred >> Edge(color="#6A1B9A", penwidth="2.0") >> dashboard

        # --- Fallback path ---
        api >> Edge(label="API failure", color="#C62828", style="dashed") >> demo
        demo >> Edge(label="fallback", color="#999999", style="dashed") >> cache


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating architecture diagram...")
    architecture_diagram()
    print("Generating data flow diagram...")
    data_flow_diagram()
    print(f"Done. Images in {OUTPUT_DIR}/")
