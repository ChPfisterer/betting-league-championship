"""
Competition model for the betting league championship application.

This module defines the Competition model with comprehensive field validation,
season management, and business logic as specified by the TDD tests
in backend/tests/models/test_competition_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, 
    CheckConstraint, Index, ForeignKey, JSON, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone, timedelta
from typing import Union, Optional, Dict, Any, List
from decimal import Decimal
import uuid
import re
from enum import Enum

from .base import Base


class CompetitionFormat(Enum):
    """Valid competition format types."""
    LEAGUE = "league"
    TOURNAMENT = "tournament"
    KNOCKOUT = "knockout"
    ROUND_ROBIN = "round_robin"
    SWISS_SYSTEM = "swiss_system"
    ELIMINATION = "elimination"
    LADDER = "ladder"


class CompetitionStatus(Enum):
    """Valid competition status values."""
    DRAFT = "draft"
    UPCOMING = "upcoming"
    REGISTRATION_OPEN = "registration_open"
    REGISTRATION_CLOSED = "registration_closed"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CompetitionVisibility(Enum):
    """Valid competition visibility levels."""
    PUBLIC = "public"
    PRIVATE = "private"
    GROUP_ONLY = "group_only"


class Competition(Base):
    """
    Competition model for organizing sports competitions and tournaments.
    
    Competitions belong to sports and seasons, define formats and rules,
    manage participants, and track progress through various status states.
    """
    
    __tablename__ = 'competitions'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the competition"
    )
    
    # Basic information
    name = Column(
        String(150),
        nullable=False,
        comment="Competition name"
    )
    slug = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="URL-friendly competition identifier"
    )
    description = Column(
        Text,
        comment="Detailed competition description"
    )
    
    # Sport and season association
    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey('sports.id', name='fk_competitions_sport_id'),
        nullable=False,
        comment="ID of the sport for this competition"
    )
    season_id = Column(
        UUID(as_uuid=True),
        ForeignKey('seasons.id', name='fk_competitions_season_id'),
        nullable=False,
        comment="ID of the season this competition belongs to"
    )
    
    # Competition configuration
    format_type = Column(
        String(20),
        nullable=False,
        comment="Competition format (league, tournament, etc.)"
    )
    status = Column(
        String(20),
        nullable=False,
        default=CompetitionStatus.DRAFT.value,
        comment="Current competition status"
    )
    
    # Dates and timing
    start_date = Column(
        DateTime(timezone=True),
        comment="Competition start date"
    )
    end_date = Column(
        DateTime(timezone=True),
        comment="Competition end date"
    )
    registration_deadline = Column(
        DateTime(timezone=True),
        comment="Deadline for team/participant registration"
    )
    betting_closes_at = Column(
        DateTime(timezone=True),
        comment="When betting closes for this competition"
    )
    
    # Visual branding
    logo_url = Column(
        String(500),
        comment="URL to competition logo"
    )
    banner_url = Column(
        String(500),
        comment="URL to competition banner image"
    )
    
    # Participation settings
    max_participants = Column(
        Integer,
        comment="Maximum number of participants allowed"
    )
    min_participants = Column(
        Integer,
        nullable=False,
        default=2,
        comment="Minimum number of participants required"
    )
    
    # Financial settings
    entry_fee = Column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal('0.00'),
        comment="Entry fee to participate"
    )
    prize_pool = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal('0.00'),
        comment="Total prize pool for winners"
    )
    prize_distribution = Column(
        JSON,
        comment="Prize distribution configuration"
    )
    
    # Access and betting settings
    visibility = Column(
        String(20),
        nullable=False,
        default=CompetitionVisibility.PUBLIC.value,
        comment="Who can view this competition"
    )
    allow_public_betting = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether public betting is allowed"
    )
    
    # Rules and configuration
    rules = Column(
        Text,
        comment="Competition rules and regulations"
    )
    point_system = Column(
        JSON,
        comment="Point scoring system configuration"
    )
    
    # Organization
    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey('groups.id', name='fk_competitions_group_id'),
        comment="ID of the organizing group (optional)"
    )
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', name='fk_competitions_created_by'),
        comment="ID of the user who created the competition"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the competition was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the competition was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "format_type IN ('league', 'tournament', 'knockout', 'round_robin', 'swiss_system', 'elimination', 'ladder')",
            name="ck_competitions_format_type"
        ),
        CheckConstraint(
            "status IN ('draft', 'upcoming', 'registration_open', 'registration_closed', 'active', 'paused', 'completed', 'cancelled')",
            name="ck_competitions_status"
        ),
        CheckConstraint(
            "visibility IN ('public', 'private', 'group_only')",
            name="ck_competitions_visibility"
        ),
        CheckConstraint(
            "min_participants > 0",
            name="ck_competitions_min_participants"
        ),
        CheckConstraint(
            "max_participants IS NULL OR max_participants >= min_participants",
            name="ck_competitions_max_participants"
        ),
        CheckConstraint(
            "entry_fee >= 0",
            name="ck_competitions_entry_fee"
        ),
        CheckConstraint(
            "prize_pool >= 0",
            name="ck_competitions_prize_pool"
        ),
        CheckConstraint(
            "end_date IS NULL OR start_date IS NULL OR end_date > start_date",
            name="ck_competitions_date_order"
        ),
        CheckConstraint(
            "LENGTH(name) >= 3",
            name="ck_competitions_name_length"
        ),
        CheckConstraint(
            "LENGTH(slug) >= 3",
            name="ck_competitions_slug_length"
        ),
        Index('ix_competitions_name', 'name'),
        Index('ix_competitions_slug', 'slug'),
        Index('ix_competitions_sport_id', 'sport_id'),
        Index('ix_competitions_season_id', 'season_id'),
        Index('ix_competitions_status', 'status'),
        Index('ix_competitions_visibility', 'visibility'),
        Index('ix_competitions_start_date', 'start_date'),
        Index('ix_competitions_created_at', 'created_at'),
    )
    
    def __init__(self, **kwargs):
        """Initialize Competition with proper defaults for TDD testing."""
        # Validate required fields before processing
        if 'name' not in kwargs or not kwargs['name']:
            raise ValueError("Competition name is required")
        
        if 'sport_id' not in kwargs or not kwargs['sport_id']:
            raise ValueError("Sport ID is required")
        
        if 'season_id' not in kwargs or not kwargs['season_id']:
            raise ValueError("Season ID is required")
        
        if 'format_type' not in kwargs or not kwargs['format_type']:
            raise ValueError("Format type is required")
        
        # Handle date validation
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise ValueError("Start date must be before end date")
        
        # Set default values for testing if not provided
        if 'status' not in kwargs:
            kwargs['status'] = CompetitionStatus.DRAFT.value
            
        if 'visibility' not in kwargs:
            kwargs['visibility'] = CompetitionVisibility.PUBLIC.value
            
        if 'allow_public_betting' not in kwargs:
            kwargs['allow_public_betting'] = True
            
        if 'min_participants' not in kwargs:
            kwargs['min_participants'] = 2
            
        if 'entry_fee' not in kwargs:
            kwargs['entry_fee'] = Decimal('0.00')
            
        if 'prize_pool' not in kwargs:
            kwargs['prize_pool'] = Decimal('0.00')
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.now(timezone.utc)
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        # Auto-generate slug from name if not provided
        if 'slug' not in kwargs and 'name' in kwargs:
            kwargs['slug'] = self._generate_slug(kwargs['name'])
            
        super().__init__(**kwargs)
    
    @staticmethod
    def _generate_slug(name: str) -> str:
        """Generate URL-friendly slug from competition name."""
        if not name:
            return ""
        
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
        slug = re.sub(r'[\s-]+', '-', slug)
        slug = slug.strip('-')
        
        return slug
    
    # Validation methods
    @validates('name')
    def validate_name(self, key: str, name: str) -> str:
        """Validate competition name."""
        if not name:
            raise ValueError("Competition name is required")
        
        name = name.strip()
        if len(name) < 3:
            raise ValueError("Competition name must be at least 3 characters long")
        
        if len(name) > 150:
            raise ValueError("Competition name cannot exceed 150 characters")
        
        return name
    
    @validates('slug')
    def validate_slug(self, key: str, slug: str) -> str:
        """Validate competition slug."""
        if not slug:
            raise ValueError("Competition slug is required")
        
        slug = slug.lower().strip()
        if len(slug) < 3:
            raise ValueError("Competition slug must be at least 3 characters long")
        
        if len(slug) > 100:
            raise ValueError("Competition slug cannot exceed 100 characters")
        
        # Must be URL-friendly
        if not re.match(r'^[a-z0-9_-]+$', slug):
            raise ValueError("Competition slug can only contain lowercase letters, numbers, underscores, and hyphens")
        
        if slug.startswith('-') or slug.endswith('-'):
            raise ValueError("Competition slug cannot start or end with hyphen")
        
        if '--' in slug:
            raise ValueError("Competition slug cannot contain consecutive hyphens")
        
        return slug
    
    @validates('format_type')
    def validate_format_type(self, key: str, format_type: str) -> str:
        """Validate competition format type."""
        if not format_type:
            raise ValueError("Format type is required")
        
        valid_formats = [fmt.value for fmt in CompetitionFormat]
        if format_type not in valid_formats:
            raise ValueError(f"Invalid format type. Must be one of: {', '.join(valid_formats)}")
        
        return format_type
    
    @validates('status')
    def validate_status(self, key: str, status: str) -> str:
        """Validate competition status."""
        if not status:
            raise ValueError("Status is required")
        
        valid_statuses = [status.value for status in CompetitionStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        return status
    
    @validates('visibility')
    def validate_visibility(self, key: str, visibility: str) -> str:
        """Validate competition visibility."""
        if not visibility:
            raise ValueError("Visibility is required")
        
        valid_visibilities = [vis.value for vis in CompetitionVisibility]
        if visibility not in valid_visibilities:
            raise ValueError(f"Invalid visibility. Must be one of: {', '.join(valid_visibilities)}")
        
        return visibility
    
    @validates('min_participants')
    def validate_min_participants(self, key: str, min_participants: int) -> int:
        """Validate minimum participants."""
        if min_participants <= 0:
            raise ValueError("Minimum participants must be greater than 0")
        
        return min_participants
    
    @validates('max_participants')
    def validate_max_participants(self, key: str, max_participants: Optional[int]) -> Optional[int]:
        """Validate maximum participants."""
        if max_participants is None:
            return max_participants
        
        if max_participants <= 0:
            raise ValueError("Maximum participants must be greater than 0")
        
        if hasattr(self, 'min_participants') and max_participants < self.min_participants:
            raise ValueError("Maximum participants must be greater than or equal to minimum participants")
        
        return max_participants
    
    @validates('sport_id')
    def validate_sport_id(self, key: str, sport_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate sport_id is provided."""
        if not sport_id:
            raise ValueError("Sport ID is required")
        return sport_id
    
    @validates('season_id')
    def validate_season_id(self, key: str, season_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate season_id is provided."""
        if not season_id:
            raise ValueError("Season ID is required")
        return season_id
    
    @validates('start_date')
    def validate_start_date(self, key: str, start_date: Optional[datetime]) -> Optional[datetime]:
        """Validate start date."""
        if start_date is None:
            return start_date
        
        # Check if end_date is already set and validate order
        if hasattr(self, 'end_date') and self.end_date and start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        
        return start_date
    
    @validates('end_date')
    def validate_end_date(self, key: str, end_date: Optional[datetime]) -> Optional[datetime]:
        """Validate end date."""
        if end_date is None:
            return end_date
        
        # Check if start_date is already set and validate order
        if hasattr(self, 'start_date') and self.start_date and end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        
        return end_date
    
    # Properties
    @property
    def is_draft(self) -> bool:
        """Check if competition is in draft status."""
        return self.status == CompetitionStatus.DRAFT.value
    
    @property
    def is_active(self) -> bool:
        """Check if competition is currently active."""
        return self.status == CompetitionStatus.ACTIVE.value
    
    @property
    def is_completed(self) -> bool:
        """Check if competition is completed."""
        return self.status == CompetitionStatus.COMPLETED.value
    
    @property
    def is_cancelled(self) -> bool:
        """Check if competition is cancelled."""
        return self.status == CompetitionStatus.CANCELLED.value
    
    @property
    def is_public(self) -> bool:
        """Check if competition is public."""
        return self.visibility == CompetitionVisibility.PUBLIC.value
    
    @property
    def has_entry_fee(self) -> bool:
        """Check if competition has entry fee."""
        return self.entry_fee > 0
    
    @property
    def has_prize_pool(self) -> bool:
        """Check if competition has prize pool."""
        return self.prize_pool > 0
    
    @property
    def duration_days(self) -> Optional[int]:
        """Get competition duration in days."""
        if not self.start_date or not self.end_date:
            return None
        return (self.end_date - self.start_date).days
    
    # Business logic methods
    def can_register(self) -> tuple[bool, str]:
        """Check if registration is currently allowed."""
        if self.status != CompetitionStatus.REGISTRATION_OPEN.value:
            return False, "Registration is not open"
        
        if self.registration_deadline and datetime.now(timezone.utc) > self.registration_deadline:
            return False, "Registration deadline has passed"
        
        return True, "Registration is open"
    
    def can_place_bet(self) -> tuple[bool, str]:
        """Check if betting is currently allowed."""
        if not self.allow_public_betting:
            return False, "Betting is not allowed for this competition"
        
        if self.betting_closes_at and datetime.now(timezone.utc) > self.betting_closes_at:
            return False, "Betting is closed"
        
        if self.status not in [CompetitionStatus.UPCOMING.value, CompetitionStatus.ACTIVE.value]:
            return False, "Betting is not available for current competition status"
        
        return True, "Betting is allowed"
    
    def start_competition(self) -> None:
        """Start the competition."""
        if self.status != CompetitionStatus.REGISTRATION_CLOSED.value:
            raise ValueError("Can only start competition when registration is closed")
        
        self.status = CompetitionStatus.ACTIVE.value
        if not self.start_date:
            self.start_date = datetime.now(timezone.utc)
    
    def complete_competition(self) -> None:
        """Complete the competition."""
        if self.status != CompetitionStatus.ACTIVE.value:
            raise ValueError("Can only complete active competitions")
        
        self.status = CompetitionStatus.COMPLETED.value
        if not self.end_date:
            self.end_date = datetime.now(timezone.utc)
    
    def cancel_competition(self, reason: Optional[str] = None) -> None:
        """Cancel the competition."""
        if self.status in [CompetitionStatus.COMPLETED.value, CompetitionStatus.CANCELLED.value]:
            raise ValueError("Cannot cancel completed or already cancelled competition")
        
        self.status = CompetitionStatus.CANCELLED.value
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Competition."""
        return f"<Competition(id={self.id}, name='{self.name}', status='{self.status}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Competition to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'sport_id': str(self.sport_id),
            'season_id': str(self.season_id),
            'format_type': self.format_type,
            'status': self.status,
            'visibility': self.visibility,
            'is_public': self.is_public,
            'is_active': self.is_active,
            'is_completed': self.is_completed,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'duration_days': self.duration_days,
            'registration_deadline': self.registration_deadline.isoformat() if self.registration_deadline else None,
            'betting_closes_at': self.betting_closes_at.isoformat() if self.betting_closes_at else None,
            'min_participants': self.min_participants,
            'max_participants': self.max_participants,
            'entry_fee': float(self.entry_fee),
            'prize_pool': float(self.prize_pool),
            'has_entry_fee': self.has_entry_fee,
            'has_prize_pool': self.has_prize_pool,
            'allow_public_betting': self.allow_public_betting,
            'group_id': str(self.group_id) if self.group_id else None,
            'created_by': str(self.created_by) if self.created_by else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Competition, 'before_update')
def update_competition_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)