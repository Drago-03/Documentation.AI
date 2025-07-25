#!/usr/bin/env python3
"""
Documentation.AI - Clean Backend Implementation
A comprehensive documentation generator using AI for GitHub repositories.
"""

import os
import json
import logging
import tempfile
import shutil
import zipfile
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import requests
import re
from urllib.parse import urlparse
import traceback

# Add the current directory to Python path for importing ai_models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import AI models
try:
    from ai_models.github_analyzer import GitHubAnalyzer as GitHubAnalyzerModel
    from ai_models.documentation_generator import DocumentationGenerator as DocumentationGeneratorModel
    from ai_models.rag_pipeline import RAGPipeline as RAGPipelineModel
    logger = logging.getLogger(__name__)
    logger.info("AI models imported successfully")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to import AI models: {e}")
    logger.error(traceback.format_exc())
    # Define dummy classes as fallback
    class GitHubAnalyzer:
        def __init__(self):
            self.github_token = os.getenv('GITHUB_TOKEN')
        def parse_github_url(self, repo_url: str) -> Dict[str, str]:
            return {'owner': 'dummy', 'repo': 'dummy'}
        def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
            raise Exception("AI models not available - import failed")
    
    class DummyDocumentationGenerator:
        def generate_documentation(self, analysis_result: Dict[str, Any], rag_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            raise Exception("AI models not available - import failed")
    
    class RAGPipeline:
        def process(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
            raise Exception("AI models not available - import failed")
        def process_repository(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
            raise Exception("AI models not available - import failed")

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-documentation-ai-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///documentation_ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload

# Initialize extensions
CORS(app, origins=["http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000"])
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('backend.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Set Flask's logger to DEBUG as well
app.logger.setLevel(logging.DEBUG)

# Database Models
class AnalysisJob(db.Model):
    """Model for storing repository analysis jobs"""
    __tablename__ = 'analysis_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    repo_url = db.Column(db.String(500), nullable=False)
    repo_name = db.Column(db.String(200))
    repo_owner = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    result = db.Column(db.Text)  # JSON string containing the generated documentation
    error_message = db.Column(db.Text)
    
    def __repr__(self):
        return f'<AnalysisJob {self.id}: {self.repo_url}>'
    
    def to_dict(self):
        """Convert the job to a dictionary"""
        return {
            'id': self.id,
            'repo_url': self.repo_url,
            'repo_name': self.repo_name,
            'repo_owner': self.repo_owner,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'result': json.loads(self.result) if self.result else None,
            'error_message': self.error_message
        }

# GitHub Repository Analyzer
class GitHubRepositoryAnalyzer:
    """Clean implementation of GitHub repository analyzer"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.session = requests.Session()
        if self.github_token:
            self.session.headers.update({
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def parse_github_url(self, repo_url: str) -> Dict[str, str]:
        """Parse GitHub repository URL to extract owner and repo name"""
        repo_url = repo_url.strip().rstrip('/')
        
        # Handle different GitHub URL formats
        patterns = [
            r'https://github\.com/([^/]+)/([^/]+)(?:\.git)?/?$',
            r'git@github\.com:([^/]+)/([^/]+)\.git$',
            r'github\.com/([^/]+)/([^/]+)/?$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, repo_url)
            if match:
                owner, repo = match.groups()
                # Remove .git suffix if present
                repo = repo.replace('.git', '')
                return {'owner': owner, 'repo': repo}
        
        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")
    
    def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository information from GitHub API"""
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}"
            response = self.session.get(url)
            
            if response.status_code == 404:
                raise ValueError("Repository not found")
            elif response.status_code != 200:
                raise ValueError(f"GitHub API error: {response.status_code}")
            
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching repository info: {e}")
            raise ValueError(f"Failed to fetch repository information: {str(e)}")
    
    def get_file_tree(self, owner: str, repo: str, path: str = "") -> List[Dict[str, Any]]:
        """Get repository file tree"""
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            response = self.session.get(url)
            
            if response.status_code != 200:
                return []
            
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching file tree: {e}")
            return []
    
    def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Analyze a GitHub repository and return comprehensive information"""
        try:
            # Parse URL
            parsed = self.parse_github_url(repo_url)
            owner, repo = parsed['owner'], parsed['repo']
            
            # Get repository info
            repo_info = self.get_repository_info(owner, repo)
            
            # Get file structure
            file_tree = self.get_file_tree(owner, repo)
            
            # Analyze languages and technologies
            languages = self._detect_languages(file_tree, owner, repo)
            technologies = self._detect_technologies(file_tree, repo_info)
            
            # Build analysis result
            analysis_result = {
                'repository_info': {
                    'name': repo_info.get('name'),
                    'full_name': repo_info.get('full_name'),
                    'description': repo_info.get('description', ''),
                    'html_url': repo_info.get('html_url'),
                    'clone_url': repo_info.get('clone_url'),
                    'language': repo_info.get('language'),
                    'stargazers_count': repo_info.get('stargazers_count', 0),
                    'forks_count': repo_info.get('forks_count', 0),
                    'open_issues_count': repo_info.get('open_issues_count', 0),
                    'created_at': repo_info.get('created_at'),
                    'updated_at': repo_info.get('updated_at'),
                    'license': repo_info.get('license', {}).get('name') if repo_info.get('license') else None,
                    'topics': repo_info.get('topics', [])
                },
                'file_structure': {
                    'total_files': len(file_tree),
                    'languages': languages,
                    'important_files': self._find_important_files(file_tree),
                    'directories': [f['name'] for f in file_tree if f['type'] == 'dir'],
                    'files': [f['name'] for f in file_tree if f['type'] == 'file']
                },
                'technologies': technologies,
                'analysis_metadata': {
                    'analyzed_at': datetime.utcnow().isoformat(),
                    'analyzer_version': '2.0.0'
                }
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing repository: {e}")
            raise
    
    def _detect_languages(self, file_tree: List[Dict], owner: str, repo: str) -> Dict[str, int]:
        """Detect programming languages in the repository"""
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/languages"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        
        # Fallback: detect from file extensions
        language_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
            '.php': 'PHP', '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust',
            '.swift': 'Swift', '.kt': 'Kotlin', '.scala': 'Scala',
            '.html': 'HTML', '.css': 'CSS', '.scss': 'SCSS'
        }
        
        languages = {}
        for file_info in file_tree:
            if file_info['type'] == 'file':
                ext = Path(file_info['name']).suffix.lower()
                if ext in language_map:
                    lang = language_map[ext]
                    languages[lang] = languages.get(lang, 0) + 1
        
        return languages
    
    def _detect_technologies(self, file_tree: List[Dict], repo_info: Dict) -> Dict[str, Any]:
        """Detect technologies and frameworks used"""
        technologies = {
            'frameworks': [],
            'databases': [],
            'tools': [],
            'deployment': []
        }
        
        file_names = [f['name'].lower() for f in file_tree if f['type'] == 'file']
        
        # Framework detection
        if 'package.json' in file_names:
            technologies['frameworks'].append('Node.js')
        if 'requirements.txt' in file_names or 'setup.py' in file_names:
            technologies['frameworks'].append('Python')
        if 'composer.json' in file_names:
            technologies['frameworks'].append('PHP')
        if 'go.mod' in file_names:
            technologies['frameworks'].append('Go')
        if 'cargo.toml' in file_names:
            technologies['frameworks'].append('Rust')
        
        # Database detection
        if any('sql' in name for name in file_names):
            technologies['databases'].append('SQL Database')
        if 'mongodb' in str(file_names):
            technologies['databases'].append('MongoDB')
        
        # Deployment detection
        if 'dockerfile' in file_names:
            technologies['deployment'].append('Docker')
        if 'docker-compose.yml' in file_names or 'docker-compose.yaml' in file_names:
            technologies['deployment'].append('Docker Compose')
        if '.github' in [f['name'] for f in file_tree if f['type'] == 'dir']:
            technologies['deployment'].append('GitHub Actions')
        
        return technologies
    
    def _find_important_files(self, file_tree: List[Dict]) -> List[str]:
        """Find important files in the repository"""
        important_patterns = [
            'readme.md', 'readme.txt', 'readme',
            'license', 'license.txt', 'license.md',
            'contributing.md', 'contributing.txt',
            'changelog.md', 'changelog.txt', 'changelog',
            'package.json', 'requirements.txt', 'setup.py',
            'dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
            'makefile', 'cmake', '.gitignore'
        ]
        
        important_files = []
        for file_info in file_tree:
            if file_info['type'] == 'file':
                name = file_info['name'].lower()
                if any(pattern in name for pattern in important_patterns):
                    important_files.append(file_info['name'])
        
        return important_files

# Documentation Generator
class DocumentationGenerator:
    """Generate comprehensive documentation from repository analysis"""
    
    def __init__(self):
        self.template_path = Path(__file__).parent / 'templates'
    
    def generate_documentation(self, analysis_result: Dict[str, Any], rag_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate complete documentation package"""
        try:
            repo_info = analysis_result.get('repository_info', {})
            file_structure = analysis_result.get('file_structure', {})
            technologies = analysis_result.get('technologies', {})
            
            documentation = {
                'readme': self._generate_readme(repo_info, file_structure, technologies),
                'api_docs': self._generate_api_documentation(repo_info, technologies),
                'setup_guide': self._generate_setup_guide(repo_info, technologies),
                'architecture_docs': self._generate_architecture_docs(repo_info, technologies),
                'contributing_guide': self._generate_contributing_guide(repo_info),
                'changelog': self._generate_changelog_template(repo_info),
                'license': self._generate_license_file(repo_info),
                'gitignore': self._generate_gitignore(technologies),
                'dockerfile': self._generate_dockerfile(technologies),
                'additional_files': {
                    '.github/workflows/ci.yml': self._generate_github_actions(technologies),
                    'docs/deployment.md': self._generate_deployment_guide(technologies),
                    'docs/troubleshooting.md': self._generate_troubleshooting_guide(technologies)
                }
            }
            
            return documentation
            
        except Exception as e:
            logger.error(f"Error generating documentation: {e}")
            raise
    
    def _generate_readme(self, repo_info: Dict, file_structure: Dict, technologies: Dict) -> str:
        """Generate a comprehensive README.md file"""
        project_name = repo_info.get('name', 'Project')
        description = repo_info.get('description', 'A software project')
        language = repo_info.get('language', 'Unknown')
        
        readme_content = f"""# {project_name}

{description}

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🔍 Overview

{description}

### Key Statistics
- **Primary Language**: {language}
- **Stars**: {repo_info.get('stargazers_count', 0)}
- **Forks**: {repo_info.get('forks_count', 0)}
- **Open Issues**: {repo_info.get('open_issues_count', 0)}

## ✨ Features

{self._generate_features_section(repo_info, technologies)}

## 🛠️ Technology Stack

{self._generate_technology_stack_section(file_structure, technologies)}

## 📋 Prerequisites

{self._generate_prerequisites_section(technologies)}

## 🚀 Installation

{self._generate_installation_section(technologies)}

## 💻 Usage

{self._generate_usage_section(technologies)}

## 📚 API Documentation

{self._generate_api_section(technologies)}

## 📁 Project Structure

```
{project_name}/
{self._generate_project_structure_tree(file_structure)}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

{self._generate_license_section(repo_info)}

## 🆘 Support

If you encounter any problems or have questions, please:

- Check the [documentation](docs/)
- Search [existing issues]({repo_info.get('html_url', '')}/issues)
- Create a [new issue]({repo_info.get('html_url', '')}/issues/new)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped build this project
- Built with modern development practices and tools

---

Made with ❤️ by the {project_name} team
"""
        return readme_content
    
    def _generate_features_section(self, repo_info: Dict, technologies: Dict) -> str:
        """Generate features section based on detected technologies"""
        features = []
        
        frameworks = technologies.get('frameworks', [])
        if 'Python' in frameworks:
            features.append("- 🐍 **Python-based** - Built with Python for reliability and performance")
        if 'Node.js' in frameworks:
            features.append("- 🟢 **Node.js** - Fast and scalable JavaScript runtime")
        if 'React' in str(technologies):
            features.append("- ⚛️ **React** - Modern user interface framework")
        
        if technologies.get('deployment'):
            features.append("- 🐳 **Containerized** - Docker support for easy deployment")
        
        features.append("- 📖 **Well Documented** - Comprehensive documentation and examples")
        features.append("- 🧪 **Tested** - Automated testing for reliability")
        features.append("- 🔧 **Configurable** - Flexible configuration options")
        
        return "\n".join(features) if features else "- Feature documentation coming soon"
    
    def _generate_technology_stack_section(self, file_structure: Dict, technologies: Dict) -> str:
        """Generate technology stack section"""
        languages = file_structure.get('languages', {})
        frameworks = technologies.get('frameworks', [])
        databases = technologies.get('databases', [])
        deployment = technologies.get('deployment', [])
        
        stack_content = ""
        
        if languages:
            stack_content += "### Languages\n"
            for lang, count in languages.items():
                stack_content += f"- **{lang}**\n"
            stack_content += "\n"
        
        if frameworks:
            stack_content += "### Frameworks & Libraries\n"
            for framework in frameworks:
                stack_content += f"- {framework}\n"
            stack_content += "\n"
        
        if databases:
            stack_content += "### Databases\n"
            for db in databases:
                stack_content += f"- {db}\n"
            stack_content += "\n"
        
        if deployment:
            stack_content += "### Deployment & DevOps\n"
            for tool in deployment:
                stack_content += f"- {tool}\n"
            stack_content += "\n"
        
        return stack_content or "Technology stack information will be updated soon."
    
    def _generate_prerequisites_section(self, technologies: Dict) -> str:
        """Generate prerequisites section"""
        prereqs = []
        
        frameworks = technologies.get('frameworks', [])
        if 'Python' in frameworks:
            prereqs.append("- Python 3.8 or higher")
            prereqs.append("- pip (Python package manager)")
        if 'Node.js' in frameworks:
            prereqs.append("- Node.js 16 or higher")
            prereqs.append("- npm or yarn")
        
        if 'Docker' in technologies.get('deployment', []):
            prereqs.append("- Docker")
            if 'Docker Compose' in technologies.get('deployment', []):
                prereqs.append("- Docker Compose")
        
        prereqs.append("- Git")
        
        return "\n".join(prereqs) if prereqs else "- No specific prerequisites required"
    
    def _generate_installation_section(self, technologies: Dict) -> str:
        """Generate installation instructions"""
        frameworks = technologies.get('frameworks', [])
        
        installation = "### Quick Start\n\n"
        
        if 'Python' in frameworks:
            installation += """```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

"""
        
        if 'Node.js' in frameworks:
            installation += """```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
npm install

# Start development server
npm start
```

"""
        
        if 'Docker' in technologies.get('deployment', []):
            installation += """### Using Docker

```bash
# Build and run with Docker
docker build -t project-name .
docker run -p 8000:8000 project-name
```

"""
            
            if 'Docker Compose' in technologies.get('deployment', []):
                installation += """```bash
# Or use Docker Compose
docker-compose up --build
```

"""
        
        return installation
    
    def _generate_usage_section(self, technologies: Dict) -> str:
        """Generate usage instructions"""
        return """### Basic Usage

```bash
# Example usage commands will be documented here
# Add specific examples based on your project
```

### Configuration

Configuration options can be set through environment variables or configuration files.

### Examples

More detailed examples and tutorials coming soon!
"""
    
    def _generate_api_section(self, technologies: Dict) -> str:
        """Generate API documentation section"""
        frameworks = technologies.get('frameworks', [])
        
        if any(web_framework in str(technologies) for web_framework in ['Flask', 'Django', 'Express', 'FastAPI']):
            return """### API Endpoints

The application provides the following API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check endpoint |
| GET | `/api/docs` | API documentation |

For detailed API documentation, visit `/api/docs` when the server is running.
"""
        
        return "API documentation will be added when API endpoints are implemented."
    
    def _generate_project_structure_tree(self, file_structure: Dict) -> str:
        """Generate project structure tree"""
        directories = file_structure.get('directories', [])
        files = file_structure.get('files', [])
        
        tree = ""
        for directory in sorted(directories):
            tree += f"├── {directory}/\n"
        
        for file in sorted(files):
            tree += f"├── {file}\n"
        
        return tree or "└── (Project structure will be documented)"
    
    def _generate_license_section(self, repo_info: Dict) -> str:
        """Generate license section"""
        license_name = repo_info.get('license')
        if license_name:
            return f"This project is licensed under the {license_name} License - see the [LICENSE](LICENSE) file for details."
        return "License information not available. Please check the repository for license details."
    
    def _generate_api_documentation(self, repo_info: Dict, technologies: Dict) -> str:
        """Generate detailed API documentation"""
        return f"""# API Documentation

## Overview

This document provides detailed information about the {repo_info.get('name', 'Project')} API.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Authentication details will be documented here.

## Endpoints

### Health Check

```http
GET /health
```

Returns the health status of the API.

#### Response

```json
{{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}}
```

## Error Handling

The API uses standard HTTP status codes and returns error responses in the following format:

```json
{{
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}}
```

## Rate Limiting

Rate limiting information will be documented here.
"""
    
    def _generate_setup_guide(self, repo_info: Dict, technologies: Dict) -> str:
        """Generate setup guide"""
        return f"""# Setup Guide

## Development Environment Setup

### System Requirements

{self._generate_prerequisites_section(technologies)}

### Step-by-Step Setup

{self._generate_installation_section(technologies)}

### Environment Variables

Create a `.env` file in the project root:

```env
# Add your environment variables here
DEBUG=true
PORT=8000
```

### Development Tools

Recommended development tools:
- IDE: VS Code, PyCharm, or your preferred editor
- Version Control: Git
- API Testing: Postman or curl

### Troubleshooting

Common setup issues and solutions will be documented here.
"""
    
    def _generate_architecture_docs(self, repo_info: Dict, technologies: Dict) -> str:
        """Generate architecture documentation"""
        return f"""# Architecture Documentation

## System Overview

{repo_info.get('description', 'System architecture documentation')}

## High-Level Architecture

```
[Client] <-> [API Gateway] <-> [Application Layer] <-> [Data Layer]
```

## Components

### Application Layer
- Core business logic
- API endpoints
- Request/response handling

### Data Layer
- Database interactions
- Data models
- Caching layer

## Design Patterns

Architecture patterns and design decisions will be documented here.

## Scalability Considerations

Scalability features and considerations will be documented here.
"""
    
    def _generate_contributing_guide(self, repo_info: Dict) -> str:
        """Generate contributing guide"""
        return f"""# Contributing to {repo_info.get('name', 'Project')}

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Process

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- Use the issue tracker to report bugs
- Include a clear description and steps to reproduce
- Add relevant labels and screenshots if applicable

### Suggesting Enhancements

- Use the issue tracker to suggest enhancements
- Provide a clear description of the enhancement
- Explain why this enhancement would be useful

### Pull Requests

- Fill in the required template
- Include appropriate tests
- Update documentation as needed

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less

### Code Style

- Follow the existing code style
- Run linters and formatters before submitting
- Add comments for complex logic

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain test coverage

## Documentation

- Update README if needed
- Add docstrings for new functions/classes
- Update API documentation for new endpoints
"""
    
    def _generate_changelog_template(self, repo_info: Dict) -> str:
        """Generate changelog template"""
        return f"""# Changelog

All notable changes to {repo_info.get('name', 'this project')} will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features will be listed here

### Changed
- Changes to existing functionality will be listed here

### Deprecated
- Soon-to-be removed features will be listed here

### Removed
- Removed features will be listed here

### Fixed
- Bug fixes will be listed here

### Security
- Security fixes will be listed here

## [1.0.0] - {datetime.now().strftime('%Y-%m-%d')}

### Added
- Initial release
- Basic project structure
- Core functionality

---

## Template for new releases:

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes
"""
    
    def _generate_license_file(self, repo_info: Dict) -> str:
        """Generate LICENSE file"""
        license_name = repo_info.get('license', 'MIT')
        current_year = datetime.now().year
        
        if license_name == 'MIT':
            return f"""MIT License

Copyright (c) {current_year} {repo_info.get('name', 'Project')}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        
        return f"""# License

This project is licensed under the {license_name} License.

Please refer to the original repository for full license details.
"""
    
    def _generate_gitignore(self, technologies: Dict) -> str:
        """Generate .gitignore file"""
        frameworks = technologies.get('frameworks', [])
        gitignore_content = "# Generated .gitignore\n\n"
        
        if 'Python' in frameworks:
            gitignore_content += """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

"""
        
        if 'Node.js' in frameworks:
            gitignore_content += """# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.eslintcache

"""
        
        gitignore_content += """# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local
.env.*.local

# Logs
logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity
"""
        
        return gitignore_content
    
    def _generate_dockerfile(self, technologies: Dict) -> str:
        """Generate Dockerfile"""
        frameworks = technologies.get('frameworks', [])
        
        if 'Python' in frameworks:
            return """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]
"""
        
        if 'Node.js' in frameworks:
            return """FROM node:16-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
"""
        
        return """FROM alpine:latest

WORKDIR /app

# Add application code
COPY . .

# Expose port
EXPOSE 8000

# Run command
CMD ["echo", "Configure Dockerfile for your specific application"]
"""
    
    def _generate_github_actions(self, technologies: Dict) -> str:
        """Generate GitHub Actions workflow"""
        frameworks = technologies.get('frameworks', [])
        
        workflow = """name: CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
"""
        
        if 'Python' in frameworks:
            workflow += """  test-python:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Run linter
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

"""
        
        if 'Node.js' in frameworks:
            workflow += """  test-node:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]

    steps:
    - uses: actions/checkout@v3
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - run: npm ci
    - run: npm run build --if-present
    - run: npm test

"""
        
        workflow += """  docker-build:
    runs-on: ubuntu-latest
    needs: [test-python]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t project-name .
    
    - name: Test Docker image
      run: docker run --rm project-name echo "Docker build successful"
"""
        
        return workflow
    
    def _generate_deployment_guide(self, technologies: Dict) -> str:
        """Generate deployment guide"""
        return """# Deployment Guide

## Overview

This guide covers various deployment options for the application.

## Local Development

```bash
# Start the application locally
npm start  # or python main.py
```

## Production Deployment

### Using Docker

```bash
# Build the image
docker build -t app-name .

# Run the container
docker run -p 8000:8000 app-name
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d
```

### Cloud Deployment

#### AWS
- EC2 instances
- ECS/Fargate
- Lambda (for serverless)

#### Google Cloud
- Compute Engine
- Cloud Run
- App Engine

#### Azure
- Virtual Machines
- Container Instances
- App Service

## Environment Configuration

Set the following environment variables for production:

```env
NODE_ENV=production
DATABASE_URL=your-database-url
API_KEY=your-api-key
```

## Monitoring and Logging

- Set up application monitoring
- Configure log aggregation
- Set up alerting for critical errors

## Security Considerations

- Use HTTPS in production
- Secure API endpoints
- Validate all inputs
- Keep dependencies updated
"""
    
    def _generate_troubleshooting_guide(self, technologies: Dict) -> str:
        """Generate troubleshooting guide"""
        return """# Troubleshooting Guide

## Common Issues

### Installation Issues

#### Issue: Dependencies not installing
```bash
# Clear package cache
npm cache clean --force
# or for Python
pip cache purge
```

#### Issue: Permission denied
```bash
# Use sudo (Linux/Mac) or run as administrator (Windows)
sudo npm install
```

### Runtime Issues

#### Issue: Port already in use
```bash
# Find process using the port
lsof -ti:3000
# Kill the process
kill -9 <PID>
```

#### Issue: Database connection failed
- Check database server is running
- Verify connection string
- Check firewall settings

### Performance Issues

#### Issue: Slow response times
- Check database query performance
- Monitor memory usage
- Review application logs

### Development Issues

#### Issue: Hot reload not working
- Check file watchers
- Restart development server
- Clear browser cache

## Debug Mode

Enable debug mode for detailed error information:

```bash
DEBUG=true npm start
```

## Log Files

Check application logs:
- Development: Console output
- Production: Log files in `/var/log/`

## Getting Help

1. Check the documentation
2. Search existing issues
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Relevant logs
"""

# Repository File Manager
class RepositoryFileManager:
    """Manage repository file generation and packaging"""
    
    def __init__(self):
        self.temp_dir = None
    
    def create_repository_package(self, documentation: Dict[str, Any], repo_info: Dict[str, Any]) -> str:
        """Create a complete repository package as a zip file"""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        repo_name = repo_info.get('name', 'documentation-package')
        repo_path = Path(self.temp_dir) / repo_name
        repo_path.mkdir(exist_ok=True)
        
        try:
            # Create main documentation files
            self._create_file(repo_path / 'README.md', documentation.get('readme', ''))
            self._create_file(repo_path / 'CONTRIBUTING.md', documentation.get('contributing_guide', ''))
            self._create_file(repo_path / 'CHANGELOG.md', documentation.get('changelog', ''))
            self._create_file(repo_path / 'LICENSE', documentation.get('license', ''))
            self._create_file(repo_path / '.gitignore', documentation.get('gitignore', ''))
            self._create_file(repo_path / 'Dockerfile', documentation.get('dockerfile', ''))
            
            # Create docs directory
            docs_path = repo_path / 'docs'
            docs_path.mkdir(exist_ok=True)
            
            self._create_file(docs_path / 'api.md', documentation.get('api_docs', ''))
            self._create_file(docs_path / 'setup.md', documentation.get('setup_guide', ''))
            self._create_file(docs_path / 'architecture.md', documentation.get('architecture_docs', ''))
            
            # Create additional files
            additional_files = documentation.get('additional_files', {})
            for file_path, content in additional_files.items():
                full_path = repo_path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                self._create_file(full_path, content)
            
            # Create .github directory
            github_path = repo_path / '.github'
            github_path.mkdir(exist_ok=True)
            
            workflows_path = github_path / 'workflows'
            workflows_path.mkdir(exist_ok=True)
            
            # Create package info file
            package_info = {
                'package_name': repo_name,
                'generated_at': datetime.utcnow().isoformat(),
                'generator': 'Documentation.AI v2.0.0',
                'repository_info': repo_info,
                'files_included': self._get_file_list(repo_path)
            }
            
            self._create_file(repo_path / 'package-info.json', json.dumps(package_info, indent=2))
            
            # Create zip file
            zip_path = Path(self.temp_dir) / f"{repo_name}-documentation.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in repo_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(self.temp_dir)
                        zipf.write(file_path, arcname)
            
            return str(zip_path)
            
        except Exception as e:
            logger.error(f"Error creating repository package: {e}")
            raise
    
    def _create_file(self, file_path: Path, content: str):
        """Create a file with the given content"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {e}")
    
    def _get_file_list(self, repo_path: Path) -> List[str]:
        """Get list of all files in the repository package"""
        files = []
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                files.append(str(file_path.relative_to(repo_path)))
        return sorted(files)
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

