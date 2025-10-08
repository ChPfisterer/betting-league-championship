"""
Competition Service

This service handles business logic for competition operations including creation,
updates, team registration, status management, statistics calculation, and comprehensive
data validation for the betting platform. Competitions organize teams within sports
and provide the framework for matches and betting.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from models import Competition, Sport, Team, Match, Bet
from core import http_not_found, http_conflict
from api.schemas.competition import (
    CompetitionCreate, 
    CompetitionUpdate,
    CompetitionStatus,
    CompetitionFormat
)


class CompetitionService:
    """Service class for competition operations."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def create_competition(self, competition_data: CompetitionCreate) -> Competition:
        """
        Create a new competition with comprehensive validation.
        
        Args:
            competition_data: Competition creation data
            
        Returns:
            Created competition instance
            
        Raises:
            HTTPException: If sport not found or competition name already exists
        """
        # Verify sport exists
        sport = self.db.query(Sport).filter(
            Sport.id == competition_data.sport_id
        ).first()
        
        if not sport:
            raise http_not_found("Sport not found or inactive")

        # Check for name uniqueness within the sport
        existing = self.db.query(Competition).filter(
            Competition.sport_id == competition_data.sport_id,
            Competition.name == competition_data.name
        ).first()
        
        if existing:
            raise http_conflict(f"Competition '{competition_data.name}' already exists in this sport")

        # Validate date logic
        if competition_data.start_date and competition_data.end_date:
            if competition_data.end_date <= competition_data.start_date:
                raise http_conflict("End date must be after start date")
                
        if competition_data.registration_deadline and competition_data.start_date:
            if competition_data.registration_deadline >= competition_data.start_date:
                raise http_conflict("Registration deadline must be before start date")

        # Validate team limits
        if (competition_data.min_teams and competition_data.max_teams and 
            competition_data.min_teams > competition_data.max_teams):
            raise http_conflict("Minimum teams cannot exceed maximum teams")

        # Determine initial status
        current_date = datetime.now().date()
        status = CompetitionStatus.DRAFT
        
        if competition_data.start_date:
            if current_date < competition_data.start_date:
                status = CompetitionStatus.UPCOMING
            elif competition_data.end_date and current_date > competition_data.end_date:
                status = CompetitionStatus.COMPLETED
            else:
                status = CompetitionStatus.ACTIVE

        # Create competition with correct field mapping
        competition = Competition(
            sport_id=competition_data.sport_id,
            season_id=competition_data.sport_id,  # Temporarily use sport_id as we need to check the seeder
            name=competition_data.name,
            description=competition_data.description,
            format_type=competition_data.format.value,  # Map format to format_type
            start_date=competition_data.start_date,
            end_date=competition_data.end_date,
            registration_deadline=competition_data.registration_deadline,
            max_participants=competition_data.max_teams,  # Map max_teams to max_participants
            min_participants=competition_data.min_teams,  # Map min_teams to min_participants
            entry_fee=competition_data.entry_fee,
            prize_pool=competition_data.prize_pool,
            rules=competition_data.rules,
            visibility='public' if competition_data.is_public else 'private',  # Map is_public to visibility
            allow_public_betting=competition_data.allow_betting  # Map allow_betting to allow_public_betting
        )

        self.db.add(competition)
        self.db.commit()
        self.db.refresh(competition)
        
        return competition

    def get_competition(self, competition_id: UUID) -> Optional[Competition]:
        """Get competition by ID."""
        return self.db.query(Competition).filter(
            Competition.id == competition_id
        ).first()

    def get_competition_by_name(self, name: str, sport_id: Optional[UUID] = None) -> Optional[Competition]:
        """Get competition by name, optionally within a specific sport."""
        query = self.db.query(Competition).filter(
            Competition.name == name
        )
        
        if sport_id:
            query = query.filter(Competition.sport_id == sport_id)
            
        return query.first()

    def list_competitions(
        self,
        skip: int = 0,
        limit: int = 100,
        sport_id: Optional[UUID] = None,
        status: Optional[CompetitionStatus] = None,
        format: Optional[CompetitionFormat] = None,
        is_public: Optional[bool] = None,
        allow_betting: Optional[bool] = None,
        search: Optional[str] = None,
        year: Optional[int] = None
    ) -> List[Competition]:
        """
        List competitions with comprehensive filtering options.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            sport_id: Filter by sport ID
            status: Filter by competition status
            format: Filter by competition format
            is_public: Filter by public visibility
            allow_betting: Filter by betting allowance
            search: Search in name and description
            year: Filter by year (start_date year)
            
        Returns:
            List of competitions matching criteria
        """
        query = self.db.query(Competition)

        # Apply filters
        if sport_id:
            query = query.filter(Competition.sport_id == sport_id)
            
        if status:
            query = query.filter(Competition.status == status)
            
        if format:
            query = query.filter(Competition.format == format)
            
        if is_public is not None:
            if is_public:
                query = query.filter(Competition.visibility == 'public')
            else:
                query = query.filter(Competition.visibility != 'public')
            
        if allow_betting is not None:
            query = query.filter(Competition.allow_public_betting == allow_betting)
            
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Competition.name.ilike(search_filter),
                    Competition.description.ilike(search_filter),
                    Competition.location.ilike(search_filter)
                )
            )
            
        if year:
            query = query.filter(
                func.extract('year', Competition.start_date) == year
            )

        # Order by start date (newest first) and apply pagination
        return query.order_by(Competition.start_date.desc()).offset(skip).limit(limit).all()

    def update_competition(
        self, 
        competition_id: UUID, 
        update_data: CompetitionUpdate
    ) -> Optional[Competition]:
        """
        Update competition with validation.
        
        Args:
            competition_id: Competition ID to update
            update_data: Updated competition data
            
        Returns:
            Updated competition or None if not found
            
        Raises:
            HTTPException: If validation fails or name conflicts
        """
        competition = self.get_competition(competition_id)
        if not competition:
            return None

        # Check name uniqueness if name is being updated
        if update_data.name and update_data.name != competition.name:
            existing = self.db.query(Competition).filter(
                Competition.sport_id == competition.sport_id,
                Competition.name == update_data.name,
                Competition.id != competition_id,
                Competition.is_active == True
            ).first()
            
            if existing:
                raise http_conflict(f"Competition '{update_data.name}' already exists in this sport")

        # Update fields
        for field, value in update_data.model_dump(exclude_unset=True).items():
            if hasattr(competition, field):
                setattr(competition, field, value)

        # Validate dates after update
        if competition.start_date and competition.end_date:
            if competition.end_date <= competition.start_date:
                raise http_conflict("End date must be after start date")
                
        if competition.registration_deadline and competition.start_date:
            if competition.registration_deadline >= competition.start_date:
                raise http_conflict("Registration deadline must be before start date")

        # Update status based on dates
        if competition.start_date:
            current_date = datetime.now().date()
            if current_date < competition.start_date:
                competition.status = CompetitionStatus.UPCOMING
            elif competition.end_date and current_date > competition.end_date:
                competition.status = CompetitionStatus.COMPLETED
            else:
                competition.status = CompetitionStatus.ACTIVE

        competition.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(competition)
        
        return competition

    def delete_competition(self, competition_id: UUID) -> bool:
        """
        Soft delete competition (sets is_active to False).
        
        Args:
            competition_id: Competition ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        competition = self.get_competition(competition_id)
        if not competition:
            return False

        competition.is_active = False
        competition.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

    def update_status(self, competition_id: UUID, status: CompetitionStatus) -> Optional[Competition]:
        """
        Update competition status.
        
        Args:
            competition_id: Competition ID
            status: New status
            
        Returns:
            Updated competition or None if not found
        """
        competition = self.get_competition(competition_id)
        if not competition:
            return None

        competition.status = status
        competition.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(competition)
        
        return competition

    def register_team(self, competition_id: UUID, team_id: UUID) -> bool:
        """
        Register a team for the competition.
        
        Args:
            competition_id: Competition ID
            team_id: Team ID to register
            
        Returns:
            True if registration successful
            
        Raises:
            HTTPException: If validation fails
        """
        competition = self.get_competition(competition_id)
        if not competition:
            raise http_not_found("Competition not found")

        # Verify team exists and belongs to same sport
        team = self.db.query(Team).filter(
            Team.id == team_id,
            Team.sport_id == competition.sport_id,
            Team.is_active == True
        ).first()
        
        if not team:
            raise http_not_found("Team not found or does not belong to this sport")

        # For now, just return success - we'll implement proper team registration later
        # when we have the competition-team relationship table
        return True

    def unregister_team(self, competition_id: UUID, team_id: UUID) -> bool:
        """
        Unregister a team from the competition.
        
        Args:
            competition_id: Competition ID
            team_id: Team ID to unregister
            
        Returns:
            True if unregistration successful
        """
        # For now, just return success - we'll implement proper team unregistration later
        # when we have the competition-team relationship table
        return True

    def get_competition_teams(self, competition_id: UUID) -> List[Team]:
        """Get all teams registered for a competition."""
        # For now, return empty list - we'll implement proper team listing later
        # when we have the competition-team relationship table
        return []

    def get_competition_statistics(self, competition_id: UUID) -> Dict[str, Any]:
        """
        Calculate comprehensive competition statistics.
        
        Args:
            competition_id: Competition ID
            
        Returns:
            Dictionary with competition statistics
        """
        competition = self.get_competition(competition_id)
        if not competition:
            return {}

        # Count registered teams (simplified for now)
        total_teams = 0

        # Count matches
        total_matches = self.db.query(Match).filter(
            Match.competition_id == competition_id
        ).count()
        
        completed_matches = self.db.query(Match).filter(
            Match.competition_id == competition_id,
            Match.status == 'completed'
        ).count()
        
        pending_matches = total_matches - completed_matches

        # Count bets
        total_bets = self.db.query(Bet).join(Match).filter(
            Match.competition_id == competition_id
        ).count()
        
        total_bet_amount = self.db.query(func.coalesce(func.sum(Bet.amount), 0)).join(Match).filter(
            Match.competition_id == competition_id
        ).scalar() or 0

        # Calculate days remaining
        days_remaining = None
        if competition.end_date:
            today = datetime.now().date()
            if competition.end_date > today:
                days_remaining = (competition.end_date - today).days

        # Calculate participation rate
        participation_rate = 0.0
        if competition.max_teams:
            participation_rate = (total_teams / competition.max_teams) * 100

        return {
            'total_teams': total_teams,
            'total_matches': total_matches,
            'completed_matches': completed_matches,
            'pending_matches': pending_matches,
            'total_bets': total_bets,
            'total_bet_amount': float(total_bet_amount),
            'days_remaining': days_remaining,
            'participation_rate': participation_rate
        }

    def get_competitions_by_sport(self, sport_id: UUID, limit: int = 100) -> List[Competition]:
        """Get competitions by sport ID."""
        return self.db.query(Competition).filter(
            Competition.sport_id == sport_id
        ).order_by(Competition.start_date.desc()).limit(limit).all()

    def search_competitions(self, query: str, limit: int = 100) -> List[Competition]:
        """Search competitions by name, description, or location."""
        search_filter = f"%{query}%"
        return self.db.query(Competition).filter(
            or_(
                Competition.name.ilike(search_filter),
                Competition.description.ilike(search_filter)
            )
        ).order_by(Competition.start_date.desc()).limit(limit).all()

    def get_public_competitions(self, limit: int = 100) -> List[Competition]:
        """Get all public competitions."""
        return self.db.query(Competition).filter(
            Competition.visibility == 'public'
        ).order_by(Competition.start_date.desc()).limit(limit).all()

    def get_active_competitions(self, limit: int = 100) -> List[Competition]:
        """Get all active competitions."""
        return self.db.query(Competition).filter(
            Competition.status == CompetitionStatus.ACTIVE.value
        ).order_by(Competition.start_date.desc()).limit(limit).all()