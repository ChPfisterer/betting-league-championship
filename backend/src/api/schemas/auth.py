"""
Authentication schemas for API responses.

This module contains Pydantic models for authentication-related API responses,
including token responses for both traditional and OAuth 2.0 authentication.
"""

from typing import Optional
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Response model for authentication token endpoints."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="Refresh token for token renewal")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user_id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="User email address")
    is_admin: bool = Field(..., description="Whether user has admin privileges")


class RefreshTokenResponse(BaseModel):
    """Response model for token refresh endpoints."""
    access_token: str = Field(..., description="New JWT access token")
    refresh_token: Optional[str] = Field(None, description="New refresh token (if rotated)")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class LogoutResponse(BaseModel):
    """Response model for logout endpoints."""
    message: str = Field(..., description="Logout confirmation message")
    logout_url: Optional[str] = Field(None, description="Optional logout URL for external providers")