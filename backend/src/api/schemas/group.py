"""
Pydantic schemas for Group API endpoints.

This module defines request and response models for Group-related
API operations including validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, field_validator

from models.group import GroupType, GroupVisibility


class GroupBase(BaseModel):
    """Base group schema with common fields."""
    
    name: str
    description: Optional[str] = None
    group_type: GroupType
    visibility: GroupVisibility = GroupVisibility.PUBLIC
    max_members: Optional[int] = None
    
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
        if v is not None:
            v = v.strip()
            if len(v) > 500:
                raise ValueError('Description must not exceed 500 characters')
            return v if v else None
        return v
    
    @field_validator('max_members')
    @classmethod
    def validate_max_members(cls, v):
        """Validate max members limit."""
        if v is not None and v <= 0:
            raise ValueError('Max members must be greater than 0')
        return v


class GroupCreate(GroupBase):
    """Schema for creating a new group."""
    pass


class GroupUpdate(BaseModel):
    """Schema for updating group information."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[GroupVisibility] = None
    max_members: Optional[int] = None
    
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
            v = v.strip()
            if len(v) > 500:
                raise ValueError('Description must not exceed 500 characters')
            return v if v else None
        return v
    
    @field_validator('max_members')
    @classmethod
    def validate_max_members(cls, v):
        """Validate max members limit."""
        if v is not None and v <= 0:
            raise ValueError('Max members must be greater than 0')
        return v


class GroupResponse(GroupBase):
    """Schema for group responses."""
    
    id: UUID
    creator_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    member_count: int = 0
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class GroupSummary(BaseModel):
    """Minimal group summary for lists."""
    
    id: UUID
    name: str
    group_type: GroupType
    visibility: GroupVisibility
    member_count: int = 0
    
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