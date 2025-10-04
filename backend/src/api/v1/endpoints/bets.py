"""
Bet API endpoints.

Placeholder endpoints for betting management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_bets():
    """List bets - placeholder."""
    return {"message": "Bets endpoint - coming soon"}
