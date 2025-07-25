import React, { useState } from 'react';
import { 
  Star, 
  GitFork, 
  Eye, 
  Download, 
  Code, 
  Book, 
  Code2,
  Settings,
  GitBranch,
  Users,
  Activity,
  ExternalLink,
  Copy,
  Check,
  Tag,
  AlertCircle,
  Shield,
  Clock,
  Package,
  User,
  ChevronRight,
  FileText,
  Image,
  Terminal,
  Play
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/hljs';

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
  maintainers?: Array<{
    login: string;
    avatar_url: string;
    html_url: string;
    type: string;
  }>;
  dependencies?: Array<{
    name: string;
    version?: string;
    type: 'runtime' | 'dev' | 'peer';
  }>;
}

interface GitHubRepoProps {
  repository: Repository;
  documentation: {
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
  downloadUrl?: string;
}

const languageColors: Record<string, string> = {
  'TypeScript': '#3178c6',
  'JavaScript': '#f1e05a',
  'Python': '#3572A5',
  'Java': '#b07219',
  'C++': '#f34b7d',
  'C': '#555555',
  'C#': '#239120',
  'PHP': '#4F5D95',
  'Go': '#00ADD8',
  'Rust': '#dea584',
  'Swift': '#fa7343',
  'Kotlin': '#A97BFF',
  'Ruby': '#701516',
  'Scala': '#c22d40',
  'HTML': '#e34c26',
  'CSS': '#1572B6',
  'Shell': '#89e051',
  'Dockerfile': '#384d54',
  'Vue': '#4FC08D',
  'React': '#61DAFB',
};

const GitHubRepoPreview: React.FC<GitHubRepoProps> = ({ 
  repository, 
  documentation, 
  downloadUrl 
}) => {
  const [activeTab, setActiveTab] = useState<string>('readme');
  const [copiedLink, setCopiedLink] = useState(false);
  const [previewMode, setPreviewMode] = useState<'preview' | 'code'>('preview');

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatNumber = (num: number) => {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedLink(true);
      setTimeout(() => setCopiedLink(false), 2000);
    } catch (err) {
      console.error('Failed to copy to clipboard');
    }
  };

  const downloadContent = (content: string, filename: string) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  const getCurrentContent = () => {
    const content = documentation[activeTab as keyof typeof documentation];
    if (typeof content === 'string') {
      return content || 'No content available.';
    } else if (typeof content === 'object' && content !== null) {
      return Object.entries(content)
        .map(([filename, fileContent]) => `## ${filename}\n\n${fileContent}`)
        .join('\n\n') || 'No content available.';
    }
    return 'No content available.';
  };

  // Enhanced markdown components for GitHub-like rendering
  const markdownComponents = {
    code: ({ node, inline, className, children, ...props }: any) => {
      const match = /language-(\w+)/.exec(className || '');
      const language = match ? match[1] : '';
      
      if (inline) {
        return (
          <code className="bg-gray-100 dark:bg-gray-800 text-red-600 dark:text-red-400 px-1 py-0.5 rounded text-sm font-mono" {...props}>
            {children}
          </code>
        );
      }
      
      return (
        <div className="relative">
          <SyntaxHighlighter
            style={tomorrow}
            language={language}
            PreTag="div"
            className="rounded-lg border border-gray-200 dark:border-gray-700"
            customStyle={{
              margin: '0',
              background: 'var(--tw-bg-opacity)',
            }}
          >
            {String(children).replace(/\n$/, '')}
          </SyntaxHighlighter>
        </div>
      );
    },
    blockquote: ({ children }: any) => (
      <blockquote className="border-l-4 border-gray-300 dark:border-gray-600 pl-4 py-2 my-4 bg-gray-50 dark:bg-gray-800/50 italic">
        {children}
      </blockquote>
    ),
    table: ({ children }: any) => (
      <div className="overflow-x-auto my-4">
        <table className="min-w-full border border-gray-200 dark:border-gray-700 rounded-lg">
          {children}
        </table>
      </div>
    ),
    thead: ({ children }: any) => (
      <thead className="bg-gray-50 dark:bg-gray-800">
        {children}
      </thead>
    ),
    th: ({ children }: any) => (
      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100 border-b border-gray-200 dark:border-gray-700">
        {children}
      </th>
    ),
    td: ({ children }: any) => (
      <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700">
        {children}
      </td>
    ),
    h1: ({ children }: any) => (
      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4 pb-2 border-b border-gray-200 dark:border-gray-700">
        {children}
      </h1>
    ),
    h2: ({ children }: any) => (
      <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-3 pb-2 border-b border-gray-200 dark:border-gray-700">
        {children}
      </h2>
    ),
    h3: ({ children }: any) => (
      <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
        {children}
      </h3>
    ),
    a: ({ href, children }: any) => (
      <a 
        href={href} 
        target="_blank" 
        rel="noopener noreferrer"
        className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 underline"
      >
        {children}
      </a>
    ),
    img: ({ src, alt }: any) => (
      <img 
        src={src} 
        alt={alt} 
        className="max-w-full h-auto rounded-lg border border-gray-200 dark:border-gray-700"
      />
    ),
  };

