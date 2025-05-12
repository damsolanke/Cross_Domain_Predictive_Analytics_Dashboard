from flask import jsonify, request, send_file
from . import visualization_bp, visualization
import pandas as pd
import json
import io
import csv
import numpy as np

@visualization_bp.route('/correlation-matrix', methods=['POST'])
def correlation_matrix():
    """Generate correlation matrix visualization from provided data"""
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        return jsonify({
            'success': True,
            'visualization': visualization.create_correlation_matrix(df)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@visualization_bp.route('/prediction-plot', methods=['POST'])
def prediction_plot():
    """Generate prediction vs actual plot with confidence intervals"""
    try:
        data = request.get_json()
        actual_data = pd.Series(data['actual'])
        predicted_data = pd.Series(data['predicted'])
        confidence_intervals = data.get('confidence_intervals')
        
        return jsonify({
            'success': True,
            'visualization': visualization.create_prediction_plot(
                actual_data,
                predicted_data,
                confidence_intervals
            )
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@visualization_bp.route('/scatter-matrix', methods=['POST'])
def scatter_matrix():
    """Generate scatter matrix visualization for cross-domain relationships"""
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        return jsonify({
            'success': True,
            'visualization': visualization.create_scatter_matrix(df)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@visualization_bp.route('/confidence-visualization', methods=['POST'])
def confidence_visualization():
    """Generate confidence visualization for predictions"""
    try:
        data = request.get_json()
        predictions = pd.Series(data['predictions'])
        confidence_scores = pd.Series(data['confidence_scores'])
        
        return jsonify({
            'success': True,
            'visualization': visualization.create_confidence_visualization(
                predictions,
                confidence_scores
            )
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@visualization_bp.route('/time-series-decomposition', methods=['POST'])
def time_series_decomposition():
    """Generate time series decomposition visualization"""
    try:
        data = request.get_json()
        series = pd.Series(data['values'], index=pd.to_datetime(data['index']))
        period = data.get('period', 12)
        
        return jsonify({
            'success': True,
            'visualization': visualization.create_time_series_decomposition(series, period)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@visualization_bp.route('/feature-importance', methods=['POST'])
def feature_importance():
    """Generate feature importance visualization"""
    try:
        data = request.get_json()
        feature_names = data['feature_names']
        importance_scores = np.array(data['importance_scores'])
        
        return jsonify({
            'success': True,
            'visualization': visualization.create_feature_importance(feature_names, importance_scores)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@visualization_bp.route('/anomaly-detection', methods=['POST'])
def anomaly_detection():
    """Generate anomaly detection visualization"""
    try:
        data = request.get_json()
        series = pd.Series(data['values'], index=pd.to_datetime(data['index']))
        contamination = data.get('contamination', 0.1)
        
        return jsonify({
            'success': True,
            'visualization': visualization.create_anomaly_detection(series, contamination)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@visualization_bp.route('/comparison-view', methods=['POST'])
def comparison_view():
    """Generate comparison view visualization"""
    try:
        data = request.get_json()
        datasets = {
            name: pd.Series(d['values'], index=pd.to_datetime(d['index']))
            for name, d in data['datasets'].items()
        }
        
        return jsonify({
            'success': True,
            'visualization': visualization.create_comparison_view(datasets)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# Export routes
@visualization_bp.route('/export/<format>', methods=['POST'])
def export_data(format):
    """Export visualization data in various formats"""
    try:
        data = request.get_json()
        df = pd.DataFrame(data['data'])
        
        if format == 'csv':
            output = io.StringIO()
            df.to_csv(output, index=True)
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name='visualization_data.csv'
            )
        elif format == 'json':
            return jsonify({
                'success': True,
                'data': df.to_dict(orient='records')
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Unsupported format: {format}'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@visualization_bp.route('/batch-export', methods=['POST'])
def batch_export():
    """Export multiple visualizations in a single request"""
    try:
        data = request.get_json()
        format = data.get('format', 'csv')
        visualizations = data['visualizations']
        
        if format == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(['Visualization', 'Timestamp', 'Data'])
            
            # Write data
            for viz_name, viz_data in visualizations.items():
                df = pd.DataFrame(viz_data)
                writer.writerow([viz_name, pd.Timestamp.now(), df.to_json()])
            
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name='batch_export.csv'
            )
        else:
            return jsonify({
                'success': False,
                'error': f'Unsupported format: {format}'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400 