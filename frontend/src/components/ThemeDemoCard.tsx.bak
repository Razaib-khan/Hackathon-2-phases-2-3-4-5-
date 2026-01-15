import { useTheme } from '@/utils/theme';

export const ThemeDemoCard = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="card max-w-md mx-auto p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Theme Demo</h2>
      <p className="mb-4">
        Current theme: <span className="font-semibold">{theme}</span>
      </p>
      <p className="text-sm text-muted-foreground mb-4">
        The background and text colors change based on the selected theme.
      </p>
      <button
        onClick={toggleTheme}
        className="btn-primary px-4 py-2 rounded-md"
      >
        Toggle to {theme === 'light' ? 'Dark' : 'Light'} Mode
      </button>
    </div>
  );
};