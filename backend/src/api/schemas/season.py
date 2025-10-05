"""
Season Pydantic schemas for API serialization and validation.

This module defines comprehensive schemas for season operations including
creation, updates, responses, and statistics. Seasons provide temporal
organization for competitions and enable historical tracking.
"""

from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from enum import Enum

from .competition import CompetitionSummary


class SeasonStatus(str, Enum):
    """Season status enumeration."""
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SeasonType(str, Enum):
    """Season type enumeration."""
    REGULAR = "regular"
    PLAYOFFS = "playoffs"
    PRESEASON = "preseason"
    POSTSEASON = "postseason"
    CHAMPIONSHIP = "championship"
    QUALIFIER = "qualifier"


class SeasonBase(BaseModel):
    """Base season schema with common fields."""
    
    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Season name (e.g., '2024-25 Premier League')"
    )
    
    year: int = Field(
        ...,
        ge=1900,
        le=2100,
        description="Primary year for the season"
    )
    
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Season description"
    )
    
    season_type: SeasonType = Field(
        SeasonType.REGULAR,
        description="Type of season"
    )
    
    start_date: date = Field(
        ...,
        description="Season start date"
    )
    
    end_date: date = Field(
        ...,
        description="Season end date"
    )
    
    registration_start: Optional[date] = Field(
        None,
        description="Registration period start date"
    )
    
    registration_end: Optional[date] = Field(
        None,
        description="Registration period end date"
    )
    
    max_teams: Optional[int] = Field(
        None,
        ge=2,
        le=1000,
        description="Maximum number of teams for the season"
    )
    
    min_teams: Optional[int] = Field(
        None,
        ge=2,
        le=1000,
        description="Minimum number of teams for the season"
    )
    
    points_for_win: int = Field(
        3,
        ge=0,
        le=10,
        description="Points awarded for a win"
    )
    
    points_for_draw: int = Field(
        1,
        ge=0,
        le=10,
        description="Points awarded for a draw"
    )
    
    points_for_loss: int = Field(
        0,
        ge=0,
        le=10,
        description="Points awarded for a loss"
    )
    
    allow_draws: bool = Field(
        True,
        description="Whether draws are allowed in this season"
    )
    
    playoff_teams: Optional[int] = Field(
        None,
        ge=2,
        le=100,
        description="Number of teams qualifying for playoffs"
    )
    
    relegation_teams: Optional[int] = Field(
        None,
        ge=0,
        le=50,
        description="Number of teams relegated at season end"
    )
    
    promotion_teams: Optional[int] = Field(
        None,
        ge=0,
        le=50,
        description="Number of teams promoted from lower divisions"
    )
    
    is_public: bool = Field(
        True,
        description="Whether season is publicly visible"
    )
    
    allow_betting: bool = Field(
        True,
        description="Whether betting is allowed for this season"
    )

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: date, info) -> date:
        """Validate that end date is after start date."""
        if 'start_date' in info.data and v <= info.data['start_date']:
            raise ValueError('End date must be after start date')
        return v

    @field_validator('registration_end')
    @classmethod
    def validate_registration_end(cls, v: Optional[date], info) -> Optional[date]:
        """Validate registration period dates."""
        if v is not None:
            if 'registration_start' in info.data and info.data['registration_start'] is not None:
                if v <= info.data['registration_start']:
                    raise ValueError('Registration end must be after registration start')
            if 'start_date' in info.data and v >= info.data['start_date']:
                raise ValueError('Registration must end before season starts')
        return v

    @field_validator('max_teams')
    @classmethod
    def validate_max_teams(cls, v: Optional[int], info) -> Optional[int]:
        """Validate that max teams is greater than min teams."""
        if v is not None and 'min_teams' in info.data and info.data['min_teams'] is not None:
            if v < info.data['min_teams']:
                raise ValueError('Maximum teams must be greater than or equal to minimum teams')
        return v

    @field_validator('playoff_teams')
    @classmethod
    def validate_playoff_teams(cls, v: Optional[int], info) -> Optional[int]:
        """Validate playoff teams against max teams."""
        if v is not None and 'max_teams' in info.data and info.data['max_teams'] is not None:
            if v > info.data['max_teams']:
                raise ValueError('Playoff teams cannot exceed maximum teams')
        return v


class SeasonCreate(SeasonBase):
    """Schema for creating a new season."""
    
    sport_id: UUID = Field(
        ...,
        description="ID of the sport this season belongs to"
    )


