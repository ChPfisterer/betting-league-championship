"""
Team API endpoints.

Placeholder endpoints for team management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_teams():
    """List teams - placeholder."""
    return {"message": "Teams endpoint - coming soon"}
