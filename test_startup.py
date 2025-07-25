#!/usr/bin/env python3
"""
Test script to check application startup and identify issues
"""

import sys
import traceback
import os
from pathlib import Path

print("=== Documentation.AI Startup Test ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {Path.cwd()}")
print(f"Python path: {sys.path}")

# Test 1: Import dependencies
print("\n1. Testing imports...")
try:
    import flask
    print(f"  ✓ Flask {flask.__version__}")
except Exception as e:
    print(f"  ✗ Flask import failed: {e}")

try:
    import flask_cors
    print(f"  ✓ Flask-CORS")
except Exception as e:
    print(f"  ✗ Flask-CORS import failed: {e}")

try:
    import flask_sqlalchemy
    print(f"  ✓ Flask-SQLAlchemy")
except Exception as e:
    print(f"  ✗ Flask-SQLAlchemy import failed: {e}")

try:
    import sqlalchemy
    print(f"  ✓ SQLAlchemy {sqlalchemy.__version__}")
except Exception as e:
    print(f"  ✗ SQLAlchemy import failed: {e}")

try:
    import requests
    print(f"  ✓ Requests {requests.__version__}")
except Exception as e:
    print(f"  ✗ Requests import failed: {e}")

# Test 2: Basic app import
print("\n2. Testing app import...")
try:
    sys.path.insert(0, str(Path.cwd()))
    from app import app, db, AnalysisJob
    print("  ✓ App imported successfully")
except Exception as e:
    print(f"  ✗ App import failed: {e}")
    print(f"  Full traceback:\n{traceback.format_exc()}")
    sys.exit(1)

# Test 3: Database initialization
print("\n3. Testing database...")
try:
    with app.app_context():
        db.create_all()
        job_count = AnalysisJob.query.count()
        print(f"  ✓ Database initialized, {job_count} jobs found")
except Exception as e:
    print(f"  ✗ Database test failed: {e}")
    print(f"  Full traceback:\n{traceback.format_exc()}")

# Test 4: Create test job
print("\n4. Testing job creation...")
try:
    with app.app_context():
        test_job = AnalysisJob(
            repo_url="https://github.com/test/repo",
            repo_name="repo",
            repo_owner="test",
            status="pending"
        )
        db.session.add(test_job)
        db.session.commit()
        print(f"  ✓ Test job created with ID: {test_job.id}")
        
        # Clean up
        db.session.delete(test_job)
        db.session.commit()
        print("  ✓ Test job cleaned up")
except Exception as e:
    print(f"  ✗ Job creation test failed: {e}")
    print(f"  Full traceback:\n{traceback.format_exc()}")

print("\n=== Test completed ===")
