"""
Competition Pydantic schemas for API serialization and validation.

This module defines comprehensive schemas for competition operations including
creation, updates, responses, and statistics. Competitions organize teams
within sports and provide the framework for matches and betting.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from enum import Enum

from .sport import SportSummary
from .team import TeamSummary


class CompetitionStatus(str, Enum):
    """Competition status enumeration."""
    DRAFT = "draft"
    UPCOMING = "upcoming"  
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"


class CompetitionFormat(str, Enum):
    """Competition format enumeration."""
    LEAGUE = "league"
    TOURNAMENT = "tournament"
    CUP = "cup"
    PLAYOFF = "playoff"
    ROUND_ROBIN = "round_robin"
    KNOCKOUT = "knockout"
    SWISS = "swiss"


class CompetitionBase(BaseModel):
    """Base competition schema with common fields."""
    
    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Competition name"
    )
    
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Competition description"
    )
    
    format: CompetitionFormat = Field(
        ...,
        description="Competition format"
    )
    
    start_date: Optional[datetime] = Field(
        None,
        description="Competition start date"
    )
    
    end_date: Optional[datetime] = Field(
        None,
        description="Competition end date"
    )
    
    registration_deadline: Optional[datetime] = Field(
        None,
        description="Team registration deadline"
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
    
    entry_fee: Optional[float] = Field(
        None,
        ge=0,
        description="Competition entry fee"
    )
    
    prize_pool: Optional[float] = Field(
        None,
        ge=0,
        description="Total prize pool"
    )
    
    rules: Optional[str] = Field(
        None,
        max_length=5000,
        description="Competition rules and regulations"
    )
    
    location: Optional[str] = Field(
        None,
        max_length=200,
        description="Competition location/venue"
    )
    
    website: Optional[str] = Field(
        None,
        max_length=500,
        description="Competition website URL"
    )
    
    is_public: bool = Field(
        True,
        description="Whether competition is publicly visible"
    )
    
    allow_betting: bool = Field(
        True,
        description="Whether betting is allowed on this competition"
    )

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate that end date is after start date."""
        if v is not None and 'start_date' in info.data and info.data['start_date'] is not None:
            if v <= info.data['start_date']:
                raise ValueError('End date must be after start date')
        return v

    @field_validator('registration_deadline')
    @classmethod
    def validate_registration_deadline(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate that registration deadline is before start date."""
        if v is not None and 'start_date' in info.data and info.data['start_date'] is not None:
            if v >= info.data['start_date']:
                raise ValueError('Registration deadline must be before start date')
        return v

    @field_validator('max_teams')
    @classmethod
    def validate_max_teams(cls, v: Optional[int], info) -> Optional[int]:
        """Validate that max teams is greater than min teams."""
        if v is not None and 'min_teams' in info.data and info.data['min_teams'] is not None:
            if v < info.data['min_teams']:
                raise ValueError('Maximum teams must be greater than or equal to minimum teams')
        return v

    @field_validator('website')
    @classmethod
    def validate_website_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate website URL format."""
        if v is not None and v.strip():
            v = v.strip()
            if not (v.startswith('http://') or v.startswith('https://')):
                v = f'https://{v}'
        return v if v and v.strip() else None


class CompetitionCreate(CompetitionBase):
    """Schema for creating a new competition."""
    
    sport_id: UUID = Field(
        ...,
        description="ID of the sport this competition belongs to"
    )


class CompetitionUpdate(BaseModel):
    """Schema for updating an existing competition."""
    
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=200,
        description="Competition name"
    )
    
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Competition description"
    )
    
    format: Optional[CompetitionFormat] = Field(
        None,
        description="Competition format"
    )
    
    start_date: Optional[datetime] = Field(
        None,
        description="Competition start date"
    )
    
    end_date: Optional[datetime] = Field(
        None,
        description="Competition end date"
    )
    
    registration_deadline: Optional[datetime] = Field(
        None,
        description="Team registration deadline"
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
    
    entry_fee: Optional[float] = Field(
        None,
        ge=0,
        description="Competition entry fee"
    )
    
    prize_pool: Optional[float] = Field(
        None,
        ge=0,
        description="Total prize pool"
    )
    
    rules: Optional[str] = Field(
        None,
        max_length=5000,
        description="Competition rules and regulations"
    )
    
    location: Optional[str] = Field(
        None,
        max_length=200,
        description="Competition location/venue"
    )
    
    website: Optional[str] = Field(
        None,
        max_length=500,
        description="Competition website URL"
    )
    
    is_public: Optional[bool] = Field(
        None,
        description="Whether competition is publicly visible"
    )
    
    allow_betting: Optional[bool] = Field(
        None,
        description="Whether betting is allowed on this competition"
    )

    @field_validator('website')
    @classmethod
    def validate_website_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate website URL format."""
        if v is not None and v.strip():
            v = v.strip()
            if not (v.startswith('http://') or v.startswith('https://')):
                v = f'https://{v}'
        return v if v and v.strip() else None


class CompetitionResponse(CompetitionBase):
    """Schema for competition responses."""
    
    id: UUID = Field(..., description="Competition unique identifier")
    sport_id: UUID = Field(..., description="Sport ID this competition belongs to")
    status: CompetitionStatus = Field(..., description="Current competition status")
    created_at: datetime = Field(..., description="Competition creation timestamp")
    updated_at: datetime = Field(..., description="Competition last update timestamp")
    is_active: bool = Field(..., description="Whether competition is active")

    class Config:
        from_attributes = True


class CompetitionSummary(BaseModel):
    """Lightweight competition schema for lists and references."""
    
    id: UUID = Field(..., description="Competition unique identifier")
    name: str = Field(..., description="Competition name")
    format: CompetitionFormat = Field(..., description="Competition format")
    status: CompetitionStatus = Field(..., description="Current competition status")
    start_date: Optional[datetime] = Field(None, description="Competition start date")
    end_date: Optional[datetime] = Field(None, description="Competition end date")
    is_active: bool = Field(..., description="Whether competition is active")
    is_public: bool = Field(..., description="Whether competition is publicly visible")
    allow_betting: bool = Field(..., description="Whether betting is allowed")

    class Config:
        from_attributes = True


class CompetitionWithSport(CompetitionResponse):
    """Competition response with sport details."""
    
    sport: SportSummary = Field(..., description="Sport details")

    class Config:
        from_attributes = True


class CompetitionStats(BaseModel):
    """Competition statistics schema."""
    
    total_teams: int = Field(..., description="Total number of registered teams")
    total_matches: int = Field(..., description="Total number of matches")
    completed_matches: int = Field(..., description="Number of completed matches")
    pending_matches: int = Field(..., description="Number of pending matches")
    total_bets: int = Field(..., description="Total number of bets placed")
    total_bet_amount: float = Field(..., description="Total amount bet")
    days_remaining: Optional[int] = Field(None, description="Days until competition ends")
    participation_rate: float = Field(..., description="Team participation rate (0-100)")

    class Config:
        from_attributes = True


class CompetitionWithStats(CompetitionResponse):
    """Competition response with statistics."""
    
    stats: CompetitionStats = Field(..., description="Competition statistics")

    class Config:
        from_attributes = True


class CompetitionTeamRegistration(BaseModel):
    """Schema for team registration in competition."""
    
    team_id: UUID = Field(..., description="Team ID to register")
    registration_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Registration notes"
    )

    class Config:
        from_attributes = True


class CompetitionTeamList(BaseModel):
    """Schema for listing teams in a competition."""
    
    competition_id: UUID = Field(..., description="Competition ID")
    teams: List[TeamSummary] = Field(..., description="List of registered teams")
    total_teams: int = Field(..., description="Total number of teams")
    max_teams: Optional[int] = Field(None, description="Maximum allowed teams")
    registration_open: bool = Field(..., description="Whether registration is still open")

    class Config:
        from_attributes = True