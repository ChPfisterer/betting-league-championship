"""
User model for the betting league championship application.

This module defines the User model with comprehensive field validation,
authentication support, and business logic as specified by the TDD tests
in backend/tests/models/test_user_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, 
    CheckConstraint, Index, event
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone, timedelta
from typing import Union
from typing import Optional, Dict, Any, List
import uuid
import re
import bcrypt
from enum import Enum

from .base import Base


class UserStatus(Enum):
    """User account status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"
    BANNED = "banned"


class UserRole(Enum):
    """User role enumeration."""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class KYCStatus(Enum):
    """KYC verification status enumeration."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    VERIFIED = "verified"
    REJECTED = "rejected"


class User(Base):
    """
    User model representing user accounts in the system.
    
    This model handles user authentication, profile information,
    account status, and relationships with other entities.
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Unique user identifier"
    )
    
    # Authentication fields
    username = Column(
        String(50), 
        unique=True, 
        nullable=False,
        comment="Unique username for login"
    )
    email = Column(
        String(255), 
        unique=True, 
        nullable=False,
        comment="User email address"
    )
    password_hash = Column(
        String(255), 
        nullable=False,
        comment="Hashed password for authentication"
    )
    
    # Profile fields
    first_name = Column(
        String(100), 
        nullable=False,
        comment="User's first name"
    )
    last_name = Column(
        String(100), 
        nullable=False,
        comment="User's last name"
    )
    display_name = Column(
        String(100),
        nullable=False,
        comment="User's display name (computed or custom)"
    )
    date_of_birth = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="User's date of birth for age verification"
    )
    phone_number = Column(
        String(20),
        comment="User's phone number"
    )
    
    # Account status and metadata
    status = Column(
        String(20),
        nullable=False,
        default=UserStatus.PENDING.value,
        comment="Current account status"
    )
    role = Column(
        String(20),
        nullable=False,
        default=UserRole.USER.value,
        comment="User role and permissions level"
    )
    
    # Status fields for compatibility with tests
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether user account is active"
    )
    is_verified = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether user account is verified"
    )
    
    # Verification and compliance
    email_verified = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether email address has been verified"
    )
    phone_verified = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether phone number has been verified"
    )
    kyc_status = Column(
        String(20),
        nullable=False,
        default=KYCStatus.NOT_STARTED.value,
        comment="Know Your Customer verification status"
    )
    kyc_verified_at = Column(
        DateTime(timezone=True),
        comment="When KYC verification was completed"
    )
    
    # Security and authentication
    last_login = Column(
        DateTime(timezone=True),
        comment="Last successful login timestamp"
    )
    last_login_ip = Column(
        String(45),
        comment="IP address of last login"
    )
    failed_login_attempts = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of consecutive failed login attempts"
    )
    locked_until = Column(
        DateTime(timezone=True),
        comment="Account locked until this timestamp"
    )
    password_changed_at = Column(
        DateTime(timezone=True),
        comment="When password was last changed"
    )
    
    # Preferences and settings
    language = Column(
        String(10),
        nullable=False,
        default='en',
        comment="User's preferred language"
    )
    timezone = Column(
        String(50),
        nullable=False,
        default='UTC',
        comment="User's timezone preference"
    )
    currency = Column(
        String(3),
        nullable=False,
        default='GBP',
        comment="User's preferred currency"
    )
    notifications_enabled = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether to send notifications to user"
    )
    
    # Additional profile data
    biography = Column(
        Text,
        comment="User's biography or description"
    )
    avatar_url = Column(
        String(500),
        comment="URL to user's profile picture"
    )
    website_url = Column(
        String(500),
        comment="User's personal website URL"
    )
    
    # Compliance and legal
    terms_accepted = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether user has accepted terms of service"
    )
    terms_accepted_at = Column(
        DateTime(timezone=True),
        comment="When terms were accepted"
    )
    privacy_policy_accepted = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether user has accepted privacy policy"
    )
    marketing_consent = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether user consents to marketing communications"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the user account was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the user account was last updated"
    )
    deleted_at = Column(
        DateTime(timezone=True),
        comment="When the user account was deleted (soft delete)"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'active', 'suspended', 'deactivated', 'banned')",
            name="ck_users_status"
        ),
        CheckConstraint(
            "role IN ('user', 'moderator', 'admin', 'super_admin')",
            name="ck_users_role"
        ),
        CheckConstraint(
            "kyc_status IN ('not_started', 'in_progress', 'pending_review', 'verified', 'rejected')",
            name="ck_users_kyc_status"
        ),
        CheckConstraint(
            "failed_login_attempts >= 0",
            name="ck_users_failed_login_attempts"
        ),
        CheckConstraint(
            "date_of_birth < current_timestamp",
            name="ck_users_date_of_birth_past"
        ),
        CheckConstraint(
            "length(username) >= 3",
            name="ck_users_username_length"
        ),
        CheckConstraint(
            "length(first_name) >= 1",
            name="ck_users_first_name_length"
        ),
        CheckConstraint(
            "length(last_name) >= 1",
            name="ck_users_last_name_length"
        ),
        # Indexes for performance
        Index('ix_users_email', 'email'),
        Index('ix_users_username', 'username'),
        Index('ix_users_status', 'status'),
        Index('ix_users_kyc_status', 'kyc_status'),
        Index('ix_users_created_at', 'created_at'),
        Index('ix_users_last_login', 'last_login'),
    )
    
    def __init__(self, **kwargs):
        """Initialize User with proper defaults for TDD testing."""
        # Set default values for testing if not provided
        if 'is_active' not in kwargs:
            kwargs['is_active'] = True
            
        if 'is_verified' not in kwargs:
            kwargs['is_verified'] = False
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.now(timezone.utc)
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        super().__init__(**kwargs)
    
    # Validation methods
    @validates('email')
    def validate_email(self, key: str, email: str) -> str:
        """Validate email format."""
        if not email:
            raise ValueError("Email is required")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        return email.lower().strip()
    
    @validates('username')
    def validate_username(self, key: str, username: str) -> str:
        """Validate username format and requirements."""
        if not username:
            raise ValueError("Username is required")
        
        username = username.strip()
        
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        if len(username) > 50:
            raise ValueError("Username must be no more than 50 characters long")
        
        # Only alphanumeric characters, underscores, and hyphens
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")
        
        return username.lower()
    
    @validates('phone_number')
    def validate_phone_number(self, key: str, phone_number: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        if not phone_number:
            return None
        
        phone_number = phone_number.strip()
        
        # Basic phone number validation (international format)
        phone_pattern = r'^\+?[1-9]\d{6,14}$'
        if not re.match(phone_pattern, phone_number):
            raise ValueError("Invalid phone number format")
        
        return phone_number
    
    @validates('date_of_birth')
    def validate_date_of_birth(self, key: str, date_of_birth: Union[str, datetime]) -> datetime:
        """Validate date of birth requirements."""
        if not date_of_birth:
            raise ValueError("Date of birth is required")
        
        # Convert string to datetime if needed
        if isinstance(date_of_birth, str):
            try:
                # Try parsing different date formats
                if 'T' in date_of_birth:
                    # ISO format with time
                    date_of_birth = datetime.fromisoformat(date_of_birth.replace('Z', '+00:00'))
                else:
                    # Date only format
                    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
                    # Make it timezone aware
                    date_of_birth = date_of_birth.replace(tzinfo=timezone.utc)
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD or ISO format")
        
        # Ensure timezone awareness
        if date_of_birth.tzinfo is None:
            date_of_birth = date_of_birth.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        
        # Must be in the past
        if date_of_birth >= now:
            raise ValueError("Date of birth must be in the past")
        
        # Must be at least 18 years old
        age = (now - date_of_birth).days / 365.25
        if age < 18:
            raise ValueError("User must be at least 18 years old")
        
        # Must be reasonable (not more than 120 years old)
        if age > 120:
            raise ValueError("Date of birth is not valid")
        
        return date_of_birth
    
    # Properties
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        """Calculate user's age in years."""
        now = datetime.now(timezone.utc)
        return int((now - self.date_of_birth).days / 365.25)
    
    @property
    def is_locked(self) -> bool:
        """Check if user account is currently locked."""
        if not self.locked_until:
            return False
        return datetime.now(timezone.utc) < self.locked_until
    
    @property
    def can_login(self) -> bool:
        """Check if user can currently log in."""
        return (
            self.is_active and 
            not self.is_locked and 
            self.email_verified
        )
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.role in [UserRole.ADMIN.value, UserRole.SUPER_ADMIN.value]
    
    @property
    def is_moderator(self) -> bool:
        """Check if user has moderator privileges."""
        return self.role in [
            UserRole.MODERATOR.value, 
            UserRole.ADMIN.value, 
            UserRole.SUPER_ADMIN.value
        ]
    
    # Alias properties for test compatibility
    @property
    def bio(self) -> Optional[str]:
        """Alias for biography field."""
        return self.biography
        
    @bio.setter
    def bio(self, value: Optional[str]) -> None:
        """Setter for bio alias."""
        self.biography = value
    
    @property
    def last_login_at(self) -> Optional[datetime]:
        """Alias for last_login field."""
        return self.last_login
        
    @last_login_at.setter
    def last_login_at(self, value: Optional[datetime]) -> None:
        """Setter for last_login_at alias."""
        self.last_login = value
    
    # Authentication methods
    def set_password(self, password: str) -> None:
        """Set user password with proper hashing."""
        if not password:
            raise ValueError("Password is required")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Hash password with bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        self.password_changed_at = datetime.now(timezone.utc)
    
    def check_password(self, password: str) -> bool:
        """Verify password against stored hash."""
        if not password or not self.password_hash:
            return False
        
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )
    
    def record_login(self, ip_address: Optional[str] = None) -> None:
        """Record successful login."""
        self.last_login = datetime.now(timezone.utc)
        self.last_login_ip = ip_address
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def record_failed_login(self) -> None:
        """Record failed login attempt and potentially lock account."""
        self.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts for 30 minutes
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    # Account management methods
    def activate(self) -> None:
        """Activate user account."""
        if self.status == UserStatus.PENDING.value:
            self.status = UserStatus.ACTIVE.value
        else:
            raise ValueError(f"Cannot activate user with status: {self.status}")
    
    def suspend(self, reason: Optional[str] = None) -> None:
        """Suspend user account."""
        if self.status == UserStatus.ACTIVE.value:
            self.status = UserStatus.SUSPENDED.value
        else:
            raise ValueError(f"Cannot suspend user with status: {self.status}")
    
    def deactivate(self) -> None:
        """Deactivate user account."""
        self.status = UserStatus.DEACTIVATED.value
    
    def ban(self, reason: Optional[str] = None) -> None:
        """Ban user account permanently."""
        self.status = UserStatus.BANNED.value
    
    def verify_email(self) -> None:
        """Mark email as verified."""
        self.email_verified = True
    
    def verify_phone(self) -> None:
        """Mark phone as verified."""
        self.phone_verified = True
    
    def complete_kyc(self) -> None:
        """Mark KYC verification as complete."""
        self.kyc_status = KYCStatus.VERIFIED.value
        self.kyc_verified_at = datetime.now(timezone.utc)
    
    def accept_terms(self) -> None:
        """Record terms of service acceptance."""
        self.terms_accepted = True
        self.terms_accepted_at = datetime.now(timezone.utc)
    
    # Utility methods
    def to_dict(self, include_sensitive: bool = False, include_relationships: bool = False) -> Dict[str, Any]:
        """
        Convert user to dictionary representation.
        
        Args:
            include_sensitive: Whether to include sensitive fields like password_hash
            include_relationships: Whether to include related objects
        
        Returns:
            Dictionary representation of the user
        """
        result = super().to_dict(include_relationships)
        
        # Add computed properties
        result.update({
            'full_name': self.full_name,
            'age': self.age,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'is_locked': self.is_locked,
            'can_login': self.can_login,
            'is_admin': self.is_admin,
            'is_moderator': self.is_moderator,
        })
        
        # Remove sensitive data unless explicitly requested
        if not include_sensitive:
            result.pop('password_hash', None)
            result.pop('last_login_ip', None)
            result.pop('failed_login_attempts', None)
        
        return result
    
    # Relationships
    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        """String representation of user."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# Event listeners for automatic timestamp updates
@event.listens_for(User, 'before_update')
def update_timestamp(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)