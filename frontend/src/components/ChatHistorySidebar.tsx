// components/ChatHistorySidebar.tsx
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { MessageSquare, Plus, Trash2 } from 'lucide-react';

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
  onDeleteSession?: (sessionId: string) => void; // Optional callback for deleting sessions
}

const ChatHistorySidebar = ({
  sessions,
  currentSessionId,
  onSelectSession,
  onCreateNewSession,
  onDeleteSession
}: ChatHistorySidebarProps) => {
  const [hoveredSessionId, setHoveredSessionId] = useState<string | null>(null);

  const handleDeleteClick = (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent triggering session selection
    if (onDeleteSession) {
      onDeleteSession(sessionId);
    }
  };

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
            <div
              key={session.id}
              className="relative group"
              onMouseEnter={() => setHoveredSessionId(session.id)}
              onMouseLeave={() => setHoveredSessionId(null)}
            >
              <Button
                variant={currentSessionId === session.id ? 'secondary' : 'ghost'}
                className="w-full justify-start text-left h-auto py-3 px-3 pr-10" // Add padding on right for delete button
                onClick={() => onSelectSession(session.id)}
              >
                <div className="truncate text-sm">{session.title}</div>
                <div className="text-xs text-gray-500 mt-1">
                  {session.updatedAt.toLocaleDateString()}
                </div>
              </Button>

              {/* Delete button that appears on hover */}
              {(hoveredSessionId === session.id || currentSessionId === session.id) && onDeleteSession && (
                <button
                  onClick={(e) => handleDeleteClick(session.id, e)}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 rounded-md hover:bg-red-100 text-red-500 hover:text-red-700 transition-colors opacity-0 group-hover:opacity-100"
                  aria-label={`Delete ${session.title}`}
                >
                  <Trash2 size={14} />
                </button>
              )}
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
};

export default ChatHistorySidebar;