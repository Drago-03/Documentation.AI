import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

interface Documentation {
  readme: string;
  api_docs: string;
  setup_guide: string;
  architecture_docs: string;
  contributing_guide: string;
  changelog: string;
  deployment_guide: string;
  testing_guide: string;
  troubleshooting: string;
  additional_files: Record<string, string>;
}

interface JobResult {
  job_id: number;
  repo_url: string;
  status: string;
  created_at: string;
  documentation: Documentation;
}

const ResultsPage = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const [result, setResult] = useState<JobResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('readme');

  useEffect(() => {
    if (jobId) {
      fetchResults();
    }
  }, [jobId]);

  const fetchResults = async () => {
    try {
      const response = await axios.get(`/api/job/${jobId}`);
      
      if (response.data.status === 'completed') {
        setResult(response.data);
      } else if (response.data.status === 'processing') {
        // Poll for updates
        setTimeout(fetchResults, 2000);
        return;
      } else {
        setError('Analysis failed or job not found');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch results');
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = (content: string, filename: string) => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const tabs = [
    { id: 'readme', label: 'README.md', content: result?.documentation?.readme },
    { id: 'api', label: 'API Docs', content: result?.documentation?.api_docs },
    { id: 'setup', label: 'Setup Guide', content: result?.documentation?.setup_guide },
    { id: 'architecture', label: 'Architecture', content: result?.documentation?.architecture_docs },
    { id: 'contributing', label: 'Contributing', content: result?.documentation?.contributing_guide },
    { id: 'deployment', label: 'Deployment', content: result?.documentation?.deployment_guide },
  ];

  if (loading) {
    return (
      <div className="pt-24 pb-20 px-4 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mb-4"></div>
          <p className="text-white/70">Loading results...</p>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="pt-24 pb-20 px-4 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Error</h2>
          <p className="text-white/70">{error || 'Results not found'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pt-24 pb-20 px-4 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Documentation Results</h1>
          <p className="text-white/70">Repository: {result.repo_url}</p>
          <p className="text-white/50 text-sm">Generated on: {new Date(result.created_at).toLocaleString()}</p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4 mb-8">
          <button
            onClick={() => {
              if (result.documentation?.readme) {
                downloadFile(result.documentation.readme, 'README.md');
              }
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-300"
          >
            Download README
          </button>
          
          <button
            onClick={() => {
              const allDocs = Object.entries(result.documentation || {})
                .map(([key, value]) => `# ${key.toUpperCase()}\n\n${value}\n\n---\n\n`)
                .join('');
              downloadFile(allDocs, 'complete-documentation.md');
            }}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors duration-300"
          >
            Download All Docs
          </button>
        </div>

        {/* Tabs */}
        <div className="glass rounded-2xl overflow-hidden">
          {/* Tab Headers */}
          <div className="border-b border-white/10">
            <div className="flex flex-wrap">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-6 py-4 text-sm font-medium transition-colors duration-300 ${
                    activeTab === tab.id
                      ? 'text-white bg-white/10 border-b-2 border-blue-400'
                      : 'text-white/70 hover:text-white hover:bg-white/5'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          <div className="p-8">
            {tabs.map((tab) => (
              <div
                key={tab.id}
                className={`${activeTab === tab.id ? 'block' : 'hidden'}`}
              >
                {tab.content ? (
                  <div className="prose prose-invert max-w-none">
                    <ReactMarkdown
                      className="text-white/90 leading-relaxed"
                      components={{
                        h1: ({ children }) => <h1 className="text-3xl font-bold text-white mb-6">{children}</h1>,
                        h2: ({ children }) => <h2 className="text-2xl font-semibold text-white mb-4 mt-8">{children}</h2>,
                        h3: ({ children }) => <h3 className="text-xl font-medium text-white mb-3 mt-6">{children}</h3>,
                        p: ({ children }) => <p className="text-white/80 mb-4 leading-relaxed">{children}</p>,
                        code: ({ inline, children }) => 
                          inline ? (
                            <code className="bg-white/10 text-blue-300 px-2 py-1 rounded text-sm">{children}</code>
                          ) : (
                            <pre className="bg-black/30 p-4 rounded-lg overflow-x-auto">
                              <code className="text-green-300">{children}</code>
                            </pre>
                          ),
                        ul: ({ children }) => <ul className="list-disc list-inside text-white/80 mb-4 space-y-2">{children}</ul>,
                        li: ({ children }) => <li className="text-white/80">{children}</li>,
                        blockquote: ({ children }) => (
                          <blockquote className="border-l-4 border-blue-400 pl-4 italic text-white/70 mb-4">
                            {children}
                          </blockquote>
                        ),
                      }}
                    >
                      {tab.content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <div className="text-center text-white/50 py-12">
                    <p>No content available for this section</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Additional Files */}
        {result.documentation?.additional_files && Object.keys(result.documentation.additional_files).length > 0 && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold text-white mb-6">Additional Files</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(result.documentation.additional_files).map(([filename, content]) => (
                <div key={filename} className="glass p-4 rounded-xl">
                  <h3 className="font-semibold text-white mb-2">{filename}</h3>
                  <p className="text-white/60 text-sm mb-3">
                    {content.substring(0, 100)}...
                  </p>
                  <button
                    onClick={() => downloadFile(content, filename)}
                    className="text-blue-400 hover:text-blue-300 text-sm transition-colors duration-300"
                  >
                    Download File
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPage;
