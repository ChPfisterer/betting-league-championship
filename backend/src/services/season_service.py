"""
Season Service

This service handles business logic for season operations including creation,
updates, status management, statistics calculation, and comprehensive data 
validation for the betting platform. Seasons provide temporal organization 
for competitions and enable historical tracking.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract

from models import Season, Sport, Competition, Team, Match, Bet
from core import http_not_found, http_conflict
from api.schemas.season import (
    SeasonCreate, 
    SeasonUpdate,
    SeasonStatus,
    SeasonType
)


class SeasonService:
    """Service class for season operations."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def create_season(self, season_data: SeasonCreate) -> Season:
        """
        Create a new season with comprehensive validation.
        
        Args:
            season_data: Season creation data
            
        Returns:
            Created season instance
            
        Raises:
            HTTPException: If sport not found or season name already exists
        """
        # Verify sport exists and is active
        sport = self.db.query(Sport).filter(
            Sport.id == season_data.sport_id,
            Sport.is_active == True
        ).first()
        
        if not sport:
            raise http_not_found("Sport not found or inactive")

        # Check for name uniqueness within the sport
        existing = self.db.query(Season).filter(
            Season.sport_id == season_data.sport_id,
            Season.name == season_data.name,
            Season.is_active == True
        ).first()
        
        if existing:
            raise http_conflict(f"Season '{season_data.name}' already exists in this sport")

        # Validate date logic
        if season_data.end_date <= season_data.start_date:
            raise http_conflict("End date must be after start date")
                
        if season_data.registration_start and season_data.registration_end:
            if season_data.registration_end <= season_data.registration_start:
                raise http_conflict("Registration end must be after registration start")
                
            if season_data.registration_end >= season_data.start_date:
                raise http_conflict("Registration must end before season starts")

        # Validate team limits
        if (season_data.min_teams and season_data.max_teams and 
            season_data.min_teams > season_data.max_teams):
            raise http_conflict("Minimum teams cannot exceed maximum teams")

        # Validate playoff teams
        if (season_data.playoff_teams and season_data.max_teams and 
            season_data.playoff_teams > season_data.max_teams):
            raise http_conflict("Playoff teams cannot exceed maximum teams")

        # Determine initial status
        current_date = date.today()
        status = SeasonStatus.UPCOMING
        
        if current_date >= season_data.start_date:
            if current_date <= season_data.end_date:
                status = SeasonStatus.ACTIVE
            else:
                status = SeasonStatus.COMPLETED

        # Create season
        season = Season(
            sport_id=season_data.sport_id,
            name=season_data.name,
            year=season_data.year,
            description=season_data.description,
            season_type=season_data.season_type,
            status=status,
            start_date=season_data.start_date,
            end_date=season_data.end_date,
            registration_start=season_data.registration_start,
            registration_end=season_data.registration_end,
            max_teams=season_data.max_teams,
            min_teams=season_data.min_teams,
            points_for_win=season_data.points_for_win,
            points_for_draw=season_data.points_for_draw,
            points_for_loss=season_data.points_for_loss,
            allow_draws=season_data.allow_draws,
            playoff_teams=season_data.playoff_teams,
            relegation_teams=season_data.relegation_teams,
            promotion_teams=season_data.promotion_teams,
            is_public=season_data.is_public,
            allow_betting=season_data.allow_betting,
            is_active=True
        )

        self.db.add(season)
        self.db.commit()
        self.db.refresh(season)
        
        return season

    def get_season(self, season_id: UUID) -> Optional[Season]:
        """Get season by ID."""
        return self.db.query(Season).filter(
            Season.id == season_id,
            Season.is_active == True
        ).first()

    def get_season_by_name(self, name: str, sport_id: Optional[UUID] = None) -> Optional[Season]:
        """Get season by name, optionally within a specific sport."""
        query = self.db.query(Season).filter(
            Season.name == name,
            Season.is_active == True
        )
        
        if sport_id:
            query = query.filter(Season.sport_id == sport_id)
            
        return query.first()

    def list_seasons(
        self,
        skip: int = 0,
        limit: int = 100,
        sport_id: Optional[UUID] = None,
        status: Optional[SeasonStatus] = None,
        season_type: Optional[SeasonType] = None,
        year: Optional[int] = None,
        is_public: Optional[bool] = None,
        allow_betting: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Season]:
        """
        List seasons with comprehensive filtering options.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            sport_id: Filter by sport ID
            status: Filter by season status
            season_type: Filter by season type
            year: Filter by year
            is_public: Filter by public visibility
            allow_betting: Filter by betting allowance
            search: Search in name and description
            
        Returns:
            List of seasons matching criteria
        """
        query = self.db.query(Season).filter(Season.is_active == True)

        # Apply filters
        if sport_id:
            query = query.filter(Season.sport_id == sport_id)
            
        if status:
            query = query.filter(Season.status == status)
            
        if season_type:
            query = query.filter(Season.season_type == season_type)
            
        if year:
            query = query.filter(Season.year == year)
            
        if is_public is not None:
            query = query.filter(Season.is_public == is_public)
            
        if allow_betting is not None:
            query = query.filter(Season.allow_betting == allow_betting)
            
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Season.name.ilike(search_filter),
                    Season.description.ilike(search_filter)
                )
            )

        # Order by year (newest first) and apply pagination
        return query.order_by(Season.year.desc(), Season.start_date.desc()).offset(skip).limit(limit).all()

    def update_season(
        self, 
        season_id: UUID, 
        update_data: SeasonUpdate
    ) -> Optional[Season]:
        """
        Update season with validation.
        
        Args:
            season_id: Season ID to update
            update_data: Updated season data
            
        Returns:
            Updated season or None if not found
            
        Raises:
            HTTPException: If validation fails or name conflicts
        """
        season = self.get_season(season_id)
        if not season:
            return None

        # Check name uniqueness if name is being updated
        if update_data.name and update_data.name != season.name:
            existing = self.db.query(Season).filter(
                Season.sport_id == season.sport_id,
                Season.name == update_data.name,
                Season.id != season_id,
                Season.is_active == True
            ).first()
            
            if existing:
                raise http_conflict(f"Season '{update_data.name}' already exists in this sport")

        # Update fields
        for field, value in update_data.model_dump(exclude_unset=True).items():
            if hasattr(season, field):
                setattr(season, field, value)

        # Validate dates after update
        if season.start_date and season.end_date:
            if season.end_date <= season.start_date:
                raise http_conflict("End date must be after start date")
                
        if season.registration_start and season.registration_end:
            if season.registration_end <= season.registration_start:
                raise http_conflict("Registration end must be after registration start")
                
            if season.registration_end >= season.start_date:
                raise http_conflict("Registration must end before season starts")

        # Update status based on dates
        current_date = date.today()
        if current_date < season.start_date:
            season.status = SeasonStatus.UPCOMING
        elif current_date <= season.end_date:
            season.status = SeasonStatus.ACTIVE
        else:
            season.status = SeasonStatus.COMPLETED

        season.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(season)
        
        return season

    def delete_season(self, season_id: UUID) -> bool:
        """
        Soft delete season (sets is_active to False).
        
        Args:
            season_id: Season ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        season = self.get_season(season_id)
        if not season:
            return False

        season.is_active = False
        season.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

    def update_status(self, season_id: UUID, status: SeasonStatus) -> Optional[Season]:
        """
        Update season status.
        
        Args:
            season_id: Season ID
            status: New status
            
        Returns:
            Updated season or None if not found
        """
        season = self.get_season(season_id)
        if not season:
            return None

        season.status = status
        season.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(season)
        
        return season

    def get_season_competitions(self, season_id: UUID) -> List[Competition]:
        """Get all competitions in a season."""
        return self.db.query(Competition).filter(
            Competition.season_id == season_id,
            Competition.is_active == True
        ).order_by(Competition.start_date).all()

    def get_season_statistics(self, season_id: UUID) -> Dict[str, Any]:
        """
        Calculate comprehensive season statistics.
        
        Args:
            season_id: Season ID
            
        Returns:
            Dictionary with season statistics
        """
        season = self.get_season(season_id)
        if not season:
            return {}

        # Count competitions
        total_competitions = self.db.query(Competition).filter(
            Competition.season_id == season_id,
            Competition.is_active == True
        ).count()

        # Count teams (unique teams participating in any competition in this season)
        total_teams = self.db.query(func.count(func.distinct(Team.id))).join(Competition).filter(
            Competition.season_id == season_id,
            Competition.is_active == True,
            Team.is_active == True
        ).scalar() or 0

        # Count matches
        total_matches = self.db.query(Match).join(Competition).filter(
            Competition.season_id == season_id,
            Competition.is_active == True
        ).count()
        
        completed_matches = self.db.query(Match).join(Competition).filter(
            Competition.season_id == season_id,
            Competition.is_active == True,
            Match.status == 'completed'
        ).count()
        
        pending_matches = total_matches - completed_matches

        # Count bets
        total_bets = self.db.query(Bet).join(Match).join(Competition).filter(
            Competition.season_id == season_id,
            Competition.is_active == True
        ).count()
        
        total_bet_amount = self.db.query(func.coalesce(func.sum(Bet.amount), 0)).join(Match).join(Competition).filter(
            Competition.season_id == season_id,
            Competition.is_active == True
        ).scalar() or 0

        # Calculate days remaining
        days_remaining = None
        if season.end_date:
            today = date.today()
            if season.end_date > today:
                days_remaining = (season.end_date - today).days

        # Calculate progress percentage
        progress_percentage = 0.0
        if season.start_date and season.end_date:
            total_days = (season.end_date - season.start_date).days
            if total_days > 0:
                elapsed_days = max(0, (date.today() - season.start_date).days)
                progress_percentage = min(100.0, (elapsed_days / total_days) * 100)

        # Calculate average goals per match (if applicable)
        average_goals_per_match = None
        if completed_matches > 0:
            total_goals = self.db.query(
                func.coalesce(func.sum(Match.home_score + Match.away_score), 0)
            ).join(Competition).filter(
                Competition.season_id == season_id,
                Competition.is_active == True,
                Match.status == 'completed',
                Match.home_score.isnot(None),
                Match.away_score.isnot(None)
            ).scalar() or 0
            
            if total_goals > 0:
                average_goals_per_match = total_goals / completed_matches

        return {
            'total_competitions': total_competitions,
            'total_teams': total_teams,
            'total_matches': total_matches,
            'completed_matches': completed_matches,
            'pending_matches': pending_matches,
            'total_bets': total_bets,
            'total_bet_amount': float(total_bet_amount),
            'days_remaining': days_remaining,
            'progress_percentage': progress_percentage,
            'average_goals_per_match': average_goals_per_match
        }

    def get_seasons_by_sport(self, sport_id: UUID, limit: int = 100) -> List[Season]:
        """Get seasons by sport ID."""
        return self.db.query(Season).filter(
            Season.sport_id == sport_id,
            Season.is_active == True
        ).order_by(Season.year.desc(), Season.start_date.desc()).limit(limit).all()

    def get_seasons_by_year(self, year: int, limit: int = 100) -> List[Season]:
        """Get seasons by year."""
        return self.db.query(Season).filter(
            Season.year == year,
            Season.is_active == True
        ).order_by(Season.start_date.desc()).limit(limit).all()

    def search_seasons(self, query: str, limit: int = 100) -> List[Season]:
        """Search seasons by name or description."""
        search_filter = f"%{query}%"
        return self.db.query(Season).filter(
            Season.is_active == True,
            or_(
                Season.name.ilike(search_filter),
                Season.description.ilike(search_filter)
            )
        ).order_by(Season.year.desc(), Season.start_date.desc()).limit(limit).all()

    def get_public_seasons(self, limit: int = 100) -> List[Season]:
        """Get all public seasons."""
        return self.db.query(Season).filter(
            Season.is_active == True,
            Season.is_public == True
        ).order_by(Season.year.desc(), Season.start_date.desc()).limit(limit).all()

    def get_active_seasons(self, limit: int = 100) -> List[Season]:
        """Get all active seasons."""
        return self.db.query(Season).filter(
            Season.is_active == True,
            Season.status == SeasonStatus.ACTIVE
        ).order_by(Season.year.desc(), Season.start_date.desc()).limit(limit).all()

    def get_current_seasons(self, sport_id: Optional[UUID] = None) -> List[Season]:
        """Get currently active seasons, optionally filtered by sport."""
        current_date = date.today()
        query = self.db.query(Season).filter(
            Season.is_active == True,
            Season.start_date <= current_date,
            Season.end_date >= current_date
        )
        
        if sport_id:
            query = query.filter(Season.sport_id == sport_id)
            
        return query.order_by(Season.start_date.desc()).all()

    def calculate_team_standings(self, season_id: UUID) -> List[Dict[str, Any]]:
        """
        Calculate team standings for a season based on match results.
        
        Args:
            season_id: Season ID
            
        Returns:
            List of team standings with points, wins, draws, losses, etc.
        """
        season = self.get_season(season_id)
        if not season:
            return []

        # Get all teams participating in this season
        teams = self.db.query(Team).join(Competition).filter(
            Competition.season_id == season_id,
            Competition.is_active == True,
            Team.is_active == True
        ).distinct().all()

        standings = []
        
        for team in teams:
            # Calculate team statistics
            home_matches = self.db.query(Match).join(Competition).filter(
                Competition.season_id == season_id,
                Match.home_team_id == team.id,
                Match.status == 'completed'
            ).all()
            
            away_matches = self.db.query(Match).join(Competition).filter(
                Competition.season_id == season_id,
                Match.away_team_id == team.id,
                Match.status == 'completed'
            ).all()

            wins = draws = losses = 0
            goals_for = goals_against = 0
            points = 0

            # Calculate home stats
            for match in home_matches:
                goals_for += match.home_score or 0
                goals_against += match.away_score or 0
                
                if match.home_score > match.away_score:
                    wins += 1
                    points += season.points_for_win
                elif match.home_score == match.away_score and season.allow_draws:
                    draws += 1
                    points += season.points_for_draw
                else:
                    losses += 1
                    points += season.points_for_loss

            # Calculate away stats
            for match in away_matches:
                goals_for += match.away_score or 0
                goals_against += match.home_score or 0
                
                if match.away_score > match.home_score:
                    wins += 1
                    points += season.points_for_win
                elif match.away_score == match.home_score and season.allow_draws:
                    draws += 1
                    points += season.points_for_draw
                else:
                    losses += 1
                    points += season.points_for_loss

            games_played = wins + draws + losses
            goal_difference = goals_for - goals_against

            standings.append({
                'team_id': team.id,
                'team_name': team.name,
                'points': points,
                'games_played': games_played,
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'goal_difference': goal_difference
            })

        # Sort by points (desc), then goal difference (desc), then goals for (desc)
        standings.sort(key=lambda x: (-x['points'], -x['goal_difference'], -x['goals_for']))
        
        # Add position
        for i, standing in enumerate(standings, 1):
            standing['position'] = i

        return standings