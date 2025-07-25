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
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    // Apply dark mode class to body
    if (darkMode) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
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
      <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'} transition-colors duration-300`}>
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
