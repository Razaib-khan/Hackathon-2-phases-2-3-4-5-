// components/ui/scroll-area.tsx
'use client';

import React from 'react';

interface ScrollAreaProps extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: 'vertical' | 'horizontal' | 'both';
}

const ScrollArea = React.forwardRef<HTMLDivElement, ScrollAreaProps>(
  ({ className, children, orientation = 'vertical', ...props }, ref) => {
    const baseClasses = 'relative overflow-hidden';

    // Determine scrollbar classes based on orientation
    let scrollbarClasses = '';
    if (orientation === 'vertical') {
      scrollbarClasses = 'overflow-y-auto';
    } else if (orientation === 'horizontal') {
      scrollbarClasses = 'overflow-x-auto';
    } else {
      scrollbarClasses = 'overflow-auto';
    }

    const classes = `${baseClasses} ${scrollbarClasses} ${className || ''}`;

    return (
      <div
        className={classes}
        ref={ref}
        {...props}
      >
        <div className="[&>div]:!block">{children}</div>
      </div>
    );
  }
);

ScrollArea.displayName = 'ScrollArea';

// Create a ScrollBar component for compatibility
interface ScrollBarProps extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: 'vertical' | 'horizontal';
}

const ScrollBar = React.forwardRef<HTMLDivElement, ScrollBarProps>(
  ({ orientation = 'vertical', className, ...props }, ref) => {
    const baseClasses = 'flex touch-none select-none transition-colors';
    const orientationClasses = orientation === 'vertical'
      ? 'h-full w-2.5 border-l border-l-transparent p-[1px]'
      : 'h-2.5 flex-col border-t border-t-transparent p-[1px]';

    const classes = `${baseClasses} ${orientationClasses} ${className || ''}`;

    return (
      <div
        className={classes}
        ref={ref}
        {...props}
      >
        <div className="bg-border rounded-full flex-1" />
      </div>
    );
  }
);

ScrollBar.displayName = 'ScrollBar';

export { ScrollArea, ScrollBar };