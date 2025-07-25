#!/bin/bash

# Documentation.AI - Fixed Startup Script
echo "🚀 Documentation.AI - Fixed Startup"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

# Kill any existing processes on our ports
echo -e "${YELLOW}🧹 Cleaning up existing processes...${NC}"
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
sleep 2

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed or not in PATH${NC}"
    exit 1
fi

# Check if required directories exist
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ app.py not found. Please run from the project root directory.${NC}"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo -e "${RED}❌ frontend directory not found.${NC}"
    exit 1
fi

# Check if Node.js and npm are available
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed or not in PATH${NC}"
    exit 1
fi

# Install Python dependencies if needed
echo -e "${BLUE}📦 Checking Python dependencies...${NC}"
if [ ! -d ".venv" ] && [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}⚠️ No virtual environment or requirements.txt found${NC}"
fi

# Install frontend dependencies if needed
echo -e "${BLUE}📦 Checking frontend dependencies...${NC}"
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}📥 Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Start backend server
echo -e "${BLUE}🎯 Starting backend server on port 5000...${NC}"
python app.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start and check if it's responding
echo -e "${YELLOW}⏳ Waiting for backend to start...${NC}"
backend_ready=false
for i in {1..30}; do
    sleep 1
    if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
        backend_ready=true
        break
    fi
    echo -n "."
done

echo ""

if [ "$backend_ready" = true ]; then
    echo -e "${GREEN}✅ Backend server is running on http://localhost:5000${NC}"
    echo -e "${GREEN}✅ Health check: curl http://localhost:5000/api/health${NC}"
else
    echo -e "${RED}❌ Backend server failed to start or is not responding${NC}"
    echo -e "${YELLOW}📋 Check backend.log for errors:${NC}"
    tail -10 backend.log
    cleanup
fi

# Start frontend server
echo -e "${BLUE}🎯 Starting frontend server on port 3000...${NC}"
cd frontend

# Set the port explicitly for React
export PORT=3000
npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo -e "${YELLOW}⏳ Waiting for frontend to start...${NC}"
frontend_ready=false
for i in {1..60}; do
    sleep 1
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        frontend_ready=true
        break
    fi
    echo -n "."
done

echo ""

if [ "$frontend_ready" = true ]; then
    echo -e "${GREEN}✅ Frontend server is running on http://localhost:3000${NC}"
else
    echo -e "${YELLOW}⚠️ Frontend server is starting... (this may take a while)${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Documentation.AI is starting up!${NC}"
echo -e "${BLUE}🌐 Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}📡 Backend: http://localhost:5000${NC}"
echo -e "${BLUE}🩺 Health Check: http://localhost:5000/api/health${NC}"
echo ""
echo -e "${YELLOW}📋 To view logs:${NC}"
echo -e "   Backend: tail -f backend.log"
echo -e "   Frontend: tail -f frontend.log"
echo ""
echo -e "${YELLOW}🛑 Press Ctrl+C to stop all servers${NC}"

# Keep script running and monitoring
while true; do
    sleep 5
    
    # Check if backend is still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Backend server stopped unexpectedly${NC}"
        echo -e "${YELLOW}📋 Last backend log entries:${NC}"
        tail -5 backend.log
        cleanup
    fi
    
    # Check if frontend is still running
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Frontend server stopped unexpectedly${NC}"
        echo -e "${YELLOW}📋 Last frontend log entries:${NC}"
        tail -5 frontend.log
        cleanup
    fi
done
