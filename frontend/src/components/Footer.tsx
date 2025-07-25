import React from 'react';
import { Code, FileText, Zap, Shield, Download, GitBranch } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Features Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-8">
          <div className="flex flex-col items-center text-center">
            <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg mb-2">
              <Code className="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-gray-100">AI Analysis</span>
            <span className="text-xs text-gray-500 dark:text-gray-400">Smart code parsing</span>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="p-2 bg-green-50 dark:bg-green-900/20 rounded-lg mb-2">
              <FileText className="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-gray-100">Auto Docs</span>
            <span className="text-xs text-gray-500 dark:text-gray-400">README & API docs</span>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="p-2 bg-purple-50 dark:bg-purple-900/20 rounded-lg mb-2">
              <Zap className="h-5 w-5 text-purple-600 dark:text-purple-400" />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-gray-100">Fast Setup</span>
            <span className="text-xs text-gray-500 dark:text-gray-400">One-click generation</span>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="p-2 bg-orange-50 dark:bg-orange-900/20 rounded-lg mb-2">
              <Shield className="h-5 w-5 text-orange-600 dark:text-orange-400" />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-gray-100">Secure</span>
            <span className="text-xs text-gray-500 dark:text-gray-400">Private processing</span>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="p-2 bg-cyan-50 dark:bg-cyan-900/20 rounded-lg mb-2">
              <Download className="h-5 w-5 text-cyan-600 dark:text-cyan-400" />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-gray-100">Export</span>
            <span className="text-xs text-gray-500 dark:text-gray-400">Multiple formats</span>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="p-2 bg-pink-50 dark:bg-pink-900/20 rounded-lg mb-2">
              <GitBranch className="h-5 w-5 text-pink-600 dark:text-pink-400" />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-gray-100">Git Ready</span>
            <span className="text-xs text-gray-500 dark:text-gray-400">GitHub optimized</span>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-200 dark:border-gray-800 pt-6 text-center">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            © 2024 Documentation.AI. Built for developers.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
