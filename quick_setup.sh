#!/bin/bash
echo "Creating virtual environment..."
cd /Users/mantejsingh/Desktop/Documentation.AI
python3 -m venv .venv
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Installing Flask..."
pip install flask
echo "Testing Flask..."
python -c "import flask; print('Flask installed successfully')"
