"""
Match API endpoints for the betting platform.

This module provides comprehensive CRUD operations for match management,
including creation, listing, updating, score tracking, status management,
and statistics. Matches are the core events where betting takes place.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, get_current_user, http_not_found, http_conflict
from models import User, Match, Team, Competition
from api.schemas.match import (
    MatchCreate,
    MatchUpdate,
    MatchScoreUpdate,
    MatchStatusUpdate,
    MatchResponse,
    MatchSummary,
    MatchWithStats,
    MatchWithTeams,
    MatchWithCompetition,
    MatchStatus,
    MatchType
)
from services.match_service import MatchService


router = APIRouter()


@router.post(
    "/",
    response_model=MatchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Match",
    description="Create a new match with comprehensive validation"
)
async def create_match(
    match_data: MatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MatchResponse:
    """
    Create a new match.
    
    Args:
        match_data: Match creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created match details
        
    Raises:
        HTTPException: If validation fails
    """
    service = MatchService(db)
    match = service.create_match(match_data)
    return MatchResponse.model_validate(match)


@router.get(
    "/",
    response_model=List[MatchSummary],
    summary="List Matches",
    description="List matches with comprehensive filtering options"
)
async def list_matches(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    competition_id: Optional[UUID] = Query(None, description="Filter by competition ID"),
    season_id: Optional[UUID] = Query(None, description="Filter by season ID"),
    team_id: Optional[UUID] = Query(None, description="Filter by team (home or away)"),
    status: Optional[MatchStatus] = Query(None, description="Filter by match status"),
    match_type: Optional[MatchType] = Query(None, description="Filter by match type"),
    date_from: Optional[date] = Query(None, description="Filter matches from this date"),
    date_to: Optional[date] = Query(None, description="Filter matches until this date"),
    venue_city: Optional[str] = Query(None, description="Filter by venue city"),
    allow_betting: Optional[bool] = Query(None, description="Filter by betting allowance"),
    db: Session = Depends(get_db)
) -> List[MatchSummary]:
    """
    List matches with filtering options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        competition_id: Filter by competition ID
        season_id: Filter by season ID
        team_id: Filter by team (home or away)
        status: Filter by match status
        match_type: Filter by match type
        date_from: Filter matches from this date
        date_to: Filter matches until this date
        venue_city: Filter by venue city
        allow_betting: Filter by betting allowance
        db: Database session
        
    Returns:
        List of match summaries
    """
    service = MatchService(db)
    matches = service.list_matches(
        skip=skip,
        limit=limit,
        competition_id=competition_id,
        season_id=season_id,
        team_id=team_id,
        status=status,
        match_type=match_type,
        date_from=date_from,
        date_to=date_to,
        venue_city=venue_city,
        allow_betting=allow_betting
    )
    return [MatchSummary.model_validate(match) for match in matches]


@router.get(
    "/upcoming",
    response_model=List[MatchSummary],
    summary="List Upcoming Matches",
    description="Get upcoming matches within specified days"
)
async def list_upcoming_matches(
    days: int = Query(7, ge=1, le=365, description="Number of days to look ahead"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[MatchSummary]:
    """
    Get upcoming matches.
    
    Args:
        days: Number of days to look ahead
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of upcoming match summaries
    """
    service = MatchService(db)
    matches = service.get_upcoming_matches(days=days, limit=limit)
    return [MatchSummary.model_validate(match) for match in matches]


@router.get(
    "/live",
    response_model=List[MatchSummary],
    summary="List Live Matches",
    description="Get all currently live matches"
)
async def list_live_matches(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[MatchSummary]:
    """
    Get live matches.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of live match summaries
    """
    service = MatchService(db)
    matches = service.get_live_matches(limit=limit)
    return [MatchSummary.model_validate(match) for match in matches]


@router.get(
    "/recent",
    response_model=List[MatchSummary],
    summary="List Recent Results",
    description="Get recent completed matches"
)
async def list_recent_results(
    days: int = Query(7, ge=1, le=365, description="Number of days to look back"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[MatchSummary]:
    """
    Get recent match results.
    
    Args:
        days: Number of days to look back
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of recent match summaries
    """
    service = MatchService(db)
    matches = service.get_recent_results(days=days, limit=limit)
    return [MatchSummary.model_validate(match) for match in matches]


@router.get(
    "/{match_id}",
    response_model=MatchResponse,
    summary="Get Match",
    description="Get match details by ID"
)
async def get_match(
    match_id: UUID,
    db: Session = Depends(get_db)
) -> MatchResponse:
    """
    Get match by ID.
    
    Args:
        match_id: Match unique identifier
        db: Database session
        
    Returns:
        Match details
        
    Raises:
        HTTPException: If match not found
    """
    service = MatchService(db)
    match = service.get_match(match_id)
    
    if not match:
        raise http_not_found(f"Match with ID {match_id} not found")
        
    return MatchResponse.model_validate(match)


@router.get(
    "/{match_id}/stats",
    response_model=MatchWithStats,
    summary="Get Match Statistics",
    description="Get comprehensive match statistics"
)
async def get_match_statistics(
    match_id: UUID,
    db: Session = Depends(get_db)
) -> MatchWithStats:
    """
    Get match statistics.
    
    Args:
        match_id: Match unique identifier
        db: Database session
        
    Returns:
        Match details with statistics
        
    Raises:
        HTTPException: If match not found
    """
    service = MatchService(db)
    match = service.get_match(match_id)
    
    if not match:
        raise http_not_found(f"Match with ID {match_id} not found")
        
    stats = service.get_match_statistics(match_id)
    
    # Create response with stats
    match_dict = MatchResponse.model_validate(match).model_dump()
    match_dict['stats'] = stats
    
    return MatchWithStats.model_validate(match_dict)


@router.get(
    "/{match_id}/with-teams",
    response_model=MatchWithTeams,
    summary="Get Match with Teams",
    description="Get match details including team information"
)
async def get_match_with_teams(
    match_id: UUID,
    db: Session = Depends(get_db)
) -> MatchWithTeams:
    """
    Get match with team details.
    
    Args:
        match_id: Match unique identifier
        db: Database session
        
    Returns:
        Match details with team information
        
    Raises:
        HTTPException: If match not found
    """
    service = MatchService(db)
    match = service.get_match(match_id)
    
    if not match:
        raise http_not_found(f"Match with ID {match_id} not found")
    
    # Load team relationships
    home_team = db.query(Team).filter(Team.id == match.home_team_id).first()
    away_team = db.query(Team).filter(Team.id == match.away_team_id).first()
    
    match_dict = MatchResponse.model_validate(match).model_dump()
    match_dict['home_team'] = home_team
    match_dict['away_team'] = away_team
    
    return MatchWithTeams.model_validate(match_dict)


@router.get(
    "/{match_id}/with-competition",
    response_model=MatchWithCompetition,
    summary="Get Match with Competition",
    description="Get match details including competition information"
)
async def get_match_with_competition(
    match_id: UUID,
    db: Session = Depends(get_db)
) -> MatchWithCompetition:
    """
    Get match with competition details.
    
    Args:
        match_id: Match unique identifier
        db: Database session
        
    Returns:
        Match details with competition information
        
    Raises:
        HTTPException: If match not found
    """
    service = MatchService(db)
    match = service.get_match(match_id)
    
    if not match:
        raise http_not_found(f"Match with ID {match_id} not found")
    
    # Load competition relationship
    competition = db.query(Competition).filter(Competition.id == match.competition_id).first()
    
    match_dict = MatchResponse.model_validate(match).model_dump()
    match_dict['competition'] = competition
    
    return MatchWithCompetition.model_validate(match_dict)


@router.get(
    "/team/{team_id}",
    response_model=List[MatchSummary],
    summary="List Matches by Team",
    description="Get all matches for a specific team"
)
async def list_matches_by_team(
    team_id: UUID,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[MatchSummary]:
    """
    Get matches by team.
    
    Args:
        team_id: Team unique identifier
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of matches for the team
    """
    service = MatchService(db)
    matches = service.get_matches_by_team(team_id, limit=limit)
    return [MatchSummary.model_validate(match) for match in matches]


@router.get(
    "/competition/{competition_id}",
    response_model=List[MatchSummary],
    summary="List Matches by Competition",
    description="Get all matches for a specific competition"
)
async def list_matches_by_competition(
    competition_id: UUID,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[MatchSummary]:
    """
    Get matches by competition.
    
    Args:
        competition_id: Competition unique identifier
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of matches for the competition
    """
    service = MatchService(db)
    matches = service.get_matches_by_competition(competition_id, limit=limit)
    return [MatchSummary.model_validate(match) for match in matches]


@router.get(
    "/head-to-head/{team1_id}/{team2_id}",
    response_model=List[MatchSummary],
    summary="Get Head-to-Head Matches",
    description="Get head-to-head matches between two teams"
)
async def get_head_to_head(
    team1_id: UUID,
    team2_id: UUID,
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[MatchSummary]:
    """
    Get head-to-head matches between two teams.
    
    Args:
        team1_id: First team ID
        team2_id: Second team ID
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of head-to-head matches
    """
    service = MatchService(db)
    matches = service.get_head_to_head(team1_id, team2_id, limit=limit)
    return [MatchSummary.model_validate(match) for match in matches]


@router.put(
    "/{match_id}",
    response_model=MatchResponse,
    summary="Update Match",
    description="Update match details with validation"
)
async def update_match(
    match_id: UUID,
    update_data: MatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MatchResponse:
    """
    Update match.
    
    Args:
        match_id: Match unique identifier
        update_data: Updated match data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated match details
        
    Raises:
        HTTPException: If match not found or validation fails
    """
    service = MatchService(db)
    match = service.update_match(match_id, update_data)
    
    if not match:
        raise http_not_found(f"Match with ID {match_id} not found")
        
    return MatchResponse.model_validate(match)


@router.patch(
    "/{match_id}/score",
    response_model=MatchResponse,
    summary="Update Match Score",
    description="Update match score and determine winner"
)
async def update_match_score(
    match_id: UUID,
    score_data: MatchScoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MatchResponse:
    """
    Update match score.
    
    Args:
        match_id: Match unique identifier
        score_data: Score update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated match details
        
    Raises:
        HTTPException: If match not found or validation fails
    """
    service = MatchService(db)
    match = service.update_score(match_id, score_data)
    
    if not match:
        raise http_not_found(f"Match with ID {match_id} not found")
        
    return MatchResponse.model_validate(match)


@router.patch(
    "/{match_id}/status",
    response_model=MatchResponse,
    summary="Update Match Status",
    description="Update match status (scheduled, live, completed, etc.)"
)
async def update_match_status(
    match_id: UUID,
    status_data: MatchStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MatchResponse:
    """
    Update match status.
    
    Args:
        match_id: Match unique identifier
        status_data: Status update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated match details
        
    Raises:
        HTTPException: If match not found
    """
    service = MatchService(db)
    match = service.update_status(match_id, status_data)
    
    if not match:
        raise http_not_found(f"Match with ID {match_id} not found")
        
    return MatchResponse.model_validate(match)


@router.delete(
    "/{match_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Match",
    description="Soft delete match (sets as inactive)"
)
async def delete_match(
    match_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete match (soft delete).
    
    Args:
        match_id: Match unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If match not found or cannot be deleted
    """
    service = MatchService(db)
    deleted = service.delete_match(match_id)
    
    if not deleted:
        raise http_not_found(f"Match with ID {match_id} not found")


@router.get(
    "/search/{query}",
    response_model=List[MatchSummary],
    summary="Search Matches",
    description="Search matches by venue name or notes"
)
async def search_matches(
    query: str,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[MatchSummary]:
    """
    Search matches.
    
    Args:
        query: Search query string
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of matching matches
    """
    service = MatchService(db)
    matches = service.search_matches(query, limit=limit)
    return [MatchSummary.model_validate(match) for match in matches]
