import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Star, 
  GitFork, 
  Eye, 
  Download, 
  Code, 
  Book, 
  FileText, 
  Folder, 
  File,
  ExternalLink,
  Copy,
  Check,
  Calendar,
  User,
  Tag,
  AlertCircle,
  RefreshCw,
  ChevronRight,
  Clock
} from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { toast } from 'react-hot-toast';

interface Repository {
  name: string;
  full_name: string;
  description: string;
  html_url: string;
  language: string;
  stargazers_count: number;
  forks_count: number;
  open_issues_count: number;
  created_at: string;
  updated_at: string;
  license?: { name: string };
  topics: string[];
}

interface JobData {
  job_id: number;
  repo_url: string;
  repo_name: string;
  repo_owner: string;
  status: string;
  created_at: string;
  updated_at: string;
  download_url?: string;
  documentation?: {
    readme: string;
    api_docs: string;
    setup_guide: string;
    architecture_docs: string;
    contributing_guide: string;
    changelog: string;
    license: string;
    gitignore: string;
    dockerfile: string;
    additional_files: Record<string, string>;
  };
  analysis?: {
    repository_info: Repository;
    file_structure: {
      total_files: number;
      languages: Record<string, number>;
      important_files: string[];
      directories: string[];
      files: string[];
    };
    technologies: {
      frameworks: string[];
      databases: string[];
      tools: string[];
      deployment: string[];
    };
  };
  error_message?: string;
}

interface FileTreeItem {
  name: string;
  type: 'file' | 'folder';
  content?: string;
  children?: FileTreeItem[];
}

