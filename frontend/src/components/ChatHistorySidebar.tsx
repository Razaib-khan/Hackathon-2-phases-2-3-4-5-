// components/ChatHistorySidebar.tsx
import React from 'react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { MessageSquare, Plus } from 'lucide-react';

interface ChatSession {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}

interface ChatHistorySidebarProps {
  sessions: ChatSession[];
  currentSessionId: string | null;
  onSelectSession: (sessionId: string) => void;
  onCreateNewSession: () => void;
}

const ChatHistorySidebar = ({
  sessions,
  currentSessionId,
  onSelectSession,
  onCreateNewSession
}: ChatHistorySidebarProps) => {
  return (
    <div className="w-64 bg-gray-50 border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold flex items-center">
            <MessageSquare className="h-5 w-5 mr-2" />
            Chat History
          </h2>
          <Button size="sm" onClick={onCreateNewSession}>
            <Plus className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 p-2">
        <div className="space-y-1">
          {sessions.map((session) => (
            <Button
              key={session.id}
              variant={currentSessionId === session.id ? 'secondary' : 'ghost'}
              className="w-full justify-start text-left h-auto py-3 px-3"
              onClick={() => onSelectSession(session.id)}
            >
              <div className="truncate text-sm">{session.title}</div>
              <div className="text-xs text-gray-500 mt-1">
                {session.updatedAt.toLocaleDateString()}
              </div>
            </Button>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
};

export default ChatHistorySidebar;