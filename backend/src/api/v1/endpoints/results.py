"""
Result API endpoints for match results and outcomes.

This module provides comprehensive CRUD operations for result management,
including result recording, validation, confirmation, dispute handling,
and automatic bet settlement integration.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, http_not_found, http_conflict
from core.keycloak_security import get_current_user_hybrid
from models import User, Result, Match
from api.schemas.result import (
    ResultCreate,
    ResultUpdate,
    ResultConfirmation,
    ResultDispute,
    ResultResponse,
    ResultSummary,
    ResultWithMatch,
    ResultWithDetails,
    ResultHistory,
    ResultStatistics,
    ResultOutcome,
    ResultValidation,
    ResultAnalytics,
    ResultBulkCreate,
    ResultBulkResponse,
    ResultType,
    ResultStatus
)
from services.result_service import ResultService


router = APIRouter()


@router.post(
    "/",
    response_model=ResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record Result",
    description="Record a new match result with comprehensive validation"
)
async def record_result(
    result_data: ResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultResponse:
    """
    Record a new match result.
    
    Args:
        result_data: Result recording data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Recorded result details
        
    Raises:
        HTTPException: If validation fails
    """
    service = ResultService(db)
    try:
        result = service.create_result(result_data)
        return ResultResponse.model_validate(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=List[ResultSummary],
    summary="List Results",
    description="List results with comprehensive filtering options"
)
async def list_results(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    match_id: Optional[UUID] = Query(None, description="Filter by match ID"),
    result_type: Optional[ResultType] = Query(None, description="Filter by result type"),
    status: Optional[ResultStatus] = Query(None, description="Filter by result status"),
    recorded_by: Optional[UUID] = Query(None, description="Filter by user who recorded result"),
    date_from: Optional[datetime] = Query(None, description="Filter results from this date"),
    date_to: Optional[datetime] = Query(None, description="Filter results until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[ResultSummary]:
    """
    List results with filtering options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        match_id: Filter by match ID
        result_type: Filter by result type
        status: Filter by result status
        recorded_by: Filter by user who recorded result
        date_from: Filter results from this date
        date_to: Filter results until this date
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of result summaries
    """
    service = ResultService(db)
    results = service.list_results(
        skip=skip,
        limit=limit,
        match_id=match_id,
        result_type=result_type,
        status=status,
        recorded_by=recorded_by,
        date_from=date_from,
        date_to=date_to
    )
    return [ResultSummary.model_validate(result) for result in results]


@router.get(
    "/pending",
    response_model=List[ResultSummary],
    summary="List Pending Results",
    description="Get all pending results that need confirmation"
)
async def list_pending_results(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[ResultSummary]:
    """
    Get pending results.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of pending results
    """
    service = ResultService(db)
    results = service.get_pending_results(limit=limit)
    return [ResultSummary.model_validate(result) for result in results]


@router.get(
    "/disputed",
    response_model=List[ResultSummary],
    summary="List Disputed Results",
    description="Get all disputed results that need resolution"
)
async def list_disputed_results(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[ResultSummary]:
    """
    Get disputed results.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of disputed results
    """
    service = ResultService(db)
    results = service.get_disputed_results(limit=limit)
    return [ResultSummary.model_validate(result) for result in results]


@router.get(
    "/{result_id}",
    response_model=ResultResponse,
    summary="Get Result",
    description="Get result details by ID"
)
async def get_result(
    result_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultResponse:
    """
    Get result by ID.
    
    Args:
        result_id: Result unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Result details
        
    Raises:
        HTTPException: If result not found
    """
    service = ResultService(db)
    result = service.get_result(result_id)
    
    if not result:
        raise http_not_found(f"Result with ID {result_id} not found")
        
    return ResultResponse.model_validate(result)


@router.get(
    "/{result_id}/with-match",
    response_model=ResultWithMatch,
    summary="Get Result with Match",
    description="Get result details including match information"
)
async def get_result_with_match(
    result_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultWithMatch:
    """
    Get result with match details.
    
    Args:
        result_id: Result unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Result details with match information
        
    Raises:
        HTTPException: If result not found
    """
    service = ResultService(db)
    result = service.get_result(result_id)
    
    if not result:
        raise http_not_found(f"Result with ID {result_id} not found")
    
    # Load match relationship
    match = db.query(Match).filter(Match.id == result.match_id).first()
    
    result_dict = ResultResponse.model_validate(result).model_dump()
    result_dict['match'] = match
    
    return ResultWithMatch.model_validate(result_dict)


@router.get(
    "/{result_id}/outcome",
    response_model=ResultOutcome,
    summary="Get Result Outcome",
    description="Calculate match outcome from result data"
)
async def get_result_outcome(
    result_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultOutcome:
    """
    Get result outcome calculation.
    
    Args:
        result_id: Result unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Result outcome data
        
    Raises:
        HTTPException: If result not found or cannot calculate outcome
    """
    service = ResultService(db)
    outcome = service.calculate_outcome(result_id)
    
    if not outcome:
        raise http_not_found(f"Cannot calculate outcome for result {result_id}")
    
    return outcome


@router.get(
    "/{result_id}/validate",
    response_model=ResultValidation,
    summary="Validate Result",
    description="Validate result data and check for errors"
)
async def validate_result(
    result_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultValidation:
    """
    Validate result data.
    
    Args:
        result_id: Result unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Validation result with errors and warnings
    """
    service = ResultService(db)
    validation = service.validate_result(result_id)
    return ResultValidation(**validation)


@router.get(
    "/match/{match_id}",
    response_model=List[ResultSummary],
    summary="List Results by Match",
    description="Get all results for a specific match"
)
async def list_results_by_match(
    match_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[ResultSummary]:
    """
    Get results by match.
    
    Args:
        match_id: Match unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of results for the match
    """
    service = ResultService(db)
    results = service.get_match_results(match_id)
    return [ResultSummary.model_validate(result) for result in results]


@router.get(
    "/user/{user_id}",
    response_model=List[ResultSummary],
    summary="List Results by User",
    description="Get all results recorded by a specific user"
)
async def list_results_by_user(
    user_id: UUID,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[ResultSummary]:
    """
    Get results by user.
    
    Args:
        user_id: User unique identifier
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of results recorded by the user
    """
    service = ResultService(db)
    results = service.get_user_results(user_id, limit=limit)
    return [ResultSummary.model_validate(result) for result in results]


@router.get(
    "/statistics/overview",
    response_model=ResultStatistics,
    summary="Get Result Statistics",
    description="Get comprehensive result statistics"
)
async def get_result_statistics(
    date_from: Optional[datetime] = Query(None, description="Filter from this date"),
    date_to: Optional[datetime] = Query(None, description="Filter until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultStatistics:
    """
    Get result statistics.
    
    Args:
        date_from: Filter from this date
        date_to: Filter until this date
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Result statistics
    """
    service = ResultService(db)
    return service.get_statistics(date_from=date_from, date_to=date_to)


@router.get(
    "/analytics/period",
    response_model=ResultAnalytics,
    summary="Get Result Analytics",
    description="Get result analytics for a specific period"
)
async def get_result_analytics(
    period_days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultAnalytics:
    """
    Get result analytics.
    
    Args:
        period_days: Number of days to analyze
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Result analytics data
    """
    service = ResultService(db)
    return service.get_analytics(period_days=period_days)


@router.put(
    "/{result_id}",
    response_model=ResultResponse,
    summary="Update Result",
    description="Update result data"
)
async def update_result(
    result_id: UUID,
    update_data: ResultUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultResponse:
    """
    Update result.
    
    Args:
        result_id: Result unique identifier
        update_data: Updated result data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated result details
        
    Raises:
        HTTPException: If result not found or cannot be updated
    """
    service = ResultService(db)
    try:
        result = service.update_result(result_id, update_data)
        if not result:
            raise http_not_found(f"Result with ID {result_id} not found")
        return ResultResponse.model_validate(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{result_id}/confirm",
    response_model=ResultResponse,
    summary="Confirm Result",
    description="Confirm a result and trigger bet settlement"
)
async def confirm_result(
    result_id: UUID,
    confirmation: ResultConfirmation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultResponse:
    """
    Confirm result.
    
    Args:
        result_id: Result unique identifier
        confirmation: Confirmation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Confirmed result details
        
    Raises:
        HTTPException: If result not found or cannot be confirmed
    """
    service = ResultService(db)
    try:
        result = service.confirm_result(result_id, confirmation)
        if not result:
            raise http_not_found(f"Result with ID {result_id} not found")
        return ResultResponse.model_validate(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{result_id}/dispute",
    response_model=ResultResponse,
    summary="Dispute Result",
    description="Dispute a result with evidence and reasoning"
)
async def dispute_result(
    result_id: UUID,
    dispute: ResultDispute,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultResponse:
    """
    Dispute result.
    
    Args:
        result_id: Result unique identifier
        dispute: Dispute data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Disputed result details
        
    Raises:
        HTTPException: If result not found
    """
    service = ResultService(db)
    result = service.dispute_result(result_id, dispute)
    
    if not result:
        raise http_not_found(f"Result with ID {result_id} not found")
    
    return ResultResponse.model_validate(result)


@router.post(
    "/bulk",
    response_model=ResultBulkResponse,
    summary="Bulk Create Results",
    description="Create multiple results in a single operation"
)
async def bulk_create_results(
    bulk_data: ResultBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> ResultBulkResponse:
    """
    Create multiple results in bulk.
    
    Args:
        bulk_data: Bulk creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Bulk creation summary
    """
    service = ResultService(db)
    result = service.bulk_create_results(bulk_data)
    return ResultBulkResponse(**result)


@router.delete(
    "/{result_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Result",
    description="Delete a result (with restrictions)"
)
async def delete_result(
    result_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> None:
    """
    Delete result.
    
    Args:
        result_id: Result unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If result not found or cannot be deleted
    """
    service = ResultService(db)
    try:
        deleted = service.delete_result(result_id)
        if not deleted:
            raise http_not_found(f"Result with ID {result_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/search/{query}",
    response_model=List[ResultSummary],
    summary="Search Results",
    description="Search results by notes or additional data"
)
async def search_results(
    query: str,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[ResultSummary]:
    """
    Search results.
    
    Args:
        query: Search query string
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of matching results
    """
    service = ResultService(db)
    results = service.search_results(query, limit=limit)
    return [ResultSummary.model_validate(result) for result in results]
