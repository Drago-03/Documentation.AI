# UI/UX Design Rules & Guidelines

## GitHub Design Language

### Core Design Principles

1. **GitHub Consistency** - All UI elements must match GitHub's design system
2. **Clean Minimalism** - Prioritize clarity and simplicity
3. **Dark Mode First** - Design for dark mode, ensure light mode compatibility
4. **Responsive Design** - Mobile-first approach with breakpoint consistency
5. **Accessibility** - WCAG 2.1 AA compliance mandatory

### Color Palette

#### GitHub Color System
```css
/* Light Mode */
--color-canvas-default: #ffffff;
--color-canvas-subtle: #f6f8fa;
--color-border-default: #d0d7de;
--color-fg-default: #24292f;
--color-fg-muted: #656d76;
--color-accent-emphasis: #0969da;
--color-danger-emphasis: #cf222e;
--color-success-emphasis: #1a7f37;

/* Dark Mode */
--color-canvas-default: #0d1117;
--color-canvas-subtle: #161b22;
--color-border-default: #30363d;
--color-fg-default: #e6edf3;
--color-fg-muted: #7d8590;
--color-accent-emphasis: #2f81f7;
--color-danger-emphasis: #f85149;
--color-success-emphasis: #3fb950;
```

#### Language Colors (GitHub Standard)
```css
.language-typescript { color: #3178c6; }
.language-javascript { color: #f1e05a; }
.language-python { color: #3572A5; }
.language-java { color: #b07219; }
.language-go { color: #00ADD8; }
.language-rust { color: #dea584; }
.language-react { color: #61DAFB; }
```

### Typography

#### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", 
             "Noto Sans", Helvetica, Arial, sans-serif;
```

#### Font Sizes (Tailwind Scale)
- `text-xs`: 12px - Tags, captions
- `text-sm`: 14px - Secondary text, buttons
- `text-base`: 16px - Body text, form inputs
- `text-lg`: 18px - Card titles
- `text-xl`: 20px - Section headers
- `text-2xl`: 24px - Page titles
- `text-3xl`: 30px - Hero headings

### Component Design Standards

#### Buttons
```tsx
// Primary Button (GitHub Green)
<button className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800">
  Primary Action
</button>

// Secondary Button
<button className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700">
  Secondary Action
</button>

// Danger Button
<button className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 border border-transparent rounded-md">
  Delete
</button>
```

#### Cards & Containers
```tsx
// Standard Card
<div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
  <div className="p-6">
    {/* Card content */}
  </div>
</div>

// Repository Card (GitHub Style)
<div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-gray-300 dark:hover:border-gray-600 transition-colors">
  {/* Repository preview */}
</div>
```

#### Navigation
```tsx
// GitHub-style tabs
<nav className="flex space-x-1 border-b border-gray-200 dark:border-gray-700">
  <button className="px-3 py-2 text-sm font-medium text-gray-900 dark:text-gray-100 border-b-2 border-orange-500">
    Active Tab
  </button>
  <button className="px-3 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100">
    Inactive Tab
  </button>
</nav>
```

#### Forms & Inputs
```tsx
// GitHub-style input
<input 
  type="text"
  className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
  placeholder="Enter repository URL..."
/>

// Select dropdown
<select className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
  <option>Choose option</option>
</select>
```

### Layout Guidelines

#### Responsive Breakpoints (Tailwind)
- `sm`: 640px+ (tablet)
- `md`: 768px+ (small laptop)
- `lg`: 1024px+ (desktop)
- `xl`: 1280px+ (large desktop)
- `2xl`: 1536px+ (extra large)

#### Grid System
```tsx
// Main layout (GitHub repository style)
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
    <div className="lg:col-span-3">
      {/* Main content */}
    </div>
    <div className="lg:col-span-1">
      {/* Sidebar */}
    </div>
  </div>
</div>
```

#### Spacing Scale
- `space-1`: 4px - Tight spacing
- `space-2`: 8px - Close elements
- `space-3`: 12px - Related elements
- `space-4`: 16px - Standard spacing
- `space-6`: 24px - Section spacing
- `space-8`: 32px - Large sections
- `space-12`: 48px - Major sections

### Icon Usage

#### Lucide React Icons (GitHub Style)
```tsx
import { 
  Star, GitFork, Eye, Download, Code, Book,
  Settings, Users, Activity, AlertCircle, Shield 
} from 'lucide-react';

// Icon sizing
<Star className="h-4 w-4" />  // Small icons (buttons, inline)
<Star className="h-5 w-5" />  // Medium icons (headings)
<Star className="h-6 w-6" />  // Large icons (features)
```

### Animation & Transitions

#### Standard Transitions
```css
/* Hover transitions */
.transition-colors { transition: color 150ms ease-in-out; }
.transition-opacity { transition: opacity 150ms ease-in-out; }
.transition-transform { transition: transform 150ms ease-in-out; }

/* Loading states */
.animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
.animate-spin { animation: spin 1s linear infinite; }
```

#### Hover Effects
```tsx
// Button hover
className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"

// Card hover
className="hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-md transition-all"

// Icon hover
className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
```

### Dark Mode Implementation

#### Tailwind Dark Mode Classes
```tsx
// Background colors
className="bg-white dark:bg-gray-800"
className="bg-gray-50 dark:bg-gray-900"

// Text colors
className="text-gray-900 dark:text-gray-100"
className="text-gray-600 dark:text-gray-400"

// Border colors
className="border-gray-200 dark:border-gray-700"
className="border-gray-300 dark:border-gray-600"
```

#### Theme Toggle Component
```tsx
const ThemeToggle = () => {
  const [darkMode, setDarkMode] = useState(false);
  
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <button
      onClick={() => setDarkMode(!darkMode)}
      className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
    >
      {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
    </button>
  );
};
```

### Accessibility Standards

#### ARIA Labels
```tsx
// Interactive elements
<button aria-label="Star repository">
  <Star className="h-4 w-4" />
</button>

// Form labels
<label htmlFor="repo-url" className="sr-only">Repository URL</label>
<input id="repo-url" type="text" />

// Skip navigation
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

#### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Proper tab order implementation
- Focus indicators visible and clear
- Escape key support for modals

#### Color Contrast
- Minimum 4.5:1 ratio for normal text
- Minimum 3:1 ratio for large text
- Test with tools like WebAIM Contrast Checker

### Performance Guidelines

#### Optimization Rules
- Use `next/image` for all images
- Implement lazy loading for heavy components
- Minimize CSS bundle size
- Use Tailwind's purge configuration
- Optimize font loading with `font-display: swap`

#### Code Splitting
```tsx
// Lazy load heavy components
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Use Suspense for loading states
<Suspense fallback={<LoadingSpinner />}>
  <HeavyComponent />
</Suspense>
```

### Testing UI Components

#### Visual Testing Checklist
- [ ] Component renders correctly in light mode
- [ ] Component renders correctly in dark mode
- [ ] Responsive design works across breakpoints
- [ ] Hover states function properly
- [ ] Focus states are visible
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility
- [ ] Color contrast meets standards

#### Storybook Integration
```tsx
// Component.stories.tsx
export default {
  title: 'Components/Button',
  component: Button,
  parameters: {
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#0d1117' }
      ]
    }
  }
};
```
