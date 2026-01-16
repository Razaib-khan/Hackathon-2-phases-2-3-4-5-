# Speckit Plus Todo Application - Security Features

This document outlines the security measures implemented in the Speckit Plus Todo Application.

## Security Measures Implemented

### 1. Authentication & Authorization
- JWT-based authentication with configurable expiration
- Secure password hashing using bcrypt
- Role-based access control for user data isolation

### 2. Input Validation & Sanitization
- Pydantic validators for all user inputs
- HTML/JS injection prevention
- Email format validation
- Length and content restrictions

### 3. Rate Limiting
- Per-endpoint rate limiting to prevent abuse
- Configurable limits for different API endpoints
- Protection against brute force attacks

### 4. Security Headers
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security
- Content-Security-Policy

### 5. Error Handling
- Generic error messages to prevent information disclosure
- Proper exception handling without exposing internal details

## Security Configuration

The application uses the following environment variables for security configuration:

- `JWT_SECRET_KEY`: Secret key for JWT tokens (required for production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT expiration time (default: 30)
- `RATE_LIMIT_DEFAULT`: Default rate limit (default: 100/minute)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins (default: *)
- `MIN_PASSWORD_LENGTH`: Minimum password length (default: 8)

## Production Deployment Notes

1. Set a strong `JWT_SECRET_KEY` environment variable
2. Configure specific `ALLOWED_ORIGINS` instead of wildcard (*)
3. Adjust rate limits based on expected usage patterns
4. Enable HTTPS in production environments
5. Regularly rotate security keys

## Testing Security Features

Run the security-focused tests with:
```bash
pytest tests/test_security.py
```