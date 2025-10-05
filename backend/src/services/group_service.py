"""
Group service layer.

Business logic for group management including CRUD operations,
membership management, and group statistics.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session

from core import ValidationError, NotFoundError, PermissionError, ConflictError
from models.group import Group, PointSystem
from models.group_membership import GroupMembership, MembershipRole, MembershipStatus
from models.user import User
from api.schemas.group import GroupCreate, GroupUpdate, GroupWithStats


class GroupService:
    """Service class for group operations."""
    
    @staticmethod
    def create_group(db: Session, group_data: GroupCreate, creator_id: UUID) -> Group:
        """
        Create a new group.
        
        Args:
            db: Database session
            group_data: Group creation data
            creator_id: ID of the user creating the group
            
        Returns:
            Group: Created group
            
        Raises:
            ValidationError: If group name already exists or validation fails
            NotFoundError: If creator not found
        """
        # Verify creator exists
        creator = db.query(User).filter(User.id == creator_id).first()
        if not creator:
            raise NotFoundError(f"User with ID {creator_id} not found")
        
        # Check if group name already exists
        existing_group = db.query(Group).filter(
            Group.name == group_data.name
        ).first()
        if existing_group:
            raise ValidationError(f"Group name '{group_data.name}' already exists")
        
        # Create new group
        group = Group(
            name=group_data.name,
            description=group_data.description,
            is_private=group_data.is_private,
            max_members=group_data.max_members,
            allow_member_invites=group_data.allow_member_invites,
            auto_approve_members=group_data.auto_approve_members,
            point_system=group_data.point_system.value,
            avatar_url=group_data.avatar_url,
            banner_url=group_data.banner_url,
            rules_text=group_data.rules_text,
            entry_fee=group_data.entry_fee,
            creator_id=creator_id
        )
        
        db.add(group)
        db.flush()  # Get the group ID
        
        # Add creator as admin member
        membership = GroupMembership(
            group_id=group.id,
            user_id=creator_id,
            role=MembershipRole.CREATOR,
            status=MembershipStatus.ACTIVE
        )
        
        db.add(membership)
        db.commit()
        db.refresh(group)
        
        return group
    
    @staticmethod
    def get_group_by_id(db: Session, group_id: UUID) -> Optional[Group]:
        """Get group by ID."""
        return db.query(Group).filter(Group.id == group_id).first()
    
    @staticmethod
    def get_group_by_name(db: Session, name: str) -> Optional[Group]:
        """Get group by name."""
        return db.query(Group).filter(Group.name == name).first()
    
    @staticmethod
    def update_group(
        db: Session, 
        group_id: UUID, 
        group_data: GroupUpdate, 
        user_id: UUID
    ) -> Group:
        """
        Update group information.
        
        Args:
            db: Database session
            group_id: Group ID to update
            group_data: Update data
            user_id: ID of user making the update
            
        Returns:
            Group: Updated group
            
        Raises:
            NotFoundError: If group not found
            PermissionError: If user doesn't have permission
            ValidationError: If name already exists
        """
        group = GroupService.get_group_by_id(db, group_id)
        if not group:
            raise NotFoundError(f"Group with ID {group_id} not found")
        
        # Check if user has permission to update
        if not GroupService.can_user_manage_group(db, user_id, group_id):
            raise PermissionError("Insufficient permissions to update group")
        
        # Check name uniqueness if name is being updated
        if group_data.name and group_data.name != group.name:
            existing_group = db.query(Group).filter(
                and_(Group.name == group_data.name, Group.id != group_id)
            ).first()
            if existing_group:
                raise ValidationError(f"Group name '{group_data.name}' already exists")
        
        # Update fields
        if group_data.name is not None:
            group.name = group_data.name
        if group_data.description is not None:
            group.description = group_data.description
        if group_data.is_private is not None:
            group.is_private = group_data.is_private
        if group_data.max_members is not None:
            group.max_members = group_data.max_members
        if group_data.allow_member_invites is not None:
            group.allow_member_invites = group_data.allow_member_invites
        if group_data.auto_approve_members is not None:
            group.auto_approve_members = group_data.auto_approve_members
        if group_data.point_system is not None:
            group.point_system = group_data.point_system.value
        if group_data.avatar_url is not None:
            group.avatar_url = group_data.avatar_url
        if group_data.banner_url is not None:
            group.banner_url = group_data.banner_url
        if group_data.rules_text is not None:
            group.rules_text = group_data.rules_text
        if group_data.entry_fee is not None:
            group.entry_fee = group_data.entry_fee
        
        group.touch()  # Update timestamp
        
        db.commit()
        db.refresh(group)
        
        return group
    
    @staticmethod
    def delete_group(db: Session, group_id: UUID, user_id: UUID) -> None:
        """
        Delete group.
        
        Args:
            db: Database session
            group_id: Group ID to delete
            user_id: ID of user making the deletion
            
        Raises:
            NotFoundError: If group not found
            PermissionError: If user doesn't have permission
        """
        group = GroupService.get_group_by_id(db, group_id)
        if not group:
            raise NotFoundError(f"Group with ID {group_id} not found")
        
        # Only creator can delete group
        if group.creator_id != user_id:
            raise PermissionError("Only group creator can delete the group")
        
        # Remove all memberships first
        db.query(GroupMembership).filter(
            GroupMembership.group_id == group_id
        ).delete()
        
        # Delete the group
        db.delete(group)
        db.commit()
    
    @staticmethod
    def get_group_with_stats(db: Session, group_id: UUID) -> Optional[GroupWithStats]:
        """
        Get group with statistics.
        
        Args:
            db: Database session
            group_id: Group ID
            
        Returns:
            Optional[GroupWithStats]: Group with stats or None
        """
        group = GroupService.get_group_by_id(db, group_id)
        if not group:
            return None
        
        # Calculate statistics
        stats = GroupService.calculate_group_stats(db, group_id)
        
        return GroupWithStats(
            id=group.id,
            name=group.name,
            description=group.description,
            group_type=group.group_type,
            visibility=group.visibility,
            max_members=group.max_members,
            creator_id=group.creator_id,
            created_at=group.created_at,
            updated_at=group.updated_at,
            member_count=stats["member_count"],
            total_bets=stats["total_bets"],
            active_bets=stats["active_bets"],
            total_winnings=stats["total_winnings"]
        )
    
    @staticmethod
    def calculate_group_stats(db: Session, group_id: UUID) -> dict:
        """
        Calculate group statistics.
        
        Args:
            db: Database session
            group_id: Group ID
            
        Returns:
            dict: Group statistics
        """
        # Member count
        member_count = db.query(func.count(GroupMembership.id)).filter(
            and_(
                GroupMembership.group_id == group_id,
                GroupMembership.status == MembershipStatus.ACTIVE
            )
        ).scalar() or 0
        
        # For now, return basic stats (bet stats would require Bet model integration)
        return {
            "member_count": member_count,
            "total_bets": 0,  # TODO: Calculate from Bet model
            "active_bets": 0,  # TODO: Calculate from Bet model
            "total_winnings": 0.0  # TODO: Calculate from Bet model
        }
    
    @staticmethod
    def build_group_list_query(
        db: Session,
        is_private: Optional[bool] = None,
        point_system: Optional[PointSystem] = None,
        search: Optional[str] = None,
        user_id: Optional[UUID] = None
    ):
        """
        Build query for group list with filters.
        
        Args:
            db: Database session
            is_private: Filter by privacy setting
            point_system: Filter by point system
            search: Search term
            user_id: Filter by user membership
            
        Returns:
            Query: SQLAlchemy query
        """
        query = db.query(Group)
        
        # Filter by privacy
        if is_private is not None:
            query = query.filter(Group.is_private == is_private)
        
        # Filter by point system
        if point_system:
            query = query.filter(Group.point_system == point_system.value)
        
        # Search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Group.name.ilike(search_term),
                    Group.description.ilike(search_term)
                )
            )
        
        # Filter by user membership
        if user_id:
            query = query.join(GroupMembership).filter(
                and_(
                    GroupMembership.user_id == user_id,
                    GroupMembership.status == MembershipStatus.ACTIVE
                )
            )
        
        return query.order_by(Group.name)
    
    @staticmethod
    def can_user_view_group(db: Session, user_id: UUID, group_id: UUID) -> bool:
        """
        Check if user can view group.
        
        Args:
            db: Database session
            user_id: User ID
            group_id: Group ID
            
        Returns:
            bool: True if user can view group
        """
        group = GroupService.get_group_by_id(db, group_id)
        if not group:
            return False
        
        # Public groups can be viewed by anyone
        if not group.is_private:
            return True
        
        # Private groups require membership
        if group.is_private:
            membership = db.query(GroupMembership).filter(
                and_(
                    GroupMembership.group_id == group_id,
                    GroupMembership.user_id == user_id,
                    GroupMembership.status == MembershipStatus.ACTIVE
                )
            ).first()
            return membership is not None
        
        return False
    
    @staticmethod
    def can_user_manage_group(db: Session, user_id: UUID, group_id: UUID) -> bool:
        """
        Check if user can manage group (update/delete).
        
        Args:
            db: Database session
            user_id: User ID
            group_id: Group ID
            
        Returns:
            bool: True if user can manage group
        """
        group = GroupService.get_group_by_id(db, group_id)
        if not group:
            return False
        
        # Creator can always manage
        if group.creator_id == user_id:
            return True
        
        # Check if user is admin
        membership = db.query(GroupMembership).filter(
            and_(
                GroupMembership.group_id == group_id,
                GroupMembership.user_id == user_id,
                GroupMembership.status == MembershipStatus.ACTIVE,
                GroupMembership.role.in_([MembershipRole.ADMIN, MembershipRole.MODERATOR])
            )
        ).first()
        
        return membership is not None
    
    @staticmethod
    def join_group(db: Session, group_id: UUID, user_id: UUID) -> GroupMembership:
        """
        Join a group.
        
        Args:
            db: Database session
            group_id: Group ID
            user_id: User ID
            
        Returns:
            GroupMembership: Created membership
            
        Raises:
            NotFoundError: If group or user not found
            ConflictError: If already a member or group is full
        """
        group = GroupService.get_group_by_id(db, group_id)
        if not group:
            raise NotFoundError(f"Group with ID {group_id} not found")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Check if already a member
        existing_membership = db.query(GroupMembership).filter(
            and_(
                GroupMembership.group_id == group_id,
                GroupMembership.user_id == user_id
            )
        ).first()
        
        if existing_membership:
            if existing_membership.status == MembershipStatus.ACTIVE:
                raise ConflictError("User is already a member of this group")
            elif existing_membership.status == MembershipStatus.BANNED:
                raise ConflictError("User is banned from this group")
        
        # Check group capacity
        if group.max_members:
            current_members = db.query(func.count(GroupMembership.id)).filter(
                and_(
                    GroupMembership.group_id == group_id,
                    GroupMembership.status == MembershipStatus.ACTIVE
                )
            ).scalar() or 0
            
            if current_members >= group.max_members:
                raise ConflictError("Group has reached maximum capacity")
        
        # Create or reactivate membership
        if existing_membership:
            existing_membership.status = MembershipStatus.ACTIVE
            existing_membership.role = MembershipRole.MEMBER
            existing_membership.touch()
            membership = existing_membership
        else:
            membership = GroupMembership(
                group_id=group_id,
                user_id=user_id,
                role=MembershipRole.MEMBER,
                status=MembershipStatus.ACTIVE
            )
            db.add(membership)
        
        db.commit()
        db.refresh(membership)
        
        return membership
    
    @staticmethod
    def leave_group(db: Session, group_id: UUID, user_id: UUID) -> None:
        """
        Leave a group.
        
        Args:
            db: Database session
            group_id: Group ID
            user_id: User ID
            
        Raises:
            NotFoundError: If group or membership not found
            ValidationError: If trying to leave as creator
        """
        group = GroupService.get_group_by_id(db, group_id)
        if not group:
            raise NotFoundError(f"Group with ID {group_id} not found")
        
        # Creator cannot leave their own group
        if group.creator_id == user_id:
            raise ValidationError("Group creator cannot leave the group")
        
        membership = db.query(GroupMembership).filter(
            and_(
                GroupMembership.group_id == group_id,
                GroupMembership.user_id == user_id,
                GroupMembership.status == MembershipStatus.ACTIVE
            )
        ).first()
        
        if not membership:
            raise NotFoundError("User is not a member of this group")
        
        # Remove membership
        db.delete(membership)
        db.commit()