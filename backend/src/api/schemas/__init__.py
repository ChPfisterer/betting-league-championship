"""
Pydantic schemas package for API request/response models.

This module organizes all Pydantic schemas for the betting platform API,
providing consistent validation and serialization across all endpoints.
"""

from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserResponse,
    UserProfile,
    UserSummary,
    UserLogin,
    UserLoginResponse,
    UserRegistrationResponse
)

from .group import (
    GroupBase,
    GroupCreate,
    GroupUpdate,
    GroupResponse,
    GroupSummary,
    GroupWithStats
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPasswordUpdate",
    "UserResponse",
    "UserProfile",
    "UserSummary",
    "UserLogin",
    "UserLoginResponse",
    "UserRegistrationResponse",
    
    # Group schemas
    "GroupBase",
    "GroupCreate",
    "GroupUpdate",
    "GroupResponse",
    "GroupSummary",
    "GroupWithStats",
]