import React, { useState, useEffect } from 'react';
import axios from 'axios';

const HistoryPage = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get('/api/jobs');
      setJobs(response.data);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-400 bg-green-400/20';
      case 'processing':
        return 'text-yellow-400 bg-yellow-400/20';
      case 'failed':
        return 'text-red-400 bg-red-400/20';
      default:
        return 'text-gray-400 bg-gray-400/20';
    }
  };

  if (loading) {
    return (
      <div className="pt-24 pb-20 px-4 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mb-4"></div>
          <p className="text-white/70">Loading analysis history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pt-24 pb-20 px-4 min-h-screen">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Analysis History
          </h1>
          <p className="text-xl text-white/70 max-w-2xl mx-auto">
            View your previous repository analysis results and generated documentation.
          </p>
        </div>

        {/* Jobs List */}
        {jobs.length === 0 ? (
          <div className="text-center py-20">
            <div className="glass p-12 rounded-2xl max-w-md mx-auto">
              <h3 className="text-2xl font-semibold text-white mb-4">No Analysis History</h3>
              <p className="text-white/70 mb-6">
                You haven't analyzed any repositories yet. Start by analyzing your first repository!
              </p>
              <a
                href="/analyze"
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 inline-block"
              >
                Analyze Repository
              </a>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {jobs.map((job: any) => (
              <div key={job.job_id} className="glass p-6 rounded-2xl hover:shadow-2xl transition-all duration-300">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-white truncate">
                        {job.repo_url.split('/').slice(-2).join('/')}
                      </h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(job.status)}`}>
                        {job.status}
                      </span>
                    </div>
                    
                    <p className="text-white/60 text-sm mb-2">{job.repo_url}</p>
                    
                    <p className="text-white/50 text-xs">
                      Analyzed on {new Date(job.created_at).toLocaleDateString()} at{' '}
                      {new Date(job.created_at).toLocaleTimeString()}
                    </p>
                  </div>

                  <div className="flex space-x-3 mt-4 md:mt-0">
                    {job.status === 'completed' && (
                      <a
                        href={`/results/${job.job_id}`}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300"
                      >
                        View Results
                      </a>
                    )}
                    
                    {job.status === 'processing' && (
                      <span className="bg-yellow-600/20 text-yellow-400 px-4 py-2 rounded-lg text-sm">
                        Processing...
                      </span>
                    )}
                    
                    {job.status === 'failed' && (
                      <a
                        href="/analyze"
                        className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300"
                      >
                        Retry Analysis
                      </a>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Statistics */}
        {jobs.length > 0 && (
          <div className="mt-16">
            <h2 className="text-2xl font-bold text-white mb-8 text-center">Statistics</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="glass p-6 rounded-2xl text-center">
                <div className="text-3xl font-bold text-blue-400 mb-2">
                  {jobs.length}
                </div>
                <div className="text-white/70">Total Analyses</div>
              </div>
              
              <div className="glass p-6 rounded-2xl text-center">
                <div className="text-3xl font-bold text-green-400 mb-2">
                  {jobs.filter((job: any) => job.status === 'completed').length}
                </div>
                <div className="text-white/70">Completed</div>
              </div>
              
              <div className="glass p-6 rounded-2xl text-center">
                <div className="text-3xl font-bold text-purple-400 mb-2">
                  {Math.round((jobs.filter((job: any) => job.status === 'completed').length / jobs.length) * 100)}%
                </div>
                <div className="text-white/70">Success Rate</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;
