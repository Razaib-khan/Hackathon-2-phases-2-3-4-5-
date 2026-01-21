import React, { useState } from 'react';
import { toggleTaskCompletion, deleteTask as deleteTaskAPI, updateTask as updateTaskAPI, Task as TaskType } from '@/services/api';
import ConfirmationModal from '@/components/Modal/ConfirmationModal';

// Define the task type based on API contract
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  timestamp: string; // ISO date-time format
  status: boolean; // completion status
  created_at: string; // ISO date-time format
  updated_at: string; // ISO date-time format
}

// Define the props interface
interface TaskItemProps {
  task: Task;
  onUpdateTask: (task: Task) => void;
  onEditTask?: (task: Task) => void;  // Make optional for backward compatibility
  onDeleteTask: (id: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onUpdateTask, onEditTask, onDeleteTask }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Get priority color class
  const getPriorityClass = (priority: Task['priority']) => {
    switch (priority) {
      case 'Critical':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'High':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  // Handle completion toggle
  const handleToggleCompletion = async () => {
    if (isUpdating) return; // Prevent multiple clicks

    setIsUpdating(true);
    try {
      const updatedTask = await toggleTaskCompletion(task.user_id, task.id, !task.status);
      // Update the parent component's state with the updated task
      onUpdateTask(updatedTask);
    } catch (error: any) {
      console.error('Failed to toggle task completion:', error);
      let errorMsg = 'Failed to update task completion status.';

      if (error.response?.data?.detail) {
        errorMsg += ` ${error.response.data.detail}`;
      } else if (error.message) {
        errorMsg += ` ${error.message}`;
      }

      setErrorMessage(errorMsg);
      setShowErrorModal(true);
    } finally {
      setIsUpdating(false);
    }
  };

  // Handle task deletion
  const handleDeleteTask = () => {
    if (isDeleting) return; // Prevent multiple clicks
    setShowDeleteModal(true);
  };

  const confirmDeleteTask = async () => {
    setIsDeleting(true);
    try {
      await deleteTaskAPI(task.user_id, task.id);
      // Notify parent component to remove the task from the list
      onDeleteTask(task.id);
      setShowDeleteModal(false);
    } catch (error: any) {
      console.error('Failed to delete task:', error);
      let errorMsg = 'Failed to delete task.';

      if (error.response?.data?.detail) {
        errorMsg += ` ${error.response.data.detail}`;
      } else if (error.message) {
        errorMsg += ` ${error.message}`;
      }

      setErrorMessage(errorMsg);
      setShowErrorModal(true);
    } finally {
      setIsDeleting(false);
    }
  };

  const cancelDeleteTask = () => {
    setShowDeleteModal(false);
  };

  return (
    <>
      <div className={`bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden transition-all duration-200 hover:shadow-md ${task.status ? 'opacity-75 bg-gray-50' : ''}`}>
        <div className="p-4 md:p-5">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-2">
                {/* Completion Checkbox */}
                <button
                  onClick={handleToggleCompletion}
                  disabled={isUpdating}
                  className={`flex-shrink-0 w-5 h-5 rounded border flex items-center justify-center ${
                    task.status
                      ? 'bg-green-500 border-green-500 text-white'
                      : 'border-gray-300 hover:border-green-400'
                  } transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-300`}
                  aria-label={task.status ? 'Mark as incomplete' : 'Mark as complete'}
                >
                  {task.status && (
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  )}
                </button>

                <h3 className={`font-semibold truncate ${task.status ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                  {task.title}
                </h3>
                <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getPriorityClass(task.priority)}`}>
                  {task.priority}
                </span>
              </div>

              <div className="flex items-center gap-3 ml-8"> {/* Indent to align with checkbox */}
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                  task.status
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {task.status ? 'Completed' : 'Pending'}
                </span>
                <span className="text-xs text-gray-500">
                  {new Date(task.timestamp).toLocaleDateString()}
                </span>
              </div>
            </div>

            <div className="flex gap-2 mt-2 md:mt-0">
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md transition-colors"
                disabled={isUpdating || isDeleting}
              >
                {isExpanded ? 'Show Less' : 'Details'}
              </button>
              <button
                onClick={() => onEditTask && onEditTask(task)}
                className="px-3 py-1.5 text-sm bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-md transition-colors"
                disabled={isUpdating || isDeleting}
              >
                Edit
              </button>
              <button
                onClick={handleDeleteTask}
                className="px-3 py-1.5 text-sm bg-red-100 hover:bg-red-200 text-red-700 rounded-md transition-colors"
                disabled={isUpdating || isDeleting}
              >
                {isDeleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>

          {isExpanded && (
            <div className="mt-4 pt-4 border-t border-gray-100 ml-8"> {/* Indent to align with checkbox */}
              <p className={`whitespace-pre-wrap ${task.status ? 'text-gray-500' : 'text-gray-600'}`}>
                {task.description || 'No description provided.'}
              </p>
              <div className="mt-3 text-sm text-gray-500">
                <p>Created: {new Date(task.created_at).toLocaleString()}</p>
                <p>Updated: {new Date(task.updated_at).toLocaleString()}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      <ConfirmationModal
        isOpen={showDeleteModal}
        title="Delete Task"
        message={`Are you sure you want to delete the task "${task.title}"? This action cannot be undone.`}
        confirmText="Delete Task"
        cancelText="Cancel"
        onConfirm={confirmDeleteTask}
        onCancel={cancelDeleteTask}
        variant="danger"
      />

      <ConfirmationModal
        isOpen={showErrorModal}
        title="Error"
        message={errorMessage}
        confirmText="OK"
        cancelText=""
        onConfirm={() => setShowErrorModal(false)}
        onCancel={() => setShowErrorModal(false)}
        variant="default"
      />
    </>
  );
};

export default TaskItem;