#!/usr/bin/env python3
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import and run the Flask app directly
if __name__ == '__main__':
    print("Starting Cross-Domain Predictive Analytics Dashboard...")
    print("Server running at http://localhost:5000")
    
    # Use the proper app creation function from app/__init__.py
    from app import create_app, socketio
    
    flask_app = create_app()
    
    # Run Flask's development server with SocketIO
    socketio.run(flask_app, host='0.0.0.0', port=5000, debug=False)