# Initialize components with better error handling
try:
    # Check if GitHubAnalyzerModel was successfully imported
    if 'GitHubAnalyzerModel' in locals() or 'GitHubAnalyzerModel' in globals():
        github_analyzer = GitHubAnalyzerModel()
    else:
        github_analyzer = GitHubAnalyzer()
    logger.info("✅ GitHubAnalyzer initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize GitHubAnalyzer: {e}")
    logger.error(traceback.format_exc())
    # Create a fallback class
    class FallbackGitHubAnalyzer:
        def parse_github_url(self, repo_url: str) -> Dict[str, str]:
            raise Exception(f"GitHubAnalyzer initialization failed: {e}")
        def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
            raise Exception(f"GitHubAnalyzer initialization failed: {e}")
    github_analyzer = FallbackGitHubAnalyzer()

try:
    doc_generator = DocumentationGeneratorModel() if 'DocumentationGeneratorModel' in globals() else DocumentationGenerator()
    logger.info("✅ DocumentationGenerator initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize DocumentationGenerator: {e}")
    logger.error(traceback.format_exc())
    # Create a fallback class
    class FallbackDocumentationGenerator:
        def generate_documentation(self, analysis_result: Dict[str, Any], rag_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            raise Exception(f"DocumentationGenerator initialization failed: {e}")
    doc_generator = FallbackDocumentationGenerator()

try:
    rag_pipeline = RAGPipelineModel() if 'RAGPipelineModel' in globals() else RAGPipeline()
    logger.info("✅ RAGPipeline initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize RAGPipeline: {e}")
    logger.error(traceback.format_exc())
    # Create a fallback class
    class FallbackRAGPipeline:
        def process(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
            raise Exception(f"RAGPipeline initialization failed: {e}")
    rag_pipeline = FallbackRAGPipeline()

file_manager = RepositoryFileManager()
logger.info("✅ RepositoryFileManager initialized successfully")

# Routes
@app.route('/')
def index():
    """Home route"""
    return jsonify({
        'name': 'Documentation.AI API',
        'version': '2.0.0',
        'description': 'AI-powered documentation generator for GitHub repositories',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'analyze': '/api/analyze',
            'job_status': '/api/job/<id>',
            'jobs': '/api/jobs',
            'download': '/api/download/<id>'
        }
    })

@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests"""
    return '', 204  # No Content

# Handle malformed API URLs with double slashes
@app.route('/api//<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_double_slash_api(path):
    """Redirect malformed API URLs with double slashes"""
    logger.warning(f"Received malformed API URL with double slash: /api//{path}")
    
    # For analyze endpoint, handle directly instead of redirecting
    if path == 'analyze':
        if request.method == 'GET':
            return jsonify({
                'message': 'Repository analysis endpoint',
                'method': 'POST',
                'required_fields': ['repo_url'],
                'description': 'Submit a GitHub repository URL to generate AI documentation',
                'example': {
                    'repo_url': 'https://github.com/owner/repository'
                },
                'note': 'URL was corrected from double slash'
            })
        elif request.method == 'POST':
            # Forward to the actual analyze function
            return analyze_repository()
    
    # For other endpoints, redirect to the corrected URL
    corrected_url = f"/api/{path}"
    logger.info(f"Redirecting to: {corrected_url}")
    from flask import redirect
    return redirect(corrected_url)

@app.route('/api/health')
def health_check():
    """Enhanced health check endpoint with detailed system status"""
    try:
        # Test database connection
        db_status = "healthy"
        db_error = None
        try:
            with db.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
        except Exception as e:
            db_status = "unhealthy"
            db_error = str(e)
        
        # Check AI models status
        github_analyzer_status = "healthy" if not hasattr(github_analyzer, '__class__') or 'Fallback' not in github_analyzer.__class__.__name__ else "unhealthy"
        doc_generator_status = "healthy" if not hasattr(doc_generator, '__class__') or 'Fallback' not in doc_generator.__class__.__name__ else "unhealthy"
        rag_pipeline_status = "healthy" if not hasattr(rag_pipeline, '__class__') or 'Fallback' not in rag_pipeline.__class__.__name__ else "unhealthy"
        
        # Environment variables check
        env_vars = {
            'GITHUB_TOKEN': '✅ Set' if os.getenv('GITHUB_TOKEN') else '❌ Missing',
            'GEMINI_API_KEY': '✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Missing',
            'SECRET_KEY': '✅ Set' if os.getenv('SECRET_KEY') else '❌ Using default'
        }
        
        # Overall status
        overall_status = "healthy" if all([
            db_status == "healthy",
            github_analyzer_status == "healthy",
            doc_generator_status == "healthy"
        ]) else "degraded"
        
        return jsonify({
            'status': overall_status,
            'timestamp': datetime.utcnow().isoformat(),
            'version': '2.0.0',
            'services': {
                'database': {
                    'status': db_status,
                    'error': db_error
                },
                'github_analyzer': {
                    'status': github_analyzer_status,
                    'class': type(github_analyzer).__name__
                },
                'documentation_generator': {
                    'status': doc_generator_status,
                    'class': type(doc_generator).__name__
                },
                'rag_pipeline': {
                    'status': rag_pipeline_status,
                    'class': type(rag_pipeline).__name__
                },
                'file_manager': {
                    'status': 'healthy',
                    'class': type(file_manager).__name__
                }
            },
            'environment': env_vars,
            'endpoints': {
                'health': '/api/health',
                'analyze': '/api/analyze',
                'jobs': '/api/jobs',
                'job_status': '/api/job/<id>',
                'download': '/api/download/<id>'
            }
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'critical',
            'error': str(e),
            'error_type': type(e).__name__,
            'traceback': traceback.format_exc().split('\n')
        }), 500

@app.route('/api/analyze', methods=['GET', 'POST'])
@app.route('/api/analyze/', methods=['GET', 'POST'])
def analyze_repository():
    """Handle repository analysis requests"""
    if request.method == 'GET':
        # Return information about the endpoint
        return jsonify({
            'message': 'Repository analysis endpoint',
            'method': 'POST',
            'required_fields': ['repo_url'],
            'description': 'Submit a GitHub repository URL to generate AI documentation',
            'example': {
                'repo_url': 'https://github.com/owner/repository'
            }
        })
    
    # Handle POST request for actual analysis
    job = None
    try:
        logger.info("=== Starting repository analysis ===")
        
        # Check if AI models are available
        if hasattr(github_analyzer, '__class__') and 'Fallback' in github_analyzer.__class__.__name__:
            error_msg = "AI models failed to initialize. Check backend logs for details."
            logger.error(error_msg)
            return jsonify({
                'error': error_msg,
                'error_type': 'InitializationError',
                'debug_info': {
                    'traceback': ['AI models initialization failed during startup']
                }
            }), 500
        
        # Validate request
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        logger.debug(f"Request data: {data}")
        
        repo_url = data.get('repo_url', '').strip()
        
        if not repo_url:
            logger.error("Repository URL is missing")
            return jsonify({'error': 'Repository URL is required'}), 400
        
        logger.info(f"Processing repository URL: {repo_url}")
        
        # Parse repository URL
        try:
            parsed = github_analyzer.parse_github_url(repo_url)
            owner, repo = parsed['owner'], parsed['repo']
            logger.info(f"Parsed repository: {owner}/{repo}")
        except ValueError as e:
            logger.error(f"Failed to parse repository URL: {e}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error parsing URL: {e}")
            logger.error(traceback.format_exc())
            return jsonify({'error': f'Failed to parse repository URL: {str(e)}'}), 400
        
        # Create analysis job
        try:
            logger.info("Creating analysis job in database")
            job = AnalysisJob(
                repo_url=repo_url,
                repo_name=repo,
                repo_owner=owner,
                status='processing'
            )
            db.session.add(job)
            db.session.commit()
            logger.info(f"Created job with ID: {job.id}")
        except Exception as e:
            logger.error(f"Failed to create analysis job: {e}")
            logger.error(traceback.format_exc())
            return jsonify({
                'error': f'Failed to create analysis job: {str(e)}',
                'error_type': 'DatabaseError',
                'debug_info': {
                    'traceback': traceback.format_exc().split('\n')
                }
            }), 500
        
        logger.info(f"Starting analysis for repository: {repo_url} (Job ID: {job.id})")
        
        # Step 1: Analyze repository
        try:
            logger.info("Step 1: Analyzing repository")
            analysis_result = github_analyzer.analyze_repository(repo_url)
            logger.info("Repository analysis completed successfully")
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            logger.error(traceback.format_exc())
            job.status = 'failed'
            job.error_message = f"Repository analysis failed: {str(e)}"
            db.session.commit()
            return jsonify({
                'error': f'Repository analysis failed: {str(e)}',
                'error_type': 'RepositoryAnalysisError',
                'job_id': job.id,
                'debug_info': {
                    'traceback': traceback.format_exc().split('\n')
                }
            }), 500
        
        # Step 2: Process with RAG pipeline
        try:
            logger.info("Step 2: Processing with RAG pipeline")
            rag_result = rag_pipeline.process_repository(analysis_result)
            logger.info("RAG pipeline processing completed successfully")
        except Exception as e:
            logger.error(f"RAG pipeline processing failed: {e}")
            logger.error(traceback.format_exc())
            # Continue with empty rag_result as fallback
            rag_result = {
                'processing_status': 'failed',
                'error': str(e),
                'semantic_insights': [],
                'code_patterns': [],
                'knowledge_graph': {},
                'document_count': 0,
                'embedding_dimension': 0
            }
        
        # Step 3: Generate documentation
        try:
            logger.info("Step 3: Generating documentation")
            documentation = doc_generator.generate_documentation(analysis_result, rag_result)
            logger.info("Documentation generation completed successfully")
        except Exception as e:
            logger.error(f"Documentation generation failed: {e}")
            logger.error(traceback.format_exc())
            job.status = 'failed'
            job.error_message = f"Documentation generation failed: {str(e)}"
            db.session.commit()
            return jsonify({
                'error': f'Documentation generation failed: {str(e)}',
                'error_type': 'DocumentationGenerationError',
                'job_id': job.id,
                'debug_info': {
                    'traceback': traceback.format_exc().split('\n')
                }
            }), 500
        
        # Step 3: Create repository package
        try:
            logger.info("Step 3: Creating repository package")
            package_path = file_manager.create_repository_package(
                documentation, 
                analysis_result['repository_info']
            )
            logger.info(f"Repository package created: {package_path}")
        except Exception as e:
            logger.error(f"Package creation failed: {e}")
            logger.error(traceback.format_exc())
            job.status = 'failed'
            job.error_message = f"Package creation failed: {str(e)}"
            db.session.commit()
            return jsonify({
                'error': f'Package creation failed: {str(e)}',
                'error_type': 'PackageCreationError',
                'job_id': job.id,
                'debug_info': {
                    'traceback': traceback.format_exc().split('\n')
                }
            }), 500
        
        # Update job with results
        try:
            logger.info("Updating job with results")
            result_data = {
                'analysis': analysis_result,
                'documentation': documentation,
                'package_path': package_path,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            job.status = 'completed'
            job.result = json.dumps(result_data)
            db.session.commit()
            logger.info(f"Analysis completed successfully for job {job.id}")
        except Exception as e:
            logger.error(f"Failed to update job results: {e}")
            logger.error(traceback.format_exc())
            return jsonify({
                'error': f'Failed to save results: {str(e)}',
                'error_type': 'DatabaseSaveError',
                'job_id': job.id,
                'debug_info': {
                    'traceback': traceback.format_exc().split('\n')
                }
            }), 500
        
        return jsonify({
            'job_id': job.id,
            'status': 'completed',
            'message': 'Documentation generated successfully',
            'repository': {
                'name': repo,
                'owner': owner,
                'url': repo_url
            },
            'download_url': f'/api/download/{job.id}',
            'result': {
                'readme_preview': documentation.get('readme', '')[:500] + '...' if len(documentation.get('readme', '')) > 500 else documentation.get('readme', ''),
                'files_generated': len(documentation) + len(documentation.get('additional_files', {}))
            }
        })
        
    except Exception as e:
        error_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        logger.error(f"CRITICAL ERROR [{error_id}]: Unhandled exception in analyze_repository")
        logger.error(f"Error Type: {type(e).__name__}")
        logger.error(f"Error Message: {str(e)}")
        logger.error(f"Full Traceback:\n{traceback.format_exc()}")
        
        # Update job status to failed
        if job:
            try:
                job.status = 'failed'
                job.error_message = f"Critical error [{error_id}]: {str(e)}"
                db.session.commit()
                logger.info(f"Updated job {job.id} status to failed")
            except Exception as db_error:
                logger.error(f"Failed to update job status: {db_error}")
                logger.error(traceback.format_exc())
        
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
            'error_id': error_id,
            'error_type': type(e).__name__,
            'job_id': job.id if job else None,
            'debug_info': {
                'traceback': traceback.format_exc().split('\n'),
                'request_data': request.get_json(silent=True) if request.is_json else None,
                'github_analyzer_type': type(github_analyzer).__name__,
                'doc_generator_type': type(doc_generator).__name__
            }
        }), 500

@app.route('/api/job/<int:job_id>')
def get_job_status(job_id):
    """Get the status of an analysis job"""
    try:
        job = AnalysisJob.query.get_or_404(job_id)
        
        response_data = {
            'job_id': job.id,
            'repo_url': job.repo_url,
            'repo_name': job.repo_name,
            'repo_owner': job.repo_owner,
            'status': job.status,
            'created_at': job.created_at.isoformat(),
            'updated_at': job.updated_at.isoformat()
        }
        
        if job.status == 'completed' and job.result:
            try:
                result_data = json.loads(job.result)
                response_data['download_url'] = f'/api/download/{job.id}'
                response_data['documentation'] = result_data.get('documentation', {})
                response_data['analysis'] = result_data.get('analysis', {})
            except json.JSONDecodeError:
                logger.error(f"Failed to parse result for job {job.id}")
        
        if job.status == 'failed' and job.error_message:
            response_data['error_message'] = job.error_message
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error fetching job status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs')
def get_all_jobs():
    """Get all analysis jobs with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        jobs = AnalysisJob.query.order_by(AnalysisJob.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'jobs': [{
                'job_id': job.id,
                'repo_url': job.repo_url,
                'repo_name': job.repo_name,
                'repo_owner': job.repo_owner,
                'status': job.status,
                'created_at': job.created_at.isoformat(),
                'download_url': f'/api/download/{job.id}' if job.status == 'completed' else None
            } for job in jobs.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': jobs.total,
                'pages': jobs.pages,
                'has_next': jobs.has_next,
                'has_prev': jobs.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<int:job_id>')
def download_documentation(job_id):
    """Download the generated documentation package"""
    try:
        job = AnalysisJob.query.get_or_404(job_id)
        
        if job.status != 'completed':
            return jsonify({'error': 'Job not completed'}), 400
        
        if not job.result:
            return jsonify({'error': 'No result available'}), 404
        
        try:
            result_data = json.loads(job.result)
            package_path = result_data.get('package_path')
            
            if not package_path or not Path(package_path).exists():
                return jsonify({'error': 'Package file not found'}), 404
            
            return send_file(
                package_path,
                as_attachment=True,
                download_name=f"{job.repo_name}-documentation.zip",
                mimetype='application/zip'
            )
            
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid result data'}), 500
        
    except Exception as e:
        logger.error(f"Error downloading documentation: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(Exception)
def handle_all_exceptions(error):
    """Handle all unhandled exceptions with detailed error information"""
    error_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    
    # Log the full error details
    logger.error(f"ERROR_ID: {error_id}")
    logger.error(f"Exception Type: {type(error).__name__}")
    logger.error(f"Exception Message: {str(error)}")
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request Method: {request.method}")
    logger.error(f"Request Headers: {dict(request.headers)}")
    if request.is_json:
        logger.error(f"Request JSON: {request.get_json(silent=True)}")
    logger.error(f"Full Traceback:\n{traceback.format_exc()}")
    
    # Return detailed error response
    error_response = {
        'error': 'Internal server error',
        'error_id': error_id,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'timestamp': datetime.utcnow().isoformat(),
        'request_info': {
            'url': request.url,
            'method': request.method,
            'endpoint': request.endpoint
        }
    }
    
    # Add debug information in development
    if app.debug:
        error_response['debug_info'] = {
            'traceback': traceback.format_exc().split('\n'),
            'request_data': request.get_json(silent=True) if request.is_json else None,
            'request_args': dict(request.args),
            'request_form': dict(request.form)
        }
    
    return jsonify(error_response), 500

@app.before_request
def log_request_info():
    """Log detailed request information"""
    logger.debug(f"Request: {request.method} {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    if request.is_json:
        logger.debug(f"JSON Data: {request.get_json(silent=True)}")
    if request.form:
        logger.debug(f"Form Data: {dict(request.form)}")
    if request.args:
        logger.debug(f"Query Args: {dict(request.args)}")

@app.after_request
def log_response_info(response):
    """Log response information"""
    logger.debug(f"Response Status: {response.status_code}")
    logger.debug(f"Response Headers: {dict(response.headers)}")
    return response

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested resource does not exist',
        'available_endpoints': [
            '/api/health',
            '/api/analyze',
            '/api/job/<id>',
            '/api/jobs',
            '/api/download/<id>'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred on the server'
    }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    return jsonify({
        'error': 'File too large',
        'message': 'The uploaded file exceeds the maximum allowed size'
    }), 413

# Initialize database
def init_db():
    """Initialize the database with detailed error handling"""
    try:
        with app.app_context():
            logger.info("Initializing database...")
            
            # Check if database file exists and is accessible
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            logger.info(f"Database path: {db_path}")
            
            # Create instance directory if it doesn't exist
            instance_dir = Path('instance')
            instance_dir.mkdir(exist_ok=True)
            logger.info(f"Instance directory: {instance_dir.absolute()}")
            
            # Test database connection
            try:
                with db.engine.connect() as connection:
                    connection.execute(text('SELECT 1'))
                logger.info("Database connection test successful")
            except Exception as e:
                logger.warning(f"Database connection test failed, will create tables: {e}")
            
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Test table creation
            try:
                job_count = AnalysisJob.query.count()
                logger.info(f"Database verification successful. Found {job_count} existing jobs.")
            except Exception as e:
                logger.error(f"Database verification failed: {e}")
                raise
                
            logger.info("Database initialization completed successfully")
            
    except Exception as e:
        logger.error(f"Critical error during database initialization: {e}")
        logger.error(traceback.format_exc())
        raise

def check_dependencies():
    """Check if all required dependencies and services are available"""
    logger.info("=== Checking Dependencies ===")
    
    # Check environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token:
        logger.info("✓ GitHub token found")
    else:
        logger.warning("⚠ GitHub token not found - API rate limits may apply")
    
    # Check database
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
            logger.info("✓ Database connection successful")
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        raise
    
    # Check write permissions for temp directory
    try:
        temp_test_dir = tempfile.mkdtemp()
        test_file = Path(temp_test_dir) / 'test.txt'
        test_file.write_text('test')
        test_file.unlink()
        Path(temp_test_dir).rmdir()
        logger.info("✓ Temporary directory write permissions OK")
    except Exception as e:
        logger.error(f"✗ Temporary directory write test failed: {e}")
        raise
    
    logger.info("=== All dependency checks passed ===")

if __name__ == '__main__':
    try:
        # Initialize database
        init_db()
        
        # Check dependencies
        check_dependencies()
        
        # Configuration
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        
        logger.info(f"🚀 Starting Documentation.AI Backend Server")
        logger.info(f"📍 Server: http://{host}:{port}")
        logger.info(f"🐛 Debug mode: {debug}")
        logger.info(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
        logger.info(f"🔧 Working directory: {Path.cwd()}")
        logger.info(f"📁 Instance directory: {Path('instance').absolute()}")
        
        # Start the Flask application
        app.run(host=host, port=port, debug=debug, threaded=True)
        
    except Exception as e:
        logger.error(f"CRITICAL: Failed to start application: {e}")
        logger.error(traceback.format_exc())
        raise
