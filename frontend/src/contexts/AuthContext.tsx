'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  favorite_teacher: string;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (firstName: string, lastName: string, email: string, password: string, favoriteTeacher: string) => Promise<void>;
  deleteUser: (password: string) => Promise<void>;
  updateUser: (firstName: string, lastName: string, email: string) => Promise<void>;
  getUserFullName: () => string;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  // Helper to get user's full name
  const getUserFullName = (): string => {
    if (!user) return '';
    return `${user.first_name} ${user.last_name}`;
  };
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check for existing session on initial load
    const storedToken = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
      } catch (error) {
        console.error('Failed to parse stored user data:', error);
        // Clear invalid data
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
      }
    }

    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      // Call the backend API to authenticate user
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      const { user, token } = data;

      localStorage.setItem('access_token', token);
      localStorage.setItem('user', JSON.stringify(user));

      setToken(token);
      setUser(user);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (firstName: string, lastName: string, email: string, password: string, favoriteTeacher: string) => {
    setLoading(true);
    try {
      // Call the backend API to register user
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          email,
          password,  // Note: in a real app, you'd want to hash the password
          favorite_teacher: favoriteTeacher  // Use the actual favorite teacher provided
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      const userData = await response.json();

      // After successful registration, log the user in automatically
      // Call the signin endpoint to get the token
      const loginResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!loginResponse.ok) {
        const errorData = await loginResponse.json();
        throw new Error(errorData.detail || 'Login after registration failed');
      }

      const loginData = await loginResponse.json();
      const { user, token } = loginData;

      localStorage.setItem('access_token', token);
      localStorage.setItem('user', JSON.stringify(user));

      setToken(token);
      setUser(user);
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const updateUser = async (firstName: string, lastName: string, email: string) => {
    setLoading(true);
    try {
      if (!token) {
        throw new Error('User not authenticated');
      }

      // Call the backend API to update user profile
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/auth/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          email,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update profile');
      }

      const updatedUserData = await response.json();

      // Update user in local storage
      localStorage.setItem('user', JSON.stringify(updatedUserData));
      setUser(updatedUserData);
    } catch (error) {
      console.error('Update user failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const deleteUser = async (password: string) => {
    setLoading(true);
    try {
      // Call the backend API to delete the account
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/auth/account`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });

      // Handle network errors
      if (!response.ok) {
        if (response.status >= 400 && response.status < 500) {
          // Client error - likely contains error details
          try {
            const errorData = await response.json();
            throw new Error(errorData.detail || errorData.message || 'Failed to delete account');
          } catch (parseError) {
            // If response is not JSON, use status text
            throw new Error(`Failed to delete account: ${response.statusText}`);
          }
        } else if (response.status >= 500) {
          // Server error
          throw new Error('Server error occurred. Please try again later.');
        } else {
          // Other HTTP errors
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
      }

      const responseData = await response.json();
      console.log('Account deletion response:', responseData);

      // Clear local storage and state after successful deletion
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      setToken(null);
      setUser(null);
    } catch (error) {
      console.error('Delete account failed:', error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error
        throw new Error('Network error: Unable to connect to server. Please check your connection and try again.');
      }
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    // Redirect to signin page after logout using Next.js router which respects basePath
    router.push('/auth/signin');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, register, updateUser, deleteUser, getUserFullName, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};