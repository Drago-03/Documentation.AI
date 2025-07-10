import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-black/20 backdrop-blur-md border-t border-white/10 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">About Documentation.AI</h3>
            <p className="text-white/70 text-sm leading-relaxed">
              Automatically generate comprehensive documentation for your GitHub repositories using 
              advanced AI models and natural language processing.
            </p>
          </div>

          {/* Features */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Features</h3>
            <ul className="space-y-2 text-sm text-white/70">
              <li>• AI-powered code analysis</li>
              <li>• Automated README generation</li>
              <li>• API documentation</li>
              <li>• Architecture insights</li>
              <li>• Setup and deployment guides</li>
            </ul>
          </div>

          {/* Technology */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Built With</h3>
            <ul className="space-y-2 text-sm text-white/70">
              <li>• React & TypeScript</li>
              <li>• Python Flask API</li>
              <li>• Google Gemini AI</li>
              <li>• RAG Pipeline</li>
              <li>• TailwindCSS</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-white/10 mt-8 pt-8 text-center">
          <p className="text-white/50 text-sm">
            © 2024 Documentation.AI. Built with ❤️ for developers.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
