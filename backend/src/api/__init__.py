"""
API routers for the betting platform.

This module organizes and exposes all API endpoints for the betting platform,
providing a clean separation of concerns and modular route organization.
"""

from fastapi import APIRouter

from .v1 import api_router as api_v1_router

# Main API router
api_router = APIRouter()

# Include versioned API routers
api_router.include_router(api_v1_router, prefix="/api/v1")

__all__ = ["api_router"]