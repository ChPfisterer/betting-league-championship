"""
Pydantic schemas for Audit Log operations.

This module provides comprehensive schemas for audit logging functionality,
including activity tracking, security monitoring, and compliance reporting
for the betting platform.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic.types import Json


class LogLevel(str, Enum):
    """Audit log severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ActionType(str, Enum):
    """Types of actions that can be audited."""
    # Authentication actions
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_UNLOCKED = "account_unlocked"
    
    # User management
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    USER_ACTIVATED = "user_activated"
    USER_DEACTIVATED = "user_deactivated"
    
    # Group management
    GROUP_CREATED = "group_created"
    GROUP_UPDATED = "group_updated"
    GROUP_DELETED = "group_deleted"
    GROUP_JOINED = "group_joined"
    GROUP_LEFT = "group_left"
    GROUP_MEMBER_ADDED = "group_member_added"
    GROUP_MEMBER_REMOVED = "group_member_removed"
    GROUP_ROLE_CHANGED = "group_role_changed"
    GROUP_OWNERSHIP_TRANSFERRED = "group_ownership_transferred"
    
    # Betting actions
    BET_PLACED = "bet_placed"
    BET_UPDATED = "bet_updated"
    BET_CANCELLED = "bet_cancelled"
    BET_SETTLED = "bet_settled"
    BET_PAYOUT = "bet_payout"
    
    # Sports management
    SPORT_CREATED = "sport_created"
    SPORT_UPDATED = "sport_updated"
    SPORT_DELETED = "sport_deleted"
    TEAM_CREATED = "team_created"
    TEAM_UPDATED = "team_updated"
    TEAM_DELETED = "team_deleted"
    COMPETITION_CREATED = "competition_created"
    COMPETITION_UPDATED = "competition_updated"
    COMPETITION_DELETED = "competition_deleted"
    SEASON_CREATED = "season_created"
    SEASON_UPDATED = "season_updated"
    SEASON_DELETED = "season_deleted"
    MATCH_CREATED = "match_created"
    MATCH_UPDATED = "match_updated"
    MATCH_DELETED = "match_deleted"
    PLAYER_CREATED = "player_created"
    PLAYER_UPDATED = "player_updated"
    PLAYER_DELETED = "player_deleted"
    
    # Results management
    RESULT_CREATED = "result_created"
    RESULT_UPDATED = "result_updated"
    RESULT_CONFIRMED = "result_confirmed"
    RESULT_DISPUTED = "result_disputed"
    RESULT_FINALIZED = "result_finalized"
    
    # Security events
    PERMISSION_DENIED = "permission_denied"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_BREACH_ATTEMPT = "data_breach_attempt"
    API_RATE_LIMIT_EXCEEDED = "api_rate_limit_exceeded"
    
    # System events
    SYSTEM_STARTUP = "system_startup"
    SYSTEM_SHUTDOWN = "system_shutdown"
    SYSTEM_ERROR = "system_error"
    DATABASE_ERROR = "database_error"
    BACKUP_CREATED = "backup_created"
    MAINTENANCE_MODE = "maintenance_mode"
    
    # Administrative actions
    ADMIN_ACTION = "admin_action"
    CONFIG_CHANGED = "config_changed"
    FEATURE_TOGGLE = "feature_toggle"
    DATA_EXPORT = "data_export"
    DATA_IMPORT = "data_import"
    BULK_OPERATION = "bulk_operation"


class EntityType(str, Enum):
    """Types of entities that can be audited."""
    USER = "user"
    GROUP = "group"
    GROUP_MEMBERSHIP = "group_membership"
    SPORT = "sport"
    TEAM = "team"
    COMPETITION = "competition"
    SEASON = "season"
    MATCH = "match"
    PLAYER = "player"
    BET = "bet"
    RESULT = "result"
    AUDIT_LOG = "audit_log"
    SYSTEM = "system"
    SESSION = "session"
    API_KEY = "api_key"
    PERMISSION = "permission"


