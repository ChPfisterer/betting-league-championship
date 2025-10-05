"""
Match Service

This service handles business logic for match operations including creation,
updates, score management, status tracking, statistics calculation, and comprehensive
data validation for the betting platform. Matches are the core events where 
betting takes place and results are determined.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from models import Match, Competition, Season, Team, Sport, Bet
from core import http_not_found, http_conflict
from api.schemas.match import (
    MatchCreate, 
    MatchUpdate,
    MatchScoreUpdate,
    MatchStatusUpdate,
    MatchStatus,
    MatchType
)


class MatchService:
    """Service class for match operations."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def create_match(self, match_data: MatchCreate) -> Match:
        """
        Create a new match with comprehensive validation.
        
        Args:
            match_data: Match creation data
            
        Returns:
            Created match instance
            
        Raises:
            HTTPException: If validation fails or teams/competition not found
        """
        # Verify competition exists and is active
        competition = self.db.query(Competition).filter(
            Competition.id == match_data.competition_id,
            Competition.is_active == True
        ).first()
        
        if not competition:
            raise http_not_found("Competition not found or inactive")

        # Verify season exists if provided
        season = None
        if match_data.season_id:
            season = self.db.query(Season).filter(
                Season.id == match_data.season_id,
                Season.is_active == True
            ).first()
            
            if not season:
                raise http_not_found("Season not found or inactive")

        # Verify teams exist and belong to same sport as competition
        home_team = self.db.query(Team).filter(
            Team.id == match_data.home_team_id,
            Team.sport_id == competition.sport_id,
            Team.is_active == True
        ).first()
        
        if not home_team:
            raise http_not_found("Home team not found or does not belong to this sport")

        away_team = self.db.query(Team).filter(
            Team.id == match_data.away_team_id,
            Team.sport_id == competition.sport_id,
            Team.is_active == True
        ).first()
        
        if not away_team:
            raise http_not_found("Away team not found or does not belong to this sport")

        # Validate teams are different
        if match_data.home_team_id == match_data.away_team_id:
            raise http_conflict("Home and away teams must be different")

        # Check for duplicate matches (same teams, same competition, same date)
        existing = self.db.query(Match).filter(
            Match.competition_id == match_data.competition_id,
            Match.home_team_id == match_data.home_team_id,
            Match.away_team_id == match_data.away_team_id,
            func.date(Match.scheduled_at) == match_data.scheduled_at.date(),
            Match.is_active == True
        ).first()
        
        if existing:
            raise http_conflict("A match between these teams on this date already exists")

        # Set default betting closes time if not provided
        betting_closes_at = match_data.betting_closes_at
        if not betting_closes_at:
            betting_closes_at = match_data.scheduled_at

        # Create match
        match = Match(
            competition_id=match_data.competition_id,
            season_id=match_data.season_id,
            home_team_id=match_data.home_team_id,
            away_team_id=match_data.away_team_id,
            scheduled_at=match_data.scheduled_at,
            venue=match_data.venue,
            venue_name=match_data.venue_name,
            venue_city=match_data.venue_city,
            venue_country=match_data.venue_country,
            match_type=match_data.match_type,
            round_number=match_data.round_number,
            week_number=match_data.week_number,
            is_home_game=match_data.is_home_game,
            allow_betting=match_data.allow_betting,
            betting_closes_at=betting_closes_at,
            notes=match_data.notes,
            status=MatchStatus.SCHEDULED,
            is_active=True
        )

        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        
        return match

    def get_match(self, match_id: UUID) -> Optional[Match]:
        """Get match by ID."""
        return self.db.query(Match).filter(
            Match.id == match_id,
            Match.is_active == True
        ).first()

    def list_matches(
        self,
        skip: int = 0,
        limit: int = 100,
        competition_id: Optional[UUID] = None,
        season_id: Optional[UUID] = None,
        team_id: Optional[UUID] = None,
        status: Optional[MatchStatus] = None,
        match_type: Optional[MatchType] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        venue_city: Optional[str] = None,
        allow_betting: Optional[bool] = None
    ) -> List[Match]:
        """
        List matches with comprehensive filtering options.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            competition_id: Filter by competition ID
            season_id: Filter by season ID
            team_id: Filter by team (home or away)
            status: Filter by match status
            match_type: Filter by match type
            date_from: Filter matches from this date
            date_to: Filter matches until this date
            venue_city: Filter by venue city
            allow_betting: Filter by betting allowance
            
        Returns:
            List of matches matching criteria
        """
        query = self.db.query(Match).filter(Match.is_active == True)

        # Apply filters
        if competition_id:
            query = query.filter(Match.competition_id == competition_id)
            
        if season_id:
            query = query.filter(Match.season_id == season_id)
            
        if team_id:
            query = query.filter(
                or_(Match.home_team_id == team_id, Match.away_team_id == team_id)
            )
            
        if status:
            query = query.filter(Match.status == status)
            
        if match_type:
            query = query.filter(Match.match_type == match_type)
            
        if date_from:
            query = query.filter(func.date(Match.scheduled_at) >= date_from)
            
        if date_to:
            query = query.filter(func.date(Match.scheduled_at) <= date_to)
            
        if venue_city:
            query = query.filter(Match.venue_city.ilike(f"%{venue_city}%"))
            
        if allow_betting is not None:
            query = query.filter(Match.allow_betting == allow_betting)

        # Order by scheduled date and apply pagination
        return query.order_by(Match.scheduled_at.asc()).offset(skip).limit(limit).all()

    def update_match(
        self, 
        match_id: UUID, 
        update_data: MatchUpdate
    ) -> Optional[Match]:
        """
        Update match with validation.
        
        Args:
            match_id: Match ID to update
            update_data: Updated match data
            
        Returns:
            Updated match or None if not found
            
        Raises:
            HTTPException: If validation fails
        """
        match = self.get_match(match_id)
        if not match:
            return None

        # Prevent updates to completed/cancelled matches
        if match.status in [MatchStatus.COMPLETED, MatchStatus.CANCELLED]:
            raise http_conflict("Cannot update completed or cancelled matches")

        # Update fields
        for field, value in update_data.model_dump(exclude_unset=True).items():
            if hasattr(match, field):
                setattr(match, field, value)

        match.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(match)
        
        return match

    def update_score(
        self, 
        match_id: UUID, 
        score_data: MatchScoreUpdate
    ) -> Optional[Match]:
        """
        Update match score.
        
        Args:
            match_id: Match ID
            score_data: Score update data
            
        Returns:
            Updated match or None if not found
            
        Raises:
            HTTPException: If validation fails
        """
        match = self.get_match(match_id)
        if not match:
            return None

        # Only allow score updates for live or completed matches
        if match.status not in [MatchStatus.LIVE, MatchStatus.HALFTIME, MatchStatus.COMPLETED]:
            raise http_conflict("Can only update scores for live or completed matches")

        # Update scores
        match.home_score = score_data.home_score
        match.away_score = score_data.away_score

        # Determine winner
        if score_data.home_score > score_data.away_score:
            match.winner_team_id = match.home_team_id
            match.is_draw = False
        elif score_data.away_score > score_data.home_score:
            match.winner_team_id = match.away_team_id
            match.is_draw = False
        else:
            match.winner_team_id = None
            match.is_draw = True

        # Mark as completed if final score
        if score_data.is_final:
            match.status = MatchStatus.COMPLETED
            if not match.finished_at:
                match.finished_at = datetime.utcnow()
                
            # Calculate duration
            if match.started_at and match.finished_at:
                duration = match.finished_at - match.started_at
                match.duration_minutes = int(duration.total_seconds() / 60)

        match.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(match)
        
        return match

    def update_status(
        self, 
        match_id: UUID, 
        status_data: MatchStatusUpdate
    ) -> Optional[Match]:
        """
        Update match status.
        
        Args:
            match_id: Match ID
            status_data: Status update data
            
        Returns:
            Updated match or None if not found
        """
        match = self.get_match(match_id)
        if not match:
            return None

        old_status = match.status
        match.status = status_data.status

        # Handle status-specific logic
        if status_data.status == MatchStatus.LIVE and old_status == MatchStatus.SCHEDULED:
            match.started_at = datetime.utcnow()
        elif status_data.status == MatchStatus.COMPLETED and not match.finished_at:
            match.finished_at = datetime.utcnow()
            
            # Calculate duration if started
            if match.started_at:
                duration = match.finished_at - match.started_at
                match.duration_minutes = int(duration.total_seconds() / 60)

        match.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(match)
        
        return match

    def delete_match(self, match_id: UUID) -> bool:
        """
        Soft delete match (sets is_active to False).
        
        Args:
            match_id: Match ID to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            HTTPException: If match cannot be deleted
        """
        match = self.get_match(match_id)
        if not match:
            return False

        # Prevent deletion of matches with bets
        bet_count = self.db.query(Bet).filter(Bet.match_id == match_id).count()
        if bet_count > 0:
            raise http_conflict("Cannot delete match with existing bets")

        match.is_active = False
        match.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

    def get_match_statistics(self, match_id: UUID) -> Dict[str, Any]:
        """
        Calculate comprehensive match statistics.
        
        Args:
            match_id: Match ID
            
        Returns:
            Dictionary with match statistics
        """
        match = self.get_match(match_id)
        if not match:
            return {}

        # Count bets
        total_bets = self.db.query(Bet).filter(Bet.match_id == match_id).count()
        
        total_bet_amount = self.db.query(func.coalesce(func.sum(Bet.amount), 0)).filter(
            Bet.match_id == match_id
        ).scalar() or 0

        # Count bets by outcome (simplified - actual implementation would depend on bet types)
        home_team_bets = self.db.query(Bet).filter(
            Bet.match_id == match_id,
            Bet.predicted_outcome == 'home_win'
        ).count()
        
        away_team_bets = self.db.query(Bet).filter(
            Bet.match_id == match_id,
            Bet.predicted_outcome == 'away_win'
        ).count()
        
        draw_bets = self.db.query(Bet).filter(
            Bet.match_id == match_id,
            Bet.predicted_outcome == 'draw'
        ).count()

        return {
            'total_bets': total_bets,
            'total_bet_amount': float(total_bet_amount),
            'home_team_bets': home_team_bets,
            'away_team_bets': away_team_bets,
            'draw_bets': draw_bets,
            'attendance': None,  # Would be set manually
            'tv_viewers': None,  # Would be set manually
            'home_odds': None,   # Would be calculated based on bets
            'away_odds': None,   # Would be calculated based on bets
            'draw_odds': None    # Would be calculated based on bets
        }

    def get_matches_by_team(self, team_id: UUID, limit: int = 100) -> List[Match]:
        """Get matches for a specific team."""
        return self.db.query(Match).filter(
            or_(Match.home_team_id == team_id, Match.away_team_id == team_id),
            Match.is_active == True
        ).order_by(Match.scheduled_at.desc()).limit(limit).all()

    def get_matches_by_competition(self, competition_id: UUID, limit: int = 100) -> List[Match]:
        """Get matches by competition ID."""
        return self.db.query(Match).filter(
            Match.competition_id == competition_id,
            Match.is_active == True
        ).order_by(Match.scheduled_at.asc()).limit(limit).all()

    def get_upcoming_matches(self, days: int = 7, limit: int = 100) -> List[Match]:
        """Get upcoming matches within specified days."""
        from_date = datetime.now()
        to_date = from_date + datetime.timedelta(days=days)
        
        return self.db.query(Match).filter(
            Match.scheduled_at >= from_date,
            Match.scheduled_at <= to_date,
            Match.status == MatchStatus.SCHEDULED,
            Match.is_active == True
        ).order_by(Match.scheduled_at.asc()).limit(limit).all()

    def get_live_matches(self, limit: int = 100) -> List[Match]:
        """Get all currently live matches."""
        return self.db.query(Match).filter(
            Match.status.in_([MatchStatus.LIVE, MatchStatus.HALFTIME]),
            Match.is_active == True
        ).order_by(Match.started_at.asc()).limit(limit).all()

    def get_recent_results(self, days: int = 7, limit: int = 100) -> List[Match]:
        """Get recent completed matches."""
        from_date = datetime.now() - datetime.timedelta(days=days)
        
        return self.db.query(Match).filter(
            Match.finished_at >= from_date,
            Match.status == MatchStatus.COMPLETED,
            Match.is_active == True
        ).order_by(Match.finished_at.desc()).limit(limit).all()

    def search_matches(self, query: str, limit: int = 100) -> List[Match]:
        """Search matches by venue name or notes."""
        search_filter = f"%{query}%"
        return self.db.query(Match).filter(
            Match.is_active == True,
            or_(
                Match.venue_name.ilike(search_filter),
                Match.venue_city.ilike(search_filter),
                Match.notes.ilike(search_filter)
            )
        ).order_by(Match.scheduled_at.desc()).limit(limit).all()

    def get_head_to_head(self, team1_id: UUID, team2_id: UUID, limit: int = 10) -> List[Match]:
        """Get head-to-head matches between two teams."""
        return self.db.query(Match).filter(
            or_(
                and_(Match.home_team_id == team1_id, Match.away_team_id == team2_id),
                and_(Match.home_team_id == team2_id, Match.away_team_id == team1_id)
            ),
            Match.is_active == True
        ).order_by(Match.scheduled_at.desc()).limit(limit).all()