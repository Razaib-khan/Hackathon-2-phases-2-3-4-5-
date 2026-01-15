# Error Handling Patterns for Frontend-Backend Systems

Comprehensive error handling strategies between frontend and backend systems.

## HTTP Status Code Handling

### Client-Side Status Code Mapping
Map HTTP status codes to appropriate user-facing messages:

```typescript
// Status code to user message mapping
const STATUS_CODE_MESSAGES: { [key: number]: string } = {
  400: "Invalid request. Please check your input and try again.",
  401: "Session expired. Please sign in again.",
  403: "Access denied. You don't have permission for this action.",
  404: "Resource not found. The requested item may have been removed.",
  409: "Conflict occurred. The resource already exists.",
  422: "Validation failed. Please check the form for errors.",
  429: "Too many requests. Please wait before trying again.",
  500: "Server error. We're experiencing technical difficulties.",
  502: "Connection error. Please check your internet connection.",
  503: "Service unavailable. Please try again later."
};

// Error handler with status code mapping
class ApiErrorHandler {
  static handle(error: any): ApiError {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const serverMessage = error.response.data?.detail || error.response.data?.message;

      return {
        status,
        message: STATUS_CODE_MESSAGES[status] || serverMessage || 'An unexpected error occurred',
        serverMessage,
        isClientError: status >= 400 && status < 500,
        isServerError: status >= 500
      };
    } else if (error.request) {
      // Request made but no response received
      return {
        status: 0,
        message: 'Network error. Please check your connection.',
        isClientError: false,
        isServerError: false
      };
    } else {
      // Something else happened
      return {
        status: -1,
        message: error.message || 'An unexpected error occurred',
        isClientError: false,
        isServerError: false
      };
    }
  }
}
```

### Backend Error Response Structure
Consistent error response format across all endpoints:

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import traceback
import logging

# Custom exception handlers
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format"""
    error_response = {
        "error": {
            "type": "http_error",
            "status_code": exc.status_code,
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    }

    # Log error for monitoring
    logging.error(f"HTTP {exc.status_code} error at {request.url.path}: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with consistent format"""
    error_details = []
    for error in exc.errors():
        error_details.append({
            "loc": error['loc'],
            "msg": error['msg'],
            "type": error['type']
        })

    error_response = {
        "error": {
            "type": "validation_error",
            "status_code": 422,
            "message": "Validation failed",
            "details": error_details,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    }

    logging.warning(f"Validation error at {request.url.path}: {error_details}")

    return JSONResponse(
        status_code=422,
        content=error_response
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    error_response = {
        "error": {
            "type": "internal_error",
            "status_code": 500,
            "message": "An internal server error occurred",
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    }

    # Log full traceback for debugging
    logging.error(f"Internal error at {request.url.path}: {str(exc)}")
    logging.error(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content=error_response
    )
```

## Authentication Error Handling

### Token Validation Errors
Handle JWT token validation failures gracefully:

```typescript
// Frontend token validation
class AuthTokenValidator {
  static isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp < currentTime;
    } catch (error) {
      return true; // Treat malformed tokens as expired
    }
  }

  static async validateAndRefresh(): Promise<boolean> {
    const token = localStorage.getItem('access_token');

    if (!token) {
      return false;
    }

    if (this.isTokenExpired(token)) {
      // Attempt refresh
      try {
        const refreshTokenResponse = await fetch('/api/auth/refresh', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (refreshTokenResponse.ok) {
          const { access_token } = await refreshTokenResponse.json();
          localStorage.setItem('access_token', access_token);
          return true;
        } else {
          // Refresh failed, user needs to sign in again
          this.handleTokenExpiration();
          return false;
        }
      } catch (error) {
        this.handleTokenExpiration();
        return false;
      }
    }

    return true;
  }

  static handleTokenExpiration(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
}
```

```python
# Backend token validation with proper error handling
from jose import JWTError, jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta

def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True}
        )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return {"user_id": user_id}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except Exception as e:
        logging.error(f"Token verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed"
        )
```

## Network Error Handling

### Retry Logic with Exponential Backoff
Implement intelligent retry mechanisms:

```typescript
class NetworkRetryHandler {
  static async requestWithRetry(
    requestFn: () => Promise<any>,
    maxRetries: number = 3,
    baseDelay: number = 1000
  ): Promise<any> {
    let lastError: any;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await requestFn();
      } catch (error) {
        lastError = error;

        // Don't retry on certain error types
        if (this.shouldNotRetry(error)) {
          throw error;
        }

        if (attempt < maxRetries) {
          const delay = this.calculateExponentialBackoff(baseDelay, attempt);
          await this.sleep(delay);
        }
      }
    }

    throw lastError;
  }

  private static shouldNotRetry(error: any): boolean {
    // Don't retry on 4xx errors (client errors)
    if (error.response?.status >= 400 && error.response?.status < 500) {
      return true;
    }

    // Don't retry on specific 5xx errors
    if ([501, 505].includes(error.response?.status)) {
      return true;
    }

    return false;
  }

  private static calculateExponentialBackoff(baseDelay: number, attempt: number): number {
    return baseDelay * Math.pow(2, attempt) + Math.random() * 1000;
  }

  private static sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## Database Error Handling