  const tabs = [
    { key: 'readme', label: 'README', icon: Book, color: 'text-blue-600' },
    { key: 'api_docs', label: 'API Docs', icon: Code2, color: 'text-green-600' },
    { key: 'setup_guide', label: 'Setup', icon: Settings, color: 'text-purple-600' },
    { key: 'architecture_docs', label: 'Architecture', icon: GitBranch, color: 'text-orange-600' },
    { key: 'contributing_guide', label: 'Contributing', icon: Users, color: 'text-pink-600' },
    { key: 'changelog', label: 'Changelog', icon: Activity, color: 'text-indigo-600' },
  ];

  const getLanguageColor = (language: string) => {
    return languageColors[language] || '#586069';
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* GitHub-style Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          {/* Repository Info */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <Book className="h-6 w-6 text-gray-600 dark:text-gray-400" />
              <nav className="flex items-center space-x-1 text-sm">
                <a 
                  href={repository.html_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 dark:text-blue-400 hover:underline font-semibold"
                >
                  {repository.full_name.split('/')[0]}
                </a>
                <span className="text-gray-500 dark:text-gray-400">/</span>
                <span className="text-gray-900 dark:text-gray-100 font-semibold">
                  {repository.name}
                </span>
              </nav>
              <span className="px-2 py-1 text-xs font-medium border border-gray-300 dark:border-gray-600 rounded-full text-gray-700 dark:text-gray-300">
                Public
              </span>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-2">
              <button className="px-3 py-1.5 text-sm font-medium rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center space-x-1">
                <Eye className="h-4 w-4" />
                <span>Watch</span>
                <span className="bg-gray-200 dark:bg-gray-600 px-1.5 py-0.5 rounded-full text-xs">
                  {formatNumber(Math.floor(repository.stargazers_count * 0.1))}
                </span>
              </button>

              <button className="px-3 py-1.5 text-sm font-medium rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center space-x-1">
                <Star className="h-4 w-4" />
                <span>Star</span>
                <span className="bg-gray-200 dark:bg-gray-600 px-1.5 py-0.5 rounded-full text-xs">
                  {formatNumber(repository.stargazers_count)}
                </span>
              </button>

              <button className="px-3 py-1.5 text-sm font-medium rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center space-x-1">
                <GitFork className="h-4 w-4" />
                <span>Fork</span>
                <span className="bg-gray-200 dark:bg-gray-600 px-1.5 py-0.5 rounded-full text-xs">
                  {formatNumber(repository.forks_count)}
                </span>
              </button>

              {downloadUrl && (
                <a
                  href={downloadUrl}
                  className="px-3 py-1.5 text-sm font-medium rounded-md bg-green-600 text-white hover:bg-green-700 transition-colors flex items-center space-x-1"
                >
                  <Download className="h-4 w-4" />
                  <span>Download</span>
                </a>
              )}
            </div>
          </div>

          {/* Description and Topics */}
          <div className="mb-4">
            <p className="text-gray-700 dark:text-gray-300 mb-3">
              {repository.description}
            </p>
            
            {repository.topics && repository.topics.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {repository.topics.map((topic) => (
                  <span
                    key={topic}
                    className="px-2.5 py-1 text-xs font-medium bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full border border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-900/50 cursor-pointer transition-colors"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Stats */}
          <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400 mb-4">
            {repository.language && (
              <div className="flex items-center space-x-1">
                <div 
                  className="w-3 h-3 rounded-full"
                  // eslint-disable-next-line react/forbid-dom-props
                  style={{ backgroundColor: getLanguageColor(repository.language) }}
                />
                <span>{repository.language}</span>
              </div>
            )}
            
            {repository.license && (
              <div className="flex items-center space-x-1">
                <Shield className="h-4 w-4" />
                <span>{repository.license.name}</span>
              </div>
            )}

            <div className="flex items-center space-x-1">
              <Clock className="h-4 w-4" />
              <span>Updated {formatDate(repository.updated_at)}</span>
            </div>

            <div className="flex items-center space-x-1">
              <AlertCircle className="h-4 w-4" />
              <span>{repository.open_issues_count} issues</span>
            </div>
          </div>

          {/* Code Section */}
          <div className="flex items-center space-x-2">
            <div className="flex items-center">
              <button className="px-3 py-1.5 text-sm font-medium bg-green-600 text-white rounded-l-md hover:bg-green-700 transition-colors flex items-center space-x-1">
                <Code className="h-4 w-4" />
                <span>Code</span>
              </button>
              <button 
                onClick={() => copyToClipboard(repository.html_url)}
                className="px-2 py-1.5 bg-green-600 text-white rounded-r-md hover:bg-green-700 transition-colors border-l border-green-700"
              >
                {copiedLink ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
              </button>
            </div>
            
            <a
              href={repository.html_url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-1.5 text-sm font-medium border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors flex items-center space-x-1"
            >
              <ExternalLink className="h-4 w-4" />
              <span>View on GitHub</span>
            </a>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Documentation Content */}
          <div className="lg:col-span-3">
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
              <div className="border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <nav className="flex space-x-1 p-2">
                    {tabs.map((tab) => {
                      const Icon = tab.icon;
                      return (
                        <button
                          key={tab.key}
                          onClick={() => setActiveTab(tab.key)}
                          className={`px-3 py-2 text-sm font-medium rounded-md flex items-center space-x-1 transition-colors border ${
                            activeTab === tab.key
                              ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-700'
                              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 border-transparent'
                          }`}
                        >
                          <Icon className={`h-4 w-4 ${activeTab === tab.key ? tab.color : ''}`} />
                          <span>{tab.label}</span>
                        </button>
                      );
                    })}
                  </nav>
                  
                  {/* Preview/Code Toggle */}
                  <div className="flex items-center space-x-1 p-2 border-l border-gray-200 dark:border-gray-700">
                    <button
                      onClick={() => copyToClipboard(getCurrentContent())}
                      className="px-2 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors flex items-center space-x-1"
                      title="Copy content"
                    >
                      {copiedLink ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                    </button>
                    <button
                      onClick={() => downloadContent(getCurrentContent(), `${activeTab}.md`)}
                      className="px-2 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors flex items-center space-x-1"
                      title="Download file"
                    >
                      <Download className="h-4 w-4" />
                    </button>
                    <div className="w-px h-6 bg-gray-200 dark:bg-gray-700"></div>
                    <button
                      onClick={() => setPreviewMode('preview')}
                      className={`px-3 py-1.5 text-sm font-medium rounded-l-md flex items-center space-x-1 transition-colors ${
                        previewMode === 'preview'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                      }`}
                    >
                      <Eye className="h-4 w-4" />
                      <span>Preview</span>
                    </button>
                    <button
                      onClick={() => setPreviewMode('code')}
                      className={`px-3 py-1.5 text-sm font-medium rounded-r-md flex items-center space-x-1 transition-colors ${
                        previewMode === 'code'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                      }`}
                    >
                      <Code className="h-4 w-4" />
                      <span>Code</span>
                    </button>
                  </div>
                </div>
              </div>

              {/* Content Display */}
              <div className="relative">
                {previewMode === 'preview' ? (
                  <div className="p-6">
                    <div className="prose prose-lg dark:prose-invert max-w-none prose-headings:text-gray-900 dark:prose-headings:text-gray-100 prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-a:text-blue-600 dark:prose-a:text-blue-400 prose-strong:text-gray-900 dark:prose-strong:text-gray-100 prose-code:text-red-600 dark:prose-code:text-red-400 prose-pre:bg-gray-900 dark:prose-pre:bg-gray-800">
                      <ReactMarkdown components={markdownComponents}>
                        {(() => {
                          const content = documentation[activeTab as keyof typeof documentation];
                          if (typeof content === 'string') {
                            return content || '# No content available\n\nThis section is currently empty.';
                          } else if (typeof content === 'object' && content !== null) {
                            // Handle additional_files object
                            const result = Object.entries(content)
                              .map(([filename, fileContent]) => `## ${filename}\n\n\`\`\`\n${fileContent}\n\`\`\``)
                              .join('\n\n');
                            return result || '# No content available\n\nThis section is currently empty.';
                          }
                          return '# No content available\n\nThis section is currently empty.';
                        })()}
                      </ReactMarkdown>
                    </div>
                  </div>
                ) : (
                  <div className="p-0">
                    <SyntaxHighlighter
                      language="markdown"
                      style={tomorrow}
                      customStyle={{
                        margin: 0,
                        borderRadius: 0,
                        background: 'transparent',
                      }}
                      className="!bg-gray-50 dark:!bg-gray-900 text-sm"
                    >
                      {(() => {
                        const content = documentation[activeTab as keyof typeof documentation];
                        if (typeof content === 'string') {
                          return content || 'No content available.';
                        } else if (typeof content === 'object' && content !== null) {
                          return Object.entries(content)
                            .map(([filename, fileContent]) => `## ${filename}\n\n${fileContent}`)
                            .join('\n\n') || 'No content available.';
                        }
                        return 'No content available.';
                      })()}
                    </SyntaxHighlighter>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* About */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">About</h3>
              <p className="text-sm text-gray-700 dark:text-gray-300 mb-4">
                {repository.description}
              </p>

              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Stars</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">
                    {formatNumber(repository.stargazers_count)}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Forks</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">
                    {formatNumber(repository.forks_count)}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Watchers</span>
                  <span className="font-medium text-gray-900 dark:text-gray-100">
                    {formatNumber(Math.floor(repository.stargazers_count * 0.1))}
                  </span>
                </div>
              </div>

              {repository.topics && repository.topics.length > 0 && (
                <div className="mt-4">
                  <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">Topics</h4>
                  <div className="flex flex-wrap gap-1">
                    {repository.topics.slice(0, 6).map((topic) => (
                      <span
                        key={topic}
                        className="px-2 py-1 text-xs bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded cursor-pointer hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors"
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Releases */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Releases</h3>
                <Tag className="h-5 w-5 text-gray-500 dark:text-gray-400" />
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                No releases published
              </div>
              <button className="text-sm text-blue-600 dark:text-blue-400 hover:underline mt-2">
                Create a new release
              </button>
            </div>

            {/* Languages */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">Languages</h3>
              {repository.language && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-2">
                      <div 
                        className="w-3 h-3 rounded-full"
                        // eslint-disable-next-line react/forbid-dom-props
                        style={{ backgroundColor: getLanguageColor(repository.language) }}
                      />
                      <span className="text-gray-900 dark:text-gray-100">{repository.language}</span>
                    </div>
                    <span className="text-gray-600 dark:text-gray-400">100%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      className="h-2 rounded-full"
                      // eslint-disable-next-line react/forbid-dom-props
                      style={{ 
                        backgroundColor: getLanguageColor(repository.language),
                        width: '100%'
                      }}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Maintainers */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Contributors</h3>
                <Users className="h-5 w-5 text-gray-500 dark:text-gray-400" />
              </div>
              
              {repository.maintainers && repository.maintainers.length > 0 ? (
                <div className="space-y-3">
                  {repository.maintainers.slice(0, 5).map((maintainer) => (
                    <a
                      key={maintainer.login}
                      href={maintainer.html_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors group"
                    >
                      <img
                        src={maintainer.avatar_url}
                        alt={maintainer.login}
                        className="w-8 h-8 rounded-full border border-gray-200 dark:border-gray-600"
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-1">
                          <span className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                            {maintainer.login}
                          </span>
                          {maintainer.type === 'Organization' && (
                            <span className="px-1.5 py-0.5 text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded">
                              ORG
                            </span>
                          )}
                        </div>
                      </div>
                      <ExternalLink className="w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </a>
                  ))}
                  
                  {repository.maintainers.length > 5 && (
                    <div className="text-sm text-gray-500 dark:text-gray-400 text-center pt-2">
                      +{repository.maintainers.length - 5} more contributors
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex items-center space-x-3 p-2">
                  <img
                    src={`https://github.com/${repository.full_name.split('/')[0]}.png`}
                    alt={repository.full_name.split('/')[0]}
                    className="w-8 h-8 rounded-full border border-gray-200 dark:border-gray-600"
                  />
                  <div className="flex-1">
                    <a
                      href={`https://github.com/${repository.full_name.split('/')[0]}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
                    >
                      {repository.full_name.split('/')[0]}
                    </a>
                  </div>
                </div>
              )}
            </div>

            {/* Key Dependencies */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Dependencies</h3>
                <Package className="h-5 w-5 text-gray-500 dark:text-gray-400" />
              </div>
              
              {repository.dependencies && repository.dependencies.length > 0 ? (
                <div className="space-y-2">
                  {repository.dependencies.slice(0, 8).map((dep, index) => (
                    <div key={index} className="flex items-center justify-between py-1">
                      <div className="flex items-center space-x-2 flex-1 min-w-0">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          dep.type === 'runtime' 
                            ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
                            : dep.type === 'dev'
                            ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300'
                        }`}>
                          {dep.type}
                        </span>
                        <span className="text-sm text-gray-900 dark:text-gray-100 truncate font-mono">
                          {dep.name}
                        </span>
                      </div>
                      {dep.version && (
                        <span className="text-xs text-gray-500 dark:text-gray-400 font-mono">
                          {dep.version}
                        </span>
                      )}
                    </div>
                  ))}
                  
                  {repository.dependencies.length > 8 && (
                    <div className="text-sm text-gray-500 dark:text-gray-400 text-center pt-2 border-t border-gray-200 dark:border-gray-700">
                      +{repository.dependencies.length - 8} more dependencies
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  No dependencies detected
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GitHubRepoPreview;

export type { Repository, GitHubRepoProps };
