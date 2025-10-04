"""
Bet model for the betting league championship application.

This module defines the Bet model with comprehensive field validation,
betting logic, and risk management as specified by the TDD tests
in backend/tests/models/test_bet_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, 
    CheckConstraint, Index, ForeignKey, JSON, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone
from typing import Union, Optional, Dict, Any, List
from decimal import Decimal
import uuid
import re
from enum import Enum

from .base import Base


class BetType(Enum):
    """Valid bet type values."""
    SINGLE = "single"
    MULTIPLE = "multiple"
    ACCUMULATOR = "accumulator"
    SYSTEM = "system"
    EACH_WAY = "each_way"


class BetStatus(Enum):
    """Valid bet status values."""
    PENDING = "pending"
    MATCHED = "matched"
    WON = "won"
    LOST = "lost"
    VOID = "void"
    PARTIALLY_MATCHED = "partially_matched"
    SETTLED = "settled"
    CANCELLED = "cancelled"


class MarketType(Enum):
    """Valid market type values."""
    MATCH_WINNER = "match_winner"
    OVER_UNDER = "over_under"
    HANDICAP = "handicap"
    BOTH_TEAMS_SCORE = "both_teams_score"
    CORRECT_SCORE = "correct_score"
    FIRST_GOALSCORER = "first_goalscorer"
    TOTAL_GOALS = "total_goals"
    DOUBLE_CHANCE = "double_chance"


class RiskCategory(Enum):
    """Valid risk category values."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    VERY_HIGH = "very_high"


