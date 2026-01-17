"""
Security configuration for the Speckit Plus Todo Application
"""
import os
from typing import List, Optional


class SecurityConfig:
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = os.getenv("RATE_LIMIT_DEFAULT", "100/minute")
    RATE_LIMIT_AUTH: str = os.getenv("RATE_LIMIT_AUTH", "10/minute")
    RATE_LIMIT_TASKS: str = os.getenv("RATE_LIMIT_TASKS", "50/minute")

    # Security Headers
    ENABLE_SECURITY_HEADERS: bool = os.getenv("ENABLE_SECURITY_HEADERS", "True").lower() == "true"

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Password requirements
    MIN_PASSWORD_LENGTH: int = int(os.getenv("MIN_PASSWORD_LENGTH", "8"))

    @classmethod
    def validate_config(cls):
        """Validate security configuration"""
        if not cls.JWT_SECRET_KEY:
            import warnings
            cls.JWT_SECRET_KEY = "speckit_plus_todo_secret_key_change_in_production"
            warnings.warn(
                "Using default JWT secret key. This is insecure for production. "
                "Please set JWT_SECRET_KEY environment variable.",
                UserWarning
            )

        if "*" in cls.ALLOWED_ORIGINS:
            import warnings
            warnings.warn(
                "Wildcard CORS origin (*) is set. This is insecure for production. "
                "Please specify allowed origins in ALLOWED_ORIGINS environment variable.",
                UserWarning
            )