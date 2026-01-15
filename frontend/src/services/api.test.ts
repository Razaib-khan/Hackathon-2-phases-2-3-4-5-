import axios from 'axios';
import getApiService, {
  getTasks,
  getTask,
  createTask,
  updateTask,
  deleteTask,
  toggleTaskCompletion,
  Task,
  CreateTaskRequest,
  UpdateTaskRequest
} from './api';

// Mock axios to test the service without making actual network requests
jest.mock('axios');

describe('API Service', () => {
  const mockUserId = 'test-user-id';
  const mockTaskId = 'test-task-id';
  const mockTask: Task = {
    id: mockTaskId,
    user_id: mockUserId,
    title: 'Test Task',
    description: 'Test Description',
    priority: 'High',
    timestamp: new Date().toISOString(),
    status: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock the axios.create return value with proper interceptors
    (axios.create as jest.MockedFunction<typeof axios.create>).mockReturnValue({
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn(),
      patch: jest.fn(),
      interceptors: {
        request: { use: jest.fn() },
        response: { use: jest.fn() }
      }
    } as any);
  });

  describe('getTasks', () => {
    it('should fetch tasks for a user', async () => {
      const mockResponse = {
        data: {
          tasks: [mockTask],
          total: 1,
          page: 1,
          limit: 20
        }
      };

      const axiosInstance = (axios.create as jest.MockedFunction<typeof axios.create>).mock.results[0].value;
      (axiosInstance.get as jest.MockedFunction<any>).mockResolvedValue(mockResponse);

      const result = await getTasks(mockUserId);

      expect(axiosInstance.get).toHaveBeenCalledWith(`/api/${mockUserId}/tasks`, { params: undefined });
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('createTask', () => {
    it('should create a new task', async () => {
      const taskData: CreateTaskRequest = {
        title: 'New Task',
        priority: 'Medium'
      };

      const mockResponse = { data: mockTask };

      const axiosInstance = (axios.create as jest.MockedFunction<typeof axios.create>).mock.results[0].value;
      (axiosInstance.post as jest.MockedFunction<any>).mockResolvedValue(mockResponse);

      const result = await createTask(mockUserId, taskData);

      expect(axiosInstance.post).toHaveBeenCalledWith(`/api/${mockUserId}/tasks`, taskData);
      expect(result).toEqual(mockTask);
    });
  });

  describe('updateTask', () => {
    it('should update an existing task', async () => {
      const updateData: UpdateTaskRequest = {
        title: 'Updated Task',
        status: true
      };

      const mockResponse = { data: { ...mockTask, title: 'Updated Task', status: true } };

      const axiosInstance = (axios.create as jest.MockedFunction<typeof axios.create>).mock.results[0].value;
      (axiosInstance.put as jest.MockedFunction<any>).mockResolvedValue(mockResponse);

      const result = await updateTask(mockUserId, mockTaskId, updateData);

      expect(axiosInstance.put).toHaveBeenCalledWith(`/api/${mockUserId}/tasks/${mockTaskId}`, updateData);
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('deleteTask', () => {
    it('should delete a task', async () => {
      const axiosInstance = (axios.create as jest.MockedFunction<typeof axios.create>).mock.results[0].value;
      (axiosInstance.delete as jest.MockedFunction<any>).mockResolvedValue({});

      await expect(deleteTask(mockUserId, mockTaskId)).resolves.not.toThrow();
      expect(axiosInstance.delete).toHaveBeenCalledWith(`/api/${mockUserId}/tasks/${mockTaskId}`);
    });
  });

  describe('toggleTaskCompletion', () => {
    it('should toggle task completion status', async () => {
      const mockResponse = { data: { ...mockTask, status: true } };

      const axiosInstance = (axios.create as jest.MockedFunction<typeof axios.create>).mock.results[0].value;
      (axiosInstance.patch as jest.MockedFunction<any>).mockResolvedValue(mockResponse);

      const result = await toggleTaskCompletion(mockUserId, mockTaskId, true);

      expect(axiosInstance.patch).toHaveBeenCalledWith(`/api/${mockUserId}/tasks/${mockTaskId}/complete`, { complete: true });
      expect(result).toEqual(mockResponse.data);
    });
  });
});