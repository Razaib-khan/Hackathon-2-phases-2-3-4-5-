import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskForm from './TaskForm';
import { TaskFormData } from './types';

describe('TaskForm', () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  const defaultProps = {
    onSubmit: mockOnSubmit,
    onCancel: mockOnCancel,
    submitButtonText: 'Save Task',
    userId: 'test-user-id',
  };

  beforeEach(() => {
    mockOnSubmit.mockClear();
    mockOnCancel.mockClear();
  });

  test('renders all form fields correctly', () => {
    render(<TaskForm {...defaultProps} />);

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/priority/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/due date & time/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /save task/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
  });

  test('allows user to input task data', () => {
    render(<TaskForm {...defaultProps} />);

    const titleInput = screen.getByLabelText(/title/i);
    const descriptionTextarea = screen.getByLabelText(/description/i);
    const prioritySelect = screen.getByLabelText(/priority/i);

    fireEvent.change(titleInput, { target: { value: 'Test Task' } });
    fireEvent.change(descriptionTextarea, { target: { value: 'Test Description' } });
    fireEvent.change(prioritySelect, { target: { value: 'critical' } });

    expect(titleInput).toHaveValue('Test Task');
    expect(descriptionTextarea).toHaveValue('Test Description');
    expect(prioritySelect).toHaveValue('critical');
  });

  test('validates required fields', () => {
    render(<TaskForm {...defaultProps} />);

    fireEvent.click(screen.getByRole('button', { name: /save task/i }));

    expect(screen.getByText(/title is required/i)).toBeInTheDocument();
  });

  test('calls onSubmit with form data when submitted', () => {
    render(<TaskForm {...defaultProps} />);

    const titleInput = screen.getByLabelText(/title/i);
    fireEvent.change(titleInput, { target: { value: 'New Task' } });

    fireEvent.click(screen.getByRole('button', { name: /save task/i }));

    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
    const submittedData = mockOnSubmit.mock.calls[0][0];
    expect(submittedData.title).toBe('New Task');
  });

  test('calls onCancel when cancel button is clicked', () => {
    render(<TaskForm {...defaultProps} />);

    fireEvent.click(screen.getByRole('button', { name: /cancel/i }));

    expect(mockOnCancel).toHaveBeenCalledTimes(1);
  });

  test('populates form with initial data when provided', () => {
    const initialData: Partial<TaskFormData> = {
      title: 'Initial Task',
      description: 'Initial Description',
      priority: 'critical',
      status: 'todo',
      timestamp: new Date().toISOString().slice(0, 16),
    };

    render(<TaskForm {...defaultProps} userId="test-user-id" initialData={initialData} />);

    expect(screen.getByDisplayValue('Initial Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Initial Description')).toBeInTheDocument();
    expect(screen.getByRole('option', { selected: true }).textContent).toBe('Critical');
  });
});