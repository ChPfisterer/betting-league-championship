"""
Match API endpoints.

Placeholder endpoints for match management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_matches():
    """List matches - placeholder."""
    return {"message": "Matches endpoint - coming soon"}
