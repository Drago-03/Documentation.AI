#!/bin/bash

# Documentation.AI - Start Script
echo "🚀 Starting Documentation.AI..."

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
    echo -e "${GREEN}👋 Documentation.AI stopped successfully!${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check dependencies
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed.${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencies found${NC}"

# Setup Python environment
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Install Python dependencies if needed
if [ ! -f ".venv/.last_install" ] || [ "requirements.txt" -nt ".venv/.last_install" ]; then
    echo -e "${BLUE}� Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    touch .venv/.last_install
fi

# Setup environment file
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env file with your API keys${NC}"
fi

# Setup frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Start backend server
echo -e "${BLUE}🎯 Starting backend server...${NC}"
python app.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend server
echo -e "${BLUE}🎯 Starting frontend server...${NC}"
cd frontend
npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}🎉 Documentation.AI is running!${NC}"
echo ""
echo -e "${BLUE}📱 Access Points:${NC}"
echo -e "   Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "   Backend:  ${GREEN}http://localhost:5002${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Wait for processes
wait
else
    echo -e "${YELLOW}⚠️  Full app startup failed, starting simplified server...${NC}"
    # Kill the failed process
    kill $BACKEND_PID 2>/dev/null
    
    # Start simple server
    python app_simple.py > backend.log 2>&1 &
    BACKEND_PID=$!
    
    sleep 5
    if curl -s http://localhost:5001/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Simplified backend server started successfully${NC}"
        echo -e "${YELLOW}📝 Note: AI features are disabled in simplified mode${NC}"
    else
        echo -e "${RED}❌ Even simplified server failed to start.${NC}"
        echo -e "${YELLOW}📋 Backend log contents:${NC}"
        cat backend.log
        cleanup
    fi
fi

# Start frontend server in background
echo -e "${BLUE}🎯 Starting frontend server on http://localhost:3000...${NC}"
cd frontend
PORT=3000 npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 8

# Check if frontend started successfully
if ! curl -s http://localhost:3000 > /dev/null; then
    echo -e "${YELLOW}⚠️  Frontend server may still be starting up...${NC}"
fi

echo -e "${GREEN}✅ Frontend server started${NC}"
echo ""
echo -e "${CYAN}🎉 Documentation.AI is now running!${NC}"
echo ""
echo -e "${BLUE}📱 Access your application:${NC}"
echo -e "   ${CYAN}Frontend (Main App): http://localhost:3000${NC}"
echo -e "   ${CYAN}Backend API:         http://localhost:5001${NC}"
echo -e "   ${CYAN}API Health Check:    http://localhost:5001/api/health${NC}"
echo ""
echo -e "${YELLOW}📋 Useful commands:${NC}"
echo -e "   ${CYAN}View backend logs:   tail -f backend.log${NC}"
echo -e "   ${CYAN}View frontend logs:  tail -f frontend.log${NC}"
echo ""
echo -e "${GREEN}🚨 Press Ctrl+C to stop both servers${NC}"
echo ""

# Keep script running and wait for user to stop
while true; do
    # Check if processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Backend server stopped unexpectedly. Check backend.log${NC}"
        cleanup
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Frontend server stopped unexpectedly. Check frontend.log${NC}"
        cleanup
    fi
    
    sleep 5
done
