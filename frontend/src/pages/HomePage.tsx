import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Code, Sparkles, Zap, Shield, Cpu, Globe } from 'lucide-react';

const HomePage = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Code,
      title: 'AI Code Analysis',
      description: 'Advanced AI models analyze your repository structure, dependencies, and architecture patterns.',
      color: 'from-blue-400 to-blue-600'
    },
    {
      icon: Sparkles,
      title: 'Auto Documentation',
      description: 'Generate comprehensive README files, API docs, and setup guides automatically.',
      color: 'from-purple-400 to-purple-600'
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Process repositories in seconds with our optimized RAG pipeline and caching system.',
      color: 'from-yellow-400 to-orange-500'
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your code is analyzed securely without storing sensitive information permanently.',
      color: 'from-green-400 to-green-600'
    },
    {
      icon: Cpu,
      title: 'Smart Insights',
      description: 'Get architectural insights, complexity analysis, and improvement suggestions.',
      color: 'from-red-400 to-pink-600'
    },
    {
      icon: Globe,
      title: 'Multi-Language',
      description: 'Support for Python, JavaScript, Java, Go, Rust, and many other programming languages.',
      color: 'from-indigo-400 to-indigo-600'
    }
  ];

  return (
    <div className="pt-16">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-gradient">Documentation.AI</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-white/80 mb-8 max-w-3xl mx-auto leading-relaxed">
              Transform your GitHub repositories into professionally documented projects 
              with the power of AI and advanced natural language processing.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <motion.button
                onClick={() => navigate('/analyze')}
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-300 flex items-center space-x-2 group shadow-2xl"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <span>Start Analyzing</span>
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform duration-300" />
              </motion.button>

              <motion.button
                onClick={() => navigate('/history')}
                className="bg-white/10 backdrop-blur-md border border-white/20 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-300 hover:bg-white/20"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                View Examples
              </motion.button>
            </div>
          </motion.div>

          {/* Floating Animation */}
          <motion.div
            className="absolute top-20 left-10 w-20 h-20 bg-blue-500/20 rounded-full blur-xl"
            animate={{
              y: [-20, 20, -20],
              x: [-10, 10, -10],
            }}
            transition={{
              duration: 6,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          
          <motion.div
            className="absolute bottom-20 right-10 w-16 h-16 bg-purple-500/20 rounded-full blur-xl"
            animate={{
              y: [20, -20, 20],
              x: [10, -10, 10],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Powerful Features
            </h2>
            <p className="text-xl text-white/70 max-w-3xl mx-auto">
              Everything you need to create professional documentation for your projects
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="glass p-6 rounded-2xl hover:shadow-2xl transition-all duration-300 group cursor-pointer"
                  whileHover={{ scale: 1.02 }}
                >
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  
                  <h3 className="text-xl font-semibold text-white mb-3">
                    {feature.title}
                  </h3>
                  
                  <p className="text-white/70 leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-4 bg-black/20">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              How It Works
            </h2>
            <p className="text-xl text-white/70 max-w-3xl mx-auto">
              Simple, fast, and intelligent documentation generation in three steps
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: 'Submit Repository',
                description: 'Paste your GitHub repository URL and let our AI analyze your codebase structure, dependencies, and patterns.'
              },
              {
                step: '02',
                title: 'AI Processing',
                description: 'Advanced AI models with RAG pipeline analyze your code, extract insights, and understand your project architecture.'
              },
              {
                step: '03',
                title: 'Get Documentation',
                description: 'Receive comprehensive documentation including README, API docs, setup guides, and architectural insights.'
              }
            ].map((item, index) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-2xl font-bold text-white">
                  {item.step}
                </div>
                
                <h3 className="text-2xl font-semibold text-white mb-4">
                  {item.title}
                </h3>
                
                <p className="text-white/70 leading-relaxed">
                  {item.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="glass p-12 rounded-3xl"
          >
            <h2 className="text-4xl font-bold text-white mb-6">
              Ready to Transform Your Documentation?
            </h2>
            
            <p className="text-xl text-white/70 mb-8">
              Join thousands of developers who have improved their project documentation with AI
            </p>

            <motion.button
              onClick={() => navigate('/analyze')}
              className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold py-4 px-10 rounded-xl transition-all duration-300 text-lg shadow-2xl"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Get Started Free
            </motion.button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
