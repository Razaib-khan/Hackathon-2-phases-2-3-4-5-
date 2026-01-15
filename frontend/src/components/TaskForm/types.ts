// Define TypeScript interfaces for task-related data

export interface TaskFormData {
  id?: string;
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  timestamp: string; // ISO string format
  status?: 'todo' | 'in-progress' | 'done';
  completed?: boolean;
  createdAt?: string;
  updatedAt?: string;
}

export interface TaskFormProps {
  initialData?: Partial<TaskFormData>;
  onSubmit: (data: TaskFormData) => void;
  onCancel?: () => void;
  submitButtonText?: string;
  userId: string;
}

export type PriorityLevel = 'critical' | 'high' | 'medium' | 'low';