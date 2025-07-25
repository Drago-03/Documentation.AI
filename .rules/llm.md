# LLM Rules for Documentation.AI

## Universal LLM Guidelines

This file contains rules and guidelines that apply to ALL language models working on the Documentation.AI codebase, including GPT-4, Claude, Gemini, and any future models.

### Project Overview

Documentation.AI is a Flask-based backend service with React frontend that generates comprehensive documentation for GitHub repositories using AI analysis. The system emphasizes modularity, error resilience, and comprehensive testing.

### Core Principles

1. **Consistency**: Follow established patterns throughout the codebase
2. **Reliability**: Implement comprehensive error handling and fallbacks
3. **Maintainability**: Write clear, well-documented, testable code
4. **Security**: Validate all inputs and sanitize outputs
5. **Performance**: Use async operations and efficient algorithms

## File Organization Rules

### MANDATORY Directory Structure

**These rules are ABSOLUTE and must be followed by ALL LLMs:**

- **`/tests/`** - ALL test files MUST go here
  - Python tests: `test_*.py` naming convention
  - Integration tests: `integration/` subdirectory
  - Test fixtures: `fixtures/` subdirectory
  - Never place tests in source directories

- **`/scripts/`** - ALL shell scripts MUST go here
  - Bash/Zsh scripts: `.sh` extension
  - Windows scripts: `.bat` or `.ps1` extensions
  - Setup scripts: `setup_*.sh` pattern
  - Utility scripts: `run_*.sh` pattern

- **`/ai_models/`** - AI model implementations
  - One model per file
  - Include fallback classes
  - Implement health checks

- **`/utils/`** - Utility functions and helpers
  - Pure functions when possible
  - Comprehensive error handling
  - Proper type annotations

- **`/database/`** - Database models and migrations
  - SQLAlchemy models in `models.py`
  - Database utilities
  - Migration scripts

- **`/frontend/`** - React application
  - Components in `src/components/`
  - Pages in `src/pages/`
  - TypeScript for type safety

## Code Quality Standards

### Python Code Requirements

**Type Annotations:**
```python
def analyze_repository(repo_url: str) -> Dict[str, Any]:
    """Analyze GitHub repository and return metadata."""
```

**Error Handling Pattern:**
```python
try:
    result = risky_operation()
    logger.info("Operation completed successfully")
    return result
except SpecificError as e:
    logger.error(f"Specific error occurred: {e}")
    raise
except Exception as e:
    error_id = generate_error_id()
    logger.error(f"Unexpected error [{error_id}]: {e}")
    logger.error(traceback.format_exc())
    raise
```

**Logging Standards:**
```python
import logging

logger = logging.getLogger(__name__)

# Use structured logging
logger.info("Operation started", extra={
    'operation': 'analyze_repo',
    'repo_url': repo_url,
    'timestamp': datetime.utcnow().isoformat()
})
```

### JavaScript/TypeScript Requirements

**Type Safety:**
```typescript
interface AnalysisResult {
    id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    result?: any;
    error?: string;
}

const processResult = (result: AnalysisResult): void => {
    // Implementation
};
```

**Error Handling:**
```typescript
const apiCall = async (url: string): Promise<ApiResponse> => {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
};
```

### Shell Script Standards

**Script Template:**
```bash
#!/bin/bash
# Description: [What this script does]
# Usage: ./script_name.sh [arguments]

set -e  # Exit on error
set -u  # Exit on undefined variable

# Function definitions first
log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1" >&2
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1" >&2
}

# Error handling
cleanup() {
    log_info "Performing cleanup..."
    # Cleanup code here
}

trap cleanup EXIT

# Main function
main() {
    log_info "Script started"
    
    # Validate prerequisites
    command -v python3 >/dev/null 2>&1 || {
        log_error "Python3 is required but not installed"
        exit 1
    }
    
    # Script logic here
    
    log_info "Script completed successfully"
}

# Execute main function
main "$@"
```

