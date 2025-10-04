"""
Services module for the betting platform.

This module contains business logic services for all models,
providing a clean separation between API controllers and data access.
"""

from .user_service import UserService

__all__ = [
    "UserService",
]