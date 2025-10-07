"""
Keycloak-aware security utilities and authentication.

This module provides security functions that integrate with both
traditional JWT authentication and Keycloak OAuth 2.0 tokens.
"""

import logging
from typing import Optional, Union
from uuid import UUID
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.security import get_current_user as get_current_user_traditional
from services.keycloak_service import KeycloakService, get_keycloak_service
from models.user import User
from core.database import get_db


# Configure logging
logger = logging.getLogger(__name__)

# Security scheme for Keycloak OAuth
keycloak_oauth2 = HTTPBearer(auto_error=False)


class OAuth2Helper:
    """Helper class for OAuth 2.0 operations with Keycloak."""
    
    @staticmethod
    def extract_token_from_header(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(keycloak_oauth2)
    ) -> Optional[str]:
        """
        Extract bearer token from Authorization header.
        
        Args:
            credentials: HTTP Authorization credentials
            
        Returns:
            Token string if present, None otherwise
        """
        if credentials and credentials.scheme.lower() == "bearer":
            return credentials.credentials
        return None


async def get_current_user_from_keycloak(
    token: Optional[str] = Depends(OAuth2Helper.extract_token_from_header),
    keycloak_service: KeycloakService = Depends(get_keycloak_service),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from Keycloak access token.
    
    This function validates a Keycloak-issued JWT token, extracts user information,
    and synchronizes the user with the local database.
    
    Args:
        token: JWT access token from Authorization header
        keycloak_service: Keycloak service for token validation
        db: Database session
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException: If token is invalid or user authentication fails
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Validate token with Keycloak
        token_info = keycloak_service.validate_token(token)
        
        # Sync user with local database (skip for service accounts)
        user = keycloak_service.sync_user_with_keycloak(token_info)
        
        # For service accounts, user will be None - they don't need database sync
        if user is not None and not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )
        
        if user:
            logger.info(f"Successfully authenticated user: {user.username} via Keycloak")
        return user
        
    except ValueError as e:
        # Token validation failed
        logger.warning(f"Invalid Keycloak token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Other authentication errors
        logger.error(f"Keycloak authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )


async def get_current_user_hybrid(
    token: Optional[str] = Depends(OAuth2Helper.extract_token_from_header),
    keycloak_service: KeycloakService = Depends(get_keycloak_service),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from Keycloak access token only.
    
    This function authenticates users exclusively through Keycloak OAuth 2.0 tokens.
    Traditional JWT authentication has been removed.
    
    Args:
        token: JWT access token from Authorization header
        keycloak_service: Keycloak service for token validation
        db: Database session
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException: If Keycloak authentication fails
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token required. Please login with Keycloak.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Authenticate using Keycloak only
    return await get_current_user_from_keycloak(token, keycloak_service, db)


async def get_current_user_id_hybrid(
    current_user: User = Depends(get_current_user_hybrid)
) -> UUID:
    """
    Get current user ID from Keycloak authentication.
    
    This is a convenience function for endpoints that only need user ID
    for authentication verification without the full user object.
    
    Args:
        current_user: Current authenticated user from Keycloak
        
    Returns:
        User ID (UUID)
    """
    return current_user.id


async def require_admin(
    current_user: User = Depends(get_current_user_from_keycloak)
) -> User:
    """
    Require admin privileges for the current user (Keycloak version).
    
    Args:
        current_user: Current authenticated user from Keycloak
        
    Returns:
        User object if admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.is_admin:
        logger.warning(f"Admin access denied for user: {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user


async def require_admin_hybrid(
    current_user: User = Depends(get_current_user_hybrid)
) -> User:
    """
    Require admin privileges supporting both authentication methods.
    
    Args:
        current_user: Current authenticated user (Keycloak or traditional)
        
    Returns:
        User object if admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.is_admin:
        logger.warning(f"Admin access denied for user: {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user


def validate_keycloak_token_sync(token: str, keycloak_service: KeycloakService) -> dict:
    """
    Synchronous token validation for non-async contexts.
    
    Args:
        token: JWT access token
        keycloak_service: Keycloak service instance
        
    Returns:
        Decoded token information
        
    Raises:
        ValueError: If token is invalid
    """
    try:
        return keycloak_service.validate_token(token)
    except Exception as e:
        raise ValueError(f"Token validation failed: {e}")


# Convenience functions for backward compatibility
async def get_current_active_user_keycloak(
    current_user: User = Depends(get_current_user_from_keycloak)
) -> User:
    """
    Get current active user via Keycloak (alias for get_current_user_from_keycloak).
    
    Args:
        current_user: Current user from Keycloak authentication
        
    Returns:
        Active user object
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
    return current_user
