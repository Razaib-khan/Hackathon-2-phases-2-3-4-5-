# TaskForm Component

The TaskForm component provides a user interface for creating and updating tasks with validation and proper TypeScript typing.

## Features

- Form fields for task title, description, priority, and due date/time
- Client-side validation for required fields
- Support for both creating new tasks and editing existing ones
- Proper TypeScript typing with exported interfaces
- Responsive design with Tailwind CSS
- Cancel functionality
- Character limits for descriptions

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `initialData` | `Partial<TaskFormData>` | No | Pre-populate the form with existing task data |
| `onSubmit` | `(data: TaskFormData) => void` | Yes | Callback fired when the form is submitted with valid data |
| `onCancel` | `() => void` | No | Callback fired when the cancel button is clicked |
| `submitButtonText` | `string` | No | Custom text for the submit button (defaults to "Submit") |

## Interfaces

### TaskFormData
```typescript
interface TaskFormData {
  id?: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  timestamp: string; // ISO string format
  status?: 'todo' | 'in-progress' | 'done';
  completed?: boolean;
  createdAt?: string;
  updatedAt?: string;
}
```

## Usage

```jsx
import TaskForm from './components/TaskForm';

const MyComponent = () => {
  const handleTaskSubmit = (taskData) => {
    console.log('Task submitted:', taskData);
    // Process the task data (save to API, update state, etc.)
  };

  const handleCancel = () => {
    console.log('Form cancelled');
    // Handle cancellation (e.g., close modal, navigate away)
  };

  return (
    <TaskForm
      onSubmit={handleTaskSubmit}
      onCancel={handleCancel}
      submitButtonText="Save Task"
    />
  );
};
```

## Validation

The form includes client-side validation for:
- Title is required and must be 100 characters or less
- Description must be 500 characters or less
- Timestamp is required

## Styling

The component uses Tailwind CSS utility classes for responsive design and consistent styling with the rest of the application.