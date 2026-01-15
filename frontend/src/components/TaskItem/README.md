# TaskItem Component

The `TaskItem` component displays individual task details with proper TypeScript typing. It accepts a single task object and callbacks for updating and deleting the task.

## Features

- Displays task title, description, priority, and status
- Visual indicators for priority levels (high, medium, low) using Tailwind CSS
- Visual indicators for status (todo, in-progress, done) using Tailwind CSS
- Expandable/collapsible details section
- Edit and delete functionality
- Responsive design with Tailwind CSS

## Props

- `task`: An object containing task details (id, title, description, priority, status, timestamp)
- `onUpdateTask`: Callback function to handle task updates
- `onDeleteTask`: Callback function to handle task deletion

## Usage

```tsx
import TaskItem from './components/TaskItem';

<TaskItem
  task={task}
  onUpdateTask={handleUpdateTask}
  onDeleteTask={handleDeleteTask}
/>
```

## Styling

The component uses Tailwind CSS for styling with:
- Priority-based color coding (red for high, yellow for medium, green for low)
- Status-based color coding (gray for todo, blue for in-progress, green for done)
- Responsive layout that adapts to different screen sizes
- Hover effects for interactive elements