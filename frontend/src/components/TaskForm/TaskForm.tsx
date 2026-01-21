import React, { useState } from 'react';
import { TaskFormData, TaskFormProps } from './types';
import { createTask, updateTask, Task as ApiTask } from '@/services/api';

// Helper function to convert Date to datetime-local format (YYYY-MM-DDTHH:mm)
const formatDateForInput = (dateString?: string): string => {
  if (!dateString) {
    return new Date().toISOString().slice(0, 16);
  }

  // If it's already in the right format, return as is
  if (dateString.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/)) {
    return dateString;
  }

  // Otherwise, try to parse it as a date
  try {
    return new Date(dateString).toISOString().slice(0, 16);
  } catch {
    return new Date().toISOString().slice(0, 16);
  }
};

const TaskForm: React.FC<TaskFormProps> = ({
  initialData = {},
  onSubmit,
  onCancel,
  submitButtonText = 'Submit',
  userId,
}) => {
  // Initialize form state with initial data or default values
  const [formData, setFormData] = useState<TaskFormData>({
    title: initialData.title || '',
    description: initialData.description || '',
    priority: (initialData.priority as 'critical' | 'high' | 'medium' | 'low') || 'medium',
    timestamp: formatDateForInput(initialData.timestamp),
    status: initialData.status || 'todo',
  });

  // Validation state
  const [errors, setErrors] = useState<Partial<TaskFormData>>({});
  const [isLoading, setIsLoading] = useState(false);

  // Handle input changes
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name as keyof TaskFormData]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: Partial<TaskFormData> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }

    if (formData.title.length > 100) {
      newErrors.title = 'Title must be 100 characters or less';
    }

    if (formData.description.length > 500) {
      newErrors.description = 'Description must be 500 characters or less';
    }

    if (!formData.timestamp) {
      newErrors.timestamp = 'Timestamp is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Helper function to map priority values to backend format
  const mapPriorityToBackend = (priority: string) => {
    switch(priority.toLowerCase()) {
      case 'critical': return 'Critical';
      case 'high': return 'High';
      case 'medium': return 'Medium';
      case 'low': return 'Low';
      default: return 'Medium';
    }
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Convert form data to API format with proper priority mapping
      const taskData = {
        title: formData.title,
        description: formData.description,
        priority: mapPriorityToBackend(formData.priority) as 'Critical' | 'High' | 'Medium' | 'Low',
        timestamp: new Date(formData.timestamp).toISOString(), // Convert to proper ISO format
      };

      let result: ApiTask;

      if (initialData.id) {
        // Update existing task
        result = await updateTask(userId, initialData.id, {
          title: taskData.title,
          description: taskData.description,
          priority: taskData.priority as 'Critical' | 'High' | 'Medium' | 'Low',
        });
      } else {
        // Create new task
        result = await createTask(userId, {
          title: taskData.title,
          description: taskData.description,
          priority: taskData.priority as 'Critical' | 'High' | 'Medium' | 'Low',
          timestamp: taskData.timestamp,
        });
      }

      // Convert ApiTask to TaskFormData for the callback
      const taskFormData: TaskFormData = {
        id: result.id,
        title: result.title,
        description: result.description || '',
        priority: result.priority.toLowerCase() as 'critical' | 'high' | 'medium' | 'low',
        timestamp: result.timestamp,
        status: result.status ? 'done' : 'todo', // Assuming status is boolean for completion
        completed: result.status,
        createdAt: result.created_at,
        updatedAt: result.updated_at
      };

      onSubmit(taskFormData);
    } catch (error: any) {
      console.error('Failed to save task:', error);
      let errorMessage = `Failed to ${initialData.id ? 'update' : 'create'} task.`;

      if (error.response?.data?.detail) {
        errorMessage += ` ${error.response.data.detail}`;
      } else if (error.message) {
        errorMessage += ` ${error.message}`;
      }

      alert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md w-full max-w-md mx-auto">
      <div className="mb-4">
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 ${
            errors.title ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-blue-200'
          } dark:bg-gray-800 dark:border-gray-600 dark:text-white dark:placeholder-gray-400`}
          placeholder="Enter task title"
          disabled={isLoading}
        />
        {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
      </div>

      <div className="mb-4">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-200 dark:bg-gray-800 dark:border-gray-600 dark:text-white dark:placeholder-gray-400"
          placeholder="Enter task description"
          disabled={isLoading}
        />
        {formData.description.length > 400 && (
          <p className="mt-1 text-sm text-gray-500">
            {500 - formData.description.length} characters remaining
          </p>
        )}
      </div>

      <div className="mb-4">
        <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
          Priority
        </label>
        <select
          id="priority"
          name="priority"
          value={formData.priority}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-200 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
          disabled={isLoading}
        >
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      <div className="mb-6">
        <label htmlFor="timestamp" className="block text-sm font-medium text-gray-700 mb-1">
          Due Date & Time *
        </label>
        <input
          type="datetime-local"
          id="timestamp"
          name="timestamp"
          value={formData.timestamp}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 ${
            errors.timestamp ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-blue-200'
          } dark:bg-gray-800 dark:border-gray-600 dark:text-white`}
          disabled={isLoading}
        />
        {errors.timestamp && <p className="mt-1 text-sm text-red-600">{errors.timestamp}</p>}
      </div>

      <div className="flex justify-end space-x-3">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-200"
            disabled={isLoading}
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          disabled={isLoading}
        >
          {isLoading ? 'Saving...' : submitButtonText}
        </button>
      </div>
    </form>
  );
};

export default TaskForm;