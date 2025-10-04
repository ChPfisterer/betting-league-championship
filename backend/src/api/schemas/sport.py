"""
Pydantic schemas for Sport API endpoints.

This module defines request and response models for Sport-related
API operations including validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, field_validator


class SportBase(BaseModel):
    """Base sport schema with common fields."""
    
    name: str
    description: Optional[str] = None
    rules: Optional[str] = None
    is_active: bool = True
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate sport name."""
        if not v or len(v.strip()) < 2:
            raise ValueError('Sport name must be at least 2 characters long')
        if len(v) > 100:
            raise ValueError('Sport name must not exceed 100 characters')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        """Validate sport description."""
        if v is not None:
            v = v.strip()
            if len(v) > 1000:
                raise ValueError('Description must not exceed 1000 characters')
            return v if v else None
        return v
    
    @field_validator('rules')
    @classmethod
    def validate_rules(cls, v):
        """Validate sport rules."""
        if v is not None:
            v = v.strip()
            if len(v) > 5000:
                raise ValueError('Rules must not exceed 5000 characters')
            return v if v else None
        return v


class SportCreate(SportBase):
    """Schema for creating a new sport."""
    pass


class SportUpdate(BaseModel):
    """Schema for updating sport information."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[str] = None
    is_active: Optional[bool] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate sport name."""
        if v is not None:
            if not v or len(v.strip()) < 2:
                raise ValueError('Sport name must be at least 2 characters long')
            if len(v) > 100:
                raise ValueError('Sport name must not exceed 100 characters')
            return v.strip()
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        """Validate sport description."""
        if v is not None:
            v = v.strip()
            if len(v) > 1000:
                raise ValueError('Description must not exceed 1000 characters')
            return v if v else None
        return v
    
    @field_validator('rules')
    @classmethod
    def validate_rules(cls, v):
        """Validate sport rules."""
        if v is not None:
            v = v.strip()
            if len(v) > 5000:
                raise ValueError('Rules must not exceed 5000 characters')
            return v if v else None
        return v


class SportResponse(SportBase):
    """Schema for sport responses."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class SportSummary(BaseModel):
    """Minimal sport summary for lists."""
    
    id: UUID
    name: str
    is_active: bool
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class SportWithStats(SportResponse):
    """Extended sport schema with statistics."""
    
    total_teams: int = 0
    total_competitions: int = 0
    total_matches: int = 0
    active_competitions: int = 0
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True