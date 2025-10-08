"""
Competition API endpoints for the betting platform.

This module provides comprehensive CRUD operations for competition management,
including creation, listing, updating, team registration, status management,
and statistics. Competitions organize teams within sports and provide the
framework for matches and betting.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, http_not_found, http_conflict
from core.keycloak_security import get_current_user_hybrid
from models import User, Competition, Sport
from api.schemas.competition import (
    CompetitionCreate,
    CompetitionUpdate,
    CompetitionResponse,
    CompetitionSummary,
    CompetitionWithStats,
    CompetitionWithSport,
    CompetitionTeamRegistration,
    CompetitionTeamList,
    CompetitionStatus,
    CompetitionFormat
)
from services.competition_service import CompetitionService


router = APIRouter()


def _transform_competition_to_summary(comp: Competition) -> dict:
    """Transform Competition model data to match CompetitionSummary schema expectations."""
    return {
        'id': comp.id,
        'name': comp.name,
        'format': comp.format_type,  # Map format_type to format
        'status': comp.status,
        'start_date': comp.start_date,
        'end_date': comp.end_date,
        'is_active': comp.status in ['active', 'upcoming', 'registration_open'],  # Derive is_active from status
        'is_public': comp.visibility == 'public',  # Map visibility to is_public
        'allow_betting': comp.allow_public_betting  # Map allow_public_betting to allow_betting
    }


@router.post(
    "/",
    response_model=CompetitionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Competition",
    description="Create a new competition with comprehensive validation"
)
async def create_competition(
    competition_data: CompetitionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> CompetitionResponse:
    """
    Create a new competition.
    
    Args:
        competition_data: Competition creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created competition details
        
    Raises:
        HTTPException: If sport not found or validation fails
    """
    service = CompetitionService(db)
    competition = service.create_competition(competition_data)
    return CompetitionResponse.model_validate(competition)


@router.get(
    "/",
    response_model=List[CompetitionSummary],
    summary="List Competitions",
    description="List competitions with comprehensive filtering options"
)
async def list_competitions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    sport_id: Optional[UUID] = Query(None, description="Filter by sport ID"),
    status: Optional[CompetitionStatus] = Query(None, description="Filter by status"),
    format: Optional[CompetitionFormat] = Query(None, description="Filter by format"),
    is_public: Optional[bool] = Query(None, description="Filter by public visibility"),
    allow_betting: Optional[bool] = Query(None, description="Filter by betting allowance"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db)
) -> List[CompetitionSummary]:
    """
    List competitions with filtering options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        sport_id: Filter by sport ID
        status: Filter by competition status
        format: Filter by competition format
        is_public: Filter by public visibility
        allow_betting: Filter by betting allowance
        search: Search text for name/description
        year: Filter by year
        db: Database session
        
    Returns:
        List of competition summaries
    """
    service = CompetitionService(db)
    competitions = service.list_competitions(
        skip=skip,
        limit=limit,
        sport_id=sport_id,
        status=status,
        format=format,
        is_public=is_public,
        allow_betting=allow_betting,
        search=search,
        year=year
    )
    
    # Transform Competition model data to match schema expectations
    return [CompetitionSummary.model_validate(_transform_competition_to_summary(comp)) for comp in competitions]


@router.get(
    "/active",
    response_model=List[CompetitionSummary],
    summary="List Active Competitions",
    description="Get all currently active competitions"
)
async def list_active_competitions(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[CompetitionSummary]:
    """
    Get all active competitions.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of active competition summaries
    """
    service = CompetitionService(db)
    competitions = service.get_active_competitions(limit=limit)
    return [CompetitionSummary.model_validate(_transform_competition_to_summary(comp)) for comp in competitions]


@router.get(
    "/public",
    response_model=List[CompetitionSummary],
    summary="List Public Competitions",
    description="Get all public competitions"
)
async def list_public_competitions(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[CompetitionSummary]:
    """
    Get all public competitions.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of public competition summaries
    """
    service = CompetitionService(db)
    competitions = service.get_public_competitions(limit=limit)
    return [CompetitionSummary.model_validate(_transform_competition_to_summary(comp)) for comp in competitions]


@router.get(
    "/{competition_id}",
    response_model=CompetitionResponse,
    summary="Get Competition",
    description="Get competition details by ID"
)
async def get_competition(
    competition_id: UUID,
    db: Session = Depends(get_db)
) -> CompetitionResponse:
    """
    Get competition by ID.
    
    Args:
        competition_id: Competition unique identifier
        db: Database session
        
    Returns:
        Competition details
        
    Raises:
        HTTPException: If competition not found
    """
    service = CompetitionService(db)
    competition = service.get_competition(competition_id)
    
    if not competition:
        raise http_not_found(f"Competition with ID {competition_id} not found")
        
    return CompetitionResponse.model_validate(competition)


@router.get(
    "/{competition_id}/stats",
    response_model=CompetitionWithStats,
    summary="Get Competition Statistics",
    description="Get comprehensive competition statistics"
)
async def get_competition_statistics(
    competition_id: UUID,
    db: Session = Depends(get_db)
) -> CompetitionWithStats:
    """
    Get competition statistics.
    
    Args:
        competition_id: Competition unique identifier
        db: Database session
        
    Returns:
        Competition details with statistics
        
    Raises:
        HTTPException: If competition not found
    """
    service = CompetitionService(db)
    competition = service.get_competition(competition_id)
    
    if not competition:
        raise http_not_found(f"Competition with ID {competition_id} not found")
        
    stats = service.get_competition_statistics(competition_id)
    
    # Create response with stats
    competition_dict = CompetitionResponse.model_validate(competition).model_dump()
    competition_dict['stats'] = stats
    
    return CompetitionWithStats.model_validate(competition_dict)


@router.get(
    "/{competition_id}/with-sport",
    response_model=CompetitionWithSport,
    summary="Get Competition with Sport",
    description="Get competition details including sport information"
)
async def get_competition_with_sport(
    competition_id: UUID,
    db: Session = Depends(get_db)
) -> CompetitionWithSport:
    """
    Get competition with sport details.
    
    Args:
        competition_id: Competition unique identifier
        db: Database session
        
    Returns:
        Competition details with sport information
        
    Raises:
        HTTPException: If competition not found
    """
    service = CompetitionService(db)
    competition = service.get_competition(competition_id)
    
    if not competition:
        raise http_not_found(f"Competition with ID {competition_id} not found")
    
    # Load sport relationship
    sport = db.query(Sport).filter(Sport.id == competition.sport_id).first()
    
    competition_dict = CompetitionResponse.model_validate(competition).model_dump()
    competition_dict['sport'] = sport
    
    return CompetitionWithSport.model_validate(competition_dict)


@router.get(
    "/sport/{sport_id}",
    response_model=List[CompetitionSummary],
    summary="List Competitions by Sport",
    description="Get all competitions for a specific sport"
)
async def list_competitions_by_sport(
    sport_id: UUID,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[CompetitionSummary]:
    """
    Get competitions by sport.
    
    Args:
        sport_id: Sport unique identifier
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of competitions for the sport
    """
    service = CompetitionService(db)
    competitions = service.get_competitions_by_sport(sport_id, limit=limit)
    return [CompetitionSummary.model_validate(_transform_competition_to_summary(comp)) for comp in competitions]


@router.get(
    "/name/{name}",
    response_model=CompetitionResponse,
    summary="Get Competition by Name",
    description="Find competition by exact name match"
)
async def get_competition_by_name(
    name: str,
    sport_id: Optional[UUID] = Query(None, description="Scope search to specific sport"),
    db: Session = Depends(get_db)
) -> CompetitionResponse:
    """
    Get competition by name.
    
    Args:
        name: Competition name
        sport_id: Optional sport ID to scope the search
        db: Database session
        
    Returns:
        Competition details
        
    Raises:
        HTTPException: If competition not found
    """
    service = CompetitionService(db)
    competition = service.get_competition_by_name(name, sport_id)
    
    if not competition:
        raise http_not_found(f"Competition '{name}' not found")
        
    return CompetitionResponse.model_validate(competition)


@router.put(
    "/{competition_id}",
    response_model=CompetitionResponse,
    summary="Update Competition",
    description="Update competition details with validation"
)
async def update_competition(
    competition_id: UUID,
    update_data: CompetitionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> CompetitionResponse:
    """
    Update competition.
    
    Args:
        competition_id: Competition unique identifier
        update_data: Updated competition data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated competition details
        
    Raises:
        HTTPException: If competition not found or validation fails
    """
    service = CompetitionService(db)
    competition = service.update_competition(competition_id, update_data)
    
    if not competition:
        raise http_not_found(f"Competition with ID {competition_id} not found")
        
    return CompetitionResponse.model_validate(competition)


@router.delete(
    "/{competition_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Competition",
    description="Soft delete competition (sets as inactive)"
)
async def delete_competition(
    competition_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> None:
    """
    Delete competition (soft delete).
    
    Args:
        competition_id: Competition unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If competition not found
    """
    service = CompetitionService(db)
    deleted = service.delete_competition(competition_id)
    
    if not deleted:
        raise http_not_found(f"Competition with ID {competition_id} not found")


@router.post(
    "/{competition_id}/status",
    response_model=CompetitionResponse,
    summary="Update Competition Status",
    description="Update competition status (active, completed, cancelled, etc.)"
)
async def update_competition_status(
    competition_id: UUID,
    status: CompetitionStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> CompetitionResponse:
    """
    Update competition status.
    
    Args:
        competition_id: Competition unique identifier
        status: New competition status
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated competition details
        
    Raises:
        HTTPException: If competition not found
    """
    service = CompetitionService(db)
    competition = service.update_status(competition_id, status)
    
    if not competition:
        raise http_not_found(f"Competition with ID {competition_id} not found")
        
    return CompetitionResponse.model_validate(competition)


@router.post(
    "/{competition_id}/register-team",
    status_code=status.HTTP_201_CREATED,
    summary="Register Team",
    description="Register a team for the competition"
)
async def register_team(
    competition_id: UUID,
    registration_data: CompetitionTeamRegistration,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> dict:
    """
    Register a team for the competition.
    
    Args:
        competition_id: Competition unique identifier
        registration_data: Team registration data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Registration success message
        
    Raises:
        HTTPException: If registration fails
    """
    service = CompetitionService(db)
    success = service.register_team(competition_id, registration_data.team_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team registration failed"
        )
        
    return {"message": "Team registered successfully"}


@router.delete(
    "/{competition_id}/unregister-team/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unregister Team",
    description="Unregister a team from the competition"
)
async def unregister_team(
    competition_id: UUID,
    team_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> None:
    """
    Unregister a team from the competition.
    
    Args:
        competition_id: Competition unique identifier
        team_id: Team unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If team not found in competition
    """
    service = CompetitionService(db)
    success = service.unregister_team(competition_id, team_id)
    
    if not success:
        raise http_not_found("Team not found in this competition")


@router.get(
    "/{competition_id}/teams",
    response_model=CompetitionTeamList,
    summary="Get Competition Teams",
    description="Get all teams registered for the competition"
)
async def get_competition_teams(
    competition_id: UUID,
    db: Session = Depends(get_db)
) -> CompetitionTeamList:
    """
    Get teams registered for a competition.
    
    Args:
        competition_id: Competition unique identifier
        db: Database session
        
    Returns:
        List of teams in the competition
        
    Raises:
        HTTPException: If competition not found
    """
    service = CompetitionService(db)
    competition = service.get_competition(competition_id)
    
    if not competition:
        raise http_not_found(f"Competition with ID {competition_id} not found")
        
    teams = service.get_competition_teams(competition_id)
    
    # Check if registration is still open
    from datetime import datetime
    registration_open = True
    if competition.registration_deadline:
        registration_open = datetime.now().date() <= competition.registration_deadline
        
    return CompetitionTeamList(
        competition_id=competition_id,
        teams=teams,
        total_teams=len(teams),
        max_teams=competition.max_teams,
        registration_open=registration_open
    )


@router.get(
    "/search/{query}",
    response_model=List[CompetitionSummary],
    summary="Search Competitions",
    description="Search competitions by name, description, or location"
)
async def search_competitions(
    query: str,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[CompetitionSummary]:
    """
    Search competitions.
    
    Args:
        query: Search query string
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of matching competitions
    """
    service = CompetitionService(db)
    competitions = service.search_competitions(query, limit=limit)
    return [CompetitionSummary.model_validate(_transform_competition_to_summary(comp)) for comp in competitions]
