#!/usr/bin/env python3
import sys
import os

# Add current directory to path so we can import app module correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the Flask application factory function
from app import create_app, socketio

# Create the Flask application INSTANCE (not a module)
flask_app = create_app()  # This should return an actual Flask app instance

# Run the application
if __name__ == '__main__':
    print("Starting Cross-Domain Predictive Analytics Dashboard...")
    # Run socketio 
    socketio.run(flask_app, host='0.0.0.0', port=5000)