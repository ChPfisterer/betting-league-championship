"""
Team model for the betting league championship application.

This module defines the Team model with comprehensive field validation,
roster management, and business logic as specified by the TDD tests
in backend/tests/models/test_team_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, 
    CheckConstraint, Index, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone
from typing import Union, Optional, Dict, Any, List
import uuid
import re
from enum import Enum

from .base import Base


class Team(Base):
    """
    Team model for representing sports teams in competitions.
    
    Teams belong to specific sports and participate in leagues/competitions,
    maintaining rosters of players and performance statistics.
    """
    
    __tablename__ = 'teams'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the team"
    )
    
    # Basic information
    name = Column(
        String(100),
        nullable=False,
        comment="Full team name"
    )
    slug = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="URL-friendly team identifier"
    )
    short_name = Column(
        String(20),
        comment="Abbreviated team name (e.g., 'MAN UTD')"
    )
    
    # Sport association
    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey('sports.id', name='fk_teams_sport_id'),
        nullable=False,
        comment="ID of the sport this team plays"
    )
    
    # Status
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether team is active for competitions"
    )
    
    # Descriptive information
    description = Column(
        Text,
        comment="Team description and history"
    )
    
    # Visual branding
    logo_url = Column(
        String(500),
        comment="URL to team logo"
    )
    banner_url = Column(
        String(500),
        comment="URL to team banner image"
    )
    primary_color = Column(
        String(7),
        comment="Primary team color (hex format)"
    )
    secondary_color = Column(
        String(7),
        comment="Secondary team color (hex format)"
    )
    
    # Historical information
    founded_year = Column(
        Integer,
        comment="Year the team was founded"
    )
    
    # Location and venue
    home_venue = Column(
        String(100),
        comment="Name of team's home venue"
    )
    country = Column(
        String(50),
        comment="Country where team is based"
    )
    city = Column(
        String(50),
        comment="City where team is based"
    )
    
    # Online presence
    website = Column(
        String(200),
        comment="Team's official website"
    )
    social_links = Column(
        JSON,
        comment="Social media links (Twitter, Instagram, etc.)"
    )
    
    # Team management
    coach_name = Column(
        String(100),
        comment="Name of the head coach"
    )
    captain_id = Column(
        UUID(as_uuid=True),
        ForeignKey('players.id', name='fk_teams_captain_id'),
        comment="ID of the team captain"
    )
    
    # Roster configuration
    max_players = Column(
        Integer,
        nullable=False,
        default=25,
        comment="Maximum number of players allowed"
    )
    
    # League and competition status
    current_league = Column(
        String(100),
        comment="Current league or division"
    )
    league_position = Column(
        Integer,
        comment="Current position in league standings"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the team was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the team was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "max_players > 0",
            name="ck_teams_max_players"
        ),
        CheckConstraint(
            "founded_year > 1800",
            name="ck_teams_founded_year"
        ),
        CheckConstraint(
            "league_position > 0",
            name="ck_teams_league_position"
        ),
        CheckConstraint(
            "LENGTH(name) >= 2",
            name="ck_teams_name_length"
        ),
        CheckConstraint(
            "LENGTH(slug) >= 2",
            name="ck_teams_slug_length"
        ),
        CheckConstraint(
            "primary_color ~ '^#[0-9A-Fa-f]{6}$'",
            name="ck_teams_primary_color_format"
        ),
        CheckConstraint(
            "secondary_color ~ '^#[0-9A-Fa-f]{6}$'",
            name="ck_teams_secondary_color_format"
        ),
        Index('ix_teams_name', 'name'),
        Index('ix_teams_slug', 'slug'),
        Index('ix_teams_sport_id', 'sport_id'),
        Index('ix_teams_is_active', 'is_active'),
        Index('ix_teams_country', 'country'),
        Index('ix_teams_current_league', 'current_league'),
        Index('ix_teams_created_at', 'created_at'),
    )
    
    def __init__(self, **kwargs):
        """Initialize Team with proper defaults for TDD testing."""
        # Set default values for testing if not provided
        if 'is_active' not in kwargs:
            kwargs['is_active'] = True
            
        if 'max_players' not in kwargs:
            kwargs['max_players'] = 25
            
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
        """Generate URL-friendly slug from team name."""
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
        """Validate team name."""
        if not name:
            raise ValueError("Team name is required")
        
        name = name.strip()
        if len(name) < 2:
            raise ValueError("Team name must be at least 2 characters long")
        
        if len(name) > 100:
            raise ValueError("Team name cannot exceed 100 characters")
        
        # Check for basic format
        if not re.match(r'^[a-zA-Z0-9\s\-\'\.&]+$', name):
            raise ValueError("Team name contains invalid characters")
        
        return name
    
    @validates('slug')
    def validate_slug(self, key: str, slug: str) -> str:
        """Validate team slug."""
        if not slug:
            raise ValueError("Team slug is required")
        
        slug = slug.lower().strip()
        if len(slug) < 2:
            raise ValueError("Team slug must be at least 2 characters long")
        
        if len(slug) > 50:
            raise ValueError("Team slug cannot exceed 50 characters")
        
        # Must be URL-friendly
        if not re.match(r'^[a-z0-9-]+$', slug):
            raise ValueError("Team slug can only contain lowercase letters, numbers, and hyphens")
        
        if slug.startswith('-') or slug.endswith('-'):
            raise ValueError("Team slug cannot start or end with hyphen")
        
        if '--' in slug:
            raise ValueError("Team slug cannot contain consecutive hyphens")
        
        return slug
    
    @validates('short_name')
    def validate_short_name(self, key: str, short_name: Optional[str]) -> Optional[str]:
        """Validate team short name."""
        if not short_name:
            return short_name
        
        short_name = short_name.strip().upper()
        if len(short_name) > 20:
            raise ValueError("Short name cannot exceed 20 characters")
        
        if not re.match(r'^[A-Z0-9\s]+$', short_name):
            raise ValueError("Short name can only contain uppercase letters, numbers, and spaces")
        
        return short_name
    
    @validates('max_players')
    def validate_max_players(self, key: str, max_players: int) -> int:
        """Validate maximum players count."""
        if max_players <= 0:
            raise ValueError("Maximum players must be greater than 0")
        
        if max_players > 100:
            raise ValueError("Maximum players cannot exceed 100")
        
        return max_players
    
    @validates('founded_year')
    def validate_founded_year(self, key: str, founded_year: Optional[int]) -> Optional[int]:
        """Validate team founding year."""
        if founded_year is None:
            return founded_year
        
        current_year = datetime.now().year
        if founded_year < 1800:
            raise ValueError("Founded year cannot be before 1800")
        
        if founded_year > current_year:
            raise ValueError("Founded year cannot be in the future")
        
        return founded_year
    
    @validates('primary_color', 'secondary_color')
    def validate_color(self, key: str, color: Optional[str]) -> Optional[str]:
        """Validate color format (hex)."""
        if not color:
            return color
        
        color = color.strip().upper()
        if not re.match(r'^#[0-9A-F]{6}$', color):
            raise ValueError("Color must be in hex format (#RRGGBB)")
        
        return color
    
    @validates('league_position')
    def validate_league_position(self, key: str, league_position: Optional[int]) -> Optional[int]:
        """Validate league position."""
        if league_position is None:
            return league_position
        
        if league_position <= 0:
            raise ValueError("League position must be positive")
        
        return league_position
    
    @validates('website')
    def validate_website(self, key: str, website: Optional[str]) -> Optional[str]:
        """Validate website URL format."""
        if not website:
            return website
        
        website = website.strip()
        if not re.match(r'^https?://.+', website):
            raise ValueError("Website must be a valid HTTP/HTTPS URL")
        
        return website
    
    # Properties
    @property
    def display_name(self) -> str:
        """Get display name (short name if available, otherwise full name)."""
        return self.short_name or self.name
    
    @property
    def age(self) -> Optional[int]:
        """Get team age in years."""
        if not self.founded_year:
            return None
        return datetime.now().year - self.founded_year
    
    @property
    def has_captain(self) -> bool:
        """Check if team has a designated captain."""
        return self.captain_id is not None
    
    @property
    def current_players_count(self) -> int:
        """Get current number of players (will be implemented with relationships)."""
        # This will be implemented when Player relationships are added
        return 0
    
    @property
    def has_full_roster(self) -> bool:
        """Check if team has reached maximum players."""
        return self.current_players_count >= self.max_players
    
    @property
    def location(self) -> Optional[str]:
        """Get formatted location string."""
        if self.city and self.country:
            return f"{self.city}, {self.country}"
        elif self.city:
            return self.city
        elif self.country:
            return self.country
        return None
    
    # Business logic methods
    def can_add_player(self) -> tuple[bool, str]:
        """Check if team can add another player."""
        if not self.is_active:
            return False, "Team is not active"
        
        if self.has_full_roster:
            return False, "Team roster is full"
        
        return True, "Can add player"
    
    def update_league_position(self, position: int) -> None:
        """Update team's league position."""
        if position <= 0:
            raise ValueError("League position must be positive")
        
        self.league_position = position
    
    def set_captain(self, player_id: str) -> None:
        """Set team captain."""
        # Validation will be added when Player relationships are implemented
        self.captain_id = uuid.UUID(player_id)
    
    def get_social_link(self, platform: str) -> Optional[str]:
        """Get social media link for specific platform."""
        if not self.social_links or not isinstance(self.social_links, dict):
            return None
        
        return self.social_links.get(platform.lower())
    
    def set_social_link(self, platform: str, url: str) -> None:
        """Set social media link for specific platform."""
        if not self.social_links:
            self.social_links = {}
        
        if not isinstance(self.social_links, dict):
            self.social_links = {}
        
        self.social_links[platform.lower()] = url
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get team performance statistics."""
        # This will be implemented when Match/Result relationships are added
        return {
            'matches_played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'win_percentage': 0.0
        }
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Team."""
        return f"<Team(id={self.id}, name='{self.name}', sport_id={self.sport_id})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Team to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'short_name': self.short_name,
            'display_name': self.display_name,
            'sport_id': str(self.sport_id),
            'is_active': self.is_active,
            'description': self.description,
            'logo_url': self.logo_url,
            'banner_url': self.banner_url,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'founded_year': self.founded_year,
            'age': self.age,
            'home_venue': self.home_venue,
            'country': self.country,
            'city': self.city,
            'location': self.location,
            'website': self.website,
            'social_links': self.social_links,
            'coach_name': self.coach_name,
            'captain_id': str(self.captain_id) if self.captain_id else None,
            'max_players': self.max_players,
            'current_players_count': self.current_players_count,
            'has_full_roster': self.has_full_roster,
            'current_league': self.current_league,
            'league_position': self.league_position,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Team, 'before_update')
def update_team_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)