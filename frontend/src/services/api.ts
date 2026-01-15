import http from './http';

// Define TypeScript interfaces based on the API contract
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

export interface CreateTaskRequest {
  title: string;
  description?: string;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  timestamp?: string; // ISO date-time format
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  priority?: 'Critical' | 'High' | 'Medium' | 'Low';
  status?: boolean;
}

export interface TaskResponse {
  tasks: Task[];
  total: number;
  page: number;
  limit: number;
}

export interface ToggleCompletionRequest {
  complete: boolean;
}

export interface ApiResponse<T = any> {
  data: T;
}

class ApiService {
  // Use the shared http instance
  private axiosClient = http;

  constructor() {
    // Interceptors are already set up in the http instance
  }

  // GET all tasks for a user with optional filters
  async getTasks(
    userId: string,
    params?: {
      search?: string;
      priority?: 'Critical' | 'High' | 'Medium' | 'Low';
      status?: 'complete' | 'incomplete';
      timestamp_from?: string;
      timestamp_to?: string;
      page?: number;
      limit?: number;
    }
  ): Promise<TaskResponse> {
    try {
      const response: any = await this.axiosClient.get(`/api/${userId}/tasks`, { params });
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // GET a specific task
  async getTask(userId: string, taskId: string): Promise<Task> {
    try {
      const response: any = await this.axiosClient.get(`/api/${userId}/tasks/${taskId}`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // POST - Create a new task
  async createTask(userId: string, taskData: CreateTaskRequest): Promise<Task> {
    try {
      const response: any = await this.axiosClient.post(
        `/api/${userId}/tasks`,
        taskData
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // PUT - Update a task
  async updateTask(userId: string, taskId: string, taskData: UpdateTaskRequest): Promise<Task> {
    try {
      const response: any = await this.axiosClient.put(
        `/api/${userId}/tasks/${taskId}`,
        taskData
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // DELETE - Delete a task
  async deleteTask(userId: string, taskId: string): Promise<void> {
    try {
      await this.axiosClient.delete(`/api/${userId}/tasks/${taskId}`);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // PATCH - Toggle task completion status
  async toggleTaskCompletion(
    userId: string,
    taskId: string,
    complete: boolean
  ): Promise<Task> {
    try {
      const response: any = await this.axiosClient.patch(
        `/api/${userId}/tasks/${taskId}/complete`,
        { complete }
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // Error handling utility
  private handleError(error: any): void {
    if (error.response) {
      // Server responded with error status
      console.error(`API Error: ${error.response.status} - ${error.response.statusText}`);
      console.error('Response data:', error.response.data);
      console.error('Request URL:', error.config?.url);
      console.error('Request params:', error.config?.params);
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network Error: No response received');
      console.error('Request details:', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
      console.error('Error details:', error);
    }
  }
}

// Create a singleton instance of the API service
let apiService: ApiService | null = null;

// Function to get or create the API service instance
const getApiService = (): ApiService => {
  if (!apiService) {
    apiService = new ApiService();
  }
  return apiService;
};

// Export individual methods as functions that get the service instance when called
export const getTasks = (
  userId: string,
  params?: {
    search?: string;
    priority?: 'Critical' | 'High' | 'Medium' | 'Low';
    status?: 'complete' | 'incomplete';
    timestamp_from?: string;
    timestamp_to?: string;
    page?: number;
    limit?: number;
  }
) => getApiService().getTasks(userId, params);

export const getTask = (userId: string, taskId: string) => getApiService().getTask(userId, taskId);

export const createTask = (userId: string, taskData: CreateTaskRequest) => getApiService().createTask(userId, taskData);

export const updateTask = (userId: string, taskId: string, taskData: UpdateTaskRequest) => getApiService().updateTask(userId, taskId, taskData);

export const deleteTask = (userId: string, taskId: string) => getApiService().deleteTask(userId, taskId);

export const toggleTaskCompletion = (userId: string, taskId: string, complete: boolean) => getApiService().toggleTaskCompletion(userId, taskId, complete);

// Export the service instance as a function to be called when needed
export default getApiService;