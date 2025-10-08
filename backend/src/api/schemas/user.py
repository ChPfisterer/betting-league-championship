"""
Pydantic schemas for User API endpoints.

This module defines request and response models for User-related
API operations including validation and serialization.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
import re

from pydantic import BaseModel, EmailStr, field_validator, validator

from models.user import UserStatus
from core.config import settings


class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    username: str
    email: str  # Changed from EmailStr to str for custom validation
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format with development support for .local domains."""
        if not v:
            raise ValueError('Email is required')
        
        # Basic email pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # In development/debug mode, allow .local domains
        if settings.debug:
            local_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.local$'
            if re.match(local_pattern, v):
                return v
        
        # Standard email validation
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        
        return v
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Validate username format."""
        if not v or len(v.strip()) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username must not exceed 50 characters')
        return v.strip()
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        """Validate name fields."""
        if v is not None:
            v = v.strip()
            if len(v) > 100:
                raise ValueError('Name must not exceed 100 characters')
            return v if v else None
        return v


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('Password must not exceed 128 characters')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        """Validate name fields."""
        if v is not None:
            v = v.strip()
            if len(v) > 100:
                raise ValueError('Name must not exceed 100 characters')
            return v if v else None
        return v


class UserPasswordUpdate(BaseModel):
    """Schema for updating user password."""
    
    current_password: str
    new_password: str
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('Password must not exceed 128 characters')
        return v


class UserResponse(UserBase):
    """Schema for user responses."""
    
    id: UUID
    status: UserStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class UserProfile(UserResponse):
    """Extended user profile schema."""
    
    total_bets: int = 0
    total_winnings: float = 0.0
    win_rate: float = 0.0
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class UserSummary(BaseModel):
    """Minimal user summary for lists."""
    
    id: UUID
    username: str
    status: UserStatus
    
    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    
    username: str
    password: str


class UserLoginResponse(BaseModel):
    """Schema for login response."""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class UserRegistrationResponse(BaseModel):
    """Schema for registration response."""
    
    user: UserResponse
    message: str = "User registered successfully"