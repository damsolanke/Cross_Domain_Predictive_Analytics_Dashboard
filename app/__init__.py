from flask import Flask
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize SocketIO without an app (will be attached in create_app)
# Set logger to False and engineio_logger to False to avoid debug-related issues
socketio = SocketIO(logger=False, engineio_logger=False)

def create_app():
    app = Flask(__name__)

    # Configure the app
    import secrets
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    app.config['TESTING'] = os.environ.get('TESTING', 'False') == 'True'
    app.config['DEBUG'] = False  # Explicitly set debug to False

    # Set up API keys for external services
    app.config['API_KEYS'] = {
        # Weather API (OpenWeatherMap)
        'OPENWEATHER_API_KEY': os.environ.get('WEATHER_API_KEY', 'demo_key'),

        # Economic data API (Alpha Vantage)
        'ECONOMIC_API_KEY': os.environ.get('ECONOMIC_API_KEY', 'demo_key'),

        # Social media / news API (News API)
        'SOCIAL_MEDIA_API_KEY': os.environ.get('SOCIAL_MEDIA_API_KEY', 'demo_key'),

        # Transportation API (TomTom, TransitLand)
        'TRANSPORTATION_API_KEY': os.environ.get('TRANSPORTATION_API_KEY', 'demo_key'),
    }

    # Set default API endpoint settings
    app.config['API_SETTINGS'] = {
        'DEFAULT_CACHE_TTL': 600,  # Default cache time (10 minutes)
        'WEATHER_API_URL': 'https://api.openweathermap.org/data/2.5',
        'ECONOMIC_API_URL': 'https://www.alphavantage.co/query',
        'NEWS_API_URL': 'https://newsapi.org/v2',
        'TRAFFIC_API_URL': 'https://api.tomtom.com/traffic/services/4',
        'TRANSIT_API_URL': 'https://transit.land/api/v2'
    }

    # Initialize extensions with app
    socketio.init_app(app, cors_allowed_origins="*")

    # Initialize system integration first to avoid circular imports
    with app.app_context():
        # First, initialize events system
        # In a real implementation, this could set up Socket.IO events
        pass

        # Then initialize system integration
        from app.system_integration.integration import init_system_integration
        system_integrator = init_system_integration(app)
        
        # Initialize API connectors with real data sources
        try:
            from app.system_integration.api_connectors import init_api_connectors
            init_api_connectors()
            app.logger.info("API connectors initialized successfully.")
        except Exception as e:
            app.logger.warning(f"Failed to initialize API connectors: {e}. Using fallback mock data.")
    
    # Import and register blueprints
    from .visualizations import visualization_bp
    app.register_blueprint(visualization_bp, url_prefix='/visualization')
    
    # Now register other blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.system_integration import system_integration as system_integration_blueprint
    app.register_blueprint(system_integration_blueprint, url_prefix='/system')
    
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Register Natural Language Query blueprints
    from app.nlq.api import nlq_blueprint
    app.register_blueprint(nlq_blueprint)
    
    from app.nlq.routes import nlq_routes
    app.register_blueprint(nlq_routes)
    
    # Register analytics blueprint
    from app.main.analytics_controller import analytics
    app.register_blueprint(analytics)
    
    # Register demo-related blueprints
    try:
        from app.demo.correlation_demo import correlation_demo as correlation_demo_blueprint
        app.register_blueprint(correlation_demo_blueprint)
    except ImportError:
        # This is fine if the demo is not available
        pass
    
    # Import SocketIO event handlers
    import app.system_integration.socket_events
    
    return app