"""
Keycloak integration service.

This module provides integration with Keycloak for OAuth 2.0 authentication,
user management, and token validation.
"""

import os
import secrets
import logging
import requests
from typing import Dict, Any, Optional, Tuple
from urllib.parse import urlencode

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from core.security import get_password_hash


# Configure logging
logger = logging.getLogger(__name__)


class KeycloakService:
    """
    Service for Keycloak OAuth 2.0 integration.
    
    Handles authentication, token validation, user synchronization,
    and OAuth flow management with Keycloak server.
    """
    
    def __init__(self):
        """Initialize Keycloak service with configuration."""
        # Use external URL for client-side redirects
        self.server_url = os.getenv("KEYCLOAK_URL", "http://localhost:8090")
        # Use internal URL for server-side communication
        self.internal_server_url = os.getenv("KEYCLOAK_INTERNAL_URL", "http://keycloak:8080")
        self.realm_name = os.getenv("KEYCLOAK_REALM", "betting-platform")
        self.client_id = os.getenv("KEYCLOAK_CLIENT_ID", "betting-api")
        self.client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")
        
        # Store configuration without initializing problematic client
        self.keycloak_openid = None
        
        logger.info(f"Keycloak service initialized for realm: {self.realm_name}")
    
    def get_authorization_url(self, redirect_uri: str) -> Tuple[str, str]:
        """
        Generate OAuth 2.0 authorization URL for user login.
        
        Args:
            redirect_uri: URI to redirect after authentication
            
        Returns:
            Tuple of (authorization_url, state) for OAuth flow
            
        Raises:
            KeycloakError: If URL generation fails
        """
        try:
            # Generate random state for CSRF protection
            state = secrets.token_urlsafe(32)
            
            # Use external URL for client-side redirects
            external_url = os.getenv("KEYCLOAK_EXTERNAL_URL", "http://localhost:8090")
            
            # Build authorization URL manually to avoid client issues
            auth_params = {
                "client_id": self.client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": "openid profile email",
                "state": state
            }
            
            auth_url = f"{external_url}/realms/{self.realm_name}/protocol/openid-connect/auth?" + urlencode(auth_params)
            
            logger.info(f"Generated authorization URL for redirect_uri: {redirect_uri}")
            return auth_url, state
            
        except Exception as e:
            logger.error(f"Failed to generate authorization URL: {e}")
            raise ValueError(f"Authorization URL generation failed: {e}")
    
    def exchange_authorization_code(
        self, 
        code: str, 
        redirect_uri: str, 
        state: str
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access and refresh tokens.
        
        Args:
            code: Authorization code from OAuth callback
            redirect_uri: Original redirect URI
            state: State parameter for CSRF verification
            
        Returns:
            Token data including access_token, refresh_token, etc.
            
        Raises:
            ValueError: If code exchange fails or state is invalid
        """
        try:
            # Use internal URL for server-to-server communication
            token_url = f"{self.internal_server_url}/realms/{self.realm_name}/protocol/openid-connect/token"
            
            # Prepare token exchange request
            token_data = {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "code": code,
                "redirect_uri": redirect_uri
            }
            
            # Add client secret if available
            if self.client_secret:
                token_data["client_secret"] = self.client_secret
            
            # Make token exchange request
            response = requests.post(
                token_url,
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Token exchange failed with status {response.status_code}: {response.text}")
                raise ValueError(f"Token exchange failed: {response.text}")
            
            token_response = response.json()
            logger.info("Successfully exchanged authorization code for tokens")
            return token_response
            
        except requests.RequestException as e:
            logger.error(f"Keycloak token exchange failed: {e}")
            raise ValueError(f"Invalid authorization code: {e}")
        except Exception as e:
            logger.error(f"Token exchange error: {e}")
            raise ValueError(f"Token exchange failed: {e}")
    
    def validate_token(self, access_token: str) -> Dict[str, Any]:
        """
        Validate and decode access token.
        
        Args:
            access_token: JWT access token to validate
            
        Returns:
            Decoded token claims/user information
            
        Raises:
            ValueError: If token is invalid or expired
        """
        try:
            # Get public key from Keycloak
            certs_url = f"{self.internal_server_url}/realms/{self.realm_name}/protocol/openid-connect/certs"
            certs_response = requests.get(certs_url, timeout=10)
            certs_response.raise_for_status()
            certs = certs_response.json()
            
            # Decode token header to get key ID
            unverified_header = jwt.get_unverified_header(access_token)
            kid = unverified_header.get("kid")
            
            # Find the matching public key
            public_key = None
            for key in certs["keys"]:
                if key["kid"] == kid:
                    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                    break
            
            if not public_key:
                raise ValueError("Public key not found for token")
            
            # Decode and validate token
            token_info = jwt.decode(
                access_token,
                public_key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=f"{self.internal_server_url}/realms/{self.realm_name}"
            )
            
            logger.info(f"Successfully validated token for user: {token_info.get('preferred_username')}")
            return token_info
            
        except JWTError as e:
            logger.error(f"JWT validation failed: {e}")
            raise ValueError(f"Invalid token: {e}")
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            raise ValueError(f"Token validation failed: {e}")
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            New token data with refreshed access token
            
        Raises:
            ValueError: If refresh token is invalid
        """
        try:
            # Use internal URL for server-to-server communication
            token_url = f"{self.internal_server_url}/realms/{self.realm_name}/protocol/openid-connect/token"
            
            # Prepare refresh token request
            token_data = {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "refresh_token": refresh_token
            }
            
            # Add client secret if available
            if self.client_secret:
                token_data["client_secret"] = self.client_secret
            
            # Make refresh token request
            response = requests.post(
                token_url,
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Token refresh failed with status {response.status_code}: {response.text}")
                raise ValueError(f"Invalid refresh token: {response.text}")
            
            token_response = response.json()
            logger.info("Successfully refreshed access token")
            return token_response
            
        except requests.RequestException as e:
            logger.error(f"Token refresh failed: {e}")
            raise ValueError(f"Invalid refresh token: {e}")
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            raise ValueError(f"Token refresh failed: {e}")
    
    def get_logout_url(self, redirect_uri: Optional[str] = None) -> str:
        """
        Get Keycloak logout URL.
        
        Args:
            redirect_uri: Optional URI to redirect after logout
            
        Returns:
            Logout URL
        """
        # Use external URL for client-side redirects
        external_url = os.getenv("KEYCLOAK_EXTERNAL_URL", "http://localhost:8090")
        logout_url = f"{external_url}/realms/{self.realm_name}/protocol/openid-connect/logout"
        
        if redirect_uri:
            logout_url += f"?redirect_uri={redirect_uri}"
        
        return logout_url
    
    def sync_user_with_keycloak(self, token_info: Dict[str, Any]) -> User:
        """
        Synchronize user data between Keycloak and local database.
        
        Args:
            token_info: Decoded token with user claims
            
        Returns:
            Local User object (created or updated)
            
        Raises:
            Exception: If user synchronization fails
        """
        try:
            # Extract user information from token
            keycloak_user_id = token_info.get("sub")
            username = token_info.get("preferred_username")
            email = token_info.get("email")
            first_name = token_info.get("given_name", "")
            last_name = token_info.get("family_name", "")
            
            # Check if user has admin role
            realm_access = token_info.get("realm_access", {})
            roles = realm_access.get("roles", [])
            is_admin = "admin" in roles or "betting-admin" in roles
            
            # Get database session
            db: Session = next(get_db())
            
            try:
                # Check if user exists (by Keycloak ID or username)
                user = db.query(User).filter(
                    (User.keycloak_id == keycloak_user_id) | 
                    (User.username == username)
                ).first()
                
                if user:
                    # Update existing user
                    user.keycloak_id = keycloak_user_id
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.is_admin = is_admin
                    user.is_active = True
                    
                    logger.info(f"Updated existing user: {username}")
                else:
                    # Create new user
                    user = User(
                        keycloak_id=keycloak_user_id,
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        hashed_password=get_password_hash(secrets.token_urlsafe(32)),
                        is_admin=is_admin,
                        is_active=True
                    )
                    db.add(user)
                    
                    logger.info(f"Created new user: {username}")
                
                db.commit()
                db.refresh(user)
                
                return user
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"User synchronization failed: {e}")
            raise Exception(f"Failed to sync user: {e}")


# Dependency function for FastAPI
def get_keycloak_service() -> KeycloakService:
    """
    Dependency function to get Keycloak service instance.
    
    Returns:
        KeycloakService instance
    """
    return KeycloakService()


# Make it available for import
KeycloakService.__call__ = get_keycloak_service
