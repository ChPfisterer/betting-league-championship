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
from datetime import datetime, timezone

from jose import jwt, JWTError
from jose.backends import RSAKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User


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
        # Use localhost for both client and server communication in development
        self.server_url = os.getenv("KEYCLOAK_URL", "http://localhost:8090")
        # Use KEYCLOAK_URL as fallback for internal communication (Docker service-to-service)
        self.internal_server_url = os.getenv("KEYCLOAK_INTERNAL_URL", self.server_url)
        self.realm_name = os.getenv("KEYCLOAK_REALM", "betting-platform")
        # Backend should validate tokens intended for the API, not the frontend client
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
            
            logger.info(f"Token key ID: {kid}")
            logger.info(f"Available key IDs: {[key.get('kid') for key in certs.get('keys', [])]}")
            
            # Find the matching public key
            public_key = None
            for key in certs["keys"]:
                if key["kid"] == kid:
                    # Create RSA public key from JWK
                    try:
                        from jose.backends.cryptography_backend import CryptographyRSAKey
                        rsa_key = CryptographyRSAKey(key, algorithm="RS256")
                        # Use the CryptographyRSAKey directly - it has the methods we need
                        public_key = rsa_key
                        logger.info("Successfully created public key using CryptographyRSAKey")
                    except (ImportError, AttributeError) as e:
                        logger.warning(f"CryptographyRSAKey approach failed: {e}, using manual construction")
                        # Fallback to manual key construction
                        import base64
                        from cryptography.hazmat.primitives.asymmetric import rsa
                        from cryptography.hazmat.primitives import serialization
                        
                        # Convert JWK to RSA public key
                        n = base64.urlsafe_b64decode(key["n"] + "==")
                        e = base64.urlsafe_b64decode(key["e"] + "==")
                        
                        # Convert bytes to integers
                        n_int = int.from_bytes(n, 'big')
                        e_int = int.from_bytes(e, 'big')
                        
                        # Create RSA public key
                        public_key = rsa.RSAPublicNumbers(e_int, n_int).public_key()
                        logger.info("Successfully created public key using manual construction")
                    break
            
            if not public_key:
                # Try using the first available key if kid doesn't match
                if certs.get("keys"):
                    logger.warning(f"Key ID {kid} not found, trying first available key")
                    key = certs["keys"][0]
                    try:
                        from jose.backends.cryptography_backend import CryptographyRSAKey
                        rsa_key = CryptographyRSAKey(key, algorithm="RS256")
                        public_key = rsa_key
                        logger.info("Successfully created public key using first available key")
                    except Exception as e:
                        logger.error(f"Failed to create key from first available: {e}")
                
            if not public_key:
                raise ValueError("Public key not found for token")
            
            # First, decode token without validation to see the issuer and audience
            unverified_token = jwt.get_unverified_claims(access_token)
            actual_issuer = unverified_token.get("iss")
            actual_audience = unverified_token.get("aud")
            logger.info(f"Token issuer: {actual_issuer}")
            logger.info(f"Token audience: {actual_audience}")
            logger.info(f"Token subject: {unverified_token.get('sub')}")
            logger.info(f"Token client_id: {unverified_token.get('azp')} or {unverified_token.get('client_id')}")
            
            # Expected issuers (try both internal and external URLs)
            expected_issuers = [
                f"{self.internal_server_url}/realms/{self.realm_name}",
                f"{self.server_url}/realms/{self.realm_name}",
                f"http://localhost:8090/realms/{self.realm_name}",
                f"http://localhost:8080/realms/{self.realm_name}"
            ]
            logger.info(f"Expected issuers: {expected_issuers}")
            
            # Try validation with different issuers and audiences
            # Accept tokens from frontend client, API client, and default account audience
            valid_audiences = [
                "betting-frontend",  # Frontend SPA client (token originator)
                "betting-api",       # Backend API client (preferred audience)
                "account",           # Default Keycloak audience
                self.client_id       # Current client_id (flexible)
            ]
            token_info = None
            
            for expected_issuer in expected_issuers:
                for audience in valid_audiences:
                    try:
                        token_info = jwt.decode(
                            access_token,
                            public_key,
                            algorithms=["RS256"],
                            audience=audience,
                            issuer=expected_issuer
                        )
                        logger.info(f"Token validation successful with issuer: {expected_issuer} and audience: {audience}")
                        break
                    except JWTError as e:
                        logger.debug(f"Token validation failed with issuer {expected_issuer} and audience {audience}: {e}")
                        continue
                if token_info:
                    break
            
            if not token_info:
                # If all issuer validations fail, try without issuer validation but with different audiences
                logger.warning("All issuer validations failed, trying without issuer validation")
                for audience in valid_audiences:
                    try:
                        token_info = jwt.decode(
                            access_token,
                            public_key,
                            algorithms=["RS256"],
                            audience=audience
                            # No issuer validation
                        )
                        logger.info(f"Token validation successful without issuer validation, audience: {audience}")
                        break
                    except JWTError as e:
                        logger.debug(f"Token validation failed without issuer validation, audience {audience}: {e}")
                        continue
            
            if token_info:
                logger.info(f"Successfully validated token for user: {token_info.get('preferred_username')}")
                return token_info
            else:
                raise JWTError("All token validation attempts failed")
            
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
            # Fallback to preferred_username if sub is not available (Keycloak configuration issue)
            if not keycloak_user_id:
                keycloak_user_id = token_info.get("preferred_username")
                logger.warning(f"Token missing 'sub' field, using 'preferred_username' as Keycloak ID: {keycloak_user_id}")
            else:
                # Validate that sub field looks like a proper UUID (Keycloak user ID format)
                import re
                uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
                if re.match(uuid_pattern, str(keycloak_user_id), re.IGNORECASE):
                    logger.info(f"Using proper UUID from 'sub' field: {keycloak_user_id}")
                else:
                    logger.warning(f"'sub' field is not a UUID, using as-is: {keycloak_user_id}")
            
            username = token_info.get("preferred_username")
            email = token_info.get("email")
            first_name = token_info.get("given_name", "")
            last_name = token_info.get("family_name", "")
            
            # DEBUG: Log all token information for troubleshooting
            logger.info(f"=== KEYCLOAK USER SYNC DEBUG ===")
            logger.info(f"Keycloak User ID (sub): {keycloak_user_id}")
            logger.info(f"Username (preferred_username): {username}")
            logger.info(f"Email: {email}")
            logger.info(f"First Name: {first_name}")
            logger.info(f"Last Name: {last_name}")
            logger.info(f"Full token_info keys: {list(token_info.keys())}")
            logger.info(f"================================")
            
            # Skip user synchronization for service accounts
            if username and username.startswith("service-account-"):
                logger.info(f"Skipping user synchronization for service account: {username}")
                # Create a temporary user object for service accounts (not saved to database)
                
                service_user = User(
                    keycloak_id=keycloak_user_id,
                    username=username,
                    email=email or f"{username}@keycloak.service",
                    first_name="Service",
                    last_name="Account", 
                    display_name=username,
                    date_of_birth=datetime(1990, 1, 1, tzinfo=timezone.utc),
                    password_hash="service_account_no_password",
                    role="service",
                    is_active=True
                )
                # Don't add to database session - this is just for authentication context
                return service_user
            
            # Check if user has admin role
            realm_access = token_info.get("realm_access", {})
            roles = realm_access.get("roles", [])
            is_admin = "admin" in roles or "betting-admin" in roles
            
            # Get database session
            db: Session = next(get_db())
            
            try:
                # First, check if user exists by Keycloak ID (most reliable)
                user = db.query(User).filter(User.keycloak_id == keycloak_user_id).first()
                logger.info(f"DEBUG: Looking for user by Keycloak ID {keycloak_user_id}: {'FOUND' if user else 'NOT FOUND'}")
                
                if user:
                    logger.info(f"DEBUG: Found existing user by Keycloak ID - ID: {user.id}, Username: {user.username}, Email: {user.email}")
                
                if user:
                    # Update existing user with Keycloak ID - only update non-conflicting fields
                    # Don't update email if it would cause a constraint violation or if email is None
                    if email:
                        existing_email_user = db.query(User).filter(
                            User.email == email,
                            User.id != user.id
                        ).first()
                        
                        if not existing_email_user:
                            user.email = email
                        else:
                            logger.warning(f"Email {email} already exists for another user, skipping email update")
                    
                    user.first_name = first_name or user.first_name or "Unknown"
                    user.last_name = last_name or user.last_name or "User"
                    user.role = "admin" if is_admin else "user"
                    user.is_active = True
                    
                    logger.info(f"Updated existing user by Keycloak ID: {username}")
                else:
                    # Check if user exists by username (legacy user without Keycloak ID)
                    user = db.query(User).filter(User.username == username).first()
                    logger.info(f"DEBUG: Looking for user by username '{username}': {'FOUND' if user else 'NOT FOUND'}")
                    
                    if user:
                        logger.info(f"DEBUG: Found existing user by username - ID: {user.id}, Username: {user.username}, Email: {user.email}")
                        # Link existing user to Keycloak
                        user.keycloak_id = keycloak_user_id
                        
                        # Only update email if it won't cause a constraint violation and email is not None
                        if email:
                            existing_email_user = db.query(User).filter(
                                User.email == email,
                                User.id != user.id
                            ).first()
                            
                            if not existing_email_user:
                                user.email = email
                            else:
                                logger.warning(f"Email {email} already exists for another user, keeping original email {user.email}")
                        
                        user.first_name = first_name or user.first_name or "Unknown"
                        user.last_name = last_name or user.last_name or "User"
                        user.role = "admin" if is_admin else "user"
                        user.is_active = True
                        
                        logger.info(f"Linked existing user to Keycloak: {username}")
                    else:
                        # Create new user
                        logger.info(f"DEBUG: Creating NEW user for Keycloak user")
                        display_name = f"{first_name} {last_name}".strip() or username
                        
                        # Ensure email is not None - generate fallback if missing
                        user_email = email if email else f"{username}@keycloak.local"
                        
                        user = User(
                            keycloak_id=keycloak_user_id,
                            username=username,
                            email=user_email,
                            first_name=first_name or "Unknown",
                            last_name=last_name or "User",
                            display_name=display_name,
                            date_of_birth=datetime(1990, 1, 1, tzinfo=timezone.utc),  # Default date
                            role="admin" if is_admin else "user",
                            is_active=True
                        )
                        db.add(user)
                        
                        logger.info(f"DEBUG: Created new user - Username: {username}, Email: {user_email}")
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
