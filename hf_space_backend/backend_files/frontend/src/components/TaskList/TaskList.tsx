import React from 'react';
import TaskItem from '../TaskItem/TaskItem';
import { Task } from '../../types/task';

interface TaskListProps {
  tasks: Task[];
  onUpdateTask: (task: Task) => void;
  onDeleteTask: (id: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onUpdateTask, onDeleteTask }) => {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500 text-lg">No tasks found. Add a new task to get started!</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <ul
        className="
          grid
          grid-cols-1
          sm:grid-cols-1
          md:grid-cols-2
          lg:grid-cols-3
          gap-4
          w-full
        "
        role="list"
      >
        {tasks.map((task) => (
          <li
            key={task.id}
            className="
              transition-all
              duration-200
              ease-in-out
              hover:scale-[1.02]
            "
          >
            <TaskItem
              task={task}
              onUpdate={onUpdateTask}
              onDelete={onDeleteTask}
            />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;