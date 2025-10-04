"""
Result API endpoints.

Placeholder endpoints for result management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_results():
    """List results - placeholder."""
    return {"message": "Results endpoint - coming soon"}
