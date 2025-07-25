@echo off
echo 🚀 Setting up Documentation.AI...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 14.x or higher.
    pause
    exit /b 1
)

echo ✅ Python and Node.js found

REM Create virtual environment
echo 📦 Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Setup environment file
if not exist .env (
    echo 📝 Creating environment file...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your API keys before running the application
)

REM Setup frontend
echo 📦 Setting up frontend...
cd frontend

REM Install Node.js dependencies
call npm install

REM Build frontend for production
call npm run build

cd ..

echo ✅ Setup completed!
echo.
echo Next steps:
echo 1. Edit the .env file with your API keys
echo 2. Run 'python app.py' to start the backend server
echo 3. Run 'cd frontend && npm start' to start the frontend development server
echo.
echo 🎉 Documentation.AI is ready to use!
pause
