# Development Rules & Guidelines

This folder contains comprehensive development rules and guidelines for the Documentation.AI project.

## Rule Files Structure

- `coding-standards.md` - Coding conventions and best practices
- `ui-design-rules.md` - UI/UX design guidelines and standards
- `authentication-rules.md` - Clerk authentication integration guide
- `api-rules.md` - Backend API development rules (to be created)
- `security-rules.md` - Security implementation guidelines (to be created)
- `testing-rules.md` - Testing standards and procedures (to be created)
- `git-workflow.md` - Git workflow and branching strategy (to be created)
- `deployment-rules.md` - Deployment and production guidelines (to be created)

## Quick Reference

### Core Principles
1. **GitHub-Style UI** - All UI components must replicate GitHub's design language
2. **Type Safety** - TypeScript strict mode enabled throughout
3. **Responsive Design** - Mobile-first approach with Tailwind CSS
4. **Dark Mode Support** - Full dark/light mode compatibility
5. **Accessibility** - WCAG 2.1 AA compliance
6. **Performance** - Optimize for speed and efficiency
7. **Security** - Security-first development approach

### Key Technologies
- **Frontend**: React 18+ with TypeScript
- **Styling**: Tailwind CSS with dark mode
- **Backend**: Flask with Python 3.12+
- **Authentication**: Clerk with GitHub OAuth
- **AI Integration**: Custom AI models with fallbacks
- **Database**: SQLite with potential PostgreSQL migration

### Development Workflow
1. Feature branches from `main`
2. Comprehensive testing before PR
3. Code review required
4. Continuous integration checks
5. Documentation updates required
- **Content**: Project structure, naming conventions, security guidelines
- **Target**: All developers and AI models

### 2. `copilot.md`
- **Scope**: GitHub Copilot specific development patterns
- **Content**: Code templates, error handling patterns, Flask route examples
- **Target**: GitHub Copilot AI assistant

### 3. `claude.md`
- **Scope**: Claude AI specific development guidelines
- **Content**: Detailed patterns for Flask, React, testing, and deployment
- **Target**: Claude AI assistant (Anthropic)

### 4. `llm.md`
- **Scope**: Universal guidelines for all language models
- **Content**: Core principles, mandatory file organization, testing standards
- **Target**: All AI language models (GPT-4, Claude, Gemini, etc.)

## Key Principles

### File Organization (MANDATORY)
- **Tests**: ALL test files MUST go in `/tests/` directory
- **Scripts**: ALL shell scripts MUST go in `/scripts/` directory
- **AI Models**: Keep in `/ai_models/` directory
- **Utilities**: Place helper functions in `/utils/` directory

### Code Quality Standards
- **Type Annotations**: Required for all Python functions
- **Error Handling**: Comprehensive try-catch blocks with logging
- **Testing**: High test coverage with appropriate test patterns
- **Documentation**: Clear docstrings and comments

### Security Requirements
- **Input Validation**: Validate all user inputs
- **Output Sanitization**: Sanitize all outputs
- **No Hardcoded Secrets**: Use environment variables
- **Rate Limiting**: Implement for public APIs

## How to Use These Rules

### For AI Models
1. **Read the universal rules** in `llm.md` first
2. **Read your specific model rules** (e.g., `claude.md` for Claude)
3. **Follow the file organization mandates** strictly
4. **Implement the code patterns** shown in examples
5. **Test everything** using the testing guidelines

### For Human Developers
1. **Review all rule files** to understand AI model expectations
2. **Follow the same standards** for consistency
3. **Update rules** when adding new patterns or requirements
4. **Validate AI output** against these rules

## Project Structure Context

```
Documentation.AI/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker configuration
├── .env                      # Environment variables
├── ai_models/               # AI model implementations
├── database/                # Database models and utilities
├── utils/                   # Helper functions and utilities
├── tests/                   # ALL test files go here
├── scripts/                 # ALL shell scripts go here
├── frontend/                # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   └── pages/          # React pages
│   └── package.json        # Frontend dependencies
├── instance/                # Database files
└── .rules/                  # This directory - development rules
    ├── README.md           # This file
    ├── general.md          # General development guidelines
    ├── copilot.md          # GitHub Copilot specific rules
    ├── claude.md           # Claude AI specific rules
    └── llm.md              # Universal LLM guidelines
```

## Critical Reminders

### ABSOLUTE REQUIREMENTS
1. **File Placement Rules are MANDATORY**
   - Tests → `/tests/` directory
   - Scripts → `/scripts/` directory
   - No exceptions

2. **Error Handling is REQUIRED**
   - Every function must handle exceptions
   - Always log errors with context
   - Provide user-friendly error messages

3. **Type Safety is MANDATORY**
   - Use type hints in Python
   - Use TypeScript for frontend
   - Validate all inputs

### FORBIDDEN PRACTICES
- ❌ Placing test files outside `/tests/` directory
- ❌ Placing scripts outside `/scripts/` directory
- ❌ Hardcoding configuration values
- ❌ Ignoring errors or exceptions
- ❌ Committing sensitive information

## Rule Updates

When updating these rules:

1. **Document the change** in the relevant rule file
2. **Update examples** to match new patterns
3. **Notify all team members** of the changes
4. **Update this README** if the structure changes

## Validation

To ensure AI models are following these rules:

1. **Review file placement** in pull requests
2. **Check error handling** patterns
3. **Validate test coverage** and placement
4. **Verify type annotations** are present
5. **Test the changes** thoroughly

These rules are designed to maintain high code quality and consistency across all contributors to the Documentation.AI project.