## Testing Requirements

### Test File Organization

```
/tests/
├── test_app.py                    # Main Flask app tests
├── test_ai_models.py             # AI model unit tests
├── test_database_models.py       # Database model tests
├── test_utils.py                 # Utility function tests
├── integration/                  # Integration tests
│   ├── test_api_endpoints.py
│   ├── test_full_workflow.py
│   └── test_github_integration.py
├── fixtures/                     # Test data and mocks
│   ├── sample_repositories.json
│   ├── mock_api_responses.json
│   └── test_files/
└── conftest.py                   # Pytest configuration
```

### Test Writing Standards

**Unit Test Pattern:**
```python
import pytest
from unittest.mock import Mock, patch, MagicMock

class TestGitHubAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return GitHubAnalyzer()
    
    @pytest.fixture
    def mock_github_api(self):
        with patch('github.Github') as mock:
            yield mock
    
    def test_analyze_repository_success(self, analyzer, mock_github_api):
        # Arrange
        mock_repo = Mock()
        mock_repo.name = "test-repo"
        mock_github_api.return_value.get_repo.return_value = mock_repo
        
        # Act
        result = analyzer.analyze_repository("https://github.com/user/repo")
        
        # Assert
        assert result['name'] == "test-repo"
        mock_github_api.return_value.get_repo.assert_called_once()
    
    def test_analyze_repository_invalid_url(self, analyzer):
        with pytest.raises(ValueError, match="Invalid GitHub URL"):
            analyzer.analyze_repository("invalid-url")
```

**Integration Test Pattern:**
```python
class TestAPIIntegration:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()
    
    def test_full_analysis_workflow(self, client):
        # Test the complete workflow from request to response
        response = client.post('/api/analyze', json={
            'repo_url': 'https://github.com/octocat/Hello-World'
        })
        
        assert response.status_code in [200, 202]
        data = response.get_json()
        assert 'job_id' in data
```

## API Design Standards

### RESTful Endpoint Patterns

**Endpoint Structure:**
```
GET    /api/health              # System health check
POST   /api/analyze             # Start repository analysis
GET    /api/jobs/{job_id}       # Get analysis job status
GET    /api/jobs/{job_id}/result # Get analysis results
DELETE /api/jobs/{job_id}       # Cancel/delete job
GET    /api/history            # Get analysis history
```

**Response Format Standards:**
```python
# Success Response
{
    "success": true,
    "data": {
        "job_id": "uuid-string",
        "status": "processing"
    },
    "timestamp": "2024-01-15T10:30:00Z"
}

# Error Response
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid repository URL",
        "error_id": "20240115_103000_123456",
        "details": {
            "field": "repo_url",
            "provided_value": "invalid-url"
        }
    },
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Database Standards

### Model Definition Pattern

```python
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum
from database import db

class AnalysisJob(db.Model):
    """Represents a repository analysis job."""
    
    __tablename__ = 'analysis_jobs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    repo_url = Column(String(500), nullable=False)
    status = Column(Enum('pending', 'processing', 'completed', 'failed'), 
                   default='pending', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    result = Column(Text)  # JSON string
    error_message = Column(Text)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'repo_url': self.repo_url,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': json.loads(self.result) if self.result else None,
            'error_message': self.error_message
        }
```

## Environment Configuration

### Configuration Management

```python
import os
from typing import Optional

