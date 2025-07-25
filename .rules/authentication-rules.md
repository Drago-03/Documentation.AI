# Authentication Rules & Clerk Integration

## Clerk Authentication Setup

### Installation & Configuration

#### 1. Install Clerk Dependencies
```bash
# For React/Next.js frontend
npm install @clerk/nextjs
# OR for standalone React
npm install @clerk/clerk-react

# Additional dependencies
npm install @clerk/themes
```

#### 2. Environment Variables
```bash
# Frontend (.env.local)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Optional: Custom domain
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

#### 3. Clerk Provider Setup
```tsx
// app/layout.tsx (Next.js 13+)
import { ClerkProvider } from '@clerk/nextjs';
import { dark } from '@clerk/themes';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: dark, // Matches our GitHub dark theme
        variables: {
          colorPrimary: '#2f81f7', // GitHub blue
          colorTextOnPrimaryBackground: '#ffffff',
          colorBackground: '#0d1117', // GitHub dark background
          colorInputBackground: '#21262d',
          colorInputText: '#e6edf3',
        },
        elements: {
          formButtonPrimary: 
            'bg-green-600 hover:bg-green-700 text-sm normal-case',
          card: 'bg-gray-800 border border-gray-700',
          headerTitle: 'text-gray-100',
          headerSubtitle: 'text-gray-400',
        }
      }}
    >
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

### Authentication Components

#### Sign In Component
```tsx
// components/auth/SignInForm.tsx
import { SignIn } from '@clerk/nextjs';

export default function SignInForm() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-gray-100">
            Sign in to Documentation.AI
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
            Continue with your GitHub account
          </p>
        </div>
        <SignIn 
          routing="path" 
          path="/sign-in"
          redirectUrl="/dashboard"
          appearance={{
            elements: {
              rootBox: "mx-auto",
              card: "shadow-none border-0",
            }
          }}
        />
      </div>
    </div>
  );
}
```

#### User Profile Button
```tsx
// components/auth/UserButton.tsx
import { UserButton, useUser } from '@clerk/nextjs';
import { User, Settings, LogOut } from 'lucide-react';

export default function UserProfileButton() {
  const { isSignedIn, user } = useUser();

  if (!isSignedIn) return null;

  return (
    <div className="flex items-center space-x-3">
      <span className="text-sm text-gray-700 dark:text-gray-300">
        {user.firstName || user.username}
      </span>
      <UserButton 
        appearance={{
          elements: {
            avatarBox: "w-8 h-8",
            userButtonPopoverCard: "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700",
            userButtonPopoverActionButton: "hover:bg-gray-50 dark:hover:bg-gray-700",
          }
        }}
        afterSignOutUrl="/"
      />
    </div>
  );
}
```

#### Protected Route Wrapper
```tsx
// components/auth/ProtectedRoute.tsx
import { useAuth } from '@clerk/nextjs';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export default function ProtectedRoute({ 
  children, 
  fallback 
}: ProtectedRouteProps) {
  const { isSignedIn, isLoaded } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.push('/sign-in');
    }
  }, [isLoaded, isSignedIn, router]);

  if (!isLoaded) {
    return <LoadingSpinner />;
  }

  if (!isSignedIn) {
    return fallback || null;
  }

  return <>{children}</>;
}
```

### GitHub Integration (OAuth)

#### GitHub OAuth Configuration
```javascript
// Clerk Dashboard Settings
{
  "oauth_providers": {
    "github": {
      "enabled": true,
      "client_id": "your_github_oauth_app_id",
      "client_secret": "your_github_oauth_app_secret",
      "scopes": ["user:email", "public_repo", "read:org"]
    }
  }
}
```

#### GitHub Data Access
```tsx
// hooks/useGitHubData.ts
import { useUser } from '@clerk/nextjs';

export function useGitHubData() {
  const { user } = useUser();
  
  const getGitHubToken = () => {
    const githubAccount = user?.externalAccounts.find(
      account => account.provider === 'github'
    );
    return githubAccount?.approvedScopes.includes('public_repo') 
      ? githubAccount.accessToken 
      : null;
  };

  const getUserRepos = async () => {
    const token = getGitHubToken();
    if (!token) return [];

    const response = await fetch('https://api.github.com/user/repos', {
      headers: {
        'Authorization': `token ${token}`,
        'Accept': 'application/vnd.github.v3+json',
      },
    });

    return response.json();
  };

  return {
    getGitHubToken,
    getUserRepos,
    hasGitHubAccess: !!getGitHubToken(),
  };
}
```

