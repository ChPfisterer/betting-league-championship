"""
Keycloak OAuth 2.0 Authentication API endpoints.

This module provides Keycloak OAuth 2.0 authentication endpoints only.
Traditional username/password authentication has been removed.
"""

from typing import Dict
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core import get_db, settings
from services.keycloak_service import KeycloakService, get_keycloak_service

router = APIRouter()


@router.get(
    "/authorize",
    response_model=Dict[str, str],
    summary="Get OAuth authorization URL",
    description="Get Keycloak authorization URL for OAuth 2.0 flow"
)
async def get_authorization_url(
    keycloak_service: KeycloakService = Depends(get_keycloak_service)
) -> Dict[str, str]:
    """
    Get Keycloak OAuth 2.0 authorization URL.
    
    Returns:
        Dict containing the authorization URL for redirect
    """
    try:
        auth_url = keycloak_service.get_authorization_url()
        return {"authorize_url": auth_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate authorization URL: {str(e)}"
        )


@router.post(
    "/callback",
    response_model=Dict[str, str],
    summary="OAuth callback handler", 
    description="Handle OAuth 2.0 callback with authorization code"
)
async def oauth_callback(
    code: str = Query(..., description="Authorization code from OAuth provider"),
    state: str = Query(None, description="OAuth state parameter"),
    keycloak_service: KeycloakService = Depends(get_keycloak_service),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Handle OAuth 2.0 callback and exchange code for access token.
    
    Args:
        code: Authorization code from Keycloak
        state: OAuth state parameter
        keycloak_service: Keycloak service
        db: Database session
        
    Returns:
        Dict containing access token and user information
    """
    try:
        # Exchange authorization code for access token
        token_response = keycloak_service.exchange_code_for_token(code)
        
        # Validate the token and sync user
        token_info = keycloak_service.validate_token(token_response["access_token"])
        user = keycloak_service.sync_user_with_keycloak(token_info)
        
        return {
            "access_token": token_response["access_token"],
            "token_type": "bearer",
            "expires_in": str(token_response.get("expires_in", 3600)),
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth callback failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@router.post(
    "/logout",
    response_model=Dict[str, str],
    summary="User logout",
    description="Logout user from Keycloak and invalidate session"
)
async def logout_user(
    keycloak_service: KeycloakService = Depends(get_keycloak_service)
) -> Dict[str, str]:
    """
    Logout user from Keycloak.
    
    Args:
        keycloak_service: Keycloak service
        
    Returns:
        Success message and logout URL
    """
    try:
        logout_url = keycloak_service.get_logout_url()
        return {
            "message": "Logged out successfully", 
            "logout_url": logout_url
        }
    except Exception as e:
        # Even if Keycloak logout fails, we can still return success
        # as the client should discard the token
        return {"message": "Logged out successfully (client-side)"}