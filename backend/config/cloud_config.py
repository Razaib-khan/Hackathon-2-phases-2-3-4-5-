"""
Cloud configuration for the AIDO TODO Application
Contains cloud-specific settings for AKS/GKE deployment
"""

from typing import Optional
import os


class CloudConfig:
    """
    Configuration class for cloud-specific settings
    """

    # Cloud provider (aks, gke, etc.)
    CLOUD_PROVIDER: str = os.getenv("CLOUD_PROVIDER", "local")

    # AKS-specific configurations
    AKS_CLUSTER_NAME: Optional[str] = os.getenv("AKS_CLUSTER_NAME")
    AKS_RESOURCE_GROUP: Optional[str] = os.getenv("AKS_RESOURCE_GROUP")
    AKS_REGION: str = os.getenv("AKS_REGION", "westus2")

    # GKE-specific configurations
    GKE_CLUSTER_NAME: Optional[str] = os.getenv("GKE_CLUSTER_NAME")
    GKE_PROJECT_ID: Optional[str] = os.getenv("GKE_PROJECT_ID")
    GKE_REGION: str = os.getenv("GKE_REGION", "us-west1")

    # Managed database configurations
    MANAGED_DATABASE_HOST: Optional[str] = os.getenv("MANAGED_DATABASE_HOST")
    MANAGED_DATABASE_PORT: int = int(os.getenv("MANAGED_DATABASE_PORT", "5432"))
    MANAGED_DATABASE_NAME: Optional[str] = os.getenv("MANAGED_DATABASE_NAME")
    MANAGED_DATABASE_USER: Optional[str] = os.getenv("MANAGED_DATABASE_USER")

    # Cloud-specific Kafka/Event Hub configurations
    CLOUD_KAFKA_BOOTSTRAP: Optional[str] = os.getenv("CLOUD_KAFKA_BOOTSTRAP")
    CLOUD_EVENT_HUB_NAMESPACE: Optional[str] = os.getenv("CLOUD_EVENT_HUB_NAMESPACE")

    # Monitoring configurations
    CLOUD_LOG_ANALYTICS_WORKSPACE: Optional[str] = os.getenv("CLOUD_LOG_ANALYTICS_WORKSPACE")
    CLOUD_MONITORING_ENDPOINT: Optional[str] = os.getenv("CLOUD_MONITORING_ENDPOINT")

    # Security configurations
    CLOUD_IDENTITY_CLIENT_ID: Optional[str] = os.getenv("CLOUD_IDENTITY_CLIENT_ID")
    CLOUD_KEY_VAULT_URI: Optional[str] = os.getenv("CLOUD_KEY_VAULT_URI")

    @classmethod
    def is_cloud_deployment(cls) -> bool:
        """
        Check if this is a cloud deployment
        """
        return cls.CLOUD_PROVIDER.lower() in ["aks", "gke", "aws"]

    @classmethod
    def get_database_url(cls) -> str:
        """
        Get the appropriate database URL based on deployment type
        """
        if cls.is_cloud_deployment() and cls.MANAGED_DATABASE_HOST:
            return (
                f"postgresql://{cls.MANAGED_DATABASE_USER}:{os.getenv('MANAGED_DATABASE_PASSWORD')}@"
                f"{cls.MANAGED_DATABASE_HOST}:{cls.MANAGED_DATABASE_PORT}/{cls.MANAGED_DATABASE_NAME}"
            )
        else:
            # Fallback to local/standard database URL
            return os.getenv("DATABASE_URL", "")

    @classmethod
    def get_kafka_bootstrap_servers(cls) -> str:
        """
        Get the appropriate Kafka bootstrap servers based on deployment type
        """
        if cls.is_cloud_deployment() and cls.CLOUD_KAFKA_BOOTSTRAP:
            return cls.CLOUD_KAFKA_BOOTSTRAP
        elif cls.CLOUD_EVENT_HUB_NAMESPACE:
            # For Azure Event Hubs compatible Kafka endpoint
            return f"{cls.CLOUD_EVENT_HUB_NAMESPACE}.servicebus.windows.net:9093"
        else:
            # Fallback to local Kafka
            return os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


# Global configuration instance
cloud_config = CloudConfig()