"""
Teams API endpoints for the betting platform.

This module provides comprehensive CRUD operations for team management,
including creation, listing, updating, activation/deactivation, sport association,
and location-based filtering. Teams are associated with sports and participate in competitions.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, get_current_user, http_not_found, http_conflict
from models import User, Team, Sport
from api.schemas.team import (
    TeamCreate,
    TeamUpdate,
    TeamResponse,
    TeamSummary,
    TeamWithStats,
    TeamWithSport
)
from services.team_service import TeamService

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import (
    get_db,
    get_current_user_id,
    http_not_found,
    http_validation_error,
    PaginationParams,
    PaginatedResponse,
    paginate_query,
    ValidationError,
    NotFoundError
)
from api.schemas.team import (
    TeamCreate,
    TeamUpdate,
    TeamResponse,
    TeamSummary,
    TeamWithStats,
    TeamWithSport
)
from services.team_service import TeamService

router = APIRouter()


@router.post(
    "",
    response_model=TeamResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new team",
    description="Create a new team (requires authentication)"
)
async def create_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> TeamResponse:
    """Create a new team."""
    try:
        team = TeamService.create_team(db, team_data)
        return TeamResponse.from_orm(team)
    except ValidationError as e:
        raise http_validation_error(str(e))
    except NotFoundError as e:
        raise http_not_found("Sport", str(team_data.sport_id))


@router.get(
    "",
    response_model=PaginatedResponse[TeamSummary],
    summary="List teams",
    description="Retrieve a paginated list of teams with optional filtering"
)
async def list_teams(
    pagination: PaginationParams = Depends(),
    sport_id: Optional[UUID] = Query(None, description="Filter by sport"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    country: Optional[str] = Query(None, description="Filter by country"),
    search: Optional[str] = Query(None, description="Search in name, short name, city, or country"),
    db: Session = Depends(get_db)
) -> PaginatedResponse[TeamSummary]:
    """List teams with pagination and filtering."""
    query = TeamService.build_team_list_query(db, sport_id, is_active, country, search)
    
    # Apply pagination
    paginated = paginate_query(query, db, pagination)
    
    # Convert to summary format
    paginated.items = [TeamSummary.from_orm(team) for team in paginated.items]
    
    return paginated


@router.get(
    "/{team_id}",
    response_model=TeamResponse,
    summary="Get team by ID",
    description="Retrieve a specific team by its ID"
)
async def get_team(
    team_id: UUID,
    db: Session = Depends(get_db)
) -> TeamResponse:
    """Get team by ID."""
    team = TeamService.get_team_by_id(db, team_id)
    if not team:
        raise http_not_found("Team", str(team_id))
    
    return TeamResponse.from_orm(team)


@router.get(
    "/{team_id}/stats",
    response_model=TeamWithStats,
    summary="Get team with statistics",
    description="Retrieve a team with detailed statistics"
)
async def get_team_with_stats(
    team_id: UUID,
    db: Session = Depends(get_db)
) -> TeamWithStats:
    """Get team with statistics."""
    team_with_stats = TeamService.get_team_with_stats(db, team_id)
    if not team_with_stats:
        raise http_not_found("Team", str(team_id))
    
    return team_with_stats


@router.get(
    "/{team_id}/with-sport",
    response_model=TeamWithSport,
    summary="Get team with sport info",
    description="Retrieve a team with sport information"
)
async def get_team_with_sport(
    team_id: UUID,
    db: Session = Depends(get_db)
) -> TeamWithSport:
    """Get team with sport information."""
    team_with_sport = TeamService.get_team_with_sport(db, team_id)
    if not team_with_sport:
        raise http_not_found("Team", str(team_id))
    
    return team_with_sport


@router.get(
    "/sport/{sport_id}",
    response_model=List[TeamSummary],
    summary="Get teams by sport",
    description="Retrieve all teams for a specific sport"
)
async def get_teams_by_sport(
    sport_id: UUID,
    active_only: bool = Query(True, description="Only return active teams"),
    db: Session = Depends(get_db)
) -> List[TeamSummary]:
    """Get teams by sport."""
    teams = TeamService.get_teams_by_sport(db, sport_id, active_only)
    return [TeamSummary.from_orm(team) for team in teams]


@router.get(
    "/name/{name}",
    response_model=TeamResponse,
    summary="Get team by name",
    description="Retrieve a specific team by its name"
)
async def get_team_by_name(
    name: str,
    sport_id: Optional[UUID] = Query(None, description="Filter by sport"),
    db: Session = Depends(get_db)
) -> TeamResponse:
    """Get team by name."""
    team = TeamService.get_team_by_name(db, name, sport_id)
    if not team:
        raise http_not_found("Team", name)
    
    return TeamResponse.from_orm(team)


@router.put(
    "/{team_id}",
    response_model=TeamResponse,
    summary="Update team",
    description="Update team information (requires authentication)"
)
async def update_team(
    team_id: UUID,
    team_update: TeamUpdate,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> TeamResponse:
    """Update team information."""
    try:
        updated_team = TeamService.update_team(db, team_id, team_update)
        return TeamResponse.from_orm(updated_team)
    except NotFoundError as e:
        raise http_not_found("Team", str(team_id))
    except ValidationError as e:
        raise http_validation_error(str(e))


@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete team",
    description="Deactivate a team (requires authentication)"
)
async def delete_team(
    team_id: UUID,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> None:
    """Delete (deactivate) team."""
    try:
        TeamService.delete_team(db, team_id)
    except NotFoundError as e:
        raise http_not_found("Team", str(team_id))


@router.post(
    "/{team_id}/activate",
    response_model=TeamResponse,
    summary="Activate team",
    description="Activate a team (requires authentication)"
)
async def activate_team(
    team_id: UUID,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> TeamResponse:
    """Activate a team."""
    try:
        team = TeamService.activate_team(db, team_id)
        return TeamResponse.from_orm(team)
    except NotFoundError as e:
        raise http_not_found("Team", str(team_id))


@router.post(
    "/{team_id}/deactivate",
    response_model=TeamResponse,
    summary="Deactivate team",
    description="Deactivate a team (requires authentication)"
)
async def deactivate_team(
    team_id: UUID,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> TeamResponse:
    """Deactivate a team."""
    try:
        team = TeamService.deactivate_team(db, team_id)
        return TeamResponse.from_orm(team)
    except NotFoundError as e:
        raise http_not_found("Team", str(team_id))