class Bet(Base):
    """
    Bet model for managing individual sports bets.
    
    Represents a single bet placed by a user on a match with comprehensive
    validation, risk management, and payout calculation.
    """
    
    __tablename__ = 'bets'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the bet"
    )
    
    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', name='fk_bets_user_id'),
        nullable=False,
        comment="ID of the user who placed the bet"
    )
    match_id = Column(
        UUID(as_uuid=True),
        ForeignKey('matches.id', name='fk_bets_match_id'),
        nullable=False,
        comment="ID of the match being bet on"
    )
    
    # Bet details
    bet_type = Column(
        String(20),
        nullable=False,
        comment="Type of bet (single, multiple, etc.)"
    )
    market_type = Column(
        String(30),
        nullable=False,
        comment="Market type (match_winner, over_under, etc.)"
    )
    
    # Financial information
    stake_amount = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Amount staked on the bet"
    )
    odds = Column(
        Numeric(8, 3),
        nullable=False,
        comment="Odds at which the bet was placed"
    )
    potential_payout = Column(
        Numeric(12, 2),
        nullable=False,
        comment="Potential payout if bet wins"
    )
    payout_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal('0.00'),
        comment="Actual payout amount"
    )
    commission = Column(
        Numeric(8, 2),
        nullable=False,
        default=Decimal('0.00'),
        comment="Commission charged on the bet"
    )
    
    # Bet specifics
    selection = Column(
        String(100),
        comment="Specific selection (home, away, over, under, etc.)"
    )
    handicap = Column(
        Numeric(5, 2),
        comment="Handicap value for handicap bets"
    )
    
    # Status and lifecycle
    status = Column(
        String(20),
        nullable=False,
        default=BetStatus.PENDING.value,
        comment="Current status of the bet"
    )
    void_reason = Column(
        Text,
        comment="Reason for voiding the bet if applicable"
    )
    
    # Risk management
    risk_category = Column(
        String(15),
        nullable=False,
        default=RiskCategory.NORMAL.value,
        comment="Risk category assessment"
    )
    max_liability = Column(
        Numeric(12, 2),
        comment="Maximum liability for this bet"
    )
    
    # Promotional features
    bonus_applied = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether a bonus was applied to this bet"
    )
    promotion_id = Column(
        UUID(as_uuid=True),
        comment="ID of the promotion if bonus applied"
    )
    
    # Additional information
    notes = Column(
        Text,
        comment="Additional notes about the bet"
    )
    ip_address = Column(
        String(45),
        comment="IP address from which bet was placed"
    )
    device_info = Column(
        JSON,
        comment="Device information when bet was placed"
    )
    
    # Timestamps
    placed_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the bet was placed"
    )
    settled_at = Column(
        DateTime(timezone=True),
        comment="When the bet was settled"
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the bet record was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="When the bet record was last updated"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "bet_type IN ('single', 'multiple', 'accumulator', 'system', 'each_way')",
            name="ck_bets_bet_type"
        ),
        CheckConstraint(
            "market_type IN ('match_winner', 'over_under', 'handicap', 'both_teams_score', 'correct_score', 'first_goalscorer', 'total_goals', 'double_chance')",
            name="ck_bets_market_type"
        ),
        CheckConstraint(
            "status IN ('pending', 'matched', 'won', 'lost', 'void', 'partially_matched', 'settled', 'cancelled')",
            name="ck_bets_status"
        ),
        CheckConstraint(
            "risk_category IN ('low', 'normal', 'high', 'very_high')",
            name="ck_bets_risk_category"
        ),
        CheckConstraint(
            "stake_amount > 0",
            name="ck_bets_stake_amount_positive"
        ),
        CheckConstraint(
            "odds >= 1.01",
            name="ck_bets_odds_minimum"
        ),
        CheckConstraint(
            "potential_payout >= stake_amount",
            name="ck_bets_potential_payout_minimum"
        ),
        CheckConstraint(
            "payout_amount >= 0",
            name="ck_bets_payout_amount_non_negative"
        ),
        CheckConstraint(
            "commission >= 0",
            name="ck_bets_commission_non_negative"
        ),
        CheckConstraint(
            "settled_at IS NULL OR settled_at >= placed_at",
            name="ck_bets_settled_after_placed"
        ),
        Index('ix_bets_user_id', 'user_id'),
        Index('ix_bets_match_id', 'match_id'),
        Index('ix_bets_status', 'status'),
        Index('ix_bets_bet_type', 'bet_type'),
        Index('ix_bets_market_type', 'market_type'),
        Index('ix_bets_placed_at', 'placed_at'),
        Index('ix_bets_risk_category', 'risk_category'),
        Index('ix_bets_user_status', 'user_id', 'status'),
        {'extend_existing': True}
    )
    
    def __init__(self, **kwargs):
        """Initialize Bet with proper validation and defaults."""
        # Validate required fields
        if 'user_id' not in kwargs or not kwargs['user_id']:
            raise ValueError("User ID is required")
        
        if 'match_id' not in kwargs or not kwargs['match_id']:
            raise ValueError("Match ID is required")
        
        if 'bet_type' not in kwargs or not kwargs['bet_type']:
            raise ValueError("Bet type is required")
        
        if 'market_type' not in kwargs or not kwargs['market_type']:
            raise ValueError("Market type is required")
        
        if 'stake_amount' not in kwargs or kwargs['stake_amount'] is None:
            raise ValueError("Stake amount is required")
        
        if 'odds' not in kwargs or kwargs['odds'] is None:
            raise ValueError("Odds are required")
        
        # Set default values if not provided
        if 'status' not in kwargs:
            kwargs['status'] = BetStatus.PENDING.value
            
        if 'commission' not in kwargs:
            kwargs['commission'] = Decimal('0.00')
            
        if 'bonus_applied' not in kwargs:
            kwargs['bonus_applied'] = False
            
        if 'risk_category' not in kwargs:
            kwargs['risk_category'] = RiskCategory.NORMAL.value
            
        if 'payout_amount' not in kwargs:
            kwargs['payout_amount'] = Decimal('0.00')
            
        if 'placed_at' not in kwargs:
            kwargs['placed_at'] = datetime.now(timezone.utc)
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.now(timezone.utc)
        
        # Calculate potential payout if not provided
        if 'potential_payout' not in kwargs:
            kwargs['potential_payout'] = kwargs['stake_amount'] * kwargs['odds']
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        super().__init__(**kwargs)
    
    # Validation methods
    @validates('user_id')
    def validate_user_id(self, key: str, user_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate user_id is provided."""
        if not user_id:
            raise ValueError("User ID is required")
        return user_id
    
    @validates('match_id')
    def validate_match_id(self, key: str, match_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate match_id is provided."""
        if not match_id:
            raise ValueError("Match ID is required")
        return match_id
    
    @validates('bet_type')
    def validate_bet_type(self, key: str, bet_type: str) -> str:
        """Validate bet type."""
        if not bet_type:
            raise ValueError("Bet type is required")
        
        valid_types = [bt.value for bt in BetType]
        if bet_type not in valid_types:
            raise ValueError(f"Invalid bet type. Must be one of: {', '.join(valid_types)}")
        
        return bet_type
    
    @validates('market_type')
    def validate_market_type(self, key: str, market_type: str) -> str:
        """Validate market type."""
        if not market_type:
            raise ValueError("Market type is required")
        
        valid_markets = [mt.value for mt in MarketType]
        if market_type not in valid_markets:
            raise ValueError(f"Invalid market type. Must be one of: {', '.join(valid_markets)}")
        
        return market_type
    
    @validates('stake_amount')
    def validate_stake_amount(self, key: str, stake_amount: Decimal) -> Decimal:
        """Validate stake amount."""
        if stake_amount is None:
            raise ValueError("Stake amount is required")
        
        stake_amount = Decimal(str(stake_amount))
        
        if stake_amount <= 0:
            raise ValueError("Stake amount must be greater than 0")
        
        # Reasonable maximum stake limit
        if stake_amount > Decimal('10000.00'):
            raise ValueError("Stake amount cannot exceed 10,000")
        
        return stake_amount
    
    @validates('odds')
    def validate_odds(self, key: str, odds: Decimal) -> Decimal:
        """Validate odds."""
        if odds is None:
            raise ValueError("Odds are required")
        
        odds = Decimal(str(odds))
        
        if odds < Decimal('1.01'):
            raise ValueError("Odds must be at least 1.01")
        
        # Reasonable maximum odds limit
        if odds > Decimal('1000.00'):
            raise ValueError("Odds cannot exceed 1000.00")
        
        return odds
    
    @validates('status')
    def validate_status(self, key: str, status: str) -> str:
        """Validate bet status."""
        if not status:
            raise ValueError("Status is required")
        
        valid_statuses = [bs.value for bs in BetStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        return status
    
    @validates('risk_category')
    def validate_risk_category(self, key: str, risk_category: str) -> str:
        """Validate risk category."""
        if not risk_category:
            raise ValueError("Risk category is required")
        
        valid_categories = [rc.value for rc in RiskCategory]
        if risk_category not in valid_categories:
            raise ValueError(f"Invalid risk category. Must be one of: {', '.join(valid_categories)}")
        
        return risk_category
    
    # Properties
    @property
    def is_settled(self) -> bool:
        """Check if bet is settled."""
        return self.status in [BetStatus.WON.value, BetStatus.LOST.value, BetStatus.VOID.value]
    
    @property
    def is_active(self) -> bool:
        """Check if bet is active (not settled or cancelled)."""
        return self.status in [BetStatus.PENDING.value, BetStatus.MATCHED.value, BetStatus.PARTIALLY_MATCHED.value]
    
    @property
    def is_winning(self) -> bool:
        """Check if bet won."""
        return self.status == BetStatus.WON.value
    
    @property
    def profit_loss(self) -> Decimal:
        """Calculate profit/loss for settled bets."""
        if not self.is_settled:
            return Decimal('0.00')
        
        if self.status == BetStatus.WON.value:
            return self.payout_amount - self.stake_amount - self.commission
        elif self.status == BetStatus.LOST.value:
            return -self.stake_amount
        else:  # VOID
            return Decimal('0.00')
    
    @property
    def return_on_investment(self) -> Optional[Decimal]:
        """Calculate ROI percentage."""
        if not self.is_settled or self.stake_amount == 0:
            return None
        
        return (self.profit_loss / self.stake_amount) * 100
    
    # Business logic methods
    def settle_bet(self, result: str, payout: Optional[Decimal] = None) -> None:
        """Settle the bet with result."""
        if self.is_settled:
            raise ValueError("Bet is already settled")
        
        if result == 'won':
            self.status = BetStatus.WON.value
            self.payout_amount = payout or self.potential_payout
        elif result == 'lost':
            self.status = BetStatus.LOST.value
            self.payout_amount = Decimal('0.00')
        elif result == 'void':
            self.status = BetStatus.VOID.value
            self.payout_amount = self.stake_amount  # Return stake
        else:
            raise ValueError("Invalid settlement result. Must be 'won', 'lost', or 'void'")
        
        self.settled_at = datetime.now(timezone.utc)
    
    def cancel_bet(self, reason: str) -> None:
        """Cancel the bet."""
        if self.is_settled:
            raise ValueError("Cannot cancel a settled bet")
        
        self.status = BetStatus.CANCELLED.value
        self.void_reason = reason
        self.settled_at = datetime.now(timezone.utc)
    
    def void_bet(self, reason: str) -> None:
        """Void the bet and return stake."""
        self.status = BetStatus.VOID.value
        self.void_reason = reason
        self.payout_amount = self.stake_amount
        self.settled_at = datetime.now(timezone.utc)
    
    def apply_bonus(self, promotion_id: Union[str, uuid.UUID], bonus_amount: Decimal) -> None:
        """Apply a bonus to the bet."""
        if self.bonus_applied:
            raise ValueError("Bonus already applied to this bet")
        
        self.bonus_applied = True
        self.promotion_id = promotion_id
        self.potential_payout += bonus_amount
    
    def update_risk_category(self, category: str) -> None:
        """Update risk category."""
        valid_categories = [rc.value for rc in RiskCategory]
        if category not in valid_categories:
            raise ValueError(f"Invalid risk category. Must be one of: {', '.join(valid_categories)}")
        
        self.risk_category = category
    
    # Class methods for queries
    @classmethod
    def get_by_user(cls, db_session, user_id: Union[str, uuid.UUID]):
        """Get bets by user."""
        return db_session.query(cls).filter(cls.user_id == user_id).all()
    
    @classmethod
    def get_by_match(cls, db_session, match_id: Union[str, uuid.UUID]):
        """Get bets by match."""
        return db_session.query(cls).filter(cls.match_id == match_id).all()
    
    @classmethod
    def get_by_status(cls, db_session, status: str):
        """Get bets by status."""
        return db_session.query(cls).filter(cls.status == status).all()
    
    @classmethod
    def get_pending_bets(cls, db_session):
        """Get all pending bets."""
        return db_session.query(cls).filter(cls.status == BetStatus.PENDING.value).all()
    
    @classmethod
    def get_settled_bets(cls, db_session):
        """Get all settled bets."""
        return db_session.query(cls).filter(
            cls.status.in_([BetStatus.WON.value, BetStatus.LOST.value, BetStatus.VOID.value])
        ).all()
    
    # Representation
    def __repr__(self) -> str:
        """String representation of Bet."""
        return f"<Bet(id={self.id}, user_id={self.user_id}, stake={self.stake_amount}, odds={self.odds}, status='{self.status}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Bet to dictionary."""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'match_id': str(self.match_id),
            'bet_type': self.bet_type,
            'market_type': self.market_type,
            'stake_amount': float(self.stake_amount),
            'odds': float(self.odds),
            'potential_payout': float(self.potential_payout),
            'payout_amount': float(self.payout_amount),
            'commission': float(self.commission),
            'selection': self.selection,
            'handicap': float(self.handicap) if self.handicap else None,
            'status': self.status,
            'void_reason': self.void_reason,
            'risk_category': self.risk_category,
            'max_liability': float(self.max_liability) if self.max_liability else None,
            'bonus_applied': self.bonus_applied,
            'promotion_id': str(self.promotion_id) if self.promotion_id else None,
            'notes': self.notes,
            'ip_address': self.ip_address,
            'device_info': self.device_info,
            'is_settled': self.is_settled,
            'is_active': self.is_active,
            'is_winning': self.is_winning,
            'profit_loss': float(self.profit_loss),
            'return_on_investment': float(self.return_on_investment) if self.return_on_investment else None,
            'placed_at': self.placed_at.isoformat() if self.placed_at else None,
            'settled_at': self.settled_at.isoformat() if self.settled_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# SQLAlchemy event listeners for automatic timestamp updates
from sqlalchemy import event

@event.listens_for(Bet, 'before_update')
def update_bet_updated_at(mapper, connection, target):
    """Update the updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)