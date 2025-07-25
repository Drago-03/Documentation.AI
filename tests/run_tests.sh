#!/bin/bash

# Test runner for Documentation.AI
echo "🧪 Running Documentation.AI tests..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Navigate to project root if we're in tests directory
if [[ "$PWD" == *"/tests" ]]; then
    cd ..
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
    source .venv/bin/activate
fi

# Run Python tests
echo -e "${BLUE}🧪 Running Python tests...${NC}"
python -m pytest tests/ -v

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Test suite completed successfully!${NC}"
