"""
Match Pydantic schemas for API serialization and validation.

This module defines comprehensive schemas for match operations including
creation, updates, responses, and statistics. Matches are the core events
where betting takes place and results are determined.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from enum import Enum

from .competition import CompetitionSummary
from .team import TeamSummary
from .sport import SportSummary


class MatchStatus(str, Enum):
    """Match status enumeration."""
    SCHEDULED = "scheduled"
    LIVE = "live"
    HALFTIME = "halftime"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class MatchType(str, Enum):
    """Match type enumeration."""
    REGULAR = "regular"
    PLAYOFF = "playoff"
    FINAL = "final"
    SEMIFINAL = "semifinal"
    QUARTERFINAL = "quarterfinal"
    FRIENDLY = "friendly"
    QUALIFIER = "qualifier"


class MatchVenue(str, Enum):
    """Match venue type enumeration."""
    HOME = "home"
    AWAY = "away"
    NEUTRAL = "neutral"


class MatchBase(BaseModel):
    """Base match schema with common fields."""
    
    scheduled_at: datetime = Field(
        ...,
        description="When the match is scheduled to start"
    )
    
    venue: MatchVenue = Field(
        MatchVenue.HOME,
        description="Match venue type"
    )
    
    venue_name: Optional[str] = Field(
        None,
        max_length=200,
        description="Name of the venue/stadium"
    )
    
    venue_city: Optional[str] = Field(
        None,
        max_length=100,
        description="City where the match is played"
    )
    
    venue_country: Optional[str] = Field(
        None,
        max_length=100,
        description="Country where the match is played"
    )
    
    match_type: MatchType = Field(
        MatchType.REGULAR,
        description="Type of match"
    )
    
    round_number: Optional[int] = Field(
        None,
        ge=1,
        le=100,
        description="Round number in competition"
    )
    
    week_number: Optional[int] = Field(
        None,
        ge=1,
        le=60,
        description="Week number in season"
    )
    
    is_home_game: bool = Field(
        True,
        description="Whether this is a home game for the home team"
    )
    
    allow_betting: bool = Field(
        True,
        description="Whether betting is allowed on this match"
    )
    
    betting_closes_at: Optional[datetime] = Field(
        None,
        description="When betting closes for this match"
    )
    
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional notes about the match"
    )

    @field_validator('betting_closes_at')
    @classmethod
    def validate_betting_closes_at(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate that betting closes before or at match start."""
        if v is not None and 'scheduled_at' in info.data:
            if v > info.data['scheduled_at']:
                raise ValueError('Betting must close before or at match start time')
        return v


class MatchCreate(MatchBase):
    """Schema for creating a new match."""
    
    competition_id: UUID = Field(
        ...,
        description="ID of the competition this match belongs to"
    )
    
    season_id: Optional[UUID] = Field(
        None,
        description="ID of the season this match belongs to"
    )
    
    home_team_id: UUID = Field(
        ...,
        description="ID of the home team"
    )
    
    away_team_id: UUID = Field(
        ...,
        description="ID of the away team"
    )

    @field_validator('away_team_id')
    @classmethod
    def validate_different_teams(cls, v: UUID, info) -> UUID:
        """Validate that home and away teams are different."""
        if 'home_team_id' in info.data and v == info.data['home_team_id']:
            raise ValueError('Home and away teams must be different')
        return v


class MatchUpdate(BaseModel):
    """Schema for updating an existing match."""
    
    scheduled_at: Optional[datetime] = Field(
        None,
        description="When the match is scheduled to start"
    )
    
    venue: Optional[MatchVenue] = Field(
        None,
        description="Match venue type"
    )
    
    venue_name: Optional[str] = Field(
        None,
        max_length=200,
        description="Name of the venue/stadium"
    )
    
    venue_city: Optional[str] = Field(
        None,
        max_length=100,
        description="City where the match is played"
    )
    
    venue_country: Optional[str] = Field(
        None,
        max_length=100,
        description="Country where the match is played"
    )
    
    match_type: Optional[MatchType] = Field(
        None,
        description="Type of match"
    )
    
    round_number: Optional[int] = Field(
        None,
        ge=1,
        le=100,
        description="Round number in competition"
    )
    
    week_number: Optional[int] = Field(
        None,
        ge=1,
        le=60,
        description="Week number in season"
    )
    
    is_home_game: Optional[bool] = Field(
        None,
        description="Whether this is a home game for the home team"
    )
    
    allow_betting: Optional[bool] = Field(
        None,
        description="Whether betting is allowed on this match"
    )
    
    betting_closes_at: Optional[datetime] = Field(
        None,
        description="When betting closes for this match"
    )
    
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional notes about the match"
    )


class MatchScoreUpdate(BaseModel):
    """Schema for updating match scores."""
    
    home_score: int = Field(
        ...,
        ge=0,
        description="Home team score"
    )
    
    away_score: int = Field(
        ...,
        ge=0,
        description="Away team score"
    )
    
    period: Optional[str] = Field(
        None,
        description="Which period/half the score is for"
    )
    
    is_final: bool = Field(
        False,
        description="Whether this is the final score"
    )


class MatchStatusUpdate(BaseModel):
    """Schema for updating match status."""
    
    status: MatchStatus = Field(
        ...,
        description="New match status"
    )
    
    status_reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for status change"
    )


