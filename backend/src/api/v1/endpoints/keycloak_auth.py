"""
Keycloak OAuth 2.0 authentication endpoints.

This module provides OAuth 2.0 authorization code flow endpoints
for integration with Keycloak authentication server.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel, Field

from core.keycloak_security import keycloak_oauth2, get_current_user_from_keycloak
from services.keycloak_service import KeycloakService
from api.schemas.auth import TokenResponse


router = APIRouter()


class AuthorizeUrlResponse(BaseModel):
    """Response containing OAuth authorization URL."""
    authorize_url: str = Field(..., description="OAuth authorization URL to redirect user to")
    state: str = Field(..., description="OAuth state parameter for CSRF protection")


class TokenRequest(BaseModel):
    """Request to exchange authorization code for tokens."""
    code: str = Field(..., description="Authorization code from OAuth callback")
    state: str = Field(..., description="OAuth state parameter for verification")
    redirect_uri: str = Field(..., description="Redirect URI used in authorization request")


class RefreshTokenRequest(BaseModel):
    """Request to refresh access token."""
    refresh_token: str = Field(..., description="Refresh token")


@router.get("/oauth/authorize-url", response_model=AuthorizeUrlResponse)
async def get_authorize_url(
    redirect_uri: str
) -> AuthorizeUrlResponse:
    """
    Get OAuth 2.0 authorization URL for Keycloak login.
    
    Args:
        redirect_uri: The URI to redirect to after authorization
        
    Returns:
        Authorization URL and state parameter
        
    Raises:
        HTTPException: If authorization URL generation fails
    """
    try:
        keycloak_service = KeycloakService()
        auth_url, state = keycloak_service.get_authorization_url(redirect_uri)
        return AuthorizeUrlResponse(authorize_url=auth_url, state=state)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate authorization URL: {str(e)}"
        )


@router.post("/oauth/token", response_model=TokenResponse)
async def exchange_code_for_token(
    token_request: TokenRequest
) -> TokenResponse:
    """
    Exchange authorization code for access and refresh tokens.
    
    Args:
        token_request: Authorization code exchange request
        
    Returns:
        Access token, refresh token, and user information
        
    Raises:
        HTTPException: If token exchange fails
    """
    try:
        keycloak_service = KeycloakService()
        # Exchange authorization code for tokens
        token_data = keycloak_service.exchange_authorization_code(
            code=token_request.code,
            redirect_uri=token_request.redirect_uri,
            state=token_request.state
        )
        
        # Validate and decode the access token
        user_info = keycloak_service.validate_token(token_data["access_token"])
        
        # Sync user with local database
        user = keycloak_service.sync_user_with_keycloak(user_info)
        
        return TokenResponse(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_type="bearer",
            expires_in=token_data.get("expires_in", 3600),
            user_id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid authorization code or state: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token exchange failed: {str(e)}"
        )


@router.post("/oauth/refresh", response_model=TokenResponse)
async def refresh_access_token(
    refresh_request: RefreshTokenRequest
) -> TokenResponse:
    """
    Refresh access token using refresh token.
    
    Args:
        refresh_request: Refresh token request
        
    Returns:
        New access token and user information
        
    Raises:
        HTTPException: If token refresh fails
    """
    try:
        keycloak_service = KeycloakService()
        # Refresh the access token
        token_data = keycloak_service.refresh_token(refresh_request.refresh_token)
        
        # Validate and decode the new access token
        user_info = keycloak_service.validate_token(token_data["access_token"])
        
        # Sync user with local database
        user = keycloak_service.sync_user_with_keycloak(user_info)
        
        return TokenResponse(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token", refresh_request.refresh_token),
            token_type="bearer",
            expires_in=token_data.get("expires_in", 3600),
            user_id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post("/oauth/logout")
async def logout_user(
    current_user = Depends(get_current_user_from_keycloak)
) -> Dict[str, str]:
    """
    Logout user from Keycloak session.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Logout confirmation message
        
    Raises:
        HTTPException: If logout fails
    """
    try:
        keycloak_service = KeycloakService()
        logout_url = keycloak_service.get_logout_url()
        
        return {
            "message": "Logout successful",
            "logout_url": logout_url
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )


@router.get("/user/info")
async def get_user_info(
    current_user = Depends(get_current_user_from_keycloak)
) -> Dict[str, Any]:
    """
    Get current user information from Keycloak token.
    
    Args:
        current_user: Current authenticated user from Keycloak token
        
    Returns:
        User information from token claims
    """
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }


@router.get("/auth/callback", response_class=HTMLResponse)
async def oauth_callback(
    code: str = Query(..., description="Authorization code from Keycloak"),
    state: str = Query(..., description="State parameter for CSRF protection")
):
    """
    OAuth callback endpoint for testing purposes.
    
    This endpoint receives the authorization code from Keycloak and displays it
    for testing. In a real application, this would be handled by the frontend.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OAuth Callback - Testing</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .success {{ color: #28a745; }}
            .code {{ background: #f8f9fa; padding: 15px; border-radius: 4px; font-family: monospace; word-break: break-all; }}
            .copy-btn {{ background: #007bff; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }}
            .copy-btn:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="success">✅ OAuth Login Successful!</h1>
            <p>You have successfully authenticated with Keycloak. Here are the OAuth parameters:</p>
            
            <h3>Authorization Code:</h3>
            <div class="code" id="auth-code">{code}</div>
            <button class="copy-btn" onclick="copyToClipboard('auth-code')">Copy Code</button>
            
            <h3>State:</h3>
            <div class="code" id="state">{state}</div>
            <button class="copy-btn" onclick="copyToClipboard('state')">Copy State</button>
            
            <h3>Next Steps for Testing:</h3>
            <ol>
                <li>Copy the authorization code above</li>
                <li>Use it in the token exchange endpoint:</li>
                <div class="code">
curl -X POST http://localhost:8000/api/v1/auth/keycloak/oauth/token \\
  -H "Content-Type: application/json" \\
  -d '{{
    "code": "{code}",
    "redirect_uri": "http://localhost:8000/auth/callback",
    "state": "{state}"
  }}'
                </div>
            </ol>
        </div>
        
        <script>
            function copyToClipboard(elementId) {{
                const element = document.getElementById(elementId);
                const text = element.textContent;
                navigator.clipboard.writeText(text).then(() => {{
                    alert('Copied to clipboard!');
                }});
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
