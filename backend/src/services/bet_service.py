"""
Bet service for the betting platform.

This service provides comprehensive business logic for bet management,
including bet placement, validation, settlement, statistics calculation,
and odds management. Handles all betting-related operations with proper
validation and error handling.
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc

from models import Bet, User, Match, Group
from models.bet import BetType as ModelBetType, BetStatus, MarketType
from api.schemas.bet import (
    BetCreate,
    BetUpdate,
    BetSettlement,
    BetType as SchemaBetType,
    BetOutcome,
    BetStatus as SchemaBetStatus
)


class BetService:
    """Service class for bet management operations."""
    
    def __init__(self, db: Session):
        """Initialize the bet service with database session."""
        self.db = db
    
    def create_bet(self, bet_data: BetCreate, user_id: UUID) -> Bet:
        """
        Create a new bet with comprehensive validation.
        
        Args:
            bet_data: Bet creation data
            user_id: ID of user placing the bet
            
        Returns:
            Created bet instance
            
        Raises:
            ValueError: If validation fails
        """
        # Validate user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Validate match exists and betting is allowed
        match = self.db.query(Match).filter(Match.id == bet_data.match_id).first()
        if not match:
            raise ValueError(f"Match with ID {bet_data.match_id} not found")
        
        # Check if betting is allowed using the model's method
        can_bet, bet_message = match.can_place_bet()
        if not can_bet:
            raise ValueError(bet_message)
        
        # For prediction contest, validate that either outcome or scores are provided
        if not bet_data.outcome and (bet_data.predicted_home_score is None or bet_data.predicted_away_score is None):
            raise ValueError("Either outcome prediction or exact score prediction is required")
        
        # Create bet instance for prediction contest
        bet = Bet(
            user_id=user_id,
            match_id=bet_data.match_id,
            bet_type=ModelBetType.SINGLE.value,  # Default to single bet
            market_type=MarketType.MATCH_WINNER.value,  # Default to match winner for predictions
            predicted_home_score=bet_data.predicted_home_score,
            predicted_away_score=bet_data.predicted_away_score,
            points_earned=0,  # Will be calculated when match is settled
            selection=bet_data.outcome.value if bet_data.outcome else None,
            notes=bet_data.notes,
            status=BetStatus.PENDING.value,
            placed_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc)
        )
        
        self.db.add(bet)
        self.db.commit()
        self.db.refresh(bet)
        
        return bet
    
    def _validate_bet_type_requirements(self, bet_data: BetCreate) -> None:
        """Validate bet type specific requirements."""
        if bet_data.bet_type == SchemaBetType.MATCH_WINNER:
            if not bet_data.outcome:
                raise ValueError("Outcome is required for match winner bets")
        
        elif bet_data.bet_type == SchemaBetType.TOTAL_GOALS:
            if bet_data.total_value is None or bet_data.is_over is None:
                raise ValueError("Total value and over/under selection are required for total goals bets")
        
        elif bet_data.bet_type == SchemaBetType.HANDICAP:
            if bet_data.handicap_value is None:
                raise ValueError("Handicap value is required for handicap bets")
            if not bet_data.outcome:
                raise ValueError("Outcome is required for handicap bets")
        
        elif bet_data.bet_type == SchemaBetType.CORRECT_SCORE:
            if bet_data.predicted_home_score is None or bet_data.predicted_away_score is None:
                raise ValueError("Both home and away score predictions are required for correct score bets")
    
    def _map_market_type_to_schema_bet_type(self, market_type: str) -> SchemaBetType:
        """Map model MarketType back to schema BetType."""
        mapping = {
            MarketType.MATCH_WINNER.value: SchemaBetType.MATCH_WINNER,
            MarketType.OVER_UNDER.value: SchemaBetType.TOTAL_GOALS,
            MarketType.HANDICAP.value: SchemaBetType.HANDICAP,
            # Add more mappings as needed
        }
        return mapping.get(market_type, SchemaBetType.MATCH_WINNER)  # Default fallback
    
    def _map_model_status_to_schema_status(self, model_status: str) -> SchemaBetStatus:
        """Map model BetStatus to schema BetStatus."""
        # Both should have similar values, but let's be explicit
        mapping = {
            BetStatus.PENDING.value: SchemaBetStatus.PENDING,
            BetStatus.WON.value: SchemaBetStatus.WON,
            BetStatus.LOST.value: SchemaBetStatus.LOST,
            BetStatus.VOID.value: SchemaBetStatus.VOID,
            BetStatus.CANCELLED.value: SchemaBetStatus.CANCELLED,
            # Add more mappings as needed
        }
        return mapping.get(model_status, SchemaBetStatus.PENDING)  # Default fallback
    
    def transform_bet_for_response(self, bet: Bet) -> dict:
        """Transform model Bet to response schema compatible format."""
        try:
            return {
                "id": bet.id,
                "user_id": bet.user_id,
                "match_id": bet.match_id,
                "group_id": getattr(bet, 'group_id', None),
                "outcome": bet.selection,  # outcome is stored in selection field
                "predicted_home_score": bet.predicted_home_score,
                "predicted_away_score": bet.predicted_away_score,
                "points_earned": bet.points_earned,
                "notes": bet.notes,
                "status": self._map_model_status_to_schema_status(bet.status),
                "placed_at": bet.placed_at,
                "created_at": bet.created_at,
                "updated_at": bet.updated_at if hasattr(bet, 'updated_at') and bet.updated_at else bet.created_at,
                "is_active": bet.is_active  # This is a property method
            }
        except Exception as e:
            # Log the error and provide meaningful feedback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error transforming bet {bet.id}: {e}")
            raise ValueError(f"Failed to transform bet data: {e}")
    
    def get_bet(self, bet_id: UUID) -> Optional[Bet]:
        """Get bet by ID."""
        return self.db.query(Bet).filter(
            Bet.id == bet_id,
            Bet.is_active == True
        ).first()
    
    def list_bets(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[UUID] = None,
        match_id: Optional[UUID] = None,
        group_id: Optional[UUID] = None,
        bet_type: Optional[ModelBetType] = None,
        status: Optional[BetStatus] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> List[Bet]:
        """
        List bets with filtering options.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            user_id: Filter by user ID
            match_id: Filter by match ID
            group_id: Filter by group ID
            bet_type: Filter by bet type
            status: Filter by bet status
            date_from: Filter bets from this date
            date_to: Filter bets until this date
            
        Returns:
            List of bets matching criteria
        """
        query = self.db.query(Bet).filter(Bet.is_active == True)
        
        if user_id:
            query = query.filter(Bet.user_id == user_id)
        
        if match_id:
            query = query.filter(Bet.match_id == match_id)
        
        if group_id:
            query = query.filter(Bet.group_id == group_id)
        
        if bet_type:
            query = query.filter(Bet.bet_type == bet_type)
        
        if status:
            query = query.filter(Bet.status == status)
        
        if date_from:
            query = query.filter(Bet.placed_at >= date_from)
        
        if date_to:
            query = query.filter(Bet.placed_at <= date_to)
        
        return query.order_by(desc(Bet.placed_at)).offset(skip).limit(limit).all()
    
    def update_bet(self, bet_id: UUID, update_data: BetUpdate) -> Optional[Bet]:
        """
        Update bet (limited fields only).
        
        Args:
            bet_id: Bet unique identifier
            update_data: Update data
            
        Returns:
            Updated bet or None if not found
        """
        bet = self.get_bet(bet_id)
        if not bet:
            return None
        
        # Check if bet can still be updated
        if bet.status not in [BetStatus.PENDING]:
            raise ValueError("Can only update pending bets")
        
        # Check if match has started
        match = self.db.query(Match).filter(Match.id == bet.match_id).first()
        if match and match.started_at:
            raise ValueError("Cannot update bet after match has started")
        
        # Update allowed fields
        if update_data.notes is not None:
            bet.notes = update_data.notes
        
        bet.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(bet)
        
        return bet
    
    def settle_bet(self, bet_id: UUID, settlement: BetSettlement) -> Optional[Bet]:
        """
        Settle a bet based on match results.
        
        Args:
            bet_id: Bet unique identifier
            settlement: Settlement details
            
        Returns:
            Settled bet or None if not found
        """
        bet = self.get_bet(bet_id)
        if not bet:
            return None
        
        if bet.status not in [BetStatus.PENDING, BetStatus.ACTIVE]:
            raise ValueError("Can only settle pending or active bets")
        
        # Update bet with settlement
        bet.status = settlement.status
        bet.actual_payout = settlement.actual_payout
        bet.settlement_reason = settlement.settlement_reason
        bet.settled_at = datetime.utcnow()
        bet.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(bet)
        
        return bet
    
    def delete_bet(self, bet_id: UUID) -> bool:
        """
        Delete (soft delete) a bet.
        
        Args:
            bet_id: Bet unique identifier
            
        Returns:
            True if deleted successfully, False if not found
        """
        bet = self.get_bet(bet_id)
        if not bet:
            return False
        
        # Check if bet can be deleted
        if bet.status not in [BetStatus.PENDING]:
            raise ValueError("Can only delete pending bets")
        
        # Check if match has started
        match = self.db.query(Match).filter(Match.id == bet.match_id).first()
        if match and match.started_at:
            raise ValueError("Cannot delete bet after match has started")
        
        bet.is_active = False
        bet.status = BetStatus.CANCELLED
        bet.updated_at = datetime.utcnow()
        
        self.db.commit()
        
        return True
    
    def get_user_bets(self, user_id: UUID, limit: int = 100) -> List[Bet]:
        """Get all bets for a specific user."""
        return self.db.query(Bet).filter(
            Bet.user_id == user_id,
            Bet.is_active == True
        ).order_by(desc(Bet.placed_at)).limit(limit).all()
    
    def get_match_bets(self, match_id: UUID, limit: int = 100) -> List[Bet]:
        """Get all bets for a specific match."""
        return self.db.query(Bet).filter(
            Bet.match_id == match_id,
            Bet.is_active == True
        ).order_by(desc(Bet.placed_at)).limit(limit).all()
    
    def get_group_bets(self, group_id: UUID, limit: int = 100) -> List[Bet]:
        """Get all bets for a specific group."""
        return self.db.query(Bet).filter(
            Bet.group_id == group_id,
            Bet.is_active == True
        ).order_by(desc(Bet.placed_at)).limit(limit).all()
    
    def get_pending_bets(self, limit: int = 100) -> List[Bet]:
        """Get all pending bets."""
        return self.db.query(Bet).filter(
            Bet.status == BetStatus.PENDING,
            Bet.is_active == True
        ).order_by(desc(Bet.placed_at)).limit(limit).all()
    
    def get_active_bets(self, limit: int = 100) -> List[Bet]:
        """Get all active bets (matches in progress)."""
        return self.db.query(Bet).filter(
            Bet.status == BetStatus.ACTIVE,
            Bet.is_active == True
        ).order_by(desc(Bet.placed_at)).limit(limit).all()
    
    def get_user_statistics(self, user_id: UUID) -> Dict[str, Any]:
        """
        Get comprehensive prediction contest statistics for a user.
        
        Args:
            user_id: User unique identifier
            
        Returns:
            Dictionary with prediction contest statistics
        """
        user_bets = self.db.query(Bet).filter(
            Bet.user_id == user_id,
            Bet.is_active == True
        ).all()
        
        if not user_bets:
            return {
                "total_predictions": 0,
                "total_points": 0,
                "win_rate": 0.0,
                "average_points": 0.0
            }
        
        total_predictions = len(user_bets)
        total_points = sum(bet.points_earned for bet in user_bets)
        
        won_bets = [bet for bet in user_bets if bet.points_earned > 0]
        lost_bets = [bet for bet in user_bets if bet.points_earned == 0 and bet.status in [BetStatus.WON.value, BetStatus.LOST.value]]
        pending_bets = [bet for bet in user_bets if bet.status == BetStatus.PENDING.value]
        
        settled_bets = won_bets + lost_bets
        win_rate = (len(won_bets) / len(settled_bets) * 100) if settled_bets else 0
        
        average_points = total_points / total_predictions if total_predictions > 0 else 0
        
        return {
            "total_predictions": total_predictions,
            "total_points": total_points,
            "exact_score_predictions": len([bet for bet in user_bets if bet.points_earned == 3]),
            "winner_only_predictions": len([bet for bet in user_bets if bet.points_earned == 1]),
            "wrong_predictions": len([bet for bet in user_bets if bet.points_earned == 0 and bet.status in [BetStatus.WON.value, BetStatus.LOST.value]]),
            "pending_predictions": len(pending_bets),
            "win_rate": win_rate,
            "average_points_per_prediction": average_points
        }
    
    def get_match_statistics(self, match_id: UUID) -> Dict[str, Any]:
        """
        Get betting statistics for a specific match.
        
        Args:
            match_id: Match unique identifier
            
        Returns:
            Dictionary with match betting statistics
        """
        match_bets = self.db.query(Bet).filter(
            Bet.match_id == match_id,
            Bet.is_active == True
        ).all()
        
        if not match_bets:
            return {
                "total_bets": 0,
                "total_amount": 0.0,
                "unique_bettors": 0,
                "bet_type_distribution": {}
            }
        
        total_bets = len(match_bets)
        total_amount = sum(bet.amount for bet in match_bets)
        unique_bettors = len(set(bet.user_id for bet in match_bets))
        
        # Bet type distribution
        bet_type_distribution = {}
        outcome_distribution = {}
        
        for bet in match_bets:
            # Bet type stats
            bet_type = bet.bet_type
            if bet_type not in bet_type_distribution:
                bet_type_distribution[bet_type] = {"count": 0, "amount": 0.0}
            bet_type_distribution[bet_type]["count"] += 1
            bet_type_distribution[bet_type]["amount"] += bet.amount
            
            # Outcome distribution for match winner bets
            if bet.market_type == MarketType.MATCH_WINNER and bet.selection:
                outcome = bet.selection
                if outcome not in outcome_distribution:
                    outcome_distribution[outcome] = {"count": 0, "amount": 0.0}
                outcome_distribution[outcome]["count"] += 1
                outcome_distribution[outcome]["amount"] += bet.amount
        
        return {
            "total_bets": total_bets,
            "total_amount": total_amount,
            "unique_bettors": unique_bettors,
            "average_bet_size": total_amount / total_bets,
            "bet_type_distribution": bet_type_distribution,
            "outcome_distribution": outcome_distribution
        }
    
    def auto_settle_match_bets(self, match_id: UUID) -> int:
        """
        Automatically settle bets for a completed match.
        
        Args:
            match_id: Match unique identifier
            
        Returns:
            Number of bets settled
        """
        # Get match details
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match or not match.finished_at:
            return 0
        
        # Get all pending/active bets for this match
        bets_to_settle = self.db.query(Bet).filter(
            Bet.match_id == match_id,
            Bet.status.in_([BetStatus.PENDING, BetStatus.ACTIVE]),
            Bet.is_active == True
        ).all()
        
        settled_count = 0
        
        for bet in bets_to_settle:
            try:
                # Determine bet outcome based on match result
                bet_won = self._evaluate_bet_outcome(bet, match)
                
                if bet_won is None:
                    # Void bet (e.g., match cancelled)
                    bet.status = BetStatus.VOID
                    bet.actual_payout = bet.amount  # Return stake
                    bet.settlement_reason = "Match voided"
                elif bet_won:
                    # Bet won
                    bet.status = BetStatus.WON
                    bet.actual_payout = bet.potential_payout
                    bet.settlement_reason = "Bet won"
                else:
                    # Bet lost
                    bet.status = BetStatus.LOST
                    bet.actual_payout = 0.0
                    bet.settlement_reason = "Bet lost"
                
                bet.settled_at = datetime.utcnow()
                bet.updated_at = datetime.utcnow()
                settled_count += 1
                
            except Exception as e:
                # Log error and continue with other bets
                print(f"Error settling bet {bet.id}: {e}")
                continue
        
        self.db.commit()
        return settled_count
    
    def _evaluate_bet_outcome(self, bet: Bet, match: Match) -> Optional[bool]:
        """
        Evaluate whether a bet won based on match results.
        
        Args:
            bet: Bet to evaluate
            match: Completed match
            
        Returns:
            True if bet won, False if lost, None if void
        """
        if not match.home_score is not None or match.away_score is None:
            return None  # No valid score
        
        home_score = match.home_score
        away_score = match.away_score
        
        if bet.market_type == MarketType.MATCH_WINNER:
            if bet.selection == BetOutcome.HOME_WIN.value:
                return home_score > away_score
            elif bet.selection == BetOutcome.AWAY_WIN.value:
                return away_score > home_score
            elif bet.selection == BetOutcome.DRAW.value:
                return home_score == away_score
        
        elif bet.market_type == MarketType.OVER_UNDER:
            total_goals = home_score + away_score
            if bet.is_over:
                return total_goals > bet.total_value
            else:
                return total_goals < bet.total_value
        
        elif bet.market_type == MarketType.MATCH_WINNER:  # For correct score, we'll need a separate market type
            return (home_score == bet.predicted_home_score and 
                   away_score == bet.predicted_away_score)
        
        # Add more market type evaluations as needed
        # For unsupported market types, return None (void)
        return None
    
    def search_bets(self, query: str, limit: int = 100) -> List[Bet]:
        """
        Search bets by notes or settlement reason.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching bets
        """
        return self.db.query(Bet).filter(
            and_(
                Bet.is_active == True,
                or_(
                    Bet.notes.ilike(f"%{query}%"),
                    Bet.settlement_reason.ilike(f"%{query}%")
                )
            )
        ).order_by(desc(Bet.placed_at)).limit(limit).all()