class MatchResponse(MatchBase):
    """Schema for match responses."""
    
    id: UUID = Field(..., description="Match unique identifier")
    competition_id: UUID = Field(..., description="Competition ID")
    season_id: Optional[UUID] = Field(None, description="Season ID")
    home_team_id: UUID = Field(..., description="Home team ID")
    away_team_id: UUID = Field(..., description="Away team ID")
    status: MatchStatus = Field(..., description="Current match status")
    
    # Scores
    home_score: Optional[int] = Field(None, description="Home team score")
    away_score: Optional[int] = Field(None, description="Away team score")
    
    # Timing
    started_at: Optional[datetime] = Field(None, description="When the match actually started")
    finished_at: Optional[datetime] = Field(None, description="When the match finished")
    duration_minutes: Optional[int] = Field(None, description="Match duration in minutes")
    
    # Results
    winner_team_id: Optional[UUID] = Field(None, description="ID of the winning team")
    is_draw: Optional[bool] = Field(None, description="Whether the match ended in a draw")
    
    # Metadata
    created_at: datetime = Field(..., description="Match creation timestamp")
    updated_at: datetime = Field(..., description="Match last update timestamp")
    is_active: bool = Field(..., description="Whether match is active")

    class Config:
        from_attributes = True


class MatchSummary(BaseModel):
    """Lightweight match schema for lists and references."""
    
    id: UUID = Field(..., description="Match unique identifier")
    home_team_id: UUID = Field(..., description="Home team ID")
    away_team_id: UUID = Field(..., description="Away team ID")
    scheduled_at: datetime = Field(..., description="Scheduled start time")
    status: MatchStatus = Field(..., description="Current match status")
    home_score: Optional[int] = Field(None, description="Home team score")
    away_score: Optional[int] = Field(None, description="Away team score")
    venue_name: Optional[str] = Field(None, description="Venue name")
    match_type: Optional[MatchType] = Field(None, description="Match type")
    is_active: Optional[bool] = Field(True, description="Whether match is active")

    class Config:
        from_attributes = True


class MatchWithTeams(MatchResponse):
    """Match response with team details."""
    
    home_team: dict = Field(..., description="Home team details")
    away_team: dict = Field(..., description="Away team details")

    class Config:
        from_attributes = True


class MatchWithCompetition(MatchResponse):
    """Match response with competition details."""
    
    competition: dict = Field(..., description="Competition details")
    sport: Optional[dict] = Field(None, description="Sport details")

    class Config:
        from_attributes = True


class MatchStats(BaseModel):
    """Match statistics schema."""
    
    total_bets: int = Field(..., description="Total number of bets placed")
    total_bet_amount: float = Field(..., description="Total amount bet")
    home_team_bets: int = Field(..., description="Bets on home team")
    away_team_bets: int = Field(..., description="Bets on away team")
    draw_bets: int = Field(..., description="Bets on draw")
    attendance: Optional[int] = Field(None, description="Match attendance")
    tv_viewers: Optional[int] = Field(None, description="TV/streaming viewers")
    
    # Betting odds (if available)
    home_odds: Optional[float] = Field(None, description="Latest odds for home team")
    away_odds: Optional[float] = Field(None, description="Latest odds for away team")
    draw_odds: Optional[float] = Field(None, description="Latest odds for draw")

    class Config:
        from_attributes = True


class MatchWithStats(MatchResponse):
    """Match response with statistics."""
    
    stats: MatchStats = Field(..., description="Match statistics")

    class Config:
        from_attributes = True


class MatchTimeline(BaseModel):
    """Match timeline/events schema."""
    
    match_id: UUID = Field(..., description="Match ID")
    events: List[dict] = Field(..., description="List of match events")
    last_updated: datetime = Field(..., description="Last timeline update")

    class Config:
        from_attributes = True


class MatchEvent(BaseModel):
    """Individual match event schema."""
    
    minute: int = Field(..., ge=0, description="Minute when event occurred")
    event_type: str = Field(..., description="Type of event")
    description: str = Field(..., description="Event description")
    team_id: Optional[UUID] = Field(None, description="Team involved in event")
    player_id: Optional[UUID] = Field(None, description="Player involved in event")

    class Config:
        from_attributes = True


class MatchResult(BaseModel):
    """Final match result schema."""
    
    match_id: UUID = Field(..., description="Match ID")
    home_score: int = Field(..., description="Final home team score")
    away_score: int = Field(..., description="Final away team score")
    winner_team_id: Optional[UUID] = Field(None, description="Winner team ID (null for draw)")
    is_draw: bool = Field(..., description="Whether match ended in draw")
    finished_at: datetime = Field(..., description="When match finished")
    verified: bool = Field(False, description="Whether result is verified")

    class Config:
        from_attributes = True


class MatchPrediction(BaseModel):
    """Match prediction schema."""
    
    match_id: UUID = Field(..., description="Match ID")
    predicted_home_score: Optional[int] = Field(None, description="Predicted home score")
    predicted_away_score: Optional[int] = Field(None, description="Predicted away score")
    confidence: Optional[float] = Field(None, ge=0, le=100, description="Prediction confidence %")
    predicted_winner: Optional[str] = Field(None, description="Predicted winner")

    class Config:
        from_attributes = True