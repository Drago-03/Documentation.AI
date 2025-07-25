#!/bin/bash

# Setup script for Documentation.AI
echo "🚀 Setting up Documentation.AI Environment"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this from the Documentation.AI directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "💡 Make sure Python 3 is installed: brew install python3"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install essential Flask dependencies
echo "📦 Installing Flask dependencies..."
pip install flask==2.3.3 flask-cors==4.0.0 flask-sqlalchemy==3.0.5 python-dotenv==1.0.0 requests==2.31.0

# Test Flask installation
echo "🧪 Testing Flask installation..."
python -c "import flask; print('✅ Flask version:', flask.__version__)"
if [ $? -ne 0 ]; then
    echo "❌ Flask installation failed"
    exit 1
fi

# Test app import
echo "🧪 Testing app import..."
python -c "from app import app; print('✅ App imports successfully')"
if [ $? -ne 0 ]; then
    echo "❌ App import failed, but Flask is installed"
    echo "💡 This might be due to missing optional dependencies"
    echo "📦 Installing additional dependencies..."
    pip install gitpython markdown beautifulsoup4
    
    # Try again
    python -c "from app import app; print('✅ App imports successfully')"
    if [ $? -ne 0 ]; then
        echo "⚠️  App import still failing - check for missing dependencies"
        echo "🔍 Try running: source .venv/bin/activate && python app.py"
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the environment:"
echo "  source .venv/bin/activate"
echo "  python app.py"
echo ""
echo "To install additional dependencies:"
echo "  source .venv/bin/activate"
echo "  pip install -r requirements.txt"
