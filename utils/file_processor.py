import os
import mimetypes
import hashlib
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class FileProcessor:
    """Utility class for processing files in repositories"""
    
    def __init__(self):
        """Initialize the file processor"""
        self.supported_extensions = {
            # Programming languages
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.cs',
            '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.dart',
            '.r', '.m', '.pl', '.sh', '.ps1', '.bat',
            
            # Web technologies
            '.html', '.css', '.scss', '.sass', '.less', '.vue', '.svelte',
            
            # Data formats
            '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg',
            
            # Documentation
            '.md', '.rst', '.txt', '.adoc',
            
            # Configuration
            '.dockerfile', '.gitignore', '.editorconfig', '.prettierrc',
            
            # Build files
            '.makefile', '.gradle', '.maven', '.cmake'
        }
        
        self.binary_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.ico',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.tar', '.gz', '.rar', '.7z',
            '.exe', '.dll', '.so', '.dylib',
            '.mp4', '.avi', '.mov', '.wmv', '.flv',
            '.mp3', '.wav', '.aac', '.flac'
        }
    
    def is_text_file(self, file_path: Union[str, Path]) -> bool:
        """Check if a file is a text file"""
        file_path = Path(file_path)
        
        # Check by extension
        ext = file_path.suffix.lower()
        
        if ext in self.binary_extensions:
            return False
        
        if ext in self.supported_extensions:
            return True
        
        # Check MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and mime_type.startswith('text/'):
            return True
        
        # If unsure, try to read a small portion
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1024)  # Read first 1KB
            return True
        except (UnicodeDecodeError, IOError):
            return False
    
    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get comprehensive information about a file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': 'File does not exist'}
        
        info = {
            'name': file_path.name,
            'path': str(file_path),
            'size': file_path.stat().st_size,
            'extension': file_path.suffix.lower(),
            'is_text': self.is_text_file(file_path),
            'language': self.detect_language(file_path),
            'encoding': None,
            'line_count': 0,
            'checksum': None
        }
        
        # Additional info for text files
        if info['is_text']:
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # Detect encoding
                info['encoding'] = self._detect_encoding(content)
                
                # Get line count
                if info['encoding']:
                    try:
                        text_content = content.decode(info['encoding'])
                        info['line_count'] = text_content.count('\n') + 1
                    except UnicodeDecodeError:
                        info['line_count'] = 0
                
                # Calculate checksum
                info['checksum'] = hashlib.md5(content).hexdigest()
                
            except Exception as e:
                logger.warning(f"Error processing file {file_path}: {e}")
        
        return info
    
    def detect_language(self, file_path: Union[str, Path]) -> Optional[str]:
        """Detect programming language from file extension and content"""
        file_path = Path(file_path)
        ext = file_path.suffix.lower()
        name = file_path.name.lower()
        
        # Extension-based detection
        extension_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.cxx': 'C++',
            '.cc': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.hpp': 'C++ Header',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.dart': 'Dart',
            '.r': 'R',
            '.m': 'Objective-C/MATLAB',
            '.pl': 'Perl',
            '.sh': 'Shell',
            '.bash': 'Bash',
            '.zsh': 'Zsh',
            '.fish': 'Fish',
            '.ps1': 'PowerShell',
            '.bat': 'Batch',
            '.cmd': 'Batch',
            '.html': 'HTML',
            '.htm': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.sass': 'Sass',
            '.less': 'Less',
            '.vue': 'Vue.js',
            '.svelte': 'Svelte',
            '.sql': 'SQL',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.toml': 'TOML',
            '.ini': 'INI',
            '.cfg': 'Configuration',
            '.conf': 'Configuration',
            '.md': 'Markdown',
            '.rst': 'reStructuredText',
            '.tex': 'LaTeX',
            '.dockerfile': 'Dockerfile',
            '.makefile': 'Makefile',
            '.gradle': 'Gradle',
            '.maven': 'Maven'
        }
        
        if ext in extension_map:
            return extension_map[ext]
        
        # Name-based detection
        name_map = {
            'makefile': 'Makefile',
            'dockerfile': 'Dockerfile',
            'rakefile': 'Ruby',
            'gemfile': 'Ruby',
            'podfile': 'Ruby',
            'vagrantfile': 'Ruby',
            'gulpfile.js': 'JavaScript',
            'gruntfile.js': 'JavaScript',
            'webpack.config.js': 'JavaScript',
            'package.json': 'JSON',
            'composer.json': 'JSON',
            'requirements.txt': 'Text',
            'setup.py': 'Python',
            'manage.py': 'Python',
            'settings.py': 'Python'
        }
        
        if name in name_map:
            return name_map[name]
        
        return None
    
    def _detect_encoding(self, content: bytes) -> Optional[str]:
        """Detect text encoding"""
        try:
            # Try UTF-8 first
            content.decode('utf-8')
            return 'utf-8'
        except UnicodeDecodeError:
            pass
        
        # Try other common encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'ascii']
        
        for encoding in encodings:
            try:
                content.decode(encoding)
                return encoding
            except UnicodeDecodeError:
                continue
        
        return None
    
    def extract_file_content(self, file_path: Union[str, Path], max_size: int = 1024 * 1024) -> Dict[str, Any]:
        """Extract content from a file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': 'File does not exist'}
        
        # Check file size
        file_size = file_path.stat().st_size
        if file_size > max_size:
            return {
                'error': f'File too large ({file_size} bytes, max {max_size} bytes)',
                'size': file_size
            }
        
        # Check if it's a text file
        if not self.is_text_file(file_path):
            return {
                'error': 'Binary file, content extraction skipped',
                'is_binary': True
            }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                'content': content,
                'size': len(content),
                'line_count': content.count('\n') + 1,
                'language': self.detect_language(file_path)
            }
            
        except Exception as e:
            return {'error': f'Failed to read file: {str(e)}'}
    
    def analyze_code_complexity(self, content: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        if not content:
            return {}
        
        lines = content.split('\n')
        
        # Basic metrics
        metrics = {
            'total_lines': len(lines),
            'blank_lines': sum(1 for line in lines if not line.strip()),
            'comment_lines': 0,
            'code_lines': 0,
            'complexity_score': 0
        }
        
        # Language-specific comment patterns
        comment_patterns = {
            'Python': [r'^\s*#'],
            'JavaScript': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'TypeScript': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'Java': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'C++': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'C#': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'Go': [r'^\s*//'],
            'Rust': [r'^\s*//', r'^\s*/\*'],
            'Ruby': [r'^\s*#'],
            'PHP': [r'^\s*//', r'^\s*#', r'^\s*/\*'],
            'Shell': [r'^\s*#'],
            'HTML': [r'^\s*<!--'],
            'CSS': [r'^\s*/\*'],
            'SQL': [r'^\s*--', r'^\s*/\*']
        }
        
        # Count comment lines
        if language in comment_patterns:
            patterns = comment_patterns[language]
            for line in lines:
                if any(re.search(pattern, line) for pattern in patterns):
                    metrics['comment_lines'] += 1
        
        # Calculate code lines
        metrics['code_lines'] = metrics['total_lines'] - metrics['blank_lines'] - metrics['comment_lines']
        
        # Simple complexity score based on various factors
        complexity_keywords = [
            'if', 'else', 'elif', 'while', 'for', 'switch', 'case',
            'try', 'catch', 'except', 'finally', 'async', 'await',
            'function', 'def', 'class', 'interface', 'struct'
        ]
        
        complexity_score = 0
        for line in lines:
            line_lower = line.lower()
            complexity_score += sum(line_lower.count(keyword) for keyword in complexity_keywords)
        
        metrics['complexity_score'] = complexity_score
        
        # Calculate relative metrics
        if metrics['total_lines'] > 0:
            metrics['comment_ratio'] = metrics['comment_lines'] / metrics['total_lines']
            metrics['code_ratio'] = metrics['code_lines'] / metrics['total_lines']
            metrics['complexity_per_line'] = complexity_score / metrics['total_lines']
        
        return metrics
    
    def extract_imports_and_dependencies(self, content: str, language: Optional[str] = None) -> Dict[str, List[str]]:
        """Extract imports and dependencies from code"""
        imports = {
            'imports': [],
            'from_imports': [],
            'requires': [],
            'includes': []
        }
        
        if not content or not language:
            return imports
        
        lines = content.split('\n')
        
        # Language-specific import patterns
        if language == 'Python':
            for line in lines:
                line = line.strip()
                # import module
                import_match = re.match(r'import\s+([^#\n]+)', line)
                if import_match:
                    imports['imports'].append(import_match.group(1).strip())
                
                # from module import ...
                from_match = re.match(r'from\s+([^\s]+)\s+import\s+([^#\n]+)', line)
                if from_match:
                    imports['from_imports'].append(f"{from_match.group(1)} -> {from_match.group(2).strip()}")
        
        elif language in ['JavaScript', 'TypeScript']:
            for line in lines:
                line = line.strip()
                # import ... from '...'
                import_match = re.match(r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]', line)
                if import_match:
                    imports['imports'].append(import_match.group(1))
                
                # require('...')
                require_match = re.search(r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', line)
                if require_match:
                    imports['requires'].append(require_match.group(1))
        
        elif language in ['C', 'C++']:
            for line in lines:
                line = line.strip()
                # #include <...> or #include "..."
                include_match = re.match(r'#include\s*[<"]([^>"]+)[>"]', line)
                if include_match:
                    imports['includes'].append(include_match.group(1))
        
        elif language == 'Java':
            for line in lines:
                line = line.strip()
                # import package.Class;
                import_match = re.match(r'import\s+([^;]+);', line)
                if import_match:
                    imports['imports'].append(import_match.group(1).strip())
        
        elif language == 'Go':
            for line in lines:
                line = line.strip()
                # import "package"
                import_match = re.match(r'import\s+[\'"]([^\'"]+)[\'"]', line)
                if import_match:
                    imports['imports'].append(import_match.group(1))
        
        elif language == 'Rust':
            for line in lines:
                line = line.strip()
                # use crate::module;
                use_match = re.match(r'use\s+([^;]+);', line)
                if use_match:
                    imports['imports'].append(use_match.group(1).strip())
        
        return imports
    
    def extract_functions_and_classes(self, content: str, language: Optional[str] = None) -> Dict[str, List[str]]:
        """Extract function and class definitions from code"""
        definitions = {
            'functions': [],
            'classes': [],
            'methods': [],
            'interfaces': []
        }
        
        if not content or not language:
            return definitions
        
        lines = content.split('\n')
        
        # Language-specific patterns
        if language == 'Python':
            for line in lines:
                line = line.strip()
                # def function_name(
                func_match = re.match(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line)
                if func_match:
                    definitions['functions'].append(func_match.group(1))
                
                # class ClassName(
                class_match = re.match(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
                if class_match:
                    definitions['classes'].append(class_match.group(1))
        
        elif language in ['JavaScript', 'TypeScript']:
            for line in lines:
                line = line.strip()
                # function functionName(
                func_match = re.match(r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line)
                if func_match:
                    definitions['functions'].append(func_match.group(1))
                
                # const functionName = (
                arrow_func_match = re.match(r'(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(', line)
                if arrow_func_match:
                    definitions['functions'].append(arrow_func_match.group(1))
                
                # class ClassName {
                class_match = re.match(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
                if class_match:
                    definitions['classes'].append(class_match.group(1))
                
                # interface InterfaceName {
                if language == 'TypeScript':
                    interface_match = re.match(r'interface\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
                    if interface_match:
                        definitions['interfaces'].append(interface_match.group(1))
        
        elif language == 'Java':
            for line in lines:
                line = line.strip()
                # public/private/protected ... methodName(
                method_match = re.search(r'(?:public|private|protected|static).*\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line)
                if method_match and not re.search(r'\b(?:class|interface)\b', line):
                    definitions['methods'].append(method_match.group(1))
                
                # class ClassName {
                class_match = re.match(r'(?:public|private|protected)?\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
                if class_match:
                    definitions['classes'].append(class_match.group(1))
                
                # interface InterfaceName {
                interface_match = re.match(r'(?:public|private|protected)?\s*interface\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
                if interface_match:
                    definitions['interfaces'].append(interface_match.group(1))
        
        return definitions
    
    def get_file_statistics(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get comprehensive file statistics"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': 'File does not exist'}
        
        # Basic file info
        info = self.get_file_info(file_path)
        
        if not info.get('is_text', False):
            return info
        
        # Extract content
        content_info = self.extract_file_content(file_path)
        
        if 'error' in content_info:
            return {**info, **content_info}
        
        content = content_info['content']
        language = info['language']
        
        # Analyze complexity
        complexity = self.analyze_code_complexity(content, language)
        
        # Extract imports and dependencies
        imports = self.extract_imports_and_dependencies(content, language)
        
        # Extract functions and classes
        definitions = self.extract_functions_and_classes(content, language)
        
        return {
            **info,
            'complexity': complexity,
            'imports': imports,
            'definitions': definitions,
            'content_preview': content[:500] + '...' if len(content) > 500 else content
        }
