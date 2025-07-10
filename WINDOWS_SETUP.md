# Documentation.AI - Windows Setup Instructions

## Quick Start for Windows Users

### If you get PowerShell execution policy errors:

1. **Open PowerShell as Administrator**
2. **Run this command to allow script execution:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. **Type 'Y' and press Enter when prompted**

### Then run the setup:

```powershell
# Navigate to the project directory
cd "C:\Users\mante\OneDrive\Desktop\Documentation.AI"

# Run the setup script
.\setup.ps1
```

### After setup, start the application:

```powershell
# Quick start
.\start.ps1

# Or manually
python app.py
```

### Alternative: Use Command Prompt

If you prefer Command Prompt over PowerShell:

```cmd
# Navigate to project directory
cd "C:\Users\mante\OneDrive\Desktop\Documentation.AI"

# Run setup
setup.bat

# Start application
python app.py
```

## Troubleshooting

### Common Issues:

1. **"python is not recognized"**
   - Install Python from python.org
   - Make sure to check "Add Python to PATH" during installation

2. **"node is not recognized"** 
   - Install Node.js from nodejs.org
   - Restart your terminal after installation

3. **PowerShell execution policy error**
   - Run as Administrator: `Set-ExecutionPolicy RemoteSigned`

4. **Permission denied**
   - Right-click PowerShell and "Run as Administrator"

5. **Virtual environment activation fails**
   - Delete the `venv` folder and run setup again

### Need Help?

- Check the main README.md for detailed instructions
- Create an issue on GitHub if problems persist
