"""
AuditLog model for the betting league championship application.

This module defines the AuditLog model with comprehensive activity tracking,
security monitoring, and change history recording as specified by the TDD tests
in backend/tests/models/test_audit_log_model.py.
"""

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, Float,
    CheckConstraint, Index, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from datetime import datetime, timezone, timedelta
from typing import Union, Optional, Dict, Any, List
import uuid
from enum import Enum

from .base import Base


class ActionType(Enum):
    """Valid action type values for audit logging."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    BET_PLACE = "bet_place"
    BET_SETTLE = "bet_settle"
    PAYMENT = "payment"
    TRANSFER = "transfer"
    VERIFICATION = "verification"
    SUSPENSION = "suspension"
    REACTIVATION = "reactivation"


class LogLevel(Enum):
    """Valid log level values."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class EntityType(Enum):
    """Valid entity type values for audit logging."""
    USER = "user"
    GROUP = "group"
    COMPETITION = "competition"
    MATCH = "match"
    BET = "bet"
    RESULT = "result"
    PAYMENT = "payment"
    SEASON = "season"
    TEAM = "team"
    PLAYER = "player"
    ADMIN = "admin"
    SYSTEM = "system"


class AuditLog(Base):
    """
    AuditLog model for comprehensive activity tracking and security monitoring.
    
    Handles user activity logging, change history recording, security event
    monitoring, and data integrity tracking for compliance and auditing.
    """
    
    __tablename__ = 'audit_logs'
    
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the audit log entry"
    )
    
    # Core audit fields
    action_type = Column(
        String(50),
        nullable=False,
        comment="Type of action performed"
    )
    entity_type = Column(
        String(50),
        nullable=False,
        comment="Type of entity being acted upon"
    )
    entity_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        comment="ID of the entity being acted upon"
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', name='fk_audit_logs_user_id'),
        nullable=False,
        comment="ID of the user performing the action"
    )
    
    # Logging details
    log_level = Column(
        String(20),
        nullable=False,
        comment="Severity level of the log entry"
    )
    message = Column(
        Text,
        nullable=False,
        comment="Human-readable description of the action"
    )
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="When the action occurred"
    )
    
    # Session and request tracking
    session_id = Column(
        String(100),
        comment="Session ID when the action was performed"
    )
    request_id = Column(
        String(100),
        comment="Request ID for tracing across services"
    )
    correlation_id = Column(
        String(100),
        comment="Correlation ID for tracking related actions"
    )
    
    # Client information
    ip_address = Column(
        String(45),  # IPv6 support
        comment="IP address of the client"
    )
    user_agent = Column(
        Text,
        comment="User agent string from the client"
    )
    device_info = Column(
        JSON,
        comment="Additional device information"
    )
    location = Column(
        JSON,
        comment="Geographic location information"
    )
    
    # Change tracking
    changes = Column(
        JSON,
        comment="Summary of changes made"
    )
    previous_values = Column(
        JSON,
        comment="Previous values before the change"
    )
    new_values = Column(
        JSON,
        comment="New values after the change"
    )
    
    # Security and risk
    risk_score = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Risk score of the action (0-100)"
    )
    flagged = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether this action has been flagged for review"
    )
    
    # Review and compliance
    reviewed_by = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', name='fk_audit_logs_reviewed_by'),
        comment="ID of the admin who reviewed this entry"
    )
    reviewed_at = Column(
        DateTime(timezone=True),
        comment="When this entry was reviewed"
    )
    notes = Column(
        Text,
        comment="Additional notes or comments"
    )
    
    # Additional structured data
    additional_data = Column(
        JSON,
        comment="Additional structured data related to the action"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="When the audit log entry was created"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "action_type IN ('create', 'read', 'update', 'delete', 'login', 'logout', 'password_change', 'bet_place', 'bet_settle', 'payment', 'transfer', 'verification', 'suspension', 'reactivation')",
            name="ck_audit_logs_action_type"
        ),
        CheckConstraint(
            "entity_type IN ('user', 'group', 'competition', 'match', 'bet', 'result', 'payment', 'season', 'team', 'player', 'admin', 'system')",
            name="ck_audit_logs_entity_type"
        ),
        CheckConstraint(
            "log_level IN ('debug', 'info', 'warning', 'error', 'critical')",
            name="ck_audit_logs_log_level"
        ),
        CheckConstraint(
            "risk_score >= 0 AND risk_score <= 100",
            name="ck_audit_logs_risk_score_range"
        ),
        CheckConstraint(
            "char_length(message) <= 1000",
            name="ck_audit_logs_message_length"
        ),
        CheckConstraint(
            "reviewed_at IS NULL OR reviewed_at >= timestamp",
            name="ck_audit_logs_reviewed_after_action"
        ),
        Index('ix_audit_logs_action_type', 'action_type'),
        Index('ix_audit_logs_entity_type', 'entity_type'),
        Index('ix_audit_logs_entity_id', 'entity_id'),
        Index('ix_audit_logs_user_id', 'user_id'),
        Index('ix_audit_logs_log_level', 'log_level'),
        Index('ix_audit_logs_timestamp', 'timestamp'),
        Index('ix_audit_logs_flagged', 'flagged'),
        Index('ix_audit_logs_risk_score', 'risk_score'),
        Index('ix_audit_logs_session_id', 'session_id'),
        Index('ix_audit_logs_created_at', 'created_at'),
        {'extend_existing': True}
    )
    
    def __init__(self, **kwargs):
        """Initialize AuditLog with proper validation and defaults."""
        # Validate required fields
        if 'action_type' not in kwargs or not kwargs['action_type']:
            raise ValueError("Action type is required")
        
        if 'entity_type' not in kwargs or not kwargs['entity_type']:
            raise ValueError("Entity type is required")
        
        if 'entity_id' not in kwargs or not kwargs['entity_id']:
            raise ValueError("Entity ID is required")
        
        if 'user_id' not in kwargs or not kwargs['user_id']:
            raise ValueError("User ID is required")
        
        if 'log_level' not in kwargs or not kwargs['log_level']:
            raise ValueError("Log level is required")
        
        if 'message' not in kwargs or not kwargs['message']:
            raise ValueError("Message is required")
        
        if 'timestamp' not in kwargs or not kwargs['timestamp']:
            kwargs['timestamp'] = datetime.now(timezone.utc)
        
        # Set default values if not provided
        if 'flagged' not in kwargs:
            kwargs['flagged'] = False
            
        if 'risk_score' not in kwargs:
            kwargs['risk_score'] = 0
            
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
            
        # Generate UUID if not provided
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
            
        super().__init__(**kwargs)
    
    # Validation methods
    @validates('action_type')
    def validate_action_type(self, key: str, action_type: str) -> str:
        """Validate action type."""
        if not action_type:
            raise ValueError("Action type is required")
        
        valid_actions = [at.value for at in ActionType]
        if action_type not in valid_actions:
            raise ValueError(f"Invalid action type. Must be one of: {', '.join(valid_actions)}")
        
        return action_type
    
    @validates('entity_type')
    def validate_entity_type(self, key: str, entity_type: str) -> str:
        """Validate entity type."""
        if not entity_type:
            raise ValueError("Entity type is required")
        
        valid_entities = [et.value for et in EntityType]
        if entity_type not in valid_entities:
            raise ValueError(f"Invalid entity type. Must be one of: {', '.join(valid_entities)}")
        
        return entity_type
    
    @validates('log_level')
    def validate_log_level(self, key: str, log_level: str) -> str:
        """Validate log level."""
        if not log_level:
            raise ValueError("Log level is required")
        
        valid_levels = [ll.value for ll in LogLevel]
        if log_level not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of: {', '.join(valid_levels)}")
        
        return log_level
    
    @validates('message')
    def validate_message(self, key: str, message: str) -> str:
        """Validate message content."""
        if not message:
            raise ValueError("Message is required")
        
        if len(message) > 1000:
            raise ValueError("Message cannot exceed 1000 characters")
        
        return message
    
    @validates('risk_score')
    def validate_risk_score(self, key: str, risk_score: int) -> int:
        """Validate risk score range."""
        if risk_score < 0 or risk_score > 100:
            raise ValueError("Risk score must be between 0 and 100")
        
        return risk_score
    
    @validates('entity_id')
    def validate_entity_id(self, key: str, entity_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate entity_id is provided."""
        if not entity_id:
            raise ValueError("Entity ID is required")
        return entity_id
    
    @validates('user_id')
    def validate_user_id(self, key: str, user_id: Union[str, uuid.UUID]) -> Union[str, uuid.UUID]:
        """Validate user_id is provided."""
        if not user_id:
            raise ValueError("User ID is required")
        return user_id
    
    @validates('timestamp')
    def validate_timestamp(self, key: str, timestamp: datetime) -> datetime:
        """Validate timestamp is provided."""
        if not timestamp:
            raise ValueError("Timestamp is required")
        return timestamp
    
    # Properties
    @property
    def is_security_event(self) -> bool:
        """Check if this is a security-related event."""
        security_actions = [
            ActionType.LOGIN.value, 
            ActionType.LOGOUT.value,
            ActionType.PASSWORD_CHANGE.value,
            ActionType.SUSPENSION.value,
            ActionType.REACTIVATION.value
        ]
        return self.action_type in security_actions
    
    @property
    def is_financial_event(self) -> bool:
        """Check if this is a financial-related event."""
        financial_actions = [
            ActionType.BET_PLACE.value,
            ActionType.BET_SETTLE.value,
            ActionType.PAYMENT.value,
            ActionType.TRANSFER.value
        ]
        return self.action_type in financial_actions
    
    @property
    def is_high_risk(self) -> bool:
        """Check if this is a high risk event."""
        return self.risk_score >= 70
    
    @property
    def requires_review(self) -> bool:
        """Check if this entry requires manual review."""
        return self.flagged or self.is_high_risk or self.log_level in [LogLevel.ERROR.value, LogLevel.CRITICAL.value]
    
    @property
    def is_reviewed(self) -> bool:
        """Check if this entry has been reviewed."""
        return self.reviewed_by is not None and self.reviewed_at is not None
    
    @property
    def severity_score(self) -> int:
        """Get numeric severity score for sorting/filtering."""
        severity_scores = {
            LogLevel.DEBUG.value: 10,
            LogLevel.INFO.value: 20,
            LogLevel.WARNING.value: 30,
            LogLevel.ERROR.value: 40,
            LogLevel.CRITICAL.value: 50
        }
        return severity_scores.get(self.log_level, 20)
    
    @property
    def age(self) -> int:
        """Get age of the audit log entry in seconds."""
        if not self.timestamp:
            return 0
        
        now = datetime.now(timezone.utc)
        age_delta = now - self.timestamp
        return int(age_delta.total_seconds())
    
    # Business logic methods
    def flag_for_review(self, reason: Optional[str] = None) -> None:
        """Flag this entry for manual review."""
        self.flagged = True
        if reason and self.additional_data:
            self.additional_data['flag_reason'] = reason
        elif reason:
            self.additional_data = {'flag_reason': reason}
    
    def update_risk_score(self, new_score: int) -> None:
        """Update the risk score with validation."""
        if new_score < 0 or new_score > 100:
            raise ValueError("Risk score must be between 0 and 100")
        
        old_score = self.risk_score
        self.risk_score = new_score
        
        # Auto-flag if risk score is high
        if new_score >= 70:
            self.flag_for_review(f"High risk score: {new_score}")
        
        # Log the risk score change
        if not self.additional_data:
            self.additional_data = {}
        self.additional_data['risk_score_history'] = self.additional_data.get('risk_score_history', [])
        self.additional_data['risk_score_history'].append({
            'old_score': old_score,
            'new_score': new_score,
            'updated_at': datetime.now(timezone.utc).isoformat()
        })
    
    def mark_reviewed(self, reviewer_id: Union[str, uuid.UUID], notes: Optional[str] = None) -> None:
        """Mark this entry as reviewed."""
        self.reviewed_by = reviewer_id
        self.reviewed_at = datetime.now(timezone.utc)
        if notes:
            self.notes = notes
        
        # Clear flagged status if resolved
        self.flagged = False
    
    def add_context_data(self, key: str, value: Any) -> None:
        """Add additional context data."""
        if not self.additional_data:
            self.additional_data = {}
        self.additional_data[key] = value
    
    def set_changes(self, previous: Dict[str, Any], new: Dict[str, Any]) -> None:
        """Set the change tracking data."""
        self.previous_values = previous
        self.new_values = new
        
        # Calculate changes summary
        changes = {}
        for key in set(previous.keys()) | set(new.keys()):
            if key not in previous:
                changes[key] = {'action': 'added', 'new_value': new[key]}
            elif key not in new:
                changes[key] = {'action': 'removed', 'old_value': previous[key]}
            elif previous[key] != new[key]:
                changes[key] = {
                    'action': 'modified',
                    'old_value': previous[key],
                    'new_value': new[key]
                }
        
        self.changes = changes
    
    # Class methods for queries
    @classmethod
    def get_by_user(cls, db_session, user_id: Union[str, uuid.UUID], limit: int = 100):
        """Get audit logs for a specific user."""
        return db_session.query(cls).filter(cls.user_id == user_id).order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_by_entity(cls, db_session, entity_type: str, entity_id: Union[str, uuid.UUID]):
        """Get audit logs for a specific entity."""
        return db_session.query(cls).filter(
            cls.entity_type == entity_type,
            cls.entity_id == entity_id
        ).order_by(cls.timestamp.desc()).all()
    
    @classmethod
    def get_by_action_type(cls, db_session, action_type: str, limit: int = 100):
        """Get audit logs by action type."""
        return db_session.query(cls).filter(cls.action_type == action_type).order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_security_events(cls, db_session, limit: int = 100):
        """Get security-related audit logs."""
        security_actions = [
            ActionType.LOGIN.value,
            ActionType.LOGOUT.value,
            ActionType.PASSWORD_CHANGE.value,
            ActionType.SUSPENSION.value,
            ActionType.REACTIVATION.value
        ]
        return db_session.query(cls).filter(cls.action_type.in_(security_actions)).order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_high_risk_events(cls, db_session, limit: int = 100):
        """Get high risk audit logs."""
        return db_session.query(cls).filter(cls.risk_score >= 70).order_by(cls.risk_score.desc(), cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_flagged_entries(cls, db_session):
        """Get all flagged entries needing review."""
        return db_session.query(cls).filter(cls.flagged == True).order_by(cls.timestamp.desc()).all()
    
    @classmethod
    def get_by_session(cls, db_session, session_id: str):
        """Get all audit logs for a session."""
        return db_session.query(cls).filter(cls.session_id == session_id).order_by(cls.timestamp.asc()).all()
    
    @classmethod
    def get_recent_activity(cls, db_session, hours: int = 24, limit: int = 100):
        """Get recent activity within specified hours."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        return db_session.query(cls).filter(cls.timestamp >= cutoff_time).order_by(cls.timestamp.desc()).limit(limit).all()
    
    # Representation
    def __repr__(self) -> str:
        """String representation of AuditLog."""
        return f"<AuditLog(id={self.id}, action='{self.action_type}', entity='{self.entity_type}', user_id={self.user_id}, level='{self.log_level}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert AuditLog to dictionary."""
        return {
            'id': str(self.id),
            'action_type': self.action_type,
            'entity_type': self.entity_type,
            'entity_id': str(self.entity_id),
            'user_id': str(self.user_id),
            'log_level': self.log_level,
            'message': self.message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'session_id': self.session_id,
            'request_id': self.request_id,
            'correlation_id': self.correlation_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'device_info': self.device_info,
            'location': self.location,
            'changes': self.changes,
            'previous_values': self.previous_values,
            'new_values': self.new_values,
            'risk_score': self.risk_score,
            'flagged': self.flagged,
            'reviewed_by': str(self.reviewed_by) if self.reviewed_by else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'notes': self.notes,
            'additional_data': self.additional_data,
            'is_security_event': self.is_security_event,
            'is_financial_event': self.is_financial_event,
            'is_high_risk': self.is_high_risk,
            'requires_review': self.requires_review,
            'is_reviewed': self.is_reviewed,
            'severity_score': self.severity_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


# SQLAlchemy event listeners for automatic updates
from sqlalchemy import event
from datetime import timedelta

@event.listens_for(AuditLog, 'before_insert')
def auto_set_created_at(mapper, connection, target):
    """Set created_at timestamp on insert."""
    if not target.created_at:
        target.created_at = datetime.now(timezone.utc)

@event.listens_for(AuditLog, 'before_insert')
def auto_generate_id(mapper, connection, target):
    """Generate UUID on insert if not provided."""
    if not target.id:
        target.id = uuid.uuid4()