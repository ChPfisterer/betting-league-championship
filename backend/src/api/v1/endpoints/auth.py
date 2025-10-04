"""
Authentication API endpoints.

This module provides authentication endpoints including login,
registration, and token management.
"""

from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import (
    get_db,
    create_access_token,
    settings,
    http_validation_error,
    http_conflict
)
from api.schemas.user import (
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserRegistrationResponse,
    UserResponse
)
from services.user_service import UserService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register a new user account with username, email, and password"
)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserRegistrationResponse:
    """Register a new user."""
    try:
        user = UserService.create_user(db, user_data)
        return UserRegistrationResponse(
            user=UserResponse.from_orm(user),
            message="User registered successfully"
        )
    except ValueError as e:
        raise http_validation_error(str(e))


@router.post(
    "/login",
    response_model=UserLoginResponse,
    summary="User login",
    description="Authenticate user and return access token"
)
async def login_user(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
) -> UserLoginResponse:
    """Authenticate user and return access token."""
    user = UserService.authenticate_user(
        db, 
        user_credentials.username, 
        user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return UserLoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=UserResponse.from_orm(user)
    )


@router.post(
    "/login/oauth",
    response_model=UserLoginResponse,
    summary="OAuth login",
    description="Login using OAuth2 password flow (FastAPI docs compatibility)"
)
async def oauth_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> UserLoginResponse:
    """OAuth2 compatible login endpoint for FastAPI docs."""
    user = UserService.authenticate_user(
        db, 
        form_data.username, 
        form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return UserLoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=UserResponse.from_orm(user)
    )


@router.post(
    "/logout",
    response_model=Dict[str, str],
    summary="User logout",
    description="Logout user (client should discard token)"
)
async def logout_user() -> Dict[str, str]:
    """
    Logout user.
    
    Note: With JWT tokens, actual logout is handled client-side by discarding the token.
    This endpoint is provided for API consistency and future token blacklisting.
    """
    return {"message": "Logged out successfully"}