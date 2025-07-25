# Scripts Directory

This directory contains setup and utility scripts for different platforms.

## Setup Scripts

- `setup.sh` - Linux/macOS setup script
- `setup.ps1` - PowerShell setup script for Windows
- `setup.bat` - Batch setup script for Windows
- `start.ps1` - PowerShell start script for Windows

## Documentation

- `QUICK_START_GUIDE.md` - Quick start instructions
- `WINDOWS_SETUP.md` - Windows-specific setup guide
- `LOCAL_SETUP_COMPLETE.md` - Local setup completion guide
- `PORT_CONFIGURATION.md` - Port configuration documentation

## Usage

For the simplest experience, use the main `start.sh` and `stop.sh` scripts in the root directory. These scripts in this folder are provided for platform-specific needs and advanced users.

### Linux/macOS Users
```bash
# Use the main scripts in the root directory
./start.sh    # Start the application
./stop.sh     # Stop the application
```

### Windows Users
```powershell
# One-time setup
./scripts/setup.ps1

# Then start the application
python app.py
```
