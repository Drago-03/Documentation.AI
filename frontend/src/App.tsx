import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Import pages
import HomePage from './pages/HomePage';
import AnalysisPage from './pages/AnalysisPage';
import RepositoryView from './pages/RepositoryView';
import HistoryPage from './pages/HistoryPage';

// Import components
import GitHubNavbar from './components/GitHubNavbar';
import Footer from './components/Footer';

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    // Check localStorage for saved theme, default to light mode
    const savedTheme = localStorage.getItem('theme');
    return savedTheme === 'dark';
  });

  useEffect(() => {
    // Apply dark mode class to html element for better Tailwind support
    const html = document.documentElement;
    if (darkMode) {
      html.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      html.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <Router future={{ 
      v7_startTransition: true,
      v7_relativeSplatPath: true 
    }}>
      <div className={`min-h-screen transition-colors duration-300 ${
        darkMode 
          ? 'dark bg-gray-900 text-white' 
          : 'bg-white text-gray-900'
      }`}>
        <GitHubNavbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
        
        <main className="min-h-screen">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analyze" element={<AnalysisPage />} />
            <Route path="/repository/:jobId" element={<RepositoryView />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
        
        <Footer />
        
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            className: darkMode ? 'dark-toast' : 'light-toast',
            style: {
              background: darkMode ? '#1f2937' : '#ffffff',
              color: darkMode ? '#f9fafb' : '#111827',
              border: `1px solid ${darkMode ? '#374151' : '#e5e7eb'}`,
              borderRadius: '8px',
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;