class SeasonUpdate(BaseModel):
    """Schema for updating an existing season."""
    
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=200,
        description="Season name"
    )
    
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Season description"
    )
    
    season_type: Optional[SeasonType] = Field(
        None,
        description="Type of season"
    )
    
    start_date: Optional[date] = Field(
        None,
        description="Season start date"
    )
    
    end_date: Optional[date] = Field(
        None,
        description="Season end date"
    )
    
    registration_start: Optional[date] = Field(
        None,
        description="Registration period start date"
    )
    
    registration_end: Optional[date] = Field(
        None,
        description="Registration period end date"
    )
    
    max_teams: Optional[int] = Field(
        None,
        ge=2,
        le=1000,
        description="Maximum number of teams"
    )
    
    min_teams: Optional[int] = Field(
        None,
        ge=2,
        le=1000,
        description="Minimum number of teams"
    )
    
    points_for_win: Optional[int] = Field(
        None,
        ge=0,
        le=10,
        description="Points awarded for a win"
    )
    
    points_for_draw: Optional[int] = Field(
        None,
        ge=0,
        le=10,
        description="Points awarded for a draw"
    )
    
    points_for_loss: Optional[int] = Field(
        None,
        ge=0,
        le=10,
        description="Points awarded for a loss"
    )
    
    allow_draws: Optional[bool] = Field(
        None,
        description="Whether draws are allowed in this season"
    )
    
    playoff_teams: Optional[int] = Field(
        None,
        ge=2,
        le=100,
        description="Number of teams qualifying for playoffs"
    )
    
    relegation_teams: Optional[int] = Field(
        None,
        ge=0,
        le=50,
        description="Number of teams relegated at season end"
    )
    
    promotion_teams: Optional[int] = Field(
        None,
        ge=0,
        le=50,
        description="Number of teams promoted from lower divisions"
    )
    
    is_public: Optional[bool] = Field(
        None,
        description="Whether season is publicly visible"
    )
    
    allow_betting: Optional[bool] = Field(
        None,
        description="Whether betting is allowed for this season"
    )


class SeasonResponse(SeasonBase):
    """Schema for season responses."""
    
    id: UUID = Field(..., description="Season unique identifier")
    sport_id: UUID = Field(..., description="Sport ID this season belongs to")
    status: SeasonStatus = Field(..., description="Current season status")
    created_at: datetime = Field(..., description="Season creation timestamp")
    updated_at: datetime = Field(..., description="Season last update timestamp")
    is_active: bool = Field(..., description="Whether season is active")

    class Config:
        from_attributes = True


class SeasonSummary(BaseModel):
    """Lightweight season schema for lists and references."""
    
    id: UUID = Field(..., description="Season unique identifier")
    name: str = Field(..., description="Season name")
    year: int = Field(..., description="Primary year for the season")
    season_type: SeasonType = Field(..., description="Type of season")
    status: SeasonStatus = Field(..., description="Current season status")
    start_date: date = Field(..., description="Season start date")
    end_date: date = Field(..., description="Season end date")
    is_active: bool = Field(..., description="Whether season is active")
    is_public: bool = Field(..., description="Whether season is publicly visible")

    class Config:
        from_attributes = True


class SeasonStats(BaseModel):
    """Season statistics schema."""
    
    total_competitions: int = Field(..., description="Total number of competitions")
    total_teams: int = Field(..., description="Total number of participating teams")
    total_matches: int = Field(..., description="Total number of matches")
    completed_matches: int = Field(..., description="Number of completed matches")
    pending_matches: int = Field(..., description="Number of pending matches")
    total_bets: int = Field(..., description="Total number of bets placed")
    total_bet_amount: float = Field(..., description="Total amount bet")
    days_remaining: Optional[int] = Field(None, description="Days until season ends")
    progress_percentage: float = Field(..., description="Season completion percentage (0-100)")
    average_goals_per_match: Optional[float] = Field(None, description="Average goals per match")

    class Config:
        from_attributes = True


class SeasonWithStats(SeasonResponse):
    """Season response with statistics."""
    
    stats: SeasonStats = Field(..., description="Season statistics")

    class Config:
        from_attributes = True


class SeasonCompetitionList(BaseModel):
    """Schema for listing competitions in a season."""
    
    season_id: UUID = Field(..., description="Season ID")
    competitions: List[CompetitionSummary] = Field(..., description="List of competitions")
    total_competitions: int = Field(..., description="Total number of competitions")

    class Config:
        from_attributes = True


class SeasonStandings(BaseModel):
    """Season standings/leaderboard schema."""
    
    season_id: UUID = Field(..., description="Season ID")
    standings: List[dict] = Field(..., description="Team standings data")
    last_updated: datetime = Field(..., description="Last standings update")

    class Config:
        from_attributes = True