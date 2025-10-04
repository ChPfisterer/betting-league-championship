"""
Team Service

This service handles business logic for team operations including creation,
updates, activation/deactivation, sport association validation, location filtering,
statistics calculation, and comprehensive data validation for the betting platform.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from models import Team, Sport, Competition, Match
from core import http_not_found, http_conflict
from api.schemas.team import TeamCreate, TeamUpdate

from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session, joinedload

from core import ValidationError, NotFoundError
from models.team import Team
from models.sport import Sport
from api.schemas.team import TeamCreate, TeamUpdate, TeamWithStats, TeamWithSport


class TeamService:
    """Service class for team operations."""
    
    @staticmethod
    def create_team(db: Session, team_data: TeamCreate) -> Team:
        """
        Create a new team.
        
        Args:
            db: Database session
            team_data: Team creation data
            
        Returns:
            Team: Created team
            
        Raises:
            ValidationError: If team name already exists in sport
            NotFoundError: If sport not found
        """
        # Verify sport exists
        sport = db.query(Sport).filter(Sport.id == team_data.sport_id).first()
        if not sport:
            raise NotFoundError(f"Sport with ID {team_data.sport_id} not found")
        
        if not sport.is_active:
            raise ValidationError("Cannot create team for inactive sport")
        
        # Check if team name already exists in this sport
        existing_team = db.query(Team).filter(
            and_(
                Team.name == team_data.name,
                Team.sport_id == team_data.sport_id
            )
        ).first()
        if existing_team:
            raise ValidationError(f"Team name '{team_data.name}' already exists in this sport")
        
        # Create new team
        team = Team(
            name=team_data.name,
            short_name=team_data.short_name,
            city=team_data.city,
            country=team_data.country,
            founded_year=team_data.founded_year,
            logo_url=team_data.logo_url,
            website_url=team_data.website_url,
            sport_id=team_data.sport_id,
            is_active=team_data.is_active
        )
        
        db.add(team)
        db.commit()
        db.refresh(team)
        
        return team
    
    @staticmethod
    def get_team_by_id(db: Session, team_id: UUID) -> Optional[Team]:
        """Get team by ID."""
        return db.query(Team).filter(Team.id == team_id).first()
    
    @staticmethod
    def get_team_by_name(db: Session, name: str, sport_id: Optional[UUID] = None) -> Optional[Team]:
        """Get team by name, optionally within a specific sport."""
        query = db.query(Team).filter(Team.name == name)
        if sport_id:
            query = query.filter(Team.sport_id == sport_id)
        return query.first()
    
    @staticmethod
    def update_team(
        db: Session, 
        team_id: UUID, 
        team_data: TeamUpdate
    ) -> Team:
        """
        Update team information.
        
        Args:
            db: Database session
            team_id: Team ID to update
            team_data: Update data
            
        Returns:
            Team: Updated team
            
        Raises:
            NotFoundError: If team not found
            ValidationError: If name already exists in sport
        """
        team = TeamService.get_team_by_id(db, team_id)
        if not team:
            raise NotFoundError(f"Team with ID {team_id} not found")
        
        # Check name uniqueness if name is being updated
        if team_data.name and team_data.name != team.name:
            existing_team = db.query(Team).filter(
                and_(
                    Team.name == team_data.name,
                    Team.sport_id == team.sport_id,
                    Team.id != team_id
                )
            ).first()
            if existing_team:
                raise ValidationError(f"Team name '{team_data.name}' already exists in this sport")
        
        # Update fields
        if team_data.name is not None:
            team.name = team_data.name
        if team_data.short_name is not None:
            team.short_name = team_data.short_name
        if team_data.city is not None:
            team.city = team_data.city
        if team_data.country is not None:
            team.country = team_data.country
        if team_data.founded_year is not None:
            team.founded_year = team_data.founded_year
        if team_data.logo_url is not None:
            team.logo_url = team_data.logo_url
        if team_data.website_url is not None:
            team.website_url = team_data.website_url
        if team_data.is_active is not None:
            team.is_active = team_data.is_active
        
        team.touch()  # Update timestamp
        
        db.commit()
        db.refresh(team)
        
        return team
    
    @staticmethod
    def delete_team(db: Session, team_id: UUID) -> None:
        """
        Delete team.
        
        Args:
            db: Database session
            team_id: Team ID to delete
            
        Raises:
            NotFoundError: If team not found
        """
        team = TeamService.get_team_by_id(db, team_id)
        if not team:
            raise NotFoundError(f"Team with ID {team_id} not found")
        
        # Soft delete by setting is_active to False
        team.is_active = False
        team.touch()
        
        db.commit()
    
    @staticmethod
    def get_team_with_stats(db: Session, team_id: UUID) -> Optional[TeamWithStats]:
        """
        Get team with statistics.
        
        Args:
            db: Database session
            team_id: Team ID
            
        Returns:
            Optional[TeamWithStats]: Team with stats or None
        """
        team = TeamService.get_team_by_id(db, team_id)
        if not team:
            return None
        
        # Calculate statistics
        stats = TeamService.calculate_team_stats(db, team_id)
        
        return TeamWithStats(
            id=team.id,
            name=team.name,
            short_name=team.short_name,
            city=team.city,
            country=team.country,
            founded_year=team.founded_year,
            logo_url=team.logo_url,
            website_url=team.website_url,
            sport_id=team.sport_id,
            is_active=team.is_active,
            created_at=team.created_at,
            updated_at=team.updated_at,
            total_matches=stats["total_matches"],
            wins=stats["wins"],
            losses=stats["losses"],
            draws=stats["draws"],
            win_percentage=stats["win_percentage"]
        )
    
    @staticmethod
    def get_team_with_sport(db: Session, team_id: UUID) -> Optional[TeamWithSport]:
        """
        Get team with sport information.
        
        Args:
            db: Database session
            team_id: Team ID
            
        Returns:
            Optional[TeamWithSport]: Team with sport info or None
        """
        team = db.query(Team).options(joinedload(Team.sport)).filter(Team.id == team_id).first()
        if not team:
            return None
        
        return TeamWithSport(
            id=team.id,
            name=team.name,
            short_name=team.short_name,
            city=team.city,
            country=team.country,
            founded_year=team.founded_year,
            logo_url=team.logo_url,
            website_url=team.website_url,
            sport_id=team.sport_id,
            is_active=team.is_active,
            created_at=team.created_at,
            updated_at=team.updated_at,
            sport_name=team.sport.name if team.sport else "Unknown"
        )
    
    @staticmethod
    def calculate_team_stats(db: Session, team_id: UUID) -> dict:
        """
        Calculate team statistics.
        
        Args:
            db: Database session
            team_id: Team ID
            
        Returns:
            dict: Team statistics
        """
        # For now, return basic stats (match stats would require Match/Result model integration)
        return {
            "total_matches": 0,  # TODO: Calculate from Match model
            "wins": 0,  # TODO: Calculate from Result model
            "losses": 0,  # TODO: Calculate from Result model
            "draws": 0,  # TODO: Calculate from Result model
            "win_percentage": 0.0  # TODO: Calculate from results
        }
    
    @staticmethod
    def build_team_list_query(
        db: Session,
        sport_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
        country: Optional[str] = None,
        search: Optional[str] = None
    ):
        """
        Build query for team list with filters.
        
        Args:
            db: Database session
            sport_id: Filter by sport
            is_active: Filter by active status
            country: Filter by country
            search: Search term
            
        Returns:
            Query: SQLAlchemy query
        """
        query = db.query(Team)
        
        # Filter by sport
        if sport_id:
            query = query.filter(Team.sport_id == sport_id)
        
        # Filter by active status
        if is_active is not None:
            query = query.filter(Team.is_active == is_active)
        
        # Filter by country
        if country:
            query = query.filter(Team.country.ilike(f"%{country}%"))
        
        # Search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Team.name.ilike(search_term),
                    Team.short_name.ilike(search_term),
                    Team.city.ilike(search_term),
                    Team.country.ilike(search_term)
                )
            )
        
        return query.order_by(Team.name)
    
    @staticmethod
    def get_teams_by_sport(db: Session, sport_id: UUID, active_only: bool = True) -> List[Team]:
        """
        Get all teams for a specific sport.
        
        Args:
            db: Database session
            sport_id: Sport ID
            active_only: Only return active teams
            
        Returns:
            List[Team]: List of teams
        """
        query = db.query(Team).filter(Team.sport_id == sport_id)
        if active_only:
            query = query.filter(Team.is_active == True)
        return query.order_by(Team.name).all()
    
    @staticmethod
    def activate_team(db: Session, team_id: UUID) -> Team:
        """
        Activate a team.
        
        Args:
            db: Database session
            team_id: Team ID to activate
            
        Returns:
            Team: Activated team
            
        Raises:
            NotFoundError: If team not found
        """
        team = TeamService.get_team_by_id(db, team_id)
        if not team:
            raise NotFoundError(f"Team with ID {team_id} not found")
        
        team.is_active = True
        team.touch()
        
        db.commit()
        db.refresh(team)
        
        return team
    
    @staticmethod
    def deactivate_team(db: Session, team_id: UUID) -> Team:
        """
        Deactivate a team.
        
        Args:
            db: Database session
            team_id: Team ID to deactivate
            
        Returns:
            Team: Deactivated team
            
        Raises:
            NotFoundError: If team not found
        """
        team = TeamService.get_team_by_id(db, team_id)
        if not team:
            raise NotFoundError(f"Team with ID {team_id} not found")
        
        team.is_active = False
        team.touch()
        
        db.commit()
        db.refresh(team)
        
        return team