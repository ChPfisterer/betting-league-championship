"""
Bet API schemas for the betting platform.

This module defines Pydantic schemas for bet management, including creation,
updates, responses, and various bet types. Bets are the core of the betting
platform where users place wagers on match outcomes.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class BetType(str, Enum):
    """Enumeration of bet types."""
    
    MATCH_WINNER = "match_winner"      # Bet on match winner
    TOTAL_GOALS = "total_goals"        # Over/under total goals
    HANDICAP = "handicap"              # Asian handicap betting
    BOTH_TEAMS_SCORE = "both_teams_score"  # Both teams to score
    FIRST_GOAL = "first_goal"          # First team to score
    CORRECT_SCORE = "correct_score"    # Exact score prediction
    DRAW_NO_BET = "draw_no_bet"        # Draw refunds stake
    DOUBLE_CHANCE = "double_chance"    # Two outcomes covered
    HALF_TIME = "half_time"            # Half-time result
    FULL_TIME = "full_time"            # Full-time result


class BetStatus(str, Enum):
    """Enumeration of bet statuses."""
    
    PENDING = "pending"        # Bet placed, waiting for match
    ACTIVE = "active"          # Match in progress
    WON = "won"               # Bet won
    LOST = "lost"             # Bet lost
    VOID = "void"             # Bet voided/cancelled
    PUSHED = "pushed"         # Bet tied/pushed (stake returned)
    CANCELLED = "cancelled"   # Bet cancelled before match


class BetOutcome(str, Enum):
    """Enumeration of bet outcomes for match winner bets."""
    
    HOME_WIN = "home_win"
    AWAY_WIN = "away_win"
    DRAW = "draw"


class BetBase(BaseModel):
    """Base prediction schema with common fields."""
    
    # Prediction specifics
    outcome: Optional[BetOutcome] = Field(None, description="Predicted outcome")
    
    # Score prediction (main prediction mechanism)
    predicted_home_score: Optional[int] = Field(None, ge=0, description="Predicted home score")
    predicted_away_score: Optional[int] = Field(None, ge=0, description="Predicted away score")
    
    # Points earned from prediction
    points_earned: int = Field(default=0, ge=0, le=3, description="Points earned (0, 1, or 3)")
    
    # Additional parameters
    notes: Optional[str] = Field(None, max_length=500, description="Prediction notes")

    @field_validator('outcome')
    @classmethod
    def validate_outcome_for_bet_type(cls, v: Optional[BetOutcome], info) -> Optional[BetOutcome]:
        """Validate outcome is provided for match winner predictions."""
        if 'bet_type' in info.data and info.data['bet_type'] == BetType.MATCH_WINNER:
            if v is None:
                raise ValueError('Outcome is required for match winner predictions')
        return v


class BetCreate(BetBase):
    """Schema for creating a new prediction."""
    
    match_id: UUID = Field(..., description="ID of the match to predict")
    group_id: Optional[UUID] = Field(None, description="ID of the group this prediction belongs to")

    @field_validator('match_id')
    @classmethod
    def validate_match_exists(cls, v: UUID) -> UUID:
        """Validate that the match exists and betting is allowed."""
        # Note: In a real implementation, this would check the database
        # For now, we'll just validate the UUID format
        return v


class BetUpdate(BaseModel):
    """Schema for updating an existing bet (limited fields)."""
    
    notes: Optional[str] = Field(None, max_length=500, description="Update bet notes")
    
    # Only allow updating notes before match starts
    # Other fields are immutable once bet is placed


class BetPatch(BaseModel):
    """Schema for partial bet updates (PATCH operations)."""
    
    status: Optional[BetStatus] = Field(None, description="Update bet status")
    notes: Optional[str] = Field(None, max_length=500, description="Update bet notes")


class BetResponse(BetBase):
    """Schema for prediction responses."""
    
    id: UUID = Field(..., description="Prediction unique identifier")
    user_id: UUID = Field(..., description="User who made the prediction")
    match_id: UUID = Field(..., description="Match this prediction is for")
    group_id: Optional[UUID] = Field(None, description="Group this prediction belongs to")
    
    status: BetStatus = Field(..., description="Current prediction status")
    
    # Settlement details
    settled_at: Optional[datetime] = Field(None, description="When prediction was settled")
    settlement_reason: Optional[str] = Field(None, description="Reason for settlement")
    
    # Metadata
    placed_at: datetime = Field(..., description="When prediction was placed")
    created_at: datetime = Field(..., description="Prediction creation timestamp")
    updated_at: datetime = Field(..., description="Prediction last update timestamp")
    is_active: bool = Field(..., description="Whether prediction is active")

    class Config:
        from_attributes = True


class BetSummary(BaseModel):
    """Lightweight prediction schema for lists and references."""
    
    id: UUID = Field(..., description="Prediction unique identifier")
    user_id: UUID = Field(..., description="User who made the prediction")
    match_id: UUID = Field(..., description="Match this prediction is for")
    predicted_home_score: Optional[int] = Field(None, description="Predicted home score")
    predicted_away_score: Optional[int] = Field(None, description="Predicted away score")
    points_earned: int = Field(..., description="Points earned from prediction")
    status: BetStatus = Field(..., description="Current prediction status")
    placed_at: datetime = Field(..., description="When prediction was placed")
    is_active: bool = Field(..., description="Whether prediction is active")

    class Config:
        from_attributes = True


class BetWithMatch(BetResponse):
    """Bet response with match details."""
    
    match: dict = Field(..., description="Match details")

    class Config:
        from_attributes = True


class BetWithUser(BetResponse):
    """Bet response with user details."""
    
    user: dict = Field(..., description="User details")

    class Config:
        from_attributes = True


class BetStatistics(BaseModel):
    """Simple prediction statistics schema aligned with specification."""
    
    total_predictions: int = Field(..., description="Total number of predictions")
    total_points: int = Field(..., description="Total points earned")
    exact_score_predictions: int = Field(..., description="Number of exact score predictions (3 points each)")
    winner_only_predictions: int = Field(..., description="Number of winner-only predictions (1 point each)")
    wrong_predictions: int = Field(..., description="Number of incorrect predictions (0 points)")
    accuracy_percentage: float = Field(..., ge=0, le=100, description="Overall accuracy percentage")
    average_points_per_prediction: float = Field(..., description="Average points per prediction")

    class Config:
        from_attributes = True


class BetWithStats(BetResponse):
    """Bet response with statistics."""
    
    stats: BetStatistics = Field(..., description="Prediction statistics")

    class Config:
        from_attributes = True


class BetHistory(BaseModel):
    """Bet history schema."""
    
    user_id: UUID = Field(..., description="User ID")
    bets: List[BetSummary] = Field(..., description="List of user bets")
    summary_stats: BetStatistics = Field(..., description="Summary prediction statistics")
    last_updated: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class BetSettlement(BaseModel):
    """Prediction settlement schema."""
    
    bet_id: UUID = Field(..., description="Prediction ID")
    status: BetStatus = Field(..., description="Settlement status")
    points_awarded: int = Field(..., description="Points awarded for prediction")
    settlement_reason: str = Field(..., description="Reason for settlement")
    settled_by: UUID = Field(..., description="User who settled the prediction")

    class Config:
        from_attributes = True


class BetSlip(BaseModel):
    """Prediction slip schema for multiple predictions."""
    
    user_id: UUID = Field(..., description="User placing the bets")
    bets: List[BetCreate] = Field(..., min_length=1, description="List of bets to place")
    total_stake: float = Field(..., gt=0, description="Total stake amount")
    potential_return: float = Field(..., gt=0, description="Potential total return")
    slip_type: str = Field("single", description="Type of bet slip (single, accumulator, etc.)")

    @field_validator('total_stake')
    @classmethod
    def validate_total_stake(cls, v: float, info) -> float:
        """Validate total stake matches sum of individual bet amounts."""
        if 'bets' in info.data:
            expected_total = sum(bet.amount for bet in info.data['bets'])
            if abs(v - expected_total) > 0.01:
                raise ValueError('Total stake must equal sum of individual bet amounts')
        return v

    class Config:
        from_attributes = True


class BetLeaderboard(BaseModel):
    """Bet leaderboard schema."""
    
    group_id: Optional[UUID] = Field(None, description="Group ID (if group-specific)")
    period: str = Field(..., description="Leaderboard period")
    
    entries: List[dict] = Field(..., description="Leaderboard entries")
    last_updated: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


    class Config:
        from_attributes = True