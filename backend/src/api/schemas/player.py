"""
Player Pydantic schemas for API serialization and validation.

This module defines comprehensive schemas for player operations including
creation, updates, responses, and statistics. Players represent individual
athletes participating in teams and competitions.
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from enum import Enum

from .team import TeamSummary
from .sport import SportSummary


class PlayerPosition(str, Enum):
    """Player position enumeration (sport-agnostic)."""
    GOALKEEPER = "goalkeeper"
    DEFENDER = "defender"
    MIDFIELDER = "midfielder"
    FORWARD = "forward"
    CENTER = "center"
    GUARD = "guard"
    FORWARD_BASKETBALL = "forward_basketball"
    PITCHER = "pitcher"
    CATCHER = "catcher"
    INFIELDER = "infielder"
    OUTFIELDER = "outfielder"
    QUARTERBACK = "quarterback"
    RUNNING_BACK = "running_back"
    WIDE_RECEIVER = "wide_receiver"
    TIGHT_END = "tight_end"
    OFFENSIVE_LINE = "offensive_line"
    DEFENSIVE_LINE = "defensive_line"
    LINEBACKER = "linebacker"
    CORNERBACK = "cornerback"
    SAFETY = "safety"
    KICKER = "kicker"
    PUNTER = "punter"
    OTHER = "other"


class PlayerStatus(str, Enum):
    """Player status enumeration."""
    ACTIVE = "active"
    INJURED = "injured"
    SUSPENDED = "suspended"
    RETIRED = "retired"
    TRANSFERRED = "transferred"
    INACTIVE = "inactive"


class PlayerBase(BaseModel):
    """Base player schema with common fields."""
    
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Player's first name"
    )
    
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Player's last name"
    )
    
    display_name: Optional[str] = Field(
        None,
        max_length=200,
        description="Player's display/nickname"
    )
    
    jersey_number: Optional[int] = Field(
        None,
        ge=0,
        le=999,
        description="Player's jersey number"
    )
    
    position: Optional[PlayerPosition] = Field(
        None,
        description="Player's primary position"
    )
    
    secondary_positions: Optional[List[PlayerPosition]] = Field(
        None,
        description="List of secondary positions player can play"
    )
    
    date_of_birth: Optional[date] = Field(
        None,
        description="Player's date of birth"
    )
    
    nationality: Optional[str] = Field(
        None,
        max_length=100,
        description="Player's nationality"
    )
    
    height_cm: Optional[int] = Field(
        None,
        ge=100,
        le=250,
        description="Player's height in centimeters"
    )
    
    weight_kg: Optional[float] = Field(
        None,
        ge=30,
        le=200,
        description="Player's weight in kilograms"
    )
    
    preferred_foot: Optional[str] = Field(
        None,
        description="Player's preferred foot (for applicable sports)"
    )
    
    biography: Optional[str] = Field(
        None,
        max_length=2000,
        description="Player biography"
    )
    
    photo_url: Optional[str] = Field(
        None,
        max_length=500,
        description="URL to player's photo"
    )
    
    social_media: Optional[dict] = Field(
        None,
        description="Social media links (JSON object)"
    )
    
    contract_start: Optional[date] = Field(
        None,
        description="Contract start date"
    )
    
    contract_end: Optional[date] = Field(
        None,
        description="Contract end date"
    )
    
    market_value: Optional[float] = Field(
        None,
        ge=0,
        description="Player's estimated market value"
    )
    
    salary: Optional[float] = Field(
        None,
        ge=0,
        description="Player's salary"
    )
    
    is_captain: bool = Field(
        False,
        description="Whether player is team captain"
    )
    
    is_vice_captain: bool = Field(
        False,
        description="Whether player is vice captain"
    )

    @field_validator('display_name')
    @classmethod
    def validate_display_name(cls, v: Optional[str], info) -> Optional[str]:
        """Auto-generate display name if not provided."""
        if v is None and 'first_name' in info.data and 'last_name' in info.data:
            return f"{info.data['first_name']} {info.data['last_name']}"
        return v

    @field_validator('contract_end')
    @classmethod
    def validate_contract_dates(cls, v: Optional[date], info) -> Optional[date]:
        """Validate that contract end is after start."""
        if v is not None and 'contract_start' in info.data and info.data['contract_start'] is not None:
            if v <= info.data['contract_start']:
                raise ValueError('Contract end date must be after start date')
        return v

    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: Optional[date]) -> Optional[date]:
        """Validate reasonable age range."""
        if v is not None:
            today = date.today()
            age = (today - v).days / 365.25
            if age < 10 or age > 60:
                raise ValueError('Player age must be between 10 and 60 years')
        return v


class PlayerCreate(PlayerBase):
    """Schema for creating a new player."""
    
    team_id: UUID = Field(
        ...,
        description="ID of the team this player belongs to"
    )


class PlayerUpdate(BaseModel):
    """Schema for updating an existing player."""
    
    first_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Player's first name"
    )
    
    last_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Player's last name"
    )
    
    display_name: Optional[str] = Field(
        None,
        max_length=200,
        description="Player's display/nickname"
    )
    
    jersey_number: Optional[int] = Field(
        None,
        ge=0,
        le=999,
        description="Player's jersey number"
    )
    
    position: Optional[PlayerPosition] = Field(
        None,
        description="Player's primary position"
    )
    
    secondary_positions: Optional[List[PlayerPosition]] = Field(
        None,
        description="List of secondary positions"
    )
    
    date_of_birth: Optional[date] = Field(
        None,
        description="Player's date of birth"
    )
    
    nationality: Optional[str] = Field(
        None,
        max_length=100,
        description="Player's nationality"
    )
    
    height_cm: Optional[int] = Field(
        None,
        ge=100,
        le=250,
        description="Player's height in centimeters"
    )
    
    weight_kg: Optional[float] = Field(
        None,
        ge=30,
        le=200,
        description="Player's weight in kilograms"
    )
    
    preferred_foot: Optional[str] = Field(
        None,
        description="Player's preferred foot"
    )
    
    biography: Optional[str] = Field(
        None,
        max_length=2000,
        description="Player biography"
    )
    
    photo_url: Optional[str] = Field(
        None,
        max_length=500,
        description="URL to player's photo"
    )
    
    social_media: Optional[dict] = Field(
        None,
        description="Social media links"
    )
    
    contract_start: Optional[date] = Field(
        None,
        description="Contract start date"
    )
    
    contract_end: Optional[date] = Field(
        None,
        description="Contract end date"
    )
    
    market_value: Optional[float] = Field(
        None,
        ge=0,
        description="Player's estimated market value"
    )
    
    salary: Optional[float] = Field(
        None,
        ge=0,
        description="Player's salary"
    )
    
    is_captain: Optional[bool] = Field(
        None,
        description="Whether player is team captain"
    )
    
    is_vice_captain: Optional[bool] = Field(
        None,
        description="Whether player is vice captain"
    )


class PlayerResponse(PlayerBase):
    """Schema for player responses."""
    
    id: UUID = Field(..., description="Player unique identifier")
    team_id: UUID = Field(..., description="Team ID this player belongs to")
    status: PlayerStatus = Field(..., description="Player status")
    created_at: datetime = Field(..., description="Player creation timestamp")
    updated_at: datetime = Field(..., description="Player last update timestamp")
    is_active: bool = Field(..., description="Whether player is active")

    class Config:
        from_attributes = True


class PlayerSummary(BaseModel):
    """Lightweight player schema for lists and references."""
    
    id: UUID = Field(..., description="Player unique identifier")
    first_name: str = Field(..., description="Player's first name")
    last_name: str = Field(..., description="Player's last name")
    display_name: Optional[str] = Field(None, description="Player's display name")
    jersey_number: Optional[int] = Field(None, description="Jersey number")
    position: Optional[PlayerPosition] = Field(None, description="Primary position")
    nationality: Optional[str] = Field(None, description="Player's nationality")
    status: PlayerStatus = Field(..., description="Player status")
    is_active: bool = Field(..., description="Whether player is active")

    class Config:
        from_attributes = True


class PlayerWithTeam(PlayerResponse):
    """Player response with team details."""
    
    team: dict = Field(..., description="Team details")

    class Config:
        from_attributes = True


class PlayerStats(BaseModel):
    """Player statistics schema."""
    
    # General stats
    matches_played = Field(..., description="Total matches played")
    matches_started = Field(..., description="Matches started")
    minutes_played = Field(..., description="Total minutes played")
    
    # Performance stats (sport-agnostic)
    goals_scored = Field(None, description="Goals/points scored")
    assists = Field(None, description="Assists")
    yellow_cards = Field(None, description="Yellow cards received")
    red_cards = Field(None, description="Red cards received")
    
    # Additional stats (JSON for sport-specific metrics)
    detailed_stats = Field(None, description="Sport-specific detailed statistics")
    
    # Season/period info
    season_id = Field(None, description="Season these stats are for")
    last_updated = Field(..., description="When stats were last updated")

    class Config:
        from_attributes = True


class PlayerWithStats(PlayerResponse):
    """Player response with statistics."""
    
    stats = Field(..., description="Player statistics")

    class Config:
        from_attributes = True


class PlayerTransfer(BaseModel):
    """Player transfer schema."""
    
    player_id = Field(..., description="Player ID")
    from_team_id = Field(None, description="Previous team ID")
    to_team_id = Field(..., description="New team ID")
    transfer_date = Field(..., description="Transfer date")
    transfer_fee = Field(None, description="Transfer fee")
    transfer_type = Field(..., description="Type of transfer")
    notes = Field(None, description="Transfer notes")

    class Config:
        from_attributes = True


class PlayerInjury(BaseModel):
    """Player injury schema."""
    
    player_id = Field(..., description="Player ID")
    injury_type = Field(..., description="Type of injury")
    injury_date = Field(..., description="When injury occurred")
    expected_return = Field(None, description="Expected return date")
    severity = Field(None, description="Injury severity")
    description = Field(None, description="Injury description")
    is_resolved = Field(False, description="Whether injury is resolved")

    class Config:
        from_attributes = True


class PlayerPerformanceRating(BaseModel):
    """Player performance rating schema."""
    
    player_id = Field(..., description="Player ID")
    match_id = Field(None, description="Match ID (if match-specific)")
    rating = Field(..., ge=0, le=10, description="Performance rating (0-10)")
    rating_source = Field(..., description="Source of the rating")
    notes = Field(None, description="Rating notes")
    created_at = Field(..., description="When rating was given")

    class Config:
        from_attributes = True


class PlayerSearchFilter(BaseModel):
    """Advanced player search filters."""
    
    team_id = Field(None, description="Filter by team")
    position = Field(None, description="Filter by position")
    nationality = Field(None, description="Filter by nationality")
    age_min = Field(None, ge=10, description="Minimum age")
    age_max = Field(None, le=60, description="Maximum age")
    status = Field(None, description="Filter by player status")
    is_captain = Field(None, description="Filter captains only")
    market_value_min = Field(None, description="Minimum market value")
    market_value_max = Field(None, description="Maximum market value")

    class Config:
        from_attributes = True