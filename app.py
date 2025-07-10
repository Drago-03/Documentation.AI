import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import traceback

# Import our modules
from ai_models.github_analyzer import GitHubAnalyzer
from ai_models.documentation_generator import DocumentationGenerator
from ai_models.rag_pipeline import RAGPipeline
from database.models import db, AnalysisJob
from utils.file_processor import FileProcessor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///documentation_ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app)
db.init_app(app)

# Initialize AI components
github_analyzer = GitHubAnalyzer()
doc_generator = DocumentationGenerator()
rag_pipeline = RAGPipeline()
file_processor = FileProcessor()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Documentation.AI API Server',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    """Analyze a GitHub repository and generate documentation"""
    try:
        data = request.get_json()
        repo_url = data.get('repo_url')
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Validate GitHub URL
        if 'github.com' not in repo_url:
            return jsonify({'error': 'Please provide a valid GitHub repository URL'}), 400
        
        # Create analysis job
        job = AnalysisJob(repo_url=repo_url, status='processing')
        db.session.add(job)
        db.session.commit()
        
        logger.info(f"Starting analysis for repository: {repo_url}")
        
        # Step 1: Analyze repository structure and code
        analysis_result = github_analyzer.analyze_repository(repo_url)
        
        # Step 2: Process files with RAG pipeline
        rag_result = rag_pipeline.process_repository(analysis_result)
        
        # Step 3: Generate documentation
        documentation = doc_generator.generate_documentation(analysis_result, rag_result)
        
        # Update job status
        job.status = 'completed'
        job.result = documentation
        db.session.commit()
        
        return jsonify({
            'job_id': job.id,
            'status': 'completed',
            'documentation': documentation
        })
        
    except Exception as e:
        logger.error(f"Error analyzing repository: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/job/<int:job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get the status of an analysis job"""
    job = AnalysisJob.query.get_or_404(job_id)
    return jsonify({
        'job_id': job.id,
        'repo_url': job.repo_url,
        'status': job.status,
        'created_at': job.created_at.isoformat(),
        'result': job.result
    })

@app.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    """Get all analysis jobs"""
    jobs = AnalysisJob.query.order_by(AnalysisJob.created_at.desc()).all()
    return jsonify([{
        'job_id': job.id,
        'repo_url': job.repo_url,
        'status': job.status,
        'created_at': job.created_at.isoformat()
    } for job in jobs])

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_models': {
            'gemini': github_analyzer.check_api_health(),
            'rag_pipeline': rag_pipeline.check_health(),
            'doc_generator': doc_generator.check_health()
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
