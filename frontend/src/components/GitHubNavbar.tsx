import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Search, 
  Menu, 
  X, 
  Github, 
  Book, 
  History, 
  Home, 
  Moon, 
  Sun,
  Settings,
  User,
  Bell,
  Plus,
  GitBranch
} from 'lucide-react';
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from '@clerk/clerk-react';

interface GitHubNavbarProps {
  darkMode: boolean;
  toggleDarkMode: () => void;
}

const GitHubNavbar: React.FC<GitHubNavbarProps> = ({ darkMode, toggleDarkMode }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/analyze', label: 'Analyze', icon: GitBranch },
    { path: '/history', label: 'History', icon: History },
  ];

  return (
    <nav className={`sticky top-0 z-50 border-b transition-colors duration-300 ${
      darkMode 
        ? 'bg-gray-900 border-gray-700' 
        : 'bg-white border-gray-200'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className={`p-2 rounded-lg ${
                darkMode ? 'bg-blue-600' : 'bg-blue-500'
              }`}>
                <Book className="h-6 w-6 text-white" />
              </div>
              <span className={`text-xl font-bold ${
                darkMode ? 'text-gray-100' : 'text-gray-900'
              }`}>
                Documentation.AI
              </span>
            </Link>
          </div>

          {/* Search Bar */}
          <div className="hidden md:flex flex-1 max-w-lg mx-8">
            <div className="relative w-full">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className={`h-4 w-4 ${
                  darkMode ? 'text-gray-400' : 'text-gray-500'
                }`} />
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search repositories..."
                className={`block w-full pl-10 pr-3 py-2 border rounded-lg text-sm transition-colors duration-300 ${
                  darkMode 
                    ? 'bg-gray-800 border-gray-600 text-gray-100 placeholder-gray-400 focus:border-blue-500' 
                    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500'
                } focus:outline-none focus:ring-1 focus:ring-blue-500`}
              />
            </div>
          </div>

          {/* Navigation Items */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                    isActive(item.path)
                      ? darkMode
                        ? 'bg-gray-800 text-blue-400'
                        : 'bg-gray-100 text-blue-600'
                      : darkMode
                        ? 'text-gray-300 hover:bg-gray-800 hover:text-gray-100'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>

          {/* Right side actions */}
          <div className="flex items-center space-x-2">
            {/* Notifications */}
            <button 
              title="Notifications"
              className={`p-2 rounded-lg transition-colors duration-200 ${
                darkMode 
                  ? 'text-gray-400 hover:bg-gray-800 hover:text-gray-100' 
                  : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900'
              }`}>
              <Bell className="h-5 w-5" />
            </button>

            {/* Add new */}
            <button 
              title="Add new"
              className={`p-2 rounded-lg transition-colors duration-200 ${
                darkMode 
                  ? 'text-gray-400 hover:bg-gray-800 hover:text-gray-100' 
                  : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900'
              }`}>
              <Plus className="h-5 w-5" />
            </button>

            {/* Dark mode toggle */}
            <button
              title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
              onClick={toggleDarkMode}
              className={`p-2 rounded-lg transition-colors duration-200 ${
                darkMode 
                  ? 'text-gray-400 hover:bg-gray-800 hover:text-gray-100' 
                  : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900'
              }`}
            >
              {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>

            {/* Authentication */}
            <div className="flex items-center space-x-2">
              <SignedOut>
                <SignInButton>
                  <button className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                    darkMode 
                      ? 'text-gray-300 hover:bg-gray-800 hover:text-gray-100 border border-gray-600' 
                      : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900 border border-gray-300'
                  }`}>
                    Sign In
                  </button>
                </SignInButton>
                <SignUpButton>
                  <button className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                    darkMode 
                      ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                      : 'bg-blue-600 hover:bg-blue-700 text-white'
                  }`}>
                    Sign Up
                  </button>
                </SignUpButton>
              </SignedOut>
              <SignedIn>
                <UserButton 
                  appearance={{
                    elements: {
                      avatarBox: "h-8 w-8"
                    }
                  }}
                />
              </SignedIn>
            </div>

            {/* Mobile menu toggle */}
            <div className="md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className={`p-2 rounded-lg transition-colors duration-200 ${
                  darkMode 
                    ? 'text-gray-400 hover:bg-gray-800 hover:text-gray-100' 
                    : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Search */}
        <div className="md:hidden pb-3">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className={`h-4 w-4 ${
                darkMode ? 'text-gray-400' : 'text-gray-500'
              }`} />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search repositories..."
              className={`block w-full pl-10 pr-3 py-2 border rounded-lg text-sm transition-colors duration-300 ${
                darkMode 
                  ? 'bg-gray-800 border-gray-600 text-gray-100 placeholder-gray-400 focus:border-blue-500' 
                  : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500'
              } focus:outline-none focus:ring-1 focus:ring-blue-500`}
            />
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      {isMenuOpen && (
        <div className={`md:hidden border-t transition-colors duration-300 ${
          darkMode ? 'border-gray-700 bg-gray-900' : 'border-gray-200 bg-white'
        }`}>
          <div className="px-4 pt-2 pb-3 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsMenuOpen(false)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-base font-medium transition-colors duration-200 ${
                    isActive(item.path)
                      ? darkMode
                        ? 'bg-gray-800 text-blue-400'
                        : 'bg-gray-100 text-blue-600'
                      : darkMode
                        ? 'text-gray-300 hover:bg-gray-800 hover:text-gray-100'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
            
            {/* Mobile Authentication */}
            <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
              <SignedOut>
                <div className="space-y-2">
                  <SignInButton>
                    <button 
                      onClick={() => setIsMenuOpen(false)}
                      className={`w-full flex items-center justify-center px-3 py-2 rounded-lg text-base font-medium transition-colors duration-200 ${
                        darkMode 
                          ? 'text-gray-300 hover:bg-gray-800 hover:text-gray-100 border border-gray-600' 
                          : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900 border border-gray-300'
                      }`}
                    >
                      Sign In
                    </button>
                  </SignInButton>
                  <SignUpButton>
                    <button 
                      onClick={() => setIsMenuOpen(false)}
                      className={`w-full flex items-center justify-center px-3 py-2 rounded-lg text-base font-medium transition-colors duration-200 ${
                        darkMode 
                          ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                          : 'bg-blue-600 hover:bg-blue-700 text-white'
                      }`}
                    >
                      Sign Up
                    </button>
                  </SignUpButton>
                </div>
              </SignedOut>
              <SignedIn>
                <div className="flex items-center justify-center">
                  <UserButton 
                    appearance={{
                      elements: {
                        avatarBox: "h-10 w-10"
                      }
                    }}
                  />
                </div>
              </SignedIn>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default GitHubNavbar;