class AuditLogBase(BaseModel):
    """Base schema for audit log entries."""
    
    action_type: ActionType = Field(
        ...,
        description="Type of action being logged"
    )
    entity_type: Optional[EntityType] = Field(
        None,
        description="Type of entity involved in the action"
    )
    entity_id: Optional[UUID] = Field(
        None,
        description="ID of the entity involved in the action"
    )
    user_id: Optional[UUID] = Field(
        None,
        description="ID of the user performing the action"
    )
    session_id: Optional[str] = Field(
        None,
        max_length=255,
        description="Session ID associated with the action"
    )
    ip_address: Optional[str] = Field(
        None,
        max_length=45,
        description="IP address of the user performing the action"
    )
    user_agent: Optional[str] = Field(
        None,
        max_length=1000,
        description="User agent string from the request"
    )
    level: LogLevel = Field(
        default=LogLevel.INFO,
        description="Severity level of the log entry"
    )
    message: str = Field(
        ...,
        max_length=2000,
        description="Human-readable description of the action"
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional structured data about the action"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata for the audit entry"
    )
    request_id: Optional[str] = Field(
        None,
        max_length=255,
        description="Request ID for tracing distributed operations"
    )
    source: Optional[str] = Field(
        None,
        max_length=100,
        description="Source system or component that generated the log"
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="Tags for categorizing and filtering audit logs"
    )