const RepositoryView: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  
  const [jobData, setJobData] = useState<JobData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('readme');
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [copiedContent, setCopiedContent] = useState<string | null>(null);

  useEffect(() => {
    if (jobId) {
      fetchJobData();
    }
  }, [jobId]);

  const fetchJobData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/job/${jobId}`);
      
      if (response.data.status === 'processing') {
        // Poll for updates if still processing
        setTimeout(fetchJobData, 2000);
        return;
      }
      
      setJobData(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch repository data');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!jobData?.download_url) return;
    
    try {
      const response = await axios.get(jobData.download_url, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${jobData.repo_name}-documentation.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Documentation downloaded successfully!');
    } catch (error) {
      toast.error('Failed to download documentation');
    }
  };

  const copyToClipboard = async (content: string, type: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedContent(type);
      setTimeout(() => setCopiedContent(null), 2000);
      toast.success(`${type} copied to clipboard!`);
    } catch (error) {
      toast.error('Failed to copy to clipboard');
    }
  };

  const getLanguageColor = (language: string): string => {
    const colors: Record<string, string> = {
      'JavaScript': '#f1e05a',
      'TypeScript': '#2b7489',
      'Python': '#3572A5',
      'Java': '#b07219',
      'C++': '#f34b7d',
      'C': '#555555',
      'C#': '#239120',
      'PHP': '#4F5D95',
      'Ruby': '#701516',
      'Go': '#00ADD8',
      'Rust': '#dea584',
      'Swift': '#ffac45',
      'Kotlin': '#F18E33',
      'HTML': '#e34c26',
      'CSS': '#1572B6',
      'SCSS': '#c6538c'
    };
    return colors[language] || '#333333';
  };

  const getFileIcon = (fileName: string) => {
    const ext = fileName.split('.').pop()?.toLowerCase();
    if (['md', 'txt', 'rst'].includes(ext || '')) return FileText;
    if (['js', 'ts', 'py', 'java', 'cpp', 'c', 'cs', 'php', 'rb', 'go', 'rs'].includes(ext || '')) return Code;
    return File;
  };

  const buildFileTree = (): FileTreeItem[] => {
    if (!jobData?.documentation) return [];

    const files: FileTreeItem[] = [
      { name: 'README.md', type: 'file', content: jobData.documentation.readme },
      { name: 'CONTRIBUTING.md', type: 'file', content: jobData.documentation.contributing_guide },
      { name: 'CHANGELOG.md', type: 'file', content: jobData.documentation.changelog },
      { name: 'LICENSE', type: 'file', content: jobData.documentation.license },
      { name: '.gitignore', type: 'file', content: jobData.documentation.gitignore },
      { name: 'Dockerfile', type: 'file', content: jobData.documentation.dockerfile },
    ];

    // Add docs folder
    const docsFiles: FileTreeItem[] = [
      { name: 'api.md', type: 'file', content: jobData.documentation.api_docs },
      { name: 'setup.md', type: 'file', content: jobData.documentation.setup_guide },
      { name: 'architecture.md', type: 'file', content: jobData.documentation.architecture_docs },
    ];

    // Add additional files
    Object.entries(jobData.documentation.additional_files || {}).forEach(([path, content]) => {
      const pathParts = path.split('/');
      if (pathParts.length > 1) {
        docsFiles.push({ name: pathParts[pathParts.length - 1], type: 'file', content });
      }
    });

    files.push({
      name: 'docs',
      type: 'folder',
      children: docsFiles
    });

    return files;
  };

  const tabs = [
    { id: 'readme', label: 'README', icon: Book },
    { id: 'files', label: 'Code', icon: Code },
    { id: 'docs', label: 'Documentation', icon: FileText },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin text-blue-500 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">Loading repository data...</p>
          {jobData?.status === 'processing' && (
            <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
              Analysis in progress, please wait...
            </p>
          )}
        </div>
      </div>
    );
  }

  if (error || !jobData) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
            Error Loading Repository
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            {error || 'Repository data not found'}
          </p>
          <button
            onClick={() => navigate('/analyze')}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Try Another Repository
          </button>
        </div>
      </div>
    );
  }

  const repository = jobData.analysis?.repository_info;
  const fileStructure = jobData.analysis?.file_structure;
  const technologies = jobData.analysis?.technologies;
  const fileTree = buildFileTree();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      {/* Repository Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              {/* Breadcrumb */}
              <nav className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400 mb-2">
                <span>{jobData.repo_owner}</span>
                <ChevronRight className="h-4 w-4" />
                <span className="text-blue-600 dark:text-blue-400">{jobData.repo_name}</span>
              </nav>

              {/* Repository Title */}
              <div className="flex items-center space-x-3 mb-4">
                <Book className="h-6 w-6 text-gray-600 dark:text-gray-400" />
                <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {jobData.repo_name}
                </h1>
                <span className="px-2 py-1 text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-full border">
                  Generated Documentation
                </span>
              </div>

              {/* Description */}
              {repository?.description && (
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  {repository.description}
                </p>
              )}

              {/* Stats */}
              {repository && (
                <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4" />
                    <span>{repository.stargazers_count}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <GitFork className="h-4 w-4" />
                    <span>{repository.forks_count}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Eye className="h-4 w-4" />
                    <span>Watching</span>
                  </div>
                  {repository.language && (
                    <div className="flex items-center space-x-1">
                      <div 
                        className="h-3 w-3 rounded-full"
                        style={{ backgroundColor: getLanguageColor(repository.language) }}
                      />
                      <span>{repository.language}</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-2 ml-6">
              {repository?.html_url && (
                <a
                  href={repository.html_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-1 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                >
                  <ExternalLink className="h-4 w-4" />
                  <span>View Original</span>
                </a>
              )}
              
              <button
                onClick={handleDownload}
                disabled={!jobData.download_url}
                className="flex items-center space-x-1 px-3 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed rounded-lg transition-colors"
              >
                <Download className="h-4 w-4" />
                <span>Download</span>
              </button>
            </div>
          </div>

          {/* Topics */}
          {repository?.topics && repository.topics.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-4">
              {repository.topics.map((topic) => (
                <span
                  key={topic}
                  className="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full"
                >
                  {topic}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="lg:grid lg:grid-cols-4 lg:gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1 mb-6 lg:mb-0">
            {/* About */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-4">
              <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">About</h3>
              
              {repository?.description && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  {repository.description}
                </p>
              )}

              <div className="space-y-2 text-sm">
                {repository?.html_url && (
                  <div className="flex items-center space-x-2">
                    <ExternalLink className="h-4 w-4 text-gray-400" />
                    <a
                      href={repository.html_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 dark:text-blue-400 hover:underline truncate"
                    >
                      {repository.html_url.replace('https://', '')}
                    </a>
                  </div>
                )}

                {repository?.license && (
                  <div className="flex items-center space-x-2">
                    <Tag className="h-4 w-4 text-gray-400" />
                    <span className="text-gray-600 dark:text-gray-400">
                      {repository.license.name}
                    </span>
                  </div>
                )}

                <div className="flex items-center space-x-2">
                  <Calendar className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-600 dark:text-gray-400">
                    Generated {new Date(jobData.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>

            {/* Languages */}
            {fileStructure?.languages && Object.keys(fileStructure.languages).length > 0 && (
              <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-4">
                <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">Languages</h3>
                <div className="space-y-2">
                  {Object.entries(fileStructure.languages).map(([language, count]) => (
                    <div key={language} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <div 
                          className="h-3 w-3 rounded-full"
                          style={{ backgroundColor: getLanguageColor(language) }}
                        />
                        <span className="text-sm text-gray-600 dark:text-gray-400">{language}</span>
                      </div>
                      <span className="text-sm text-gray-500 dark:text-gray-500">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Technologies */}
            {technologies && (
              <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
                <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">Technologies</h3>
                <div className="space-y-3">
                  {technologies.frameworks.length > 0 && (
                    <div>
                      <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">
                        Frameworks
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {technologies.frameworks.map((framework) => (
                          <span
                            key={framework}
                            className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded"
                          >
                            {framework}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {technologies.deployment.length > 0 && (
                    <div>
                      <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">
                        Deployment
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {technologies.deployment.map((tool) => (
                          <span
                            key={tool}
                            className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded"
                          >
                            {tool}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {/* Tabs */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
              <div className="border-b border-gray-200 dark:border-gray-700">
                <nav className="flex space-x-8 px-6">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex items-center space-x-2 py-4 text-sm font-medium border-b-2 transition-colors ${
                          activeTab === tab.id
                            ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                            : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                        }`}
                      >
                        <Icon className="h-4 w-4" />
                        <span>{tab.label}</span>
                      </button>
                    );
                  })}
                </nav>
              </div>

              {/* Tab Content */}
              <div className="p-6">
                {activeTab === 'readme' && jobData.documentation?.readme && (
                  <div className="prose dark:prose-invert max-w-none">
                    <div className="flex justify-end mb-4">
                      <button
                        onClick={() => copyToClipboard(jobData.documentation!.readme, 'README')}
                        className="flex items-center space-x-1 px-3 py-1 text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
                      >
                        {copiedContent === 'README' ? (
                          <Check className="h-3 w-3" />
                        ) : (
                          <Copy className="h-3 w-3" />
                        )}
                        <span>Copy</span>
                      </button>
                    </div>
                    <ReactMarkdown>{jobData.documentation.readme}</ReactMarkdown>
                  </div>
                )}

                {activeTab === 'files' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                        Generated Files
                      </h3>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        {fileTree.length} items
                      </span>
                    </div>
                    
                    <div className="border border-gray-200 dark:border-gray-700 rounded-lg">
                      {fileTree.map((item, index) => (
                        <div key={index}>
                          <div
                            className={`flex items-center space-x-3 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer ${
                              index !== fileTree.length - 1 ? 'border-b border-gray-200 dark:border-gray-700' : ''
                            }`}
                            onClick={() => {
                              if (item.type === 'file') {
                                setSelectedFile(item.content || '');
                              }
                            }}
                          >
                            {item.type === 'folder' ? (
                              <Folder className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                            ) : (
                              React.createElement(getFileIcon(item.name), { 
                                className: "h-4 w-4 text-gray-600 dark:text-gray-400" 
                              })
                            )}
                            <span className="text-sm text-gray-900 dark:text-gray-100">
                              {item.name}
                            </span>
                            {item.type === 'folder' && item.children && (
                              <span className="text-xs text-gray-500 dark:text-gray-400">
                                ({item.children.length} files)
                              </span>
                            )}
                          </div>
                          
                          {item.type === 'folder' && item.children && (
                            <div className="pl-8 bg-gray-50 dark:bg-gray-750">
                              {item.children.map((child, childIndex) => (
                                <div
                                  key={childIndex}
                                  className="flex items-center space-x-3 px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer border-b border-gray-200 dark:border-gray-700 last:border-b-0"
                                  onClick={() => {
                                    if (child.content) {
                                      setSelectedFile(child.content);
                                    }
                                  }}
                                >
                                  {React.createElement(getFileIcon(child.name), { 
                                    className: "h-4 w-4 text-gray-600 dark:text-gray-400" 
                                  })}
                                  <span className="text-sm text-gray-900 dark:text-gray-100">
                                    {child.name}
                                  </span>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>

                    {selectedFile && (
                      <div className="mt-6">
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="text-md font-medium text-gray-900 dark:text-gray-100">
                            File Content
                          </h4>
                          <button
                            onClick={() => copyToClipboard(selectedFile, 'File Content')}
                            className="flex items-center space-x-1 px-3 py-1 text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
                          >
                            {copiedContent === 'File Content' ? (
                              <Check className="h-3 w-3" />
                            ) : (
                              <Copy className="h-3 w-3" />
                            )}
                            <span>Copy</span>
                          </button>
                        </div>
                        
                        <pre className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg overflow-x-auto text-sm text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-700">
                          <code>{selectedFile}</code>
                        </pre>
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'docs' && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {[
                        { key: 'api_docs', title: 'API Documentation', icon: Code },
                        { key: 'setup_guide', title: 'Setup Guide', icon: Book },
                        { key: 'architecture_docs', title: 'Architecture', icon: FileText },
                        { key: 'contributing_guide', title: 'Contributing', icon: User },
                      ].map((doc) => {
                        const Icon = doc.icon;
                        const content = jobData.documentation?.[doc.key as keyof typeof jobData.documentation];
                        return (
                          <div
                            key={doc.key}
                            className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-gray-300 dark:hover:border-gray-600 transition-colors cursor-pointer"
                            onClick={() => setSelectedFile(content as string)}
                          >
                            <div className="flex items-center space-x-2 mb-2">
                              <Icon className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                              <h4 className="font-medium text-gray-900 dark:text-gray-100">
                                {doc.title}
                              </h4>
                            </div>
                            <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                              {content ? 
                                (content as string).substring(0, 100) + '...' : 
                                'Click to view content'
                              }
                            </p>
                          </div>
                        );
                      })}
                    </div>

                    {selectedFile && (
                      <div className="mt-6">
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                            Documentation Content
                          </h4>
                          <button
                            onClick={() => copyToClipboard(selectedFile, 'Documentation')}
                            className="flex items-center space-x-1 px-3 py-1 text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
                          >
                            {copiedContent === 'Documentation' ? (
                              <Check className="h-3 w-3" />
                            ) : (
                              <Copy className="h-3 w-3" />
                            )}
                            <span>Copy</span>
                          </button>
                        </div>
                        
                        <div className="prose dark:prose-invert max-w-none">
                          <ReactMarkdown>{selectedFile}</ReactMarkdown>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RepositoryView;
