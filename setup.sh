#!/bin/bash

echo "🚀 Setting up Documentation.AI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14.x or higher."
    exit 1
fi

echo "✅ Python and Node.js found"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the application"
fi

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend

# Install Node.js dependencies
npm install

# Build frontend for production
npm run build

cd ..

echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your API keys"
echo "2. Run 'python app.py' to start the backend server"
echo "3. Run 'cd frontend && npm start' to start the frontend development server"
echo ""
echo "🎉 Documentation.AI is ready to use!"
