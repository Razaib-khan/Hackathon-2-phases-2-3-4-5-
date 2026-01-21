// context/ToastContext.tsx
"use client";

import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ToastNotifications from '@/components/ToastNotifications';

interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

type ToastAction =
  | { type: 'ADD_TOAST'; payload: Omit<Toast, 'id'> }
  | { type: 'REMOVE_TOAST'; payload: string };

interface ToastState {
  toasts: Toast[];
}

const ToastContext = createContext<{
  showToast: (type: 'success' | 'error' | 'warning' | 'info', message: string, duration?: number) => void;
  removeToast: (id: string) => void;
}>({
  showToast: () => {},
  removeToast: () => {},
});

const toastReducer = (state: ToastState, action: ToastAction): ToastState => {
  switch (action.type) {
    case 'ADD_TOAST':
      return {
        ...state,
        toasts: [
          ...state.toasts,
          {
            id: uuidv4(),
            type: action.payload.type,
            message: action.payload.message,
            duration: action.payload.duration,
          },
        ],
      };
    case 'REMOVE_TOAST':
      return {
        ...state,
        toasts: state.toasts.filter(toast => toast.id !== action.payload),
      };
    default:
      return state;
  }
};

interface ToastProviderProps {
  children: ReactNode;
}

export const ToastProvider: React.FC<ToastProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(toastReducer, { toasts: [] });

  const showToast = (type: 'success' | 'error' | 'warning' | 'info', message: string, duration?: number) => {
    dispatch({
      type: 'ADD_TOAST',
      payload: { type, message, duration },
    });
  };

  const removeToast = (id: string) => {
    dispatch({ type: 'REMOVE_TOAST', payload: id });
  };

  return (
    <ToastContext.Provider value={{ showToast, removeToast }}>
      {children}
      <ToastNotifications toasts={state.toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};