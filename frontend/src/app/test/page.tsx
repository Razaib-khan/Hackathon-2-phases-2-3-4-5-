'use client';

import React, { useState, useEffect } from 'react';
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  toggleTaskCompletion,
  Task
} from '@/src/services/api';

const TestPage = () => {
  const [userId, setUserId] = useState('test-user-123');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newTask, setNewTask] = useState({
    title: 'Test Task',
    description: 'Test description',
    priority: 'Medium' as 'Critical' | 'High' | 'Medium' | 'Low',
  });
  const [taskId, setTaskId] = useState('');

  useEffect(() => {
    loadTasks();
  }, [userId]);

  const loadTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getTasks(userId);
      setTasks(response.tasks);
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks');
      console.error('Load tasks error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async () => {
    setLoading(true);
    setError(null);
    try {
      const createdTask = await createTask(userId, newTask);
      setTasks([...tasks, createdTask]);
      setNewTask({
        title: 'Test Task',
        description: 'Test description',
        priority: 'Medium',
      });
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      console.error('Create task error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTask = async () => {
    if (!taskId) {
      setError('Please enter a task ID to update');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const updatedTask = await updateTask(userId, taskId, {
        title: 'Updated Test Task',
        description: 'Updated description',
        priority: 'High',
      });

      setTasks(tasks.map(t => t.id === taskId ? updatedTask : t));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      console.error('Update task error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTask = async () => {
    if (!taskId) {
      setError('Please enter a task ID to delete');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await deleteTask(userId, taskId);
      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
      console.error('Delete task error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleCompletion = async () => {
    if (!taskId) {
      setError('Please enter a task ID to toggle');
      return;
    }

    const task = tasks.find(t => t.id === taskId);
    if (!task) {
      setError('Task not found');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const updatedTask = await toggleTaskCompletion(userId, taskId, !task.status);
      setTasks(tasks.map(t => t.id === taskId ? updatedTask : t));
    } catch (err: any) {
      setError(err.message || 'Failed to toggle completion');
      console.error('Toggle completion error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">API Integration Test</h1>

      <div className="mb-6 p-4 bg-gray-100 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">User ID</h2>
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="w-full p-2 border rounded"
          placeholder="Enter user ID"
        />
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <p>Error: {error}</p>
        </div>
      )}

      {loading && <div className="mb-4 p-4 text-center">Loading...</div>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="p-4 bg-white border rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Create Task</h3>
          <div className="space-y-3">
            <input
              type="text"
              value={newTask.title}
              onChange={(e) => setNewTask({...newTask, title: e.target.value})}
              className="w-full p-2 border rounded"
              placeholder="Task title"
            />
            <input
              type="text"
              value={newTask.description}
              onChange={(e) => setNewTask({...newTask, description: e.target.value})}
              className="w-full p-2 border rounded"
              placeholder="Task description"
            />
            <select
              value={newTask.priority}
              onChange={(e) => setNewTask({...newTask, priority: e.target.value as any})}
              className="w-full p-2 border rounded"
            >
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
            <button
              onClick={handleCreateTask}
              disabled={loading}
              className="w-full p-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
            >
              Create Task
            </button>
          </div>
        </div>

        <div className="p-4 bg-white border rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Operations</h3>
          <div className="space-y-3">
            <input
              type="text"
              value={taskId}
              onChange={(e) => setTaskId(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="Task ID for operations"
            />
            <button
              onClick={handleUpdateTask}
              disabled={loading}
              className="w-full p-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 disabled:opacity-50"
            >
              Update Task
            </button>
            <button
              onClick={handleDeleteTask}
              disabled={loading}
              className="w-full p-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50"
            >
              Delete Task
            </button>
            <button
              onClick={handleToggleCompletion}
              disabled={loading}
              className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
            >
              Toggle Completion
            </button>
            <button
              onClick={loadTasks}
              disabled={loading}
              className="w-full p-2 bg-purple-500 text-white rounded hover:bg-purple-600 disabled:opacity-50"
            >
              Refresh Tasks
            </button>
          </div>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Current Tasks ({tasks.length})</h2>
        {tasks.length === 0 ? (
          <p className="text-gray-500">No tasks found</p>
        ) : (
          <div className="space-y-3">
            {tasks.map(task => (
              <div key={task.id} className="p-4 border rounded-lg bg-white">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className={`font-medium ${task.status ? 'line-through text-gray-500' : ''}`}>
                      {task.title}
                    </h3>
                    <p className="text-gray-600 text-sm">{task.description}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`px-2 py-1 text-xs rounded ${
                        task.priority === 'Critical' ? 'bg-red-100 text-red-800' :
                        task.priority === 'High' ? 'bg-orange-100 text-orange-800' :
                        task.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {task.priority}
                      </span>
                      <span className="text-xs text-gray-500">
                        {task.status ? 'Completed' : 'Pending'}
                      </span>
                    </div>
                  </div>
                  <div className="text-right text-xs text-gray-500">
                    <div>ID: {task.id}</div>
                    <div>Created: {new Date(task.created_at).toLocaleDateString()}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TestPage;