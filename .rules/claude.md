# Claude AI Rules for Documentation.AI

## Project Context & Architecture

### System Overview
Documentation.AI is a Flask-based backend with React frontend that generates documentation for GitHub repositories using AI models. The system architecture emphasizes modularity, error resilience, and maintainability.

## Development Guidelines for Claude

### 1. File Organization Rules

**ALWAYS follow these directory conventions:**

- **Tests**: All test files MUST go in `/tests/` directory
  - Python tests: `test_*.py` format
  - Follow pytest conventions
  - Mirror the structure of the main codebase

- **Scripts**: All shell scripts MUST go in `/scripts/` directory
  - Naming: `kebab-case.sh`
  - Include proper error handling and logging
  - Make scripts executable with `chmod +x`

- **AI Models**: Keep in `/ai_models/` directory
  - Each model in separate file
  - Use lazy loading patterns
  - Include health check methods

- **Utilities**: Place helper functions in `/utils/` directory
  - Pure functions when possible
  - Comprehensive error handling
  - Proper type annotations

### 2. Backend Development (Flask)

**Essential Patterns:**

```python
# Route Definition Pattern
@app.route('/api/endpoint', methods=['POST'])
def endpoint_function():
    try:
        logger.info("Starting operation")
        
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        
        # Main logic
        result = process_data(data)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            'error': 'Invalid input',
            'error_type': 'ValidationError',
            'message': str(e)
        }), 400
        
    except Exception as e:
        error_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        logger.error(f"Error [{error_id}]: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error',
            'error_id': error_id,
            'error_type': type(e).__name__,
            'debug_info': {
                'traceback': traceback.format_exc().split('\n')
            }
        }), 500
```

**Database Operations:**

```python
# Always use try-catch for database operations
try:
    with app.app_context():
        job = AnalysisJob(
            repo_url=repo_url,
            status='processing'
        )
        db.session.add(job)
        db.session.commit()
        logger.info(f"Created job with ID: {job.id}")
except Exception as e:
    logger.error(f"Database operation failed: {e}")
    db.session.rollback()
    raise
```

### 3. AI Model Integration

**Lazy Loading Pattern:**

```python
class AIModel:
    def __init__(self):
        self.model = None
        self.api_key = os.getenv('API_KEY')
        
    def _load_model(self):
        if self.model is None and self.api_key:
            try:
                self.model = load_external_model()
                logger.info("Model loaded successfully")
            except Exception as e:
                logger.error(f"Model loading failed: {e}")
                self.model = None
        return self.model
        
    def process(self, data):
        model = self._load_model()
        if not model:
            raise Exception("Model not available")
        return model.process(data)
```

**Fallback Implementation:**

```python
try:
    from ai_models.github_analyzer import GitHubAnalyzer
    analyzer = GitHubAnalyzer()
except ImportError as e:
    logger.error(f"AI model import failed: {e}")
    
    class FallbackAnalyzer:
        def analyze_repository(self, repo_url):
            raise Exception("AI models not available")
    
    analyzer = FallbackAnalyzer()
```

### 4. Frontend Development (React/TypeScript)

**Component Structure:**

```typescript
// Components go in /frontend/src/components/
interface ComponentProps {
    data: DataType;
    onAction: (id: string) => void;
}

const Component: React.FC<ComponentProps> = ({ data, onAction }) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const handleAction = async (id: string) => {
        try {
            setLoading(true);
            setError(null);
            await onAction(id);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    
    if (error) {
        return <ErrorComponent message={error} />;
    }
    
    return (
        <div className="component">
            {/* Component JSX */}
        </div>
    );
};
```

### 5. Testing Requirements

**Test File Structure:**

```
/tests/
├── test_app.py              # Main application tests
├── test_ai_models.py        # AI model tests
├── test_database.py         # Database operation tests
├── test_utils.py            # Utility function tests
├── integration/             # Integration tests
│   ├── test_api_endpoints.py
│   └── test_full_workflow.py
└── fixtures/                # Test data
    ├── sample_repos.json
    └── mock_responses.json
```

**Test Patterns:**

