Write-Host "🚀 Setting up Documentation.AI..." -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.8 or higher." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 14.x or higher." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment
Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Setup environment file
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating environment file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit .env file with your API keys before running the application" -ForegroundColor Yellow
}

# Setup frontend
Write-Host "📦 Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install Node.js dependencies
Write-Host "📥 Installing frontend dependencies..." -ForegroundColor Yellow
npm install

# Build frontend for production
Write-Host "🏗️  Building frontend..." -ForegroundColor Yellow
npm run build

Set-Location ..

Write-Host "" 
Write-Host "✅ Setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit the .env file with your API keys" -ForegroundColor White
Write-Host "2. Run 'python app.py' to start the backend server" -ForegroundColor White
Write-Host "3. Run 'cd frontend && npm start' to start the frontend development server" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Documentation.AI is ready to use!" -ForegroundColor Green

Read-Host "Press Enter to exit"
