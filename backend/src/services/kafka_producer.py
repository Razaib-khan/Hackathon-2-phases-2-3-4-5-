"""
Kafka Producer Service for the Speckit Plus Todo Application
Handles publishing events to Kafka topics
"""

import json
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

from models.events import BaseEvent, EventTypeEnum, TASK_EVENTS_TOPIC, REMINDERS_TOPIC, TASK_UPDATES_TOPIC
from config.kafka_config import kafka_config


class KafkaProducerService:
    """
    Service class for producing events to Kafka topics
    """

    def __init__(self):
        self.producer = None
        self.logger = logging.getLogger(__name__)
        self._initialize_producer()

    def _initialize_producer(self):
        """
        Initialize the Kafka producer with configuration
        """
        try:
            producer_config = kafka_config.get_producer_config()

            # Create Kafka producer
            self.producer = KafkaProducer(
                **producer_config,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )

            self.logger.info("Kafka producer initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Kafka producer: {str(e)}")
            raise

    def _serialize_event(self, event: BaseEvent) -> Dict[str, Any]:
        """
        Serialize an event to a dictionary format suitable for Kafka
        """
        return {
            "event_id": event.event_id,
            "event_type": event.event_type.value if hasattr(event.event_type, 'value') else event.event_type,
            "timestamp": event.timestamp.isoformat() if isinstance(event.timestamp, datetime) else event.timestamp,
            "correlation_id": event.correlation_id,
            "causation_id": event.causation_id,
            "user_id": event.user_id,
            "data": event.data
        }

    def _send_event(self, topic: str, event: BaseEvent, key: Optional[str] = None) -> bool:
        """
        Send an event to the specified Kafka topic
        """
        try:
            serialized_event = self._serialize_event(event)

            future = self.producer.send(
                topic=topic,
                value=serialized_event,
                key=key
            )

            # Wait for the message to be sent (with timeout)
            record_metadata = future.get(timeout=10)

            self.logger.info(f"Event sent to topic {topic}, partition {record_metadata.partition}, "
                            f"offset {record_metadata.offset}")

            return True

        except KafkaError as e:
            self.logger.error(f"Kafka error sending event to topic {topic}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending event to topic {topic}: {str(e)}")
            return False

    def publish_task_created(self, event: BaseEvent, user_id: str) -> bool:
        """
        Publish a task created event to the task events topic
        """
        return self._send_event(TASK_EVENTS_TOPIC, event, key=user_id)

    def publish_task_updated(self, event: BaseEvent, user_id: str) -> bool:
        """
        Publish a task updated event to the task events topic
        """
        return self._send_event(TASK_EVENTS_TOPIC, event, key=user_id)

    def publish_task_completed(self, event: BaseEvent, user_id: str) -> bool:
        """
        Publish a task completed event to the task events topic
        """
        return self._send_event(TASK_EVENTS_TOPIC, event, key=user_id)

    def publish_task_deleted(self, event: BaseEvent, user_id: str) -> bool:
        """
        Publish a task deleted event to the task events topic
        """
        return self._send_event(TASK_EVENTS_TOPIC, event, key=user_id)

    def publish_reminder_triggered(self, event: BaseEvent, user_id: str) -> bool:
        """
        Publish a reminder triggered event to the reminders topic
        """
        return self._send_event(REMINDERS_TOPIC, event, key=user_id)

    def publish_recurring_task_generated(self, event: BaseEvent, user_id: str) -> bool:
        """
        Publish a recurring task generated event to the task updates topic
        """
        return self._send_event(TASK_UPDATES_TOPIC, event, key=user_id)

    def publish_generic_task_event(self, event: BaseEvent, user_id: str) -> bool:
        """
        Publish a generic task event to the appropriate topic based on event type
        """
        if event.event_type == EventTypeEnum.REMINDER_TRIGGERED:
            return self.publish_reminder_triggered(event, user_id)
        elif event.event_type == EventTypeEnum.RECURRING_TASK_GENERATED:
            return self.publish_recurring_task_generated(event, user_id)
        else:
            # Default to task-events topic for other task events
            return self._send_event(TASK_EVENTS_TOPIC, event, key=user_id)

    def flush(self):
        """
        Flush all pending messages to Kafka
        """
        if self.producer:
            self.producer.flush()
            self.logger.info("Kafka producer flushed all pending messages")

    def close(self):
        """
        Close the Kafka producer connection
        """
        if self.producer:
            self.producer.close()
            self.logger.info("Kafka producer closed successfully")


# Global producer instance (in a real app, this would be dependency injected)
_producer_instance = None


def get_kafka_producer() -> KafkaProducerService:
    """
    Get or create the global Kafka producer instance
    """
    global _producer_instance
    if _producer_instance is None:
        _producer_instance = KafkaProducerService()
    return _producer_instance


def publish_event(event: BaseEvent, user_id: str) -> bool:
    """
    Convenience function to publish an event using the global producer
    """
    producer = get_kafka_producer()
    return producer.publish_generic_task_event(event, user_id)


def publish_task_created_event(event: BaseEvent, user_id: str) -> bool:
    """
    Convenience function to publish a task created event
    """
    producer = get_kafka_producer()
    return producer.publish_task_created(event, user_id)


def publish_task_updated_event(event: BaseEvent, user_id: str) -> bool:
    """
    Convenience function to publish a task updated event
    """
    producer = get_kafka_producer()
    return producer.publish_task_updated(event, user_id)


def publish_task_completed_event(event: BaseEvent, user_id: str) -> bool:
    """
    Convenience function to publish a task completed event
    """
    producer = get_kafka_producer()
    return producer.publish_task_completed(event, user_id)


def publish_task_deleted_event(event: BaseEvent, user_id: str) -> bool:
    """
    Convenience function to publish a task deleted event
    """
    producer = get_kafka_producer()
    return producer.publish_task_deleted(event, user_id)


def publish_reminder_triggered_event(event: BaseEvent, user_id: str) -> bool:
    """
    Convenience function to publish a reminder triggered event
    """
    producer = get_kafka_producer()
    return producer.publish_reminder_triggered(event, user_id)


def publish_recurring_task_generated_event(event: BaseEvent, user_id: str) -> bool:
    """
    Convenience function to publish a recurring task generated event
    """
    producer = get_kafka_producer()
    return producer.publish_recurring_task_generated(event, user_id)