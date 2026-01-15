import React, { useState, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react';
import { getTasks, Task } from '../../services/api'; // Import the API service and Task interface
import TaskItem from '../TaskItem/TaskItem';
import SearchBar from '../SearchFilter/SearchBar';
import FilterControls, { FilterOptions } from '../SearchFilter/FilterControls';

// Define the props interface
interface TaskListProps {
  userId: string; // Add userId prop for API calls
  onEditTask: (task: Task) => void;
  onTaskUpdate?: (task: Task) => void;  // Make optional for backward compatibility
  onDeleteTask: (id: string) => void;
}

// Define the ref type for exposing methods
export interface TaskListHandle {
  refreshTasks: () => void;
}

const TaskList = forwardRef<TaskListHandle, TaskListProps>(({ userId, onEditTask, onTaskUpdate, onDeleteTask }, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    priority: 'all',
    status: 'all',
    startDate: '',
    endDate: '',
  });

  // Expose refreshTasks function to parent components
  useImperativeHandle(ref, () => ({
    refreshTasks: fetchFilteredTasks
  }));

  // Function to fetch tasks with search and filter parameters
  const fetchFilteredTasks = useCallback(async () => {
    // Validate userId format before making API call
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(userId)) {
      setError('Invalid user ID format. Please ensure you are logged in.');
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      // Prepare API parameters based on current filters
      const params: any = {};

      if (searchTerm) {
        params.search = searchTerm;
      }

      // Map priority filter to API parameter
      if (filterOptions.priority && filterOptions.priority !== 'all') {
        params.priority = filterOptions.priority === 'critical' ? 'Critical' :
                         filterOptions.priority === 'low' ? 'Low' :
                         filterOptions.priority === 'medium' ? 'Medium' :
                         filterOptions.priority === 'high' ? 'High' : undefined;
      }

      // Map status filter to API parameter
      if (filterOptions.status && filterOptions.status !== 'all') {
        if (filterOptions.status === 'done') {
          params.status_filter = 'complete';
        } else if (filterOptions.status === 'todo' || filterOptions.status === 'in-progress') {
          params.status_filter = 'incomplete';
        }
      }

      // Add date range filters - only if dates are valid and not empty
      if (filterOptions.startDate && filterOptions.startDate.trim() !== '') {
        params.timestamp_from = filterOptions.startDate;
      }
      if (filterOptions.endDate && filterOptions.endDate.trim() !== '') {
        params.timestamp_to = filterOptions.endDate;
      }

      // Call the API with the prepared parameters
      const response = await getTasks(userId, params);
      setTasks(response?.tasks || []);
    } catch (error) {
      console.error('Failed to fetch filtered tasks:', error);
      setError('Failed to load tasks. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [userId, searchTerm, filterOptions]);

  // Fetch tasks when search or filter criteria change
  useEffect(() => {
    // Debounce API calls to avoid excessive requests
    const debounceTimer = setTimeout(() => {
      fetchFilteredTasks();
    }, 300); // 300ms delay to avoid too many API calls

    // Cleanup function to clear the timer
    return () => clearTimeout(debounceTimer);
  }, [searchTerm, filterOptions, fetchFilteredTasks]);

  // Fetch initial tasks when component mounts
  useEffect(() => {
    // Validate userId format before making API call
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(userId)) {
      setError('Invalid user ID format. Please ensure you are logged in.');
      setLoading(false);
      return;
    }

    fetchFilteredTasks();
  }, [fetchFilteredTasks, userId]);

  const handleSearchChange = (searchTerm: string) => {
    setSearchTerm(searchTerm);
  };

  const handleFilterChange = (filters: FilterOptions) => {
    setFilterOptions(filters);
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Task List</h2>

      {/* Search and Filter Controls */}
      <div className="mb-8">
        <SearchBar onSearchChange={handleSearchChange} />
        <FilterControls onFilterChange={handleFilterChange} />
      </div>

      {/* Error indicator */}
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <p>{error}</p>
        </div>
      )}

      {/* Loading indicator */}
      {loading && (
        <div className="text-center py-10 bg-white rounded-lg shadow-sm border border-gray-200">
          <p className="text-gray-500">Loading tasks...</p>
        </div>
      )}

      {/* Task List */}
      {!loading && !error && tasks && tasks.length === 0 ? (
        <div className="text-center py-10 bg-white rounded-lg shadow-sm border border-gray-200">
          <p className="text-gray-500">
            {searchTerm || filterOptions.priority !== 'all' || filterOptions.status !== 'all' || filterOptions.startDate || filterOptions.endDate
              ? 'No tasks match your search and filter criteria'
              : 'No tasks available'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks?.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onUpdateTask={onTaskUpdate || onEditTask} // Use onTaskUpdate for status changes, fallback to onEditTask for backward compatibility
              onEditTask={onEditTask} // Add new prop for edit requests
              onDeleteTask={onDeleteTask}
            />
          ))}
        </div>
      )}
    </div>
  );
});

export default TaskList;
