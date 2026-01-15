import React from 'react';

export interface FilterOptions {
  priority?: 'low' | 'medium' | 'high' | 'all';
  status?: 'todo' | 'in-progress' | 'done' | 'all';
  startDate?: string;
  endDate?: string;
}

export interface FilterControlsProps {
  onFilterChange: (filters: FilterOptions) => void;
}

declare const FilterControls: React.FC<FilterControlsProps>;

export default FilterControls;