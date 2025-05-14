"""
API endpoints for advanced analytics and predictive capabilities.
"""

from flask import Blueprint, jsonify, request, render_template, send_file
from app.system_integration.cross_domain_correlation import CrossDomainCorrelator
from app.system_integration.cross_domain_prediction import CrossDomainPredictor
from app.system_integration.report_generator import ReportGenerator
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
advanced_analytics = Blueprint('advanced_analytics', __name__, url_prefix='/api/analytics')

# Global objects
correlator = CrossDomainCorrelator()
predictor = CrossDomainPredictor(correlator=correlator)
report_generator = ReportGenerator()

@advanced_analytics.route('/correlations')
def get_correlations():
    """Get current correlation data."""
    try:
        # Calculate correlations
        correlator.calculate_correlations()
        
        # Get correlation data for visualization
        correlation_data = correlator.get_correlation_data_for_visualization()
        
        return jsonify(correlation_data)
    
    except Exception as e:
        logger.error(f"Error getting correlations: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/insights')
def get_insights():
    """Get correlation insights."""
    try:
        # Generate insights
        insights = correlator.generate_insights()
        
        # Get query parameters for filtering
        domain = request.args.get('domain')
        strength = request.args.get('min_strength')
        limit = request.args.get('limit', 100, type=int)
        
        # Apply filters
        filtered_insights = insights
        
        if domain:
            filtered_insights = [
                i for i in filtered_insights 
                if (i.get('domain1') == domain or i.get('domain2') == domain)
            ]
        
        if strength:
            try:
                min_strength = float(strength)
                filtered_insights = [
                    i for i in filtered_insights 
                    if abs(i.get('correlation_value', 0)) >= min_strength
                ]
            except ValueError:
                pass
        
        # Limit results
        filtered_insights = filtered_insights[:limit]
        
        return jsonify(filtered_insights)
    
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/anomalies')
def get_anomalies():
    """Get correlation anomalies."""
    try:
        # Detect anomalies
        anomalies = correlator.detect_anomalies()
        
        return jsonify(anomalies)
    
    except Exception as e:
        logger.error(f"Error getting anomalies: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/prediction/models', methods=['GET'])
def get_prediction_models():
    """Get all prediction models."""
    try:
        # Get model info
        models = predictor.get_model_info()
        
        return jsonify(models)
    
    except Exception as e:
        logger.error(f"Error getting prediction models: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/prediction/models/<model_name>', methods=['GET'])
def get_prediction_model(model_name):
    """Get information about a specific prediction model."""
    try:
        # Get model info
        model_info = predictor.get_model_info(model_name)
        
        if 'error' in model_info:
            return jsonify(model_info), 404
        
        return jsonify(model_info)
    
    except Exception as e:
        logger.error(f"Error getting prediction model {model_name}: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/prediction/models', methods=['POST'])
def create_prediction_model():
    """Create a new prediction model."""
    try:
        # Get request data
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Required parameters
        target_domain = data.get('target_domain')
        target_variable = data.get('target_variable')
        
        if not target_domain or not target_variable:
            return jsonify({'error': 'Target domain and variable are required'}), 400
        
        # Optional parameters
        model_type = data.get('model_type', 'linear')
        model_params = data.get('model_params', {})
        feature_domains = data.get('feature_domains')
        lookback_days = data.get('lookback_days', 30)
        
        # Create model
        result = predictor.create_prediction_model(
            target_domain=target_domain,
            target_variable=target_variable,
            model_type=model_type,
            model_params=model_params,
            feature_domains=feature_domains,
            lookback_days=lookback_days
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
    
    except Exception as e:
        logger.error(f"Error creating prediction model: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/prediction/models/<model_name>', methods=['DELETE'])
def delete_prediction_model(model_name):
    """Delete a prediction model."""
    try:
        # Delete model
        result = predictor.delete_model(model_name)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error deleting prediction model {model_name}: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/prediction/predict/<model_name>', methods=['GET', 'POST'])
def make_prediction(model_name):
    """Make a prediction using a model."""
    try:
        # Get input data if provided
        input_data = None
        if request.method == 'POST':
            input_data = request.json
        
        # Make prediction
        prediction = predictor.predict(model_name, input_data)
        
        if 'error' in prediction:
            return jsonify(prediction), 400
        
        return jsonify(prediction)
    
    except Exception as e:
        logger.error(f"Error making prediction with model {model_name}: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/prediction/features/<model_name>', methods=['GET'])
def get_important_features(model_name):
    """Get important features for a model."""
    try:
        # Get number of features to return
        top_n = request.args.get('top_n', 10, type=int)
        
        # Get features
        features = predictor.get_important_features(model_name, top_n)
        
        if 'error' in features:
            return jsonify(features), 404
        
        return jsonify(features)
    
    except Exception as e:
        logger.error(f"Error getting features for model {model_name}: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/prediction/domain/<domain>', methods=['GET'])
def predict_domain(domain):
    """Make predictions for all variables in a domain."""
    try:
        # Get optional variable filter
        variable = request.args.get('variable')
        
        # Make predictions
        predictions = predictor.predict_domain(domain, variable)
        
        return jsonify(predictions)
    
    except Exception as e:
        logger.error(f"Error predicting for domain {domain}: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/prediction/history', methods=['GET'])
def get_prediction_history():
    """Get prediction history."""
    try:
        # Get number of predictions to return
        limit = request.args.get('limit', 10, type=int)
        
        # Get history
        history = predictor.get_prediction_history(limit)
        
        return jsonify(history)
    
    except Exception as e:
        logger.error(f"Error getting prediction history: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/reports/correlation', methods=['GET'])
def generate_correlation_report():
    """Generate a correlation report."""
    try:
        # Get format type
        format_type = request.args.get('format', 'html')
        if format_type not in ['html', 'md', 'json']:
            return jsonify({'error': f'Unsupported format: {format_type}'}), 400
        
        # Get date range
        days = request.args.get('days', 7, type=int)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Calculate correlations
        correlator.calculate_correlations()
        
        # Get correlation data and insights
        correlation_data = correlator.get_correlation_data_for_visualization()
        insights = correlator.generate_insights()
        
        # Get predictions if available
        predictions = predictor.get_prediction_history(limit=100)
        
        # Generate report
        report = report_generator.generate_correlation_report(
            correlations=correlation_data,
            insights=insights,
            predictions=predictions,
            start_date=start_date,
            end_date=end_date,
            format_type=format_type
        )
        
        # Save report if not JSON
        if format_type != 'json':
            file_path = report_generator.save_report(
                report_content=report,
                report_name='correlation_report',
                format_type=format_type
            )
            
            # If HTML, return it directly
            if format_type == 'html':
                return report
        
        # Return JSON or Markdown as response
        if format_type == 'json':
            return jsonify(json.loads(report))
        
        return report, 200, {'Content-Type': 'text/markdown'}
    
    except Exception as e:
        logger.error(f"Error generating correlation report: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/reports/insights', methods=['GET'])
def generate_insight_report():
    """Generate an insight report."""
    try:
        # Get format type
        format_type = request.args.get('format', 'html')
        if format_type not in ['html', 'md', 'json']:
            return jsonify({'error': f'Unsupported format: {format_type}'}), 400
        
        # Get optional domain filter
        domain = request.args.get('domain')
        
        # Get date range
        days = request.args.get('days', 7, type=int)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get insights
        insights = correlator.generate_insights()
        
        # Generate report
        report = report_generator.generate_insight_report(
            insights=insights,
            domain=domain,
            start_date=start_date,
            end_date=end_date,
            format_type=format_type
        )
        
        # Save report if not JSON
        if format_type != 'json':
            file_path = report_generator.save_report(
                report_content=report,
                report_name=f"{''+domain+'_' if domain else ''}insight_report",
                format_type=format_type
            )
            
            # If HTML, return it directly
            if format_type == 'html':
                return report
        
        # Return JSON or Markdown as response
        if format_type == 'json':
            return jsonify(json.loads(report))
        
        return report, 200, {'Content-Type': 'text/markdown'}
    
    except Exception as e:
        logger.error(f"Error generating insight report: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/reports/prediction', methods=['GET'])
def generate_prediction_report():
    """Generate a prediction report."""
    try:
        # Get format type
        format_type = request.args.get('format', 'html')
        if format_type not in ['html', 'md', 'json']:
            return jsonify({'error': f'Unsupported format: {format_type}'}), 400
        
        # Get date range
        days = request.args.get('days', 7, type=int)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get predictions
        predictions = predictor.get_prediction_history(limit=100)
        
        # Get correlation data for context
        correlation_data = correlator.get_correlation_data_for_visualization()
        
        # Generate report
        report = report_generator.generate_prediction_report(
            predictions=predictions,
            correlations=correlation_data,
            start_date=start_date,
            end_date=end_date,
            format_type=format_type
        )
        
        # Save report if not JSON
        if format_type != 'json':
            file_path = report_generator.save_report(
                report_content=report,
                report_name='prediction_report',
                format_type=format_type
            )
            
            # If HTML, return it directly
            if format_type == 'html':
                return report
        
        # Return JSON or Markdown as response
        if format_type == 'json':
            return jsonify(json.loads(report))
        
        return report, 200, {'Content-Type': 'text/markdown'}
    
    except Exception as e:
        logger.error(f"Error generating prediction report: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_analytics.route('/reports/list', methods=['GET'])
def list_reports():
    """List available reports."""
    try:
        # Get report directory
        report_dir = report_generator.output_dir
        
        # List reports
        reports = []
        for file_path in Path(report_dir).glob('*.*'):
            # Get report info
            name = file_path.stem
            format_type = file_path.suffix[1:]  # Remove the dot
            created = datetime.fromtimestamp(file_path.stat().st_mtime)
            size = file_path.stat().st_size
            
            reports.append({
                'name': name,
                'format': format_type,
                'created': created.isoformat(),
                'size': size,
                'path': str(file_path)
            })
        
        # Sort by creation date (newest first)
        reports.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify(reports)
    
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        return jsonify({'error': str(e)}), 500