### Transaction and Connection Errors
Handle database-specific errors appropriately:

```python
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError
from sqlmodel import Session
import logging

def handle_database_operation(operation_fn, session: Session, max_retries: int = 3):
    """Execute database operation with error handling and retry logic"""
    for attempt in range(max_retries):
        try:
            result = operation_fn(session)
            session.commit()
            return result

        except IntegrityError as e:
            session.rollback()
            logging.error(f"Integrity error: {str(e)}")

            # Check for specific constraint violations
            if 'unique constraint' in str(e).lower():
                raise HTTPException(
                    status_code=409,
                    detail="A resource with this identifier already exists"
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Data integrity violation"
                )

        except OperationalError as e:
            session.rollback()
            logging.error(f"Operational error: {str(e)}")

            if attempt < max_retries - 1:
                # Brief delay before retry
                time.sleep(0.5 * (attempt + 1))
                continue
            else:
                raise HTTPException(
                    status_code=503,
                    detail="Database temporarily unavailable"
                )

        except DatabaseError as e:
            session.rollback()
            logging.error(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Database operation failed"
            )
```

## Frontend Error Boundary Patterns

### React Error Boundaries
Handle frontend rendering errors gracefully:

```typescript
import React from 'react';

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ApiErrorBoundary extends React.Component<
  { children: React.ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log error to monitoring service
    console.error('API Error Boundary caught error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h2>Something went wrong with the API request.</h2>
          <p>Please try refreshing the page or contact support.</p>
          <button onClick={() => window.location.reload()}>
            Refresh Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Higher-order component for API error handling
const withApiErrorHandling = (WrappedComponent: React.ComponentType) => {
  return class extends React.Component {
    state = {
      error: null,
      loading: false,
      retryCount: 0
    };

    handleError = (error: any) => {
      this.setState({ error: ApiErrorHandler.handle(error) });
    };

    handleRetry = () => {
      this.setState({ error: null, retryCount: this.state.retryCount + 1 });
    };

    render() {
      const { error } = this.state;

      if (error) {
        return (
          <div className="api-error-overlay">
            <div className="error-content">
              <h3>API Error</h3>
              <p>{error.message}</p>
              <button onClick={this.handleRetry}>Retry</button>
              <button onClick={() => window.location.href = '/'}>
                Go Home
              </button>
            </div>
          </div>
        );
      }

      return <WrappedComponent {...this.props} />;
    }
  };
};
```

## User Experience Error Handling

### Loading and Error States
Provide clear feedback for different error scenarios:

