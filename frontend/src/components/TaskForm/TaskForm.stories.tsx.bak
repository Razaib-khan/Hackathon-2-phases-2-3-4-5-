import type { Meta, StoryObj } from '@storybook/react';
import TaskForm, { TaskFormData } from './TaskForm';

const meta = {
  title: 'Components/TaskForm',
  component: TaskForm,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    submitButtonText: { control: 'text' },
  },
} satisfies Meta<typeof TaskForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    onSubmit: (data: TaskFormData) => alert(`Submitted: ${JSON.stringify(data)}`),
    submitButtonText: 'Submit Task',
  },
};

export const WithInitialData: Story = {
  args: {
    initialData: {
      title: 'Sample Task',
      description: 'This is a sample task description',
      priority: 'critical',
      timestamp: new Date().toISOString().slice(0, 16),
    },
    onSubmit: (data: TaskFormData) => console.log('Updated:', data),
    onCancel: () => console.log('Cancelled'),
    submitButtonText: 'Update Task',
  },
};

export const EmptyForm: Story = {
  args: {
    onSubmit: (data: TaskFormData) => console.log('Submitted:', data),
    onCancel: () => console.log('Cancelled'),
    submitButtonText: 'Create Task',
  },
};