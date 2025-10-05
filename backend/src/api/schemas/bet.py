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
    """Base bet schema with common fields."""
    
    bet_type: BetType = Field(..., description="Type of bet")
    amount: float = Field(..., gt=0, description="Bet amount")
    odds: float = Field(..., gt=1.0, description="Betting odds")
    potential_payout: float = Field(..., gt=0, description="Potential payout")
    
    # Bet specifics
    outcome: Optional[BetOutcome] = Field(None, description="Predicted outcome")
    handicap_value: Optional[float] = Field(None, description="Handicap value (if applicable)")
    total_value: Optional[float] = Field(None, description="Total goals/points value (if applicable)")
    is_over: Optional[bool] = Field(None, description="Over/under selection (if applicable)")
    
    # Score prediction (for correct score bets)
    predicted_home_score: Optional[int] = Field(None, ge=0, description="Predicted home score")
    predicted_away_score: Optional[int] = Field(None, ge=0, description="Predicted away score")
    
    # Additional bet parameters
    bet_parameters: Optional[dict] = Field(None, description="Additional bet-specific parameters")
    notes: Optional[str] = Field(None, max_length=500, description="Bet notes")

    @field_validator('potential_payout')
    @classmethod
    def validate_potential_payout(cls, v: float, info) -> float:
        """Validate that potential payout matches amount * odds."""
        if 'amount' in info.data and 'odds' in info.data:
            expected_payout = info.data['amount'] * info.data['odds']
            if abs(v - expected_payout) > 0.01:  # Allow small floating point differences
                raise ValueError('Potential payout must equal amount * odds')
        return v

    @field_validator('outcome')
    @classmethod
    def validate_outcome_for_bet_type(cls, v: Optional[BetOutcome], info) -> Optional[BetOutcome]:
        """Validate outcome is provided for match winner bets."""
        if 'bet_type' in info.data and info.data['bet_type'] == BetType.MATCH_WINNER:
            if v is None:
                raise ValueError('Outcome is required for match winner bets')
        return v


class BetCreate(BetBase):
    """Schema for creating a new bet."""
    
    match_id: UUID = Field(..., description="ID of the match to bet on")
    group_id: Optional[UUID] = Field(None, description="ID of the group this bet belongs to")

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


class BetResponse(BetBase):
    """Schema for bet responses."""
    
    id: UUID = Field(..., description="Bet unique identifier")
    user_id: UUID = Field(..., description="User who placed the bet")
    match_id: UUID = Field(..., description="Match this bet is for")
    group_id: Optional[UUID] = Field(None, description="Group this bet belongs to")
    
    status: BetStatus = Field(..., description="Current bet status")
    actual_payout: Optional[float] = Field(None, description="Actual payout (if settled)")
    
    # Settlement details
    settled_at: Optional[datetime] = Field(None, description="When bet was settled")
    settlement_reason: Optional[str] = Field(None, description="Reason for settlement")
    
    # Metadata
    placed_at: datetime = Field(..., description="When bet was placed")
    created_at: datetime = Field(..., description="Bet creation timestamp")
    updated_at: datetime = Field(..., description="Bet last update timestamp")
    is_active: bool = Field(..., description="Whether bet is active")

    class Config:
        from_attributes = True


class BetSummary(BaseModel):
    """Lightweight bet schema for lists and references."""
    
    id: UUID = Field(..., description="Bet unique identifier")
    user_id: UUID = Field(..., description="User who placed the bet")
    match_id: UUID = Field(..., description="Match this bet is for")
    bet_type: BetType = Field(..., description="Type of bet")
    amount: float = Field(..., description="Bet amount")
    odds: float = Field(..., description="Betting odds")
    potential_payout: float = Field(..., description="Potential payout")
    status: BetStatus = Field(..., description="Current bet status")
    placed_at: datetime = Field(..., description="When bet was placed")
    is_active: bool = Field(..., description="Whether bet is active")

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


