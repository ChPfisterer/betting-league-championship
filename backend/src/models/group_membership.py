"""
GroupMembership model for the betting league championship application.

This module defines the GroupMembership model with comprehensive user role management,
permission tracking, and membership lifecycle as specified by the TDD tests
in backend/tests/models/test_group_membership_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, CheckConstraint, 
    Index, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone
from typing import Union, Optional, Dict, Any
import uuid
from enum import Enum

from .base import Base


class MembershipRole(Enum):
    """Valid membership role values."""
    CREATOR = "creator"
    ADMIN = "admin" 
    MODERATOR = "moderator"
    MEMBER = "member"


class MembershipStatus(Enum):
    """Valid membership status values."""
    ACTIVE = "active"
    PENDING = "pending"
    INVITED = "invited"
    BANNED = "banned"
    LEFT = "left"


class GroupMembership(Base):
    """
    GroupMembership model for comprehensive user role and permission management.
    
    Handles user participation in groups with role-based permissions,
    invitation tracking, ban management, and membership lifecycle.
    """
    
    __tablename__ = 'group_memberships'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the membership"
    )
    
    # Foreign keys
    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey('groups.id', name='fk_group_memberships_group_id'),
        nullable=False,
        comment="ID of the group"
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', name='fk_group_memberships_user_id'),
        nullable=False,
        comment="ID of the user"
    )
    
    # Role and status
    role = Column(
        String(20),
        nullable=False,
        default=MembershipRole.MEMBER.value,
        comment="Role of the user in the group"
    )
    status = Column(
        String(20),
        nullable=False,
        default=MembershipStatus.PENDING.value,
        comment="Status of the membership"
    )
    
    # Invitation tracking
    invited_by_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', name='fk_group_memberships_invited_by_id'),
        comment="ID of the user who sent the invitation"
    )
    invitation_sent_at = Column(
        DateTime(timezone=True),
        comment="When the invitation was sent"
    )
    
    # Membership timeline
    joined_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the user joined the group"
    )
    left_at = Column(
        DateTime(timezone=True),
        comment="When the user left the group"
    )
    
    # Ban management
    banned_at = Column(
        DateTime(timezone=True),
        comment="When the user was banned"
    )
    banned_by_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', name='fk_group_memberships_banned_by_id'),
        comment="ID of the user who banned this member"
    )
    ban_reason = Column(
        Text,
        comment="Reason for the ban"
    )
    
    # Additional information
    notes = Column(
        Text,
        comment="Additional notes about the membership"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the membership record was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the membership was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('creator', 'admin', 'moderator', 'member')",
            name="ck_group_memberships_role"
        ),
        CheckConstraint(
            "status IN ('active', 'pending', 'invited', 'banned', 'left')",
            name="ck_group_memberships_status"
        ),
        CheckConstraint(
            "left_at IS NULL OR left_at >= joined_at",
            name="ck_group_memberships_left_after_joined"
        ),
        CheckConstraint(
            "banned_at IS NULL OR banned_at >= joined_at",
            name="ck_group_memberships_banned_after_joined"
        ),
        CheckConstraint(
            "invitation_sent_at IS NULL OR invitation_sent_at <= joined_at",
            name="ck_group_memberships_invitation_before_joined"
        ),
        UniqueConstraint('group_id', 'user_id', name='uq_group_memberships_group_user'),
        Index('ix_group_memberships_group_id', 'group_id'),
        Index('ix_group_memberships_user_id', 'user_id'),
        Index('ix_group_memberships_role', 'role'),
        Index('ix_group_memberships_status', 'status'),
        Index('ix_group_memberships_joined_at', 'joined_at'),
        Index('ix_group_memberships_invited_by_id', 'invited_by_id'),
        Index('ix_group_memberships_banned_by_id', 'banned_by_id'),
        {'extend_existing': True}
    )
    
    def __init__(self, **kwargs):
        """Initialize GroupMembership with proper validation and defaults."""
        # Validate required fields
        if 'user_id' not in kwargs or not kwargs['user_id']:
            raise ValueError("User ID is required")
        
        if 'group_id' not in kwargs or not kwargs['group_id']:
            raise ValueError("Group ID is required")
        
        # Set default values if not provided
        if 'role' not in kwargs:
            kwargs['role'] = MembershipRole.MEMBER.value
            
        if 'status' not in kwargs:
            kwargs['status'] = MembershipStatus.PENDING.value
            
        if 'joined_at' not in kwargs:
            kwargs['joined_at'] = datetime.now(timezone.utc)
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.now(timezone.utc)
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        super().__init__(**kwargs)
    
    # Validation methods
    @validates('user_id')
    def validate_user_id(self, key: str, user_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate user_id is provided."""
        if not user_id:
            raise ValueError("User ID is required")
        return user_id
    
    @validates('group_id')
    def validate_group_id(self, key: str, group_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate group_id is provided."""
        if not group_id:
            raise ValueError("Group ID is required")
        return group_id
    
    @validates('role')
    def validate_role(self, key: str, role: str) -> str:
        """Validate role."""
        if not role:
            raise ValueError("Role is required")
        
        valid_roles = [r.value for r in MembershipRole]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        return role
    
    @validates('status')
    def validate_status(self, key: str, status: str) -> str:
        """Validate status."""
        if not status:
            raise ValueError("Status is required")
        
        valid_statuses = [s.value for s in MembershipStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        return status
    
    @validates('joined_at')
    def validate_joined_at(self, key: str, joined_at: datetime) -> datetime:
        """Validate joined_at is provided."""
        if not joined_at:
            raise ValueError("Joined at time is required")
        return joined_at
    
    # Properties
    @property
    def is_active(self) -> bool:
        """Check if membership is active."""
        return self.status == MembershipStatus.ACTIVE.value
    
    @property
    def is_banned(self) -> bool:
        """Check if member is banned."""
        return self.status == MembershipStatus.BANNED.value
    
    @property
    def has_left(self) -> bool:
        """Check if member has left."""
        return self.status == MembershipStatus.LEFT.value
    
    @property
    def is_pending(self) -> bool:
        """Check if membership is pending."""
        return self.status == MembershipStatus.PENDING.value
    
    @property
    def can_moderate(self) -> bool:
        """Check if member can moderate the group."""
        return self.role in [MembershipRole.CREATOR.value, MembershipRole.ADMIN.value, MembershipRole.MODERATOR.value]
    
    @property
    def can_invite(self) -> bool:
        """Check if member can invite others."""
        return self.role in [MembershipRole.CREATOR.value, MembershipRole.ADMIN.value, MembershipRole.MODERATOR.value]
    
    @property
    def can_admin(self) -> bool:
        """Check if member has admin privileges."""
        return self.role in [MembershipRole.CREATOR.value, MembershipRole.ADMIN.value]
    
    @property
    def is_creator(self) -> bool:
        """Check if member is the group creator."""
        return self.role == MembershipRole.CREATOR.value
    
    @property
    def role_level(self) -> int:
        """Get numeric role level for hierarchy comparison."""
        role_levels = {
            MembershipRole.MEMBER.value: 1,
            MembershipRole.MODERATOR.value: 2,
            MembershipRole.ADMIN.value: 3,
            MembershipRole.CREATOR.value: 4
        }
        return role_levels.get(self.role, 0)
    
    @property
    def membership_duration(self) -> Optional[int]:
        """Get membership duration in days."""
        if not self.joined_at:
            return None
        
        end_time = self.left_at or datetime.now(timezone.utc)
        duration = end_time - self.joined_at
        return duration.days
    
    # Business logic methods
    def promote(self, new_role: str) -> None:
        """Promote member to a higher role."""
        if not self.is_active:
            raise ValueError("Cannot promote inactive member")
        
        valid_roles = [r.value for r in MembershipRole]
        if new_role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        role_levels = {
            MembershipRole.MEMBER.value: 1,
            MembershipRole.MODERATOR.value: 2,
            MembershipRole.ADMIN.value: 3,
            MembershipRole.CREATOR.value: 4
        }
        
        current_level = role_levels.get(self.role, 0)
        new_level = role_levels.get(new_role, 0)
        
        if new_level <= current_level:
            raise ValueError("New role must be higher than current role")
        
        self.role = new_role
        self.updated_at = datetime.now(timezone.utc)
    
    def demote(self, new_role: str) -> None:
        """Demote member to a lower role."""
        if not self.is_active:
            raise ValueError("Cannot demote inactive member")
        
        if self.is_creator:
            raise ValueError("Cannot demote group creator")
        
        valid_roles = [r.value for r in MembershipRole if r != MembershipRole.CREATOR]
        if new_role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        role_levels = {
            MembershipRole.MEMBER.value: 1,
            MembershipRole.MODERATOR.value: 2,
            MembershipRole.ADMIN.value: 3,
            MembershipRole.CREATOR.value: 4
        }
        
        current_level = role_levels.get(self.role, 0)
        new_level = role_levels.get(new_role, 0)
        
        if new_level >= current_level:
            raise ValueError("New role must be lower than current role")
        
        self.role = new_role
        self.updated_at = datetime.now(timezone.utc)
    
    def ban(self, banned_by_id: Union[str, uuid.UUID], reason: Optional[str] = None) -> None:
        """Ban the member from the group."""
        if self.is_creator:
            raise ValueError("Cannot ban group creator")
        
        if self.is_banned:
            raise ValueError("Member is already banned")
        
        self.status = MembershipStatus.BANNED.value
        self.banned_at = datetime.now(timezone.utc)
        self.banned_by_id = banned_by_id
        self.ban_reason = reason
        self.updated_at = datetime.now(timezone.utc)
    
    def unban(self) -> None:
        """Unban the member."""
        if not self.is_banned:
            raise ValueError("Member is not banned")
        
        self.status = MembershipStatus.ACTIVE.value
        self.banned_at = None
        self.banned_by_id = None
        self.ban_reason = None
        self.updated_at = datetime.now(timezone.utc)
    
    def leave(self) -> None:
        """Mark member as having left the group."""
        if self.is_creator:
            raise ValueError("Group creator cannot leave (must transfer ownership first)")
        
        if self.has_left:
            raise ValueError("Member has already left")
        
        self.status = MembershipStatus.LEFT.value
        self.left_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def activate(self) -> None:
        """Activate a pending membership."""
        if not self.is_pending:
            raise ValueError("Can only activate pending memberships")
        
        self.status = MembershipStatus.ACTIVE.value
        self.updated_at = datetime.now(timezone.utc)
    
    def send_invitation(self, invited_by_id: Union[str, uuid.UUID]) -> None:
        """Mark invitation as sent."""
        self.status = MembershipStatus.INVITED.value
        self.invited_by_id = invited_by_id
        self.invitation_sent_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def accept_invitation(self) -> None:
        """Accept the invitation and activate membership."""
        if self.status != MembershipStatus.INVITED.value:
            raise ValueError("No pending invitation to accept")
        
        self.status = MembershipStatus.ACTIVE.value
        self.joined_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def can_manage_member(self, target_member: 'GroupMembership') -> bool:
        """Check if this member can manage another member."""
        if not self.is_active:
            return False
        
        if target_member.is_creator:
            return False  # Nobody can manage creator
        
        if self.is_creator:
            return True  # Creator can manage everyone
        
        return self.role_level > target_member.role_level
    
    # Class methods for queries
    @classmethod
    def get_by_user_and_group(cls, db_session, user_id: Union[str, uuid.UUID], group_id: Union[str, uuid.UUID]):
        """Get membership by user and group."""
        return db_session.query(cls).filter(
            cls.user_id == user_id,
            cls.group_id == group_id
        ).first()
    
    @classmethod
    def get_active_members(cls, db_session, group_id: Union[str, uuid.UUID]):
        """Get all active members of a group."""
        return db_session.query(cls).filter(
            cls.group_id == group_id,
            cls.status == MembershipStatus.ACTIVE.value
        ).all()
    
    @classmethod
    def get_by_role(cls, db_session, group_id: Union[str, uuid.UUID], role: str):
        """Get members by role in a group."""
        return db_session.query(cls).filter(
            cls.group_id == group_id,
            cls.role == role,
            cls.status == MembershipStatus.ACTIVE.value
        ).all()
    
    @classmethod
    def get_pending_memberships(cls, db_session, group_id: Union[str, uuid.UUID]):
        """Get pending memberships for a group."""
        return db_session.query(cls).filter(
            cls.group_id == group_id,
            cls.status.in_([MembershipStatus.PENDING.value, MembershipStatus.INVITED.value])
        ).all()
    
    @classmethod
    def get_user_groups(cls, db_session, user_id: Union[str, uuid.UUID]):
        """Get all groups a user is a member of."""
        return db_session.query(cls).filter(
            cls.user_id == user_id,
            cls.status == MembershipStatus.ACTIVE.value
        ).all()
    
    # Representation
    def __repr__(self) -> str:
        """String representation of GroupMembership."""
        return f"<GroupMembership(id={self.id}, group_id={self.group_id}, user_id={self.user_id}, role='{self.role}', status='{self.status}')>"
    
    def to_dict(self, include_user: bool = False, include_group: bool = False) -> Dict[str, Any]:
        """Convert GroupMembership to dictionary."""
        result = {
            'id': str(self.id),
            'group_id': str(self.group_id),
            'user_id': str(self.user_id),
            'role': self.role,
            'status': self.status,
            'invited_by_id': str(self.invited_by_id) if self.invited_by_id else None,
            'invitation_sent_at': self.invitation_sent_at.isoformat() if self.invitation_sent_at else None,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'left_at': self.left_at.isoformat() if self.left_at else None,
            'banned_at': self.banned_at.isoformat() if self.banned_at else None,
            'banned_by_id': str(self.banned_by_id) if self.banned_by_id else None,
            'ban_reason': self.ban_reason,
            'notes': self.notes,
            'is_active': self.is_active,
            'is_banned': self.is_banned,
            'has_left': self.has_left,
            'is_pending': self.is_pending,
            'can_moderate': self.can_moderate,
            'can_invite': self.can_invite,
            'can_admin': self.can_admin,
            'is_creator': self.is_creator,
            'role_level': self.role_level,
            'membership_duration': self.membership_duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        # Add related objects if requested
        if include_user and hasattr(self, 'user'):
            result['user'] = self.user.to_dict() if self.user else None
            
        if include_group and hasattr(self, 'group'):
            result['group'] = self.group.to_dict() if self.group else None
        
        return result


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(GroupMembership, 'before_update')
def update_group_membership_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)