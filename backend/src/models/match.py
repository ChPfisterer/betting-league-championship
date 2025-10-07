"""
Match model for the betting league championship application.

This module defines the Match model with comprehensive field validation,
match scheduling, scoring, and business logic as specified by the TDD tests
in backend/tests/models/test_match_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, 
    CheckConstraint, Index, ForeignKey, JSON, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone, timedelta
from typing import Union, Optional, Dict, Any, List, Tuple
from decimal import Decimal
import uuid
import re
from enum import Enum

from .base import Base


class MatchStatus(Enum):
    """Valid match status values."""
    SCHEDULED = "scheduled"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"
    LIVE = "live"
    HALFTIME = "halftime"
    EXTRA_TIME = "extra_time"
    PENALTIES = "penalties"
    FINISHED = "finished"


class Match(Base):
    """
    Match model for managing individual sports matches/games.
    
    Matches belong to competitions and feature two teams competing against
    each other. Handles scheduling, scoring, live updates, and betting.
    """
    
    __tablename__ = 'matches'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the match"
    )
    
    # Competition and team associations
    competition_id = Column(
        UUID(as_uuid=True),
        ForeignKey('competitions.id', name='fk_matches_competition_id'),
        nullable=False,
        comment="ID of the competition this match belongs to"
    )
    home_team_id = Column(
        UUID(as_uuid=True),
        ForeignKey('teams.id', name='fk_matches_home_team_id'),
        nullable=False,
        comment="ID of the home team"
    )
    away_team_id = Column(
        UUID(as_uuid=True),
        ForeignKey('teams.id', name='fk_matches_away_team_id'),
        nullable=False,
        comment="ID of the away team"
    )
    
    # Match scheduling and timing
    scheduled_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="When the match is scheduled to start"
    )
    started_at = Column(
        DateTime(timezone=True),
        comment="When the match actually started"
    )
    finished_at = Column(
        DateTime(timezone=True),
        comment="When the match finished"
    )
    betting_closes_at = Column(
        DateTime(timezone=True),
        comment="When betting closes for this match"
    )
    
    # Match organization
    round_number = Column(
        Integer,
        comment="Round number in the competition"
    )
    match_day = Column(
        Integer,
        comment="Match day number"
    )
    venue = Column(
        String(200),
        comment="Venue where the match is played"
    )
    referee = Column(
        String(100),
        comment="Match referee"
    )
    
    # Match status and state
    status = Column(
        String(20),
        nullable=False,
        default=MatchStatus.SCHEDULED.value,
        comment="Current match status"
    )
    
    # Scoring
    home_score = Column(
        Integer,
        comment="Home team score in regular time"
    )
    away_score = Column(
        Integer,
        comment="Away team score in regular time"
    )
    extra_time_home_score = Column(
        Integer,
        comment="Home team score in extra time"
    )
    extra_time_away_score = Column(
        Integer,
        comment="Away team score in extra time"
    )
    penalties_home_score = Column(
        Integer,
        comment="Home team penalty shootout score"
    )
    penalties_away_score = Column(
        Integer,
        comment="Away team penalty shootout score"
    )
    
    # Match data
    match_events = Column(
        JSON,
        comment="Match events (goals, cards, substitutions, etc.)"
    )
    weather_conditions = Column(
        String(100),
        comment="Weather conditions during the match"
    )
    attendance = Column(
        Integer,
        comment="Number of spectators"
    )
    
    # Betting and odds
    live_odds = Column(
        JSON,
        comment="Live betting odds during the match"
    )
    
    # Additional information
    notes = Column(
        Text,
        comment="Additional match notes"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the match was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the match was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('scheduled', 'postponed', 'cancelled', 'live', 'halftime', 'extra_time', 'penalties', 'finished')",
            name="ck_matches_status"
        ),
        CheckConstraint(
            "home_team_id != away_team_id",
            name="ck_matches_different_teams"
        ),
        CheckConstraint(
            "home_score IS NULL OR home_score >= 0",
            name="ck_matches_home_score"
        ),
        CheckConstraint(
            "away_score IS NULL OR away_score >= 0",
            name="ck_matches_away_score"
        ),
        CheckConstraint(
            "extra_time_home_score IS NULL OR extra_time_home_score >= 0",
            name="ck_matches_extra_time_home_score"
        ),
        CheckConstraint(
            "extra_time_away_score IS NULL OR extra_time_away_score >= 0",
            name="ck_matches_extra_time_away_score"
        ),
        CheckConstraint(
            "penalties_home_score IS NULL OR penalties_home_score >= 0",
            name="ck_matches_penalties_home_score"
        ),
        CheckConstraint(
            "penalties_away_score IS NULL OR penalties_away_score >= 0",
            name="ck_matches_penalties_away_score"
        ),
        CheckConstraint(
            "attendance IS NULL OR attendance >= 0",
            name="ck_matches_attendance"
        ),
        CheckConstraint(
            "round_number IS NULL OR round_number > 0",
            name="ck_matches_round_number"
        ),
        CheckConstraint(
            "match_day IS NULL OR match_day > 0",
            name="ck_matches_match_day"
        ),
        CheckConstraint(
            "finished_at IS NULL OR started_at IS NULL OR finished_at > started_at",
            name="ck_matches_finish_after_start"
        ),
        Index('ix_matches_competition_id', 'competition_id'),
        Index('ix_matches_home_team_id', 'home_team_id'),
        Index('ix_matches_away_team_id', 'away_team_id'),
        Index('ix_matches_status', 'status'),
        Index('ix_matches_scheduled_at', 'scheduled_at'),
        Index('ix_matches_started_at', 'started_at'),
        Index('ix_matches_created_at', 'created_at'),
        Index('ix_matches_competition_teams', 'competition_id', 'home_team_id', 'away_team_id'),
    )
    
    # Relationships
    competition = relationship("Competition", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    
    def __init__(self, **kwargs):
        """Initialize Match with proper defaults for TDD testing."""
        # Validate required fields before processing
        if 'competition_id' not in kwargs or not kwargs['competition_id']:
            raise ValueError("Competition ID is required")
        
        if 'home_team_id' not in kwargs or not kwargs['home_team_id']:
            raise ValueError("Home team ID is required")
        
        if 'away_team_id' not in kwargs or not kwargs['away_team_id']:
            raise ValueError("Away team ID is required")
        
        if 'scheduled_at' not in kwargs or not kwargs['scheduled_at']:
            raise ValueError("Scheduled time is required")
        
        # Validate teams are different
        if kwargs.get('home_team_id') == kwargs.get('away_team_id'):
            raise ValueError("Home team and away team must be different")
        
        # Handle datetime validation
        started_at = kwargs.get('started_at')
        finished_at = kwargs.get('finished_at')
        scheduled_at = kwargs.get('scheduled_at')
        
        if started_at and scheduled_at and started_at < scheduled_at:
            raise ValueError("Started time cannot be before scheduled time")
        
        if finished_at and started_at and finished_at <= started_at:
            raise ValueError("Finished time must be after started time")
        
        # Set default values for testing if not provided
        if 'status' not in kwargs:
            kwargs['status'] = MatchStatus.SCHEDULED.value
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.now(timezone.utc)
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        # Set default betting closes time if not provided
        if 'betting_closes_at' not in kwargs and 'scheduled_at' in kwargs:
            # Default to 15 minutes before scheduled time
            kwargs['betting_closes_at'] = kwargs['scheduled_at'] - timedelta(minutes=15)
            
        super().__init__(**kwargs)
    
    # Validation methods
    @validates('competition_id')
    def validate_competition_id(self, key: str, competition_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate competition_id is provided."""
        if not competition_id:
            raise ValueError("Competition ID is required")
        return competition_id
    
    @validates('home_team_id')
    def validate_home_team_id(self, key: str, home_team_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate home_team_id is provided."""
        if not home_team_id:
            raise ValueError("Home team ID is required")
        return home_team_id
    
    @validates('away_team_id')
    def validate_away_team_id(self, key: str, away_team_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate away_team_id is provided and different from home team."""
        if not away_team_id:
            raise ValueError("Away team ID is required")
        
        if hasattr(self, 'home_team_id') and self.home_team_id == away_team_id:
            raise ValueError("Away team must be different from home team")
        
        return away_team_id
    
    @validates('scheduled_at')
    def validate_scheduled_at(self, key: str, scheduled_at: datetime) -> datetime:
        """Validate scheduled time."""
        if not scheduled_at:
            raise ValueError("Scheduled time is required")
        
        # Check if started_at is already set and validate order
        if hasattr(self, 'started_at') and self.started_at and scheduled_at > self.started_at:
            raise ValueError("Scheduled time cannot be after started time")
        
        return scheduled_at
    
    @validates('started_at')
    def validate_started_at(self, key: str, started_at: Optional[datetime]) -> Optional[datetime]:
        """Validate started time."""
        if started_at is None:
            return started_at
        
        # Check against scheduled time
        if hasattr(self, 'scheduled_at') and self.scheduled_at and started_at < self.scheduled_at:
            raise ValueError("Started time cannot be before scheduled time")
        
        # Check against finished time
        if hasattr(self, 'finished_at') and self.finished_at and started_at >= self.finished_at:
            raise ValueError("Started time must be before finished time")
        
        return started_at
    
    @validates('finished_at')
    def validate_finished_at(self, key: str, finished_at: Optional[datetime]) -> Optional[datetime]:
        """Validate finished time."""
        if finished_at is None:
            return finished_at
        
        # Check against started time
        if hasattr(self, 'started_at') and self.started_at and finished_at <= self.started_at:
            raise ValueError("Finished time must be after started time")
        
        return finished_at
    
    @validates('status')
    def validate_status(self, key: str, status: str) -> str:
        """Validate match status."""
        if not status:
            raise ValueError("Status is required")
        
        valid_statuses = [status.value for status in MatchStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        return status
    
    @validates('home_score', 'away_score', 'extra_time_home_score', 'extra_time_away_score', 
               'penalties_home_score', 'penalties_away_score')
    def validate_scores(self, key: str, score: Optional[int]) -> Optional[int]:
        """Validate score values."""
        if score is not None and score < 0:
            raise ValueError("Scores cannot be negative")
        return score
    
    @validates('attendance', 'round_number', 'match_day')
    def validate_positive_integers(self, key: str, value: Optional[int]) -> Optional[int]:
        """Validate positive integer fields."""
        if value is not None and value < 0:
            raise ValueError(f"{key} cannot be negative")
        if key in ['round_number', 'match_day'] and value is not None and value <= 0:
            raise ValueError(f"{key} must be greater than 0")
        return value
    
    # Properties
    @property
    def is_scheduled(self) -> bool:
        """Check if match is scheduled."""
        return self.status == MatchStatus.SCHEDULED.value
    
    @property
    def is_live(self) -> bool:
        """Check if match is currently live."""
        return self.status in [MatchStatus.LIVE.value, MatchStatus.HALFTIME.value, 
                              MatchStatus.EXTRA_TIME.value, MatchStatus.PENALTIES.value]
    
    @property
    def is_finished(self) -> bool:
        """Check if match is finished."""
        return self.status == MatchStatus.FINISHED.value
    
    @property
    def is_cancelled(self) -> bool:
        """Check if match is cancelled."""
        return self.status == MatchStatus.CANCELLED.value
    
    @property
    def is_postponed(self) -> bool:
        """Check if match is postponed."""
        return self.status == MatchStatus.POSTPONED.value
    
    @property
    def has_started(self) -> bool:
        """Check if match has started."""
        return self.started_at is not None
    
    @property
    def has_finished(self) -> bool:
        """Check if match has finished."""
        return self.finished_at is not None
    
    @property
    def duration_minutes(self) -> Optional[int]:
        """Get match duration in minutes."""
        if not self.started_at or not self.finished_at:
            return None
        return int((self.finished_at - self.started_at).total_seconds() / 60)
    
    @property
    def home_team_won(self) -> Optional[bool]:
        """Check if home team won (None if not finished or draw)."""
        if not self.is_finished or self.home_score is None or self.away_score is None:
            return None
        
        # Consider extra time and penalties if available
        home_total = self.home_score + (self.extra_time_home_score or 0)
        away_total = self.away_score + (self.extra_time_away_score or 0)
        
        # If penalties were taken, use penalty score
        if self.penalties_home_score is not None and self.penalties_away_score is not None:
            return self.penalties_home_score > self.penalties_away_score
        
        if home_total == away_total:
            return None  # Draw
        
        return home_total > away_total
    
    @property
    def away_team_won(self) -> Optional[bool]:
        """Check if away team won (None if not finished or draw)."""
        home_won = self.home_team_won
        if home_won is None:
            return None
        return not home_won
    
    @property
    def is_draw(self) -> Optional[bool]:
        """Check if match is a draw (None if not finished)."""
        if not self.is_finished or self.home_score is None or self.away_score is None:
            return None
        
        # Consider extra time and penalties
        home_total = self.home_score + (self.extra_time_home_score or 0)
        away_total = self.away_score + (self.extra_time_away_score or 0)
        
        # If penalties were taken, it's not a draw
        if self.penalties_home_score is not None and self.penalties_away_score is not None:
            return False
        
        return home_total == away_total
    
    # Business logic methods
    def can_place_bet(self) -> tuple[bool, str]:
        """Check if betting is currently allowed."""
        if self.betting_closes_at and datetime.now(timezone.utc) > self.betting_closes_at:
            return False, "Betting is closed"
        
        if self.status not in [MatchStatus.SCHEDULED.value]:
            return False, "Betting is not available for current match status"
        
        return True, "Betting is allowed"
    
    def start_match(self) -> None:
        """Start the match."""
        if self.status != MatchStatus.SCHEDULED.value:
            raise ValueError("Can only start scheduled matches")
        
        self.status = MatchStatus.LIVE.value
        if not self.started_at:
            self.started_at = datetime.now(timezone.utc)
    
    def finish_match(self) -> None:
        """Finish the match."""
        if self.status not in [MatchStatus.LIVE.value, MatchStatus.HALFTIME.value, 
                              MatchStatus.EXTRA_TIME.value, MatchStatus.PENALTIES.value]:
            raise ValueError("Can only finish live matches")
        
        self.status = MatchStatus.FINISHED.value
        if not self.finished_at:
            self.finished_at = datetime.now(timezone.utc)
    
    def cancel_match(self, reason: Optional[str] = None) -> None:
        """Cancel the match."""
        if self.status == MatchStatus.FINISHED.value:
            raise ValueError("Cannot cancel finished match")
        
        self.status = MatchStatus.CANCELLED.value
        if reason and self.notes:
            self.notes = f"{self.notes}\nCancellation reason: {reason}"
        elif reason:
            self.notes = f"Cancellation reason: {reason}"
    
    def postpone_match(self, new_time: Optional[datetime] = None, reason: Optional[str] = None) -> None:
        """Postpone the match."""
        if self.status in [MatchStatus.FINISHED.value, MatchStatus.CANCELLED.value]:
            raise ValueError("Cannot postpone finished or cancelled match")
        
        self.status = MatchStatus.POSTPONED.value
        
        if new_time:
            self.scheduled_at = new_time
            # Update betting closes time
            self.betting_closes_at = new_time - timedelta(minutes=15)
        
        if reason and self.notes:
            self.notes = f"{self.notes}\nPostponement reason: {reason}"
        elif reason:
            self.notes = f"Postponement reason: {reason}"
    
    def update_score(self, home_score: int, away_score: int, 
                    extra_time_home: Optional[int] = None, extra_time_away: Optional[int] = None,
                    penalties_home: Optional[int] = None, penalties_away: Optional[int] = None) -> None:
        """Update match score."""
        if not self.is_live and self.status != MatchStatus.FINISHED.value:
            raise ValueError("Can only update score for live or finished matches")
        
        if home_score < 0 or away_score < 0:
            raise ValueError("Scores cannot be negative")
        
        self.home_score = home_score
        self.away_score = away_score
        
        if extra_time_home is not None:
            self.extra_time_home_score = extra_time_home
        if extra_time_away is not None:
            self.extra_time_away_score = extra_time_away
        if penalties_home is not None:
            self.penalties_home_score = penalties_home
        if penalties_away is not None:
            self.penalties_away_score = penalties_away
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Match."""
        return f"<Match(id={self.id}, home_team={self.home_team_id}, away_team={self.away_team_id}, status='{self.status}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Match to dictionary."""
        return {
            'id': str(self.id),
            'competition_id': str(self.competition_id),
            'home_team_id': str(self.home_team_id),
            'away_team_id': str(self.away_team_id),
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'betting_closes_at': self.betting_closes_at.isoformat() if self.betting_closes_at else None,
            'round_number': self.round_number,
            'match_day': self.match_day,
            'venue': self.venue,
            'referee': self.referee,
            'status': self.status,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'extra_time_home_score': self.extra_time_home_score,
            'extra_time_away_score': self.extra_time_away_score,
            'penalties_home_score': self.penalties_home_score,
            'penalties_away_score': self.penalties_away_score,
            'attendance': self.attendance,
            'weather_conditions': self.weather_conditions,
            'notes': self.notes,
            'is_scheduled': self.is_scheduled,
            'is_live': self.is_live,
            'is_finished': self.is_finished,
            'is_cancelled': self.is_cancelled,
            'is_postponed': self.is_postponed,
            'has_started': self.has_started,
            'has_finished': self.has_finished,
            'duration_minutes': self.duration_minutes,
            'home_team_won': self.home_team_won,
            'away_team_won': self.away_team_won,
            'is_draw': self.is_draw,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Match, 'before_update')
def update_match_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)