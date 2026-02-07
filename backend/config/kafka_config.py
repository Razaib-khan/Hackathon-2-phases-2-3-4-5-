"""
Kafka configuration for the Speckit Plus Todo Application
Contains configuration settings for Kafka connection and topics
"""

from typing import Dict, List, Optional
from pydantic import BaseSettings
import os


class KafkaConfig(BaseSettings):
    """
    Kafka configuration settings
    """
    # Kafka broker configuration
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_security_protocol: str = os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
    kafka_sasl_mechanism: Optional[str] = os.getenv("KAFKA_SASL_MECHANISM", None)
    kafka_sasl_username: Optional[str] = os.getenv("KAFKA_SASL_USERNAME", None)
    kafka_sasl_password: Optional[str] = os.getenv("KAFKA_SASL_PASSWORD", None)

    # Topic definitions
    task_events_topic: str = os.getenv("KAFKA_TASK_EVENTS_TOPIC", "task-events")
    reminders_topic: str = os.getenv("KAFKA_REMINDERS_TOPIC", "reminders")
    task_updates_topic: str = os.getenv("KAFKA_TASK_UPDATES_TOPIC", "task-updates")

    # Consumer configuration
    consumer_group_id: str = os.getenv("KAFKA_CONSUMER_GROUP_ID", "todo-consumer-group")
    consumer_auto_offset_reset: str = os.getenv("KAFKA_CONSUMER_AUTO_OFFSET_RESET", "earliest")
    consumer_enable_auto_commit: bool = os.getenv("KAFKA_CONSUMER_ENABLE_AUTO_COMMIT", "true").lower() == "true"

    # Producer configuration
    producer_acknowledgments: str = os.getenv("KAFKA_PRODUCER_ACKS", "all")
    producer_retries: int = int(os.getenv("KAFKA_PRODUCER_RETRIES", "3"))
    producer_batch_size: int = int(os.getenv("KAFKA_PRODUCER_BATCH_SIZE", "16384"))
    producer_linger_ms: int = int(os.getenv("KAFKA_PRODUCER_LINGER_MS", "5"))
    producer_buffer_memory: int = int(os.getenv("KAFKA_PRODUCER_BUFFER_MEMORY", "33554432"))

    # Connection and timeout settings
    request_timeout_ms: int = int(os.getenv("KAFKA_REQUEST_TIMEOUT_MS", "30000"))
    connection_max_idle_ms: int = int(os.getenv("KAFKA_CONNECTION_MAX_IDLE_MS", "540000"))

    # SSL configuration (if needed)
    ssl_cafile: Optional[str] = os.getenv("KAFKA_SSL_CAFILE", None)
    ssl_certfile: Optional[str] = os.getenv("KAFKA_SSL_CERTFILE", None)
    ssl_keyfile: Optional[str] = os.getenv("KAFKA_SSL_KEYFILE", None)

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_kafka_config_dict(self) -> Dict[str, any]:
        """
        Get Kafka configuration as dictionary for use with kafka-python
        """
        config = {
            "bootstrap_servers": [server.strip() for server in self.kafka_bootstrap_servers.split(",")],
            "security_protocol": self.kafka_security_protocol,
        }

        # Add SASL configuration if provided
        if self.kafka_sasl_mechanism:
            config.update({
                "sasl_mechanism": self.kafka_sasl_mechanism,
                "sasl_plain_username": self.kafka_sasl_username,
                "sasl_plain_password": self.kafka_sasl_password,
            })

        # Add SSL configuration if provided
        if self.ssl_cafile:
            config["ssl_cafile"] = self.ssl_cafile
        if self.ssl_certfile:
            config["ssl_certfile"] = self.ssl_certfile
        if self.ssl_keyfile:
            config["ssl_keyfile"] = self.ssl_keyfile

        return config

    def get_consumer_config(self) -> Dict[str, any]:
        """
        Get consumer-specific configuration
        """
        config = self.get_kafka_config_dict()
        config.update({
            "group_id": self.consumer_group_id,
            "auto_offset_reset": self.consumer_auto_offset_reset,
            "enable_auto_commit": self.consumer_enable_auto_commit,
            "request_timeout_ms": self.request_timeout_ms,
            "max_poll_records": 100,  # Limit records per poll for better performance
        })
        return config

    def get_producer_config(self) -> Dict[str, any]:
        """
        Get producer-specific configuration
        """
        config = self.get_kafka_config_dict()
        config.update({
            "acks": self.producer_acknowledgments,
            "retries": self.producer_retries,
            "batch_size": self.producer_batch_size,
            "linger_ms": self.producer_linger_ms,
            "buffer_memory": self.producer_buffer_memory,
            "request_timeout_ms": self.request_timeout_ms,
            "compression_type": "snappy",  # Compress messages to save bandwidth
        })
        return config


# Global configuration instance
kafka_config = KafkaConfig()


# Topic configuration for the application
TOPIC_CONFIG = {
    kafka_config.task_events_topic: {
        "num_partitions": 3,
        "replication_factor": 1,
        "retention_ms": 604800000,  # 7 days retention
    },
    kafka_config.reminders_topic: {
        "num_partitions": 3,
        "replication_factor": 1,
        "retention_ms": 86400000,  # 1 day retention
    },
    kafka_config.task_updates_topic: {
        "num_partitions": 3,
        "replication_factor": 1,
        "retention_ms": 259200000,  # 3 days retention
    }
}


def get_topic_list() -> List[str]:
    """
    Get list of all topics used by the application
    """
    return [
        kafka_config.task_events_topic,
        kafka_config.reminders_topic,
        kafka_config.task_updates_topic
    ]