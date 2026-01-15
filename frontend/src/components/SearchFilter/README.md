# FilterControls Component

The FilterControls component provides a user interface for filtering tasks by priority, status, and timestamp ranges.

## Features

- Filter by priority (low, medium, high)
- Filter by status (to-do, in-progress, done)
- Filter by date range (start and end dates)
- Clear filters functionality
- Responsive layout using Tailwind CSS
- Fully typed with TypeScript

## Props

| Prop | Type | Description |
|------|------|-------------|
| `onFilterChange` | `(filters: FilterOptions) => void` | Callback function triggered when filter options change |

## Types

```typescript
interface FilterOptions {
  priority?: 'low' | 'medium' | 'high' | 'all';
  status?: 'todo' | 'in-progress' | 'done' | 'all';
  startDate?: string; // ISO date string (YYYY-MM-DD)
  endDate?: string;   // ISO date string (YYYY-MM-DD)
}
```

## Usage Example

```tsx
import FilterControls, { FilterOptions } from './components/SearchFilter';

const MyComponent = () => {
  const handleFilterChange = (filters: FilterOptions) => {
    // Apply filters to your data
    console.log('New filters:', filters);
  };

  return (
    <div>
      <FilterControls onFilterChange={handleFilterChange} />
      {/* Rest of your component */}
    </div>
  );
};
```

## Styling

The component uses Tailwind CSS for styling with responsive design. It includes:

- Responsive grid layout (1 column on mobile, 4 columns on medium screens and up)
- Color-coded active states for filter buttons
- Focus states for accessibility
- Clean, modern UI elements