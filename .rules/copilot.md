# GitHub Copilot Rules for Documentation.AI

## Development Guidelines

### Code Generation Rules

1. **File Placement**:
   - Place all test files in `/tests/` directory
   - Place shell scripts in `/scripts/` directory
   - Place utility functions in `/utils/` directory
   - Keep AI models in `/ai_models/` directory
   - Main application logic stays in `app.py`

2. **Python Code Standards**:
   - Always include type hints for function parameters and return values
   - Use docstrings for all classes and methods
   - Implement comprehensive error handling with try-catch blocks
   - Add logging statements for debugging and monitoring
   - Follow PEP 8 style guidelines

3. **Flask Backend Rules**:
   - Use blueprint pattern for route organization when adding new features
   - Implement proper CORS configuration
   - Add request validation for all endpoints
   - Include comprehensive error responses with error IDs
   - Use SQLAlchemy models for database operations

4. **React Frontend Rules**:
   - Use TypeScript for all new components
   - Follow React hooks pattern
   - Implement proper error boundaries
   - Use Tailwind CSS for styling
   - Keep components in `/frontend/src/components/`
   - Keep pages in `/frontend/src/pages/`

### Testing Requirements

1. **Test File Naming**:
   - Use `test_*.py` for Python test files
   - Place all tests in `/tests/` directory
   - Create test files for each module in corresponding structure

2. **Test Coverage**:
   - Write unit tests for all utility functions
   - Write integration tests for API endpoints
   - Test error scenarios and edge cases
   - Mock external dependencies (GitHub API, AI models)

### Error Handling Pattern

```python
@app.route('/api/endpoint', methods=['POST'])
def endpoint_function():
    try:
        logger.info("Starting operation")
        # Main logic here
        return jsonify({'success': True})
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            'error': 'Invalid input',
            'error_type': 'ValidationError',
            'message': str(e)
        }), 400
    except Exception as e:
        error_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        logger.error(f"Unexpected error [{error_id}]: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error',
            'error_id': error_id,
            'error_type': type(e).__name__
        }), 500
```

### Database Operations

1. **Model Usage**:
   - Use existing models in `/database/models.py`
   - Always handle database exceptions
   - Use database sessions properly with context managers
   - Include proper validation

2. **Migration Pattern**:
   ```python
   with app.app_context():
       try:
           db.create_all()
           logger.info("Database tables created successfully")
       except Exception as e:
           logger.error(f"Database initialization failed: {e}")
   ```

### AI Model Integration

1. **Lazy Loading**:
   - Load AI models only when needed
   - Implement fallback classes for failed imports
   - Use health check methods to verify model status

2. **Error Handling**:
   ```python
   try:
       from ai_models.github_analyzer import GitHubAnalyzer
       analyzer = GitHubAnalyzer()
   except ImportError as e:
       logger.error(f"Failed to import AI model: {e}")
       # Use fallback implementation
   ```

### File Operations

1. **Path Handling**:
   - Use `pathlib.Path` for file operations
   - Validate file paths before operations
   - Handle file not found errors gracefully

2. **Security**:
   - Sanitize all file paths
   - Validate file extensions
   - Limit file sizes
   - Use temporary directories for processing

### Environment Configuration

1. **Environment Variables**:
   - Use `.env` file for configuration
   - Provide sensible defaults
   - Document all required environment variables
   - Never hardcode sensitive information

2. **Configuration Pattern**:
   ```python
   app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
   app.config['PORT'] = int(os.getenv('PORT', 5000))
   ```

### Logging Standards

1. **Log Levels**:
   - DEBUG: Detailed debugging information
   - INFO: General information about application flow
   - WARNING: Something unexpected but recoverable
   - ERROR: Serious problems that need attention

2. **Log Format**:
   ```python
   logger.info(f"Processing repository: {repo_url}")
   logger.error(f"Failed to process {repo_url}: {error_message}")
   ```

### Documentation Requirements

1. **Code Documentation**:
   - Include docstrings for all public methods
   - Document complex algorithms
   - Add inline comments for non-obvious code

2. **API Documentation**:
   - Document all endpoints with examples
   - Include request/response schemas
   - Document error responses

### Performance Considerations

1. **Async Operations**:
   - Use background tasks for long-running operations
   - Implement proper timeout handling
   - Provide progress indicators

2. **Caching**:
   - Cache expensive operations
   - Use appropriate cache invalidation
   - Monitor cache hit rates

### Security Best Practices

1. **Input Validation**:
   - Validate all user inputs
   - Sanitize file paths
   - Check for malicious content

2. **Authentication**:
   - Use secure session management
   - Implement proper token handling
   - Follow OAuth best practices for GitHub integration
