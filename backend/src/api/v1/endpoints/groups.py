"""
Group API endpoints.

This module provides REST API endpoints for group management including
CRUD operations, membership management, and group statistics.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import (
    get_db,
    get_current_user,
    get_current_user_id,
    http_not_found,
    http_forbidden,
    http_conflict,
    http_validation_error,
    PaginationParams,
    PaginatedResponse,
    paginate_query,
    ValidationError,
    NotFoundError,
    PermissionError,
    ConflictError
)
from models.user import User
from models.group import PointSystem
from api.schemas.group import (
    GroupCreate,
    GroupUpdate,
    GroupResponse,
    GroupSummary,
    GroupWithStats
)
from services.group_service import GroupService

router = APIRouter()


@router.post(
    "",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new group",
    description="Create a new group with the authenticated user as creator"
)
async def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> GroupResponse:
    """Create a new group."""
    try:
        group = GroupService.create_group(db, group_data, current_user.id)
        return GroupResponse.from_orm(group)
    except ValidationError as e:
        raise http_validation_error(str(e))
    except NotFoundError as e:
        raise http_not_found("User", str(current_user.id))


@router.get(
    "",
    response_model=PaginatedResponse[GroupSummary],
    summary="List groups",
    description="Retrieve a paginated list of groups with optional filtering"
)
async def list_groups(
    pagination: PaginationParams = Depends(),
    is_private: Optional[bool] = Query(None, description="Filter by privacy setting"),
    point_system: Optional[PointSystem] = Query(None, description="Filter by point system"),
    search: Optional[str] = Query(None, description="Search in name or description"),
    my_groups: bool = Query(False, description="Show only groups I'm a member of"),
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> PaginatedResponse[GroupSummary]:
    """List groups with pagination and filtering."""
    query = GroupService.build_group_list_query(
        db, 
        is_private, 
        point_system, 
        search,
        current_user_id if my_groups else None
    )
    
    # Apply pagination
    paginated = paginate_query(query, db, pagination)
    
    # Convert to summary format and add member counts
    group_summaries = []
    for group in paginated.items:
        stats = GroupService.calculate_group_stats(db, group.id)
        summary = GroupSummary.from_orm(group)
        summary.member_count = stats["member_count"]
        group_summaries.append(summary)
    
    paginated.items = group_summaries
    return paginated


@router.get(
    "/{group_id}",
    response_model=GroupResponse,
    summary="Get group by ID",
    description="Retrieve a specific group by its ID"
)
async def get_group(
    group_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> GroupResponse:
    """Get group by ID."""
    # Check if user can view this group
    if not GroupService.can_user_view_group(db, current_user_id, group_id):
        raise http_forbidden("Insufficient permissions to view this group")
    
    group = GroupService.get_group_by_id(db, group_id)
    if not group:
        raise http_not_found("Group", str(group_id))
    
    return GroupResponse.from_orm(group)


@router.get(
    "/{group_id}/stats",
    response_model=GroupWithStats,
    summary="Get group with statistics",
    description="Retrieve a group with detailed statistics"
)
async def get_group_with_stats(
    group_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> GroupWithStats:
    """Get group with statistics."""
    # Check if user can view this group
    if not GroupService.can_user_view_group(db, current_user_id, group_id):
        raise http_forbidden("Insufficient permissions to view this group")
    
    group_with_stats = GroupService.get_group_with_stats(db, group_id)
    if not group_with_stats:
        raise http_not_found("Group", str(group_id))
    
    return group_with_stats


@router.get(
    "/name/{name}",
    response_model=GroupResponse,
    summary="Get group by name",
    description="Retrieve a specific group by its name"
)
async def get_group_by_name(
    name: str,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> GroupResponse:
    """Get group by name."""
    group = GroupService.get_group_by_name(db, name)
    if not group:
        raise http_not_found("Group", name)
    
    # Check if user can view this group
    if not GroupService.can_user_view_group(db, current_user_id, group.id):
        raise http_forbidden("Insufficient permissions to view this group")
    
    return GroupResponse.from_orm(group)


@router.put(
    "/{group_id}",
    response_model=GroupResponse,
    summary="Update group",
    description="Update group information (requires admin permissions)"
)
async def update_group(
    group_id: UUID,
    group_update: GroupUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> GroupResponse:
    """Update group information."""
    try:
        updated_group = GroupService.update_group(
            db, group_id, group_update, current_user.id
        )
        return GroupResponse.from_orm(updated_group)
    except NotFoundError as e:
        raise http_not_found("Group", str(group_id))
    except PermissionError as e:
        raise http_forbidden(str(e))
    except ValidationError as e:
        raise http_validation_error(str(e))


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete group",
    description="Delete a group (creator only)"
)
async def delete_group(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> None:
    """Delete group."""
    try:
        GroupService.delete_group(db, group_id, current_user.id)
    except NotFoundError as e:
        raise http_not_found("Group", str(group_id))
    except PermissionError as e:
        raise http_forbidden(str(e))


@router.post(
    "/{group_id}/join",
    response_model=dict,
    summary="Join group",
    description="Join a group as a member"
)
async def join_group(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """Join a group."""
    try:
        GroupService.join_group(db, group_id, current_user.id)
        return {"message": "Successfully joined the group"}
    except NotFoundError as e:
        raise http_not_found("Group", str(group_id))
    except ConflictError as e:
        raise http_conflict(str(e))


@router.post(
    "/{group_id}/leave",
    response_model=dict,
    summary="Leave group",
    description="Leave a group"
)
async def leave_group(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """Leave a group."""
    try:
        GroupService.leave_group(db, group_id, current_user.id)
        return {"message": "Successfully left the group"}
    except NotFoundError as e:
        raise http_not_found("Group or Membership", str(group_id))
    except ValidationError as e:
        raise http_validation_error(str(e))


@router.get(
    "/{group_id}/members",
    response_model=List[dict],
    summary="Get group members",
    description="Get list of group members (requires membership to view)"
)
async def get_group_members(
    group_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> List[dict]:
    """Get group members."""
    # Check if user can view this group
    if not GroupService.can_user_view_group(db, current_user_id, group_id):
        raise http_forbidden("Insufficient permissions to view group members")
    
    group = GroupService.get_group_by_id(db, group_id)
    if not group:
        raise http_not_found("Group", str(group_id))
    
    # For now, return placeholder
    # TODO: Implement full member list with GroupMembership service
    return [{"message": "Group members endpoint - full implementation coming soon"}]
