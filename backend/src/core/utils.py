"""
Core utilities and helper functions.

Common utilities used across the betting platform API including
pagination, validation helpers, and data transformation utilities.
"""

from datetime import datetime, timezone
from math import ceil
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, validator
from sqlalchemy import func
from sqlalchemy.orm import Query as SQLQuery, Session

from .config import get_settings

settings = get_settings()

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination parameters for API endpoints."""
    
    page: int = Query(1, ge=1, description="Page number (1-based)")
    size: int = Query(
        settings.default_page_size, 
        ge=1, 
        le=settings.max_page_size,
        description=f"Page size (max {settings.max_page_size})"
    )
    
    @validator('size')
    def validate_size(cls, v):
        """Ensure page size doesn't exceed maximum."""
        if v > settings.max_page_size:
            return settings.max_page_size
        return v
    
    @property
    def offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""
    
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_previous: bool
    
    @validator('pages', pre=True, always=True)
    def calculate_pages(cls, v, values):
        """Calculate total pages from total items and size."""
        total = values.get('total', 0)
        size = values.get('size', 1)
        return ceil(total / size) if total > 0 else 1
    
    @validator('has_next', pre=True, always=True)
    def calculate_has_next(cls, v, values):
        """Calculate if there's a next page."""
        page = values.get('page', 1)
        pages = values.get('pages', 1)
        return page < pages
    
    @validator('has_previous', pre=True, always=True)
    def calculate_has_previous(cls, v, values):
        """Calculate if there's a previous page."""
        page = values.get('page', 1)
        return page > 1


def paginate_query(
    query: SQLQuery,
    db: Session,
    pagination: PaginationParams
) -> PaginatedResponse:
    """
    Apply pagination to a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query to paginate
        db: Database session
        pagination: Pagination parameters
        
    Returns:
        PaginatedResponse: Paginated results
    """
    # Get total count
    total = db.query(func.count()).select_from(query.subquery()).scalar()
    
    # Apply pagination
    items = query.offset(pagination.offset).limit(pagination.size).all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=ceil(total / pagination.size) if total > 0 else 1,
        has_next=pagination.page < ceil(total / pagination.size),
        has_previous=pagination.page > 1
    )


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def validate_uuid(value: str) -> UUID:
    """
    Validate and convert string to UUID.
    
    Args:
        value: String value to convert
        
    Returns:
        UUID: Validated UUID
        
    Raises:
        ValueError: If value is not a valid UUID
    """
    try:
        return UUID(value)
    except ValueError:
        raise ValueError(f"Invalid UUID format: {value}")


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format currency amount for display.
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        str: Formatted currency string
    """
    return f"{amount:.2f} {currency}"


def sanitize_string(value: Optional[str]) -> Optional[str]:
    """
    Sanitize string input by trimming whitespace.
    
    Args:
        value: String to sanitize
        
    Returns:
        Optional[str]: Sanitized string or None
    """
    if value is None:
        return None
    
    sanitized = value.strip()
    return sanitized if sanitized else None


def build_sort_criteria(
    sort_by: Optional[str] = None,
    sort_order: str = "asc"
) -> Dict[str, str]:
    """
    Build sorting criteria for database queries.
    
    Args:
        sort_by: Field to sort by
        sort_order: Sort order (asc/desc)
        
    Returns:
        Dict[str, str]: Sort criteria
    """
    return {
        "sort_by": sort_by,
        "sort_order": sort_order.lower() if sort_order else "asc"
    }


class APIResponse(BaseModel):
    """Standard API response wrapper."""
    
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    
    @classmethod
    def success_response(
        cls, 
        data: Any = None, 
        message: Optional[str] = None
    ) -> "APIResponse":
        """Create a success response."""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_response(
        cls, 
        errors: List[str], 
        message: Optional[str] = None
    ) -> "APIResponse":
        """Create an error response."""
        return cls(success=False, errors=errors, message=message)