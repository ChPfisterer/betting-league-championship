"""
Result model for the betting league championship application.

This module defines the Result model with comprehensive match result tracking,
statistics management, and event recording as specified by the TDD tests
in backend/tests/models/test_result_model.py.
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
from enum import Enum

from .base import Base


class ResultStatus(Enum):
    """Valid result status values."""
    SCHEDULED = "scheduled"
    LIVE = "live"
    HALF_TIME = "half_time"
    SECOND_HALF = "second_half"
    EXTRA_TIME = "extra_time"
    PENALTIES = "penalties"
    FINAL = "final"
    ABANDONED = "abandoned"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"


class EventType(Enum):
    """Valid event type values."""
    GOAL = "goal"
    YELLOW_CARD = "yellow_card"
    RED_CARD = "red_card"
    SUBSTITUTION = "substitution"
    PENALTY = "penalty"
    OWN_GOAL = "own_goal"
    OFFSIDE = "offside"
    CORNER = "corner"
    FREE_KICK = "free_kick"
    KICKOFF = "kickoff"
    HALF_TIME = "half_time"
    FULL_TIME = "full_time"


class Result(Base):
    """
    Result model for managing match results and statistics.
    
    Handles match outcome recording, score tracking, event timelines,
    and comprehensive statistics for betting settlement and analysis.
    """
    
    __tablename__ = 'results'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the result"
    )
    
    # Foreign keys
    match_id = Column(
        UUID(as_uuid=True),
        ForeignKey('matches.id', name='fk_results_match_id'),
        nullable=False,
        unique=True,
        comment="ID of the match this result belongs to"
    )
    
    # Main score information
    home_score = Column(
        Integer,
        nullable=False,
        comment="Home team final score"
    )
    away_score = Column(
        Integer,
        nullable=False,
        comment="Away team final score"
    )
    
    # Detailed scoring breakdown
    half_time_home_score = Column(
        Integer,
        comment="Home team score at half time"
    )
    half_time_away_score = Column(
        Integer,
        comment="Away team score at half time"
    )
    extra_time_home_score = Column(
        Integer,
        comment="Home team score in extra time"
    )
    extra_time_away_score = Column(
        Integer,
        comment="Away team score in extra time"
    )
    penalty_home_score = Column(
        Integer,
        comment="Home team penalty shootout score"
    )
    penalty_away_score = Column(
        Integer,
        comment="Away team penalty shootout score"
    )
    
    # Match outcome
    winner_team_id = Column(
        UUID(as_uuid=True),
        ForeignKey('teams.id', name='fk_results_winner_team_id'),
        comment="ID of the winning team (null for draw)"
    )
    
    # Status and verification
    status = Column(
        String(20),
        nullable=False,
        comment="Current status of the match result"
    )
    is_official = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether the result is official"
    )
    verified_by = Column(
        String(100),
        comment="Official who verified the result"
    )
    verified_at = Column(
        DateTime(timezone=True),
        comment="When the result was officially verified"
    )
    
    # Match statistics
    possession_home = Column(
        Integer,
        comment="Home team possession percentage"
    )
    possession_away = Column(
        Integer,
        comment="Away team possession percentage"
    )
    shots_home = Column(
        Integer,
        comment="Home team total shots"
    )
    shots_away = Column(
        Integer,
        comment="Away team total shots"
    )
    corners_home = Column(
        Integer,
        comment="Home team corner kicks"
    )
    corners_away = Column(
        Integer,
        comment="Away team corner kicks"
    )
    yellow_cards_home = Column(
        Integer,
        comment="Home team yellow cards"
    )
    yellow_cards_away = Column(
        Integer,
        comment="Away team yellow cards"
    )
    red_cards_home = Column(
        Integer,
        comment="Home team red cards"
    )
    red_cards_away = Column(
        Integer,
        comment="Away team red cards"
    )
    
    # Additional data
    match_events = Column(
        JSON,
        comment="Timeline of match events"
    )
    statistics = Column(
        JSON,
        comment="Additional match statistics"
    )
    notes = Column(
        Text,
        comment="Additional notes about the result"
    )
    
    # Timestamps
    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="When the match started"
    )
    finished_at = Column(
        DateTime(timezone=True),
        comment="When the match finished"
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the result record was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the result record was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('scheduled', 'live', 'half_time', 'second_half', 'extra_time', 'penalties', 'final', 'abandoned', 'postponed', 'cancelled')",
            name="ck_results_status"
        ),
        CheckConstraint(
            "home_score >= 0",
            name="ck_results_home_score_non_negative"
        ),
        CheckConstraint(
            "away_score >= 0",
            name="ck_results_away_score_non_negative"
        ),
        CheckConstraint(
            "half_time_home_score IS NULL OR half_time_home_score >= 0",
            name="ck_results_half_time_home_score_non_negative"
        ),
        CheckConstraint(
            "half_time_away_score IS NULL OR half_time_away_score >= 0",
            name="ck_results_half_time_away_score_non_negative"
        ),
        CheckConstraint(
            "extra_time_home_score IS NULL OR extra_time_home_score >= 0",
            name="ck_results_extra_time_home_score_non_negative"
        ),
        CheckConstraint(
            "extra_time_away_score IS NULL OR extra_time_away_score >= 0",
            name="ck_results_extra_time_away_score_non_negative"
        ),
        CheckConstraint(
            "penalty_home_score IS NULL OR penalty_home_score >= 0",
            name="ck_results_penalty_home_score_non_negative"
        ),
        CheckConstraint(
            "penalty_away_score IS NULL OR penalty_away_score >= 0",
            name="ck_results_penalty_away_score_non_negative"
        ),
        CheckConstraint(
            "possession_home IS NULL OR (possession_home >= 0 AND possession_home <= 100)",
            name="ck_results_possession_home_percentage"
        ),
        CheckConstraint(
            "possession_away IS NULL OR (possession_away >= 0 AND possession_away <= 100)",
            name="ck_results_possession_away_percentage"
        ),
        CheckConstraint(
            "shots_home IS NULL OR shots_home >= 0",
            name="ck_results_shots_home_non_negative"
        ),
        CheckConstraint(
            "shots_away IS NULL OR shots_away >= 0",
            name="ck_results_shots_away_non_negative"
        ),
        CheckConstraint(
            "corners_home IS NULL OR corners_home >= 0",
            name="ck_results_corners_home_non_negative"
        ),
        CheckConstraint(
            "corners_away IS NULL OR corners_away >= 0",
            name="ck_results_corners_away_non_negative"
        ),
        CheckConstraint(
            "yellow_cards_home IS NULL OR yellow_cards_home >= 0",
            name="ck_results_yellow_cards_home_non_negative"
        ),
        CheckConstraint(
            "yellow_cards_away IS NULL OR yellow_cards_away >= 0",
            name="ck_results_yellow_cards_away_non_negative"
        ),
        CheckConstraint(
            "red_cards_home IS NULL OR red_cards_home >= 0",
            name="ck_results_red_cards_home_non_negative"
        ),
        CheckConstraint(
            "red_cards_away IS NULL OR red_cards_away >= 0",
            name="ck_results_red_cards_away_non_negative"
        ),
        CheckConstraint(
            "finished_at IS NULL OR finished_at >= started_at",
            name="ck_results_finished_after_started"
        ),
        CheckConstraint(
            "verified_at IS NULL OR verified_at >= started_at",
            name="ck_results_verified_after_started"
        ),
        Index('ix_results_match_id', 'match_id'),
        Index('ix_results_status', 'status'),
        Index('ix_results_winner_team_id', 'winner_team_id'),
        Index('ix_results_is_official', 'is_official'),
        Index('ix_results_started_at', 'started_at'),
        Index('ix_results_finished_at', 'finished_at'),
        {'extend_existing': True}
    )
    
    def __init__(self, **kwargs):
        """Initialize Result with proper validation and defaults."""
        # Validate required fields
        if 'match_id' not in kwargs or not kwargs['match_id']:
            raise ValueError("Match ID is required")
        
        if 'home_score' not in kwargs or kwargs['home_score'] is None:
            raise ValueError("Home score is required")
        
        if 'away_score' not in kwargs or kwargs['away_score'] is None:
            raise ValueError("Away score is required")
        
        if 'status' not in kwargs or not kwargs['status']:
            raise ValueError("Status is required")
        
        if 'started_at' not in kwargs or not kwargs['started_at']:
            raise ValueError("Started at time is required")
        
        # Validate possession values if provided
        if 'possession_home' in kwargs and kwargs['possession_home'] is not None:
            if kwargs['possession_home'] < 0 or kwargs['possession_home'] > 100:
                raise ValueError("Home possession must be between 0 and 100")
                
        if 'possession_away' in kwargs and kwargs['possession_away'] is not None:
            if kwargs['possession_away'] < 0 or kwargs['possession_away'] > 100:
                raise ValueError("Away possession must be between 0 and 100")
        
        # Set default values if not provided
        if 'is_official' not in kwargs:
            kwargs['is_official'] = False
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.now(timezone.utc)
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        super().__init__(**kwargs)
    
    # Validation methods
    @validates('match_id')
    def validate_match_id(self, key: str, match_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate match_id is provided."""
        if not match_id:
            raise ValueError("Match ID is required")
        return match_id
    
    @validates('home_score')
    def validate_home_score(self, key: str, home_score: int) -> int:
        """Validate home score."""
        if home_score is None:
            raise ValueError("Home score is required")
        
        if home_score < 0:
            raise ValueError("Home score cannot be negative")
        
        return home_score
    
    @validates('away_score')
    def validate_away_score(self, key: str, away_score: int) -> int:
        """Validate away score."""
        if away_score is None:
            raise ValueError("Away score is required")
        
        if away_score < 0:
            raise ValueError("Away score cannot be negative")
        
        return away_score
    
    @validates('status')
    def validate_status(self, key: str, status: str) -> str:
        """Validate result status."""
        if not status:
            raise ValueError("Status is required")
        
        valid_statuses = [rs.value for rs in ResultStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        return status
    
    @validates('started_at')
    def validate_started_at(self, key: str, started_at: datetime) -> datetime:
        """Validate started_at time."""
        if not started_at:
            raise ValueError("Started at time is required")
        
        return started_at
    
    @validates('finished_at')
    def validate_finished_at(self, key: str, finished_at: Optional[datetime]) -> Optional[datetime]:
        """Validate finished_at time."""
        if finished_at and self.started_at and finished_at < self.started_at:
            raise ValueError("Finished time cannot be before start time")
        
        return finished_at
    
    @validates('possession_home')
    def validate_possession_home(self, key: str, possession_home: Optional[int]) -> Optional[int]:
        """Validate home possession percentage."""
        if possession_home is not None:
            if possession_home < 0 or possession_home > 100:
                raise ValueError("Home possession must be between 0 and 100")
        
        return possession_home
    
    @validates('possession_away')
    def validate_possession_away(self, key: str, possession_away: Optional[int]) -> Optional[int]:
        """Validate away possession percentage."""
        if possession_away is not None:
            if possession_away < 0 or possession_away > 100:
                raise ValueError("Away possession must be between 0 and 100")
        
        return possession_away
    
    # Properties
    @property
    def is_final(self) -> bool:
        """Check if match result is final."""
        return self.status == ResultStatus.FINAL.value
    
    @property
    def is_finished(self) -> bool:
        """Check if match is finished."""
        return self.status in [ResultStatus.FINAL.value, ResultStatus.ABANDONED.value, 
                              ResultStatus.CANCELLED.value]
    
    @property
    def is_live(self) -> bool:
        """Check if match is currently live."""
        return self.status in [ResultStatus.LIVE.value, ResultStatus.SECOND_HALF.value,
                              ResultStatus.EXTRA_TIME.value, ResultStatus.PENALTIES.value]
    
    @property
    def is_draw(self) -> bool:
        """Check if match ended in a draw."""
        return self.home_score == self.away_score and self.is_finished
    
    @property
    def home_win(self) -> bool:
        """Check if home team won."""
        return self.home_score > self.away_score and self.is_finished
    
    @property
    def away_win(self) -> bool:
        """Check if away team won."""
        return self.away_score > self.home_score and self.is_finished
    
    @property
    def winner(self) -> Optional[str]:
        """Get match winner: 'home', 'away', or None for draw/unfinished."""
        if not self.is_finished:
            return None
        
        if self.home_score > self.away_score:
            return 'home'
        elif self.away_score > self.home_score:
            return 'away'
        else:
            return None  # Draw
    
    @property
    def total_goals(self) -> int:
        """Get total goals scored in the match."""
        return self.home_score + self.away_score
    
    @property
    def goal_difference(self) -> int:
        """Get goal difference from home team perspective."""
        return self.home_score - self.away_score
    
    @property
    def match_duration(self) -> Optional[int]:
        """Get match duration in minutes."""
        if not self.finished_at or not self.started_at:
            return None
        
        duration = self.finished_at - self.started_at
        return int(duration.total_seconds() / 60)
    
    @property
    def duration(self) -> Optional[int]:
        """Get match duration in minutes (alias for match_duration)."""
        return self.match_duration
    
    # Business logic methods
    def update_score(self, home_score: int, away_score: int) -> None:
        """Update the match score."""
        if home_score < 0 or away_score < 0:
            raise ValueError("Scores cannot be negative")
        
        self.home_score = home_score
        self.away_score = away_score
        
        # Update winner
        if home_score > away_score:
            # Would need to get home team ID from match relationship
            pass
        elif away_score > home_score:
            # Would need to get away team ID from match relationship  
            pass
        else:
            self.winner_team_id = None
    
    def update_half_time_score(self, home_score: int, away_score: int) -> None:
        """Update half time score."""
        if home_score < 0 or away_score < 0:
            raise ValueError("Half time scores cannot be negative")
        
        self.half_time_home_score = home_score
        self.half_time_away_score = away_score
    
    def update_status(self, status: str) -> None:
        """Update match status."""
        valid_statuses = [rs.value for rs in ResultStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        self.status = status
        
        # Auto-set finished_at when match ends
        if status in [ResultStatus.FINAL.value, ResultStatus.ABANDONED.value]:
            if not self.finished_at:
                self.finished_at = datetime.now(timezone.utc)
    
    def finalize_result(self, verified_by: str) -> None:
        """Finalize and verify the result."""
        if self.status != ResultStatus.FINAL.value:
            raise ValueError("Can only finalize results with final status")
        
        self.is_official = True
        self.verified_by = verified_by
        self.verified_at = datetime.now(timezone.utc)
        
        if not self.finished_at:
            self.finished_at = datetime.now(timezone.utc)
    
    def add_event(self, event_type: str, minute: int, team_id: Optional[str] = None, 
                  player_id: Optional[str] = None, description: Optional[str] = None) -> None:
        """Add a match event."""
        valid_event_types = [et.value for et in EventType]
        if event_type not in valid_event_types:
            raise ValueError(f"Invalid event type. Must be one of: {', '.join(valid_event_types)}")
        
        if not self.match_events:
            self.match_events = []
        
        event = {
            'type': event_type,
            'minute': minute,
            'team_id': team_id,
            'player_id': player_id,
            'description': description,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        self.match_events.append(event)
    
    def update_statistics(self, stats: Dict[str, Any]) -> None:
        """Update match statistics."""
        if not self.statistics:
            self.statistics = {}
        
        self.statistics.update(stats)
    
    # Class methods for queries
    @classmethod
    def get_by_match(cls, db_session, match_id: Union[str, uuid.UUID]):
        """Get result by match ID."""
        return db_session.query(cls).filter(cls.match_id == match_id).first()
    
    @classmethod
    def get_by_status(cls, db_session, status: str):
        """Get results by status."""
        return db_session.query(cls).filter(cls.status == status).all()
    
    @classmethod
    def get_live_results(cls, db_session):
        """Get all live match results."""
        live_statuses = [ResultStatus.LIVE.value, ResultStatus.SECOND_HALF.value,
                        ResultStatus.EXTRA_TIME.value, ResultStatus.PENALTIES.value]
        return db_session.query(cls).filter(cls.status.in_(live_statuses)).all()
    
    @classmethod
    def get_final_results(cls, db_session):
        """Get all final results."""
        return db_session.query(cls).filter(cls.status == ResultStatus.FINAL.value).all()
    
    @classmethod
    def get_high_scoring_matches(cls, db_session, min_goals: int = 5):
        """Get matches with high total goals."""
        return db_session.query(cls).filter(
            (cls.home_score + cls.away_score) >= min_goals,
            cls.status == ResultStatus.FINAL.value
        ).all()
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Result."""
        return f"<Result(id={self.id}, match_id={self.match_id}, score={self.home_score}-{self.away_score}, status='{self.status}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Result to dictionary."""
        return {
            'id': str(self.id),
            'match_id': str(self.match_id),
            'home_score': self.home_score,
            'away_score': self.away_score,
            'half_time_home_score': self.half_time_home_score,
            'half_time_away_score': self.half_time_away_score,
            'extra_time_home_score': self.extra_time_home_score,
            'extra_time_away_score': self.extra_time_away_score,
            'penalty_home_score': self.penalty_home_score,
            'penalty_away_score': self.penalty_away_score,
            'winner_team_id': str(self.winner_team_id) if self.winner_team_id else None,
            'status': self.status,
            'is_official': self.is_official,
            'verified_by': self.verified_by,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'possession_home': self.possession_home,
            'possession_away': self.possession_away,
            'shots_home': self.shots_home,
            'shots_away': self.shots_away,
            'corners_home': self.corners_home,
            'corners_away': self.corners_away,
            'yellow_cards_home': self.yellow_cards_home,
            'yellow_cards_away': self.yellow_cards_away,
            'red_cards_home': self.red_cards_home,
            'red_cards_away': self.red_cards_away,
            'match_events': self.match_events,
            'statistics': self.statistics,
            'notes': self.notes,
            'is_finished': self.is_finished,
            'is_live': self.is_live,
            'is_draw': self.is_draw,
            'home_win': self.home_win,
            'away_win': self.away_win,
            'total_goals': self.total_goals,
            'goal_difference': self.goal_difference,
            'match_duration': self.match_duration,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Result, 'before_update')
def update_result_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)