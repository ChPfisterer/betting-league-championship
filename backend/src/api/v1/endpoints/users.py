"""
User API endpoints.

This module provides REST API endpoints for user management including
CRUD operations, authentication, and user profile management.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import (
    get_db,
    http_not_found,
    http_forbidden,
    http_conflict,
    http_validation_error,
    PaginationParams,
    PaginatedResponse,
    paginate_query
)
from core.keycloak_security import get_current_user_hybrid, get_current_user_id_hybrid
from models.user import User, UserStatus
from api.schemas.user import (
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserResponse,
    UserProfile,
    UserSummary
)
from services.user_service import UserService

router = APIRouter()


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Get current user profile",
    description="Retrieve the authenticated user's profile with statistics"
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user_hybrid)
) -> UserProfile:
    """Get current user's profile."""
    return UserService.get_user_profile(current_user)


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="Update the authenticated user's profile information"
)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Update current user's profile."""
    try:
        updated_user = UserService.update_user(db, current_user.id, user_update)
        return UserResponse.from_orm(updated_user)
    except ValueError as e:
        raise http_validation_error(str(e))


@router.put(
    "/me/password",
    response_model=dict,
    summary="Update current user password",
    description="Update the authenticated user's password"
)
async def update_current_user_password(
    password_update: UserPasswordUpdate,
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
) -> dict:
    """Update current user's password."""
    try:
        UserService.update_user_password(
            db, 
            current_user.id, 
            password_update.current_password,
            password_update.new_password
        )
        return {"message": "Password updated successfully"}
    except ValueError as e:
        raise http_validation_error(str(e))


@router.get(
    "",
    response_model=PaginatedResponse[UserSummary],
    summary="List users",
    description="Retrieve a paginated list of users with optional filtering"
)
async def list_users(
    pagination: PaginationParams = Depends(),
    status_filter: Optional[UserStatus] = Query(None, description="Filter by user status"),
    search: Optional[str] = Query(None, description="Search in username, email, or name"),
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id_hybrid)  # Require authentication
) -> PaginatedResponse[UserSummary]:
    """List users with pagination and filtering."""
    query = UserService.build_user_list_query(db, status_filter, search)
    
    # Apply pagination
    paginated = paginate_query(query, db, pagination)
    
    # Convert to summary format
    paginated.items = [UserSummary.from_orm(user) for user in paginated.items]
    
    return paginated


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID"
)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id_hybrid)  # Require authentication
) -> UserResponse:
    """Get user by ID."""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise http_not_found("User", str(user_id))
    
    return UserResponse.from_orm(user)


@router.get(
    "/{user_id}/profile",
    response_model=UserProfile,
    summary="Get user profile",
    description="Retrieve a user's profile with statistics"
)
async def get_user_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id_hybrid)  # Require authentication
) -> UserProfile:
    """Get user profile with statistics."""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise http_not_found("User", str(user_id))
    
    return UserService.get_user_profile(user)


@router.get(
    "/username/{username}",
    response_model=UserResponse,
    summary="Get user by username",
    description="Retrieve a specific user by their username"
)
async def get_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id_hybrid)  # Require authentication
) -> UserResponse:
    """Get user by username."""
    user = UserService.get_user_by_username(db, username)
    if not user:
        raise http_not_found("User", username)
    
    return UserResponse.from_orm(user)


@router.put(
    "/{user_id}/status",
    response_model=UserResponse,
    summary="Update user status",
    description="Update a user's status (admin only)"
)
async def update_user_status(
    user_id: UUID,
    new_status: UserStatus,
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Update user status (admin only)."""
    # Check if current user is admin
    if not UserService.is_admin(current_user):
        raise http_forbidden("Admin access required")
    
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise http_not_found("User", str(user_id))
    
    try:
        updated_user = UserService.update_user_status(db, user_id, new_status)
        return UserResponse.from_orm(updated_user)
    except ValueError as e:
        raise http_validation_error(str(e))


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user account (admin only or self)"
)
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
) -> None:
    """Delete user account."""
    # Check if current user is admin or deleting their own account
    if not (UserService.is_admin(current_user) or current_user.id == user_id):
        raise http_forbidden("Can only delete your own account or admin access required")
    
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise http_not_found("User", str(user_id))
    
    try:
        UserService.delete_user(db, user_id)
    except ValueError as e:
        raise http_validation_error(str(e))