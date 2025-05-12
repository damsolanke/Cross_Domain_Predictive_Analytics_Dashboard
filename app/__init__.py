from flask import Flask
from flask_socketio import SocketIO
import os

# Initialize SocketIO without an app (will be attached in create_app)
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = 'REDACTED'
    app.config['TESTING'] = os.environ.get('TESTING', 'False') == 'True'
    
    # Initialize extensions with app
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Initialize system integration first to avoid circular imports
    with app.app_context():
        # First, initialize events system
        # In a real implementation, this could set up Socket.IO events
        pass
        
        # Then initialize system integration
        from app.system_integration.integration import init_system_integration
        init_system_integration(app)
    
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