import React, { createContext, useContext, ReactNode } from 'react';

interface TaskRefreshContextType {
  refreshTasks: () => void;
}

const TaskRefreshContext = createContext<TaskRefreshContextType | undefined>(undefined);

interface TaskRefreshProviderProps {
  children: ReactNode;
  onRefresh: () => void;
}

export const TaskRefreshProvider: React.FC<TaskRefreshProviderProps> = ({ children, onRefresh }) => {
  const refreshTasks = () => {
    onRefresh();
  };

  return (
    <TaskRefreshContext.Provider value={{ refreshTasks }}>
      {children}
    </TaskRefreshContext.Provider>
  );
};

export const useTaskRefresh = (): TaskRefreshContextType => {
  const context = useContext(TaskRefreshContext);
  if (context === undefined) {
    throw new Error('useTaskRefresh must be used within a TaskRefreshProvider');
  }
  return context;
};