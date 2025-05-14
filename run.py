#!/usr/bin/env python3
"""
Run script for the Cross-Domain Predictive Analytics Dashboard
"""
import sys
import os
from flask import Flask

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    print("Starting Cross-Domain Predictive Analytics Dashboard...")
    print("Server running at http://localhost:5002")
    
    # Create a simple Flask app without using the module-level app
    flask_app = Flask(__name__, 
                      template_folder="app/templates",
                      static_folder="app/static")
    
    # Configure the application
    flask_app.config['SECRET_KEY'] = 'REDACTED'
    flask_app.config['DEBUG'] = False
    
    # Register blueprints
    from app.main.routes import main
    flask_app.register_blueprint(main)
    
    # Register Natural Language Query blueprints
    from app.nlq.routes import nlq_routes
    flask_app.register_blueprint(nlq_routes)
    
    from app.nlq.api import nlq_blueprint
    flask_app.register_blueprint(nlq_blueprint)
    
    # Register System Integration blueprint
    from app.system_integration import system_integration
    flask_app.register_blueprint(system_integration, url_prefix='/system')
    
    # Run the application
    flask_app.run(host='0.0.0.0', port=5002, debug=False)