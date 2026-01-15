// Simple integration test to verify the API service exports work correctly
import {
  getTasks,
  getTask,
  createTask,
  updateTask,
  deleteTask,
  toggleTaskCompletion
} from '../api';

describe('API Service Integration', () => {
  // These tests verify that the API service exports are available
  // Actual functionality would be tested in an end-to-end environment

  test('should have all required methods exported', () => {
    expect(typeof getTasks).toBe('function');
    expect(typeof getTask).toBe('function');
    expect(typeof createTask).toBe('function');
    expect(typeof updateTask).toBe('function');
    expect(typeof deleteTask).toBe('function');
    expect(typeof toggleTaskCompletion).toBe('function');
  });
});