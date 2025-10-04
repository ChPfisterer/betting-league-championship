"""
Group model for the betting league championship application.

This module defines the Group model with comprehensive field validation,
membership management, and business logic as specified by the TDD tests
in backend/tests/models/test_group_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, 
    CheckConstraint, Index, ForeignKey, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone
from typing import Union, Optional, Dict, Any, List
import uuid
import re
from enum import Enum

from .base import Base


class PointSystem(Enum):
    """Valid point systems for groups."""
    STANDARD = "standard"
    CONFIDENCE = "confidence"
    SPREAD = "spread"
    CUSTOM = "custom"


class Group(Base):
    """
    Group model for organizing betting leagues and competitions.
    
    Groups allow users to create private or public betting communities
    with customizable rules, point systems, and member management.
    """
    
    __tablename__ = 'groups'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the group"
    )
    
    # Basic information
    name = Column(
        String(100),
        nullable=False,
        comment="Group name"
    )
    description = Column(
        Text,
        nullable=False,
        comment="Group description and purpose"
    )
    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', name='fk_groups_creator_id'),
        nullable=False,
        comment="ID of the user who created the group"
    )
    
    # Privacy and access settings
    is_private = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether group is private (invite only)"
    )
    max_members = Column(
        Integer,
        nullable=False,
        default=50,
        comment="Maximum number of members allowed"
    )
    allow_member_invites = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether members can invite others"
    )
    auto_approve_members = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether to auto-approve new members"
    )
    
    # Point system and competition settings
    point_system = Column(
        String(20),
        nullable=False,
        default=PointSystem.STANDARD.value,
        comment="Point system used for scoring"
    )
    
    # Optional profile and branding
    avatar_url = Column(
        String(500),
        comment="URL to group avatar image"
    )
    banner_url = Column(
        String(500),
        comment="URL to group banner image"
    )
    rules_text = Column(
        Text,
        comment="Custom rules and guidelines for the group"
    )
    
    # Access and joining
    join_code = Column(
        String(20),
        unique=True,
        comment="Unique code for joining private groups"
    )
    
    # Financial settings
    entry_fee = Column(
        Numeric(10, 2),
        comment="Entry fee required to join group"
    )
    prize_pool = Column(
        Numeric(12, 2),
        comment="Total prize pool for group competitions"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the group was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the group was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "point_system IN ('standard', 'confidence', 'spread', 'custom')",
            name="ck_groups_point_system"
        ),
        CheckConstraint(
            "max_members > 0",
            name="ck_groups_max_members"
        ),
        CheckConstraint(
            "entry_fee >= 0",
            name="ck_groups_entry_fee"
        ),
        CheckConstraint(
            "prize_pool >= 0",
            name="ck_groups_prize_pool"
        ),
        CheckConstraint(
            "LENGTH(name) >= 3",
            name="ck_groups_name_length"
        ),
        CheckConstraint(
            "LENGTH(description) >= 10",
            name="ck_groups_description_length"
        ),
        Index('ix_groups_name', 'name'),
        Index('ix_groups_creator_id', 'creator_id'),
        Index('ix_groups_is_private', 'is_private'),
        Index('ix_groups_created_at', 'created_at'),
        Index('ix_groups_join_code', 'join_code'),
    )
    
    def __init__(self, **kwargs):
        """Initialize Group with proper defaults for TDD testing."""
        # Set default values for testing if not provided
        if 'is_private' not in kwargs:
            kwargs['is_private'] = False
            
        if 'max_members' not in kwargs:
            kwargs['max_members'] = 50
            
        if 'allow_member_invites' not in kwargs:
            kwargs['allow_member_invites'] = True
            
        if 'auto_approve_members' not in kwargs:
            kwargs['auto_approve_members'] = True
            
        if 'point_system' not in kwargs:
            kwargs['point_system'] = PointSystem.STANDARD.value
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.now(timezone.utc)
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        super().__init__(**kwargs)
    
    # Validation methods
    @validates('name')
    def validate_name(self, key: str, name: str) -> str:
        """Validate group name."""
        if not name:
            raise ValueError("Group name is required")
        
        name = name.strip()
        if len(name) < 3:
            raise ValueError("Group name must be at least 3 characters long")
        
        if len(name) > 100:
            raise ValueError("Group name cannot exceed 100 characters")
        
        # Check for invalid characters
        if not re.match(r'^[a-zA-Z0-9\s\-_\'\.]+$', name):
            raise ValueError("Group name contains invalid characters")
        
        return name
    
    @validates('description')
    def validate_description(self, key: str, description: str) -> str:
        """Validate group description."""
        if not description:
            raise ValueError("Group description is required")
        
        description = description.strip()
        if len(description) < 10:
            raise ValueError("Group description must be at least 10 characters long")
        
        if len(description) > 5000:
            raise ValueError("Group description cannot exceed 5000 characters")
        
        return description
    
    @validates('point_system')
    def validate_point_system(self, key: str, point_system: str) -> str:
        """Validate point system value."""
        if not point_system:
            raise ValueError("Point system is required")
        
        valid_systems = [system.value for system in PointSystem]
        if point_system not in valid_systems:
            raise ValueError(f"Invalid point system. Must be one of: {', '.join(valid_systems)}")
        
        return point_system
    
    @validates('max_members')
    def validate_max_members(self, key: str, max_members: int) -> int:
        """Validate maximum members count."""
        if max_members <= 0:
            raise ValueError("Maximum members must be greater than 0")
        
        if max_members > 1000:
            raise ValueError("Maximum members cannot exceed 1000")
        
        return max_members
    
    @validates('join_code')
    def validate_join_code(self, key: str, join_code: Optional[str]) -> Optional[str]:
        """Validate join code format."""
        if not join_code:
            return join_code
        
        join_code = join_code.upper().strip()
        
        if len(join_code) < 4:
            raise ValueError("Join code must be at least 4 characters long")
        
        if len(join_code) > 20:
            raise ValueError("Join code cannot exceed 20 characters")
        
        if not re.match(r'^[A-Z0-9]+$', join_code):
            raise ValueError("Join code can only contain uppercase letters and numbers")
        
        return join_code
    
    @validates('entry_fee')
    def validate_entry_fee(self, key: str, entry_fee: Optional[float]) -> Optional[float]:
        """Validate entry fee amount."""
        if entry_fee is None:
            return entry_fee
        
        if entry_fee < 0:
            raise ValueError("Entry fee cannot be negative")
        
        if entry_fee > 10000:
            raise ValueError("Entry fee cannot exceed 10,000")
        
        return entry_fee
    
    # Properties
    @property
    def member_count(self) -> int:
        """Get current number of members."""
        # This will be implemented when relationships are added
        return 0
    
    @property
    def is_full(self) -> bool:
        """Check if group has reached maximum capacity."""
        return self.member_count >= self.max_members
    
    @property
    def requires_join_code(self) -> bool:
        """Check if group requires join code for access."""
        return self.is_private and self.join_code is not None
    
    @property
    def has_entry_fee(self) -> bool:
        """Check if group requires entry fee."""
        return self.entry_fee is not None and self.entry_fee > 0
    
    # Business logic methods
    def generate_join_code(self) -> str:
        """Generate a unique join code for the group."""
        import random
        import string
        
        # Generate 8-character alphanumeric code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.join_code = code
        return code
    
    def configure_point_system(self, config: Dict[str, Any]) -> None:
        """Configure custom point system settings."""
        if self.point_system != PointSystem.CUSTOM.value:
            raise ValueError("Can only configure custom point systems")
        
        # This will be expanded with actual configuration logic
        # For now, just validate the config structure
        required_keys = ['scoring_method', 'point_values']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")
    
    def can_join(self, user_id: str) -> tuple[bool, str]:
        """Check if a user can join this group."""
        if self.is_full:
            return False, "Group is full"
        
        # Add more join validation logic here
        return True, "Can join"
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Group."""
        return f"<Group(id={self.id}, name='{self.name}', members={self.member_count}/{self.max_members})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Group to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'creator_id': str(self.creator_id),
            'is_private': self.is_private,
            'max_members': self.max_members,
            'allow_member_invites': self.allow_member_invites,
            'auto_approve_members': self.auto_approve_members,
            'point_system': self.point_system,
            'avatar_url': self.avatar_url,
            'banner_url': self.banner_url,
            'rules_text': self.rules_text,
            'join_code': self.join_code,
            'entry_fee': float(self.entry_fee) if self.entry_fee else None,
            'prize_pool': float(self.prize_pool) if self.prize_pool else None,
            'member_count': self.member_count,
            'is_full': self.is_full,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Group, 'before_update')
def update_group_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)