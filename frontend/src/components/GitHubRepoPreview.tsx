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
  Clock
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';

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

  const tabs = [
    { key: 'readme', label: 'README', icon: Book },
    { key: 'api_docs', label: 'API Docs', icon: Code2 },
    { key: 'setup_guide', label: 'Setup', icon: Settings },
    { key: 'architecture_docs', label: 'Architecture', icon: GitBranch },
    { key: 'contributing_guide', label: 'Contributing', icon: Users },
    { key: 'changelog', label: 'Changelog', icon: Activity },
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
                <nav className="flex space-x-1 p-2">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <button
                        key={tab.key}
                        onClick={() => setActiveTab(tab.key)}
                        className={`px-3 py-2 text-sm font-medium rounded-md flex items-center space-x-1 transition-colors ${
                          activeTab === tab.key
                            ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
                            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                        }`}
                      >
                        <Icon className="h-4 w-4" />
                        <span>{tab.label}</span>
                      </button>
                    );
                  })}
                </nav>
              </div>

              {/* Content Display */}
              <div className="p-6">
                <div className="prose dark:prose-invert max-w-none">
                  <ReactMarkdown>
                    {(() => {
                      const content = documentation[activeTab as keyof typeof documentation];
                      if (typeof content === 'string') {
                        return content || 'No content available.';
                      }
                      return 'No content available.';
                    })()}
                  </ReactMarkdown>
                </div>
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
                        style={{ backgroundColor: getLanguageColor(repository.language) }}
                      />
                      <span className="text-gray-900 dark:text-gray-100">{repository.language}</span>
                    </div>
                    <span className="text-gray-600 dark:text-gray-400">100%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      className="h-2 rounded-full"
                      style={{ 
                        backgroundColor: getLanguageColor(repository.language),
                        width: '100%'
                      }}
                    />
                  </div>
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
