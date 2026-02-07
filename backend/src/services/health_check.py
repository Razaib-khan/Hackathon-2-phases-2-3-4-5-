"""
Health check service for the AIDO TODO Application
Provides health check endpoints and monitoring capabilities
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from sqlmodel import Session, select
from models.task import Task
from models.user import User
from database.database import engine

# Import Dapr and Kafka clients if available
try:
    from dapr.clients import DaprClient
    HAS_DAPR = True
except ImportError:
    HAS_DAPR = False

try:
    from kafka import KafkaAdminClient
    from config.kafka_config import kafka_config
    HAS_KAFKA = True
except ImportError:
    HAS_KAFKA = False

logger = logging.getLogger(__name__)


class HealthCheckService:
    """
    Service class for performing health checks on various components
    """

    @staticmethod
    def check_database_health() -> Dict[str, Any]:
        """
        Check the health of the database connection
        """
        try:
            with Session(engine) as session:
                # Perform a simple query to test the connection
                stmt = select(Task).limit(1)
                session.exec(stmt)

            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "component": "database",
                "details": "Database connection is healthy"
            }
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "component": "database",
                "error": str(e)
            }

    @staticmethod
    def check_dapr_health() -> Dict[str, Any]:
        """
        Check the health of the Dapr sidecar
        """
        if not HAS_DAPR:
            return {
                "status": "disabled",
                "timestamp": datetime.utcnow().isoformat(),
                "component": "dapr",
                "details": "Dapr integration not available"
            }

        try:
            with DaprClient() as dapr_client:
                # Try to get metadata from Dapr to check if it's responsive
                metadata = dapr_client.get_metadata()

            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "component": "dapr",
                "version": metadata.version,
                "actors": metadata.registered_components
            }
        except Exception as e:
            logger.error(f"Dapr health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "component": "dapr",
                "error": str(e)
            }

    @staticmethod
    def check_kafka_health() -> Dict[str, Any]:
        """
        Check the health of the Kafka connection
        """
        if not HAS_KAFKA:
            return {
                "status": "disabled",
                "timestamp": datetime.utcnow().isoformat(),
                "component": "kafka",
                "details": "Kafka integration not available"
            }

        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=kafka_config.kafka_bootstrap_servers.split(',')
            )

            # List topics to check if Kafka is responsive
            topics = admin_client.list_consumer_groups()

            admin_client.close()

            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "component": "kafka",
                "details": f"Connected to Kafka, {len(topics)} consumer groups found"
            }
        except Exception as e:
            logger.error(f"Kafka health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "component": "kafka",
                "error": str(e)
            }

    @staticmethod
    def get_overall_health() -> Dict[str, Any]:
        """
        Get the overall health status of the application
        """
        database_health = HealthCheckService.check_database_health()
        dapr_health = HealthCheckService.check_dapr_health()
        kafka_health = HealthCheckService.check_kafka_health()

        # Determine overall status
        statuses = [database_health["status"], dapr_health["status"], kafka_health["status"]]

        if "unhealthy" in statuses:
            overall_status = "unhealthy"
        elif "degraded" in statuses or any(s == "disabled" for s in statuses):
            overall_status = "degraded"
        else:
            overall_status = "healthy"

        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "database": database_health,
                "dapr": dapr_health,
                "kafka": kafka_health
            }
        }

    @staticmethod
    def get_metrics() -> Dict[str, Any]:
        """
        Get application metrics for monitoring
        """
        try:
            with Session(engine) as session:
                # Count total tasks
                total_tasks = session.exec(select(Task)).all()
                total_users = session.exec(select(User)).all()

                # Count by status
                completed_tasks = session.exec(
                    select(Task).where(Task.status == True)
                ).all()

                pending_tasks = session.exec(
                    select(Task).where(Task.status == False)
                ).all()

                # Count by priority
                critical_tasks = session.exec(
                    select(Task).where(Task.priority == "Critical")
                ).all()

                high_tasks = session.exec(
                    select(Task).where(Task.priority == "High")
                ).all()

                medium_tasks = session.exec(
                    select(Task).where(Task.priority == "Medium")
                ).all()

                low_tasks = session.exec(
                    select(Task).where(Task.priority == "Low")
                ).all()

            return {
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": {
                    "total_users": len(total_users),
                    "total_tasks": len(total_tasks),
                    "completed_tasks": len(completed_tasks),
                    "pending_tasks": len(pending_tasks),
                    "critical_tasks": len(critical_tasks),
                    "high_tasks": len(high_tasks),
                    "medium_tasks": len(medium_tasks),
                    "low_tasks": len(low_tasks)
                }
            }
        except Exception as e:
            logger.error(f"Metrics collection failed: {str(e)}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
                "metrics": {}
            }


# Convenience functions
def get_health_status() -> Dict[str, Any]:
    """
    Convenience function to get overall health status
    """
    return HealthCheckService.get_overall_health()


def get_application_metrics() -> Dict[str, Any]:
    """
    Convenience function to get application metrics
    """
    return HealthCheckService.get_metrics()


def is_healthy() -> bool:
    """
    Check if the application is healthy
    """
    health = HealthCheckService.get_overall_health()
    return health["status"] == "healthy"