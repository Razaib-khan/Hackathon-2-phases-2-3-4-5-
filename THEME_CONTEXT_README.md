# Theme Context

The theme context provides a way to manage the application's theme state (light/dark mode) across the entire application.

## Features

- Toggle between light and dark themes
- Persist user's theme preference in localStorage
- Apply appropriate CSS classes to the application
- Custom hook for easy access to theme state

## Files

- `frontend/src/utils/theme.ts` - Contains the ThemeContext implementation
- `frontend/src/components/ThemeToggle.tsx` - A reusable component to toggle themes
- `frontend/app/globals.css` - CSS variables for theme colors
- `frontend/app/layout.tsx` - Wraps the application with ThemeProvider

## Usage

### In any component:

```tsx
'use client';

import { useTheme } from '@/src/utils/theme';

const MyComponent = () => {
  const { theme, toggleTheme, setTheme } = useTheme();

  return (
    <div>
      <p>Current theme: {theme}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
      <button onClick={() => setTheme('light')}>Light Mode</button>
      <button onClick={() => setTheme('dark')}>Dark Mode</button>
    </div>
  );
};
```

### To use the ThemeToggle component:

```tsx
import ThemeToggle from '@/src/components/ThemeToggle';

const Header = () => {
  return (
    <header>
      <h1>My App</h1>
      <ThemeToggle />
    </header>
  );
};
```

## How it works

1. The ThemeProvider wraps the entire application in `app/layout.tsx`
2. Theme preference is stored in localStorage and retrieved on initial load
3. CSS classes ('light' or 'dark') are applied to the html element
4. CSS variables are used to define different color schemes for each theme
5. The useTheme hook provides access to the current theme and functions to change it