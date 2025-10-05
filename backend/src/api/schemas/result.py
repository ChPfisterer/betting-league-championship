"""
Result schemas for match results and outcomes.

This module defines Pydantic schemas for managing match results,
including final scores, statistics, and outcome calculations for
automatic bet settlement and platform analytics.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any, List
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, field_validator, ConfigDict

from models.result import ResultStatus


class ResultStatus(str, Enum):
    """Result status enumeration for result processing."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"


class ResultType(str, Enum):
    """Result type enumeration."""
    FINAL = "final"
    PROVISIONAL = "provisional"
    HALF_TIME = "half_time"
    LIVE = "live"


class ResultBase(BaseModel):
    """Base schema for result data."""
    
    match_id: UUID = Field(..., description="Match unique identifier")
    result_type: ResultType = Field(..., description="Type of result")
    home_score: Optional[int] = Field(None, ge=0, description="Home team score")
    away_score: Optional[int] = Field(None, ge=0, description="Away team score")
    status: ResultStatus = Field(ResultStatus.PENDING, description="Result status")
    additional_data: Optional[Dict[str, Any]] = Field(None, description="Additional result data")
    notes: Optional[str] = Field(None, max_length=500, description="Result notes")


class ResultCreate(ResultBase):
    """Schema for creating a new result."""
    
    recorded_by: UUID = Field(..., description="User who recorded the result")
    
    @field_validator('additional_data')
    @classmethod
    def validate_additional_data(cls, v):
        """Validate additional data structure."""
        if v is not None:
            # Ensure all keys are strings and values are JSON-serializable
            if not isinstance(v, dict):
                raise ValueError("Additional data must be a dictionary")
            
            for key, value in v.items():
                if not isinstance(key, str):
                    raise ValueError("All keys in additional_data must be strings")
                
                # Check if value is JSON-serializable
                try:
                    import json
                    json.dumps(value)
                except (TypeError, ValueError):
                    raise ValueError(f"Value for key '{key}' is not JSON-serializable")
        
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "match_id": "bb0e8400-e29b-41d4-a716-446655440000",
                "result_type": "final",
                "home_score": 2,
                "away_score": 1,
                "status": "confirmed",
                "recorded_by": "aa0e8400-e29b-41d4-a716-446655440000",
                "additional_data": {
                    "goals": [
                        {"minute": 23, "player": "John Doe", "team": "home"},
                        {"minute": 67, "player": "Jane Smith", "team": "home"},
                        {"minute": 89, "player": "Bob Wilson", "team": "away"}
                    ],
                    "cards": [
                        {"minute": 45, "player": "Mike Brown", "type": "yellow"},
                        {"minute": 78, "player": "Sarah Davis", "type": "red"}
                    ]
                },
                "notes": "Match completed in regular time"
            }
        }
    )


class ResultUpdate(BaseModel):
    """Schema for updating result data."""
    
    home_score: Optional[int] = Field(None, ge=0, description="Updated home team score")
    away_score: Optional[int] = Field(None, ge=0, description="Updated away team score")
    status: Optional[ResultStatus] = Field(None, description="Updated result status")
    additional_data: Optional[Dict[str, Any]] = Field(None, description="Updated additional data")
    notes: Optional[str] = Field(None, max_length=500, description="Updated result notes")
    
    @field_validator('additional_data')
    @classmethod
    def validate_additional_data(cls, v):
        """Validate additional data structure."""
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError("Additional data must be a dictionary")
            
            for key, value in v.items():
                if not isinstance(key, str):
                    raise ValueError("All keys in additional_data must be strings")
                
                try:
                    import json
                    json.dumps(value)
                except (TypeError, ValueError):
                    raise ValueError(f"Value for key '{key}' is not JSON-serializable")
        
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "home_score": 3,
                "away_score": 1,
                "status": "confirmed",
                "notes": "Score updated after video review"
            }
        }
    )


class ResultResponse(ResultBase):
    """Schema for result response data."""
    
    id: UUID = Field(..., description="Result unique identifier")
    recorded_by: UUID = Field(..., description="User who recorded the result")
    recorded_at: datetime = Field(..., description="When result was recorded")
    updated_at: Optional[datetime] = Field(None, description="When result was last updated")
    confirmed_at: Optional[datetime] = Field(None, description="When result was confirmed")
    
    model_config = ConfigDict(from_attributes=True)


