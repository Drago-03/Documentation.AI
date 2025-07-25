#!/usr/bin/env python3
"""Test script to check imports and identify issues"""

import sys
import os
import traceback
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("🔍 Testing imports...")
print(f"Python path: {sys.path[0]}")
print(f"Current directory: {os.getcwd()}")

# Test 1: Check if ai_models directory exists
ai_models_dir = Path(__file__).parent / 'ai_models'
print(f"AI models directory exists: {ai_models_dir.exists()}")
if ai_models_dir.exists():
    print(f"AI models files: {list(ai_models_dir.glob('*.py'))}")

# Test 2: Try importing each module individually
modules_to_test = [
    'ai_models.github_analyzer',
    'ai_models.documentation_generator', 
    'ai_models.rag_pipeline'
]

for module_name in modules_to_test:
    try:
        print(f"\n📦 Testing {module_name}...")
        module = __import__(module_name, fromlist=[''])
        print(f"✅ {module_name} imported successfully")
        
        # Get the class from the module
        class_name = module_name.split('.')[-1].title().replace('_', '')
        if class_name == 'GithubAnalyzer':
            class_name = 'GitHubAnalyzer'
        elif class_name == 'DocumentationGenerator':
            class_name = 'DocumentationGenerator'
        elif class_name == 'RagPipeline':
            class_name = 'RAGPipeline'
            
        if hasattr(module, class_name):
            cls = getattr(module, class_name)
            print(f"✅ Found class {class_name}")
            
            # Try to instantiate
            try:
                instance = cls()
                print(f"✅ {class_name} instantiated successfully")
            except Exception as e:
                print(f"❌ Failed to instantiate {class_name}: {e}")
        else:
            print(f"❌ Class {class_name} not found in module")
            print(f"Available attributes: {[attr for attr in dir(module) if not attr.startswith('_')]}")
            
    except Exception as e:
        print(f"❌ Failed to import {module_name}: {e}")
        print(f"Error details: {traceback.format_exc()}")

# Test 3: Try importing Flask dependencies
flask_deps = ['Flask', 'flask_cors', 'flask_sqlalchemy']
print(f"\n🌐 Testing Flask dependencies...")
for dep in flask_deps:
    try:
        __import__(dep)
        print(f"✅ {dep} imported successfully")
    except Exception as e:
        print(f"❌ Failed to import {dep}: {e}")

# Test 4: Check environment variables
print(f"\n🔧 Environment variables:")
env_vars = ['GITHUB_TOKEN', 'GEMINI_API_KEY', 'SECRET_KEY']
for var in env_vars:
    value = os.getenv(var)
    print(f"{var}: {'✅ Set' if value else '❌ Not set'}")

print(f"\n✨ Import test completed!")
