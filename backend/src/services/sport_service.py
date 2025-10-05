"""
Sport Service

This service handles business logic for sport operations including creation,
updates, activation/deactivation, statistics calculation, and comprehensive
data validation for the betting platform.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from models import Sport, Team, Competition
from core import http_not_found, http_conflict
from api.schemas.sport import SportCreate, SportUpdate

from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session

from core import ValidationError, NotFoundError
from models.sport import Sport
from api.schemas.sport import SportCreate, SportUpdate, SportWithStats


class SportService:
    """Service class for sport operations."""
    
    @staticmethod
    def create_sport(db: Session, sport_data: SportCreate) -> Sport:
        """
        Create a new sport.
        
        Args:
            db: Database session
            sport_data: Sport creation data
            
        Returns:
            Sport: Created sport
            
        Raises:
            ValidationError: If sport name already exists
        """
        # Check if sport name already exists
        existing_sport = db.query(Sport).filter(
            Sport.name == sport_data.name
        ).first()
        if existing_sport:
            raise ValidationError(f"Sport name '{sport_data.name}' already exists")
        
        # Create new sport
        sport = Sport(
            name=sport_data.name,
            description=sport_data.description,
            rules=sport_data.rules,
            is_active=sport_data.is_active
        )
        
        db.add(sport)
        db.commit()
        db.refresh(sport)
        
        return sport
    
    @staticmethod
    def get_sport_by_id(db: Session, sport_id: UUID) -> Optional[Sport]:
        """Get sport by ID."""
        return db.query(Sport).filter(Sport.id == sport_id).first()
    
    @staticmethod
    def get_sport_by_name(db: Session, name: str) -> Optional[Sport]:
        """Get sport by name."""
        return db.query(Sport).filter(Sport.name == name).first()
    
    @staticmethod
    def update_sport(
        db: Session, 
        sport_id: UUID, 
        sport_data: SportUpdate
    ) -> Sport:
        """
        Update sport information.
        
        Args:
            db: Database session
            sport_id: Sport ID to update
            sport_data: Update data
            
        Returns:
            Sport: Updated sport
            
        Raises:
            NotFoundError: If sport not found
            ValidationError: If name already exists
        """
        sport = SportService.get_sport_by_id(db, sport_id)
        if not sport:
            raise NotFoundError(f"Sport with ID {sport_id} not found")
        
        # Check name uniqueness if name is being updated
        if sport_data.name and sport_data.name != sport.name:
            existing_sport = db.query(Sport).filter(
                and_(Sport.name == sport_data.name, Sport.id != sport_id)
            ).first()
            if existing_sport:
                raise ValidationError(f"Sport name '{sport_data.name}' already exists")
        
        # Update fields
        if sport_data.name is not None:
            sport.name = sport_data.name
        if sport_data.description is not None:
            sport.description = sport_data.description
        if sport_data.rules is not None:
            sport.rules = sport_data.rules
        if sport_data.is_active is not None:
            sport.is_active = sport_data.is_active
        
        sport.touch()  # Update timestamp
        
        db.commit()
        db.refresh(sport)
        
        return sport
    
    @staticmethod
    def delete_sport(db: Session, sport_id: UUID) -> None:
        """
        Delete sport.
        
        Args:
            db: Database session
            sport_id: Sport ID to delete
            
        Raises:
            NotFoundError: If sport not found
        """
        sport = SportService.get_sport_by_id(db, sport_id)
        if not sport:
            raise NotFoundError(f"Sport with ID {sport_id} not found")
        
        # Soft delete by setting is_active to False
        sport.is_active = False
        sport.touch()
        
        db.commit()
    
    @staticmethod
    def get_sport_with_stats(db: Session, sport_id: UUID) -> Optional[SportWithStats]:
        """
        Get sport with statistics.
        
        Args:
            db: Database session
            sport_id: Sport ID
            
        Returns:
            Optional[SportWithStats]: Sport with stats or None
        """
        sport = SportService.get_sport_by_id(db, sport_id)
        if not sport:
            return None
        
        # Calculate statistics
        stats = SportService.calculate_sport_stats(db, sport_id)
        
        return SportWithStats(
            id=sport.id,
            name=sport.name,
            description=sport.description,
            rules=sport.rules,
            is_active=sport.is_active,
            created_at=sport.created_at,
            updated_at=sport.updated_at,
            total_teams=stats["total_teams"],
            total_competitions=stats["total_competitions"],
            total_matches=stats["total_matches"],
            active_competitions=stats["active_competitions"]
        )
    
    @staticmethod
    def calculate_sport_stats(db: Session, sport_id: UUID) -> dict:
        """
        Calculate sport statistics.
        
        Args:
            db: Database session
            sport_id: Sport ID
            
        Returns:
            dict: Sport statistics
        """
        # Import here to avoid circular imports
        from models.team import Team
        
        # Team count
        total_teams = db.query(func.count(Team.id)).filter(
            and_(Team.sport_id == sport_id, Team.is_active == True)
        ).scalar() or 0
        
        # For now, return basic stats (competition and match stats would require model integration)
        return {
            "total_teams": total_teams,
            "total_competitions": 0,  # TODO: Calculate from Competition model
            "total_matches": 0,  # TODO: Calculate from Match model
            "active_competitions": 0  # TODO: Calculate from Competition model
        }
    
    @staticmethod
    def build_sport_list_query(
        db: Session,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ):
        """
        Build query for sport list with filters.
        
        Args:
            db: Database session
            is_active: Filter by active status
            search: Search term
            
        Returns:
            Query: SQLAlchemy query
        """
        query = db.query(Sport)
        
        # Filter by active status
        if is_active is not None:
            query = query.filter(Sport.is_active == is_active)
        
        # Search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Sport.name.ilike(search_term),
                    Sport.description.ilike(search_term)
                )
            )
        
        return query.order_by(Sport.name)
    
    @staticmethod
    def get_active_sports(db: Session) -> List[Sport]:
        """
        Get all active sports.
        
        Args:
            db: Database session
            
        Returns:
            List[Sport]: List of active sports
        """
        return db.query(Sport).filter(Sport.is_active == True).order_by(Sport.name).all()
    
    @staticmethod
    def activate_sport(db: Session, sport_id: UUID) -> Sport:
        """
        Activate a sport.
        
        Args:
            db: Database session
            sport_id: Sport ID to activate
            
        Returns:
            Sport: Activated sport
            
        Raises:
            NotFoundError: If sport not found
        """
        sport = SportService.get_sport_by_id(db, sport_id)
        if not sport:
            raise NotFoundError(f"Sport with ID {sport_id} not found")
        
        sport.is_active = True
        sport.touch()
        
        db.commit()
        db.refresh(sport)
        
        return sport
    
    @staticmethod
    def deactivate_sport(db: Session, sport_id: UUID) -> Sport:
        """
        Deactivate a sport.
        
        Args:
            db: Database session
            sport_id: Sport ID to deactivate
            
        Returns:
            Sport: Deactivated sport
            
        Raises:
            NotFoundError: If sport not found
        """
        sport = SportService.get_sport_by_id(db, sport_id)
        if not sport:
            raise NotFoundError(f"Sport with ID {sport_id} not found")
        
        sport.is_active = False
        sport.touch()
        
        db.commit()
        db.refresh(sport)
        
        return sport