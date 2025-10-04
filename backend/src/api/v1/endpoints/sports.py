"""
Sports API endpoints for the betting platform.

This module provides comprehensive CRUD operations for sports management,
including creation, listing, updating, activation/deactivation, and statistics.
Sports serve as the foundation for team and competition organization.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, get_current_user, http_not_found, http_conflict
from models import User, Sport
from api.schemas.sport import (
    SportCreate,
    SportUpdate,
    SportResponse,
    SportSummary,
    SportWithStats
)
from services.sport_service import SportService

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
from api.schemas.sport import (
    SportCreate,
    SportUpdate,
    SportResponse,
    SportSummary,
    SportWithStats
)
from services.sport_service import SportService

router = APIRouter()


@router.post(
    "",
    response_model=SportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new sport",
    description="Create a new sport (requires authentication)"
)
async def create_sport(
    sport_data: SportCreate,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> SportResponse:
    """Create a new sport."""
    try:
        sport = SportService.create_sport(db, sport_data)
        return SportResponse.from_orm(sport)
    except ValidationError as e:
        raise http_validation_error(str(e))


@router.get(
    "",
    response_model=PaginatedResponse[SportSummary],
    summary="List sports",
    description="Retrieve a paginated list of sports with optional filtering"
)
async def list_sports(
    pagination: PaginationParams = Depends(),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in name or description"),
    db: Session = Depends(get_db)
) -> PaginatedResponse[SportSummary]:
    """List sports with pagination and filtering."""
    query = SportService.build_sport_list_query(db, is_active, search)
    
    # Apply pagination
    paginated = paginate_query(query, db, pagination)
    
    # Convert to summary format
    paginated.items = [SportSummary.from_orm(sport) for sport in paginated.items]
    
    return paginated


@router.get(
    "/active",
    response_model=List[SportSummary],
    summary="Get active sports",
    description="Retrieve all active sports"
)
async def get_active_sports(
    db: Session = Depends(get_db)
) -> List[SportSummary]:
    """Get all active sports."""
    sports = SportService.get_active_sports(db)
    return [SportSummary.from_orm(sport) for sport in sports]


@router.get(
    "/{sport_id}",
    response_model=SportResponse,
    summary="Get sport by ID",
    description="Retrieve a specific sport by its ID"
)
async def get_sport(
    sport_id: UUID,
    db: Session = Depends(get_db)
) -> SportResponse:
    """Get sport by ID."""
    sport = SportService.get_sport_by_id(db, sport_id)
    if not sport:
        raise http_not_found("Sport", str(sport_id))
    
    return SportResponse.from_orm(sport)


@router.get(
    "/{sport_id}/stats",
    response_model=SportWithStats,
    summary="Get sport with statistics",
    description="Retrieve a sport with detailed statistics"
)
async def get_sport_with_stats(
    sport_id: UUID,
    db: Session = Depends(get_db)
) -> SportWithStats:
    """Get sport with statistics."""
    sport_with_stats = SportService.get_sport_with_stats(db, sport_id)
    if not sport_with_stats:
        raise http_not_found("Sport", str(sport_id))
    
    return sport_with_stats


@router.get(
    "/name/{name}",
    response_model=SportResponse,
    summary="Get sport by name",
    description="Retrieve a specific sport by its name"
)
async def get_sport_by_name(
    name: str,
    db: Session = Depends(get_db)
) -> SportResponse:
    """Get sport by name."""
    sport = SportService.get_sport_by_name(db, name)
    if not sport:
        raise http_not_found("Sport", name)
    
    return SportResponse.from_orm(sport)


@router.put(
    "/{sport_id}",
    response_model=SportResponse,
    summary="Update sport",
    description="Update sport information (requires authentication)"
)
async def update_sport(
    sport_id: UUID,
    sport_update: SportUpdate,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> SportResponse:
    """Update sport information."""
    try:
        updated_sport = SportService.update_sport(db, sport_id, sport_update)
        return SportResponse.from_orm(updated_sport)
    except NotFoundError as e:
        raise http_not_found("Sport", str(sport_id))
    except ValidationError as e:
        raise http_validation_error(str(e))


@router.delete(
    "/{sport_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete sport",
    description="Deactivate a sport (requires authentication)"
)
async def delete_sport(
    sport_id: UUID,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> None:
    """Delete (deactivate) sport."""
    try:
        SportService.delete_sport(db, sport_id)
    except NotFoundError as e:
        raise http_not_found("Sport", str(sport_id))


@router.post(
    "/{sport_id}/activate",
    response_model=SportResponse,
    summary="Activate sport",
    description="Activate a sport (requires authentication)"
)
async def activate_sport(
    sport_id: UUID,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> SportResponse:
    """Activate a sport."""
    try:
        sport = SportService.activate_sport(db, sport_id)
        return SportResponse.from_orm(sport)
    except NotFoundError as e:
        raise http_not_found("Sport", str(sport_id))


@router.post(
    "/{sport_id}/deactivate",
    response_model=SportResponse,
    summary="Deactivate sport",
    description="Deactivate a sport (requires authentication)"
)
async def deactivate_sport(
    sport_id: UUID,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id)  # Require authentication
) -> SportResponse:
    """Deactivate a sport."""
    try:
        sport = SportService.deactivate_sport(db, sport_id)
        return SportResponse.from_orm(sport)
    except NotFoundError as e:
        raise http_not_found("Sport", str(sport_id))
