"""
Pydantic schemas for Team API endpoints.

This module defines request and response models for Team-related
API operations including validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, field_validator


class TeamBase(BaseModel):
    """Base team schema with common fields."""
    
    name: str
    short_name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    is_active: bool = True
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate team name."""
        if not v or len(v.strip()) < 2:
            raise ValueError('Team name must be at least 2 characters long')
        if len(v) > 100:
            raise ValueError('Team name must not exceed 100 characters')
        return v.strip()
    
    @field_validator('short_name')
    @classmethod
    def validate_short_name(cls, v):
        """Validate team short name."""
        if v is not None:
            v = v.strip()
            if len(v) > 10:
                raise ValueError('Short name must not exceed 10 characters')
            return v if v else None
        return v
    
    @field_validator('city', 'country')
    @classmethod
    def validate_location(cls, v):
        """Validate location fields."""
        if v is not None:
            v = v.strip()
            if len(v) > 100:
                raise ValueError('Location field must not exceed 100 characters')
            return v if v else None
        return v
    
    @field_validator('founded_year')
    @classmethod
    def validate_founded_year(cls, v):
        """Validate founded year."""
        if v is not None:
            if v < 1800 or v > 2030:
                raise ValueError('Founded year must be between 1800 and 2030')
        return v
    
    @field_validator('logo_url', 'website_url')
    @classmethod
    def validate_urls(cls, v):
        """Validate URL fields."""
        if v is not None:
            v = v.strip()
            if len(v) > 500:
                raise ValueError('URL must not exceed 500 characters')
            return v if v else None
        return v


class TeamCreate(TeamBase):
    """Schema for creating a new team."""
    
    sport_id: UUID
    
    @field_validator('sport_id')
    @classmethod
    def validate_sport_id(cls, v):
        """Validate sport ID is provided."""
        if not v:
            raise ValueError('Sport ID is required')
        return v


class TeamUpdate(BaseModel):
    """Schema for updating team information."""
    
    name: Optional[str] = None
    short_name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    is_active: Optional[bool] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate team name."""
        if v is not None:
            if not v or len(v.strip()) < 2:
                raise ValueError('Team name must be at least 2 characters long')
            if len(v) > 100:
                raise ValueError('Team name must not exceed 100 characters')
            return v.strip()
        return v
    
    @field_validator('short_name')
    @classmethod
    def validate_short_name(cls, v):
        """Validate team short name."""
        if v is not None:
            v = v.strip()
            if len(v) > 10:
                raise ValueError('Short name must not exceed 10 characters')
            return v if v else None
        return v
    
    @field_validator('city', 'country')
    @classmethod
    def validate_location(cls, v):
        """Validate location fields."""
        if v is not None:
            v = v.strip()
            if len(v) > 100:
                raise ValueError('Location field must not exceed 100 characters')
            return v if v else None
        return v
    
    @field_validator('founded_year')
    @classmethod
    def validate_founded_year(cls, v):
        """Validate founded year."""
        if v is not None:
            if v < 1800 or v > 2030:
                raise ValueError('Founded year must be between 1800 and 2030')
        return v
    
    @field_validator('logo_url', 'website_url')
    @classmethod
    def validate_urls(cls, v):
        """Validate URL fields."""
        if v is not None:
            v = v.strip()
            if len(v) > 500:
                raise ValueError('URL must not exceed 500 characters')
            return v if v else None
        return v


class TeamResponse(TeamBase):
    """Schema for team responses."""
    
    id: UUID
    sport_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class TeamSummary(BaseModel):
    """Minimal team summary for lists."""
    
    id: UUID
    name: str
    short_name: Optional[str] = None
    sport_id: UUID
    is_active: bool
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class TeamWithStats(TeamResponse):
    """Extended team schema with statistics."""
    
    total_matches: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    win_percentage: float = 0.0
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class TeamWithSport(TeamResponse):
    """Team schema with sport information."""
    
    sport_name: str
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True