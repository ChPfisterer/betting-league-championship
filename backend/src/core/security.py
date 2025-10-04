"""
Core security and authentication utilities.

This module provides security utilities, authentication helpers,
and OAuth integration for the betting platform API.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()


class SecurityError(Exception):
    """Custom security exception."""
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Token payload data
        expires_delta: Token expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm="HS256"
    )
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Dict[str, Any]: Token payload
        
    Raises:
        SecurityError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=["HS256"]
        )
        return payload
    except JWTError as e:
        raise SecurityError(f"Invalid token: {str(e)}")


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    """
    Extract current user ID from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        UUID: Current user ID
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return UUID(user_id)
    except (SecurityError, ValueError):
        raise credentials_exception


async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user from database.
    
    Args:
        user_id: Current user ID from token
        db: Database session
        
    Returns:
        User: Current user object
        
    Raises:
        HTTPException: If user not found
    """
    # Import here to avoid circular imports
    import sys
    if '/Users/chp/repos/GitHub/betting-league-championship/backend/src' not in sys.path:
        sys.path.append('/Users/chp/repos/GitHub/betting-league-championship/backend/src')
    
    from models.user import User
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# Optional authentication dependency
OptionalAuth = Depends(get_current_user_id)
RequiredAuth = Depends(get_current_user)