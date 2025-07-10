import os
import re
import requests
import json
import google.generativeai as genai
from git import Repo
import tempfile
import shutil
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
from datetime import datetime

logger = logging.getLogger(__name__)

class GitHubAnalyzer:
    """Advanced GitHub repository analyzer using Gemini AI"""
    
    def __init__(self):
        """Initialize the GitHub analyzer"""
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            logger.warning("Gemini API key not found. AI analysis will be limited.")
            self.model = None
    
    def check_api_health(self) -> bool:
        """Check if the Gemini API is accessible"""
        try:
            if self.model:
                response = self.model.generate_content("Test connection")
                return True
        except Exception as e:
            logger.error(f"Gemini API health check failed: {e}")
        return False
    
    def parse_github_url(self, repo_url: str) -> Dict[str, str]:
        """Parse GitHub repository URL to extract owner and repo name"""
        # Clean up the URL
        repo_url = repo_url.strip().rstrip('/')
        
        # Handle different GitHub URL formats
        patterns = [
            r'https://github\.com/([^/]+)/([^/]+)',
            r'git@github\.com:([^/]+)/([^/]+)\.git',
            r'github\.com/([^/]+)/([^/]+)'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, repo_url)
            if match:
                return {
                    'owner': match.group(1),
                    'repo': match.group(2).replace('.git', ''),
                    'full_name': f"{match.group(1)}/{match.group(2).replace('.git', '')}"
                }
        
        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")
    
    def get_repository_metadata(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository metadata from GitHub API"""
        url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {}
        
        if self.github_token:
            headers['Authorization'] = f"token {self.github_token}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch repository metadata: {e}")
            return {}
    
    def clone_repository(self, repo_url: str, temp_dir: str) -> str:
        """Clone repository to temporary directory"""
        try:
            logger.info(f"Cloning repository: {repo_url}")
            Repo.clone_from(repo_url, temp_dir)
            return temp_dir
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            raise
    
    def analyze_file_structure(self, repo_path: str) -> Dict[str, Any]:
        """Analyze the file structure of the repository"""
        structure = {
            'total_files': 0,
            'languages': {},
            'directories': [],
            'important_files': [],
            'file_tree': {},
            'workflows': [],
            'configs': []
        }
        
        # Define important files to look for
        important_files = [
            'README.md', 'readme.md', 'README.txt',
            'package.json', 'requirements.txt', 'Pipfile', 'setup.py',
            'Dockerfile', 'docker-compose.yml',
            '.gitignore', 'LICENSE', 'CONTRIBUTING.md',
            'Makefile', 'CMakeLists.txt',
            '.env.example', 'config.yml', 'config.yaml'
        ]
        
        # Define file extensions for language detection
        language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.sass': 'Sass',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.bat': 'Batch',
            '.ps1': 'PowerShell',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.json': 'JSON',
            '.xml': 'XML',
            '.md': 'Markdown'
        }
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common build/cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist', 'target']]
            
            rel_root = os.path.relpath(root, repo_path)
            if rel_root != '.':
                structure['directories'].append(rel_root)
            
            for file in files:
                if file.startswith('.') and file not in ['.env.example', '.gitignore']:
                    continue
                
                structure['total_files'] += 1
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                
                # Check for important files
                if file in important_files:
                    structure['important_files'].append(rel_path)
                
                # Detect programming language
                _, ext = os.path.splitext(file)
                if ext.lower() in language_extensions:
                    lang = language_extensions[ext.lower()]
                    structure['languages'][lang] = structure['languages'].get(lang, 0) + 1
                
                # Check for GitHub workflows
                if '.github/workflows' in rel_path and ext in ['.yml', '.yaml']:
                    structure['workflows'].append(rel_path)
                
                # Check for config files
                if any(config_word in file.lower() for config_word in ['config', 'settings', 'env']):
                    structure['configs'].append(rel_path)
        
        return structure
    
    def analyze_code_content(self, repo_path: str, file_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code content using AI"""
        code_analysis = {
            'main_language': None,
            'frameworks': [],
            'dependencies': [],
            'architecture_patterns': [],
            'code_quality_insights': [],
            'entry_points': [],
            'api_endpoints': [],
            'database_usage': [],
            'testing_frameworks': []
        }
        
        # Determine main language
        if file_structure['languages']:
            code_analysis['main_language'] = max(file_structure['languages'], key=file_structure['languages'].get)
        
        # Analyze key files
        key_files_content = {}
        key_files = ['package.json', 'requirements.txt', 'setup.py', 'Cargo.toml', 'go.mod', 'build.gradle']
        
        for filename in key_files:
            file_path = os.path.join(repo_path, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        key_files_content[filename] = f.read()
                except Exception as e:
                    logger.warning(f"Could not read {filename}: {e}")
        
        # Extract dependencies from key files
        code_analysis['dependencies'] = self._extract_dependencies(key_files_content)
        
        # Analyze main source files
        source_files = self._find_main_source_files(repo_path, file_structure)
        code_analysis.update(self._analyze_source_files(source_files))
        
        # Use AI for advanced analysis if available
        if self.model and key_files_content:
            ai_analysis = self._ai_code_analysis(key_files_content, source_files)
            code_analysis.update(ai_analysis)
        
        return code_analysis
    
    def _extract_dependencies(self, files_content: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract dependencies from various package files"""
        dependencies = []
        
        for filename, content in files_content.items():
            if filename == 'package.json':
                try:
                    package_data = json.loads(content)
                    deps = package_data.get('dependencies', {})
                    dev_deps = package_data.get('devDependencies', {})
                    
                    for dep, version in deps.items():
                        dependencies.append({
                            'name': dep,
                            'version': version,
                            'type': 'production',
                            'ecosystem': 'npm'
                        })
                    
                    for dep, version in dev_deps.items():
                        dependencies.append({
                            'name': dep,
                            'version': version,
                            'type': 'development',
                            'ecosystem': 'npm'
                        })
                except json.JSONDecodeError:
                    pass
            
            elif filename == 'requirements.txt':
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse requirement line
                        dep_match = re.match(r'^([a-zA-Z0-9\-_]+)([>=<!=]+.*)?', line)
                        if dep_match:
                            dependencies.append({
                                'name': dep_match.group(1),
                                'version': dep_match.group(2) or 'latest',
                                'type': 'production',
                                'ecosystem': 'pip'
                            })
        
        return dependencies
    
    def _find_main_source_files(self, repo_path: str, file_structure: Dict[str, Any]) -> List[str]:
        """Find main source files for analysis"""
        main_files = []
        
        # Common entry point files
        entry_points = [
            'main.py', 'app.py', 'server.py', 'index.py',
            'index.js', 'app.js', 'server.js', 'main.js',
            'Main.java', 'Application.java',
            'main.go', 'main.rs', 'main.cpp'
        ]
        
        for entry_point in entry_points:
            file_path = os.path.join(repo_path, entry_point)
            if os.path.exists(file_path):
                main_files.append(file_path)
        
        # Find files in src directories
        for root, dirs, files in os.walk(repo_path):
            if 'src' in os.path.basename(root).lower():
                for file in files[:5]:  # Limit to first 5 files per src directory
                    if any(file.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.go', '.rs']):
                        main_files.append(os.path.join(root, file))
        
        return main_files[:10]  # Limit to 10 files for analysis
    
    def _analyze_source_files(self, source_files: List[str]) -> Dict[str, Any]:
        """Analyze source files for patterns and structure"""
        analysis = {
            'frameworks': [],
            'architecture_patterns': [],
            'api_endpoints': [],
            'database_usage': [],
            'testing_frameworks': []
        }
        
        framework_patterns = {
            'Flask': [r'from flask import', r'Flask\('],
            'Django': [r'from django', r'django\.'],
            'FastAPI': [r'from fastapi import', r'FastAPI\('],
            'Express.js': [r'express\(\)', r'require\([\'"]express[\'\"]\)'],
            'React': [r'import React', r'from [\'"]react[\'"]'],
            'Vue.js': [r'new Vue\(', r'from [\'"]vue[\'"]'],
            'Angular': [r'@Component', r'from [\'"]@angular'],
            'Spring Boot': [r'@SpringBootApplication', r'spring\.boot'],
            'Rails': [r'Rails\.application', r'class.*< ApplicationController']
        }
        
        api_patterns = [
            r'@app\.route\([\'"][^\'\"]*[\'"]',  # Flask routes
            r'app\.(get|post|put|delete)\([\'"][^\'\"]*[\'"]',  # Express routes
            r'@RequestMapping', r'@GetMapping', r'@PostMapping',  # Spring
            r'def (get|post|put|delete)_'  # RESTful methods
        ]
        
        db_patterns = {
            'SQLAlchemy': [r'from sqlalchemy', r'db\.Model'],
            'MongoDB': [r'from pymongo', r'MongoClient'],
            'PostgreSQL': [r'psycopg2', r'postgresql://'],
            'MySQL': [r'mysql', r'MySQLdb'],
            'SQLite': [r'sqlite3', r'\.db']
        }
        
        for file_path in source_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check for frameworks
                for framework, patterns in framework_patterns.items():
                    if any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns):
                        if framework not in analysis['frameworks']:
                            analysis['frameworks'].append(framework)
                
                # Check for API endpoints
                for pattern in api_patterns:
                    matches = re.findall(pattern, content)
                    analysis['api_endpoints'].extend(matches)
                
                # Check for database usage
                for db_type, patterns in db_patterns.items():
                    if any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns):
                        if db_type not in analysis['database_usage']:
                            analysis['database_usage'].append(db_type)
                
            except Exception as e:
                logger.warning(f"Could not analyze file {file_path}: {e}")
        
        return analysis
    
    def _ai_code_analysis(self, files_content: Dict[str, str], source_files: List[str]) -> Dict[str, Any]:
        """Use Gemini AI for advanced code analysis"""
        try:
            # Prepare content for AI analysis
            analysis_prompt = f"""
            Analyze this software project and provide insights about:
            
            1. Architecture patterns used
            2. Code quality observations
            3. Project structure assessment
            4. Technology stack evaluation
            5. Potential improvements
            
            Package files content:
            {json.dumps(files_content, indent=2)}
            
            Please provide a structured analysis in JSON format.
            """
            
            response = self.model.generate_content(analysis_prompt)
            
            # Try to extract JSON from response
            response_text = response.text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            
            if json_match:
                try:
                    ai_insights = json.loads(json_match.group())
                    return {
                        'architecture_patterns': ai_insights.get('architecture_patterns', []),
                        'code_quality_insights': ai_insights.get('code_quality_insights', []),
                        'ai_recommendations': ai_insights.get('recommendations', [])
                    }
                except json.JSONDecodeError:
                    pass
            
            # Fallback: parse free text response
            return {
                'ai_recommendations': [response_text]
            }
            
        except Exception as e:
            logger.error(f"AI code analysis failed: {e}")
            return {}
    
    def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Main method to analyze a GitHub repository"""
        logger.info(f"Starting comprehensive analysis of {repo_url}")
        
        try:
            # Parse repository URL
            repo_info = self.parse_github_url(repo_url)
            
            # Get repository metadata
            metadata = self.get_repository_metadata(repo_info['owner'], repo_info['repo'])
            
            # Clone repository to temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                clone_path = self.clone_repository(repo_url, temp_dir)
                
                # Analyze file structure
                file_structure = self.analyze_file_structure(clone_path)
                
                # Analyze code content
                code_analysis = self.analyze_code_content(clone_path, file_structure)
                
                # Compile final analysis
                analysis_result = {
                    'repository_info': repo_info,
                    'metadata': metadata,
                    'file_structure': file_structure,
                    'code_analysis': code_analysis,
                    'analysis_timestamp': str(datetime.now()),
                    'analyzer_version': '1.0.0'
                }
                
                logger.info("Repository analysis completed successfully")
                return analysis_result
                
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            raise
