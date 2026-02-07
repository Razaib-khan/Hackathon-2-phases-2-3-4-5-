"""
Kafka Consumer Service for the Speckit Plus Todo Application
Handles consuming events from Kafka topics
"""

import json
import asyncio
import logging
from typing import Callable, Dict, Any, Optional
from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from kafka.errors import KafkaError
import threading
import time

from models.events import BaseEvent, EventTypeEnum, TASK_EVENTS_TOPIC, REMINDERS_TOPIC, TASK_UPDATES_TOPIC
from config.kafka_config import kafka_config


class KafkaConsumerService:
    """
    Service class for consuming events from Kafka topics
    """

    def __init__(self):
        self.consumer = None
        self.running = False
        self.logger = logging.getLogger(__name__)
        self.event_handlers: Dict[EventTypeEnum, Callable] = {}
        self._initialize_consumer()

    def _initialize_consumer(self):
        """
        Initialize the Kafka consumer with configuration
        """
        try:
            consumer_config = kafka_config.get_consumer_config()

            # Create Kafka consumer
            self.consumer = KafkaConsumer(
                **consumer_config,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else None,
                key_deserializer=lambda k: k.decode('utf-8') if k else None
            )

            self.logger.info("Kafka consumer initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Kafka consumer: {str(e)}")
            raise

    def register_event_handler(self, event_type: EventTypeEnum, handler: Callable):
        """
        Register a handler function for a specific event type
        """
        self.event_handlers[event_type] = handler
        self.logger.info(f"Registered handler for event type: {event_type}")

    def _deserialize_event(self, message_value: Dict[str, Any]) -> Optional[BaseEvent]:
        """
        Deserialize a message from Kafka into an event object
        """
        try:
            # Import dynamically to avoid circular imports
            from models.events import EventFactory

            event_type = EventTypeEnum(message_value.get("event_type"))
            user_id = message_value.get("user_id")
            data = message_value.get("data", {})
            correlation_id = message_value.get("correlation_id")
            causation_id = message_value.get("causation_id")

            # Create event using factory
            event = EventFactory.create_event(
                event_type=event_type,
                user_id=user_id,
                data=data,
                correlation_id=correlation_id,
                causation_id=causation_id
            )

            return event
        except Exception as e:
            self.logger.error(f"Failed to deserialize event: {str(e)}")
            return None

    def start_consuming(self, topics: Optional[list] = None):
        """
        Start consuming messages from specified topics (or all registered topics)
        """
        if topics is None:
            topics = [TASK_EVENTS_TOPIC, REMINDERS_TOPIC, TASK_UPDATES_TOPIC]

        try:
            # Subscribe to topics
            self.consumer.subscribe(topics=topics)

            # Get assignment to confirm subscription
            assignment = self.consumer.assignment()
            self.logger.info(f"Subscribed to topics: {[tp.topic for tp in assignment]}")

            self.running = True
            self.logger.info("Started consuming messages...")

            while self.running:
                # Poll for messages with timeout
                message_batch = self.consumer.poll(timeout_ms=1000)  # 1 second timeout

                if not message_batch:
                    continue  # No messages received, continue loop

                # Process each message in the batch
                for topic_partition, messages in message_batch.items():
                    for message in messages:
                        self._process_message(topic_partition.topic, message)

        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal, stopping consumer...")
        except Exception as e:
            self.logger.error(f"Error in message consumption: {str(e)}")
        finally:
            self.stop_consuming()

    def _process_message(self, topic: str, message):
        """
        Process a single message from Kafka
        """
        try:
            # Deserialize the message value
            if message.value is None:
                self.logger.warning(f"Received message with null value from topic {topic}")
                return

            event = self._deserialize_event(message.value)

            if event is None:
                self.logger.warning(f"Failed to deserialize message from topic {topic}")
                return

            # Handle the event based on its type
            self._handle_event(event)

            self.logger.info(f"Successfully processed event: {event.event_type} from topic {topic}")

        except Exception as e:
            self.logger.error(f"Error processing message from topic {topic}: {str(e)}")

    def _handle_event(self, event: BaseEvent):
        """
        Handle an event based on its type by calling the appropriate handler
        """
        try:
            event_type = event.event_type

            if event_type in self.event_handlers:
                handler = self.event_handlers[event_type]

                # Call the handler with the event
                handler(event)
            else:
                self.logger.warning(f"No handler registered for event type: {event_type}")

        except Exception as e:
            self.logger.error(f"Error in event handler for {event.event_type}: {str(e)}")

    def stop_consuming(self):
        """
        Stop consuming messages
        """
        self.running = False
        if self.consumer:
            self.consumer.close()
            self.logger.info("Kafka consumer stopped and closed")

    def seek_to_beginning(self, topics: Optional[list] = None):
        """
        Seek to the beginning of topics to replay all messages
        """
        if topics is None:
            topics = [TASK_EVENTS_TOPIC, REMINDERS_TOPIC, TASK_UPDATES_TOPIC]

        topic_partitions = []
        for topic in topics:
            partitions = self.consumer.partitions_for_topic(topic)
            if partitions:
                for partition in partitions:
                    topic_partitions.append(TopicPartition(topic, partition))

        if topic_partitions:
            self.consumer.seek_to_beginning(*topic_partitions)
            self.logger.info(f"Seeked to beginning for topics: {topics}")

    def get_consumer_position(self, topics: Optional[list] = None) -> Dict[str, Any]:
        """
        Get current position of consumer for specified topics
        """
        if topics is None:
            topics = [TASK_EVENTS_TOPIC, REMINDERS_TOPIC, TASK_UPDATES_TOPIC]

        positions = {}
        for topic in topics:
            partitions = self.consumer.partitions_for_topic(topic)
            if partitions:
                for partition in partitions:
                    tp = TopicPartition(topic, partition)
                    position = self.consumer.position(tp)
                    highwater = self.consumer.highwater_mark(tp)

                    positions[f"{topic}-{partition}"] = {
                        "position": position,
                        "highwater": highwater,
                        "lag": highwater - position if highwater is not None and position is not None else None
                    }

        return positions


# Global consumer instance (in a real app, this would be dependency injected)
_consumer_instance = None


def get_kafka_consumer() -> KafkaConsumerService:
    """
    Get or create the global Kafka consumer instance
    """
    global _consumer_instance
    if _consumer_instance is None:
        _consumer_instance = KafkaConsumerService()
    return _consumer_instance


def start_consumer(topics: Optional[list] = None):
    """
    Start the Kafka consumer to begin processing messages
    """
    consumer = get_kafka_consumer()
    consumer.start_consuming(topics)


def stop_consumer():
    """
    Stop the Kafka consumer
    """
    consumer = get_kafka_consumer()
    consumer.stop_consuming()


def register_event_handler(event_type: EventTypeEnum, handler: Callable):
    """
    Register a handler function for a specific event type
    """
    consumer = get_kafka_consumer()
    consumer.register_event_handler(event_type, handler)


def get_consumer_position(topics: Optional[list] = None) -> Dict[str, Any]:
    """
    Get current position of consumer for specified topics
    """
    consumer = get_kafka_consumer()
    return consumer.get_consumer_position(topics)


def seek_to_beginning(topics: Optional[list] = None):
    """
    Seek to the beginning of topics to replay all messages
    """
    consumer = get_kafka_consumer()
    consumer.seek_to_beginning(topics)