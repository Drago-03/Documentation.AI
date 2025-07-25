#!/usr/bin/env python3
"""
Quick test to verify the backend starts without errors
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("🔍 Testing backend startup...")

try:
    # Test basic imports
    print("📦 Testing imports...")
    from flask import Flask
    print("  ✅ Flask imported")
    
    from flask_cors import CORS
    print("  ✅ Flask-CORS imported")
    
    from flask_sqlalchemy import SQLAlchemy
    print("  ✅ Flask-SQLAlchemy imported")
    
    # Test environment loading
    print("📝 Testing environment...")
    from dotenv import load_dotenv
    load_dotenv()
    
    port = os.getenv('PORT', '5000')
    print(f"  ✅ PORT configured: {port}")
    
    # Test AI model imports (they might fail, but shouldn't crash)
    print("🤖 Testing AI model imports...")
    try:
        from ai_models.github_analyzer import GitHubAnalyzer
        print("  ✅ GitHubAnalyzer imported")
    except Exception as e:
        print(f"  ⚠️ GitHubAnalyzer import warning: {e}")
    
    try:
        from ai_models.documentation_generator import DocumentationGenerator  
        print("  ✅ DocumentationGenerator imported")
    except Exception as e:
        print(f"  ⚠️ DocumentationGenerator import warning: {e}")
    
    try:
        from ai_models.rag_pipeline import RAGPipeline
        print("  ✅ RAGPipeline imported")
    except Exception as e:
        print(f"  ⚠️ RAGPipeline import warning: {e}")
    
    # Test app creation (without running)
    print("🚀 Testing app creation...")
    from app import app, db
    print("  ✅ App created successfully")
    
    with app.app_context():
        try:
            db.create_all()
            print("  ✅ Database initialized")
        except Exception as e:
            print(f"  ⚠️ Database warning: {e}")
    
    print(f"\n✨ Backend test completed successfully!")
    print(f"🌐 Backend should start on: http://localhost:{port}")
    print(f"🔗 Frontend proxy should point to: http://localhost:{port}")
    
except Exception as e:
    print(f"\n❌ Backend test failed: {e}")
    import traceback
    print(f"📚 Full traceback:\n{traceback.format_exc()}")
    sys.exit(1)
