import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskList from './TaskList';
import { Task } from '../../types/task';

// Mock TaskItem to isolate TaskList testing
jest.mock('../TaskItem/TaskItem', () => {
  return {
    __esModule: true,
    default: ({ task }: { task: Task }) => (
      <div data-testid="mock-task-item">{task.title}</div>
    ),
  };
});

describe('TaskList', () => {
  const mockTasks: Task[] = [
    {
      id: '1',
      title: 'Test Task 1',
      description: 'Test Description 1',
      completed: false,
      createdAt: new Date('2023-01-01'),
    },
    {
      id: '2',
      title: 'Test Task 2',
      completed: true,
      createdAt: new Date('2023-01-02'),
    },
  ];

  const mockOnUpdateTask = jest.fn();
  const mockOnDeleteTask = jest.fn();

  it('renders without crashing', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );
    expect(screen.getByTestId('mock-task-item')).toBeInTheDocument();
  });

  it('displays the correct number of tasks', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );

    const taskItems = screen.getAllByTestId('mock-task-item');
    expect(taskItems).toHaveLength(2);
  });

  it('shows empty state when no tasks are provided', () => {
    render(
      <TaskList
        tasks={[]}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );

    expect(screen.getByText(/No tasks found/i)).toBeInTheDocument();
  });

  it('passes correct props to TaskItem', () => {
    render(
      <TaskList
        tasks={mockTasks.slice(0, 1)} // Just one task
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
      />
    );

    expect(screen.getByText('Test Task 1')).toBeInTheDocument();
  });
});