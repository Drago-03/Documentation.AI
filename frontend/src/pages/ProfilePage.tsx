import React from 'react';
import { useUser, SignedIn, SignedOut } from '@clerk/clerk-react';
import { User, Mail, Calendar, Shield } from 'lucide-react';

const ProfilePage: React.FC = () => {
  const { user } = useUser();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <SignedIn>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
            {/* Header */}
            <div className="px-6 py-8 bg-gradient-to-r from-blue-500 to-purple-600">
              <div className="flex items-center space-x-4">
                <div className="w-20 h-20 rounded-full overflow-hidden bg-white/20 flex items-center justify-center">
                  {user?.imageUrl ? (
                    <img 
                      src={user.imageUrl} 
                      alt={user.fullName || 'User'} 
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <User className="h-10 w-10 text-white" />
                  )}
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-white">
                    {user?.fullName || 'User Profile'}
                  </h1>
                  <p className="text-blue-100">
                    {user?.primaryEmailAddress?.emailAddress}
                  </p>
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="px-6 py-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* User Information */}
                <div className="space-y-4">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                    <User className="h-5 w-5 mr-2 text-blue-500" />
                    User Information
                  </h2>
                  
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3">
                      <Mail className="h-4 w-4 text-gray-500" />
                      <span className="text-gray-700 dark:text-gray-300">
                        {user?.primaryEmailAddress?.emailAddress || 'No email'}
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <Calendar className="h-4 w-4 text-gray-500" />
                      <span className="text-gray-700 dark:text-gray-300">
                        Joined {user?.createdAt ? new Date(user.createdAt).toLocaleDateString() : 'Unknown'}
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <Shield className="h-4 w-4 text-gray-500" />
                      <span className="text-gray-700 dark:text-gray-300">
                        {user?.primaryEmailAddress?.verification?.status === 'verified' ? 'Verified' : 'Unverified'} Email
                      </span>
                    </div>
                  </div>
                </div>

                {/* Recent Activity */}
                <div className="space-y-4">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    Recent Activity
                  </h2>
                  <div className="text-gray-500 dark:text-gray-400">
                    <p>No recent activity to display.</p>
                    <p className="text-sm mt-2">
                      Your repository analysis history will appear here.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </SignedIn>

        <SignedOut>
          <div className="text-center py-20">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-12 max-w-md mx-auto">
              <User className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
                Sign In Required
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Please sign in to view your profile and access your documentation history.
              </p>
            </div>
          </div>
        </SignedOut>
      </div>
    </div>
  );
};

export default ProfilePage;
