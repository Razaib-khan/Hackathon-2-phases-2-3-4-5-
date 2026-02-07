"""
Task Scheduler Service for the Speckit Plus Todo Application
Handles background scheduling for due date reminders and recurring task generation
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional
import threading
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from sqlmodel import Session, select
from models.task import Task
from models.user import User
from .task_service import generate_next_occurrence, handle_due_dates_and_reminders


class TaskSchedulerService:
    """
    Service class for handling task scheduling, reminders, and recurring task generation
    """

    def __init__(self, session: Session):
        self.session = session
        self.scheduler = AsyncIOScheduler()
        self.logger = logging.getLogger(__name__)

    def start(self):
        """
        Start the task scheduler service
        """
        if not self.scheduler.running:
            self.scheduler.start()

            # Schedule recurring tasks check every hour
            self.scheduler.add_job(
                self._check_recurring_tasks,
                CronTrigger(minute=0),  # Every hour at minute 0
                id='recurring_tasks_checker',
                name='Check for recurring tasks to generate'
            )

            # Schedule due date and reminder checks every 5 minutes
            self.scheduler.add_job(
                self._check_due_dates_and_reminders,
                CronTrigger(minute='*/5'),  # Every 5 minutes
                id='due_dates_reminders_checker',
                name='Check for due dates and reminders'
            )

            self.logger.info("Task scheduler started successfully")

    def stop(self):
        """
        Stop the task scheduler service
        """
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.logger.info("Task scheduler stopped successfully")

    async def _check_recurring_tasks(self):
        """
        Check for recurring tasks that need to generate next occurrences
        """
        try:
            self.logger.info("Checking for recurring tasks...")

            # Query for recurring tasks that need to generate next occurrence
            recurring_tasks = self.session.exec(
                select(Task).where(
                    Task.is_recurring == True,
                    Task.next_occurrence.is_not(None),
                    Task.next_occurrence <= datetime.utcnow()
                )
            ).all()

            generated_tasks = []
            for task in recurring_tasks:
                try:
                    next_task = generate_next_occurrence(self.session, task)
                    if next_task:
                        generated_tasks.append(next_task)
                        self.logger.info(f"Generated next occurrence for task {task.id}")
                except Exception as e:
                    self.logger.error(f"Failed to generate next occurrence for task {task.id}: {str(e)}")

            self.logger.info(f"Generated {len(generated_tasks)} new recurring task occurrences")

        except Exception as e:
            self.logger.error(f"Error in recurring tasks check: {str(e)}")

    async def _check_due_dates_and_reminders(self):
        """
        Check for tasks with due dates or reminders that need attention
        """
        try:
            self.logger.info("Checking for due dates and reminders...")

            # Process tasks with due dates or reminders
            tasks_needing_attention = handle_due_dates_and_reminders(self.session)

            # Here we would typically trigger notifications
            # For now, we'll just log the tasks that need attention
            for task in tasks_needing_attention:
                if task.due_date and task.due_date <= datetime.utcnow():
                    self.logger.info(f"Task {task.id} is due: {task.title}")
                if task.reminder_time and task.reminder_time <= datetime.utcnow():
                    self.logger.info(f"Reminder triggered for task {task.id}: {task.title}")

            self.logger.info(f"Processed {len(tasks_needing_attention)} tasks with due dates/reminders")

        except Exception as e:
            self.logger.error(f"Error in due dates and reminders check: {str(e)}")

    async def schedule_task_reminder(self, task_id: str, reminder_time: datetime):
        """
        Schedule a specific reminder for a task
        """
        try:
            # This would schedule a one-time job for the specific reminder
            job_id = f"reminder_{task_id}_{reminder_time.timestamp()}"

            def trigger_reminder():
                # In a real implementation, this would trigger the actual reminder notification
                self.logger.info(f"Triggering reminder for task {task_id}")

                # Get the task to confirm it exists
                task = self.session.get(Task, task_id)
                if task:
                    self.logger.info(f"Reminder triggered for task '{task.title}'")

            self.scheduler.add_job(
                trigger_reminder,
                'date',
                run_date=reminder_time,
                id=job_id,
                name=f'Reminder for task {task_id}'
            )

            self.logger.info(f"Scheduled reminder for task {task_id} at {reminder_time}")

        except Exception as e:
            self.logger.error(f"Failed to schedule reminder for task {task_id}: {str(e)}")

    async def schedule_recurring_task_generation(self, task_id: str, pattern: dict):
        """
        Schedule recurring task generation based on pattern
        """
        try:
            # In a real implementation, this would set up ongoing checks for this specific recurring task
            # For now, we rely on the general hourly check
            self.logger.info(f"Scheduled recurring generation checks for task {task_id}")

        except Exception as e:
            self.logger.error(f"Failed to schedule recurring generation for task {task_id}: {str(e)}")


# Global scheduler instance (in a real app, this would be dependency injected)
_scheduler_instance = None


def get_scheduler_instance(session: Session) -> TaskSchedulerService:
    """
    Get or create the global scheduler instance
    """
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = TaskSchedulerService(session)
    return _scheduler_instance


async def start_scheduler(session: Session):
    """
    Start the task scheduler service
    """
    scheduler = get_scheduler_instance(session)
    scheduler.start()
    return scheduler


async def stop_scheduler():
    """
    Stop the task scheduler service
    """
    global _scheduler_instance
    if _scheduler_instance:
        _scheduler_instance.stop()
        _scheduler_instance = None