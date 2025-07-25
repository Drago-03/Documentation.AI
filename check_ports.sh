#!/bin/bash

# Port Check and Server Startup Script
echo "🔍 Checking current port usage..."

# Check if ports are in use
check_port() {
    local port=$1
    local service=$2
    if lsof -i :$port >/dev/null 2>&1; then
        echo "⚠️  Port $port is already in use by:"
        lsof -i :$port
        return 1
    else
        echo "✅ Port $port is available for $service"
        return 0
    fi
}

# Check backend port (5000)
echo ""
echo "📡 Backend Port Check (5000):"
check_port 5000 "Backend (Flask)"

# Check frontend port (3000)
echo ""
echo "🌐 Frontend Port Check (3000):"
check_port 3000 "Frontend (React)"

echo ""
echo "🔧 Current Configuration:"
echo "   Backend: http://localhost:5000"
echo "   Frontend: http://localhost:3000"
echo "   Frontend proxy target: http://localhost:5000"

echo ""
echo "🚀 To start the servers:"
echo "   1. Backend: python app.py"
echo "   2. Frontend: cd frontend && npm start"
echo "   3. Or use: ./start.sh"

echo ""
echo "🩺 To test if backend is running:"
echo "   curl http://localhost:5000/api/health"

echo ""
echo "🌐 To test the full stack:"
echo "   Open http://localhost:3000 in your browser"
