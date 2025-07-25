import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-hot-toast';

const AnalysisPage = () => {
  const navigate = useNavigate();
  const [repoUrl, setRepoUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!repoUrl.trim()) {
      toast.error('Please enter a repository URL');
      return;
    }

    if (!repoUrl.includes('github.com')) {
      toast.error('Please enter a valid GitHub repository URL');
      return;
    }

    setIsAnalyzing(true);
    setProgress(0);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 1000);

      const response = await axios.post('/api/analyze', {
        repo_url: repoUrl
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (response.data.job_id) {
        toast.success('Analysis completed successfully!');
        // Navigate to repository view
        navigate(`/repository/${response.data.job_id}`);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Analysis failed. Please try again.');
      setProgress(0);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="pt-24 pb-20 px-4 min-h-screen">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Analyze Your Repository
          </h1>
          <p className="text-xl text-white/70 max-w-2xl mx-auto">
            Enter your GitHub repository URL and let our AI create comprehensive documentation for your project.
          </p>
        </div>

        {/* Analysis Form */}
        <div className="glass p-8 rounded-2xl mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="repo-url" className="block text-lg font-medium text-white mb-3">
                GitHub Repository URL
              </label>
              <input
                type="url"
                id="repo-url"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="w-full px-4 py-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all duration-300"
                disabled={isAnalyzing}
              />
            </div>

            <button
              type="submit"
              disabled={isAnalyzing}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-300 flex items-center justify-center space-x-2"
            >
              {isAnalyzing ? (
                <>
                  <div className="spinner"></div>
                  <span>Analyzing Repository...</span>
                </>
              ) : (
                <span>Start Analysis</span>
              )}
            </button>
          </form>

          {/* Progress Bar */}
          {isAnalyzing && (
            <div className="mt-6">
              <div className="flex justify-between text-sm text-white/70 mb-2">
                <span>Analysis Progress</span>
                <span>{progress}%</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              
              <div className="mt-4 text-center text-white/60">
                {progress < 30 && "Cloning repository..."}
                {progress >= 30 && progress < 60 && "Analyzing code structure..."}
                {progress >= 60 && progress < 90 && "Generating documentation..."}
                {progress >= 90 && "Finalizing results..."}
              </div>
            </div>
          )}
        </div>

        {/* Example Repositories */}
        <div className="glass p-6 rounded-2xl">
          <h3 className="text-xl font-semibold text-white mb-4">Try These Example Repositories</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              {
                name: 'React Todo App',
                url: 'https://github.com/facebook/react',
                description: 'Popular React library repository'
              },
              {
                name: 'Express.js Framework',
                url: 'https://github.com/expressjs/express',
                description: 'Fast, unopinionated, minimalist web framework'
              },
              {
                name: 'Python Flask',
                url: 'https://github.com/pallets/flask',
                description: 'Lightweight WSGI web application framework'
              },
              {
                name: 'Vue.js Framework',
                url: 'https://github.com/vuejs/vue',
                description: 'Progressive JavaScript framework'
              }
            ].map((repo, index) => (
              <button
                key={index}
                onClick={() => setRepoUrl(repo.url)}
                className="text-left p-4 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all duration-300 group"
                disabled={isAnalyzing}
              >
                <h4 className="font-medium text-white group-hover:text-blue-300 transition-colors duration-300">
                  {repo.name}
                </h4>
                <p className="text-sm text-white/60 mt-1">{repo.description}</p>
                <p className="text-xs text-blue-400 mt-2 truncate">{repo.url}</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;
