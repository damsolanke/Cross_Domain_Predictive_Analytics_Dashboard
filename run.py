#!/usr/bin/env python3
"""
Run script for the Cross-Domain Predictive Analytics Dashboard.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    from app import create_app, socketio

    print("Starting Cross-Domain Predictive Analytics Dashboard...")
    print("Server running at http://localhost:5000")

    app = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
