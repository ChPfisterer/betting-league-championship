"""
Core module for the betting platform API.

This module provides the foundational components including
configuration, database, security, exceptions, and utilities.
"""

from .config import Settings, get_settings, settings
from .database import get_db, get_db_context, DatabaseSession, Base
from .security import (
    get_password_hash,
    verify_password
)
from .exceptions import (
    BettingPlatformException,
    ValidationError,
    NotFoundError,
    PermissionError,
    ConflictError,
    BusinessLogicError,
    http_not_found,
    http_forbidden,
    http_conflict,
    http_validation_error,
    http_bad_request,
    convert_to_http_exception
)
from .utils import (
    PaginationParams,
    PaginatedResponse,
    paginate_query,
    utc_now,
    validate_uuid,
    format_currency,
    sanitize_string,
    build_sort_criteria,
    APIResponse
)

__all__ = [
    # Config
    "Settings",
    "get_settings", 
    "settings",
    
    # Database
    "get_db",
    "get_db_context",
    "DatabaseSession",
    "Base",
    
    # Security (Keycloak-only)
    "get_password_hash",
    "verify_password",
    
    # Exceptions
    "BettingPlatformException",
    "ValidationError",
    "NotFoundError",
    "PermissionError",
    "ConflictError",
    "BusinessLogicError",
    "http_not_found",
    "http_forbidden",
    "http_conflict",
    "http_validation_error",
    "http_bad_request",
    "convert_to_http_exception",
    
    # Utils
    "PaginationParams",
    "PaginatedResponse",
    "paginate_query",
    "utc_now",
    "validate_uuid",
    "format_currency",
    "sanitize_string",
    "build_sort_criteria",
    "APIResponse",
]