```typescript
// Loading and error state management
interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
  retry: () => void;
}

function useApiCall<T>(
  apiFunction: () => Promise<T>,
  deps: React.DependencyList = []
): ApiState<T> {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: true,
    error: null,
    retry: () => {} // Will be replaced
  });

  const fetchData = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const data = await apiFunction();
      setState({ data, loading: false, error: null, retry: fetchData });
    } catch (error) {
      const apiError = ApiErrorHandler.handle(error);
      setState({ data: null, loading: false, error: apiError, retry: fetchData });
    }
  }, [apiFunction]);

  useEffect(() => {
    fetchData();
  }, deps);

  return { ...state, retry: fetchData };
}

// Custom hook for form submission with error handling
function useFormSubmission<T>(
  submitFunction: (data: T) => Promise<any>
) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  const submit = async (data: T) => {
    try {
      setLoading(true);
      setError(null);
      await submitFunction(data);
      setSuccess(true);
    } catch (err) {
      setError(ApiErrorHandler.handle(err));
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSuccess(false);
    setError(null);
  };

  return { submit, loading, success, error, reset };
}
```

## Logging and Monitoring

### Structured Error Logging
Log errors with sufficient context for debugging:

```python
import structlog
from datetime import datetime

logger = structlog.get_logger()

def log_api_error(request, response, error, user_id=None):
    """Structured logging for API errors"""
    logger.error(
        "api_error_occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        status_code=getattr(response, 'status_code', 500),
        method=request.method,
        path=request.url.path,
        user_id=user_id,
        timestamp=datetime.utcnow().isoformat(),
        request_body=getattr(request, 'body', None),
        traceback=traceback.format_exc() if hasattr(error, '__traceback__') else None
    )

# Middleware for automatic error logging
async def error_logging_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code >= 400:
            # Log error responses
            log_api_error(request, response, None)
        return response
    except Exception as e:
        # Log exceptions
        response = JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )
        log_api_error(request, response, e)
        raise
```

## Error Recovery Strategies

### Graceful Degradation
Provide fallback functionality when parts of the system fail:

```typescript
// Service worker with offline capability
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').then(registration => {
    console.log('SW registered: ', registration);
  }).catch(registrationError => {
    console.log('SW registration failed: ', registrationError);
  });
}

// Fallback data when API fails
class FallbackDataManager {
  private static readonly CACHE_KEY = 'api_fallback_data';

  static saveFallbackData(key: string, data: any): void {
    try {
      const fallbackData = JSON.parse(localStorage.getItem(this.CACHE_KEY) || '{}');
      fallbackData[key] = {
        data,
        timestamp: Date.now(),
        ttl: 24 * 60 * 60 * 1000 // 24 hours
      };
      localStorage.setItem(this.CACHE_KEY, JSON.stringify(fallbackData));
    } catch (e) {
      console.error('Failed to save fallback data:', e);
    }
  }

  static getFallbackData(key: string): any {
    try {
      const fallbackData = JSON.parse(localStorage.getItem(this.CACHE_KEY) || '{}');
      const item = fallbackData[key];

      if (item && (Date.now() - item.timestamp) < item.ttl) {
        return item.data;
      }
      return null;
    } catch (e) {
      console.error('Failed to retrieve fallback data:', e);
      return null;
    }
  }

  static async apiCallWithFallback<T>(
    apiCall: () => Promise<T>,
    fallbackKey: string,
    fallbackCall?: () => Promise<T>
  ): Promise<T> {
    try {
      const result = await apiCall();
      // Save successful result as fallback
      this.saveFallbackData(fallbackKey, result);
      return result;
    } catch (error) {
      // Try fallback API call if provided
      if (fallbackCall) {
        try {
          const fallbackResult = await fallbackCall();
          this.saveFallbackData(fallbackKey, fallbackResult);
          return fallbackResult;
        } catch (fallbackError) {
          console.error('Both primary and fallback API calls failed:', fallbackError);
        }
      }

      // Return cached fallback data if available
      const cachedData = this.getFallbackData(fallbackKey);
      if (cachedData) {
        console.warn('Using fallback data due to API error');
        return cachedData;
      }

      throw error; // Re-throw original error
    }
  }
}
```