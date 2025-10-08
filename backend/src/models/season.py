"""
Season model for the betting league championship application.

This module defines the Season model with comprehensive field validation,
date management, and business logic as specified by the TDD tests
in backend/tests/models/test_season_model.py.
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


class SeasonStatus(Enum):
    """Valid season status values."""
    UPCOMING = "upcoming"
    REGISTRATION = "registration"
    ACTIVE = "active"
    PLAYOFFS = "playoffs"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Season(Base):
    """
    Season model for organizing sports competitions within time periods.
    
    Seasons represent specific time periods (typically a year) during which
    competitions are organized for a particular sport. They manage registration
    periods, rules, and overall season-wide settings.
    """
    
    __tablename__ = 'seasons'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the season"
    )
    
    # Basic information
    name = Column(
        String(150),
        nullable=False,
        comment="Season name (e.g., '2024-25 Premier League')"
    )
    slug = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="URL-friendly season identifier"
    )
    description = Column(
        Text,
        comment="Detailed season description"
    )
    
    # Sport association
    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey('sports.id', name='fk_seasons_sport_id'),
        nullable=False,
        comment="ID of the sport for this season"
    )
    
    # Season timing
    year = Column(
        Integer,
        nullable=False,
        comment="Primary year for the season"
    )
    start_date = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="Season start date"
    )
    end_date = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="Season end date"
    )
    
    # Registration periods
    registration_start = Column(
        DateTime(timezone=True),
        comment="When team/participant registration opens"
    )
    registration_end = Column(
        DateTime(timezone=True),
        comment="When team/participant registration closes"
    )
    
    # Season status and settings
    status = Column(
        String(20),
        nullable=False,
        default=SeasonStatus.UPCOMING.value,
        comment="Current season status"
    )
    is_current = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether this is the current active season for the sport"
    )
    
    # Season configuration
    max_competitions = Column(
        Integer,
        comment="Maximum number of competitions allowed"
    )
    prize_pool_total = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal('0.00'),
        comment="Total prize pool for the season"
    )
    
    # Rules and formats
    rules = Column(
        Text,
        comment="Season-specific rules and regulations"
    )
    season_format = Column(
        String(50),
        comment="Season format (e.g., 'round_robin', 'knockout', 'league')"
    )
    playoff_format = Column(
        String(50),
        comment="Playoff format if applicable"
    )
    promotion_rules = Column(
        JSON,
        comment="Rules for promotion to higher divisions"
    )
    relegation_rules = Column(
        JSON,
        comment="Rules for relegation to lower divisions"
    )
    point_system = Column(
        JSON,
        comment="Point scoring system for the season"
    )
    tie_breaker_rules = Column(
        JSON,
        comment="Rules for breaking ties in standings"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the season was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the season was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('upcoming', 'registration', 'active', 'playoffs', 'completed', 'cancelled')",
            name="ck_seasons_status"
        ),
        CheckConstraint(
            "year >= 1900 AND year <= 2100",
            name="ck_seasons_year_range"
        ),
        CheckConstraint(
            "end_date > start_date",
            name="ck_seasons_date_order"
        ),
        CheckConstraint(
            "registration_end IS NULL OR registration_start IS NULL OR registration_end > registration_start",
            name="ck_seasons_registration_order"
        ),
        CheckConstraint(
            "max_competitions IS NULL OR max_competitions > 0",
            name="ck_seasons_max_competitions"
        ),
        CheckConstraint(
            "prize_pool_total >= 0",
            name="ck_seasons_prize_pool"
        ),
        CheckConstraint(
            "LENGTH(name) >= 3",
            name="ck_seasons_name_length"
        ),
        CheckConstraint(
            "LENGTH(slug) >= 3",
            name="ck_seasons_slug_length"
        ),
        Index('ix_seasons_name', 'name'),
        Index('ix_seasons_slug', 'slug'),
        Index('ix_seasons_sport_id', 'sport_id'),
        Index('ix_seasons_year', 'year'),
        Index('ix_seasons_status', 'status'),
        Index('ix_seasons_is_current', 'is_current'),
        Index('ix_seasons_start_date', 'start_date'),
        Index('ix_seasons_end_date', 'end_date'),
        Index('ix_seasons_created_at', 'created_at'),
        Index('ix_seasons_sport_year', 'sport_id', 'year'),
    )
    
    # Relationships
    sport = relationship("Sport", back_populates="seasons")
    competitions = relationship("Competition", back_populates="season")
    
    def __init__(self, **kwargs):
        """Initialize Season with proper defaults for TDD testing."""
        # Validate required fields before processing
        if 'name' not in kwargs or not kwargs['name']:
            raise ValueError("Season name is required")
        
        if 'sport_id' not in kwargs or not kwargs['sport_id']:
            raise ValueError("Sport ID is required")
        
        if 'year' not in kwargs or not kwargs['year']:
            raise ValueError("Year is required")
        
        if 'start_date' not in kwargs or not kwargs['start_date']:
            raise ValueError("Start date is required")
        
        if 'end_date' not in kwargs or not kwargs['end_date']:
            raise ValueError("End date is required")
        
        # Validate date order
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise ValueError("End date must be after start date")
        
        # Validate registration dates if provided
        registration_start = kwargs.get('registration_start')
        registration_end = kwargs.get('registration_end')
        
        if registration_start and registration_end and registration_start >= registration_end:
            raise ValueError("Registration end must be after registration start")
        
        # Set default values for testing if not provided
        if 'status' not in kwargs:
            kwargs['status'] = SeasonStatus.UPCOMING.value
            
        if 'is_current' not in kwargs:
            kwargs['is_current'] = False
            
        if 'prize_pool_total' not in kwargs:
            kwargs['prize_pool_total'] = Decimal('0.00')
            
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
        """Generate URL-friendly slug from season name."""
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
        """Validate season name."""
        if not name:
            raise ValueError("Season name is required")
        
        name = name.strip()
        if len(name) < 3:
            raise ValueError("Season name must be at least 3 characters long")
        
        if len(name) > 150:
            raise ValueError("Season name cannot exceed 150 characters")
        
        return name
    
    @validates('slug')
    def validate_slug(self, key: str, slug: str) -> str:
        """Validate season slug."""
        if not slug:
            raise ValueError("Season slug is required")
        
        slug = slug.lower().strip()
        if len(slug) < 3:
            raise ValueError("Season slug must be at least 3 characters long")
        
        if len(slug) > 100:
            raise ValueError("Season slug cannot exceed 100 characters")
        
        # Must be URL-friendly
        if not re.match(r'^[a-z0-9_-]+$', slug):
            raise ValueError("Season slug can only contain lowercase letters, numbers, underscores, and hyphens")
        
        if slug.startswith('-') or slug.endswith('-'):
            raise ValueError("Season slug cannot start or end with hyphen")
        
        if '--' in slug:
            raise ValueError("Season slug cannot contain consecutive hyphens")
        
        return slug
    
    @validates('sport_id')
    def validate_sport_id(self, key: str, sport_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate sport_id is provided."""
        if not sport_id:
            raise ValueError("Sport ID is required")
        return sport_id
    
    @validates('year')
    def validate_year(self, key: str, year: int) -> int:
        """Validate year is within reasonable range."""
        if not year:
            raise ValueError("Year is required")
        
        if year < 1900 or year > 2100:
            raise ValueError("Year must be between 1900 and 2100")
        
        return year
    
    @validates('start_date')
    def validate_start_date(self, key: str, start_date: datetime) -> datetime:
        """Validate start date."""
        if not start_date:
            raise ValueError("Start date is required")
        
        # Check if end_date is already set and validate order
        if hasattr(self, 'end_date') and self.end_date and start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        
        return start_date
    
    @validates('end_date')
    def validate_end_date(self, key: str, end_date: datetime) -> datetime:
        """Validate end date."""
        if not end_date:
            raise ValueError("End date is required")
        
        # Check if start_date is already set and validate order
        if hasattr(self, 'start_date') and self.start_date and end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        
        return end_date
    
    @validates('status')
    def validate_status(self, key: str, status: str) -> str:
        """Validate season status."""
        if not status:
            raise ValueError("Status is required")
        
        valid_statuses = [status.value for status in SeasonStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        return status
    
    @validates('max_competitions')
    def validate_max_competitions(self, key: str, max_competitions: Optional[int]) -> Optional[int]:
        """Validate max competitions."""
        if max_competitions is not None and max_competitions <= 0:
            raise ValueError("Maximum competitions must be greater than 0")
        return max_competitions
    
    # Properties
    @property
    def is_upcoming(self) -> bool:
        """Check if season is upcoming."""
        return self.status == SeasonStatus.UPCOMING.value
    
    @property
    def is_registration(self) -> bool:
        """Check if season is in registration phase."""
        return self.status == SeasonStatus.REGISTRATION.value
    
    @property
    def is_active(self) -> bool:
        """Check if season is active."""
        return self.status == SeasonStatus.ACTIVE.value
    
    @property
    def is_playoffs(self) -> bool:
        """Check if season is in playoffs."""
        return self.status == SeasonStatus.PLAYOFFS.value
    
    @property
    def is_completed(self) -> bool:
        """Check if season is completed."""
        return self.status == SeasonStatus.COMPLETED.value
    
    @property
    def is_cancelled(self) -> bool:
        """Check if season is cancelled."""
        return self.status == SeasonStatus.CANCELLED.value
    
    @property
    def duration_days(self) -> int:
        """Get season duration in days."""
        return (self.end_date - self.start_date).days
    
    @property
    def is_registration_open(self) -> bool:
        """Check if registration is currently open."""
        if not self.registration_start or not self.registration_end:
            return False
        
        now = datetime.now(timezone.utc)
        return self.registration_start <= now <= self.registration_end
    
    @property
    def days_until_start(self) -> Optional[int]:
        """Get days until season starts (None if already started)."""
        if self.start_date <= datetime.now(timezone.utc):
            return None
        return (self.start_date - datetime.now(timezone.utc)).days
    
    @property
    def days_until_end(self) -> Optional[int]:
        """Get days until season ends (None if already ended)."""
        if self.end_date <= datetime.now(timezone.utc):
            return None
        return (self.end_date - datetime.now(timezone.utc)).days
    
    # Business logic methods
    def can_register(self) -> tuple[bool, str]:
        """Check if registration is currently allowed."""
        if self.status != SeasonStatus.UPCOMING.value:
            return False, "Registration is only allowed for upcoming seasons"
        
        if not self.is_registration_open:
            return False, "Registration period is not currently open"
        
        return True, "Registration is open"
    
    def start_season(self) -> None:
        """Start the season."""
        if self.status != SeasonStatus.UPCOMING.value:
            raise ValueError("Can only start upcoming seasons")
        
        self.status = SeasonStatus.ACTIVE.value
    
    def complete_season(self) -> None:
        """Complete the season."""
        if self.status != SeasonStatus.ACTIVE.value:
            raise ValueError("Can only complete active seasons")
        
        self.status = SeasonStatus.COMPLETED.value
    
    def cancel_season(self, reason: Optional[str] = None) -> None:
        """Cancel the season."""
        if self.status == SeasonStatus.COMPLETED.value:
            raise ValueError("Cannot cancel completed season")
        
        self.status = SeasonStatus.CANCELLED.value
    
    def set_as_current(self) -> None:
        """Set this season as the current season for its sport."""
        # Note: In a real implementation, this would also unset other current seasons
        # for the same sport, but that requires database session access
        self.is_current = True
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Season."""
        return f"<Season(id={self.id}, name='{self.name}', year={self.year}, status='{self.status}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Season to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'sport_id': str(self.sport_id),
            'year': self.year,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'registration_start': self.registration_start.isoformat() if self.registration_start else None,
            'registration_end': self.registration_end.isoformat() if self.registration_end else None,
            'status': self.status,
            'is_current': self.is_current,
            'is_upcoming': self.is_upcoming,
            'is_active': self.is_active,
            'is_completed': self.is_completed,
            'is_cancelled': self.is_cancelled,
            'duration_days': self.duration_days,
            'is_registration_open': self.is_registration_open,
            'days_until_start': self.days_until_start,
            'days_until_end': self.days_until_end,
            'max_competitions': self.max_competitions,
            'prize_pool_total': float(self.prize_pool_total),
            'season_format': self.season_format,
            'playoff_format': self.playoff_format,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Season, 'before_update')
def update_season_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)