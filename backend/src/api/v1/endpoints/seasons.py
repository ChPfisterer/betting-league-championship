"""
Season API endpoints.

Placeholder endpoints for season management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_seasons():
    """List seasons - placeholder."""
    return {"message": "Seasons endpoint - coming soon"}
