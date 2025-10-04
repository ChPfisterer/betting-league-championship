"""
Competition API endpoints.

Placeholder endpoints for competition management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_competitions():
    """List competitions - placeholder."""
    return {"message": "Competitions endpoint - coming soon"}
