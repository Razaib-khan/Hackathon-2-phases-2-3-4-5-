import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskList, { Task } from './TaskList';

// Mock task data
const mockTasks: Task[] = [
  {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    priority: 'high',
    status: 'todo',
    timestamp: new Date(),
  },
];

describe('TaskList', () => {
  const mockOnUpdateTask = jest.fn();
  const mockOnDeleteTask = jest.fn();

  beforeEach(() => {
    mockOnUpdateTask.mockClear();
    mockOnDeleteTask.mockClear();
  });

  it('renders without crashing', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('displays task information correctly', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('high')).toBeInTheDocument();
    expect(screen.getByText('todo')).toBeInTheDocument();
  });

  it('calls onDeleteTask when delete button is clicked', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);

    expect(mockOnDeleteTask).toHaveBeenCalledWith('1');
  });

  it('calls onUpdateTask when edit button is clicked', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );

    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    expect(mockOnUpdateTask).toHaveBeenCalledWith(mockTasks[0]);
  });

  it('expands and collapses task details', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );

    const detailsButton = screen.getByText('Details');
    fireEvent.click(detailsButton);

    expect(screen.getByText('Test Description')).toBeInTheDocument();

    fireEvent.click(detailsButton);
    // The description should be hidden after collapsing
    expect(screen.queryByText('Test Description')).not.toBeInTheDocument();
  });
});