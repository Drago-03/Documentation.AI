# Quick Start Guide for Documentation.AI on macOS 🚀

## ✅ New Features Added

### 🎯 One-Command Server Start
- Created `start.sh` script that starts both backend and frontend servers together
- Automatically handles virtual environment activation
- Checks and installs dependencies if needed
- Provides colored output for better user experience
- Handles graceful shutdown with Ctrl+C

### 🛑 Clean Server Stop
- Created `stop.sh` script to cleanly stop all running servers
- Automatically cleans up log files
- Kills all related processes

## 🚀 How to Use

### Start Both Servers (Recommended)
```bash
./start.sh
```

### Stop Both Servers
```bash
./stop.sh
```

## 🎯 What the start.sh Script Does

1. **Environment Check**: Verifies Python 3 and Node.js are installed
2. **Virtual Environment**: Creates/activates .venv automatically
3. **Dependencies**: Installs/updates Python packages if needed
4. **Environment File**: Creates .env from template if missing
5. **Frontend Setup**: Installs npm packages if needed
6. **Backend Start**: Starts Flask server on port 5001
7. **Frontend Start**: Starts React server on port 3000
8. **Monitoring**: Monitors both servers and handles cleanup

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/api/health

## 📋 Features

- ✅ Colored terminal output for better visibility
- ✅ Automatic dependency management
- ✅ Graceful shutdown handling
- ✅ Process monitoring
- ✅ Log file management
- ✅ Error detection and reporting

## 🔧 Global Virtual Environment

The script uses a local `.venv` directory within your project (not truly global), but it's automatically managed so you don't need to manually activate it each time. This approach keeps your project dependencies isolated while making the startup process seamless.

Your Documentation.AI application is now fully automated for macOS! 🎉
