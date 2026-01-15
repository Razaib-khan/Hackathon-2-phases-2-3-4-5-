import React from 'react';
import { StoryFn, Meta } from '@storybook/react';
import TaskItem, { Task } from '../TaskItem';

export default {
  title: 'Components/TaskItem',
  component: TaskItem,
  argTypes: {
    task: {
      control: { type: 'object' },
    },
    priority: {
      control: { type: 'radio', options: ['Low', 'Medium', 'High', 'Critical'] },
    },
    status: {
      control: { type: 'radio', options: ['todo', 'in-progress', 'done'] },
    },
  },
} as Meta<typeof TaskItem>;

const Template: StoryFn<typeof TaskItem> = (args) => <TaskItem {...args} />;

export const Default = Template.bind({});
Default.args = {
  task: {
    id: '1',
    title: 'Sample Task',
    description: 'This is a sample task description.',
    priority: 'Medium',
    status: 'todo',
    timestamp: new Date(),
  },
  onUpdateTask: (task: Task) => alert(`Update task: ${task.title}`),
  onDeleteTask: (id: string) => alert(`Delete task with id: ${id}`),
};

export const HighPriority = Template.bind({});
HighPriority.args = {
  ...Default.args,
  task: {
    ...Default.args?.task,
    priority: 'High',
    title: 'High Priority Task',
    description: 'This task has high priority and requires immediate attention.',
  },
};

export const InProgress = Template.bind({});
InProgress.args = {
  ...Default.args,
  task: {
    ...Default.args?.task,
    status: 'in-progress',
    title: 'In Progress Task',
    description: 'This task is currently being worked on.',
  },
};

export const Completed = Template.bind({});
Completed.args = {
  ...Default.args,
  task: {
    ...Default.args?.task,
    status: 'done',
    title: 'Completed Task',
    description: 'This task has been completed successfully.',
  },
};

export const LowPriority = Template.bind({});
LowPriority.args = {
  ...Default.args,
  task: {
    ...Default.args?.task,
    priority: 'Low',
    status: 'todo',
    title: 'Low Priority Task',
    description: 'This task has low priority and can be done later.',
  },
};