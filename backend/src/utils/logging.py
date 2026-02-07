"""
Enhanced logging configuration for the AIDO TODO Application
Provides structured logging and monitoring capabilities
"""

import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from pythonjsonlogger import jsonlogger

from config.kafka_config import kafka_config
from models.events import EventFactory, EventTypeEnum

# Import Dapr and Kafka producers if available
try:
    from .services.kafka_producer import KafkaProducerService, get_kafka_producer
    HAS_KAFKA_LOGGING = True
except ImportError:
    HAS_KAFKA_LOGGING = False

try:
    from dapr.clients import DaprClient
    HAS_DAPR_LOGGING = True
except ImportError:
    HAS_DAPR_LOGGING = False


class StructuredLogger(logging.Logger):
    """
    Custom logger that supports structured logging with additional context
    """

    def __init__(self, name: str, level: int = logging.INFO):
        super().__init__(name, level)

        # Create handler
        handler = logging.StreamHandler(sys.stdout)

        # Create formatter
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s %(module)s %(funcName)s %(lineno)d',
            rename_fields={'asctime': '@timestamp', 'name': '@logger', 'levelname': '@level'}
        )

        handler.setFormatter(formatter)
        self.addHandler(handler)

    def log_with_context(self, level: int, msg: str, context: Dict[str, Any] = None, **kwargs):
        """
        Log a message with additional context
        """
        if context is None:
            context = {}

        # Merge context with kwargs
        log_data = {**context, **kwargs}
        self.log(level, f"{msg} - {log_data}")

    def log_api_call(self, method: str, endpoint: str, user_id: str = None,
                    duration: float = None, status_code: int = None, **kwargs):
        """
        Log an API call with structured data
        """
        context = {
            "type": "api_call",
            "method": method,
            "endpoint": endpoint,
            "user_id": user_id,
            "duration_ms": duration,
            "status_code": status_code
        }
        context.update(kwargs)

        self.info("API call", extra=context)

    def log_task_operation(self, operation: str, user_id: str, task_id: str = None,
                          priority: str = None, status: bool = None, **kwargs):
        """
        Log a task operation with structured data
        """
        context = {
            "type": "task_operation",
            "operation": operation,
            "user_id": user_id,
            "task_id": task_id,
            "priority": priority,
            "status": status
        }
        context.update(kwargs)

        self.info("Task operation", extra=context)

    def log_system_metric(self, metric_name: str, value: Any, unit: str = None, **kwargs):
        """
        Log a system metric
        """
        context = {
            "type": "metric",
            "metric_name": metric_name,
            "value": value,
            "unit": unit
        }
        context.update(kwargs)

        self.info("System metric", extra=context)


def setup_logging():
    """
    Set up the logging configuration for the application
    """
    # Set the custom logger class
    logging.setLoggerClass(StructuredLogger)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove default handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add structured handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s %(module)s %(funcName)s %(lineno)d',
        rename_fields={'asctime': '@timestamp', 'name': '@logger', 'levelname': '@level'}
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Set specific loggers to appropriate levels
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> StructuredLogger:
    """
    Get a structured logger instance
    """
    return logging.getLogger(name)


def log_to_external_system(log_data: Dict[str, Any]):
    """
    Log data to external systems like Kafka or Dapr pub/sub
    """
    # Try to send to Kafka if available
    if HAS_KAFKA_LOGGING:
        try:
            from .models.events import EventFactory, EventTypeEnum
            event = EventFactory.create_event(
                event_type=EventTypeEnum.TASK_CREATED,  # Using a generic event type for logs
                user_id=log_data.get('user_id', 'system'),
                data=log_data
            )

            producer = get_kafka_producer()
            producer.publish_generic_task_event(event, log_data.get('user_id', 'system'))
        except Exception as e:
            # If Kafka logging fails, log the error but don't fail the main operation
            logging.error(f"Failed to log to Kafka: {str(e)}", exc_info=True)

    # Try to send to Dapr if available
    if HAS_DAPR_LOGGING:
        try:
            with DaprClient() as dapr_client:
                # Publish log event to Dapr pub/sub
                dapr_client.publish_event(
                    pubsub_name="kafka-pubsub",
                    topic_name="logs",
                    data=log_data,
                    metadata={"contentType": "application/json"}
                )
        except Exception as e:
            # If Dapr logging fails, log the error but don't fail the main operation
            logging.error(f"Failed to log to Dapr: {str(e)}", exc_info=True)


# Initialize logging
setup_logging()

# Global logger instance
logger = get_logger(__name__)