class ResultSummary(BaseModel):
    """Schema for result summary data."""
    
    id: UUID = Field(..., description="Result unique identifier")
    match_id: UUID = Field(..., description="Match unique identifier")
    result_type: ResultType = Field(..., description="Type of result")
    home_score: Optional[int] = Field(None, description="Home team score")
    away_score: Optional[int] = Field(None, description="Away team score")
    status: ResultStatus = Field(..., description="Result status")
    recorded_at: datetime = Field(..., description="When result was recorded")
    
    model_config = ConfigDict(from_attributes=True)


class ResultWithMatch(ResultResponse):
    """Schema for result data with match information."""
    
    match: Optional[Dict[str, Any]] = Field(None, description="Match details")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "cc0e8400-e29b-41d4-a716-446655440000",
                "match_id": "bb0e8400-e29b-41d4-a716-446655440000",
                "result_type": "final",
                "home_score": 2,
                "away_score": 1,
                "status": "confirmed",
                "recorded_by": "aa0e8400-e29b-41d4-a716-446655440000",
                "recorded_at": "2025-10-05T14:30:00Z",
                "match": {
                    "id": "bb0e8400-e29b-41d4-a716-446655440000",
                    "home_team": "Manchester United",
                    "away_team": "Liverpool FC",
                    "scheduled_time": "2025-10-05T15:00:00Z",
                    "status": "completed"
                }
            }
        }
    )


class ResultWithDetails(ResultResponse):
    """Schema for result data with full details."""
    
    match: Optional[Dict[str, Any]] = Field(None, description="Match details")
    recorded_by_user: Optional[Dict[str, Any]] = Field(None, description="User who recorded result")
    statistics: Optional[Dict[str, Any]] = Field(None, description="Match statistics")
    
    model_config = ConfigDict(from_attributes=True)


class ResultHistory(BaseModel):
    """Schema for result history tracking."""
    
    result_id: UUID = Field(..., description="Result unique identifier")
    changes: List[Dict[str, Any]] = Field(..., description="List of changes made")
    total_updates: int = Field(..., description="Total number of updates")
    first_recorded: datetime = Field(..., description="When first recorded")
    last_updated: Optional[datetime] = Field(None, description="When last updated")
    
    model_config = ConfigDict(from_attributes=True)


class ResultStatistics(BaseModel):
    """Schema for result statistics."""
    
    total_results: int = Field(..., description="Total number of results")
    confirmed_results: int = Field(..., description="Number of confirmed results")
    pending_results: int = Field(..., description="Number of pending results")
    disputed_results: int = Field(..., description="Number of disputed results")
    average_goals_per_match: Optional[Decimal] = Field(None, description="Average goals per match")
    home_win_percentage: Optional[Decimal] = Field(None, description="Home win percentage")
    away_win_percentage: Optional[Decimal] = Field(None, description="Away win percentage")
    draw_percentage: Optional[Decimal] = Field(None, description="Draw percentage")
    
    model_config = ConfigDict(from_attributes=True)


class ResultOutcome(BaseModel):
    """Schema for result outcome calculation."""
    
    result_id: UUID = Field(..., description="Result unique identifier")
    match_result: str = Field(..., description="Match result (home_win, away_win, draw)")
    total_goals: int = Field(..., description="Total goals scored")
    both_teams_scored: bool = Field(..., description="Whether both teams scored")
    clean_sheet: bool = Field(..., description="Whether there was a clean sheet")
    outcome_data: Dict[str, Any] = Field(..., description="Additional outcome data")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "result_id": "cc0e8400-e29b-41d4-a716-446655440000",
                "match_result": "home_win",
                "total_goals": 3,
                "both_teams_scored": True,
                "clean_sheet": False,
                "outcome_data": {
                    "winning_margin": 2,
                    "over_under_2_5": "over",
                    "handicap_result": "home_covered"
                }
            }
        }
    )


class ResultValidation(BaseModel):
    """Schema for result validation."""
    
    result_id: UUID = Field(..., description="Result unique identifier")
    is_valid: bool = Field(..., description="Whether result is valid")
    validation_errors: List[str] = Field(default_factory=list, description="List of validation errors")
    validation_warnings: List[str] = Field(default_factory=list, description="List of validation warnings")
    suggested_corrections: Optional[Dict[str, Any]] = Field(None, description="Suggested corrections")
    
    model_config = ConfigDict(from_attributes=True)


