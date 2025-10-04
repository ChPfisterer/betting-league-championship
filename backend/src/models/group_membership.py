"""
GroupMembership model for the betting league championship application.

This module defines the GroupMembership model for managing user participation
in betting groups. This is a minimal implementation to support Group model testing.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, CheckConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
from enum import Enum

from .base import Base


class MembershipStatus(Enum):
    """Status of group membership."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REMOVED = "removed"


class GroupMembership(Base):
    """
    GroupMembership model for managing user participation in groups.
    
    This is a minimal implementation to support Group model testing.
    Full implementation will be added in future TDD iterations.
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
    
    # Membership details
    status = Column(
        String(20),
        nullable=False,
        default=MembershipStatus.PENDING.value,
        comment="Status of the membership"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the membership was created"
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
            "status IN ('pending', 'active', 'suspended', 'removed')",
            name="ck_group_memberships_status"
        ),
        Index('ix_group_memberships_group_id', 'group_id'),
        Index('ix_group_memberships_user_id', 'user_id'),
        Index('ix_group_memberships_status', 'status'),
    )
    
    def __repr__(self) -> str:
        """String representation of GroupMembership."""
        return f"<GroupMembership(id={self.id}, group_id={self.group_id}, user_id={self.user_id})>"