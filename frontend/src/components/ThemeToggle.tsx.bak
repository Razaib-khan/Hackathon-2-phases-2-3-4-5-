'use client';

import { useTheme } from '@/utils/theme';
import { SunIcon, MoonIcon } from 'lucide-react';

export const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
    >
      {theme === 'light' ? (
        <MoonIcon className="w-5 h-5 text-gray-800 dark:text-gray-200" />
      ) : (
        <SunIcon className="w-5 h-5 text-gray-800 dark:text-gray-200" />
      )}
    </button>
  );
};