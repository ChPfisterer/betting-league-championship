"""
Player model for the betting league championship application.

This module defines the Player model with comprehensive field validation,
profile management, and business logic as specified by the TDD tests
in backend/tests/models/test_player_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, 
    CheckConstraint, Index, ForeignKey, JSON, Numeric, Date
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone, date, timedelta
from typing import Union, Optional, Dict, Any, List
from decimal import Decimal
import uuid
import re
from enum import Enum

from .base import Base


class InjuryStatus(Enum):
    """Valid injury status values."""
    FIT = "fit"
    INJURED = "injured"
    RECOVERING = "recovering"
    DOUBTFUL = "doubtful"
    SUSPENDED = "suspended"


class PreferredFoot(Enum):
    """Valid preferred foot values."""
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


class Player(Base):
    """
    Player model for managing individual sports players/athletes.
    
    Players represent individual athletes who participate in sports competitions.
    Handles personal information, career stats, team associations, and performance data.
    """
    
    __tablename__ = 'players'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the player"
    )
    
    # Basic personal information
    first_name = Column(
        String(100),
        nullable=False,
        comment="Player's first name"
    )
    middle_name = Column(
        String(100),
        comment="Player's middle name(s)"
    )
    last_name = Column(
        String(100),
        nullable=False,
        comment="Player's last name"
    )
    display_name = Column(
        String(200),
        comment="Preferred display name for the player"
    )
    nickname = Column(
        String(100),
        comment="Player's nickname"
    )
    
    # Sport and position information
    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey('sports.id', name='fk_players_sport_id'),
        nullable=False,
        comment="ID of the sport the player participates in"
    )
    position = Column(
        String(50),
        nullable=False,
        comment="Player's position in their sport"
    )
    jersey_number = Column(
        Integer,
        nullable=False,
        comment="Player's jersey/shirt number"
    )
    
    # Personal details
    date_of_birth = Column(
        Date,
        nullable=False,
        comment="Player's date of birth"
    )
    nationality = Column(
        String(100),
        nullable=False,
        comment="Player's nationality"
    )
    
    # Physical attributes
    height_cm = Column(
        Integer,
        comment="Player's height in centimeters"
    )
    weight_kg = Column(
        Numeric(5, 2),
        comment="Player's weight in kilograms"
    )
    preferred_foot = Column(
        String(10),
        comment="Player's preferred foot (left/right/both)"
    )
    
    # Career and financial information
    market_value = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal('0.00'),
        comment="Player's estimated market value"
    )
    salary = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal('0.00'),
        comment="Player's current salary"
    )
    
    # Team association
    current_team_id = Column(
        UUID(as_uuid=True),
        ForeignKey('teams.id', name='fk_players_current_team_id'),
        comment="ID of the player's current team"
    )
    
    # Agent information
    agent_name = Column(
        String(200),
        comment="Player's agent name"
    )
    agent_contact = Column(
        String(500),
        comment="Agent contact information"
    )
    
    # Contract information
    contract_start = Column(
        Date,
        comment="Contract start date"
    )
    contract_end = Column(
        Date,
        comment="Contract end date"
    )
    
    # Status and activity
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether the player is currently active"
    )
    injury_status = Column(
        String(20),
        nullable=False,
        default=InjuryStatus.FIT.value,
        comment="Player's current injury status"
    )
    retirement_date = Column(
        Date,
        comment="Date when player retired (if applicable)"
    )
    
    # Additional information
    biography = Column(
        Text,
        comment="Player's biography or description"
    )
    social_media = Column(
        JSON,
        comment="Social media profiles and handles"
    )
    profile_image_url = Column(
        String(500),
        comment="URL to player's profile image"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the player record was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the player record was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "injury_status IN ('fit', 'injured', 'recovering', 'doubtful', 'suspended')",
            name="ck_players_injury_status"
        ),
        CheckConstraint(
            "preferred_foot IS NULL OR preferred_foot IN ('left', 'right', 'both')",
            name="ck_players_preferred_foot"
        ),
        CheckConstraint(
            "jersey_number > 0 AND jersey_number <= 999",
            name="ck_players_jersey_number"
        ),
        CheckConstraint(
            "height_cm IS NULL OR height_cm > 0",
            name="ck_players_height"
        ),
        CheckConstraint(
            "weight_kg IS NULL OR weight_kg > 0",
            name="ck_players_weight"
        ),
        CheckConstraint(
            "market_value >= 0",
            name="ck_players_market_value"
        ),
        CheckConstraint(
            "salary >= 0",
            name="ck_players_salary"
        ),
        CheckConstraint(
            "date_of_birth < CURRENT_DATE",
            name="ck_players_birth_date"
        ),
        CheckConstraint(
            "retirement_date IS NULL OR retirement_date >= date_of_birth",
            name="ck_players_retirement_date"
        ),
        CheckConstraint(
            "contract_end IS NULL OR contract_start IS NULL OR contract_end > contract_start",
            name="ck_players_contract_dates"
        ),
        CheckConstraint(
            "LENGTH(first_name) >= 1",
            name="ck_players_first_name_length"
        ),
        CheckConstraint(
            "LENGTH(last_name) >= 1",
            name="ck_players_last_name_length"
        ),
        Index('ix_players_first_name', 'first_name'),
        Index('ix_players_last_name', 'last_name'),
        Index('ix_players_sport_id', 'sport_id'),
        Index('ix_players_position', 'position'),
        Index('ix_players_jersey_number', 'jersey_number'),
        Index('ix_players_nationality', 'nationality'),
        Index('ix_players_current_team_id', 'current_team_id'),
        Index('ix_players_is_active', 'is_active'),
        Index('ix_players_injury_status', 'injury_status'),
        Index('ix_players_date_of_birth', 'date_of_birth'),
        Index('ix_players_created_at', 'created_at'),
        Index('ix_players_team_jersey', 'current_team_id', 'jersey_number'),
        {'extend_existing': True}
    )
    
    def __init__(self, **kwargs):
        """Initialize Player with proper defaults for TDD testing."""
        # Validate required fields before processing
        if 'first_name' not in kwargs or not kwargs['first_name']:
            raise ValueError("First name is required")
        
        if 'last_name' not in kwargs or not kwargs['last_name']:
            raise ValueError("Last name is required")
        
        if 'sport_id' not in kwargs or not kwargs['sport_id']:
            raise ValueError("Sport ID is required")
        
        if 'position' not in kwargs or not kwargs['position']:
            raise ValueError("Position is required")
        
        if 'jersey_number' not in kwargs or kwargs['jersey_number'] is None:
            raise ValueError("Jersey number is required")
        
        if 'date_of_birth' not in kwargs or not kwargs['date_of_birth']:
            raise ValueError("Date of birth is required")
        
        if 'nationality' not in kwargs or not kwargs['nationality']:
            raise ValueError("Nationality is required")
        
        # Set default values for testing if not provided
        if 'is_active' not in kwargs:
            kwargs['is_active'] = True
            
        if 'injury_status' not in kwargs:
            kwargs['injury_status'] = InjuryStatus.FIT.value
            
        if 'market_value' not in kwargs:
            kwargs['market_value'] = Decimal('0.00')
            
        if 'salary' not in kwargs:
            kwargs['salary'] = Decimal('0.00')
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.now(timezone.utc)
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        super().__init__(**kwargs)
    
    # Validation methods
    @validates('first_name')
    def validate_first_name(self, key: str, first_name: str) -> str:
        """Validate first name."""
        if not first_name or not first_name.strip():
            raise ValueError("First name is required")
        
        first_name = first_name.strip()
        if len(first_name) < 1:
            raise ValueError("First name must be at least 1 character long")
        
        if len(first_name) > 100:
            raise ValueError("First name cannot exceed 100 characters")
        
        return first_name
    
    @validates('last_name')
    def validate_last_name(self, key: str, last_name: str) -> str:
        """Validate last name."""
        if not last_name or not last_name.strip():
            raise ValueError("Last name is required")
        
        last_name = last_name.strip()
        if len(last_name) < 1:
            raise ValueError("Last name must be at least 1 character long")
        
        if len(last_name) > 100:
            raise ValueError("Last name cannot exceed 100 characters")
        
        return last_name
    
    @validates('sport_id')
    def validate_sport_id(self, key: str, sport_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate sport_id is provided."""
        if not sport_id:
            raise ValueError("Sport ID is required")
        return sport_id
    
    @validates('position')
    def validate_position(self, key: str, position: str) -> str:
        """Validate position."""
        if not position or not position.strip():
            raise ValueError("Position is required")
        
        position = position.strip()
        if len(position) > 50:
            raise ValueError("Position cannot exceed 50 characters")
        
        return position
    
    @validates('jersey_number')
    def validate_jersey_number(self, key: str, jersey_number: int) -> int:
        """Validate jersey number."""
        if jersey_number is None:
            raise ValueError("Jersey number is required")
        
        # Convert to int if string
        try:
            jersey_number = int(jersey_number)
        except (ValueError, TypeError):
            raise ValueError("Jersey number must be a valid integer")
        
        if jersey_number <= 0 or jersey_number > 999:
            raise ValueError("Jersey number must be between 1 and 999")
        
        return jersey_number
    
    @validates('date_of_birth')
    def validate_date_of_birth(self, key: str, date_of_birth: date) -> date:
        """Validate date of birth."""
        if not date_of_birth:
            raise ValueError("Date of birth is required")
        
        if date_of_birth >= date.today():
            raise ValueError("Date of birth must be in the past")
        
        # Check for reasonable age limits (e.g., not older than 120 years)
        if date_of_birth < date.today() - timedelta(days=120*365):
            raise ValueError("Date of birth is too far in the past")
        
        return date_of_birth
    
    @validates('nationality')
    def validate_nationality(self, key: str, nationality: str) -> str:
        """Validate nationality."""
        if not nationality or not nationality.strip():
            raise ValueError("Nationality is required")
        
        nationality = nationality.strip()
        if len(nationality) > 100:
            raise ValueError("Nationality cannot exceed 100 characters")
        
        return nationality
    
    @validates('height_cm')
    def validate_height_cm(self, key: str, height_cm: Optional[int]) -> Optional[int]:
        """Validate height in centimeters."""
        if height_cm is not None and height_cm <= 0:
            raise ValueError("Height must be greater than 0")
        return height_cm
    
    @validates('weight_kg')
    def validate_weight_kg(self, key: str, weight_kg: Optional[Decimal]) -> Optional[Decimal]:
        """Validate weight in kilograms."""
        if weight_kg is not None and weight_kg <= 0:
            raise ValueError("Weight must be greater than 0")
        return weight_kg
    
    @validates('preferred_foot')
    def validate_preferred_foot(self, key: str, preferred_foot: Optional[str]) -> Optional[str]:
        """Validate preferred foot."""
        if preferred_foot is None:
            return preferred_foot
        
        valid_feet = [foot.value for foot in PreferredFoot]
        if preferred_foot not in valid_feet:
            raise ValueError(f"Invalid preferred foot. Must be one of: {', '.join(valid_feet)}")
        
        return preferred_foot
    
    @validates('injury_status')
    def validate_injury_status(self, key: str, injury_status: str) -> str:
        """Validate injury status."""
        if not injury_status:
            raise ValueError("Injury status is required")
        
        valid_statuses = [status.value for status in InjuryStatus]
        if injury_status not in valid_statuses:
            raise ValueError(f"Invalid injury status. Must be one of: {', '.join(valid_statuses)}")
        
        return injury_status
    
    # Properties
    @property
    def full_name(self) -> str:
        """Get player's full name."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def short_name(self) -> str:
        """Get player's short name (first initial + last name)."""
        return f"{self.first_name[0]}. {self.last_name}"
    
    @property
    def preferred_name(self) -> str:
        """Get player's preferred display name or full name."""
        return self.display_name or self.full_name
    
    @property
    def age(self) -> int:
        """Calculate player's current age."""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def is_injured(self) -> bool:
        """Check if player is currently injured."""
        return self.injury_status in [InjuryStatus.INJURED.value, InjuryStatus.RECOVERING.value]
    
    @property
    def is_available(self) -> bool:
        """Check if player is available for selection."""
        return (self.is_active and 
                self.injury_status not in [InjuryStatus.INJURED.value, InjuryStatus.SUSPENDED.value])
    
    @property
    def is_retired(self) -> bool:
        """Check if player is retired."""
        return self.retirement_date is not None and self.retirement_date <= date.today()
    
    @property
    def has_contract(self) -> bool:
        """Check if player currently has a contract."""
        if not self.contract_start or not self.contract_end:
            return False
        
        today = date.today()
        return self.contract_start <= today <= self.contract_end
    
    @property
    def contract_expires_soon(self) -> bool:
        """Check if contract expires within 6 months."""
        if not self.has_contract:
            return False
        
        six_months_from_now = date.today() + timedelta(days=180)
        return self.contract_end <= six_months_from_now
    
    @property
    def bmi(self) -> Optional[float]:
        """Calculate player's BMI if height and weight are available."""
        if not self.height_cm or not self.weight_kg:
            return None
        
        height_m = float(self.height_cm) / 100
        return float(self.weight_kg) / (height_m ** 2)
    
    @property
    def display_name_or_full(self) -> str:
        """Get display name or fall back to full name."""
        return self.display_name or self.full_name
    
    @property
    def is_under_contract(self) -> bool:
        """Alias for has_contract property for test compatibility."""
        return self.has_contract
    
    # Business logic methods
    def set_injury_status(self, status: str, description: Optional[str] = None) -> None:
        """Update player's injury status."""
        valid_statuses = [status.value for status in InjuryStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid injury status. Must be one of: {', '.join(valid_statuses)}")
        
        self.injury_status = status
    
    def retire(self, retirement_date: Optional[date] = None) -> None:
        """Retire the player."""
        if retirement_date is None:
            retirement_date = date.today()
        
        if retirement_date < self.date_of_birth:
            raise ValueError("Retirement date cannot be before birth date")
        
        self.retirement_date = retirement_date
        self.is_active = False
    
    def transfer_to_team(self, team_id: Union[str, uuid.UUID]) -> None:
        """Transfer player to a new team."""
        if not team_id:
            raise ValueError("Team ID is required")
        
        self.current_team_id = team_id
    
    def release_from_team(self) -> None:
        """Release player from current team."""
        self.current_team_id = None
    
    def get_statistics(self, season_id: Optional[Union[str, uuid.UUID]] = None):
        """Get player statistics for a season or overall."""
        # This would typically query a statistics table
        # For now, return empty dict as placeholder
        return {}
    
    def get_career_stats(self):
        """Get player's career statistics."""
        # This would typically aggregate statistics across all seasons
        # For now, return empty dict as placeholder
        return {}
    
    def update_injury_status(self, status: str, description: Optional[str] = None):
        """Update player's injury status with optional description."""
        self.set_injury_status(status, description)
    
    def retire(self, retirement_date: Optional[date] = None) -> None:
        """Retire the player."""
        if retirement_date is None:
            retirement_date = date.today()
        
        if retirement_date < self.date_of_birth:
            raise ValueError("Retirement date cannot be before birth date")
        
        self.retirement_date = retirement_date
        self.is_active = False
    
    def update_contract(self, start_date: date, end_date: date) -> None:
        """Update player's contract dates."""
        if start_date >= end_date:
            raise ValueError("Contract end date must be after start date")
        
        self.contract_start = start_date
        self.contract_end = end_date
    
    # Class methods for queries
    @classmethod
    def search_by_name(cls, db_session, search_term: str):
        """Search players by name."""
        search_pattern = f"%{search_term}%"
        return db_session.query(cls).filter(
            (cls.first_name.ilike(search_pattern)) |
            (cls.last_name.ilike(search_pattern)) |
            (cls.display_name.ilike(search_pattern))
        ).all()
    
    @classmethod
    def get_by_position(cls, db_session, position: str):
        """Get players by position."""
        return db_session.query(cls).filter(cls.position == position).all()
    
    @classmethod
    def get_by_team(cls, db_session, team_id: Union[str, uuid.UUID]):
        """Get players by team."""
        return db_session.query(cls).filter(cls.current_team_id == team_id).all()
    
    @classmethod
    def get_by_nationality(cls, db_session, nationality: str):
        """Get players by nationality."""
        return db_session.query(cls).filter(cls.nationality == nationality).all()
    
    @classmethod
    def get_available(cls, db_session):
        """Get available players (active and not injured/suspended)."""
        return db_session.query(cls).filter(
            cls.is_active == True,
            cls.injury_status.in_([InjuryStatus.FIT.value, InjuryStatus.DOUBTFUL.value])
        ).all()
    
    # Additional business logic methods
    def can_play_position(self, position: str) -> bool:
        """Check if player can play a specific position."""
        # Basic implementation - player can play their primary position
        return self.position.lower() == position.lower()
    
    def is_jersey_available(self, team_id: Union[str, uuid.UUID], jersey_number: int) -> bool:
        """Check if a jersey number is available for a team."""
        # Placeholder implementation - would check database for conflicts
        return jersey_number != self.jersey_number
    
    def is_eligible_for_competition(self, competition_id: Union[str, uuid.UUID]) -> bool:
        """Check if player is eligible for a competition."""
        # Basic implementation - active players are eligible
        return self.is_active and self.is_available
    
    def can_transfer(self) -> bool:
        """Check if player can be transferred."""
        # Basic implementation - active players not under long-term injury can transfer
        return self.is_active and self.injury_status != InjuryStatus.INJURED.value
    
    def is_within_salary_cap(self, team_salary_cap: Decimal) -> bool:
        """Check if player salary is within team salary cap."""
        return self.salary <= team_salary_cap
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Player."""
        return f"<Player(id={self.id}, name='{self.full_name}', position='{self.position}', #{self.jersey_number})>"
    
    def to_dict(self, include_sport: bool = False, include_team: bool = False, 
                include_statistics: bool = False, include_career: bool = False) -> Dict[str, Any]:
        """Convert Player to dictionary with optional related data."""
        result = {
            'id': str(self.id),
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'short_name': self.short_name,
            'preferred_name': self.preferred_name,
            'display_name': self.display_name,
            'nickname': self.nickname,
            'sport_id': str(self.sport_id),
            'position': self.position,
            'jersey_number': self.jersey_number,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'nationality': self.nationality,
            'height_cm': self.height_cm,
            'weight_kg': float(self.weight_kg) if self.weight_kg else None,
            'bmi': self.bmi,
            'preferred_foot': self.preferred_foot,
            'market_value': float(self.market_value),
            'salary': float(self.salary),
            'current_team_id': str(self.current_team_id) if self.current_team_id else None,
            'agent_name': self.agent_name,
            'agent_contact': self.agent_contact,
            'contract_start': self.contract_start.isoformat() if self.contract_start else None,
            'contract_end': self.contract_end.isoformat() if self.contract_end else None,
            'has_contract': self.has_contract,
            'contract_expires_soon': self.contract_expires_soon,
            'is_active': self.is_active,
            'injury_status': self.injury_status,
            'is_injured': self.is_injured,
            'is_available': self.is_available,
            'is_retired': self.is_retired,
            'retirement_date': self.retirement_date.isoformat() if self.retirement_date else None,
            'biography': self.biography,
            'social_media': self.social_media,
            'profile_image_url': self.profile_image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        # Add optional related data
        if include_sport and hasattr(self, 'sport') and self.sport:
            result['sport'] = self.sport.to_dict() if hasattr(self.sport, 'to_dict') else str(self.sport)
        
        if include_team and hasattr(self, 'current_team') and self.current_team:
            result['current_team'] = self.current_team.to_dict() if hasattr(self.current_team, 'to_dict') else str(self.current_team)
        
        if include_statistics and hasattr(self, 'statistics'):
            result['statistics'] = [stat.to_dict() if hasattr(stat, 'to_dict') else str(stat) for stat in self.statistics]
        
        if include_career and hasattr(self, 'career_history'):
            result['career_history'] = [career.to_dict() if hasattr(career, 'to_dict') else str(career) for career in self.career_history]
        
        return result


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Player, 'before_update')
def update_player_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)