"""
Pydantic schemas for Group API endpoints.

This module defines request and response models for Group-related
API operations including validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, field_validator

from models.group import PointSystem


class GroupBase(BaseModel):
    """Base group schema with common fields."""
    
    name: str
    description: str
    is_private: bool = False
    max_members: int = 50
    allow_member_invites: bool = True
    auto_approve_members: bool = True
    point_system: PointSystem = PointSystem.STANDARD
    avatar_url: Optional[str] = None
    banner_url: Optional[str] = None
    rules_text: Optional[str] = None
    entry_fee: Optional[float] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate group name."""
        if not v or len(v.strip()) < 3:
            raise ValueError('Group name must be at least 3 characters long')
        if len(v) > 100:
            raise ValueError('Group name must not exceed 100 characters')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        """Validate group description."""
        if not v or len(v.strip()) < 10:
            raise ValueError('Group description must be at least 10 characters long')
        return v.strip()
    
    @field_validator('max_members')
    @classmethod
    def validate_max_members(cls, v):
        """Validate max members limit."""
        if v <= 0:
            raise ValueError('Max members must be greater than 0')
        if v > 1000:
            raise ValueError('Max members cannot exceed 1000')
        return v


class GroupCreate(GroupBase):
    """Schema for creating a new group."""
    pass


class GroupUpdate(BaseModel):
    """Schema for updating group information."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    is_private: Optional[bool] = None
    max_members: Optional[int] = None
    allow_member_invites: Optional[bool] = None
    auto_approve_members: Optional[bool] = None
    point_system: Optional[PointSystem] = None
    avatar_url: Optional[str] = None
    banner_url: Optional[str] = None
    rules_text: Optional[str] = None
    entry_fee: Optional[float] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate group name."""
        if v is not None:
            if not v or len(v.strip()) < 3:
                raise ValueError('Group name must be at least 3 characters long')
            if len(v) > 100:
                raise ValueError('Group name must not exceed 100 characters')
            return v.strip()
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        """Validate group description."""
        if v is not None:
            if not v or len(v.strip()) < 10:
                raise ValueError('Group description must be at least 10 characters long')
            return v.strip()
        return v
    
    @field_validator('max_members')
    @classmethod
    def validate_max_members(cls, v):
        """Validate max members limit."""
        if v is not None:
            if v <= 0:
                raise ValueError('Max members must be greater than 0')
            if v > 1000:
                raise ValueError('Max members cannot exceed 1000')
        return v


class GroupResponse(GroupBase):
    """Schema for group responses."""
    
    id: UUID
    creator_id: UUID
    join_code: Optional[str] = None
    prize_pool: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    member_count: int = 0
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class GroupSummary(BaseModel):
    """Minimal group summary for lists."""
    
    id: UUID
    name: str
    is_private: bool
    member_count: int = 0
    point_system: PointSystem
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class GroupWithStats(GroupResponse):
    """Extended group schema with statistics."""
    
    total_bets: int = 0
    active_bets: int = 0
    total_winnings: float = 0.0
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True