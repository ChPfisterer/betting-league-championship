"""
Player Service

This service handles business logic for player operations including creation,
updates, team transfers, performance tracking, statistics calculation, and 
comprehensive data validation for the betting platform. Players represent 
individual athletes participating in teams and competitions.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract

from models import Player, Team, Sport, Match
from core import http_not_found, http_conflict
from api.schemas.player import (
    PlayerCreate, 
    PlayerUpdate,
    PlayerStatus,
    PlayerPosition
)


class PlayerService:
    """Service class for player operations."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def create_player(self, player_data: PlayerCreate) -> Player:
        """
        Create a new player with comprehensive validation.
        
        Args:
            player_data: Player creation data
            
        Returns:
            Created player instance
            
        Raises:
            HTTPException: If team not found or validation fails
        """
        # Verify team exists and is active
        team = self.db.query(Team).filter(
            Team.id == player_data.team_id,
            Team.is_active == True
        ).first()
        
        if not team:
            raise http_not_found("Team not found or inactive")

        # Check for jersey number uniqueness within team
        if player_data.jersey_number is not None:
            existing = self.db.query(Player).filter(
                Player.team_id == player_data.team_id,
                Player.jersey_number == player_data.jersey_number,
                Player.is_active == True
            ).first()
            
            if existing:
                raise http_conflict(f"Jersey number {player_data.jersey_number} is already taken by another player on this team")

        # Validate captain/vice-captain logic
        if player_data.is_captain:
            # Check if team already has a captain
            existing_captain = self.db.query(Player).filter(
                Player.team_id == player_data.team_id,
                Player.is_captain == True,
                Player.is_active == True
            ).first()
            
            if existing_captain:
                raise http_conflict("Team already has a captain")

        if player_data.is_vice_captain:
            # Check if team already has a vice captain
            existing_vice = self.db.query(Player).filter(
                Player.team_id == player_data.team_id,
                Player.is_vice_captain == True,
                Player.is_active == True
            ).first()
            
            if existing_vice:
                raise http_conflict("Team already has a vice captain")

        # Generate display name if not provided
        display_name = player_data.display_name
        if not display_name:
            display_name = f"{player_data.first_name} {player_data.last_name}"

        # Create player
        player = Player(
            team_id=player_data.team_id,
            first_name=player_data.first_name,
            last_name=player_data.last_name,
            display_name=display_name,
            jersey_number=player_data.jersey_number,
            position=player_data.position,
            secondary_positions=player_data.secondary_positions,
            date_of_birth=player_data.date_of_birth,
            nationality=player_data.nationality,
            height_cm=player_data.height_cm,
            weight_kg=player_data.weight_kg,
            preferred_foot=player_data.preferred_foot,
            biography=player_data.biography,
            photo_url=player_data.photo_url,
            social_media=player_data.social_media,
            contract_start=player_data.contract_start,
            contract_end=player_data.contract_end,
            market_value=player_data.market_value,
            salary=player_data.salary,
            is_captain=player_data.is_captain,
            is_vice_captain=player_data.is_vice_captain,
            status=PlayerStatus.ACTIVE,
            is_active=True
        )

        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        
        return player

    def get_player(self, player_id: UUID) -> Optional[Player]:
        """Get player by ID."""
        return self.db.query(Player).filter(
            Player.id == player_id,
            Player.is_active == True
        ).first()

    def list_players(
        self,
        skip: int = 0,
        limit: int = 100,
        team_id: Optional[UUID] = None,
        position: Optional[PlayerPosition] = None,
        nationality: Optional[str] = None,
        status: Optional[PlayerStatus] = None,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        is_captain: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Player]:
        """
        List players with comprehensive filtering options.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            team_id: Filter by team ID
            position: Filter by player position
            nationality: Filter by nationality
            status: Filter by player status
            age_min: Minimum age filter
            age_max: Maximum age filter
            is_captain: Filter captains only
            search: Search in name
            
        Returns:
            List of players matching criteria
        """
        query = self.db.query(Player).filter(Player.is_active == True)

        # Apply filters
        if team_id:
            query = query.filter(Player.team_id == team_id)
            
        if position:
            query = query.filter(Player.position == position)
            
        if nationality:
            query = query.filter(Player.nationality.ilike(f"%{nationality}%"))
            
        if status:
            query = query.filter(Player.status == status)
            
        if age_min or age_max:
            current_year = datetime.now().year
            if age_min:
                max_birth_year = current_year - age_min
                query = query.filter(extract('year', Player.date_of_birth) <= max_birth_year)
            if age_max:
                min_birth_year = current_year - age_max
                query = query.filter(extract('year', Player.date_of_birth) >= min_birth_year)
            
        if is_captain is not None:
            query = query.filter(Player.is_captain == is_captain)
            
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Player.first_name.ilike(search_filter),
                    Player.last_name.ilike(search_filter),
                    Player.display_name.ilike(search_filter)
                )
            )

        # Order by name and apply pagination
        return query.order_by(Player.last_name, Player.first_name).offset(skip).limit(limit).all()

    def update_player(
        self, 
        player_id: UUID, 
        update_data: PlayerUpdate
    ) -> Optional[Player]:
        """
        Update player with validation.
        
        Args:
            player_id: Player ID to update
            update_data: Updated player data
            
        Returns:
            Updated player or None if not found
            
        Raises:
            HTTPException: If validation fails
        """
        player = self.get_player(player_id)
        if not player:
            return None

        # Check jersey number uniqueness if being updated
        if update_data.jersey_number is not None and update_data.jersey_number != player.jersey_number:
            existing = self.db.query(Player).filter(
                Player.team_id == player.team_id,
                Player.jersey_number == update_data.jersey_number,
                Player.id != player_id,
                Player.is_active == True
            ).first()
            
            if existing:
                raise http_conflict(f"Jersey number {update_data.jersey_number} is already taken")

        # Handle captain/vice-captain updates
        if update_data.is_captain is not None and update_data.is_captain != player.is_captain:
            if update_data.is_captain:
                # Check if team already has a captain
                existing_captain = self.db.query(Player).filter(
                    Player.team_id == player.team_id,
                    Player.is_captain == True,
                    Player.id != player_id,
                    Player.is_active == True
                ).first()
                
                if existing_captain:
                    raise http_conflict("Team already has a captain")

        if update_data.is_vice_captain is not None and update_data.is_vice_captain != player.is_vice_captain:
            if update_data.is_vice_captain:
                # Check if team already has a vice captain
                existing_vice = self.db.query(Player).filter(
                    Player.team_id == player.team_id,
                    Player.is_vice_captain == True,
                    Player.id != player_id,
                    Player.is_active == True
                ).first()
                
                if existing_vice:
                    raise http_conflict("Team already has a vice captain")

        # Update fields
        for field, value in update_data.model_dump(exclude_unset=True).items():
            if hasattr(player, field):
                setattr(player, field, value)

        # Update display name if first/last name changed
        if update_data.first_name or update_data.last_name:
            if not update_data.display_name:
                player.display_name = f"{player.first_name} {player.last_name}"

        player.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(player)
        
        return player

    def delete_player(self, player_id: UUID) -> bool:
        """
        Soft delete player (sets is_active to False).
        
        Args:
            player_id: Player ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        player = self.get_player(player_id)
        if not player:
            return False

        player.is_active = False
        player.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

    def update_status(self, player_id: UUID, status: PlayerStatus) -> Optional[Player]:
        """
        Update player status.
        
        Args:
            player_id: Player ID
            status: New player status
            
        Returns:
            Updated player or None if not found
        """
        player = self.get_player(player_id)
        if not player:
            return None

        player.status = status
        player.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(player)
        
        return player

    def transfer_player(self, player_id: UUID, new_team_id: UUID) -> Optional[Player]:
        """
        Transfer player to a new team.
        
        Args:
            player_id: Player ID
            new_team_id: New team ID
            
        Returns:
            Updated player or None if not found
            
        Raises:
            HTTPException: If transfer validation fails
        """
        player = self.get_player(player_id)
        if not player:
            return None

        # Verify new team exists and is active
        new_team = self.db.query(Team).filter(
            Team.id == new_team_id,
            Team.is_active == True
        ).first()
        
        if not new_team:
            raise http_not_found("New team not found or inactive")

        # Verify teams belong to same sport
        old_team = self.db.query(Team).filter(Team.id == player.team_id).first()
        if old_team and old_team.sport_id != new_team.sport_id:
            raise http_conflict("Cannot transfer player between different sports")

        # Check jersey number availability in new team
        if player.jersey_number:
            existing = self.db.query(Player).filter(
                Player.team_id == new_team_id,
                Player.jersey_number == player.jersey_number,
                Player.is_active == True
            ).first()
            
            if existing:
                # Clear jersey number for now - will need to be reassigned
                player.jersey_number = None

        # Reset captain/vice-captain status for transfer
        player.is_captain = False
        player.is_vice_captain = False
        
        # Update team
        player.team_id = new_team_id
        player.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(player)
        
        return player

    def get_player_statistics(self, player_id: UUID, season_id: Optional[UUID] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive player statistics.
        
        Args:
            player_id: Player ID
            season_id: Optional season to filter statistics
            
        Returns:
            Dictionary with player statistics
        """
        player = self.get_player(player_id)
        if not player:
            return {}

        # Basic match statistics - simplified for now
        # In a real implementation, this would involve match events, goals, assists, etc.
        matches_played = 0
        matches_started = 0
        minutes_played = 0
        goals_scored = 0
        assists = 0
        yellow_cards = 0
        red_cards = 0

        # For now, return placeholder statistics
        return {
            'matches_played': matches_played,
            'matches_started': matches_started,
            'minutes_played': minutes_played,
            'goals_scored': goals_scored,
            'assists': assists,
            'yellow_cards': yellow_cards,
            'red_cards': red_cards,
            'detailed_stats': {},
            'season_id': season_id,
            'last_updated': datetime.utcnow()
        }

    def get_players_by_team(self, team_id: UUID, limit: int = 100) -> List[Player]:
        """Get players by team ID."""
        return self.db.query(Player).filter(
            Player.team_id == team_id,
            Player.is_active == True
        ).order_by(Player.jersey_number.asc().nullslast(), Player.last_name).limit(limit).all()

    def get_players_by_position(self, position: PlayerPosition, limit: int = 100) -> List[Player]:
        """Get players by position."""
        return self.db.query(Player).filter(
            Player.position == position,
            Player.is_active == True
        ).order_by(Player.last_name, Player.first_name).limit(limit).all()

    def get_players_by_nationality(self, nationality: str, limit: int = 100) -> List[Player]:
        """Get players by nationality."""
        return self.db.query(Player).filter(
            Player.nationality.ilike(f"%{nationality}%"),
            Player.is_active == True
        ).order_by(Player.last_name, Player.first_name).limit(limit).all()

    def search_players(self, query: str, limit: int = 100) -> List[Player]:
        """Search players by name."""
        search_filter = f"%{query}%"
        return self.db.query(Player).filter(
            Player.is_active == True,
            or_(
                Player.first_name.ilike(search_filter),
                Player.last_name.ilike(search_filter),
                Player.display_name.ilike(search_filter)
            )
        ).order_by(Player.last_name, Player.first_name).limit(limit).all()

    def get_team_captains(self, team_id: UUID) -> List[Player]:
        """Get team captains and vice-captains."""
        return self.db.query(Player).filter(
            Player.team_id == team_id,
            or_(Player.is_captain == True, Player.is_vice_captain == True),
            Player.is_active == True
        ).order_by(Player.is_captain.desc(), Player.is_vice_captain.desc()).all()

    def get_players_by_age_range(self, age_min: int, age_max: int, limit: int = 100) -> List[Player]:
        """Get players within age range."""
        current_year = datetime.now().year
        max_birth_year = current_year - age_min
        min_birth_year = current_year - age_max
        
        return self.db.query(Player).filter(
            Player.date_of_birth.isnot(None),
            extract('year', Player.date_of_birth) >= min_birth_year,
            extract('year', Player.date_of_birth) <= max_birth_year,
            Player.is_active == True
        ).order_by(Player.date_of_birth.desc()).limit(limit).all()

    def get_expiring_contracts(self, days: int = 30, limit: int = 100) -> List[Player]:
        """Get players with contracts expiring soon."""
        from datetime import date, timedelta
        expiry_date = date.today() + timedelta(days=days)
        
        return self.db.query(Player).filter(
            Player.contract_end.isnot(None),
            Player.contract_end <= expiry_date,
            Player.is_active == True
        ).order_by(Player.contract_end.asc()).limit(limit).all()

    def get_free_agents(self, limit: int = 100) -> List[Player]:
        """Get players without active contracts (free agents)."""
        today = date.today()
        
        return self.db.query(Player).filter(
            or_(
                Player.contract_end.is_(None),
                Player.contract_end < today
            ),
            Player.status == PlayerStatus.ACTIVE,
            Player.is_active == True
        ).order_by(Player.last_name, Player.first_name).limit(limit).all()