'use client';

import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import ChatWidget from './ChatWidget';

export default function ConditionalChatWidget() {
  const pathname = usePathname();
  const [shouldShowChat, setShouldShowChat] = useState(false);

  useEffect(() => {
    // Show chat widget only on /tasks and /account routes and their subroutes
    if (pathname && (pathname.startsWith('/tasks') || pathname.startsWith('/account'))) {
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