"""
Prediction-based bet schemas aligned with specification.

This module defines the new prediction contest system schemas
as specified in the requirements.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class PredictedWinner(str, Enum):
    """Enumeration of prediction outcomes."""
    HOME = "HOME"
    AWAY = "AWAY"
    DRAW = "DRAW"


class PredictionStatus(str, Enum):
    """Enumeration of prediction statuses."""
    PENDING = "pending"        # Prediction placed, waiting for match
    PROCESSED = "processed"    # Match completed, points calculated
    VOIDED = "voided"         # Prediction voided (match cancelled)


class PredictionBase(BaseModel):
    """Base prediction schema with common fields."""
    
    group_id: UUID = Field(..., description="Group ID where prediction is made")
    match_id: UUID = Field(..., description="Match ID being predicted")
    predicted_winner: PredictedWinner = Field(..., description="Predicted match winner")
    predicted_home_score: int = Field(..., ge=0, description="Predicted home team score")
    predicted_away_score: int = Field(..., ge=0, description="Predicted away team score")

    @field_validator('predicted_home_score', 'predicted_away_score')
    @classmethod
    def validate_scores(cls, v):
        if v < 0:
            raise ValueError('Scores must be non-negative')
        if v > 20:  # Reasonable upper limit
            raise ValueError('Score seems unrealistic')
        return v


class PredictionCreate(PredictionBase):
    """Schema for creating new predictions."""
    pass


class PredictionUpdate(BaseModel):
    """Schema for updating predictions (before deadline)."""
    
    predicted_winner: Optional[PredictedWinner] = None
    predicted_home_score: Optional[int] = Field(None, ge=0)
    predicted_away_score: Optional[int] = Field(None, ge=0)


class PredictionResponse(PredictionBase):
    """Schema for prediction responses."""
    
    id: UUID = Field(..., description="Prediction ID")
    user_id: UUID = Field(..., description="User who made the prediction")
    points_earned: int = Field(..., description="Points earned (0, 1, or 3)")
    is_processed: bool = Field(..., description="Whether points have been calculated")
    status: PredictionStatus = Field(..., description="Prediction status")
    placed_at: datetime = Field(..., description="When prediction was placed")
    processed_at: Optional[datetime] = Field(None, description="When points were calculated")
    
    # Match information for convenience
    match_details: Optional[dict] = Field(None, description="Match information")
    group_details: Optional[dict] = Field(None, description="Group information")

    class Config:
        from_attributes = True


class PredictionSummary(BaseModel):
    """Summary schema for prediction statistics."""
    
    id: UUID
    match_id: UUID
    predicted_winner: PredictedWinner
    predicted_score: str  # "2-1" format
    points_earned: int
    placed_at: datetime
    
    class Config:
        from_attributes = True


class GroupPredictionStats(BaseModel):
    """Group prediction statistics schema."""
    
    group_id: UUID
    total_predictions: int = Field(..., description="Total predictions in group")
    processed_predictions: int = Field(..., description="Predictions with calculated points")
    total_points_awarded: int = Field(..., description="Total points awarded in group")
    average_points_per_prediction: float = Field(..., description="Average points per prediction")
    exact_score_predictions: int = Field(..., description="Number of exact score predictions")
    winner_only_predictions: int = Field(..., description="Number of winner-only predictions")
    
    class Config:
        from_attributes = True


class UserPredictionStats(BaseModel):
    """User prediction statistics schema."""
    
    user_id: UUID
    total_predictions: int = Field(..., description="Total predictions made")
    total_points: int = Field(..., description="Total points earned")
    exact_score_count: int = Field(..., description="Exact score predictions")
    winner_only_count: int = Field(..., description="Winner-only correct predictions") 
    wrong_predictions: int = Field(..., description="Incorrect predictions")
    win_rate: float = Field(..., description="Percentage of correct predictions")
    average_points: float = Field(..., description="Average points per prediction")
    
    class Config:
        from_attributes = True


class PredictionDeadline(BaseModel):
    """Schema for betting deadline information."""
    
    match_id: UUID
    deadline: datetime = Field(..., description="Prediction deadline")
    is_open: bool = Field(..., description="Whether predictions are still accepted")
    time_remaining: Optional[str] = Field(None, description="Human readable time remaining")
    
    class Config:
        from_attributes = True