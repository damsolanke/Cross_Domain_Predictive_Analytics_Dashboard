#!/usr/bin/env python3
"""
Setup script for Cross-Domain Predictive Analytics Dashboard

This script ensures all necessary directories are created for the application.
"""

import os

# Essential directories
DIRECTORIES = [
    'app/api/connectors',
    'app/demo',
    'app/docs',
    'app/main',
    'app/models',
    'app/nlq/static/css',
    'app/nlq/static/js',
    'app/nlq/templates/components',
    'app/static/css',
    'app/static/js',
    'app/static/nlq/css',
    'app/static/nlq/js',
    'app/system_integration',
    'app/templates/analytics',
    'app/templates/components',
    'app/templates/demo',
    'app/templates/documentation',
    'app/templates/nlq/components',
    'app/templates/reports',
    'app/templates/system_integration',
    'app/tests',
    'app/visualizations',
    'docs',
    'tests',
    'documentation/screenshots',
]

def ensure_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def main():
    """Create all necessary directories."""
    print("Setting up directories for Cross-Domain Predictive Analytics Dashboard...")
    
    for directory in DIRECTORIES:
        ensure_directory(directory)
    
    print("\nDirectory setup complete!")
    print("You can now run the application using 'python run.py'")

if __name__ == "__main__":
    main() 