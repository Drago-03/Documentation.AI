# 🚀 Documentation.AI

> **Automated Repository Documentation Generator powered by AI**

Transform your GitHub repositories into professionally documented projects with the power of AI, advanced NLP, and RAG (Retrieval-Augmented Generation) pipelines.

![Documentation.AI Banner](https://via.placeholder.com/1200x400/667eea/ffffff?text=Documentation.AI)

## ✨ Features

- 🤖 **AI-Powered Analysis** - Advanced AI models analyze your repository structure, dependencies, and architecture
- 📚 **Comprehensive Documentation** - Generate README files, API docs, setup guides, and more
- ⚡ **Lightning Fast** - Process repositories in seconds with optimized RAG pipeline
- 🔒 **Secure & Private** - Your code is analyzed securely without permanent storage
- 🧠 **Smart Insights** - Get architectural insights, complexity analysis, and improvement suggestions
- 🌍 **Multi-Language Support** - Python, JavaScript, Java, Go, Rust, and many more
- 🎨 **Beautiful UI** - Modern, responsive interface with smooth animations
- 📊 **Analytics Dashboard** - Track your documentation generation history

## 🛠️ Technology Stack

### Backend
- **Python Flask** - Web framework for API endpoints
- **Google Gemini AI** - Advanced language model for code analysis
- **RAG Pipeline** - Retrieval-Augmented Generation with sentence transformers
- **FAISS** - Vector similarity search for semantic analysis
- **SQLAlchemy** - Database ORM for job tracking
- **GitPython** - Git repository manipulation

### Frontend
- **React 18** - Modern UI framework with hooks
- **TypeScript** - Type-safe JavaScript development
- **TailwindCSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations and transitions
- **Lucide React** - Beautiful icon set
- **Axios** - HTTP client for API communication

### AI & ML
- **Sentence Transformers** - Text embeddings for semantic search
- **Transformers** - Hugging Face model integration
- **NumPy & Pandas** - Data processing and analysis
- **LangChain** - LLM application framework

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 14.x+** with npm/yarn
- **Git** for repository cloning
- **API Keys** (see Configuration section)

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

#### Windows (PowerShell)
```powershell
# Clone the repository
git clone https://github.com/Drago-03/Documentation.AI.git
cd Documentation.AI

# Run PowerShell setup script
.\setup.ps1
```

#### Windows (Command Prompt)
```cmd
# Clone the repository
git clone https://github.com/Drago-03/Documentation.AI.git
cd Documentation.AI

# Run batch setup script
setup.bat
```

#### Linux/macOS
```bash
# Clone the repository
git clone https://github.com/Drago-03/Documentation.AI.git
cd Documentation.AI

# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### 1. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run build
cd ..
```

#### 3. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys (see Configuration section)
```

#### 4. Database Setup
```bash
# Initialize database (automatic on first run)
python app.py
```

## ⚙️ Configuration

Create a `.env` file with the following configuration:

```env
# AI Model API Keys
GEMINI_API_KEY=your_gemini_api_key_here
NVIDIA_API_KEY=your_nvidia_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here

# GitHub API (optional, for higher rate limits)
GITHUB_TOKEN=your_github_token_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=sqlite:///documentation_ai.db

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Sign up or log in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

#### Hugging Face Token (Optional)
1. Visit [Hugging Face](https://huggingface.co/)
2. Sign up and go to Settings > Access Tokens
3. Create a new token with read permissions
4. Add to your `.env` file

#### GitHub Token (Optional)
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with `public_repo` scope
3. Add to your `.env` file for higher API rate limits

## 🎯 Usage

### Starting the Application

#### Development Mode
```bash
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend (for development)
cd frontend
npm start
```

#### Production Mode
```bash
# Build frontend
cd frontend
npm run build
cd ..

# Start backend (serves built frontend)
python app.py
```

Visit `http://localhost:5000` to access the application.

### Using the Web Interface

1. **Home Page** - Overview and features
2. **Analyze Page** - Enter GitHub repository URL
3. **Results Page** - View generated documentation
4. **History Page** - Track previous analyses

### API Endpoints

#### Analyze Repository
```bash
POST /api/analyze
Content-Type: application/json

{
  "repo_url": "https://github.com/username/repository"
}
```

#### Get Job Status
```bash
GET /api/job/{job_id}
```

#### Get All Jobs
```bash
GET /api/jobs
```

#### Health Check
```bash
GET /api/health
```

## 🏗️ Project Structure

```
Documentation.AI/
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── setup.sh / setup.bat       # Setup scripts
├── README.md                  # This file
│
├── ai_models/                 # AI and ML components
│   ├── __init__.py
│   ├── github_analyzer.py     # Repository analysis
│   ├── documentation_generator.py # Doc generation
│   └── rag_pipeline.py        # RAG implementation
│
├── database/                  # Database models
│   ├── __init__.py
│   └── models.py              # SQLAlchemy models
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   └── file_processor.py      # File processing utilities
│
└── frontend/                  # React frontend
    ├── package.json
    ├── tailwind.config.js
    ├── public/
    └── src/
        ├── components/        # Reusable components
        ├── pages/            # Page components
        ├── App.tsx           # Main app component
        ├── index.tsx         # Entry point
        └── index.css         # Global styles
```

## 🧪 Testing

### Backend Tests
```bash
# Run Python tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=.
```

### Frontend Tests
```bash
cd frontend

# Run React tests
npm test

# Run with coverage
npm run test:coverage
```

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d
```

### Manual Docker Build
```bash
# Build backend image
docker build -t documentation-ai-backend .

# Build frontend image
cd frontend
docker build -t documentation-ai-frontend .

# Run containers
docker run -p 5000:5000 documentation-ai-backend
```

## 🚀 Production Deployment

### Environment Variables for Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Using Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Start with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- **Python**: Follow PEP 8, use Black formatter
- **JavaScript/TypeScript**: Follow Airbnb style guide, use Prettier
- **Commit Messages**: Use conventional commits format

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 **Email**: support@documentation-ai.com
- 💬 **GitHub Issues**: [Create an issue](https://github.com/yourusername/Documentation.AI/issues)
- 📖 **Documentation**: [Full docs](https://docs.documentation-ai.com)
- 💡 **Feature Requests**: [Request features](https://github.com/yourusername/Documentation.AI/discussions)

## 🙏 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI capabilities
- [Hugging Face](https://huggingface.co/) for transformer models
- [React](https://reactjs.org/) for the frontend framework
- [Flask](https://flask.palletsprojects.com/) for the backend framework
- [TailwindCSS](https://tailwindcss.com/) for styling
- All the amazing open-source contributors

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/Documentation.AI)
![GitHub forks](https://img.shields.io/github/forks/yourusername/Documentation.AI)
![GitHub issues](https://img.shields.io/github/issues/yourusername/Documentation.AI)
![License](https://img.shields.io/github/license/yourusername/Documentation.AI)

---

<div align="center">
  <strong>Built with ❤️ for developers by developers</strong>
  <br>
  <sub>Made possible by AI and the open-source community</sub>
</div>
