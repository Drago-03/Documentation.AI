#!/usr/bin/env python3
"""Test script to check if all imports work correctly"""

print("Testing imports...")

try:
    import os
    print("✅ os imported")
    
    import logging
    print("✅ logging imported")
    
    from flask import Flask, request, jsonify, send_from_directory
    print("✅ Flask imported")
    
    from flask_cors import CORS
    print("✅ Flask-CORS imported")
    
    from flask_sqlalchemy import SQLAlchemy
    print("✅ Flask-SQLAlchemy imported")
    
    from dotenv import load_dotenv
    print("✅ python-dotenv imported")
    
    # Load environment variables
    load_dotenv()
    print("✅ Environment variables loaded")
    
    # Import our modules
    from ai_models.github_analyzer import GitHubAnalyzer
    print("✅ GitHubAnalyzer imported")
    
    from ai_models.documentation_generator import DocumentationGenerator
    print("✅ DocumentationGenerator imported")
    
    from ai_models.rag_pipeline import RAGPipeline
    print("✅ RAGPipeline imported")
    
    from database.models import db, AnalysisJob
    print("✅ Database models imported")
    
    from utils.file_processor import FileProcessor
    print("✅ FileProcessor imported")
    
    print("🎉 All imports successful!")
    
    # Test Flask app creation
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    CORS(app)
    db.init_app(app)
    
    print("🎉 Flask app created successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