class ResultConfirmation(BaseModel):
    """Schema for result confirmation."""
    
    confirmed: bool = Field(..., description="Whether to confirm the result")
    confirmation_notes: Optional[str] = Field(None, max_length=500, description="Confirmation notes")
    override_validation: bool = Field(False, description="Whether to override validation errors")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "confirmed": True,
                "confirmation_notes": "Result verified by multiple officials",
                "override_validation": False
            }
        }
    )


class ResultDispute(BaseModel):
    """Schema for result dispute."""
    
    dispute_reason: str = Field(..., max_length=500, description="Reason for dispute")
    disputed_by: UUID = Field(..., description="User who disputed the result")
    evidence: Optional[Dict[str, Any]] = Field(None, description="Evidence supporting dispute")
    priority: str = Field("normal", description="Dispute priority")
    
    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        """Validate dispute priority."""
        allowed_priorities = ['low', 'normal', 'high', 'urgent']
        if v not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "dispute_reason": "Score was incorrectly recorded - video evidence shows different result",
                "disputed_by": "aa0e8400-e29b-41d4-a716-446655440000",
                "evidence": {
                    "video_timestamps": ["45:23", "67:12"],
                    "witness_statements": ["Official scorer confirmation"]
                },
                "priority": "high"
            }
        }
    )


class ResultAnalytics(BaseModel):
    """Schema for result analytics data."""
    
    period_start: datetime = Field(..., description="Analytics period start")
    period_end: datetime = Field(..., description="Analytics period end")
    total_matches: int = Field(..., description="Total matches in period")
    total_goals: int = Field(..., description="Total goals scored")
    average_goals_per_match: Decimal = Field(..., description="Average goals per match")
    home_wins: int = Field(..., description="Number of home wins")
    away_wins: int = Field(..., description="Number of away wins")
    draws: int = Field(..., description="Number of draws")
    both_teams_scored_count: int = Field(..., description="Matches where both teams scored")
    clean_sheets: int = Field(..., description="Number of clean sheets")
    highest_scoring_match: Optional[Dict[str, Any]] = Field(None, description="Highest scoring match details")
    most_goals_by_team: Optional[Dict[str, Any]] = Field(None, description="Most goals scored by a team")
    
    model_config = ConfigDict(from_attributes=True)


class ResultBulkCreate(BaseModel):
    """Schema for bulk result creation."""
    
    results: List[ResultCreate] = Field(..., description="List of results to create")
    validate_all: bool = Field(True, description="Whether to validate all results before creating")
    skip_duplicates: bool = Field(True, description="Whether to skip duplicate results")
    
    @field_validator('results')
    @classmethod
    def validate_results_count(cls, v):
        """Validate results count."""
        if len(v) == 0:
            raise ValueError("At least one result must be provided")
        if len(v) > 100:
            raise ValueError("Maximum 100 results can be created at once")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "results": [
                    {
                        "match_id": "bb0e8400-e29b-41d4-a716-446655440000",
                        "result_type": "final",
                        "home_score": 2,
                        "away_score": 1,
                        "status": "confirmed",
                        "recorded_by": "aa0e8400-e29b-41d4-a716-446655440000"
                    }
                ],
                "validate_all": True,
                "skip_duplicates": True
            }
        }
    )


class ResultBulkResponse(BaseModel):
    """Schema for bulk result creation response."""
    
    created_count: int = Field(..., description="Number of results created")
    skipped_count: int = Field(..., description="Number of results skipped")
    error_count: int = Field(..., description="Number of results with errors")
    created_results: List[UUID] = Field(..., description="IDs of created results")
    errors: List[Dict[str, Any]] = Field(default_factory=list, description="List of errors encountered")
    
    model_config = ConfigDict(from_attributes=True)


# Export all schemas
__all__ = [
    "ResultBase",
    "ResultCreate", 
    "ResultUpdate",
    "ResultResponse",
    "ResultSummary",
    "ResultWithMatch",
    "ResultWithDetails",
    "ResultHistory",
    "ResultStatistics",
    "ResultOutcome",
    "ResultValidation",
    "ResultConfirmation",
    "ResultDispute",
    "ResultAnalytics",
    "ResultBulkCreate",
    "ResultBulkResponse"
]