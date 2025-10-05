"""
Season API endpoints for the betting platform.

This module provides comprehensive CRUD operations for season management,
including creation, listing, updating, status management, and statistics.
Seasons provide temporal organization for competitions and enable historical tracking.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, get_current_user, http_not_found, http_conflict
from models import User, Season, Sport
from api.schemas.season import (
    SeasonCreate,
    SeasonUpdate,
    SeasonResponse,
    SeasonSummary,
    SeasonWithStats,
    SeasonCompetitionList,
    SeasonStandings,
    SeasonStatus,
    SeasonType
)
from services.season_service import SeasonService


router = APIRouter()


@router.post(
    "/",
    response_model=SeasonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Season",
    description="Create a new season with comprehensive validation"
)
async def create_season(
    season_data: SeasonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SeasonResponse:
    """
    Create a new season.
    
    Args:
        season_data: Season creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created season details
        
    Raises:
        HTTPException: If sport not found or validation fails
    """
    service = SeasonService(db)
    season = service.create_season(season_data)
    return SeasonResponse.model_validate(season)


@router.get(
    "/",
    response_model=List[SeasonSummary],
    summary="List Seasons",
    description="List seasons with comprehensive filtering options"
)
async def list_seasons(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    sport_id: Optional[UUID] = Query(None, description="Filter by sport ID"),
    status: Optional[SeasonStatus] = Query(None, description="Filter by status"),
    season_type: Optional[SeasonType] = Query(None, description="Filter by season type"),
    year: Optional[int] = Query(None, description="Filter by year"),
    is_public: Optional[bool] = Query(None, description="Filter by public visibility"),
    allow_betting: Optional[bool] = Query(None, description="Filter by betting allowance"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    db: Session = Depends(get_db)
) -> List[SeasonSummary]:
    """
    List seasons with filtering options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        sport_id: Filter by sport ID
        status: Filter by season status
        season_type: Filter by season type
        year: Filter by year
        is_public: Filter by public visibility
        allow_betting: Filter by betting allowance
        search: Search text for name/description
        db: Database session
        
    Returns:
        List of season summaries
    """
    service = SeasonService(db)
    seasons = service.list_seasons(
        skip=skip,
        limit=limit,
        sport_id=sport_id,
        status=status,
        season_type=season_type,
        year=year,
        is_public=is_public,
        allow_betting=allow_betting,
        search=search
    )
    return [SeasonSummary.model_validate(season) for season in seasons]


@router.get(
    "/active",
    response_model=List[SeasonSummary],
    summary="List Active Seasons",
    description="Get all currently active seasons"
)
async def list_active_seasons(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[SeasonSummary]:
    """
    Get all active seasons.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of active season summaries
    """
    service = SeasonService(db)
    seasons = service.get_active_seasons(limit=limit)
    return [SeasonSummary.model_validate(season) for season in seasons]


@router.get(
    "/current",
    response_model=List[SeasonSummary],
    summary="List Current Seasons",
    description="Get all currently running seasons"
)
async def list_current_seasons(
    sport_id: Optional[UUID] = Query(None, description="Filter by sport ID"),
    db: Session = Depends(get_db)
) -> List[SeasonSummary]:
    """
    Get all currently running seasons.
    
    Args:
        sport_id: Optional sport ID filter
        db: Database session
        
    Returns:
        List of current season summaries
    """
    service = SeasonService(db)
    seasons = service.get_current_seasons(sport_id=sport_id)
    return [SeasonSummary.model_validate(season) for season in seasons]


@router.get(
    "/public",
    response_model=List[SeasonSummary],
    summary="List Public Seasons",
    description="Get all public seasons"
)
async def list_public_seasons(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[SeasonSummary]:
    """
    Get all public seasons.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of public season summaries
    """
    service = SeasonService(db)
    seasons = service.get_public_seasons(limit=limit)
    return [SeasonSummary.model_validate(season) for season in seasons]


@router.get(
    "/{season_id}",
    response_model=SeasonResponse,
    summary="Get Season",
    description="Get season details by ID"
)
async def get_season(
    season_id: UUID,
    db: Session = Depends(get_db)
) -> SeasonResponse:
    """
    Get season by ID.
    
    Args:
        season_id: Season unique identifier
        db: Database session
        
    Returns:
        Season details
        
    Raises:
        HTTPException: If season not found
    """
    service = SeasonService(db)
    season = service.get_season(season_id)
    
    if not season:
        raise http_not_found(f"Season with ID {season_id} not found")
        
    return SeasonResponse.model_validate(season)


@router.get(
    "/{season_id}/stats",
    response_model=SeasonWithStats,
    summary="Get Season Statistics",
    description="Get comprehensive season statistics"
)
async def get_season_statistics(
    season_id: UUID,
    db: Session = Depends(get_db)
) -> SeasonWithStats:
    """
    Get season statistics.
    
    Args:
        season_id: Season unique identifier
        db: Database session
        
    Returns:
        Season details with statistics
        
    Raises:
        HTTPException: If season not found
    """
    service = SeasonService(db)
    season = service.get_season(season_id)
    
    if not season:
        raise http_not_found(f"Season with ID {season_id} not found")
        
    stats = service.get_season_statistics(season_id)
    
    # Create response with stats
    season_dict = SeasonResponse.model_validate(season).model_dump()
    season_dict['stats'] = stats
    
    return SeasonWithStats.model_validate(season_dict)


@router.get(
    "/{season_id}/competitions",
    response_model=SeasonCompetitionList,
    summary="Get Season Competitions",
    description="Get all competitions in the season"
)
async def get_season_competitions(
    season_id: UUID,
    db: Session = Depends(get_db)
) -> SeasonCompetitionList:
    """
    Get competitions in a season.
    
    Args:
        season_id: Season unique identifier
        db: Database session
        
    Returns:
        List of competitions in the season
        
    Raises:
        HTTPException: If season not found
    """
    service = SeasonService(db)
    season = service.get_season(season_id)
    
    if not season:
        raise http_not_found(f"Season with ID {season_id} not found")
        
    competitions = service.get_season_competitions(season_id)
    
    return SeasonCompetitionList(
        season_id=season_id,
        competitions=competitions,
        total_competitions=len(competitions)
    )


@router.get(
    "/{season_id}/standings",
    response_model=SeasonStandings,
    summary="Get Season Standings",
    description="Get team standings/leaderboard for the season"
)
async def get_season_standings(
    season_id: UUID,
    db: Session = Depends(get_db)
) -> SeasonStandings:
    """
    Get season standings.
    
    Args:
        season_id: Season unique identifier
        db: Database session
        
    Returns:
        Season standings/leaderboard
        
    Raises:
        HTTPException: If season not found
    """
    service = SeasonService(db)
    season = service.get_season(season_id)
    
    if not season:
        raise http_not_found(f"Season with ID {season_id} not found")
        
    standings = service.calculate_team_standings(season_id)
    
    from datetime import datetime
    return SeasonStandings(
        season_id=season_id,
        standings=standings,
        last_updated=datetime.utcnow()
    )


@router.get(
    "/sport/{sport_id}",
    response_model=List[SeasonSummary],
    summary="List Seasons by Sport",
    description="Get all seasons for a specific sport"
)
async def list_seasons_by_sport(
    sport_id: UUID,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[SeasonSummary]:
    """
    Get seasons by sport.
    
    Args:
        sport_id: Sport unique identifier
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of seasons for the sport
    """
    service = SeasonService(db)
    seasons = service.get_seasons_by_sport(sport_id, limit=limit)
    return [SeasonSummary.model_validate(season) for season in seasons]


@router.get(
    "/year/{year}",
    response_model=List[SeasonSummary],
    summary="List Seasons by Year",
    description="Get all seasons for a specific year"
)
async def list_seasons_by_year(
    year: int,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[SeasonSummary]:
    """
    Get seasons by year.
    
    Args:
        year: Year to filter by
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of seasons for the year
    """
    service = SeasonService(db)
    seasons = service.get_seasons_by_year(year, limit=limit)
    return [SeasonSummary.model_validate(season) for season in seasons]


@router.get(
    "/name/{name}",
    response_model=SeasonResponse,
    summary="Get Season by Name",
    description="Find season by exact name match"
)
async def get_season_by_name(
    name: str,
    sport_id: Optional[UUID] = Query(None, description="Scope search to specific sport"),
    db: Session = Depends(get_db)
) -> SeasonResponse:
    """
    Get season by name.
    
    Args:
        name: Season name
        sport_id: Optional sport ID to scope the search
        db: Database session
        
    Returns:
        Season details
        
    Raises:
        HTTPException: If season not found
    """
    service = SeasonService(db)
    season = service.get_season_by_name(name, sport_id)
    
    if not season:
        raise http_not_found(f"Season '{name}' not found")
        
    return SeasonResponse.model_validate(season)


@router.put(
    "/{season_id}",
    response_model=SeasonResponse,
    summary="Update Season",
    description="Update season details with validation"
)
async def update_season(
    season_id: UUID,
    update_data: SeasonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SeasonResponse:
    """
    Update season.
    
    Args:
        season_id: Season unique identifier
        update_data: Updated season data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated season details
        
    Raises:
        HTTPException: If season not found or validation fails
    """
    service = SeasonService(db)
    season = service.update_season(season_id, update_data)
    
    if not season:
        raise http_not_found(f"Season with ID {season_id} not found")
        
    return SeasonResponse.model_validate(season)


@router.delete(
    "/{season_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Season",
    description="Soft delete season (sets as inactive)"
)
async def delete_season(
    season_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete season (soft delete).
    
    Args:
        season_id: Season unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If season not found
    """
    service = SeasonService(db)
    deleted = service.delete_season(season_id)
    
    if not deleted:
        raise http_not_found(f"Season with ID {season_id} not found")


@router.post(
    "/{season_id}/status",
    response_model=SeasonResponse,
    summary="Update Season Status",
    description="Update season status (upcoming, active, completed, cancelled)"
)
async def update_season_status(
    season_id: UUID,
    status: SeasonStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SeasonResponse:
    """
    Update season status.
    
    Args:
        season_id: Season unique identifier
        status: New season status
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated season details
        
    Raises:
        HTTPException: If season not found
    """
    service = SeasonService(db)
    season = service.update_status(season_id, status)
    
    if not season:
        raise http_not_found(f"Season with ID {season_id} not found")
        
    return SeasonResponse.model_validate(season)


@router.get(
    "/search/{query}",
    response_model=List[SeasonSummary],
    summary="Search Seasons",
    description="Search seasons by name or description"
)
async def search_seasons(
    query: str,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[SeasonSummary]:
    """
    Search seasons.
    
    Args:
        query: Search query string
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of matching seasons
    """
    service = SeasonService(db)
    seasons = service.search_seasons(query, limit=limit)
    return [SeasonSummary.model_validate(season) for season in seasons]