### Navigation Integration

#### Navbar with Authentication
```tsx
// components/Navbar.tsx
import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs';
import { Github, BookOpen } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <BookOpen className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900 dark:text-gray-100">
                Documentation.AI
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <SignedOut>
              <SignInButton mode="modal">
                <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                  <Github className="h-4 w-4 mr-2" />
                  Sign in with GitHub
                </button>
              </SignInButton>
            </SignedOut>
            
            <SignedIn>
              <UserButton 
                appearance={{
                  elements: {
                    avatarBox: "w-8 h-8"
                  }
                }}
                afterSignOutUrl="/"
              />
            </SignedIn>
          </div>
        </div>
      </div>
    </nav>
  );
}
```

### Backend Integration

#### Flask JWT Verification
```python
# backend/auth.py
import jwt
from functools import wraps
from flask import request, jsonify, current_app
import requests

def verify_clerk_token(token):
    """Verify Clerk JWT token."""
    try:
        # Get Clerk's public key
        jwks_url = f"https://api.clerk.dev/v1/jwks"
        response = requests.get(jwks_url)
        jwks = response.json()
        
        # Verify and decode token
        decoded_token = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=current_app.config['CLERK_PUBLISHABLE_KEY']
        )
        
        return decoded_token
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization required'}), 401
        
        token = auth_header.split(' ')[1]
        user_data = verify_clerk_token(token)
        
        if not user_data:
            return jsonify({'error': 'Invalid token'}), 401
        
        request.user = user_data
        return f(*args, **kwargs)
    
    return decorated_function

# Usage in routes
@app.route('/api/user/repositories', methods=['GET'])
@require_auth
def get_user_repositories():
    user_id = request.user['sub']
    # Fetch user's repositories
    return jsonify({'repositories': []})
```

#### API Client with Authentication
```tsx
// utils/apiClient.ts
import { auth } from '@clerk/nextjs';

class APIClient {
  private baseURL: string;

  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5002';
  }

  private async getAuthToken(): Promise<string | null> {
    try {
      const { getToken } = auth();
      return await getToken();
    } catch (error) {
      console.error('Failed to get auth token:', error);
      return null;
    }
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getAuthToken();
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  // API methods
  async analyzeRepository(repoUrl: string) {
    return this.request('/api/analyze', {
      method: 'POST',
      body: JSON.stringify({ repo_url: repoUrl }),
    });
  }

  async getUserRepositories() {
    return this.request('/api/user/repositories');
  }
}

export const apiClient = new APIClient();
```

### Security Best Practices

#### Token Management
- Store tokens securely (httpOnly cookies when possible)
- Implement token refresh logic
- Use short-lived access tokens
- Validate tokens on every API request

#### Rate Limiting
```python
# backend/rate_limiting.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=lambda: request.user.get('sub') if hasattr(request, 'user') else get_remote_address(),
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/analyze')
@limiter.limit("10 per minute")
@require_auth
def analyze_repository():
    # Implementation
    pass
```

#### CORS Configuration
```python
# backend/app.py
from flask_cors import CORS

CORS(app, origins=[
    "http://localhost:3000",  # Development
    "https://yourdomain.com"  # Production
])
```

### Testing Authentication

#### Test Utilities
```tsx
// __tests__/auth-utils.tsx
import { render } from '@testing-library/react';
import { ClerkProvider } from '@clerk/nextjs';

export function renderWithAuth(component: React.ReactElement) {
  return render(
    <ClerkProvider publishableKey="pk_test_mock">
      {component}
    </ClerkProvider>
  );
}

// Mock authenticated user
export const mockUser = {
  id: 'user_test123',
  firstName: 'Test',
  lastName: 'User',
  emailAddresses: [{ emailAddress: 'test@example.com' }],
};
```

### Deployment Considerations

#### Environment Configuration
```bash
# Production environment variables
CLERK_SECRET_KEY=sk_live_...
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
CLERK_WEBHOOK_SECRET=whsec_...

# Webhook endpoints for user events
CLERK_WEBHOOK_URL=https://yourdomain.com/api/webhooks/clerk
```

#### Monitoring & Analytics
- Track sign-up conversion rates
- Monitor authentication errors
- Set up alerts for failed logins
- Implement user activity logging
