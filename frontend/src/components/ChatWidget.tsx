// components/ChatWidget.tsx
"use client";

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { Button } from '@/components/ui/button';
import { Bot } from 'lucide-react';

// Dynamically import the chat interface to avoid SSR issues
const ChatInterface = dynamic(() => import('./ChatInterface'), {
  ssr: false,
  loading: () => <div className="bg-gray-100 rounded-lg p-4">Loading chat...</div>
});

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isInitializing, setIsInitializing] = useState(false);

  const toggleChat = async () => {
    if (!isOpen) {
      setIsInitializing(true);
      // Simulate initialization delay
      await new Promise(resolve => setTimeout(resolve, 300));
      setIsInitializing(false);
    }
    setIsOpen(!isOpen);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="w-full max-w-md h-[600px] bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden flex flex-col">
          <ChatInterface onClose={() => setIsOpen(false)} />
        </div>
      ) : (
        <Button
          onClick={toggleChat}
          disabled={isInitializing}
          className="rounded-full w-14 h-14 p-0 shadow-lg hover:shadow-xl transition-shadow"
          aria-label="Open AI Assistant"
        >
          {isInitializing ? (
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
          ) : (
            <Bot className="h-6 w-6" />
          )}
        </Button>
      )}
    </div>
  );
};

export default ChatWidget;