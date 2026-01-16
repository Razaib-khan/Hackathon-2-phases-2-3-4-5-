import axios from 'axios';

// Create a base axios instance with common configuration
const http = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-todo-backend.hf.space',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token if available
http.interceptors.request.use(
  (config: any) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle common responses
http.interceptors.response.use(
  (response: any) => response,
  (error: any) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access - possibly remove token and redirect
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        // Optionally redirect to login page
        // window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default http;