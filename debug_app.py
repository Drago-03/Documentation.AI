#!/usr/bin/env python3
"""
Simplified Flask app to test error handling improvements
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app, origins=["http://localhost:3000", "http://localhost:5000"])

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('debug.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

@app.before_request
def log_request_info():
    """Log detailed request information"""
    logger.info(f"🔍 Request: {request.method} {request.url}")
    logger.info(f"📋 Headers: {dict(request.headers)}")
    if request.is_json:
        logger.info(f"📄 JSON Data: {request.get_json(silent=True)}")
    if request.form:
        logger.info(f"📝 Form Data: {dict(request.form)}")
    if request.args:
        logger.info(f"🔗 Query Args: {dict(request.args)}")

@app.after_request
def log_response_info(response):
    """Log response information"""
    logger.info(f"📤 Response Status: {response.status_code}")
    return response

@app.errorhandler(Exception)
def handle_all_exceptions(error):
    """Handle all unhandled exceptions with maximum detail"""
    error_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    
    # Log everything we can about the error
    logger.error(f"🚨 CRITICAL ERROR [{error_id}]")
    logger.error(f"🔥 Exception Type: {type(error).__name__}")
    logger.error(f"💥 Exception Message: {str(error)}")
    logger.error(f"🌐 Request URL: {request.url}")
    logger.error(f"📡 Request Method: {request.method}")
    logger.error(f"🏷️ Request Endpoint: {request.endpoint}")
    logger.error(f"📋 Request Headers: {dict(request.headers)}")
    if request.is_json:
        logger.error(f"📄 Request JSON: {request.get_json(silent=True)}")
    if request.form:
        logger.error(f"📝 Request Form: {dict(request.form)}")
    if request.args:
        logger.error(f"🔗 Request Args: {dict(request.args)}")
    logger.error(f"📚 Full Traceback:\\n{traceback.format_exc()}")
    
    # Return comprehensive error response
    error_response = {
        'error': 'Internal server error',
        'error_id': error_id,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'timestamp': datetime.utcnow().isoformat(),
        'request_info': {
            'url': request.url,
            'method': request.method,
            'endpoint': request.endpoint,
            'headers': dict(request.headers),
            'json_data': request.get_json(silent=True) if request.is_json else None,
            'form_data': dict(request.form) if request.form else None,
            'query_args': dict(request.args) if request.args else None
        },
        'debug_info': {
            'traceback': traceback.format_exc().split('\\n'),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'flask_version': 'unknown'
        }
    }
    
    return jsonify(error_response), 500

@app.route('/')
def index():
    """Home route with debug info"""
    return jsonify({
        'message': 'Documentation.AI Debug Server',
        'status': 'running',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'home': '/',
            'health': '/api/health',
            'debug': '/api/debug',
            'test_error': '/api/test-error'
        }
    })

@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests"""
    logger.info("📄 Favicon requested")
    return '', 204

@app.route('/api/health')
def health_check():
    """Comprehensive health check"""
    try:
        logger.info("🏥 Health check requested")
        
        # Environment check
        env_vars = {
            'GITHUB_TOKEN': '✅ Set' if os.getenv('GITHUB_TOKEN') else '❌ Missing',
            'GEMINI_API_KEY': '✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Missing',
            'SECRET_KEY': '✅ Set' if os.getenv('SECRET_KEY') else '❌ Using default'
        }
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': 'debug-1.0.0',
            'environment': env_vars,
            'system_info': {
                'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                'cwd': os.getcwd(),
                'debug_mode': app.debug
            }
        })
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'traceback': traceback.format_exc().split('\\n')
        }), 500

@app.route('/api/debug')
def debug_info():
    """Debug endpoint with detailed system information"""
    try:
        logger.info("🔧 Debug info requested")
        
        import sys
        import platform
        
        return jsonify({
            'debug_info': {
                'timestamp': datetime.utcnow().isoformat(),
                'python': {
                    'version': sys.version,
                    'executable': sys.executable,
                    'path': sys.path[:5]  # First 5 paths only
                },
                'platform': {
                    'system': platform.system(),
                    'release': platform.release(),
                    'machine': platform.machine()
                },
                'flask': {
                    'debug_mode': app.debug,
                    'testing': app.testing,
                    'secret_key_set': bool(app.secret_key)
                },
                'environment': dict(os.environ)  # This might be sensitive, be careful
            }
        })
    except Exception as e:
        logger.error(f"❌ Debug info failed: {e}")
        raise  # Let the global error handler catch this

@app.route('/api/test-error')
def test_error():
    """Endpoint to test error handling"""
    logger.info("💥 Test error requested")
    error_type = request.args.get('type', 'generic')
    
    if error_type == 'value':
        raise ValueError("This is a test ValueError")
    elif error_type == 'key':
        raise KeyError("This is a test KeyError")
    elif error_type == 'type':
        raise TypeError("This is a test TypeError")
    elif error_type == 'import':
        # This will raise ImportError
        exec("import non_existent_module")
    else:
        raise Exception("This is a generic test exception")
    
    return jsonify({'message': 'This should not be reached'})

@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    """Test analyze endpoint to replicate the 500 error"""
    try:
        logger.info("🔍 Analyze endpoint called")
        
        # Validate request
        if not request.is_json:
            logger.error("❌ Request is not JSON")
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        logger.info(f"📄 Request data: {data}")
        
        repo_url = data.get('repo_url', '').strip()
        
        if not repo_url:
            logger.error("❌ Repository URL is missing")
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Simulate the error that's happening
        logger.info("🚨 Simulating the actual error...")
        raise Exception("AI models not available - import failed during initialization")
        
    except Exception as e:
        logger.error(f"💥 Analyze failed: {e}")
        logger.error(traceback.format_exc())
        raise  # Let the global error handler catch this

if __name__ == '__main__':
    logger.info("🚀 Starting Documentation.AI Debug Server")
    logger.info(f"📍 Debug mode: {app.debug}")
    logger.info(f"📊 Current working directory: {os.getcwd()}")
    
    # Test imports at startup
    logger.info("🧪 Testing imports at startup...")
    try:
        import flask
        logger.info(f"✅ Flask imported successfully")
    except Exception as e:
        logger.error(f"❌ Flask import failed: {e}")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
