// components/ChatInterface.tsx
"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Send, X, Bot, User } from 'lucide-react';
import { useChatService } from '@/hooks/useChatService';
import ConfirmDialog from '@/components/ui/confirm-dialog';
import InputDialog from '@/components/ui/input-dialog';

interface ChatInterfaceProps {
  onClose: () => void;
}

const ChatInterface = ({ onClose }: ChatInterfaceProps) => {
  const [inputValue, setInputValue] = useState('');
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const [showNewChatDialog, setShowNewChatDialog] = useState(false);
  const [showRenameDialog, setShowRenameDialog] = useState<{sessionId: string | null, title: string}>({sessionId: null, title: ''});
  const [showDeleteDialog, setShowDeleteDialog] = useState<{sessionId: string | null, title: string}>({sessionId: null, title: ''});

  const {
    messages,
    currentSessionId,
    sessions,
    isLoading,
    sendMessage,
    createNewSession,
    loadSession,
    loadSessions,
    deleteSession,
    updateSessionTitle,
    formatDate
  } = useChatService();

  // Scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    try {
      await sendMessage(inputValue);
      setInputValue('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleNewChat = async () => {
    setShowNewChatDialog(true);
  };

  const handleCreateNewSession = (title: string) => {
    createNewSession(title || "New Conversation");
    setShowNewChatDialog(false);
  };

  const handleRenameSession = (sessionId: string, title: string) => {
    updateSessionTitle(sessionId, title);
    setShowRenameDialog({sessionId: null, title: ''});
  };

  const handleDeleteSession = (sessionId: string) => {
    deleteSession(sessionId);
    setShowDeleteDialog({sessionId: null, title: ''});
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center space-x-2">
          <Bot className="h-5 w-5 text-blue-500" />
          <h2 className="text-lg font-semibold">AI Assistant</h2>
          <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">
            Online
          </span>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" onClick={handleNewChat} disabled={isLoading}>
            + New Chat
          </Button>
          <Button variant="ghost" size="icon" onClick={onClose} aria-label="Close chat">
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Chat Sessions Selector */}
      <div className="border-b border-gray-200 bg-gray-50 p-2 overflow-x-auto">
        <div className="flex space-x-2">
          {sessions.map((session) => (
            <div key={session.id} className="relative group">
              <button
                onClick={() => loadSession(session.id)}
                className={`px-3 py-1 text-sm rounded-full whitespace-nowrap ${
                  session.id === currentSessionId
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {session.title.substring(0, 20)}{session.title.length > 20 ? '...' : ''}
              </button>
              <div className="absolute -top-1 -right-1 opacity-0 group-hover:opacity-100 transition-opacity flex space-x-1">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowRenameDialog({sessionId: session.id, title: session.title});
                  }}
                  className="bg-blue-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs hover:bg-blue-600"
                  title="Rename conversation"
                >
                  ✏
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowDeleteDialog({sessionId: session.id, title: session.title});
                  }}
                  className="bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs hover:bg-red-600"
                  title="Delete conversation"
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4 bg-white" ref={scrollAreaRef}>
        <div className="space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender_type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  message.sender_type === 'user'
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : 'bg-gray-100 text-gray-800 rounded-bl-none'
                }`}
              >
                <div className="whitespace-pre-wrap break-words">{message.content}</div>
                <div className={`text-xs mt-1 ${message.sender_type === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                  {formatDate(message.timestamp)}
                </div>
              </div>
            </div>
          ))}

          {isLoading && messages.length > 0 && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-800 rounded-2xl rounded-bl-none px-4 py-3">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200 bg-gray-50">
        <div className="flex space-x-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask me to create, update, or manage your tasks..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={!inputValue.trim() || isLoading}>
            <Send className="h-4 w-4" />
          </Button>
        </div>
        <p className="text-xs text-gray-500 mt-2 text-center">
          AI Assistant can help you manage your tasks • Powered by OpenAI
        </p>
      </form>

      {/* New Chat Dialog */}
      <InputDialog
        isOpen={showNewChatDialog}
        onClose={() => setShowNewChatDialog(false)}
        onConfirm={handleCreateNewSession}
        title="Start New Conversation"
        placeholder="Enter conversation name"
        initialValue="New Conversation"
        confirmText="Create"
        cancelText="Cancel"
      />

      {/* Rename Dialog */}
      <InputDialog
        isOpen={!!showRenameDialog.sessionId}
        onClose={() => setShowRenameDialog({sessionId: null, title: ''})}
        onConfirm={(value) => handleRenameSession(showRenameDialog.sessionId!, value)}
        title="Rename Conversation"
        placeholder="Enter new name"
        initialValue={showRenameDialog.title}
        confirmText="Rename"
        cancelText="Cancel"
      />

      {/* Delete Dialog */}
      <ConfirmDialog
        isOpen={!!showDeleteDialog.sessionId}
        onClose={() => setShowDeleteDialog({sessionId: null, title: ''})}
        onConfirm={() => handleDeleteSession(showDeleteDialog.sessionId!)}
        title="Delete Conversation"
        message={`Are you sure you want to delete the conversation "${showDeleteDialog.title}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
      />
    </div>
  );
};

export default ChatInterface;