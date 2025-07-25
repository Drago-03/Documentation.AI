#!/bin/bash

# Documentation.AI - Simple Stop Script
echo "🛑 Stopping Documentation.AI servers..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Kill backend processes
pkill -f "python.*app.py" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend server stopped${NC}"
else
    echo -e "${YELLOW}ℹ️  No backend server was running${NC}"
fi

# Kill frontend processes
pkill -f "react-scripts start" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend server stopped${NC}"
else
    echo -e "${YELLOW}ℹ️  No frontend server was running${NC}"
fi

# Clean up log files
rm -f backend.log frontend.log 2>/dev/null

echo -e "${GREEN}🎉 Documentation.AI stopped successfully!${NC}"
