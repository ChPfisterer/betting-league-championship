"""
Prediction service for the prediction contest system.

This service implements the specification-compliant prediction system:
- 1 point for correct winner predictions
- 3 points total (1 + 2 bonus) for exact score predictions
- Group-based predictions with deadline management
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc

from models.bet import Bet
from models.user import User
from models.match import Match
from models.group import Group
from models.result import Result
from api.schemas.prediction import (
    PredictionCreate, PredictionUpdate, PredictionResponse,
    PredictedWinner, PredictionStatus, UserPredictionStats,
    GroupPredictionStats
)


class PredictionService:
    """Service class for prediction management operations."""
    
    def __init__(self, db: Session):
        self.db = db

    def create_prediction(self, prediction_data: PredictionCreate, user_id: UUID) -> Bet:
        """
        Create a new prediction following specification rules.
        
        Args:
            prediction_data: Prediction creation data
            user_id: User making the prediction
            
        Returns:
            Created prediction (Bet object)
            
        Raises:
            ValueError: If prediction violates business rules
        """
        # Validate match exists and is not started
        match = self.db.query(Match).filter(Match.id == prediction_data.match_id).first()
        if not match:
            raise ValueError(f"Match with ID {prediction_data.match_id} not found")
        
        # Check if prediction deadline has passed
        if self._is_past_deadline(match):
            raise ValueError("Prediction deadline has passed for this match")
        
        # Validate group exists and user is a member
        if not self._validate_group_membership(user_id, prediction_data.group_id):
            raise ValueError("User is not a member of the specified group")
        
        # Check for existing prediction (spec allows overwriting before deadline)
        existing = self.db.query(Bet).filter(
            and_(
                Bet.user_id == user_id,
                Bet.match_id == prediction_data.match_id,
                Bet.group_id == prediction_data.group_id
            )
        ).first()
        
        if existing:
            # Update existing prediction before deadline
            return self._update_existing_prediction(existing, prediction_data)
        
        # Create new prediction using the existing Bet model structure
        # but with spec-compliant fields
        prediction = Bet(
            user_id=user_id,
            match_id=prediction_data.match_id,
            group_id=prediction_data.group_id,
            predicted_winner=prediction_data.predicted_winner.value,
            predicted_home_score=prediction_data.predicted_home_score,
            predicted_away_score=prediction_data.predicted_away_score,
            points_earned=0,  # Will be calculated after match
            is_processed=False,
            status="pending",
            placed_at=datetime.now(timezone.utc),
            
            # Keep required fields from original model for compatibility
            bet_type="prediction",  # Use existing field
            market_type="match_winner_and_score",  # Use existing field
            stake_amount=0,  # Not used in spec but required by model
            odds=1.0,        # Not used in spec but required by model
            potential_payout=0,  # Not used in spec but required by model
        )
        
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        
        return prediction

    def process_match_predictions(self, match_id: UUID) -> Dict[str, Any]:
        """
        Process all predictions for a completed match and award points.
        
        Implementation of specification scoring rules:
        - 1 point for correct winner prediction
        - 3 points total (1 + 2 bonus) for exact score prediction
        
        Args:
            match_id: Match to process
            
        Returns:
            Processing summary with statistics
        """
        # Get match and its result
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError(f"Match with ID {match_id} not found")
        
        result = self.db.query(Result).filter(Result.match_id == match_id).first()
        if not result or result.home_score is None or result.away_score is None:
            raise ValueError("Match result not available")
        
        # Get all unprocessed predictions for this match
        predictions = self.db.query(Bet).filter(
            and_(
                Bet.match_id == match_id,
                Bet.is_processed == False,
                Bet.group_id.isnot(None)  # Only process group predictions
            )
        ).all()
        
        processing_stats = {
            "match_id": match_id,
            "total_predictions": len(predictions),
            "exact_score_predictions": 0,
            "winner_predictions": 0,
            "incorrect_predictions": 0,
            "total_points_awarded": 0
        }
        
        for prediction in predictions:
            points = self._calculate_prediction_points(prediction, result)
            
            # Update prediction with calculated points
            prediction.points_earned = points
            prediction.is_processed = True
            prediction.status = "processed"
            
            # Update statistics
            processing_stats["total_points_awarded"] += points
            if points == 3:
                processing_stats["exact_score_predictions"] += 1
            elif points == 1:
                processing_stats["winner_predictions"] += 1
            else:
                processing_stats["incorrect_predictions"] += 1
        
        self.db.commit()
        return processing_stats

    def get_user_predictions(self, user_id: UUID, group_id: Optional[UUID] = None, 
                           limit: int = 50) -> List[PredictionResponse]:
        """Get user's predictions with optional group filtering."""
        query = self.db.query(Bet).filter(
            and_(
                Bet.user_id == user_id,
                Bet.group_id.isnot(None)  # Only group predictions
            )
        )
        
        if group_id:
            query = query.filter(Bet.group_id == group_id)
        
        predictions = query.order_by(desc(Bet.placed_at)).limit(limit).all()
        
        return [self._to_prediction_response(pred) for pred in predictions]

    def get_group_leaderboard(self, group_id: UUID, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get group leaderboard based on prediction points.
        
        Implements specification tiebreaker rules:
        total points → exact score predictions → correct winner predictions → registration date
        """
        # Query to get user statistics in the group
        leaderboard_query = self.db.query(
            User.id,
            User.username,
            User.first_name,
            User.last_name,
            User.created_at.label('registration_date'),
            func.sum(Bet.points_earned).label('total_points'),
            func.count(Bet.id).label('total_predictions'),
            func.sum(func.case([(Bet.points_earned == 3, 1)], else_=0)).label('exact_score_count'),
            func.sum(func.case([(Bet.points_earned == 1, 1)], else_=0)).label('winner_count'),
        ).join(
            Bet, Bet.user_id == User.id
        ).filter(
            and_(
                Bet.group_id == group_id,
                Bet.is_processed == True
            )
        ).group_by(
            User.id, User.username, User.first_name, User.last_name, User.created_at
        ).order_by(
            desc('total_points'),
            desc('exact_score_count'),
            desc('winner_count'),
            User.created_at  # Earlier registration for final tiebreaker
        ).limit(limit)
        
        results = leaderboard_query.all()
        
        leaderboard = []
        for rank, result in enumerate(results, 1):
            leaderboard.append({
                "rank": rank,
                "user_id": result.id,
                "username": result.username,
                "display_name": f"{result.first_name} {result.last_name}".strip() or result.username,
                "total_points": result.total_points or 0,
                "total_predictions": result.total_predictions or 0,
                "exact_score_predictions": result.exact_score_count or 0,
                "winner_predictions": result.winner_count or 0,
                "registration_date": result.registration_date
            })
        
        return leaderboard

    def get_user_stats(self, user_id: UUID, group_id: Optional[UUID] = None) -> UserPredictionStats:
        """Get comprehensive user prediction statistics."""
        query = self.db.query(Bet).filter(
            and_(
                Bet.user_id == user_id,
                Bet.group_id.isnot(None),
                Bet.is_processed == True
            )
        )
        
        if group_id:
            query = query.filter(Bet.group_id == group_id)
        
        predictions = query.all()
        
        total_predictions = len(predictions)
        total_points = sum(p.points_earned for p in predictions)
        exact_score_count = sum(1 for p in predictions if p.points_earned == 3)
        winner_only_count = sum(1 for p in predictions if p.points_earned == 1)
        wrong_predictions = sum(1 for p in predictions if p.points_earned == 0)
        
        win_rate = ((exact_score_count + winner_only_count) / total_predictions * 100) if total_predictions > 0 else 0
        average_points = (total_points / total_predictions) if total_predictions > 0 else 0
        
        return UserPredictionStats(
            user_id=user_id,
            total_predictions=total_predictions,
            total_points=total_points,
            exact_score_count=exact_score_count,
            winner_only_count=winner_only_count,
            wrong_predictions=wrong_predictions,
            win_rate=round(win_rate, 1),
            average_points=round(average_points, 2)
        )

    def _calculate_prediction_points(self, prediction: Bet, result: Result) -> int:
        """
        Calculate points according to specification rules.
        
        Returns:
            3 points for exact score match
            1 point for correct winner only
            0 points for incorrect prediction
        """
        home_score = result.home_score
        away_score = result.away_score
        
        # Check for exact score match (3 points total)
        if (prediction.predicted_home_score == home_score and 
            prediction.predicted_away_score == away_score):
            return 3
        
        # Check for correct winner (1 point)
        actual_winner = self._determine_winner(home_score, away_score)
        if prediction.predicted_winner == actual_winner:
            return 1
        
        # Incorrect prediction (0 points)
        return 0

    def _determine_winner(self, home_score: int, away_score: int) -> str:
        """Determine match winner from scores."""
        if home_score > away_score:
            return "HOME"
        elif away_score > home_score:
            return "AWAY"
        else:
            return "DRAW"

    def _is_past_deadline(self, match: Match) -> bool:
        """Check if prediction deadline has passed for a match."""
        # Default deadline: 1 hour before match start (as per spec)
        default_deadline = match.scheduled_at - timedelta(hours=1)
        
        # TODO: Check for group-specific deadline overrides
        # Group admins can set custom deadlines per spec
        
        return datetime.now(timezone.utc) > default_deadline

    def _validate_group_membership(self, user_id: UUID, group_id: UUID) -> bool:
        """Validate that user is a member of the specified group."""
        # TODO: Implement group membership validation
        # For now, return True - should be implemented with GroupMembership model
        return True

    def _update_existing_prediction(self, existing: Bet, prediction_data: PredictionCreate) -> Bet:
        """Update existing prediction before deadline."""
        existing.predicted_winner = prediction_data.predicted_winner.value
        existing.predicted_home_score = prediction_data.predicted_home_score
        existing.predicted_away_score = prediction_data.predicted_away_score
        existing.placed_at = datetime.now(timezone.utc)  # Update timestamp
        
        self.db.commit()
        self.db.refresh(existing)
        return existing

    def _to_prediction_response(self, prediction: Bet) -> PredictionResponse:
        """Convert Bet model to PredictionResponse."""
        return PredictionResponse(
            id=prediction.id,
            user_id=prediction.user_id,
            group_id=prediction.group_id,
            match_id=prediction.match_id,
            predicted_winner=PredictedWinner(prediction.predicted_winner),
            predicted_home_score=prediction.predicted_home_score,
            predicted_away_score=prediction.predicted_away_score,
            points_earned=prediction.points_earned,
            is_processed=prediction.is_processed,
            status=PredictionStatus(prediction.status),
            placed_at=prediction.placed_at,
            processed_at=getattr(prediction, 'processed_at', None)
        )