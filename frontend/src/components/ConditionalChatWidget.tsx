'use client';

import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import ChatWidget from './ChatWidget';

export default function ConditionalChatWidget() {
  const pathname = usePathname();
  const [shouldShowChat, setShouldShowChat] = useState(false);

  useEffect(() => {
    // Show chat widget only on /tasks and /account routes
    if (pathname === '/tasks' || pathname === '/account') {
      setShouldShowChat(true);
    } else {
      setShouldShowChat(false);
    }
  }, [pathname]);

  if (shouldShowChat) {
    return <ChatWidget />;
  }

  return null;
}