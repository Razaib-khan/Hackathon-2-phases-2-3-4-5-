"""
Security middleware for the AIDO Todo application
"""

import time
import re
from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

from .config import SECURITY_HEADERS, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW, SAFE_QUERY_PATTERNS


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Add security headers
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware
    NOTE: For production, consider using Redis-backed rate limiting
    """

    def __init__(self, app: ASGIApp, requests: int = RATE_LIMIT_REQUESTS, window: int = RATE_LIMIT_WINDOW):
        super().__init__(app)
        self.requests = requests
        self.window = window
        self.storage = {}  # In-memory storage for rate limiting

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = self.get_client_ip(request)
        current_time = time.time()

        # Clean old entries
        self.clean_old_requests(current_time)

        # Check if client exists in storage
        if client_ip not in self.storage:
            self.storage[client_ip] = []

        # Add current request
        self.storage[client_ip].append(current_time)

        # Check rate limit
        requests_in_window = [req_time for req_time in self.storage[client_ip]
                             if current_time - req_time <= self.window]

        if len(requests_in_window) > self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )

        response = await call_next(request)
        return response

    def get_client_ip(self, request: Request) -> str:
        # Try to get real IP from headers first
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()

        # Fallback to client host
        return request.client.host

    def clean_old_requests(self, current_time: float):
        # Remove requests older than the window period
        for client_ip in list(self.storage.keys()):
            self.storage[client_ip] = [
                req_time for req_time in self.storage[client_ip]
                if current_time - req_time <= self.window
            ]


class InputValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate input for common security issues
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # For POST/PUT/PATCH requests, validate body content
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                if body_bytes:
                    body_str = body_bytes.decode('utf-8')

                    # Check for potential SQL injection patterns
                    if self.contains_sql_injection(body_str):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid input: Potential SQL injection detected"
                        )

                    # Check for potential XSS patterns
                    if self.contains_xss_patterns(body_str):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid input: Potential XSS detected"
                        )
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid input: Unable to decode request body"
                )
            except Exception:
                # If we can't read the body, continue anyway
                pass

        response = await call_next(request)
        return response

    def contains_sql_injection(self, input_str: str) -> bool:
        """
        Check if input contains common SQL injection patterns
        """
        sql_patterns = [
            r"(?i)(union\s+select)",
            r"(?i)(drop\s+\w+)",
            r"(?i)(delete\s+from)",
            r"(?i)(insert\s+into)",
            r"(?i)(update\s+\w+\s+set)",
            r"(?i)(exec\s*\()",
            r"(?i)(execute\s*\()",
            r"(?i)(sp_\w+)",
            r";\s*(drop|delete|insert|update|create|alter|exec)",
        ]

        for pattern in sql_patterns:
            if re.search(pattern, input_str):
                return True
        return False

    def contains_xss_patterns(self, input_str: str) -> bool:
        """
        Check if input contains common XSS patterns
        """
        xss_patterns = [
            r"(?i)<script[^>]*>",
            r"(?i)</script>",
            r"(?i)<iframe[^>]*>",
            r"(?i)</iframe>",
            r"(?i)<img[^>]*src[=\s]*['\"]javascript:",
            r"(?i)on\w+\s*=[\s\S]*?['\"][^>]*>",
            r"(?i)javascript:",
            r"(?i)vbscript:",
            r"(?i)expression\(",
        ]

        for pattern in xss_patterns:
            if re.search(pattern, input_str):
                return True
        return False


class SecurityLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log security-related events
    """

    def __init__(self, app: ASGIApp, logger: Optional[logging.Logger] = None):
        super().__init__(app)
        self.logger = logger or logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        try:
            response = await call_next(request)

            # Log successful requests
            if response.status_code >= 400:
                self.logger.warning(
                    f"Security event: Status {response.status_code} for {request.method} {request.url}",
                    extra={
                        "method": request.method,
                        "url": str(request.url),
                        "status_code": response.status_code,
                        "client_ip": self.get_client_ip(request),
                        "user_agent": request.headers.get("user-agent", "")
                    }
                )

            return response
        except HTTPException as e:
            # Log HTTP exceptions
            self.logger.warning(
                f"Security event: HTTP {e.status_code} - {e.detail} for {request.method} {request.url}",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": e.status_code,
                    "detail": e.detail,
                    "client_ip": self.get_client_ip(request),
                    "user_agent": request.headers.get("user-agent", "")
                }
            )
            raise
        except Exception as e:
            # Log other exceptions
            self.logger.error(
                f"Security event: Unhandled exception for {request.method} {request.url}",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "exception": str(e),
                    "client_ip": self.get_client_ip(request),
                    "user_agent": request.headers.get("user-agent", "")
                },
                exc_info=True
            )
            raise
        finally:
            process_time = time.time() - start_time
            if process_time > 1.0:  # Log slow requests (potential DoS)
                self.logger.info(
                    f"Slow request: {process_time:.2f}s for {request.method} {request.url}",
                    extra={
                        "method": request.method,
                        "url": str(request.url),
                        "process_time": process_time,
                        "client_ip": self.get_client_ip(request)
                    }
                )

    def get_client_ip(self, request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()

        return request.client.host