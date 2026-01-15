'use client';

import React, { useState, useRef } from 'react';
import Link from 'next/link';
import TaskList, { TaskListHandle } from '@/src/components/TaskList/TaskList';
import TaskForm from '@/src/components/TaskForm/TaskForm';
import { Task, CreateTaskRequest } from '@/src/services/api';
import { useAuth } from '@/src/contexts/AuthContext';

const TasksPage = () => {
  const { user, logout, getUserFullName, loading } = useAuth();

  // Declare all hooks first, before any conditional returns
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const taskListRef = useRef<TaskListHandle>(null);

  // Don't proceed if user is not loaded yet or not authenticated
  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <p>Please sign in to access your tasks.</p>
          <Link href="/auth/signin" className="text-blue-600 hover:underline">
            Sign In
          </Link>
        </div>
      </div>
    );
  }

  const userId = user.id;

  const handleUpdateTask = (updatedTask: Task) => {
    // Refresh the task list or update optimistically
    console.log(`Task "${updatedTask.title}" updated`);
    // Refresh the task list to show the updated task
    if (taskListRef.current) {
      taskListRef.current.refreshTasks();
    }
  };

  const handleDeleteTask = (id: string) => {
    // Deletion is handled by the TaskItem component directly
    console.log(`Task with ID "${id}" deleted`);
    // Refresh the task list to reflect the deletion
    if (taskListRef.current) {
      taskListRef.current.refreshTasks();
    }
  };

  const handleCreateTask = (newTask: Task) => {
    console.log(`Task "${newTask.title}" created`);
    setShowForm(false);
    setEditingTask(null);
    // Refresh the task list to show the new task
    if (taskListRef.current) {
      taskListRef.current.refreshTasks();
    }
  };

  const handleFormSubmit = (task: Task) => {
    if (editingTask) {
      handleUpdateTask(task);
    } else {
      handleCreateTask(task);
    }
    setShowForm(false);
    setEditingTask(null);
  };

  // Handle task updates (including status changes) by refreshing the list
  const handleTaskUpdate = (updatedTask: Task) => {
    console.log(`Task "${updatedTask.title}" updated`);
    // Refresh the task list to show the updated task
    if (taskListRef.current) {
      taskListRef.current.refreshTasks();
    }
  };

  // Handle task updates (including status changes and edit requests) by refreshing the list
  const handleEditTask = (task: Task) => {
    console.log(`Task "${task.title}" updated`);
    // Refresh the task list to show the updated task
    if (taskListRef.current) {
      taskListRef.current.refreshTasks();
    }
    // Also set the task for editing if form is not already shown
    if (!showForm) {
      setEditingTask(task);
      setShowForm(true);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Task Management</h1>
        <div className="flex items-center space-x-4">
          {user && (
            <div className="relative">
              <button
                className="flex items-center space-x-1 text-gray-700 hover:text-gray-900"
                onClick={() => setShowDropdown(!showDropdown)}
              >
                <span>{getUserFullName() || user.email}</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>
              {showDropdown && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
                  <Link
                    href="/account"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    onClick={() => setShowDropdown(false)}
                  >
                    Account Settings
                  </Link>
                  <button
                    onClick={() => {
                      logout();
                      setShowDropdown(false);
                    }}
                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    Sign out
                  </button>
                </div>
              )}
              {/* Close dropdown when clicking outside */}
              {showDropdown && (
                <div
                  className="fixed inset-0 z-0"
                  onClick={() => setShowDropdown(false)}
                ></div>
              )}
            </div>
          )}
          <button
            onClick={() => {
              setEditingTask(null);
              setShowForm(true);
            }}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Add New Task
          </button>
        </div>
      </div>

      {showForm && (
        <div className="mb-8 flex justify-center items-center min-h-[50vh]">
          <TaskForm
            userId={userId}
            initialData={editingTask ? {
              id: editingTask.id,
              title: editingTask.title,
              description: editingTask.description || '',
              priority: editingTask.priority.toLowerCase() as 'critical' | 'high' | 'medium' | 'low',
              timestamp: editingTask.timestamp,
            } : {}}
            onSubmit={handleFormSubmit}
            onCancel={() => {
              setShowForm(false);
              setEditingTask(null);
            }}
            submitButtonText={editingTask ? 'Update Task' : 'Create Task'}
          />
        </div>
      )}

      <TaskList
        ref={taskListRef}
        userId={userId}
        onEditTask={handleEditTask} // Pass the edit handler to open form for editing
        onTaskUpdate={handleTaskUpdate} // Pass the update handler to refresh the list on status changes
        onDeleteTask={handleDeleteTask}
      />
    </div>
  );
};

export default TasksPage;