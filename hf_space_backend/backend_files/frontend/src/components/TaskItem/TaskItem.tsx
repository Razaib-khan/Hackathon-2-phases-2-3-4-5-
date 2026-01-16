import React from 'react';
import { Task } from '../../types/task';

interface TaskItemProps {
  task: Task;
  onUpdate: (task: Task) => void;
  onDelete: (id: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onUpdate, onDelete }) => {
  const handleToggleComplete = () => {
    onUpdate({
      ...task,
      completed: !task.completed,
      updatedAt: new Date(),
    });
  };

  const handleDelete = () => {
    onDelete(task.id);
  };

  return (
    <div
      className={`
        bg-white
        border
        rounded-lg
        shadow-sm
        p-4
        flex
        flex-col
        h-full
        ${task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'}
      `}
    >
      <div className="flex items-start mb-2">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          className="
            h-5
            w-5
            text-blue-600
            rounded
            border-gray-300
            focus:ring-blue-500
            cursor-pointer
            mt-0.5
          "
          aria-label={task.completed ? 'Mark task as incomplete' : 'Mark task as complete'}
        />
        <div className="ml-3 flex-1 min-w-0">
          <h3
            className={`
              text-lg
              font-medium
              truncate
              ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}
            `}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`
                text-sm
                mt-1
                ${task.completed ? 'text-gray-400' : 'text-gray-500'}
              `}
            >
              {task.description}
            </p>
          )}
        </div>
      </div>

      <div className="mt-auto pt-3 flex justify-between items-center">
        <span className={`text-xs px-2 py-1 rounded-full ${task.completed ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
          {task.completed ? 'Completed' : 'Pending'}
        </span>

        <button
          onClick={handleDelete}
          className="
            inline-flex
            items-center
            px-3
            py-1
            border
            border-transparent
            text-sm
            font-medium
            rounded-md
            text-white
            bg-red-600
            hover:bg-red-700
            focus:outline-none
            focus:ring-2
            focus:ring-offset-2
            focus:ring-red-500
          "
          aria-label={`Delete task: ${task.title}`}
        >
          Delete
        </button>
      </div>

      <div className="mt-2 text-xs text-gray-400">
        Created: {task.createdAt.toLocaleDateString()}
      </div>
    </div>
  );
};

export default TaskItem;