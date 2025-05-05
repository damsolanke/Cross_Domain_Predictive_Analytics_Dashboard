from flask import Flask
from flask_socketio import SocketIO

# Initialize SocketIO without an app (will be attached in create_app)
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = 'REDACTED'
    
    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.system_integration import system_integration as system_integration_blueprint
    app.register_blueprint(system_integration_blueprint, url_prefix='/system')
    
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    from app.demo.correlation_demo import correlation_demo as correlation_demo_blueprint
    app.register_blueprint(correlation_demo_blueprint)
    
    # Register Natural Language Query blueprint
    from app.api.natural_language_query import nlq_api
    app.register_blueprint(nlq_api)
    
    # Initialize extensions with app
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Initialize system integration
    with app.app_context():
        from app.system_integration.integration import init_system_integration
        init_system_integration(app)
    
    return app