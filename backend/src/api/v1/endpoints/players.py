"""
Player API endpoints.

Placeholder endpoints for player management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_players():
    """List players - placeholder."""
    return {"message": "Players endpoint - coming soon"}