class BetStats(BaseModel):
    """Bet statistics schema."""
    
    total_bets: int = Field(..., description="Total number of bets")
    total_amount: float = Field(..., description="Total amount bet")
    total_payout: float = Field(..., description="Total payouts")
    win_rate: float = Field(..., ge=0, le=100, description="Win rate percentage")
    average_odds: float = Field(..., description="Average betting odds")
    profit_loss: float = Field(..., description="Total profit/loss")
    
    # Bet type breakdown
    bet_type_stats: dict = Field(..., description="Statistics by bet type")
    
    # Status breakdown
    won_bets: int = Field(..., description="Number of won bets")
    lost_bets: int = Field(..., description="Number of lost bets")
    pending_bets: int = Field(..., description="Number of pending bets")
    void_bets: int = Field(..., description="Number of void bets")

    class Config:
        from_attributes = True


class BetWithStats(BetResponse):
    """Bet response with statistics."""
    
    stats: BetStats = Field(..., description="Bet statistics")

    class Config:
        from_attributes = True


class BetHistory(BaseModel):
    """Bet history schema."""
    
    user_id: UUID = Field(..., description="User ID")
    bets: List[BetSummary] = Field(..., description="List of user bets")
    summary_stats: BetStats = Field(..., description="Summary statistics")
    last_updated: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class BetSettlement(BaseModel):
    """Bet settlement schema."""
    
    bet_id: UUID = Field(..., description="Bet ID")
    status: BetStatus = Field(..., description="Settlement status")
    actual_payout: Optional[float] = Field(None, description="Actual payout amount")
    settlement_reason: str = Field(..., description="Reason for settlement")
    settled_by: UUID = Field(..., description="User who settled the bet")

    class Config:
        from_attributes = True


class BetOdds(BaseModel):
    """Bet odds schema for different outcomes."""
    
    match_id: UUID = Field(..., description="Match ID")
    
    # Match winner odds
    home_win_odds: Optional[float] = Field(None, description="Home team win odds")
    away_win_odds: Optional[float] = Field(None, description="Away team win odds")
    draw_odds: Optional[float] = Field(None, description="Draw odds")
    
    # Over/under odds
    total_goals_line: Optional[float] = Field(None, description="Total goals line")
    over_odds: Optional[float] = Field(None, description="Over odds")
    under_odds: Optional[float] = Field(None, description="Under odds")
    
    # Handicap odds
    handicap_line: Optional[float] = Field(None, description="Handicap line")
    home_handicap_odds: Optional[float] = Field(None, description="Home team handicap odds")
    away_handicap_odds: Optional[float] = Field(None, description="Away team handicap odds")
    
    # Additional odds
    both_teams_score_yes: Optional[float] = Field(None, description="Both teams score YES odds")
    both_teams_score_no: Optional[float] = Field(None, description="Both teams score NO odds")
    
    # Metadata
    last_updated: datetime = Field(..., description="When odds were last updated")
    bookmaker: Optional[str] = Field(None, description="Bookmaker/odds provider")

    class Config:
        from_attributes = True


class BetSlip(BaseModel):
    """Bet slip schema for multiple bets."""
    
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


class BetAnalytics(BaseModel):
    """Bet analytics schema."""
    
    period: str = Field(..., description="Analytics period")
    
    # Volume metrics
    total_bets_placed: int = Field(..., description="Total bets placed")
    total_amount_wagered: float = Field(..., description="Total amount wagered")
    total_payouts: float = Field(..., description="Total payouts")
    
    # Performance metrics
    house_edge: float = Field(..., description="House edge percentage")
    return_to_player: float = Field(..., description="Return to player percentage")
    
    # Popular bet types
    popular_bet_types: dict = Field(..., description="Popular bet types with counts")
    
    # Match analytics
    most_bet_matches: List[dict] = Field(..., description="Most popular matches for betting")
    
    # User analytics
    active_bettors: int = Field(..., description="Number of active bettors")
    average_bet_size: float = Field(..., description="Average bet size")

    class Config:
        from_attributes = True