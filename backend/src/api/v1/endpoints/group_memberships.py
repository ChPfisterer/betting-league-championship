"""
Group Membership API endpoints for user-group relationships.

This module provides comprehensive CRUD operations for group membership management,
including invitations, approvals, role management, and group dynamics for the
betting platform's social features.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, http_not_found, http_conflict
from core.keycloak_security import get_current_user_hybrid
from models import User, GroupMembership, Group
from api.schemas.group_membership import (
    GroupMembershipCreate,
    GroupMembershipUpdate,
    GroupMembershipResponse,
    GroupMembershipSummary,
    GroupMembershipWithUser,
    GroupMembershipWithGroup,
    GroupMembershipWithDetails,
    GroupInvitation,
    GroupJoinRequest,
    MembershipApproval,
    MembershipRoleUpdate,
    OwnershipTransfer,
    GroupMembershipStatistics,
    GroupMembershipBulkCreate,
    GroupMembershipBulkResponse,
    GroupLeaveRequest,
    GroupMembershipFilters,
    MembershipStatus,
    MembershipRole,
    InvitationType
)
from services.group_membership_service import GroupMembershipService


router = APIRouter()


@router.post(
    "/",
    response_model=GroupMembershipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Membership",
    description="Create a new group membership with comprehensive validation"
)
async def create_membership(
    membership_data: GroupMembershipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipResponse:
    """
    Create a new group membership.
    
    Args:
        membership_data: Membership creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created membership details
        
    Raises:
        HTTPException: If validation fails
    """
    service = GroupMembershipService(db)
    try:
        membership = service.create_membership(membership_data, current_user.id)
        return GroupMembershipResponse.model_validate(membership)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=List[GroupMembershipSummary],
    summary="List Memberships",
    description="List memberships with comprehensive filtering options"
)
async def list_memberships(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
    group_id: Optional[UUID] = Query(None, description="Filter by group ID"),
    status: Optional[MembershipStatus] = Query(None, description="Filter by membership status"),
    role: Optional[MembershipRole] = Query(None, description="Filter by member role"),
    invited_by: Optional[UUID] = Query(None, description="Filter by who invited the member"),
    date_from: Optional[datetime] = Query(None, description="Filter memberships from this date"),
    date_to: Optional[datetime] = Query(None, description="Filter memberships until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[GroupMembershipSummary]:
    """
    List memberships with filtering options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        user_id: Filter by user ID
        group_id: Filter by group ID
        status: Filter by membership status
        role: Filter by member role
        invited_by: Filter by who invited the member
        date_from: Filter memberships from this date
        date_to: Filter memberships until this date
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of membership summaries
    """
    service = GroupMembershipService(db)
    memberships = service.list_memberships(
        skip=skip,
        limit=limit,
        user_id=user_id,
        group_id=group_id,
        status=status,
        role=role,
        invited_by=invited_by,
        date_from=date_from,
        date_to=date_to
    )
    return [GroupMembershipSummary.model_validate(membership) for membership in memberships]


@router.get(
    "/my-groups",
    response_model=List[GroupMembershipSummary],
    summary="Get My Groups",
    description="Get all groups the current user is a member of"
)
async def get_my_groups(
    active_only: bool = Query(True, description="Include only active memberships"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[GroupMembershipSummary]:
    """
    Get current user's group memberships.
    
    Args:
        active_only: Include only active memberships
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of user's group memberships
    """
    service = GroupMembershipService(db)
    memberships = service.get_user_groups(current_user.id, active_only=active_only)
    return [GroupMembershipSummary.model_validate(membership) for membership in memberships]


@router.get(
    "/{membership_id}",
    response_model=GroupMembershipResponse,
    summary="Get Membership",
    description="Get membership details by ID"
)
async def get_membership(
    membership_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipResponse:
    """
    Get membership by ID.
    
    Args:
        membership_id: Membership unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Membership details
        
    Raises:
        HTTPException: If membership not found
    """
    service = GroupMembershipService(db)
    membership = service.get_membership(membership_id)
    
    if not membership:
        raise http_not_found(f"Membership with ID {membership_id} not found")
        
    return GroupMembershipResponse.model_validate(membership)


@router.get(
    "/{membership_id}/with-user",
    response_model=GroupMembershipWithUser,
    summary="Get Membership with User",
    description="Get membership details including user information"
)
async def get_membership_with_user(
    membership_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipWithUser:
    """
    Get membership with user details.
    
    Args:
        membership_id: Membership unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Membership details with user information
        
    Raises:
        HTTPException: If membership not found
    """
    service = GroupMembershipService(db)
    membership = service.get_membership(membership_id)
    
    if not membership:
        raise http_not_found(f"Membership with ID {membership_id} not found")
    
    # Load user relationship
    user = db.query(User).filter(User.id == membership.user_id).first()
    
    membership_dict = GroupMembershipResponse.model_validate(membership).model_dump()
    membership_dict['user'] = user
    
    return GroupMembershipWithUser.model_validate(membership_dict)


@router.get(
    "/group/{group_id}/members",
    response_model=List[GroupMembershipWithUser],
    summary="Get Group Members",
    description="Get all members of a specific group"
)
async def get_group_members(
    group_id: UUID,
    active_only: bool = Query(True, description="Include only active members"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[GroupMembershipWithUser]:
    """
    Get group members.
    
    Args:
        group_id: Group unique identifier
        active_only: Include only active members
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of group members with user information
    """
    service = GroupMembershipService(db)
    memberships = service.get_group_members(group_id, active_only=active_only)
    
    result = []
    for membership in memberships:
        user = db.query(User).filter(User.id == membership.user_id).first()
        membership_dict = GroupMembershipResponse.model_validate(membership).model_dump()
        membership_dict['user'] = user
        result.append(GroupMembershipWithUser.model_validate(membership_dict))
    
    return result


@router.get(
    "/user/{user_id}/groups",
    response_model=List[GroupMembershipWithGroup],
    summary="Get User Groups",
    description="Get all groups a specific user is a member of"
)
async def get_user_groups(
    user_id: UUID,
    active_only: bool = Query(True, description="Include only active memberships"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[GroupMembershipWithGroup]:
    """
    Get user's group memberships.
    
    Args:
        user_id: User unique identifier
        active_only: Include only active memberships
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of user's groups with group information
    """
    service = GroupMembershipService(db)
    memberships = service.get_user_groups(user_id, active_only=active_only)
    
    result = []
    for membership in memberships:
        group = db.query(Group).filter(Group.id == membership.group_id).first()
        membership_dict = GroupMembershipResponse.model_validate(membership).model_dump()
        membership_dict['group'] = group
        result.append(GroupMembershipWithGroup.model_validate(membership_dict))
    
    return result


@router.get(
    "/group/{group_id}/statistics",
    response_model=GroupMembershipStatistics,
    summary="Get Group Statistics",
    description="Get comprehensive membership statistics for a group"
)
async def get_group_statistics(
    group_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipStatistics:
    """
    Get group membership statistics.
    
    Args:
        group_id: Group unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Group membership statistics
    """
    service = GroupMembershipService(db)
    return service.get_membership_statistics(group_id)


@router.put(
    "/{membership_id}",
    response_model=GroupMembershipResponse,
    summary="Update Membership",
    description="Update membership data"
)
async def update_membership(
    membership_id: UUID,
    update_data: GroupMembershipUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipResponse:
    """
    Update membership.
    
    Args:
        membership_id: Membership unique identifier
        update_data: Updated membership data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated membership details
        
    Raises:
        HTTPException: If membership not found or cannot be updated
    """
    service = GroupMembershipService(db)
    try:
        membership = service.update_membership(membership_id, update_data, current_user.id)
        if not membership:
            raise http_not_found(f"Membership with ID {membership_id} not found")
        return GroupMembershipResponse.model_validate(membership)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{membership_id}/approve",
    response_model=GroupMembershipResponse,
    summary="Approve Membership",
    description="Approve or reject a pending membership"
)
async def approve_membership(
    membership_id: UUID,
    approval: MembershipApproval,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipResponse:
    """
    Approve or reject membership.
    
    Args:
        membership_id: Membership unique identifier
        approval: Approval data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated membership details
        
    Raises:
        HTTPException: If membership not found or cannot be approved
    """
    service = GroupMembershipService(db)
    try:
        membership = service.approve_membership(membership_id, approval, current_user.id)
        if not membership:
            raise http_not_found(f"Membership with ID {membership_id} not found")
        return GroupMembershipResponse.model_validate(membership)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{membership_id}/role",
    response_model=GroupMembershipResponse,
    summary="Update Member Role",
    description="Update a member's role in the group"
)
async def update_member_role(
    membership_id: UUID,
    role_update: MembershipRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipResponse:
    """
    Update member role.
    
    Args:
        membership_id: Membership unique identifier
        role_update: Role update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated membership details
        
    Raises:
        HTTPException: If membership not found or role cannot be updated
    """
    service = GroupMembershipService(db)
    try:
        membership = service.update_member_role(membership_id, role_update, current_user.id)
        if not membership:
            raise http_not_found(f"Membership with ID {membership_id} not found")
        return GroupMembershipResponse.model_validate(membership)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/group/{group_id}/transfer-ownership",
    response_model=dict,
    summary="Transfer Group Ownership",
    description="Transfer ownership of a group to another member"
)
async def transfer_ownership(
    group_id: UUID,
    transfer: OwnershipTransfer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> dict:
    """
    Transfer group ownership.
    
    Args:
        group_id: Group unique identifier
        transfer: Ownership transfer data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Transfer summary
        
    Raises:
        HTTPException: If transfer cannot be completed
    """
    service = GroupMembershipService(db)
    try:
        old_owner, new_owner = service.transfer_ownership(group_id, transfer, current_user.id)
        return {
            "message": "Ownership transferred successfully",
            "old_owner_id": str(old_owner.user_id),
            "new_owner_id": str(new_owner.user_id),
            "transferred_at": datetime.utcnow().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/invite",
    response_model=GroupMembershipResponse,
    summary="Invite User",
    description="Invite a user to join a group"
)
async def invite_user(
    invitation: GroupInvitation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipResponse:
    """
    Invite user to group.
    
    Args:
        invitation: Invitation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created membership/invitation
        
    Raises:
        HTTPException: If invitation cannot be sent
    """
    service = GroupMembershipService(db)
    try:
        membership = service.invite_user(invitation, current_user.id)
        return GroupMembershipResponse.model_validate(membership)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/request-join",
    response_model=GroupMembershipResponse,
    summary="Request to Join",
    description="Request to join a group"
)
async def request_to_join(
    join_request: GroupJoinRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipResponse:
    """
    Request to join group.
    
    Args:
        join_request: Join request data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created membership request
        
    Raises:
        HTTPException: If request cannot be created
    """
    service = GroupMembershipService(db)
    try:
        membership = service.request_to_join(join_request, current_user.id)
        return GroupMembershipResponse.model_validate(membership)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/group/{group_id}/leave",
    response_model=GroupMembershipResponse,
    summary="Leave Group",
    description="Leave a group (with ownership transfer if needed)"
)
async def leave_group(
    group_id: UUID,
    leave_request: GroupLeaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipResponse:
    """
    Leave group.
    
    Args:
        group_id: Group unique identifier
        leave_request: Leave request data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated membership details
        
    Raises:
        HTTPException: If cannot leave group
    """
    service = GroupMembershipService(db)
    try:
        membership = service.leave_group(group_id, leave_request, current_user.id)
        if not membership:
            raise http_not_found(f"User is not a member of group {group_id}")
        return GroupMembershipResponse.model_validate(membership)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/bulk",
    response_model=GroupMembershipBulkResponse,
    summary="Bulk Create Memberships",
    description="Create multiple memberships in a single operation"
)
async def bulk_create_memberships(
    bulk_data: GroupMembershipBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> GroupMembershipBulkResponse:
    """
    Create multiple memberships in bulk.
    
    Args:
        bulk_data: Bulk creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Bulk creation summary
    """
    service = GroupMembershipService(db)
    try:
        result = service.bulk_create_memberships(bulk_data, current_user.id)
        return GroupMembershipBulkResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{membership_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Membership",
    description="Delete a membership (with restrictions)"
)
async def delete_membership(
    membership_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> None:
    """
    Delete membership.
    
    Args:
        membership_id: Membership unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If membership not found or cannot be deleted
    """
    service = GroupMembershipService(db)
    try:
        deleted = service.delete_membership(membership_id, current_user.id)
        if not deleted:
            raise http_not_found(f"Membership with ID {membership_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/search",
    response_model=List[GroupMembershipSummary],
    summary="Search Memberships",
    description="Search memberships with advanced filtering"
)
async def search_memberships(
    filters: GroupMembershipFilters,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[GroupMembershipSummary]:
    """
    Search memberships with advanced filtering.
    
    Args:
        filters: Search filters
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of matching memberships
    """
    service = GroupMembershipService(db)
    memberships = service.search_memberships(filters, skip=skip, limit=limit)
    return [GroupMembershipSummary.model_validate(membership) for membership in memberships]
