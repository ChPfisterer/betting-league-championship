"""
Bet API endpoints for the betting platform.

This module provides comprehensive CRUD operations for bet management,
including bet placement, listing, settlement, statistics, and advanced
betting features like odds management and leaderboards.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, http_not_found, http_conflict
from core.keycloak_security import get_current_user_hybrid
from models import User, Bet, Match, Group
from api.schemas.bet import (
    BetCreate,
    BetUpdate,
    BetSettlement,
    BetResponse,
    BetSummary,
    BetWithMatch,
    BetWithUser,
    BetWithStats,
    BetHistory,
    BetOdds,
    BetSlip,
    BetLeaderboard,
    BetAnalytics,
    BetType,
    BetStatus
)
from services.bet_service import BetService


router = APIRouter()


@router.post(
    "/",
    response_model=BetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Place Bet",
    description="Place a new bet with comprehensive validation"
)
async def place_bet(
    bet_data: BetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> BetResponse:
    """
    Place a new bet.
    
    Args:
        bet_data: Bet placement data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Placed bet details
        
    Raises:
        HTTPException: If validation fails
    """
    # Add detailed logging for debugging
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Placing bet for user {current_user.username}: {bet_data.model_dump()}")
        service = BetService(db)
        bet = service.create_bet(bet_data, current_user.id)
        # Transform the model to response schema format
        bet_dict = service.transform_bet_for_response(bet)
        return BetResponse.model_validate(bet_dict)
    except ValueError as e:
        logger.error(f"Bet placement validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error placing bet: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/",
    response_model=List[BetSummary],
    summary="List Bets",
    description="List bets with comprehensive filtering options"
)
async def list_bets(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
    match_id: Optional[UUID] = Query(None, description="Filter by match ID"),
    group_id: Optional[UUID] = Query(None, description="Filter by group ID"),
    bet_type: Optional[BetType] = Query(None, description="Filter by bet type"),
    status: Optional[BetStatus] = Query(None, description="Filter by bet status"),
    date_from: Optional[datetime] = Query(None, description="Filter bets from this date"),
    date_to: Optional[datetime] = Query(None, description="Filter bets until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[BetSummary]:
    """
    List bets with filtering options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        user_id: Filter by user ID
        match_id: Filter by match ID
        group_id: Filter by group ID
        bet_type: Filter by bet type
        status: Filter by bet status
        date_from: Filter bets from this date
        date_to: Filter bets until this date
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of bet summaries
    """
    service = BetService(db)
    bets = service.list_bets(
        skip=skip,
        limit=limit,
        user_id=user_id,
        match_id=match_id,
        group_id=group_id,
        bet_type=bet_type,
        status=status,
        date_from=date_from,
        date_to=date_to
    )
    return [BetSummary.model_validate(bet) for bet in bets]


@router.get(
    "/my-bets",
    response_model=List[BetSummary],
    summary="Get My Bets",
    description="Get all bets for the current user"
)
async def get_my_bets(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[BetSummary]:
    """
    Get bets for the current user.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of user's bets
    """
    service = BetService(db)
    bets = service.get_user_bets(current_user.id, limit=limit)
    return [BetSummary.model_validate(bet) for bet in bets]


@router.get(
    "/pending",
    response_model=List[BetSummary],
    summary="List Pending Bets",
    description="Get all pending bets"
)
async def list_pending_bets(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[BetSummary]:
    """
    Get pending bets.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of pending bets
    """
    service = BetService(db)
    bets = service.get_pending_bets(limit=limit)
    return [BetSummary.model_validate(bet) for bet in bets]


@router.get(
    "/active",
    response_model=List[BetSummary],
    summary="List Active Bets",
    description="Get all active bets (matches in progress)"
)
async def list_active_bets(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[BetSummary]:
    """
    Get active bets.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of active bets
    """
    service = BetService(db)
    bets = service.get_active_bets(limit=limit)
    return [BetSummary.model_validate(bet) for bet in bets]


@router.get(
    "/{bet_id}",
    response_model=BetResponse,
    summary="Get Bet",
    description="Get bet details by ID"
)
async def get_bet(
    bet_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> BetResponse:
    """
    Get bet by ID.
    
    Args:
        bet_id: Bet unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Bet details
        
    Raises:
        HTTPException: If bet not found
    """
    service = BetService(db)
    bet = service.get_bet(bet_id)
    
    if not bet:
        raise http_not_found(f"Bet with ID {bet_id} not found")
        
    return BetResponse.model_validate(bet)


@router.get(
    "/{bet_id}/with-match",
    response_model=BetWithMatch,
    summary="Get Bet with Match",
    description="Get bet details including match information"
)
async def get_bet_with_match(
    bet_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> BetWithMatch:
    """
    Get bet with match details.
    
    Args:
        bet_id: Bet unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Bet details with match information
        
    Raises:
        HTTPException: If bet not found
    """
    service = BetService(db)
    bet = service.get_bet(bet_id)
    
    if not bet:
        raise http_not_found(f"Bet with ID {bet_id} not found")
    
    # Load match relationship
    match = db.query(Match).filter(Match.id == bet.match_id).first()
    
    bet_dict = BetResponse.model_validate(bet).model_dump()
    bet_dict['match'] = match
    
    return BetWithMatch.model_validate(bet_dict)


@router.get(
    "/user/{user_id}",
    response_model=List[BetSummary],
    summary="List Bets by User",
    description="Get all bets for a specific user"
)
async def list_bets_by_user(
    user_id: UUID,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[BetSummary]:
    """
    Get bets by user.
    
    Args:
        user_id: User unique identifier
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of bets for the user
    """
    service = BetService(db)
    bets = service.get_user_bets(user_id, limit=limit)
    return [BetSummary.model_validate(bet) for bet in bets]


@router.get(
    "/match/{match_id}",
    response_model=List[BetSummary],
    summary="List Bets by Match",
    description="Get all bets for a specific match"
)
async def list_bets_by_match(
    match_id: UUID,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[BetSummary]:
    """
    Get bets by match.
    
    Args:
        match_id: Match unique identifier
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of bets for the match
    """
    service = BetService(db)
    bets = service.get_match_bets(match_id, limit=limit)
    return [BetSummary.model_validate(bet) for bet in bets]


@router.get(
    "/group/{group_id}",
    response_model=List[BetSummary],
    summary="List Bets by Group",
    description="Get all bets for a specific group"
)
async def list_bets_by_group(
    group_id: UUID,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[BetSummary]:
    """
    Get bets by group.
    
    Args:
        group_id: Group unique identifier
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of bets for the group
    """
    service = BetService(db)
    bets = service.get_group_bets(group_id, limit=limit)
    return [BetSummary.model_validate(bet) for bet in bets]


@router.get(
    "/statistics/user/{user_id}",
    response_model=dict,
    summary="Get User Betting Statistics",
    description="Get comprehensive betting statistics for a user"
)
async def get_user_statistics(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> dict:
    """
    Get user betting statistics.
    
    Args:
        user_id: User unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        User betting statistics
    """
    service = BetService(db)
    return service.get_user_statistics(user_id)


@router.get(
    "/statistics/match/{match_id}",
    response_model=dict,
    summary="Get Match Betting Statistics",
    description="Get betting statistics for a specific match"
)
async def get_match_statistics(
    match_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> dict:
    """
    Get match betting statistics.
    
    Args:
        match_id: Match unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Match betting statistics
    """
    service = BetService(db)
    return service.get_match_statistics(match_id)


@router.put(
    "/{bet_id}",
    response_model=BetResponse,
    summary="Update Bet",
    description="Update bet details (limited fields)"
)
async def update_bet(
    bet_id: UUID,
    update_data: BetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> BetResponse:
    """
    Update bet.
    
    Args:
        bet_id: Bet unique identifier
        update_data: Updated bet data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated bet details
        
    Raises:
        HTTPException: If bet not found or cannot be updated
    """
    service = BetService(db)
    try:
        bet = service.update_bet(bet_id, update_data)
        if not bet:
            raise http_not_found(f"Bet with ID {bet_id} not found")
        return BetResponse.model_validate(bet)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{bet_id}/settle",
    response_model=BetResponse,
    summary="Settle Bet",
    description="Settle a bet based on match results"
)
async def settle_bet(
    bet_id: UUID,
    settlement: BetSettlement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> BetResponse:
    """
    Settle bet.
    
    Args:
        bet_id: Bet unique identifier
        settlement: Settlement details
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Settled bet details
        
    Raises:
        HTTPException: If bet not found or cannot be settled
    """
    service = BetService(db)
    try:
        bet = service.settle_bet(bet_id, settlement)
        if not bet:
            raise http_not_found(f"Bet with ID {bet_id} not found")
        return BetResponse.model_validate(bet)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/match/{match_id}/auto-settle",
    response_model=dict,
    summary="Auto-Settle Match Bets",
    description="Automatically settle all bets for a completed match"
)
async def auto_settle_match_bets(
    match_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> dict:
    """
    Auto-settle bets for a match.
    
    Args:
        match_id: Match unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Settlement summary
    """
    service = BetService(db)
    settled_count = service.auto_settle_match_bets(match_id)
    return {
        "match_id": match_id,
        "bets_settled": settled_count,
        "message": f"Successfully settled {settled_count} bets"
    }


@router.delete(
    "/{bet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel Bet",
    description="Cancel a pending bet"
)
async def cancel_bet(
    bet_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> None:
    """
    Cancel bet.
    
    Args:
        bet_id: Bet unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If bet not found or cannot be cancelled
    """
    service = BetService(db)
    try:
        deleted = service.delete_bet(bet_id)
        if not deleted:
            raise http_not_found(f"Bet with ID {bet_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/search/{query}",
    response_model=List[BetSummary],
    summary="Search Bets",
    description="Search bets by notes or settlement reason"
)
async def search_bets(
    query: str,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[BetSummary]:
    """
    Search bets.
    
    Args:
        query: Search query string
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of matching bets
    """
    service = BetService(db)
    bets = service.search_bets(query, limit=limit)
    return [BetSummary.model_validate(bet) for bet in bets]
