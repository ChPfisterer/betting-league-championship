"""
Group API endpoints.

Placeholder endpoints for group management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_groups():
    """List groups - placeholder."""
    return {"message": "Groups endpoint - coming soon"}