```python
# Always place in /tests/ directory
import pytest
from unittest.mock import Mock, patch
from app import app, db

class TestAPIEndpoints:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()
    
    def test_health_endpoint(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
    
    @patch('ai_models.github_analyzer.GitHubAnalyzer')
    def test_analyze_endpoint(self, mock_analyzer, client):
        mock_analyzer.return_value.analyze_repository.return_value = {}
        
        response = client.post('/api/analyze', json={
            'repo_url': 'https://github.com/test/repo'
        })
        
        assert response.status_code in [200, 202]
```

### 6. Error Handling Standards

**Comprehensive Error Response:**

```python
def create_error_response(error: Exception, status_code: int = 500) -> tuple:
    error_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    
    response = {
        'error': str(error),
        'error_id': error_id,
        'error_type': type(error).__name__,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if app.debug:
        response['debug_info'] = {
            'traceback': traceback.format_exc().split('\n')
        }
    
    return jsonify(response), status_code
```

### 7. Configuration Management

**Environment Variables:**

```python
# Always provide defaults and validation
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///documentation_ai.db')
    PORT = int(os.getenv('PORT', 5000))
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    @classmethod
    def validate(cls):
        if not cls.GITHUB_TOKEN:
            logger.warning("GITHUB_TOKEN not set - GitHub API will be limited")
```

### 8. Shell Script Standards

**Script Template:**

```bash
#!/bin/bash
# Place in /scripts/ directory

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function for logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Error handling
cleanup() {
    log_info "Cleaning up..."
    # Cleanup code here
}

trap cleanup EXIT

# Main script logic
main() {
    log_info "Starting script..."
    
    # Script logic here
    
    log_info "Script completed successfully"
}

main "$@"
```

### 9. Performance Guidelines

**Async Operations:**

```python
from threading import Thread
from queue import Queue

def background_task(job_id: int, repo_url: str):
    try:
        # Update job status
        job = AnalysisJob.query.get(job_id)
        job.status = 'processing'
        db.session.commit()
        
        # Perform analysis
        result = analyzer.analyze_repository(repo_url)
        
        # Update with results
        job.status = 'completed'
        job.result = json.dumps(result)
        db.session.commit()
        
    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        db.session.commit()
        logger.error(f"Background task failed: {e}")

# Start background task
thread = Thread(target=background_task, args=(job.id, repo_url))
thread.start()
```

### 10. Security Considerations

**Input Validation:**

```python
def validate_github_url(url: str) -> bool:
    """Validate GitHub repository URL"""
    pattern = r'^https://github\.com/[\w\-\.]+/[\w\-\.]+/?$'
    return bool(re.match(pattern, url))

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    return re.sub(r'[^\w\-_\.]', '_', filename)
```

### 11. Documentation Standards

**Docstring Format:**

```python
def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
    """
    Analyze a GitHub repository and extract metadata.
    
    Args:
        repo_url: The GitHub repository URL to analyze
        
    Returns:
        Dictionary containing repository analysis results including:
        - repository_info: Basic repo metadata
        - file_structure: File organization analysis
        - technologies: Detected technologies and frameworks
        
    Raises:
        ValueError: If repo_url is invalid
        APIError: If GitHub API request fails
        
    Example:
        >>> analyzer = GitHubAnalyzer()
        >>> result = analyzer.analyze_repository('https://github.com/user/repo')
        >>> print(result['repository_info']['name'])
    """
```

### 12. Monitoring and Logging

**Structured Logging:**

```python
import structlog

logger = structlog.get_logger()

def log_operation(operation: str, **kwargs):
    logger.info(
        "Operation started",
        operation=operation,
        **kwargs
    )
```

## Critical Reminders

1. **ALWAYS** place test files in `/tests/` directory
2. **ALWAYS** place shell scripts in `/scripts/` directory
3. **NEVER** commit sensitive information (API keys, tokens)
4. **ALWAYS** include comprehensive error handling
5. **ALWAYS** use type hints in Python code
6. **ALWAYS** validate user inputs
7. **ALWAYS** include logging for debugging
8. **NEVER** hardcode configuration values
