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
      const response = await fetch('/api/chat/sessions', {
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
      const response = await fetch(`/api/chat/sessions/${sessionId}/messages`, {
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
  const createNewSession = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('/api/chat/sessions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: 'New Conversation' }),
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
      const response = await fetch('/api/chat/messages', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: currentSessionId,
          content,
          sender_type: 'user',
        }),
      });

      if (response.ok) {
        const data = await response.json();

        // Add both user and agent messages to the local state
        setMessages(prev => [...prev, data.user_message, data.agent_response]);

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
      const response = await fetch(`/api/chat/sessions/${sessionId}/operation-logs`, {
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

  // Helper function to format dates
  const formatDate = useCallback((dateString: string) => {
    return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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
    formatDate,
  };
};