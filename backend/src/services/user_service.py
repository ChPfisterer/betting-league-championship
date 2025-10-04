"""
User service layer.

Business logic for user management including CRUD operations,
authentication, and user statistics.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from core import get_password_hash, verify_password, ValidationError, NotFoundError
from models.user import User, UserStatus
from api.schemas.user import UserCreate, UserUpdate, UserProfile


class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            db: Database session
            user_data: User creation data
            
        Returns:
            User: Created user
            
        Raises:
            ValidationError: If username or email already exists
        """
        # Check if username already exists
        existing_user = db.query(User).filter(
            User.username == user_data.username
        ).first()
        if existing_user:
            raise ValidationError(f"Username '{user_data.username}' already exists")
        
        # Check if email already exists
        existing_email = db.query(User).filter(
            User.email == user_data.email
        ).first()
        if existing_email:
            raise ValidationError(f"Email '{user_data.email}' already exists")
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            status=UserStatus.ACTIVE
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> User:
        """
        Update user information.
        
        Args:
            db: Database session
            user_id: User ID to update
            user_data: Update data
            
        Returns:
            User: Updated user
            
        Raises:
            NotFoundError: If user not found
            ValidationError: If email already exists
        """
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Check email uniqueness if email is being updated
        if user_data.email and user_data.email != user.email:
            existing_email = db.query(User).filter(
                and_(User.email == user_data.email, User.id != user_id)
            ).first()
            if existing_email:
                raise ValidationError(f"Email '{user_data.email}' already exists")
        
        # Update fields
        if user_data.email is not None:
            user.email = user_data.email
        if user_data.first_name is not None:
            user.first_name = user_data.first_name
        if user_data.last_name is not None:
            user.last_name = user_data.last_name
        
        user.touch()  # Update timestamp
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def update_user_password(
        db: Session, 
        user_id: UUID, 
        current_password: str, 
        new_password: str
    ) -> None:
        """
        Update user password.
        
        Args:
            db: Database session
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Raises:
            NotFoundError: If user not found
            ValidationError: If current password is incorrect
        """
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise ValidationError("Current password is incorrect")
        
        # Update password
        user.password_hash = get_password_hash(new_password)
        user.touch()
        
        db.commit()
    
    @staticmethod
    def update_user_status(db: Session, user_id: UUID, status: UserStatus) -> User:
        """
        Update user status.
        
        Args:
            db: Database session
            user_id: User ID
            status: New status
            
        Returns:
            User: Updated user
            
        Raises:
            NotFoundError: If user not found
        """
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        user.status = status
        user.touch()
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> None:
        """
        Delete user.
        
        Args:
            db: Database session
            user_id: User ID to delete
            
        Raises:
            NotFoundError: If user not found
        """
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Soft delete by setting status to DELETED
        user.status = UserStatus.DELETED
        user.touch()
        
        db.commit()
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password.
        
        Args:
            db: Database session
            username: Username or email
            password: Password
            
        Returns:
            Optional[User]: User if authentication successful
        """
        # Try to find user by username or email
        user = db.query(User).filter(
            or_(User.username == username, User.email == username)
        ).first()
        
        if not user or user.status != UserStatus.ACTIVE:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        # Update last login
        user.update_last_login()
        db.commit()
        
        return user
    
    @staticmethod
    def get_user_profile(user: User) -> UserProfile:
        """
        Get user profile with statistics.
        
        Args:
            user: User object
            
        Returns:
            UserProfile: User profile with stats
        """
        # Calculate user statistics
        total_bets = user.get_total_bets()
        total_winnings = user.get_total_winnings()
        win_rate = user.calculate_win_rate()
        
        return UserProfile(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=user.last_login_at,
            total_bets=total_bets,
            total_winnings=total_winnings,
            win_rate=win_rate
        )
    
    @staticmethod
    def build_user_list_query(
        db: Session,
        status_filter: Optional[UserStatus] = None,
        search: Optional[str] = None
    ):
        """
        Build query for user list with filters.
        
        Args:
            db: Database session
            status_filter: Filter by user status
            search: Search term
            
        Returns:
            Query: SQLAlchemy query
        """
        query = db.query(User)
        
        # Filter by status
        if status_filter:
            query = query.filter(User.status == status_filter)
        
        # Search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_term),
                    User.email.ilike(search_term),
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term)
                )
            )
        
        return query.order_by(User.username)
    
    @staticmethod
    def is_admin(user: User) -> bool:
        """
        Check if user has admin privileges.
        
        Args:
            user: User to check
            
        Returns:
            bool: True if user is admin
        """
        # For now, check if user has admin role
        # This could be extended with a proper role system
        return user.username == "admin" or user.email.endswith("@admin.com")