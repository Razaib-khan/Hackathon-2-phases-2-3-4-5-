import React, { useState } from 'react';

// Define TypeScript interfaces for our filter options
export interface FilterOptions {
  priority?: 'critical' | 'low' | 'medium' | 'high' | 'all';
  status?: 'todo' | 'in-progress' | 'done' | 'all';
  startDate?: string;
  endDate?: string;
}

interface FilterControlsProps {
  onFilterChange: (filters: FilterOptions) => void;
}

const FilterControls: React.FC<FilterControlsProps> = ({ onFilterChange }) => {
  const [filters, setFilters] = useState<FilterOptions>({
    priority: 'all',
    status: 'all',
    startDate: '',
    endDate: '',
  });

  const handlePriorityChange = (priority: 'critical' | 'low' | 'medium' | 'high' | 'all') => {
    const newFilters = { ...filters, priority };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleStatusChange = (status: 'todo' | 'in-progress' | 'done' | 'all') => {
    const newFilters = { ...filters, status };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleDateChange = (dateType: 'startDate' | 'endDate', value: string) => {
    const newFilters = { ...filters, [dateType]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearFilters = () => {
    const defaultFilters = {
      priority: 'all',
      status: 'all',
      startDate: '',
      endDate: '',
    };
    setFilters(defaultFilters);
    onFilterChange(defaultFilters);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Priority Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
          <div className="flex flex-wrap gap-2">
            {(['all', 'critical', 'low', 'medium', 'high'] as const).map((priority) => (
              <button
                key={priority}
                onClick={() => handlePriorityChange(priority)}
                className={`px-3 py-1 text-xs rounded-full ${
                  filters.priority === priority
                    ? priority === 'critical'
                      ? 'bg-red-500 text-white'
                      : 'bg-blue-500 text-white'
                    : priority === 'critical'
                      ? 'bg-red-200 text-red-700 hover:bg-red-300'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {priority.charAt(0).toUpperCase() + priority.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <div className="flex flex-wrap gap-2">
            {(['all', 'todo', 'in-progress', 'done'] as const).map((status) => (
              <button
                key={status}
                onClick={() => handleStatusChange(status)}
                className={`px-3 py-1 text-xs rounded-full capitalize ${
                  filters.status === status
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {status.replace('-', ' ')}
              </button>
            ))}
          </div>
        </div>

        {/* Start Date Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
          <input
            type="date"
            value={filters.startDate}
            onChange={(e) => handleDateChange('startDate', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* End Date Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
          <input
            type="date"
            value={filters.endDate}
            onChange={(e) => handleDateChange('endDate', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {/* Clear Filters Button */}
      <div className="mt-4 flex justify-end">
        <button
          onClick={clearFilters}
          className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
};

export default FilterControls;