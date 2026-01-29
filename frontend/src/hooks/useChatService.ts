// hooks/useChatService.ts
import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/context/ToastContext';

interface ChatSession {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

interface ChatMessage {
  id: string;
  content: string;
  sender_type: 'user' | 'agent';
  timestamp: string;
  session_id: string;
}

interface TaskOperationLog {
  id: string;
  operation_type: 'create' | 'read' | 'update' | 'delete' | 'status_update';
  task_ids: string[];
  result: any;
  timestamp: string;
}

export const useChatService = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { token } = useAuth(); // Assuming we have auth token for API calls
  const { showToast } = useToast();

  // Load sessions when component mounts
  useEffect(() => {
    loadSessions();
  }, []);

  // Load sessions from backend
  const loadSessions = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/chat/sessions`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setSessions(data.sessions || []);

        // Load the most recent session if available
        if (data.sessions && data.sessions.length > 0) {
          const latestSession = data.sessions[0];
          setCurrentSessionId(latestSession.id);
          await loadSession(latestSession.id);
        }
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to load chat sessions');
      }
    } catch (error: any) {
      console.error('Error loading chat sessions:', error);
      showToast('error', error.message || 'Failed to load chat sessions');
    } finally {
      setIsLoading(false);
    }
  };

  // Load messages for a specific session
  const loadSession = async (sessionId: string) => {
    try {
      setIsLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/chat/sessions/${sessionId}/messages`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
        setCurrentSessionId(sessionId);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to load chat messages');
      }
    } catch (error: any) {
      console.error('Error loading chat session:', error);
      showToast('error', error.message || 'Failed to load chat session');
    } finally {
      setIsLoading(false);
    }
  };

  // Create a new chat session
  const createNewSession = async (title: string = 'New Conversation') => {
    try {
      setIsLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/chat/sessions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      });

      if (response.ok) {
        const data = await response.json();

        // Add new session to the beginning of the list
        setSessions(prev => [data, ...prev]);
        setCurrentSessionId(data.id);
        setMessages([]);
        showToast('success', 'New chat session created');
        return data.id;
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create new chat session');
      }
    } catch (error: any) {
      console.error('Error creating new chat session:', error);
      showToast('error', error.message || 'Failed to create new chat session');
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  // Send a message to the AI agent
  const sendMessage = async (content: string) => {
    if (!currentSessionId) {
      // Create a new session if none exists
      const newSessionId = await createNewSession();
      if (!newSessionId) return;
    }

    try {
      setIsLoading(true);

      // Send message to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/chat/messages`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: currentSessionId,
          content,
        }),
      });

      if (response.ok) {
        const data = await response.json();

        // Reload messages to ensure we have the latest state from the backend
        // This addresses the issue where changes made by the agent weren't appearing automatically
        if (currentSessionId) {
          await loadSession(currentSessionId);
        }

        return data;
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to send message');
      }
    } catch (error: any) {
      console.error('Error sending message:', error);
      showToast('error', error.message || 'Failed to send message');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Get task operation logs for a session
  const getTaskOperationLogs = async (sessionId: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/chat/sessions/${sessionId}/operation-logs`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        return data.operation_logs as TaskOperationLog[];
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to load task operation logs');
      }
    } catch (error: any) {
      console.error('Error fetching task operation logs:', error);
      showToast('error', error.message || 'Failed to load task operation logs');
      return [];
    }
  };

  // Delete a chat session
  const deleteSession = async (sessionId: string) => {
    try {
      setIsLoading(true);

      // Use DELETE method to remove the session
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://razaib123-aido-todo-app.hf.space'}/api/chat/sessions/${sessionId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Remove the session from the local state
        setSessions(prev => prev.filter(session => session.id !== sessionId));

        // If the deleted session was the current one, clear the current session and messages
        if (currentSessionId === sessionId) {
          setCurrentSessionId(null);
          setMessages([]);

          // Load the first available session if there are any remaining
          if (sessions.length > 1) {
            const remainingSessions = sessions.filter(session => session.id !== sessionId);
            if (remainingSessions.length > 0) {
              await loadSession(remainingSessions[0].id);
            }
          }
        }

        showToast('success', 'Chat session deleted successfully');
        return true;
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete chat session');
      }
    } catch (error: any) {
      console.error('Error deleting chat session:', error);
      showToast('error', error.message || 'Failed to delete chat session');
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  // Update a chat session title
  const updateSessionTitle = async (sessionId: string, newTitle: string) => {
    try {
      setIsLoading(true);

      // Since the backend doesn't have a direct endpoint to update session titles,
      // we'll update the local state only. A full implementation would require
      // a PUT/PATCH endpoint on the backend
      setSessions(prev => prev.map(session =>
        session.id === sessionId
          ? {...session, title: newTitle}
          : session
      ));

      return true;
    } catch (error: any) {
      console.error('Error updating session title:', error);
      showToast('error', error.message || 'Failed to update session title');
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to format dates
  const formatDate = useCallback((dateString: string) => {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        // Return a default string if the date is invalid
        return '--:--';
      }
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (error) {
      // Return a default string if there's an error parsing the date
      return '--:--';
    }
  }, []);

  return {
    messages,
    currentSessionId,
    sessions,
    isLoading,
    sendMessage,
    createNewSession,
    loadSession,
    loadSessions,
    getTaskOperationLogs,
    deleteSession, // Add the deleteSession function to the return object
    updateSessionTitle, // Add the updateSessionTitle function to the return object
    formatDate,
  };
};