class Config:
    """Application configuration with validation."""
    
    # Required settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///documentation_ai.db')
    
    # Optional settings with defaults
    PORT: int = int(os.getenv('PORT', 5002))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # External service configurations
    GITHUB_TOKEN: Optional[str] = os.getenv('GITHUB_TOKEN')
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration and log warnings for missing optional values."""
        warnings = []
        
        if not cls.GITHUB_TOKEN:
            warnings.append("GITHUB_TOKEN not set - GitHub API rate limits will apply")
        
        if not cls.OPENAI_API_KEY:
            warnings.append("OPENAI_API_KEY not set - AI features may not work")
        
        for warning in warnings:
            logger.warning(warning)
```

## Security Guidelines

### Input Validation

```python
import re
from urllib.parse import urlparse

def validate_github_url(url: str) -> bool:
    """Validate GitHub repository URL format."""
    if not url:
        return False
    
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    
    if parsed.netloc != 'github.com':
        return False
    
    # Check path format: /owner/repo
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) != 2:
        return False
    
    # Validate owner and repo names
    for part in path_parts:
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-])*[a-zA-Z0-9]$', part):
            return False
    
    return True

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    # Remove or replace dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    # Limit length
    return sanitized[:255]
```

### Rate Limiting

```python
from functools import wraps
from time import time
from collections import defaultdict

# Simple in-memory rate limiter
rate_limits = defaultdict(list)

def rate_limit(max_requests: int, time_window: int):
    """Rate limiting decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            now = time()
            
            # Clean old requests
            rate_limits[client_ip] = [
                req_time for req_time in rate_limits[client_ip]
                if now - req_time < time_window
            ]
            
            # Check rate limit
            if len(rate_limits[client_ip]) >= max_requests:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': time_window
                }), 429
            
            # Record this request
            rate_limits[client_ip].append(now)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Performance Guidelines

### Async Operations

```python
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import asyncio

class BackgroundJobManager:
    """Manage background processing jobs."""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def submit_job(self, job_id: str, repo_url: str) -> None:
        """Submit a repository analysis job for background processing."""
        future = self.executor.submit(self._process_repository, job_id, repo_url)
        future.add_done_callback(lambda f: self._handle_job_completion(job_id, f))
    
    def _process_repository(self, job_id: str, repo_url: str) -> Dict[str, Any]:
        """Process repository analysis in background thread."""
        try:
            # Update job status
            self._update_job_status(job_id, 'processing')
            
            # Perform analysis
            analyzer = GitHubAnalyzer()
            result = analyzer.analyze_repository(repo_url)
            
            # Save results
            self._save_job_result(job_id, result)
            return result
            
        except Exception as e:
            self._handle_job_error(job_id, e)
            raise
    
    def _update_job_status(self, job_id: str, status: str) -> None:
        """Update job status in database."""
        with app.app_context():
            job = AnalysisJob.query.get(job_id)
            if job:
                job.status = status
                db.session.commit()
```

## Critical Rules Summary

### ABSOLUTE REQUIREMENTS

1. **File Placement:**
   - ALL test files → `/tests/` directory
   - ALL shell scripts → `/scripts/` directory
   - NO exceptions to these rules

2. **Error Handling:**
   - EVERY function must handle exceptions
   - ALWAYS log errors with context
   - ALWAYS provide user-friendly error messages

3. **Type Safety:**
   - USE type hints in Python
   - USE TypeScript for frontend
   - VALIDATE all inputs

4. **Testing:**
   - WRITE tests for all new code
   - MAINTAIN high test coverage
   - USE appropriate test patterns

5. **Security:**
   - VALIDATE all user inputs
   - SANITIZE all outputs
   - NEVER commit secrets

6. **Documentation:**
   - WRITE clear docstrings
   - DOCUMENT complex logic
   - MAINTAIN up-to-date README

### FORBIDDEN PRACTICES

- ❌ Placing test files outside `/tests/` directory
- ❌ Placing scripts outside `/scripts/` directory
- ❌ Hardcoding configuration values
- ❌ Ignoring errors or exceptions
- ❌ Committing sensitive information
- ❌ Writing code without type annotations
- ❌ Deploying without tests
- ❌ Using unsafe file operations
- ❌ Exposing internal errors to users

These rules ensure consistency, reliability, and maintainability across all AI models working on the Documentation.AI codebase.
