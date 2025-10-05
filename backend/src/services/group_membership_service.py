"""
Group Membership service for managing user-group relationships.

This service provides comprehensive business logic for handling group memberships,
including invitations, approvals, role management, and group dynamics for the
betting platform's social features.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID

from sqlalchemy import and_, or_, desc, asc, func, case
from sqlalchemy.orm import Session, joinedload

from models import GroupMembership, User, Group
from api.schemas.group_membership import (
    GroupMembershipCreate,
    GroupMembershipUpdate,
    GroupInvitation,
    GroupJoinRequest,
    MembershipApproval,
    MembershipRoleUpdate,
    OwnershipTransfer,
    GroupMembershipStatistics,
    GroupMembershipBulkCreate,
    GroupLeaveRequest,
    GroupMembershipFilters,
    MembershipStatus,
    MembershipRole,
    InvitationType
)


class GroupMembershipService:
    """Service for managing group memberships and relationships."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_membership(self, membership_data: GroupMembershipCreate, current_user_id: UUID) -> GroupMembership:
        """
        Create a new group membership.
        
        Args:
            membership_data: Membership creation data
            current_user_id: ID of user creating the membership
            
        Returns:
            Created membership
            
        Raises:
            ValueError: If validation fails
        """
        # Validate user exists
        user = self.db.query(User).filter(User.id == membership_data.user_id).first()
        if not user:
            raise ValueError(f"User with ID {membership_data.user_id} not found")
        
        # Validate group exists
        group = self.db.query(Group).filter(Group.id == membership_data.group_id).first()
        if not group:
            raise ValueError(f"Group with ID {membership_data.group_id} not found")
        
        # Check if membership already exists
        existing_membership = self.db.query(GroupMembership).filter(
            and_(
                GroupMembership.user_id == membership_data.user_id,
                GroupMembership.group_id == membership_data.group_id
            )
        ).first()
        
        if existing_membership:
            if existing_membership.status in [MembershipStatus.ACTIVE, MembershipStatus.PENDING]:
                raise ValueError("User is already a member or has a pending membership")
            elif existing_membership.status in [MembershipStatus.BANNED]:
                raise ValueError("User is banned from this group")
        
        # Validate inviter permissions if specified
        if membership_data.invited_by:
            inviter_membership = self._get_user_membership(membership_data.invited_by, membership_data.group_id)
            if not inviter_membership or inviter_membership.status != MembershipStatus.ACTIVE:
                raise ValueError("Inviter is not an active member of the group")
            
            if inviter_membership.role not in [MembershipRole.ADMIN, MembershipRole.MODERATOR, MembershipRole.OWNER]:
                raise ValueError("Inviter does not have permission to invite members")
        
        # Create membership
        db_membership = GroupMembership(
            user_id=membership_data.user_id,
            group_id=membership_data.group_id,
            role=membership_data.role,
            status=membership_data.status,
            invited_by=membership_data.invited_by,
            invitation_type=membership_data.invitation_type,
            invitation_message=membership_data.invitation_message,
            notes=membership_data.notes,
            joined_at=datetime.utcnow()
        )
        
        self.db.add(db_membership)
        self.db.commit()
        self.db.refresh(db_membership)
        
        return db_membership
    
    def get_membership(self, membership_id: UUID) -> Optional[GroupMembership]:
        """Get membership by ID."""
        return self.db.query(GroupMembership).filter(GroupMembership.id == membership_id).first()
    
    def get_user_membership(self, user_id: UUID, group_id: UUID) -> Optional[GroupMembership]:
        """Get user's membership in a specific group."""
        return self._get_user_membership(user_id, group_id)
    
    def _get_user_membership(self, user_id: UUID, group_id: UUID) -> Optional[GroupMembership]:
        """Internal method to get user's membership."""
        return self.db.query(GroupMembership).filter(
            and_(
                GroupMembership.user_id == user_id,
                GroupMembership.group_id == group_id
            )
        ).first()
    
    def list_memberships(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[UUID] = None,
        group_id: Optional[UUID] = None,
        status: Optional[MembershipStatus] = None,
        role: Optional[MembershipRole] = None,
        invited_by: Optional[UUID] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> List[GroupMembership]:
        """
        List memberships with filtering options.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            user_id: Filter by user ID
            group_id: Filter by group ID
            status: Filter by membership status
            role: Filter by member role
            invited_by: Filter by who invited the member
            date_from: Filter memberships from this date
            date_to: Filter memberships until this date
            
        Returns:
            List of memberships
        """
        query = self.db.query(GroupMembership)
        
        # Apply filters
        if user_id:
            query = query.filter(GroupMembership.user_id == user_id)
        
        if group_id:
            query = query.filter(GroupMembership.group_id == group_id)
        
        if status:
            query = query.filter(GroupMembership.status == status)
        
        if role:
            query = query.filter(GroupMembership.role == role)
        
        if invited_by:
            query = query.filter(GroupMembership.invited_by == invited_by)
        
        if date_from:
            query = query.filter(GroupMembership.joined_at >= date_from)
        
        if date_to:
            query = query.filter(GroupMembership.joined_at <= date_to)
        
        # Order by join date (newest first)
        query = query.order_by(desc(GroupMembership.joined_at))
        
        return query.offset(skip).limit(limit).all()
    
    def get_group_members(self, group_id: UUID, active_only: bool = True) -> List[GroupMembership]:
        """Get all members of a group."""
        query = self.db.query(GroupMembership).filter(GroupMembership.group_id == group_id)
        
        if active_only:
            query = query.filter(GroupMembership.status == MembershipStatus.ACTIVE)
        
        return query.order_by(desc(GroupMembership.joined_at)).all()
    
    def get_user_groups(self, user_id: UUID, active_only: bool = True) -> List[GroupMembership]:
        """Get all groups a user is a member of."""
        query = self.db.query(GroupMembership).filter(GroupMembership.user_id == user_id)
        
        if active_only:
            query = query.filter(GroupMembership.status == MembershipStatus.ACTIVE)
        
        return query.order_by(desc(GroupMembership.joined_at)).all()
    
    def update_membership(self, membership_id: UUID, update_data: GroupMembershipUpdate, current_user_id: UUID) -> Optional[GroupMembership]:
        """
        Update membership data.
        
        Args:
            membership_id: Membership unique identifier
            update_data: Updated membership data
            current_user_id: ID of user making the update
            
        Returns:
            Updated membership or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        membership = self.get_membership(membership_id)
        if not membership:
            return None
        
        # Check permissions
        current_user_membership = self._get_user_membership(current_user_id, membership.group_id)
        if not self._can_modify_membership(current_user_membership, membership, current_user_id):
            raise ValueError("Insufficient permissions to update this membership")
        
        # Update fields
        if update_data.role is not None:
            # Validate role update permissions
            if not self._can_update_role(current_user_membership, membership.role, update_data.role):
                raise ValueError("Insufficient permissions to assign this role")
            membership.role = update_data.role
        
        if update_data.status is not None:
            membership.status = update_data.status
            
            # Set approval fields if status is being set to active
            if update_data.status == MembershipStatus.ACTIVE and membership.status != MembershipStatus.ACTIVE:
                membership.approved_at = datetime.utcnow()
                membership.approved_by = current_user_id
        
        if update_data.notes is not None:
            membership.notes = update_data.notes
        
        membership.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(membership)
        
        return membership
    
    def approve_membership(self, membership_id: UUID, approval: MembershipApproval, current_user_id: UUID) -> Optional[GroupMembership]:
        """
        Approve or reject a membership.
        
        Args:
            membership_id: Membership unique identifier
            approval: Approval data
            current_user_id: ID of user making the approval
            
        Returns:
            Updated membership or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        membership = self.get_membership(membership_id)
        if not membership:
            return None
        
        if membership.status != MembershipStatus.PENDING:
            raise ValueError("Can only approve pending memberships")
        
        # Check permissions
        current_user_membership = self._get_user_membership(current_user_id, membership.group_id)
        if not current_user_membership or current_user_membership.role not in [MembershipRole.ADMIN, MembershipRole.MODERATOR, MembershipRole.OWNER]:
            raise ValueError("Insufficient permissions to approve memberships")
        
        if approval.approved:
            membership.status = MembershipStatus.ACTIVE
            if approval.role:
                membership.role = approval.role
            membership.approved_at = datetime.utcnow()
            membership.approved_by = current_user_id
        else:
            membership.status = MembershipStatus.LEFT
        
        if approval.notes:
            membership.notes = approval.notes
        
        membership.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(membership)
        
        return membership
    
    def update_member_role(self, membership_id: UUID, role_update: MembershipRoleUpdate, current_user_id: UUID) -> Optional[GroupMembership]:
        """
        Update a member's role.
        
        Args:
            membership_id: Membership unique identifier
            role_update: Role update data
            current_user_id: ID of user making the update
            
        Returns:
            Updated membership or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        membership = self.get_membership(membership_id)
        if not membership:
            return None
        
        # Check permissions
        current_user_membership = self._get_user_membership(current_user_id, membership.group_id)
        if not self._can_update_role(current_user_membership, membership.role, role_update.role):
            raise ValueError("Insufficient permissions to assign this role")
        
        old_role = membership.role
        membership.role = role_update.role
        membership.updated_at = datetime.utcnow()
        
        # Add note about role change
        role_change_note = f"Role changed from {old_role} to {role_update.role}"
        if role_update.reason:
            role_change_note += f". Reason: {role_update.reason}"
        
        if membership.notes:
            membership.notes += f"\n{role_change_note}"
        else:
            membership.notes = role_change_note
        
        self.db.commit()
        self.db.refresh(membership)
        
        return membership
    
    def transfer_ownership(self, group_id: UUID, transfer: OwnershipTransfer, current_user_id: UUID) -> Tuple[GroupMembership, GroupMembership]:
        """
        Transfer group ownership.
        
        Args:
            group_id: Group unique identifier
            transfer: Ownership transfer data
            current_user_id: ID of current owner
            
        Returns:
            Tuple of (old_owner_membership, new_owner_membership)
            
        Raises:
            ValueError: If validation fails
        """
        # Validate current user is owner
        current_owner_membership = self._get_user_membership(current_user_id, group_id)
        if not current_owner_membership or current_owner_membership.role != MembershipRole.OWNER:
            raise ValueError("Only group owners can transfer ownership")
        
        # Validate new owner exists and is a member
        new_owner_membership = self._get_user_membership(transfer.new_owner_id, group_id)
        if not new_owner_membership:
            raise ValueError("New owner must be a member of the group")
        
        if new_owner_membership.status != MembershipStatus.ACTIVE:
            raise ValueError("New owner must be an active member")
        
        # Transfer ownership
        current_owner_membership.role = MembershipRole.ADMIN
        new_owner_membership.role = MembershipRole.OWNER
        
        now = datetime.utcnow()
        current_owner_membership.updated_at = now
        new_owner_membership.updated_at = now
        
        # Add notes
        transfer_note = f"Ownership transferred. Reason: {transfer.reason or 'No reason provided'}"
        
        if current_owner_membership.notes:
            current_owner_membership.notes += f"\n{transfer_note}"
        else:
            current_owner_membership.notes = transfer_note
        
        if new_owner_membership.notes:
            new_owner_membership.notes += f"\nReceived ownership transfer"
        else:
            new_owner_membership.notes = "Received ownership transfer"
        
        self.db.commit()
        self.db.refresh(current_owner_membership)
        self.db.refresh(new_owner_membership)
        
        return current_owner_membership, new_owner_membership
    
    def leave_group(self, group_id: UUID, leave_request: GroupLeaveRequest, current_user_id: UUID) -> Optional[GroupMembership]:
        """
        Leave a group.
        
        Args:
            group_id: Group unique identifier
            leave_request: Leave request data
            current_user_id: ID of user leaving
            
        Returns:
            Updated membership or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        membership = self._get_user_membership(current_user_id, group_id)
        if not membership:
            raise ValueError("User is not a member of this group")
        
        if membership.status != MembershipStatus.ACTIVE:
            raise ValueError("Can only leave as an active member")
        
        # Handle ownership transfer if user is owner
        if membership.role == MembershipRole.OWNER:
            if not leave_request.transfer_ownership:
                raise ValueError("Group owners must transfer ownership before leaving")
            
            if not leave_request.new_owner_id:
                raise ValueError("Must specify new owner when transferring ownership")
            
            # Transfer ownership first
            transfer = OwnershipTransfer(
                new_owner_id=leave_request.new_owner_id,
                confirmation="TRANSFER_OWNERSHIP",
                reason=f"Ownership transfer due to leaving group. {leave_request.reason or ''}"
            )
            self.transfer_ownership(group_id, transfer, current_user_id)
        
        # Update membership status
        membership.status = MembershipStatus.LEFT
        membership.updated_at = datetime.utcnow()
        
        if leave_request.reason:
            leave_note = f"Left group. Reason: {leave_request.reason}"
            if membership.notes:
                membership.notes += f"\n{leave_note}"
            else:
                membership.notes = leave_note
        
        self.db.commit()
        self.db.refresh(membership)
        
        return membership
    
    def get_membership_statistics(self, group_id: UUID) -> GroupMembershipStatistics:
        """
        Get membership statistics for a group.
        
        Args:
            group_id: Group unique identifier
            
        Returns:
            Group membership statistics
        """
        # Get all memberships for the group
        memberships = self.db.query(GroupMembership).filter(GroupMembership.group_id == group_id).all()
        
        total_members = len(memberships)
        active_members = sum(1 for m in memberships if m.status == MembershipStatus.ACTIVE)
        pending_members = sum(1 for m in memberships if m.status == MembershipStatus.PENDING)
        suspended_members = sum(1 for m in memberships if m.status == MembershipStatus.SUSPENDED)
        
        # Role distribution (only active members)
        active_memberships = [m for m in memberships if m.status == MembershipStatus.ACTIVE]
        role_distribution = {}
        for role in MembershipRole:
            role_distribution[role.value] = sum(1 for m in active_memberships if m.role == role)
        
        # Recent activity
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_joins = sum(1 for m in memberships if m.joined_at >= thirty_days_ago)
        recent_departures = sum(1 for m in memberships if m.status == MembershipStatus.LEFT and m.updated_at and m.updated_at >= thirty_days_ago)
        
        # Average membership duration
        completed_memberships = [m for m in memberships if m.status == MembershipStatus.LEFT and m.updated_at]
        if completed_memberships:
            durations = [(m.updated_at - m.joined_at).days for m in completed_memberships]
            average_duration = sum(durations) / len(durations)
        else:
            average_duration = None
        
        return GroupMembershipStatistics(
            group_id=group_id,
            total_members=total_members,
            active_members=active_members,
            pending_members=pending_members,
            suspended_members=suspended_members,
            role_distribution=role_distribution,
            recent_joins=recent_joins,
            recent_departures=recent_departures,
            average_membership_duration=average_duration
        )
    
    def invite_user(self, invitation: GroupInvitation, current_user_id: UUID) -> GroupMembership:
        """
        Invite a user to join a group.
        
        Args:
            invitation: Invitation data
            current_user_id: ID of user sending invitation
            
        Returns:
            Created membership
            
        Raises:
            ValueError: If validation fails
        """
        # Check permissions
        current_user_membership = self._get_user_membership(current_user_id, invitation.group_id)
        if not current_user_membership or current_user_membership.role not in [MembershipRole.ADMIN, MembershipRole.MODERATOR, MembershipRole.OWNER]:
            raise ValueError("Insufficient permissions to invite members")
        
        # If inviting by user_id, create membership directly
        if invitation.user_id:
            membership_data = GroupMembershipCreate(
                user_id=invitation.user_id,
                group_id=invitation.group_id,
                role=invitation.role,
                status=MembershipStatus.PENDING,
                invited_by=current_user_id,
                invitation_type=InvitationType.DIRECT,
                invitation_message=invitation.invitation_message
            )
            return self.create_membership(membership_data, current_user_id)
        
        # If inviting by email, check if user exists
        elif invitation.email:
            user = self.db.query(User).filter(User.email == invitation.email).first()
            if user:
                membership_data = GroupMembershipCreate(
                    user_id=user.id,
                    group_id=invitation.group_id,
                    role=invitation.role,
                    status=MembershipStatus.PENDING,
                    invited_by=current_user_id,
                    invitation_type=InvitationType.DIRECT,
                    invitation_message=invitation.invitation_message
                )
                return self.create_membership(membership_data, current_user_id)
            else:
                # TODO: Create invitation record for non-existing user
                # For now, raise an error
                raise ValueError("Cannot invite non-existing users. User must register first.")
    
    def request_to_join(self, join_request: GroupJoinRequest, current_user_id: UUID) -> GroupMembership:
        """
        Request to join a group.
        
        Args:
            join_request: Join request data
            current_user_id: ID of user requesting to join
            
        Returns:
            Created membership
            
        Raises:
            ValueError: If validation fails
        """
        membership_data = GroupMembershipCreate(
            user_id=current_user_id,
            group_id=join_request.group_id,
            role=MembershipRole.MEMBER,
            status=MembershipStatus.PENDING,
            invitation_type=InvitationType.REQUEST,
            invitation_message=join_request.message
        )
        return self.create_membership(membership_data, current_user_id)
    
    def bulk_create_memberships(self, bulk_data: GroupMembershipBulkCreate, current_user_id: UUID) -> Dict[str, Any]:
        """
        Create multiple memberships in bulk.
        
        Args:
            bulk_data: Bulk creation data
            current_user_id: ID of user creating memberships
            
        Returns:
            Bulk creation summary
        """
        # Check permissions
        current_user_membership = self._get_user_membership(current_user_id, bulk_data.group_id)
        if not current_user_membership or current_user_membership.role not in [MembershipRole.ADMIN, MembershipRole.MODERATOR, MembershipRole.OWNER]:
            raise ValueError("Insufficient permissions to bulk create memberships")
        
        created_memberships = []
        invited_count = 0
        errors = []
        
        for i, membership_info in enumerate(bulk_data.memberships):
            try:
                # Handle different invitation types
                if 'user_id' in membership_info:
                    membership_data = GroupMembershipCreate(
                        user_id=UUID(membership_info['user_id']),
                        group_id=bulk_data.group_id,
                        role=membership_info.get('role', bulk_data.default_role),
                        status=MembershipStatus.PENDING,
                        invited_by=current_user_id,
                        invitation_type=InvitationType.DIRECT
                    )
                    membership = self.create_membership(membership_data, current_user_id)
                    created_memberships.append(membership.id)
                    
                elif 'email' in membership_info:
                    # Check if user exists
                    user = self.db.query(User).filter(User.email == membership_info['email']).first()
                    if user:
                        membership_data = GroupMembershipCreate(
                            user_id=user.id,
                            group_id=bulk_data.group_id,
                            role=membership_info.get('role', bulk_data.default_role),
                            status=MembershipStatus.PENDING,
                            invited_by=current_user_id,
                            invitation_type=InvitationType.DIRECT
                        )
                        membership = self.create_membership(membership_data, current_user_id)
                        created_memberships.append(membership.id)
                        
                        if bulk_data.send_invitations:
                            invited_count += 1
                    else:
                        errors.append({
                            "index": i,
                            "email": membership_info['email'],
                            "error": "User not found"
                        })
                else:
                    errors.append({
                        "index": i,
                        "error": "Must provide either user_id or email"
                    })
                    
            except Exception as e:
                errors.append({
                    "index": i,
                    "error": str(e)
                })
        
        return {
            "created_count": len(created_memberships),
            "invited_count": invited_count,
            "error_count": len(errors),
            "created_memberships": created_memberships,
            "errors": errors
        }
    
    def delete_membership(self, membership_id: UUID, current_user_id: UUID) -> bool:
        """
        Delete a membership.
        
        Args:
            membership_id: Membership unique identifier
            current_user_id: ID of user deleting membership
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If membership cannot be deleted
        """
        membership = self.get_membership(membership_id)
        if not membership:
            return False
        
        # Check permissions
        current_user_membership = self._get_user_membership(current_user_id, membership.group_id)
        if not self._can_modify_membership(current_user_membership, membership, current_user_id):
            raise ValueError("Insufficient permissions to delete this membership")
        
        # Cannot delete owner membership without transferring ownership
        if membership.role == MembershipRole.OWNER:
            raise ValueError("Cannot delete owner membership. Transfer ownership first.")
        
        self.db.delete(membership)
        self.db.commit()
        return True
    
    def search_memberships(self, filters: GroupMembershipFilters, skip: int = 0, limit: int = 100) -> List[GroupMembership]:
        """
        Search memberships with advanced filtering.
        
        Args:
            filters: Search filters
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching memberships
        """
        query = self.db.query(GroupMembership)
        
        # Apply filters
        if filters.status:
            query = query.filter(GroupMembership.status == filters.status)
        
        if filters.role:
            query = query.filter(GroupMembership.role == filters.role)
        
        if filters.joined_after:
            query = query.filter(GroupMembership.joined_at >= filters.joined_after)
        
        if filters.joined_before:
            query = query.filter(GroupMembership.joined_at <= filters.joined_before)
        
        if filters.invited_by:
            query = query.filter(GroupMembership.invited_by == filters.invited_by)
        
        if filters.search_term:
            # Join with User to search in user details
            query = query.join(User).filter(
                or_(
                    User.display_name.ilike(f"%{filters.search_term}%"),
                    User.email.ilike(f"%{filters.search_term}%")
                )
            )
        
        return query.order_by(desc(GroupMembership.joined_at)).offset(skip).limit(limit).all()
    
    def _can_modify_membership(self, current_user_membership: Optional[GroupMembership], target_membership: GroupMembership, current_user_id: UUID) -> bool:
        """Check if current user can modify target membership."""
        # Users can modify their own membership (limited actions)
        if target_membership.user_id == current_user_id:
            return True
        
        # Must be a member with appropriate role
        if not current_user_membership or current_user_membership.status != MembershipStatus.ACTIVE:
            return False
        
        # Role hierarchy check
        user_role_level = self._get_role_level(current_user_membership.role)
        target_role_level = self._get_role_level(target_membership.role)
        
        return user_role_level > target_role_level
    
    def _can_update_role(self, current_user_membership: Optional[GroupMembership], current_role: MembershipRole, new_role: MembershipRole) -> bool:
        """Check if current user can update role."""
        if not current_user_membership or current_user_membership.status != MembershipStatus.ACTIVE:
            return False
        
        user_role_level = self._get_role_level(current_user_membership.role)
        current_role_level = self._get_role_level(current_role)
        new_role_level = self._get_role_level(new_role)
        
        # Must be able to modify current role and assign new role
        return user_role_level > current_role_level and user_role_level > new_role_level
    
    def _get_role_level(self, role: MembershipRole) -> int:
        """Get numeric level for role hierarchy."""
        role_levels = {
            MembershipRole.MEMBER: 1,
            MembershipRole.MODERATOR: 2,
            MembershipRole.ADMIN: 3,
            MembershipRole.OWNER: 4
        }
        return role_levels.get(role, 0)