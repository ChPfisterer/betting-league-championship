"""
Prediction API endpoints implementing the specification-compliant prediction contest system.

This module replaces the traditional betting endpoints with simple prediction endpoints:
- Create/update predictions (winner + exact score)
- Points-based scoring (1 point winner, 3 points exact score)
- Group-based prediction contests
- Deadline management
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.keycloak_security import get_current_user_hybrid
from services.prediction_service import PredictionService
from api.schemas.prediction import (
    PredictionCreate, PredictionUpdate, PredictionResponse,
    UserPredictionStats, GroupPredictionStats
)
from models.user import User


router = APIRouter(tags=["predictions"])


@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def create_prediction(
    prediction_data: PredictionCreate,
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Create a new prediction for a match within a group.
    
    Implementation of specification rules:
    - Users can predict winner and exact final score
    - Predictions must be made before deadline (default: 1 hour before match)
    - Only one prediction per user per match per group
    - Existing predictions can be updated before deadline
    """
    try:
        service = PredictionService(db)
        prediction = service.create_prediction(prediction_data, current_user.id)
        return service._to_prediction_response(prediction)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create prediction"
        )


@router.get("/my-predictions", response_model=List[PredictionResponse])
async def get_my_predictions(
    group_id: Optional[UUID] = Query(None, description="Filter by group ID"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of predictions to return"),
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Get current user's predictions with optional group filtering.
    
    Returns predictions ordered by most recent first.
    """
    service = PredictionService(db)
    predictions = service.get_user_predictions(current_user.id, group_id, limit)
    return predictions


@router.get("/stats/user", response_model=UserPredictionStats)
async def get_user_prediction_stats(
    group_id: Optional[UUID] = Query(None, description="Filter stats by group ID"),
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive prediction statistics for current user.
    
    Includes total points, win rates, exact score predictions, etc.
    Can be filtered by specific group.
    """
    service = PredictionService(db)
    stats = service.get_user_stats(current_user.id, group_id)
    return stats


@router.get("/leaderboard/{group_id}")
async def get_group_leaderboard(
    group_id: UUID,
    limit: int = Query(50, ge=1, le=100, description="Maximum number of users to return"),
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Get group leaderboard based on prediction points.
    
    Implements specification tiebreaker rules:
    1. Total points earned
    2. Number of exact score predictions
    3. Number of correct winner predictions
    4. Earlier registration date
    """
    # TODO: Validate user is member of group
    
    service = PredictionService(db)
    leaderboard = service.get_group_leaderboard(group_id, limit)
    
    return {
        "group_id": group_id,
        "leaderboard": leaderboard,
        "generated_at": datetime.utcnow()
    }


@router.post("/process-match/{match_id}")
async def process_match_predictions(
    match_id: UUID,
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Process all predictions for a completed match and award points.
    
    This endpoint should be called after match results are available.
    Implements specification scoring:
    - 3 points for exact score match (winner + exact score)
    - 1 point for correct winner only
    - 0 points for incorrect prediction
    
    Note: In production, this would typically be automated.
    """
    # TODO: Add authorization check (admin or system role)
    
    try:
        service = PredictionService(db)
        processing_stats = service.process_match_predictions(match_id)
        return processing_stats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process match predictions"
        )


@router.get("/match/{match_id}/predictions")
async def get_match_predictions(
    match_id: UUID,
    group_id: Optional[UUID] = Query(None, description="Filter by group ID"),
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Get all predictions for a specific match.
    
    Can be filtered by group. Useful for viewing group predictions
    after match completion or for analysis.
    """
    # TODO: Implement match prediction retrieval
    # TODO: Consider privacy rules (only show after deadline or to group members)
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Match predictions endpoint not yet implemented"
    )


@router.get("/upcoming-matches")
async def get_upcoming_matches_for_predictions(
    group_id: Optional[UUID] = Query(None, description="Filter by group ID"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of matches to return"),
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Get upcoming matches available for predictions.
    
    Returns matches where:
    - Prediction deadline has not passed
    - Match has not started
    - User hasn't made prediction yet (optionally filtered)
    """
    # TODO: Implement upcoming matches retrieval with deadline logic
    # TODO: Include user's existing predictions status
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Upcoming matches endpoint not yet implemented"
    )


@router.put("/{prediction_id}", response_model=PredictionResponse)
async def update_prediction(
    prediction_id: UUID,
    prediction_update: PredictionUpdate,
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Update an existing prediction before the deadline.
    
    Users can modify their predictions up until the deadline
    (default: 1 hour before match start).
    """
    # TODO: Implement prediction update logic
    # TODO: Validate ownership and deadline constraints
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Prediction update endpoint not yet implemented"
    )


@router.delete("/{prediction_id}")
async def delete_prediction(
    prediction_id: UUID,
    current_user: User = Depends(get_current_user_hybrid),
    db: Session = Depends(get_db)
):
    """
    Delete a prediction before the deadline.
    
    Note: Specification doesn't explicitly require this,
    but may be useful for user experience.
    """
    # TODO: Consider if deletion should be allowed per specification
    # TODO: Implement deletion logic with ownership validation
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Prediction deletion endpoint not yet implemented"
    )