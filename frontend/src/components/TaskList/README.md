# TaskList Component

A responsive task list component that displays a list of tasks with proper TypeScript typing and Tailwind CSS styling.

## Features

- Responsive design that works on mobile, tablet, and desktop
- TypeScript typing for type safety
- Expandable/collapsible task details
- Priority and status indicators with color coding
- Edit and delete functionality
- Proper date formatting

## Props

```typescript
interface TaskListProps {
  tasks: Task[];
  onUpdateTask: (task: Task) => void;
  onDeleteTask: (id: string) => void;
}
```

### Task Type

```typescript
interface Task {
  id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  status: 'todo' | 'in-progress' | 'done';
  timestamp: Date;
}
```

## Usage

```tsx
import TaskList from '@/components/TaskList';

const MyComponent = () => {
  const tasks = [
    {
      id: '1',
      title: 'Example Task',
      description: 'Example description',
      priority: 'high',
      status: 'todo',
      timestamp: new Date()
    }
  ];

  const handleUpdateTask = (task: Task) => {
    // Handle task update
  };

  const handleDeleteTask = (id: string) => {
    // Handle task deletion
  };

  return (
    <TaskList
      tasks={tasks}
      onUpdateTask={handleUpdateTask}
      onDeleteTask={handleDeleteTask}
    />
  );
};
```