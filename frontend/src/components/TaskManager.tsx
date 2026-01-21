// Example usage of the API service in a Next.js component
import { useState, useEffect } from 'react';
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  toggleTaskCompletion,
  Task,
  CreateTaskRequest
} from '@/services/api';

const TaskManager = ({ userId }: { userId: string }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [newTask, setNewTask] = useState<Omit<CreateTaskRequest, 'priority'> & { priority: string }>({
    title: '',
    description: '',
    priority: 'Medium'
  });

  // Load tasks on component mount
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const response = await getTasks(userId);
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTask.title.trim()) return;

    try {
      const taskData: CreateTaskRequest = {
        title: newTask.title,
        description: newTask.description,
        priority: newTask.priority as 'Critical' | 'High' | 'Medium' | 'Low',
      };

      const createdTask = await createTask(userId, taskData);
      setTasks([...tasks, createdTask]);
      setNewTask({ title: '', description: '', priority: 'Medium' });
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleToggleComplete = async (taskId: string, currentStatus: boolean) => {
    try {
      const updatedTask = await toggleTaskCompletion(userId, taskId, !currentStatus);
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await deleteTask(userId, taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  if (loading) return <div>Loading tasks...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Task Manager</h1>

      {/* Create Task Form */}
      <form onSubmit={handleCreateTask} className="mb-8 p-4 border rounded-lg">
        <h2 className="text-xl mb-4">Create New Task</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Title *</label>
            <input
              type="text"
              value={newTask.title}
              onChange={(e) => setNewTask({...newTask, title: e.target.value})}
              className="w-full px-3 py-2 border rounded-md"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Priority</label>
            <select
              value={newTask.priority}
              onChange={(e) => setNewTask({...newTask, priority: e.target.value})}
              className="w-full px-3 py-2 border rounded-md"
            >
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <input
              type="text"
              value={newTask.description}
              onChange={(e) => setNewTask({...newTask, description: e.target.value})}
              className="w-full px-3 py-2 border rounded-md"
            />
          </div>
        </div>
        <button
          type="submit"
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
        >
          Add Task
        </button>
      </form>

      {/* Tasks List */}
      <div>
        <h2 className="text-xl mb-4">Your Tasks ({tasks.length})</h2>
        {tasks.length === 0 ? (
          <p>No tasks found.</p>
        ) : (
          <div className="space-y-4">
            {tasks.map((task) => (
              <div key={task.id} className="p-4 border rounded-lg flex justify-between items-center">
                <div>
                  <h3 className={`font-medium ${task.status ? 'line-through text-gray-500' : ''}`}>
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className="text-gray-600 mt-1">{task.description}</p>
                  )}
                  <div className="flex items-center mt-2 space-x-4">
                    <span className={`px-2 py-1 rounded text-xs ${
                      task.priority === 'Critical' ? 'bg-red-100 text-red-800' :
                      task.priority === 'High' ? 'bg-orange-100 text-orange-800' :
                      task.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {task.priority}
                    </span>
                    <span className="text-xs text-gray-500">
                      Created: {new Date(task.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleToggleComplete(task.id, task.status)}
                    className={`px-3 py-1 rounded text-sm ${
                      task.status
                        ? 'bg-gray-200 text-gray-800 hover:bg-gray-300'
                        : 'bg-green-500 text-white hover:bg-green-600'
                    }`}
                  >
                    {task.status ? 'Mark Incomplete' : 'Mark Complete'}
                  </button>
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskManager;