"""
Group Membership schemas for user-group relationships.

This module defines Pydantic schemas for managing group memberships,
including member roles, permissions, invitations, and group dynamics
for the betting platform's social features.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, field_validator, ConfigDict


class MembershipStatus(str, Enum):
    """Membership status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"
    LEFT = "left"


class MembershipRole(str, Enum):
    """Membership role enumeration."""
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    OWNER = "owner"


class InvitationType(str, Enum):
    """Invitation type enumeration."""
    DIRECT = "direct"
    LINK = "link"
    REQUEST = "request"


class GroupMembershipBase(BaseModel):
    """Base schema for group membership data."""
    
    user_id: UUID = Field(..., description="User unique identifier")
    group_id: UUID = Field(..., description="Group unique identifier")
    role: MembershipRole = Field(MembershipRole.MEMBER, description="Member role")
    status: MembershipStatus = Field(MembershipStatus.PENDING, description="Membership status")
    notes: Optional[str] = Field(None, max_length=500, description="Membership notes")


class GroupMembershipCreate(GroupMembershipBase):
    """Schema for creating a new group membership."""
    
    invited_by: Optional[UUID] = Field(None, description="User who invited this member")
    invitation_type: InvitationType = Field(InvitationType.DIRECT, description="Type of invitation")
    invitation_message: Optional[str] = Field(None, max_length=500, description="Invitation message")
    
    @field_validator('role')
    @classmethod
    def validate_role_on_create(cls, v):
        """Validate role on creation - only allow member role initially."""
        if v != MembershipRole.MEMBER:
            raise ValueError("New memberships can only be created with 'member' role")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "aa0e8400-e29b-41d4-a716-446655440000",
                "group_id": "bb0e8400-e29b-41d4-a716-446655440000",
                "role": "member",
                "status": "pending",
                "invited_by": "cc0e8400-e29b-41d4-a716-446655440000",
                "invitation_type": "direct",
                "invitation_message": "Welcome to our betting group!",
                "notes": "Invited by admin"
            }
        }
    )


class GroupMembershipUpdate(BaseModel):
    """Schema for updating group membership data."""
    
    role: Optional[MembershipRole] = Field(None, description="Updated member role")
    status: Optional[MembershipStatus] = Field(None, description="Updated membership status")
    notes: Optional[str] = Field(None, max_length=500, description="Updated membership notes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "moderator",
                "status": "active",
                "notes": "Promoted to moderator for excellent contributions"
            }
        }
    )


class GroupMembershipResponse(GroupMembershipBase):
    """Schema for group membership response data."""
    
    id: UUID = Field(..., description="Membership unique identifier")
    invited_by: Optional[UUID] = Field(None, description="User who invited this member")
    invitation_type: InvitationType = Field(..., description="Type of invitation")
    invitation_message: Optional[str] = Field(None, description="Invitation message")
    joined_at: datetime = Field(..., description="When membership was created")
    updated_at: Optional[datetime] = Field(None, description="When membership was last updated")
    approved_at: Optional[datetime] = Field(None, description="When membership was approved")
    approved_by: Optional[UUID] = Field(None, description="User who approved membership")
    
    model_config = ConfigDict(from_attributes=True)


class GroupMembershipSummary(BaseModel):
    """Schema for group membership summary data."""
    
    id: UUID = Field(..., description="Membership unique identifier")
    user_id: UUID = Field(..., description="User unique identifier")
    group_id: UUID = Field(..., description="Group unique identifier")
    role: MembershipRole = Field(..., description="Member role")
    status: MembershipStatus = Field(..., description="Membership status")
    joined_at: datetime = Field(..., description="When membership was created")
    
    model_config = ConfigDict(from_attributes=True)


class GroupMembershipWithUser(GroupMembershipResponse):
    """Schema for group membership with user information."""
    
    user: Optional[Dict[str, Any]] = Field(None, description="User details")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "dd0e8400-e29b-41d4-a716-446655440000",
                "user_id": "aa0e8400-e29b-41d4-a716-446655440000",
                "group_id": "bb0e8400-e29b-41d4-a716-446655440000",
                "role": "member",
                "status": "active",
                "joined_at": "2025-10-05T14:30:00Z",
                "user": {
                    "id": "aa0e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "display_name": "John Doe",
                    "profile_picture_url": "https://example.com/avatar.jpg"
                }
            }
        }
    )


class GroupMembershipWithGroup(GroupMembershipResponse):
    """Schema for group membership with group information."""
    
    group: Optional[Dict[str, Any]] = Field(None, description="Group details")
    
    model_config = ConfigDict(from_attributes=True)


class GroupMembershipWithDetails(GroupMembershipResponse):
    """Schema for group membership with full details."""
    
    user: Optional[Dict[str, Any]] = Field(None, description="User details")
    group: Optional[Dict[str, Any]] = Field(None, description="Group details")
    invited_by_user: Optional[Dict[str, Any]] = Field(None, description="User who sent invitation")
    approved_by_user: Optional[Dict[str, Any]] = Field(None, description="User who approved membership")
    
    model_config = ConfigDict(from_attributes=True)


class GroupInvitation(BaseModel):
    """Schema for group invitation."""
    
    group_id: UUID = Field(..., description="Group unique identifier")
    email: Optional[str] = Field(None, description="Email to invite (for non-users)")
    user_id: Optional[UUID] = Field(None, description="User ID to invite (for existing users)")
    role: MembershipRole = Field(MembershipRole.MEMBER, description="Role to assign")
    invitation_message: Optional[str] = Field(None, max_length=500, description="Invitation message")
    expires_at: Optional[datetime] = Field(None, description="When invitation expires")
    
    @field_validator('email', 'user_id')
    @classmethod
    def validate_invite_target(cls, v, info):
        """Validate that either email or user_id is provided."""
        values = info.data
        email = values.get('email')
        user_id = values.get('user_id')
        
        if not email and not user_id:
            raise ValueError("Either email or user_id must be provided")
        if email and user_id:
            raise ValueError("Cannot provide both email and user_id")
        
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_id": "bb0e8400-e29b-41d4-a716-446655440000",
                "email": "newuser@example.com",
                "role": "member",
                "invitation_message": "Join our betting group for weekly competitions!",
                "expires_at": "2025-10-12T14:30:00Z"
            }
        }
    )


class GroupJoinRequest(BaseModel):
    """Schema for group join request."""
    
    group_id: UUID = Field(..., description="Group unique identifier")
    message: Optional[str] = Field(None, max_length=500, description="Join request message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_id": "bb0e8400-e29b-41d4-a716-446655440000",
                "message": "I'd like to join your betting group. I'm an experienced bettor."
            }
        }
    )


class MembershipApproval(BaseModel):
    """Schema for membership approval/rejection."""
    
    approved: bool = Field(..., description="Whether to approve the membership")
    role: Optional[MembershipRole] = Field(None, description="Role to assign if approved")
    notes: Optional[str] = Field(None, max_length=500, description="Approval/rejection notes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "approved": True,
                "role": "member",
                "notes": "Welcome to the group!"
            }
        }
    )


class MembershipRoleUpdate(BaseModel):
    """Schema for updating member role."""
    
    role: MembershipRole = Field(..., description="New role to assign")
    reason: Optional[str] = Field(None, max_length=500, description="Reason for role change")
    
    @field_validator('role')
    @classmethod
    def validate_role_change(cls, v):
        """Validate role change - owner role requires special handling."""
        if v == MembershipRole.OWNER:
            raise ValueError("Owner role can only be transferred, not assigned directly")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "moderator",
                "reason": "Promoted for excellent group management"
            }
        }
    )


class OwnershipTransfer(BaseModel):
    """Schema for transferring group ownership."""
    
    new_owner_id: UUID = Field(..., description="User to transfer ownership to")
    confirmation: str = Field(..., description="Confirmation phrase")
    reason: Optional[str] = Field(None, max_length=500, description="Reason for transfer")
    
    @field_validator('confirmation')
    @classmethod
    def validate_confirmation(cls, v):
        """Validate confirmation phrase."""
        if v != "TRANSFER_OWNERSHIP":
            raise ValueError("Must provide exact confirmation phrase 'TRANSFER_OWNERSHIP'")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "new_owner_id": "aa0e8400-e29b-41d4-a716-446655440000",
                "confirmation": "TRANSFER_OWNERSHIP",
                "reason": "Stepping down from group leadership"
            }
        }
    )


class GroupMembershipStatistics(BaseModel):
    """Schema for group membership statistics."""
    
    group_id: UUID = Field(..., description="Group unique identifier")
    total_members: int = Field(..., description="Total number of members")
    active_members: int = Field(..., description="Number of active members")
    pending_members: int = Field(..., description="Number of pending members")
    suspended_members: int = Field(..., description="Number of suspended members")
    role_distribution: Dict[str, int] = Field(..., description="Distribution of roles")
    recent_joins: int = Field(..., description="New members in last 30 days")
    recent_departures: int = Field(..., description="Members who left in last 30 days")
    average_membership_duration: Optional[float] = Field(None, description="Average membership duration in days")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "group_id": "bb0e8400-e29b-41d4-a716-446655440000",
                "total_members": 25,
                "active_members": 23,
                "pending_members": 2,
                "suspended_members": 0,
                "role_distribution": {
                    "owner": 1,
                    "admin": 2,
                    "moderator": 3,
                    "member": 19
                },
                "recent_joins": 5,
                "recent_departures": 1,
                "average_membership_duration": 156.5
            }
        }
    )


