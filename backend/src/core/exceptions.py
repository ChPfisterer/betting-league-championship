"""
Core exceptions for the betting platform API.

Standardized exception handling with proper HTTP status codes
and consistent error response formats.
"""

from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import HTTPException, status


class BettingPlatformException(Exception):
    """Base exception for betting platform."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(BettingPlatformException):
    """Business logic validation error."""
    pass


class NotFoundError(BettingPlatformException):
    """Resource not found error."""
    pass


class PermissionError(BettingPlatformException):
    """Insufficient permissions error."""
    pass


class ConflictError(BettingPlatformException):
    """Resource conflict error."""
    pass


class BusinessLogicError(BettingPlatformException):
    """Business logic violation error."""
    pass


# HTTP Exception factories
def http_not_found(
    resource: str, 
    identifier: Optional[str] = None
) -> HTTPException:
    """Create a 404 Not Found HTTP exception."""
    detail = f"{resource} not found"
    if identifier:
        detail += f" with identifier: {identifier}"
    
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )


def http_forbidden(
    message: str = "Insufficient permissions"
) -> HTTPException:
    """Create a 403 Forbidden HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message
    )


def http_conflict(
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a 409 Conflict HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )


def http_validation_error(
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a 422 Validation Error HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )


def http_bad_request(
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a 400 Bad Request HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )


# Exception to HTTP exception mapping
EXCEPTION_STATUS_MAP = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    PermissionError: status.HTTP_403_FORBIDDEN,
    ConflictError: status.HTTP_409_CONFLICT,
    ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    BusinessLogicError: status.HTTP_400_BAD_REQUEST,
}


def convert_to_http_exception(exc: BettingPlatformException) -> HTTPException:
    """Convert platform exception to HTTP exception."""
    status_code = EXCEPTION_STATUS_MAP.get(
        type(exc), 
        status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    
    return HTTPException(
        status_code=status_code,
        detail=exc.message
    )