import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import FilterControls, { FilterOptions } from './FilterControls';

describe('FilterControls', () => {
  const mockOnFilterChange = jest.fn();
  const defaultProps = {
    onFilterChange: mockOnFilterChange,
  };

  beforeEach(() => {
    mockOnFilterChange.mockClear();
  });

  test('renders all filter controls', () => {
    render(<FilterControls {...defaultProps} />);

    expect(screen.getByLabelText(/Priority/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Status/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Start Date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/End Date/i)).toBeInTheDocument();
    expect(screen.getByText(/Clear Filters/i)).toBeInTheDocument();
  });

  test('handles priority filter changes', () => {
    render(<FilterControls {...defaultProps} />);

    const highPriorityButton = screen.getByText('High');
    fireEvent.click(highPriorityButton);

    expect(mockOnFilterChange).toHaveBeenCalledWith({
      priority: 'high',
      status: 'all',
      startDate: '',
      endDate: ''
    });
  });

  test('handles status filter changes', () => {
    render(<FilterControls {...defaultProps} />);

    const doneStatusButton = screen.getByText('Done');
    fireEvent.click(doneStatusButton);

    expect(mockOnFilterChange).toHaveBeenCalledWith({
      priority: 'all',
      status: 'done',
      startDate: '',
      endDate: ''
    });
  });

  test('handles date filter changes', () => {
    render(<FilterControls {...defaultProps} />);

    const startDateInput = screen.getByLabelText(/Start Date/i);
    fireEvent.change(startDateInput, { target: { value: '2023-01-01' } });

    expect(mockOnFilterChange).toHaveBeenCalledWith({
      priority: 'all',
      status: 'all',
      startDate: '2023-01-01',
      endDate: ''
    });
  });

  test('clears filters when Clear Filters button is clicked', () => {
    render(<FilterControls {...defaultProps} />);

    // First change a filter
    const highPriorityButton = screen.getByText('High');
    fireEvent.click(highPriorityButton);

    // Then click clear filters
    const clearButton = screen.getByText(/Clear Filters/i);
    fireEvent.click(clearButton);

    expect(mockOnFilterChange).toHaveBeenLastCalledWith({
      priority: 'all',
      status: 'all',
      startDate: '',
      endDate: ''
    });
  });
});