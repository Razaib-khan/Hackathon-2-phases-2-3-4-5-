"""
Security middleware for the Speckit Plus Todo Application
"""
from typing import Callable
from fastapi import Request, Response, HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


def add_security_headers(response: Response) -> Response:
    """
    Add security headers to response
    """
    # Prevent MIME-type sniffing
    response.headers.setdefault("X-Content-Type-Options", "nosniff")

    # Prevent clickjacking
    response.headers.setdefault("X-Frame-Options", "DENY")

    # Enable XSS protection
    response.headers.setdefault("X-XSS-Protection", "1; mode=block")

    # Strict transport security
    response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")

    # Content security policy
    response.headers.setdefault("Content-Security-Policy", "default-src 'self'; script-src 'self'")

    return response


def sanitize_input(input_str: str) -> str:
    """
    Basic input sanitization
    """
    if input_str is None:
        return input_str

    # Remove null bytes
    sanitized = input_str.replace('\x00', '')

    # Remove control characters (except common whitespace)
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\t\n\r')

    return sanitized


def register_security_middleware(app):
    """
    Register security middleware with the application
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.middleware("http")
    async def security_middleware(request: Request, call_next: Callable):
        # Add security headers to response
        response = await call_next(request)
        response = add_security_headers(response)
        return response