class AuditLogCreate(AuditLogBase):
    """Schema for creating audit log entries."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "action_type": "user_created",
                "entity_type": "user",
                "entity_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "987fcdeb-51d3-12a3-b456-426614174000",
                "session_id": "sess_abc123",
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0...",
                "level": "info",
                "message": "New user account created successfully",
                "details": {
                    "username": "john_doe",
                    "email": "john@example.com",
                    "registration_method": "email"
                },
                "metadata": {
                    "country": "US",
                    "timezone": "UTC-5"
                },
                "request_id": "req_xyz789",
                "source": "web_api",
                "tags": ["registration", "user_management"]
            }
        }
    )
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        """Validate tags list."""
        if v is not None:
            if len(v) > 20:
                raise ValueError("Maximum 20 tags allowed")
            for tag in v:
                if not isinstance(tag, str) or len(tag) > 50:
                    raise ValueError("Tags must be strings with max length 50")
        return v


class AuditLogUpdate(BaseModel):
    """Schema for updating audit log entries (limited fields)."""
    
    tags: Optional[List[str]] = Field(
        None,
        description="Updated tags for the audit log entry"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Updated metadata for the audit entry"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "tags": ["reviewed", "processed"],
                "metadata": {
                    "reviewed_by": "admin_user",
                    "review_date": "2025-10-05T10:00:00Z"
                }
            }
        }
    )


class AuditLogResponse(AuditLogBase):
    """Schema for audit log responses."""
    
    id: UUID = Field(..., description="Unique identifier for the audit log entry")
    created_at: datetime = Field(..., description="Timestamp when the log entry was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the log entry was last updated")
    
    model_config = ConfigDict(from_attributes=True)


class AuditLogSummary(BaseModel):
    """Summary schema for audit log entries."""
    
    id: UUID = Field(..., description="Unique identifier for the audit log entry")
    action_type: ActionType = Field(..., description="Type of action being logged")
    entity_type: Optional[EntityType] = Field(None, description="Type of entity involved")
    entity_id: Optional[UUID] = Field(None, description="ID of the entity involved")
    user_id: Optional[UUID] = Field(None, description="ID of the user performing the action")
    level: LogLevel = Field(..., description="Severity level of the log entry")
    message: str = Field(..., description="Human-readable description of the action")
    created_at: datetime = Field(..., description="Timestamp when the log entry was created")
    
    model_config = ConfigDict(from_attributes=True)


class AuditLogWithUser(AuditLogResponse):
    """Audit log with user information."""
    
    user: Optional[Dict[str, Any]] = Field(
        None,
        description="User information associated with the audit log"
    )


class AuditLogWithEntity(AuditLogResponse):
    """Audit log with entity information."""
    
    entity: Optional[Dict[str, Any]] = Field(
        None,
        description="Entity information associated with the audit log"
    )


class AuditLogWithDetails(AuditLogResponse):
    """Audit log with full contextual information."""
    
    user: Optional[Dict[str, Any]] = Field(
        None,
        description="User information associated with the audit log"
    )
    entity: Optional[Dict[str, Any]] = Field(
        None,
        description="Entity information associated with the audit log"
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context information"
    )


class AuditLogFilters(BaseModel):
    """Schema for filtering audit logs."""
    
    action_types: Optional[List[ActionType]] = Field(
        None,
        description="Filter by action types"
    )
    entity_types: Optional[List[EntityType]] = Field(
        None,
        description="Filter by entity types"
    )
    entity_ids: Optional[List[UUID]] = Field(
        None,
        description="Filter by entity IDs"
    )
    user_ids: Optional[List[UUID]] = Field(
        None,
        description="Filter by user IDs"
    )
    levels: Optional[List[LogLevel]] = Field(
        None,
        description="Filter by log levels"
    )
    ip_addresses: Optional[List[str]] = Field(
        None,
        description="Filter by IP addresses"
    )
    sources: Optional[List[str]] = Field(
        None,
        description="Filter by source systems"
    )
    tags: Optional[List[str]] = Field(
        None,
        description="Filter by tags (any match)"
    )
    session_ids: Optional[List[str]] = Field(
        None,
        description="Filter by session IDs"
    )
    request_ids: Optional[List[str]] = Field(
        None,
        description="Filter by request IDs"
    )
    date_from: Optional[datetime] = Field(
        None,
        description="Filter logs from this date"
    )
    date_to: Optional[datetime] = Field(
        None,
        description="Filter logs until this date"
    )
    search_query: Optional[str] = Field(
        None,
        max_length=500,
        description="Search in messages and details"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "action_types": ["user_created", "user_updated"],
                "entity_types": ["user"],
                "levels": ["info", "warning"],
                "date_from": "2025-10-01T00:00:00Z",
                "date_to": "2025-10-05T23:59:59Z",
                "search_query": "failed login",
                "tags": ["security", "authentication"]
            }
        }
    )


class AuditLogStatistics(BaseModel):
    """Statistics for audit logs."""
    
    total_logs: int = Field(..., description="Total number of audit logs")
    logs_by_level: Dict[LogLevel, int] = Field(
        ...,
        description="Count of logs by severity level"
    )
    logs_by_action_type: Dict[ActionType, int] = Field(
        ...,
        description="Count of logs by action type"
    )
    logs_by_entity_type: Dict[EntityType, int] = Field(
        ...,
        description="Count of logs by entity type"
    )
    logs_by_source: Dict[str, int] = Field(
        ...,
        description="Count of logs by source system"
    )
    top_users: List[Dict[str, Union[UUID, int]]] = Field(
        ...,
        description="Users with most audit activity"
    )
    top_ip_addresses: List[Dict[str, Union[str, int]]] = Field(
        ...,
        description="IP addresses with most activity"
    )
    activity_timeline: List[Dict[str, Union[datetime, int]]] = Field(
        ...,
        description="Activity timeline by date"
    )
    error_rate: float = Field(
        ...,
        description="Percentage of error-level logs"
    )
    recent_errors: List[AuditLogSummary] = Field(
        ...,
        description="Recent error and critical logs"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_logs": 15420,
                "logs_by_level": {
                    "info": 12340,
                    "warning": 2080,
                    "error": 800,
                    "critical": 200
                },
                "logs_by_action_type": {
                    "login": 5000,
                    "user_created": 500,
                    "bet_placed": 3000
                },
                "logs_by_entity_type": {
                    "user": 6000,
                    "bet": 4000,
                    "group": 1000
                },
                "error_rate": 6.5,
                "activity_timeline": [
                    {"date": "2025-10-01T00:00:00Z", "count": 3000},
                    {"date": "2025-10-02T00:00:00Z", "count": 3200}
                ]
            }
        }
    )


class AuditLogAnalytics(BaseModel):
    """Advanced analytics for audit logs."""
    
    security_events: Dict[str, int] = Field(
        ...,
        description="Count of security-related events"
    )
    failed_login_attempts: int = Field(
        ...,
        description="Number of failed login attempts"
    )
    suspicious_ips: List[Dict[str, Union[str, int]]] = Field(
        ...,
        description="IP addresses with suspicious activity"
    )
    user_activity_patterns: Dict[str, Any] = Field(
        ...,
        description="User activity patterns and insights"
    )
    system_health_indicators: Dict[str, Any] = Field(
        ...,
        description="System health metrics from logs"
    )
    compliance_metrics: Dict[str, Any] = Field(
        ...,
        description="Compliance and regulatory metrics"
    )
    anomaly_detection: List[Dict[str, Any]] = Field(
        ...,
        description="Detected anomalies in audit data"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "security_events": {
                    "failed_logins": 120,
                    "permission_denied": 45,
                    "suspicious_activity": 8
                },
                "failed_login_attempts": 120,
                "suspicious_ips": [
                    {"ip": "192.168.1.100", "attempts": 50},
                    {"ip": "10.0.0.5", "attempts": 25}
                ],
                "system_health_indicators": {
                    "error_rate": 2.5,
                    "uptime": 99.9,
                    "performance_issues": 3
                }
            }
        }
    )


class AuditLogExport(BaseModel):
    """Schema for audit log export requests."""
    
    format: str = Field(
        default="json",
        description="Export format (json, csv, xml)"
    )
    filters: Optional[AuditLogFilters] = Field(
        None,
        description="Filters to apply to the export"
    )
    include_details: bool = Field(
        default=True,
        description="Include detailed information in export"
    )
    compress: bool = Field(
        default=False,
        description="Compress the export file"
    )
    
    @field_validator('format')
    @classmethod
    def validate_format(cls, v):
        """Validate export format."""
        allowed_formats = ['json', 'csv', 'xml', 'xlsx']
        if v.lower() not in allowed_formats:
            raise ValueError(f"Format must be one of: {', '.join(allowed_formats)}")
        return v.lower()


class AuditLogExportResponse(BaseModel):
    """Response for audit log export requests."""
    
    export_id: UUID = Field(..., description="Unique identifier for the export")
    status: str = Field(..., description="Export status (pending, processing, completed, failed)")
    file_url: Optional[str] = Field(None, description="URL to download the export file")
    file_size: Optional[int] = Field(None, description="Size of the export file in bytes")
    record_count: Optional[int] = Field(None, description="Number of records in the export")
    created_at: datetime = Field(..., description="Export creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Export expiration timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class AuditLogBulkCreate(BaseModel):
    """Schema for bulk audit log creation."""
    
    logs: List[AuditLogCreate] = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="List of audit logs to create"
    )
    batch_id: Optional[str] = Field(
        None,
        max_length=255,
        description="Batch identifier for grouping related logs"
    )
    source: str = Field(
        ...,
        max_length=100,
        description="Source system for all logs in this batch"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "logs": [
                    {
                        "action_type": "user_created",
                        "entity_type": "user",
                        "message": "User created successfully"
                    },
                    {
                        "action_type": "group_created",
                        "entity_type": "group",
                        "message": "Group created successfully"
                    }
                ],
                "batch_id": "batch_20251005_001",
                "source": "bulk_import"
            }
        }
    )


class AuditLogBulkResponse(BaseModel):
    """Response for bulk audit log operations."""
    
    created_count: int = Field(..., description="Number of logs successfully created")
    failed_count: int = Field(..., description="Number of logs that failed to create")
    batch_id: Optional[str] = Field(None, description="Batch identifier")
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Details of any creation failures"
    )
    processing_time: float = Field(
        ...,
        description="Time taken to process the bulk operation in seconds"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "created_count": 95,
                "failed_count": 5,
                "batch_id": "batch_20251005_001",
                "errors": [
                    {
                        "index": 10,
                        "error": "Invalid entity_id format",
                        "log_data": {"action_type": "user_created"}
                    }
                ],
                "processing_time": 2.5
            }
        }
    )


class AuditLogArchive(BaseModel):
    """Schema for audit log archiving requests."""
    
    archive_before: datetime = Field(
        ...,
        description="Archive logs created before this date"
    )
    archive_levels: Optional[List[LogLevel]] = Field(
        None,
        description="Archive only logs with these levels"
    )
    archive_action_types: Optional[List[ActionType]] = Field(
        None,
        description="Archive only logs with these action types"
    )
    compress: bool = Field(
        default=True,
        description="Compress archived logs"
    )
    retention_days: int = Field(
        default=2555,  # 7 years
        ge=1,
        le=3650,
        description="Number of days to retain archived logs"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "archive_before": "2025-01-01T00:00:00Z",
                "archive_levels": ["debug", "info"],
                "compress": True,
                "retention_days": 2555
            }
        }
    )


class AuditLogArchiveResponse(BaseModel):
    """Response for audit log archiving operations."""
    
    archive_id: UUID = Field(..., description="Unique identifier for the archive")
    archived_count: int = Field(..., description="Number of logs archived")
    archive_size: int = Field(..., description="Size of the archive in bytes")
    archive_path: str = Field(..., description="Path to the archive file")
    created_at: datetime = Field(..., description="Archive creation timestamp")
    expires_at: datetime = Field(..., description="Archive expiration timestamp")
    
    model_config = ConfigDict(from_attributes=True)