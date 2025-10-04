"""
Sport API endpoints.

Placeholder endpoints for sports management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_sports():
    """List sports - placeholder."""
    return {"message": "Sports endpoint - coming soon"}
