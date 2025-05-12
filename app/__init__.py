from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Import and register blueprints
from .visualizations import visualization_bp
app.register_blueprint(visualization_bp, url_prefix='/visualization')

# Import routes
from . import main

def create_app():
    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app 