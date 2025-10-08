"""
Sport model for the betting league championship application.

This module defines the Sport model with comprehensive field validation,
category management, and business logic as specified by the TDD tests
in backend/tests/models/test_sport_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, 
    CheckConstraint, Index, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone
from typing import Union, Optional, Dict, Any, List
import uuid
import re
from enum import Enum

from .base import Base


class SportCategory(Enum):
    """Valid sport categories."""
    TEAM_SPORT = "team_sport"
    INDIVIDUAL_SPORT = "individual_sport"
    COMBAT_SPORT = "combat_sport"
    RACING = "racing"
    WATER_SPORT = "water_sport"
    WINTER_SPORT = "winter_sport"
    ESPORT = "esport"


class Sport(Base):
    """
    Sport model for defining different sports and their characteristics.
    
    Sports serve as the foundation for competitions and matches,
    defining rules, scoring systems, and betting types.
    """
    
    __tablename__ = 'sports'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the sport"
    )
    
    # Basic information
    name = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="Sport name (e.g., 'Football', 'Basketball')"
    )
    slug = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="URL-friendly sport identifier"
    )
    category = Column(
        String(20),
        nullable=False,
        comment="Sport category classification"
    )
    
    # Status
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether sport is active for betting"
    )
    
    # Optional descriptive fields
    description = Column(
        Text,
        comment="Detailed description of the sport"
    )
    rules = Column(
        Text,
        comment="Sport rules and regulations"
    )
    icon_url = Column(
        String(500),
        comment="URL to sport icon/logo"
    )
    color_scheme = Column(
        String(50),
        comment="Color scheme for UI representation"
    )
    
    # Betting and game configuration
    default_bet_types = Column(
        JSON,
        comment="Default betting types available for this sport"
    )
    scoring_system = Column(
        JSON,
        comment="Scoring system configuration"
    )
    match_duration = Column(
        Integer,
        comment="Typical match duration in minutes"
    )
    season_structure = Column(
        JSON,
        comment="Season structure and schedule information"
    )
    
    # Analytics
    popularity_score = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Popularity score for ranking sports"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the sport was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the sport was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "category IN ('team_sport', 'individual_sport', 'combat_sport', 'racing', 'water_sport', 'winter_sport', 'esport')",
            name="ck_sports_category"
        ),
        CheckConstraint(
            "popularity_score >= 0",
            name="ck_sports_popularity_score"
        ),
        CheckConstraint(
            "match_duration > 0",
            name="ck_sports_match_duration"
        ),
        CheckConstraint(
            "LENGTH(name) >= 2",
            name="ck_sports_name_length"
        ),
        CheckConstraint(
            "LENGTH(slug) >= 2",
            name="ck_sports_slug_length"
        ),
        Index('ix_sports_name', 'name'),
        Index('ix_sports_slug', 'slug'),
        Index('ix_sports_category', 'category'),
        Index('ix_sports_is_active', 'is_active'),
        Index('ix_sports_popularity_score', 'popularity_score'),
        Index('ix_sports_created_at', 'created_at'),
    )
    
    # Relationships
    teams = relationship("Team", back_populates="sport")
    competitions = relationship("Competition", back_populates="sport")
    seasons = relationship("Season", back_populates="sport")
    
    def __init__(self, **kwargs):
        """Initialize Sport with proper defaults for TDD testing."""
        # Set default values for testing if not provided
        if 'is_active' not in kwargs:
            kwargs['is_active'] = True
            
        if 'popularity_score' not in kwargs:
            kwargs['popularity_score'] = 0
            
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
        """Generate URL-friendly slug from sport name."""
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
        """Validate sport name."""
        if not name:
            raise ValueError("Sport name is required")
        
        name = name.strip()
        if len(name) < 2:
            raise ValueError("Sport name must be at least 2 characters long")
        
        if len(name) > 100:
            raise ValueError("Sport name cannot exceed 100 characters")
        
        # Check for basic format
        if not re.match(r'^[a-zA-Z0-9\s\-\'\.]+$', name):
            raise ValueError("Sport name contains invalid characters")
        
        return name
    
    @validates('slug')
    def validate_slug(self, key: str, slug: str) -> str:
        """Validate sport slug."""
        if not slug:
            raise ValueError("Sport slug is required")
        
        slug = slug.lower().strip()
        if len(slug) < 2:
            raise ValueError("Sport slug must be at least 2 characters long")
        
        if len(slug) > 50:
            raise ValueError("Sport slug cannot exceed 50 characters")
        
        # Must be URL-friendly
        if not re.match(r'^[a-z0-9-]+$', slug):
            raise ValueError("Sport slug can only contain lowercase letters, numbers, and hyphens")
        
        if slug.startswith('-') or slug.endswith('-'):
            raise ValueError("Sport slug cannot start or end with hyphen")
        
        if '--' in slug:
            raise ValueError("Sport slug cannot contain consecutive hyphens")
        
        return slug
    
    @validates('category')
    def validate_category(self, key: str, category: str) -> str:
        """Validate sport category."""
        if not category:
            raise ValueError("Sport category is required")
        
        valid_categories = [cat.value for cat in SportCategory]
        if category not in valid_categories:
            raise ValueError(f"Invalid sport category. Must be one of: {', '.join(valid_categories)}")
        
        return category
    
    @validates('popularity_score')
    def validate_popularity_score(self, key: str, popularity_score: int) -> int:
        """Validate popularity score."""
        if popularity_score < 0:
            raise ValueError("Popularity score cannot be negative")
        
        if popularity_score > 1000:
            raise ValueError("Popularity score cannot exceed 1000")
        
        return popularity_score
    
    @validates('match_duration')
    def validate_match_duration(self, key: str, match_duration: Optional[int]) -> Optional[int]:
        """Validate match duration."""
        if match_duration is None:
            return match_duration
        
        if match_duration <= 0:
            raise ValueError("Match duration must be positive")
        
        if match_duration > 1440:  # 24 hours
            raise ValueError("Match duration cannot exceed 1440 minutes (24 hours)")
        
        return match_duration
    
    @validates('color_scheme')
    def validate_color_scheme(self, key: str, color_scheme: Optional[str]) -> Optional[str]:
        """Validate color scheme format."""
        if not color_scheme:
            return color_scheme
        
        color_scheme = color_scheme.strip()
        
        # Basic validation for common color formats
        if not re.match(r'^(#[0-9A-Fa-f]{6}|[a-zA-Z]+|rgb\(\d+,\s*\d+,\s*\d+\))$', color_scheme):
            raise ValueError("Invalid color scheme format")
        
        return color_scheme
    
    # Properties
    @property
    def is_team_sport(self) -> bool:
        """Check if this is a team sport."""
        return self.category == SportCategory.TEAM_SPORT.value
    
    @property
    def is_individual_sport(self) -> bool:
        """Check if this is an individual sport."""
        return self.category == SportCategory.INDIVIDUAL_SPORT.value
    
    @property
    def formatted_duration(self) -> Optional[str]:
        """Get formatted match duration string."""
        if not self.match_duration:
            return None
        
        hours = self.match_duration // 60
        minutes = self.match_duration % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
        else:
            return f"{minutes}m"
    
    # Business logic methods
    def get_default_bet_types(self) -> List[str]:
        """Get list of default bet types for this sport."""
        if self.default_bet_types and isinstance(self.default_bet_types, list):
            return self.default_bet_types
        
        # Default bet types based on category
        if self.is_team_sport:
            return ['match_winner', 'total_points', 'spread']
        elif self.is_individual_sport:
            return ['winner', 'podium_finish', 'head_to_head']
        else:
            return ['winner', 'over_under']
    
    def configure_scoring_system(self, config: Dict[str, Any]) -> None:
        """Configure sport-specific scoring system."""
        required_keys = ['type', 'rules']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required scoring configuration key: {key}")
        
        self.scoring_system = config
    
    def update_popularity(self, delta: int) -> None:
        """Update popularity score by delta amount."""
        new_score = max(0, self.popularity_score + delta)
        self.popularity_score = min(1000, new_score)
    
    def can_create_competition(self) -> tuple[bool, str]:
        """Check if competitions can be created for this sport."""
        if not self.is_active:
            return False, "Sport is not active"
        
        return True, "Can create competition"
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Sport."""
        return f"<Sport(id={self.id}, name='{self.name}', category='{self.category}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Sport to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'category': self.category,
            'is_active': self.is_active,
            'description': self.description,
            'rules': self.rules,
            'icon_url': self.icon_url,
            'color_scheme': self.color_scheme,
            'default_bet_types': self.default_bet_types,
            'scoring_system': self.scoring_system,
            'match_duration': self.match_duration,
            'formatted_duration': self.formatted_duration,
            'season_structure': self.season_structure,
            'popularity_score': self.popularity_score,
            'is_team_sport': self.is_team_sport,
            'is_individual_sport': self.is_individual_sport,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Sport, 'before_update')
def update_sport_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)