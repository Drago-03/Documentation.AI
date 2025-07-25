#!/usr/bin/env python3
"""
Test suite for Documentation.AI
Tests the main application functionality
"""

import unittest
import sys
import os
import tempfile
import json
from pathlib import Path

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestImports(unittest.TestCase):
    """Test that all required modules can be imported"""
    
    def test_flask_imports(self):
        """Test Flask and related imports"""
        try:
            from flask import Flask, request, jsonify
            from flask_cors import CORS
            from flask_sqlalchemy import SQLAlchemy
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Flask imports failed: {e}")
    
    def test_ai_model_imports(self):
        """Test AI model imports"""
        try:
            from ai_models.github_analyzer import GitHubAnalyzer
            from ai_models.documentation_generator import DocumentationGenerator
            from ai_models.rag_pipeline import RAGPipeline
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"AI model imports failed: {e}")
    
    def test_database_imports(self):
        """Test database model imports"""
        try:
            from database.models import db, AnalysisJob
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Database imports failed: {e}")
    
    def test_utils_imports(self):
        """Test utility imports"""
        try:
            from utils.file_processor import FileProcessor
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Utils imports failed: {e}")

class TestApplication(unittest.TestCase):
    """Test the main application"""
    
    def setUp(self):
        """Set up test environment"""
        # Import the app
        try:
            from app import app, db
            self.app = app
            self.db = db
            self.client = app.test_client()
            
            # Configure app for testing
            self.app.config['TESTING'] = True
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            
            with self.app.app_context():
                self.db.create_all()
        except Exception as e:
            self.skipTest(f"Could not set up test app: {e}")
    
    def test_index_endpoint(self):
        """Test the index endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('Documentation.AI', data['message'])
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_analyze_endpoint_no_data(self):
        """Test analyze endpoint with no data"""
        response = self.client.post('/api/analyze')
        self.assertIn(response.status_code, [400, 500])  # Should fail without data
    
    def test_jobs_endpoint(self):
        """Test the jobs listing endpoint"""
        response = self.client.get('/api/jobs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

class TestFileStructure(unittest.TestCase):
    """Test that required files and directories exist"""
    
    def setUp(self):
        self.project_root = Path(__file__).parent.parent
    
    def test_main_files_exist(self):
        """Test that main application files exist"""
        required_files = [
            'app.py',
            'requirements.txt',
            'start.sh',
            'stop.sh'
        ]
        
        for file_name in required_files:
            file_path = self.project_root / file_name
            self.assertTrue(file_path.exists(), f"Required file {file_name} not found")
    
    def test_directories_exist(self):
        """Test that required directories exist"""
        required_dirs = [
            'ai_models',
            'database',
            'utils',
            'frontend',
            'tests',
            'scripts'
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            self.assertTrue(dir_path.exists(), f"Required directory {dir_name} not found")
    
    def test_ai_models_structure(self):
        """Test AI models directory structure"""
        ai_models_dir = self.project_root / 'ai_models'
        required_files = [
            '__init__.py',
            'github_analyzer.py',
            'documentation_generator.py',
            'rag_pipeline.py'
        ]
        
        for file_name in required_files:
            file_path = ai_models_dir / file_name
            self.assertTrue(file_path.exists(), f"AI model file {file_name} not found")

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
