// Global task refresh manager
// Maintains a list of subscribers that should be notified when tasks need refreshing

type RefreshCallback = () => void;

class TaskRefreshManager {
  private subscribers: RefreshCallback[] = [];

  // Subscribe to refresh events
  subscribe(callback: RefreshCallback): () => void {
    this.subscribers.push(callback);

    // Return unsubscribe function
    return () => {
      this.subscribers = this.subscribers.filter(sub => sub !== callback);
    };
  }

  // Notify all subscribers to refresh
  notify(): void {
    this.subscribers.forEach(callback => {
      try {
        callback();
      } catch (error) {
        console.error('Error in task refresh callback:', error);
      }
    });
  }
}

// Create a singleton instance
export const taskRefreshManager = new TaskRefreshManager();

// Convenience function to trigger a refresh
export const triggerTaskRefresh = () => {
  taskRefreshManager.notify();
};