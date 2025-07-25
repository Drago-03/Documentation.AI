# Tests Directory

This directory contains all test files and testing utilities for Documentation.AI.

## Test Files

- `test_app.py` - Main application tests
- `test_imports.py` - Import and dependency tests
- `run_tests.sh` - Test runner script
- `test_servers.sh` - Server testing script

## Running Tests

### Quick Test Run
```bash
# From the project root
./tests/run_tests.sh
```

### Manual Test Run
```bash
# Activate virtual environment first
source .venv/bin/activate

# Run tests with pytest
python -m pytest tests/ -v
```

### Individual Test Files
```bash
# Run specific test file
python tests/test_app.py
python tests/test_imports.py
```

## Test Coverage

The test suite covers:
- ✅ Application startup and configuration
- ✅ API endpoints and responses
- ✅ Database models and operations
- ✅ AI model imports and initialization
- ✅ File processing utilities
- ✅ Server functionality

## Adding New Tests

When adding new features, please:
1. Add corresponding tests in the appropriate `test_*.py` file
2. Update the test runner if needed
3. Ensure tests pass before committing changes

## Test Environment

Tests are designed to run in the same environment as the main application. Make sure you have:
- Python virtual environment activated
- All dependencies installed from `requirements.txt`
- Proper environment configuration (.env file)
