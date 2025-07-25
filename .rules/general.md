# General Development Rules for Documentation.AI

## Project Overview
Documentation.AI is a comprehensive documentation generator using AI for GitHub repositories. It consists of a Flask backend, React frontend, and AI models for analysis and generation.

## Core Principles
1. **Maintain separation of concerns**: Backend, frontend, AI models, utilities, and tests should remain in their designated directories
2. **Follow existing patterns**: When adding new features, follow the established architectural patterns
3. **Prioritize reliability**: Always include error handling and logging
4. **Keep it maintainable**: Write clear, documented code with proper typing

## Directory Structure Rules

### Backend (Python)
- **Main application**: `app.py` (root level)
- **AI Models**: `/ai_models/` - All AI-related classes and functions
- **Database**: `/database/` - Database models and migrations
- **Utilities**: `/utils/` - Helper functions and utilities
- **Tests**: `/tests/` - All test files (pytest format)
- **Scripts**: `/scripts/` - Shell scripts and automation tools

### Frontend (React/TypeScript)
- **Source**: `/frontend/src/` - All React components and pages
- **Components**: `/frontend/src/components/` - Reusable UI components
- **Pages**: `/frontend/src/pages/` - Main application pages
- **Build**: `/frontend/build/` - Production build files

### Configuration
- **Environment**: `.env` (root level, gitignored)
- **Dependencies**: `requirements.txt` (Python), `frontend/package.json` (Node.js)
- **Docker**: `Dockerfile`, `docker-compose.yml` (root level)

## File Naming Conventions
- Python files: `snake_case.py`
- TypeScript/React files: `PascalCase.tsx` for components, `camelCase.ts` for utilities
- Shell scripts: `kebab-case.sh`
- Test files: `test_*.py` or `*_test.py`
- Config files: lowercase with appropriate extensions

## Code Quality Standards
1. **Type hints**: Always use type hints in Python code
2. **Error handling**: Wrap external calls in try-catch blocks
3. **Logging**: Use structured logging with appropriate levels
4. **Documentation**: Include docstrings for all classes and functions
5. **Testing**: Write tests for new functionality in `/tests/`

## Git and Version Control
- Never commit sensitive information (API keys, tokens)
- Use `.gitignore` to exclude build files, cache, and secrets
- Write descriptive commit messages
- Keep commits focused and atomic

## Dependencies and Environment
- Pin dependency versions in requirements files
- Use virtual environments for Python development
- Document any system dependencies
- Keep dependency lists minimal and necessary

## Performance Guidelines
- Lazy load AI models to avoid startup delays
- Use caching for expensive operations
- Implement proper database indexing
- Optimize frontend bundle size

## Security Considerations
- Validate all user inputs
- Use environment variables for secrets
- Implement proper CORS configuration
- Sanitize file paths and user content
- Use HTTPS in production
