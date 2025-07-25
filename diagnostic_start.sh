#!/bin/bash

# Documentation.AI - Complete Diagnostic and Startup Script
echo "🔧 Documentation.AI - Diagnostic and Startup"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    local port=$1
    local service=$2
    if lsof -i :$port >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $port is already in use by $service:${NC}"
        lsof -i :$port
        return 1
    else
        echo -e "${GREEN}✅ Port $port is available for $service${NC}"
        return 0
    fi
}

# Function to wait for a service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    
    echo -e "${YELLOW}⏳ Waiting for $service_name to start...${NC}"
    for i in $(seq 1 $max_attempts); do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        sleep 1
        echo -n "."
    done
    echo -e "${RED}❌ $service_name failed to start within $max_attempts seconds${NC}"
    return 1
}

# Check environment configuration
echo -e "${BLUE}🔍 Environment Configuration:${NC}"
cd /Users/mantejsingh/Desktop/Documentation.AI
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(f'PORT: {os.getenv(\"PORT\", \"5000 (default)\")}')
print(f'HOST: {os.getenv(\"HOST\", \"0.0.0.0 (default)\")}')
print(f'FLASK_DEBUG: {os.getenv(\"FLASK_DEBUG\", \"False (default)\")}')
print(f'GITHUB_TOKEN: {\"✅ Set\" if os.getenv(\"GITHUB_TOKEN\") else \"❌ Not set\"}')
print(f'GEMINI_API_KEY: {\"✅ Set\" if os.getenv(\"GEMINI_API_KEY\") else \"❌ Not set\"}')
"

echo ""
echo -e "${BLUE}🔍 Port Status Check:${NC}"
check_port 5002 "Backend (Flask)"
echo ""
check_port 3000 "Frontend (React)"

echo ""
echo -e "${BLUE}🔍 File System Check:${NC}"
if [ -f "app.py" ]; then
    echo -e "${GREEN}✅ app.py found${NC}"
else
    echo -e "${RED}❌ app.py not found${NC}"
    exit 1
fi

if [ -d "frontend" ]; then
    echo -e "${GREEN}✅ frontend directory found${NC}"
else
    echo -e "${RED}❌ frontend directory not found${NC}"
    exit 1
fi

if [ -f "frontend/package.json" ]; then
    echo -e "${GREEN}✅ frontend/package.json found${NC}"
    proxy_config=$(cat frontend/package.json | grep '"proxy"' | sed 's/.*"proxy": *"\([^"]*\)".*/\1/')
    echo -e "${BLUE}📡 Frontend proxy configured to: $proxy_config${NC}"
else
    echo -e "${RED}❌ frontend/package.json not found${NC}"
fi

echo ""
echo -e "${BLUE}🔍 Dependencies Check:${NC}"
if command -v python &> /dev/null; then
    python_version=$(python --version 2>&1)
    echo -e "${GREEN}✅ Python: $python_version${NC}"
else
    echo -e "${RED}❌ Python not found${NC}"
    exit 1
fi

if command -v npm &> /dev/null; then
    npm_version=$(npm --version 2>&1)
    echo -e "${GREEN}✅ npm: $npm_version${NC}"
else
    echo -e "${RED}❌ npm not found${NC}"
    exit 1
fi

# Check if we should start services
echo ""
read -p "🚀 Would you like to start the services? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Cleanup existing processes
    echo -e "${YELLOW}🧹 Cleaning up existing processes...${NC}"
    lsof -ti:5002 | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    sleep 2
    
    # Function to cleanup on exit
    cleanup() {
        echo -e "\n${YELLOW}🛑 Stopping servers...${NC}"
        if [ ! -z "$BACKEND_PID" ]; then
            kill $BACKEND_PID 2>/dev/null
            echo -e "${GREEN}✅ Backend server stopped${NC}"
        fi
        if [ ! -z "$FRONTEND_PID" ]; then
            kill $FRONTEND_PID 2>/dev/null
            echo -e "${GREEN}✅ Frontend server stopped${NC}"
        fi
        exit 0
    }
    
    # Set up trap for cleanup
    trap cleanup SIGINT SIGTERM
    
    # Start backend
    echo -e "${BLUE}🎯 Starting backend server...${NC}"
    python app.py > backend.log 2>&1 &
    BACKEND_PID=$!
    
    # Wait for backend to be ready
    if wait_for_service "http://localhost:5002/api/health" "Backend"; then
        echo -e "${GREEN}🩺 Backend health check: http://localhost:5002/api/health${NC}"
        
        # Test backend health
        echo -e "${BLUE}🔬 Testing backend health...${NC}"
        curl -s http://localhost:5002/api/health | python -m json.tool 2>/dev/null || echo "Health check returned non-JSON response"
        
    else
        echo -e "${RED}❌ Backend failed to start. Check backend.log:${NC}"
        tail -10 backend.log
        cleanup
    fi
    
    # Install frontend dependencies if needed
    if [ ! -d "frontend/node_modules" ]; then
        echo -e "${YELLOW}📥 Installing frontend dependencies...${NC}"
        cd frontend
        npm install
        cd ..
    fi
    
    # Start frontend
    echo -e "${BLUE}🎯 Starting frontend server...${NC}"
    cd frontend
    PORT=3000 npm start > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for frontend
    echo -e "${YELLOW}⏳ Frontend is starting (this may take a while)...${NC}"
    sleep 10
    
    echo ""
    echo -e "${GREEN}🎉 Services are starting!${NC}"
    echo -e "${GREEN}🌐 Frontend: http://localhost:3000${NC}"
    echo -e "${GREEN}📡 Backend: http://localhost:5002${NC}"
    echo -e "${GREEN}🩺 Health Check: http://localhost:5002/api/health${NC}"
    echo ""
    echo -e "${BLUE}📋 Log files:${NC}"
    echo -e "   Backend: tail -f backend.log"
    echo -e "   Frontend: tail -f frontend.log"
    echo ""
    echo -e "${YELLOW}🛑 Press Ctrl+C to stop all servers${NC}"
    
    # Monitor services
    while true; do
        sleep 5
        
        if ! kill -0 $BACKEND_PID 2>/dev/null; then
            echo -e "${RED}❌ Backend server stopped unexpectedly${NC}"
            echo -e "${YELLOW}📋 Last backend log entries:${NC}"
            tail -5 backend.log
            cleanup
        fi
        
        if ! kill -0 $FRONTEND_PID 2>/dev/null; then
            echo -e "${YELLOW}⚠️ Frontend server stopped${NC}"
            # Frontend might restart itself, so don't exit
        fi
    done
else
    echo -e "${YELLOW}✋ Startup cancelled. You can run this script again when ready.${NC}"
    echo ""
    echo -e "${BLUE}🔧 Manual startup commands:${NC}"
    echo -e "   Backend: python app.py"
    echo -e "   Frontend: cd frontend && npm start"
fi
