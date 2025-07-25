#!/bin/bash

echo "Testing Documentation.AI servers..."

# Start backend
echo "Starting backend server..."
cd /Users/mantejsingh/Desktop/Documentation.AI
source .venv/bin/activate
python app_simple.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Test backend
echo "Testing backend API..."
curl -s http://localhost:5001/api/health || echo "Backend not responding"

# Start frontend in background for testing
echo "Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Visit: http://localhost:3000"
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
wait
