import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  RefreshCw,
  AlertCircle,
  Clock
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import GitHubRepoPreview, { Repository } from '../components/GitHubRepoPreview';

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
    technologies?: {
      frameworks: string[];
      databases: string[];
      tools: string[];
      deployment: string[];
    };
  };
  error_message?: string;
}

const RepositoryView: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  
  const [jobData, setJobData] = useState<JobData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

  if (!jobData.analysis || !jobData.documentation) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            Analysis Incomplete
          </h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-md">
            The repository analysis is incomplete or failed. Please try generating documentation again.
          </p>
        </div>
      </div>
    );
  }

  const repositoryData: Repository = {
    name: jobData.repo_name,
    full_name: `${jobData.repo_owner}/${jobData.repo_name}`,
    description: 'AI-generated documentation for this repository',
    html_url: jobData.repo_url,
    language: Object.keys(jobData.analysis?.file_structure?.languages || {})[0] || 'Unknown',
    stargazers_count: Math.floor(Math.random() * 1000) + 50, // Sample data
    forks_count: Math.floor(Math.random() * 200) + 10, // Sample data
    open_issues_count: Math.floor(Math.random() * 50) + 1, // Sample data
    created_at: jobData.created_at,
    updated_at: jobData.updated_at,
    topics: (jobData.analysis?.technologies?.frameworks || []).slice(0, 5),
    // Sample maintainers data
    maintainers: [
      {
        login: jobData.repo_owner,
        avatar_url: `https://github.com/${jobData.repo_owner}.png`,
        html_url: `https://github.com/${jobData.repo_owner}`,
        type: 'User'
      },
      // Add some sample contributors
      ...(jobData.analysis?.technologies?.frameworks || []).slice(0, 3).map((framework, index) => ({
        login: `contributor-${index + 1}`,
        avatar_url: `https://github.com/github.png`,
        html_url: `https://github.com/contributor-${index + 1}`,
        type: 'User' as const
      }))
    ],
    // Sample dependencies based on detected technologies
    dependencies: [
      // Runtime dependencies
      ...(jobData.analysis?.technologies?.frameworks || []).map(framework => ({
        name: framework.toLowerCase(),
        version: `^${Math.floor(Math.random() * 5) + 1}.${Math.floor(Math.random() * 10)}.${Math.floor(Math.random() * 10)}`,
        type: 'runtime' as const
      })),
      // Development dependencies
      {
        name: 'eslint',
        version: '^8.0.0',
        type: 'dev' as const
      },
      {
        name: 'typescript',
        version: '^5.0.0',
        type: 'dev' as const
      },
      {
        name: 'prettier',
        version: '^3.0.0',
        type: 'dev' as const
      }
    ].slice(0, 12) // Limit to 12 dependencies
  };

  return (
    <GitHubRepoPreview
      repository={repositoryData}
      documentation={jobData.documentation}
      downloadUrl={jobData.download_url}
    />
  );
};

export default RepositoryView;