class GroupMembershipHistory(BaseModel):
    """Schema for membership history tracking."""
    
    membership_id: UUID = Field(..., description="Membership unique identifier")
    changes: List[Dict[str, Any]] = Field(..., description="List of changes made")
    total_updates: int = Field(..., description="Total number of updates")
    created_at: datetime = Field(..., description="When membership was created")
    last_updated: Optional[datetime] = Field(None, description="When last updated")
    
    model_config = ConfigDict(from_attributes=True)


class GroupMembershipBulkCreate(BaseModel):
    """Schema for bulk membership creation."""
    
    group_id: UUID = Field(..., description="Group unique identifier")
    memberships: List[Dict[str, Any]] = Field(..., description="List of memberships to create")
    send_invitations: bool = Field(True, description="Whether to send invitation emails")
    default_role: MembershipRole = Field(MembershipRole.MEMBER, description="Default role for new members")
    
    @field_validator('memberships')
    @classmethod
    def validate_memberships_count(cls, v):
        """Validate memberships count."""
        if len(v) == 0:
            raise ValueError("At least one membership must be provided")
        if len(v) > 50:
            raise ValueError("Maximum 50 memberships can be created at once")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_id": "bb0e8400-e29b-41d4-a716-446655440000",
                "memberships": [
                    {"email": "user1@example.com", "role": "member"},
                    {"user_id": "aa0e8400-e29b-41d4-a716-446655440000", "role": "member"}
                ],
                "send_invitations": True,
                "default_role": "member"
            }
        }
    )


class GroupMembershipBulkResponse(BaseModel):
    """Schema for bulk membership creation response."""
    
    created_count: int = Field(..., description="Number of memberships created")
    invited_count: int = Field(..., description="Number of invitations sent")
    error_count: int = Field(..., description="Number of errors encountered")
    created_memberships: List[UUID] = Field(..., description="IDs of created memberships")
    errors: List[Dict[str, Any]] = Field(default_factory=list, description="List of errors encountered")
    
    model_config = ConfigDict(from_attributes=True)


class GroupLeaveRequest(BaseModel):
    """Schema for leaving a group."""
    
    reason: Optional[str] = Field(None, max_length=500, description="Reason for leaving")
    transfer_ownership: bool = Field(False, description="Whether to transfer ownership (for owners)")
    new_owner_id: Optional[UUID] = Field(None, description="New owner if transferring ownership")
    
    @field_validator('new_owner_id')
    @classmethod
    def validate_ownership_transfer(cls, v, info):
        """Validate ownership transfer requirements."""
        values = info.data
        transfer_ownership = values.get('transfer_ownership', False)
        
        if transfer_ownership and not v:
            raise ValueError("new_owner_id is required when transfer_ownership is True")
        if not transfer_ownership and v:
            raise ValueError("Cannot specify new_owner_id when transfer_ownership is False")
        
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "reason": "Moving to a different betting focus",
                "transfer_ownership": False
            }
        }
    )


class GroupMembershipFilters(BaseModel):
    """Schema for membership filtering options."""
    
    status: Optional[MembershipStatus] = Field(None, description="Filter by membership status")
    role: Optional[MembershipRole] = Field(None, description="Filter by member role")
    joined_after: Optional[datetime] = Field(None, description="Filter members who joined after this date")
    joined_before: Optional[datetime] = Field(None, description="Filter members who joined before this date")
    invited_by: Optional[UUID] = Field(None, description="Filter by who invited the member")
    search_term: Optional[str] = Field(None, description="Search in user names and emails")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "active",
                "role": "member",
                "joined_after": "2025-09-01T00:00:00Z",
                "search_term": "john"
            }
        }
    )


# Export all schemas
__all__ = [
    "MembershipStatus",
    "MembershipRole",
    "InvitationType",
    "GroupMembershipBase",
    "GroupMembershipCreate",
    "GroupMembershipUpdate",
    "GroupMembershipResponse",
    "GroupMembershipSummary",
    "GroupMembershipWithUser",
    "GroupMembershipWithGroup",
    "GroupMembershipWithDetails",
    "GroupInvitation",
    "GroupJoinRequest",
    "MembershipApproval",
    "MembershipRoleUpdate",
    "OwnershipTransfer",
    "GroupMembershipStatistics",
    "GroupMembershipHistory",
    "GroupMembershipBulkCreate",
    "GroupMembershipBulkResponse",
    "GroupLeaveRequest",
    "GroupMembershipFilters"
]