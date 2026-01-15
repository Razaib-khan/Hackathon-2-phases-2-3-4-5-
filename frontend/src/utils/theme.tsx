'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define the theme types
export type Theme = 'light' | 'dark';

// Define the context type
interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

// Create the context with default values
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Provider component props
interface ThemeProviderProps {
  children: ReactNode;
}

// Custom hook to use the theme context
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// Provider component
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  // Initialize theme from localStorage or default to 'light'
  const [theme, setThemeState] = useState<Theme>(() => {
    if (typeof window !== 'undefined') {
      const savedTheme = localStorage.getItem('theme') as Theme | null;
      if (savedTheme) {
        return savedTheme;
      }
      // Fallback to system preference if no saved theme
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'light';
  });

  // Apply theme to the document element
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const root = window.document.documentElement;

      // Remove existing theme classes
      root.classList.remove('light-theme', 'dark-theme');

      // Add the current theme class
      root.classList.add(`${theme}-theme`);

      // Toggle the 'dark' class for Tailwind CSS
      root.classList.toggle('dark', theme === 'dark');

      // Set the data-theme attribute for CSS selectors
      root.setAttribute('data-theme', theme);

      // Store the theme in localStorage
      localStorage.setItem('theme', theme);
    }
  }, [theme]);

  // Toggle between light and dark themes
  const toggleTheme = () => {
    setThemeState(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  // Set theme explicitly
  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
  };

  // Provide the context value
  const value = {
    theme,
    toggleTheme,
    setTheme
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

// Export the context as well to allow direct context usage if needed
export { ThemeContext };