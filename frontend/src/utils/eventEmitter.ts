// Simple event emitter for triggering task refreshes across components
class EventEmitter {
  private events: { [key: string]: Array<(data?: any) => void> } = {};

  on(event: string, callback: (data?: any) => void) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
  }

  off(event: string, callback: (data?: any) => void) {
    if (this.events[event]) {
      this.events[event] = this.events[event].filter(cb => cb !== callback);
    }
  }

  emit(event: string, data?: any) {
    if (this.events[event]) {
      this.events[event].forEach(callback => callback(data));
    }
  }
}

export const eventEmitter = new EventEmitter();

// Specific event for task refresh
export const TASK_REFRESH_EVENT = 'task-refresh';

// Function to trigger task refresh
export const triggerTaskRefresh = () => {
  eventEmitter.emit(TASK_REFRESH_EVENT);
};