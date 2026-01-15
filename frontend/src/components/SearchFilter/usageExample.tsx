import React, { useState } from 'react';
import FilterControls, { FilterOptions } from './FilterControls';

const TaskManager: React.FC = () => {
  const [tasks, setTasks] = useState<any[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<any[]>([]);

  const handleFilterChange = (filters: FilterOptions) => {
    // Apply filters to tasks
    let result = [...tasks];

    if (filters.priority && filters.priority !== 'all') {
      result = result.filter(task => task.priority === filters.priority);
    }

    if (filters.status && filters.status !== 'all') {
      result = result.filter(task => task.status === filters.status);
    }

    if (filters.startDate) {
      result = result.filter(task => new Date(task.timestamp) >= new Date(filters.startDate));
    }

    if (filters.endDate) {
      result = result.filter(task => new Date(task.timestamp) <= new Date(filters.endDate));
    }

    setFilteredTasks(result);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Task Manager</h1>

      <FilterControls onFilterChange={handleFilterChange} />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {filteredTasks.map((task, index) => (
          <div key={index} className="border p-4 rounded">
            <h3>{task.title}</h3>
            <p>Priority: {task.priority}</p>
            <p>Status: {task.status}</p>
            <p>Created: {task.timestamp}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskManager;