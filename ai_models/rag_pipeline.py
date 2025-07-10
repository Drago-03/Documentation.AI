import os
import logging
import numpy as np
from typing import Dict, List, Any, Optional
from sentence_transformers import SentenceTransformer
import faiss
import json
from pathlib import Path
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for code analysis"""
    
    def __init__(self):
        """Initialize the RAG pipeline"""
        self.embedding_model = None
        self.vector_store = None
        self.documents = []
        self.embeddings = None
        
        try:
            # Initialize sentence transformer model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("RAG pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RAG pipeline: {e}")
    
    def check_health(self) -> bool:
        """Check if the RAG pipeline is healthy"""
        return self.embedding_model is not None
    
    def process_repository(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process repository analysis with RAG pipeline"""
        logger.info("Processing repository with RAG pipeline")
        
        try:
            # Extract and process documents
            documents = self._extract_documents(analysis_result)
            
            # Create embeddings
            embeddings = self._create_embeddings(documents)
            
            # Build vector store
            vector_store = self._build_vector_store(embeddings)
            
            # Perform semantic analysis
            semantic_insights = self._perform_semantic_analysis(documents, embeddings)
            
            # Generate code patterns
            code_patterns = self._extract_code_patterns(documents)
            
            # Create knowledge graph
            knowledge_graph = self._create_knowledge_graph(analysis_result, documents)
            
            rag_result = {
                'semantic_insights': semantic_insights,
                'code_patterns': code_patterns,
                'knowledge_graph': knowledge_graph,
                'document_count': len(documents),
                'embedding_dimension': embeddings.shape[1] if embeddings is not None else 0,
                'processing_status': 'completed'
            }
            
            logger.info("RAG pipeline processing completed")
            return rag_result
            
        except Exception as e:
            logger.error(f"RAG pipeline processing failed: {e}")
            return {
                'processing_status': 'failed',
                'error': str(e),
                'semantic_insights': [],
                'code_patterns': [],
                'knowledge_graph': {},
                'document_count': 0,
                'embedding_dimension': 0
            }
    
    def _extract_documents(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract documents from analysis result"""
        documents = []
        
        # Extract from code analysis
        code_analysis = analysis_result.get('code_analysis', {})
        
        # Add dependencies as documents
        dependencies = code_analysis.get('dependencies', [])
        for dep in dependencies:
            documents.append({
                'type': 'dependency',
                'content': f"Dependency: {dep.get('name', '')} version {dep.get('version', '')} ecosystem {dep.get('ecosystem', '')}",
                'metadata': dep
            })
        
        # Add frameworks as documents
        frameworks = code_analysis.get('frameworks', [])
        for framework in frameworks:
            documents.append({
                'type': 'framework',
                'content': f"Framework: {framework} used in the project",
                'metadata': {'name': framework}
            })
        
        # Add API endpoints as documents
        api_endpoints = code_analysis.get('api_endpoints', [])
        for endpoint in api_endpoints:
            documents.append({
                'type': 'api_endpoint',
                'content': f"API endpoint: {endpoint}",
                'metadata': {'endpoint': endpoint}
            })
        
        # Add architecture patterns
        arch_patterns = code_analysis.get('architecture_patterns', [])
        for pattern in arch_patterns:
            documents.append({
                'type': 'architecture_pattern',
                'content': f"Architecture pattern: {pattern}",
                'metadata': {'pattern': pattern}
            })
        
        # Add file structure information
        file_structure = analysis_result.get('file_structure', {})
        important_files = file_structure.get('important_files', [])
        for file_path in important_files:
            documents.append({
                'type': 'important_file',
                'content': f"Important file: {file_path}",
                'metadata': {'file_path': file_path}
            })
        
        # Add language information
        languages = file_structure.get('languages', {})
        for lang, count in languages.items():
            documents.append({
                'type': 'programming_language',
                'content': f"Programming language: {lang} with {count} files",
                'metadata': {'language': lang, 'file_count': count}
            })
        
        # Add repository metadata
        metadata = analysis_result.get('metadata', {})
        if metadata.get('description'):
            documents.append({
                'type': 'repository_description',
                'content': f"Repository description: {metadata['description']}",
                'metadata': metadata
            })
        
        logger.info(f"Extracted {len(documents)} documents for RAG processing")
        return documents
    
    def _create_embeddings(self, documents: List[Dict[str, Any]]) -> Optional[np.ndarray]:
        """Create embeddings for documents"""
        if not self.embedding_model or not documents:
            return None
        
        try:
            # Extract text content from documents
            texts = [doc['content'] for doc in documents]
            
            # Create embeddings
            embeddings = self.embedding_model.encode(texts)
            
            # Store for later use
            self.documents = documents
            self.embeddings = embeddings
            
            logger.info(f"Created embeddings for {len(documents)} documents")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to create embeddings: {e}")
            return None
    
    def _build_vector_store(self, embeddings: Optional[np.ndarray]) -> Optional[Any]:
        """Build FAISS vector store"""
        if embeddings is None:
            return None
        
        try:
            # Initialize FAISS index
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            
            # Add embeddings to index
            index.add(embeddings.astype('float32'))
            
            self.vector_store = index
            logger.info(f"Built vector store with {embeddings.shape[0]} vectors")
            return index
            
        except Exception as e:
            logger.error(f"Failed to build vector store: {e}")
            return None
    
    def _perform_semantic_analysis(self, documents: List[Dict[str, Any]], embeddings: Optional[np.ndarray]) -> List[Dict[str, Any]]:
        """Perform semantic analysis on documents"""
        insights = []
        
        try:
            # Group documents by type
            doc_types = {}
            for i, doc in enumerate(documents):
                doc_type = doc['type']
                if doc_type not in doc_types:
                    doc_types[doc_type] = []
                doc_types[doc_type].append((i, doc))
            
            # Analyze patterns within each type
            for doc_type, doc_list in doc_types.items():
                if len(doc_list) > 1:
                    insights.append({
                        'type': 'pattern_analysis',
                        'category': doc_type,
                        'count': len(doc_list),
                        'description': f"Found {len(doc_list)} instances of {doc_type}",
                        'examples': [doc[1]['content'] for doc in doc_list[:3]]  # First 3 examples
                    })
            
            # Technology stack analysis
            frameworks = [doc for doc in documents if doc['type'] == 'framework']
            languages = [doc for doc in documents if doc['type'] == 'programming_language']
            
            if frameworks and languages:
                insights.append({
                    'type': 'technology_stack',
                    'description': 'Technology stack analysis',
                    'frameworks': [f['metadata']['name'] for f in frameworks],
                    'languages': [l['metadata']['language'] for l in languages],
                    'stack_complexity': len(frameworks) + len(languages)
                })
            
            # Dependency analysis
            dependencies = [doc for doc in documents if doc['type'] == 'dependency']
            if dependencies:
                ecosystems = {}
                for dep in dependencies:
                    ecosystem = dep['metadata'].get('ecosystem', 'unknown')
                    ecosystems[ecosystem] = ecosystems.get(ecosystem, 0) + 1
                
                insights.append({
                    'type': 'dependency_analysis',
                    'description': 'Dependency ecosystem analysis',
                    'total_dependencies': len(dependencies),
                    'ecosystems': ecosystems,
                    'complexity_score': len(dependencies) * 0.1
                })
            
            # API complexity analysis
            api_endpoints = [doc for doc in documents if doc['type'] == 'api_endpoint']
            if api_endpoints:
                insights.append({
                    'type': 'api_complexity',
                    'description': 'API endpoint analysis',
                    'endpoint_count': len(api_endpoints),
                    'complexity_level': 'high' if len(api_endpoints) > 10 else 'medium' if len(api_endpoints) > 5 else 'low'
                })
            
            logger.info(f"Generated {len(insights)} semantic insights")
            return insights
            
        except Exception as e:
            logger.error(f"Semantic analysis failed: {e}")
            return []
    
    def _extract_code_patterns(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract code patterns from documents"""
        patterns = []
        
        try:
            # Framework patterns
            frameworks = [doc for doc in documents if doc['type'] == 'framework']
            if frameworks:
                framework_names = [f['metadata']['name'] for f in frameworks]
                
                # Detect common patterns
                if 'Flask' in framework_names or 'Django' in framework_names or 'FastAPI' in framework_names:
                    patterns.append({
                        'pattern': 'web_framework',
                        'description': 'Web application framework pattern detected',
                        'frameworks': framework_names,
                        'confidence': 0.9
                    })
                
                if 'React' in framework_names or 'Vue.js' in framework_names or 'Angular' in framework_names:
                    patterns.append({
                        'pattern': 'frontend_spa',
                        'description': 'Single Page Application pattern detected',
                        'frameworks': framework_names,
                        'confidence': 0.85
                    })
            
            # API patterns
            api_endpoints = [doc for doc in documents if doc['type'] == 'api_endpoint']
            if api_endpoints:
                endpoint_contents = [ep['content'] for ep in api_endpoints]
                
                # Detect REST patterns
                rest_methods = ['GET', 'POST', 'PUT', 'DELETE']
                detected_methods = []
                for method in rest_methods:
                    if any(method.lower() in content.lower() for content in endpoint_contents):
                        detected_methods.append(method)
                
                if len(detected_methods) >= 2:
                    patterns.append({
                        'pattern': 'rest_api',
                        'description': 'RESTful API pattern detected',
                        'methods': detected_methods,
                        'confidence': len(detected_methods) * 0.2
                    })
            
            # Architecture patterns
            arch_docs = [doc for doc in documents if doc['type'] == 'architecture_pattern']
            for arch_doc in arch_docs:
                patterns.append({
                    'pattern': 'architecture',
                    'description': f"Architecture pattern: {arch_doc['metadata']['pattern']}",
                    'confidence': 0.8
                })
            
            # Database patterns
            dependencies = [doc for doc in documents if doc['type'] == 'dependency']
            db_deps = []
            db_keywords = ['sql', 'mongo', 'redis', 'postgres', 'mysql', 'sqlite', 'orm']
            
            for dep in dependencies:
                dep_name = dep['metadata'].get('name', '').lower()
                if any(keyword in dep_name for keyword in db_keywords):
                    db_deps.append(dep['metadata']['name'])
            
            if db_deps:
                patterns.append({
                    'pattern': 'database_integration',
                    'description': 'Database integration pattern detected',
                    'databases': db_deps,
                    'confidence': 0.7
                })
            
            logger.info(f"Extracted {len(patterns)} code patterns")
            return patterns
            
        except Exception as e:
            logger.error(f"Code pattern extraction failed: {e}")
            return []
    
    def _create_knowledge_graph(self, analysis_result: Dict[str, Any], documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create knowledge graph from analysis results"""
        try:
            graph = {
                'nodes': [],
                'edges': [],
                'metadata': {
                    'created_at': str(datetime.now()),
                    'node_count': 0,
                    'edge_count': 0
                }
            }
            
            # Add repository as root node
            repo_info = analysis_result.get('repository_info', {})
            repo_node = {
                'id': 'repository',
                'type': 'repository',
                'label': repo_info.get('repo', 'Repository'),
                'properties': repo_info
            }
            graph['nodes'].append(repo_node)
            
            # Add language nodes
            file_structure = analysis_result.get('file_structure', {})
            languages = file_structure.get('languages', {})
            
            for lang, count in languages.items():
                lang_node = {
                    'id': f'lang_{lang.lower().replace(" ", "_")}',
                    'type': 'programming_language',
                    'label': lang,
                    'properties': {'file_count': count}
                }
                graph['nodes'].append(lang_node)
                
                # Connect to repository
                graph['edges'].append({
                    'from': 'repository',
                    'to': lang_node['id'],
                    'type': 'uses_language',
                    'weight': count
                })
            
            # Add framework nodes
            code_analysis = analysis_result.get('code_analysis', {})
            frameworks = code_analysis.get('frameworks', [])
            
            for framework in frameworks:
                framework_node = {
                    'id': f'framework_{framework.lower().replace(" ", "_").replace(".", "_")}',
                    'type': 'framework',
                    'label': framework,
                    'properties': {'name': framework}
                }
                graph['nodes'].append(framework_node)
                
                # Connect to repository
                graph['edges'].append({
                    'from': 'repository',
                    'to': framework_node['id'],
                    'type': 'uses_framework',
                    'weight': 1
                })
            
            # Add dependency nodes
            dependencies = code_analysis.get('dependencies', [])
            
            for dep in dependencies[:20]:  # Limit to first 20 dependencies
                dep_node = {
                    'id': f'dep_{dep["name"].lower().replace("-", "_").replace(".", "_")}',
                    'type': 'dependency',
                    'label': dep['name'],
                    'properties': dep
                }
                graph['nodes'].append(dep_node)
                
                # Connect to repository
                graph['edges'].append({
                    'from': 'repository',
                    'to': dep_node['id'],
                    'type': 'depends_on',
                    'weight': 1
                })
            
            # Add file nodes for important files
            important_files = file_structure.get('important_files', [])
            
            for file_path in important_files:
                file_node = {
                    'id': f'file_{file_path.replace("/", "_").replace(".", "_")}',
                    'type': 'file',
                    'label': file_path,
                    'properties': {'path': file_path}
                }
                graph['nodes'].append(file_node)
                
                # Connect to repository
                graph['edges'].append({
                    'from': 'repository',
                    'to': file_node['id'],
                    'type': 'contains_file',
                    'weight': 1
                })
                
                # Connect files to languages based on extension
                file_ext = Path(file_path).suffix.lower()
                ext_to_lang = {
                    '.py': 'Python',
                    '.js': 'JavaScript',
                    '.ts': 'TypeScript',
                    '.java': 'Java',
                    '.go': 'Go',
                    '.rs': 'Rust'
                }
                
                if file_ext in ext_to_lang:
                    lang_name = ext_to_lang[file_ext]
                    lang_id = f'lang_{lang_name.lower()}'
                    
                    # Check if language node exists
                    if any(node['id'] == lang_id for node in graph['nodes']):
                        graph['edges'].append({
                            'from': file_node['id'],
                            'to': lang_id,
                            'type': 'written_in',
                            'weight': 1
                        })
            
            # Update metadata
            graph['metadata']['node_count'] = len(graph['nodes'])
            graph['metadata']['edge_count'] = len(graph['edges'])
            
            logger.info(f"Created knowledge graph with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
            return graph
            
        except Exception as e:
            logger.error(f"Knowledge graph creation failed: {e}")
            return {
                'nodes': [],
                'edges': [],
                'metadata': {'error': str(e)}
            }
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search on indexed documents"""
        if not self.embedding_model or not self.vector_store or not self.documents:
            return []
        
        try:
            # Create embedding for query
            query_embedding = self.embedding_model.encode([query])
            
            # Search in vector store
            distances, indices = self.vector_store.search(query_embedding.astype('float32'), top_k)
            
            # Return results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.documents):
                    results.append({
                        'document': self.documents[idx],
                        'similarity_score': 1 - (distance / 2),  # Convert distance to similarity
                        'rank': i + 1
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
