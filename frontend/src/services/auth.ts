import http from './http';

// Define TypeScript interfaces for authentication
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

export interface SignupData {
  email: string;
  password: string;
  name?: string;
}

export interface SigninData {
  email: string;
  password: string;
}

export interface PasswordChangeData {
  currentPassword: string;
  newPassword: string;
}

export interface PasswordRecoveryData {
  email: string;
}

export interface PasswordResetData {
  token: string;
  newPassword: string;
}

// Remove this interface since we're not using it anymore
// DeleteAccountData is no longer needed as we're passing password directly

class AuthService {
  private static instance: AuthService;
  private token: string | null = null;
  private currentUser: User | null = null;

  private constructor() {
    // Initialize token from localStorage if available for consistency with AuthContext
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('access_token');
      if (storedToken) {
        this.token = storedToken;
        http.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
      }
    }
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  /**
   * Signup a new user
   */
  async signup(signupData: SignupData): Promise<AuthResponse> {
    try {
      const response = await http.post('/api/auth/signup', signupData);
      const { user, token } = response.data;

      this.setAuthToken(token);
      this.currentUser = user;

      // Also store user in localStorage for consistency with AuthContext
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(user));
      }

      return { user, token };
    } catch (error: any) {
      throw this.handleError(error, 'Signup failed');
    }
  }

  /**
   * Sign in an existing user
   */
  async signin(signinData: SigninData): Promise<AuthResponse> {
    try {
      const response = await http.post('/api/auth/signin', signinData);
      const { user, token } = response.data;

      this.setAuthToken(token);
      this.currentUser = user;

      // Also store user in localStorage for consistency with AuthContext
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(user));
      }

      return { user, token };
    } catch (error: any) {
      throw this.handleError(error, 'Signin failed');
    }
  }

  /**
   * Sign out the current user
   */
  async signout(): Promise<void> {
    try {
      // Optionally notify the server about logout
      await http.post('/api/auth/signout', {}, {
        headers: { Authorization: `Bearer ${this.token}` }
      });
    } catch (error: any) {
      // Even if server logout fails, we still clear local state
      console.warn('Server signout failed:', error.message);
    } finally {
      this.clearAuthState();
    }
  }

  /**
   * Change user's password
   */
  async changePassword(passwordData: PasswordChangeData): Promise<{ message: string }> {
    try {
      if (!this.token) {
        throw new Error('User not authenticated');
      }

      const response = await http.put('/api/auth/password/change', passwordData, {
        headers: { Authorization: `Bearer ${this.token}` }
      });

      return response.data;
    } catch (error: any) {
      throw this.handleError(error, 'Password change failed');
    }
  }

  /**
   * Request password recovery (send reset link)
   */
  async requestPasswordRecovery(recoveryData: PasswordRecoveryData): Promise<{ message: string }> {
    try {
      const response = await http.post('/api/auth/password/recovery', recoveryData);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error, 'Password recovery request failed');
    }
  }

  /**
   * Reset password using recovery token
   */
  async resetPassword(resetData: PasswordResetData): Promise<{ message: string }> {
    try {
      const response = await http.post('/api/auth/password/reset', resetData);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error, 'Password reset failed');
    }
  }

  /**
   * Delete user account
   */
  async deleteAccount(password: string): Promise<{ message: string }> {
    try {
      if (!this.token) {
        throw new Error('User not authenticated');
      }

      const deleteData = { password }; // Create the expected payload

      const response = await http.delete('/api/auth/account', {
        data: deleteData,
        headers: { Authorization: `Bearer ${this.token}` }
      });

      // Clear auth state after successful account deletion
      this.clearAuthState();

      return response.data;
    } catch (error: any) {
      throw this.handleError(error, 'Account deletion failed');
    }
  }

  /**
   * Get current user profile
   */
  async getProfile(): Promise<User> {
    try {
      if (!this.token) {
        throw new Error('User not authenticated');
      }

      const response = await http.get('/api/auth/profile', {
        headers: { Authorization: `Bearer ${this.token}` }
      });

      this.currentUser = response.data;

      // Also store user in localStorage for consistency with AuthContext
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.data));
      }

      return response.data;
    } catch (error: any) {
      throw this.handleError(error, 'Failed to fetch user profile');
    }
  }

  /**
   * Update user profile
   */
  async updateProfile(profileData: Partial<Omit<User, 'id' | 'createdAt' | 'updatedAt'>>): Promise<User> {
    try {
      if (!this.token) {
        throw new Error('User not authenticated');
      }

      const response = await http.put('/api/auth/profile', profileData, {
        headers: { Authorization: `Bearer ${this.token}` }
      });

      this.currentUser = response.data;

      // Also store user in localStorage for consistency with AuthContext
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.data));
      }

      return response.data;
    } catch (error: any) {
      throw this.handleError(error, 'Failed to update user profile');
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.token;
  }

  /**
   * Get current user
   */
  getCurrentUser(): User | null {
    return this.currentUser;
  }

  /**
   * Get auth token
   */
  getToken(): string | null {
    return this.token;
  }

  /**
   * Set auth token and update axios defaults
   */
  private setAuthToken(token: string): void {
    this.token = token;
    // Also store in localStorage for consistency with AuthContext
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
    http.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  /**
   * Clear auth state
   */
  private clearAuthState(): void {
    this.token = null;
    this.currentUser = null;
    // Also clear from localStorage for consistency with AuthContext
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    delete http.defaults.headers.common['Authorization'];
  }

  /**
   * Handle API errors and return user-friendly messages
   */
  private handleError(error: any, defaultMessage: string): Error {
    let errorMessage = defaultMessage;

    if (error.response?.data?.message) {
      errorMessage = error.response.data.message;
    } else if (error.response?.data?.error) {
      errorMessage = error.response.data.error;
    } else if (error.response?.status === 401) {
      errorMessage = 'Unauthorized. Please sign in again.';
      this.clearAuthState(); // Clear invalid token
    } else if (error.response?.status === 403) {
      errorMessage = 'Access forbidden';
    } else if (error.response?.status === 404) {
      errorMessage = 'Resource not found';
    } else if (error.request) {
      errorMessage = 'Network error. Please check your connection.';
    } else {
      errorMessage = error.message || defaultMessage;
    }

    return new Error(errorMessage);
  }
}

export const authService = AuthService.getInstance();

export default authService;