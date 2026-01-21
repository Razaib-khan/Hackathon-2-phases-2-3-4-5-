"""
Security configuration for the AIDO Todo application
"""

from typing import List
import os
from datetime import timedelta
from fastapi.security import HTTPBearer
from passlib.context import CryptContext


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Security headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}

# Rate limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # seconds

# CORS settings
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost,http://localhost:3000").split(",")

# Input validation settings
MAX_TASK_TITLE_LENGTH = 200
MAX_TASK_DESCRIPTION_LENGTH = 1000
MAX_CHAT_MESSAGE_LENGTH = 5000
MAX_BATCH_OPERATIONS = 100  # Maximum number of operations in a batch request

# Allowed priority levels
ALLOWED_PRIORITIES = {"Low", "Medium", "High", "Critical"}

# Security middleware configuration
SECURITY_MIDDLEWARE_CONFIG = {
    "allowed_hosts": ["localhost", "127.0.0.1", os.getenv("DOMAIN_NAME", "")],
    "hsts_max_age": 31536000,
    "hsts_include_subdomains": True,
    "hsts_preload": True,
}

# API key validation for external services
EXTERNAL_SERVICES = {
    "openrouter": {
        "required_headers": ["Authorization"],
        "rate_limits": {"requests": 1000, "window": 60},  # Per minute
    }
}

# File upload security (if needed in the future)
UPLOAD_ALLOWED_EXTENSIONS = {".txt", ".pdf", ".doc", ".docx"}
UPLOAD_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# SQL injection prevention is handled by SQLModel's parameterized queries
# but we define safe query patterns here for reference
SAFE_QUERY_PATTERNS = [
    r"^[a-zA-Z0-9\s\-\_\.]+$",  # Safe alphanumeric and limited special chars
]

# Authentication schemes
bearer_scheme = HTTPBearer()

# Session security
SESSION_COOKIE_NAME = "aido_session"
SESSION_COOKIE_SECURE = os.getenv("ENVIRONMENT", "development") == "production"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "lax"
SESSION_EXPIRE_TIME = timedelta(hours=24)

# Password validation rules
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGITS = True
PASSWORD_REQUIRE_SPECIAL_CHARS = True

# Logging configuration for security events
SECURITY_LOG_LEVEL = os.getenv("SECURITY_LOG_LEVEL", "INFO")
SECURITY_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Feature flags for security-sensitive features
SECURITY_FEATURE_FLAGS = {
    "require_mfa": os.getenv("REQUIRE_MFA", "false").lower() == "true",
    "enable_rate_limiting": os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true",
    "enable_audit_logging": os.getenv("ENABLE_AUDIT_LOGGING", "true").lower() == "true",
    "enable_ip_blocking": os.getenv("ENABLE_IP_BLOCKING", "false").lower() == "true",
}

# API security settings
API_SECURITY_SETTINGS = {
    "enforce_https": os.getenv("ENVIRONMENT", "development") == "production",
    "require_auth_for_all_endpoints": True,
    "allowed_content_types": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "blocked_content_types": [
        "text/html",
        "text/javascript"
    ]
}