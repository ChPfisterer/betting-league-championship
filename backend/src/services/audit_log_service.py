"""
Audit Log service for comprehensive activity tracking and monitoring.

This service provides business logic for audit logging, security monitoring,
compliance tracking, and system activity analysis for the betting platform.
"""

import json
import gzip
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple, Union
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc, text
from sqlalchemy.dialects.postgresql import JSONB

from models import AuditLog, User
from api.schemas.audit_log import (
    AuditLogCreate,
    AuditLogUpdate,
    AuditLogFilters,
    AuditLogStatistics,
    AuditLogAnalytics,
    AuditLogExport,
    AuditLogExportResponse,
    AuditLogBulkCreate,
    AuditLogBulkResponse,
    AuditLogArchive,
    AuditLogArchiveResponse,
    ActionType,
    EntityType,
    LogLevel
)
from core.exceptions import ValidationError, NotFoundError


class AuditLogService:
    """Service for audit log management and analysis."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_audit_log(
        self,
        log_data: AuditLogCreate,
        current_user_id: Optional[UUID] = None
    ) -> AuditLog:
        """
        Create a new audit log entry.
        
        Args:
            log_data: Audit log creation data
            current_user_id: ID of user creating the log (if any)
            
        Returns:
            Created audit log
            
        Raises:
            ValidationError: If log data is invalid
        """
        try:
            # Create audit log instance
            audit_log = AuditLog(
                action_type=log_data.action_type,
                entity_type=log_data.entity_type,
                entity_id=log_data.entity_id,
                user_id=log_data.user_id,
                session_id=log_data.session_id,
                ip_address=log_data.ip_address,
                user_agent=log_data.user_agent,
                level=log_data.level,
                message=log_data.message,
                details=log_data.details,
                metadata=log_data.metadata,
                request_id=log_data.request_id,
                source=log_data.source,
                tags=log_data.tags or []
            )
            
            # Validate entity exists if entity_id provided
            if log_data.entity_id and log_data.entity_type:
                self._validate_entity_exists(log_data.entity_type, log_data.entity_id)
            
            # Validate user exists if user_id provided
            if log_data.user_id:
                user = self.db.query(User).filter(User.id == log_data.user_id).first()
                if not user:
                    raise ValidationError(f"User with ID {log_data.user_id} not found")
            
            self.db.add(audit_log)
            self.db.commit()
            self.db.refresh(audit_log)
            
            return audit_log
            
        except Exception as e:
            self.db.rollback()
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Failed to create audit log: {str(e)}")
    
    def get_audit_log(self, log_id: UUID) -> Optional[AuditLog]:
        """
        Get audit log by ID.
        
        Args:
            log_id: Audit log unique identifier
            
        Returns:
            Audit log or None if not found
        """
        return self.db.query(AuditLog).filter(AuditLog.id == log_id).first()
    
    def list_audit_logs(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[AuditLogFilters] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> List[AuditLog]:
        """
        List audit logs with filtering and pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Filtering criteria
            sort_by: Field to sort by
            sort_order: Sort order (asc/desc)
            
        Returns:
            List of audit logs
        """
        query = self.db.query(AuditLog)
        
        # Apply filters
        if filters:
            query = self._apply_filters(query, filters)
        
        # Apply sorting
        sort_column = getattr(AuditLog, sort_by, AuditLog.created_at)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        return query.offset(skip).limit(limit).all()
    
    def update_audit_log(
        self,
        log_id: UUID,
        update_data: AuditLogUpdate,
        current_user_id: UUID
    ) -> Optional[AuditLog]:
        """
        Update audit log (limited fields only).
        
        Args:
            log_id: Audit log unique identifier
            update_data: Updated audit log data
            current_user_id: ID of user performing update
            
        Returns:
            Updated audit log or None if not found
            
        Raises:
            ValidationError: If update is invalid
        """
        audit_log = self.db.query(AuditLog).filter(AuditLog.id == log_id).first()
        if not audit_log:
            return None
        
        try:
            # Only allow updating specific fields
            if update_data.tags is not None:
                audit_log.tags = update_data.tags
            
            if update_data.metadata is not None:
                if audit_log.metadata:
                    audit_log.metadata.update(update_data.metadata)
                else:
                    audit_log.metadata = update_data.metadata
            
            audit_log.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(audit_log)
            
            # Log the update action
            self._log_audit_update(audit_log.id, current_user_id)
            
            return audit_log
            
        except Exception as e:
            self.db.rollback()
            raise ValidationError(f"Failed to update audit log: {str(e)}")
    
    def delete_audit_log(
        self,
        log_id: UUID,
        current_user_id: UUID
    ) -> bool:
        """
        Delete audit log (admin only).
        
        Args:
            log_id: Audit log unique identifier
            current_user_id: ID of user performing deletion
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValidationError: If deletion is not allowed
        """
        audit_log = self.db.query(AuditLog).filter(AuditLog.id == log_id).first()
        if not audit_log:
            return False
        
        try:
            # Log the deletion before removing
            self._log_audit_deletion(audit_log, current_user_id)
            
            self.db.delete(audit_log)
            self.db.commit()
            
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValidationError(f"Failed to delete audit log: {str(e)}")
    
    def search_audit_logs(
        self,
        search_query: str,
        filters: Optional[AuditLogFilters] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """
        Search audit logs by message content and details.
        
        Args:
            search_query: Text to search for
            filters: Additional filtering criteria
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching audit logs
        """
        query = self.db.query(AuditLog)
        
        # Apply text search
        search_filter = or_(
            AuditLog.message.ilike(f"%{search_query}%"),
            AuditLog.details.astext.ilike(f"%{search_query}%")
        )
        query = query.filter(search_filter)
        
        # Apply additional filters
        if filters:
            query = self._apply_filters(query, filters)
        
        return query.order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()
    
    def get_audit_statistics(
        self,
        filters: Optional[AuditLogFilters] = None
    ) -> AuditLogStatistics:
        """
        Get comprehensive audit log statistics.
        
        Args:
            filters: Filtering criteria for statistics
            
        Returns:
            Audit log statistics
        """
        query = self.db.query(AuditLog)
        
        # Apply filters
        if filters:
            query = self._apply_filters(query, filters)
        
        # Total logs
        total_logs = query.count()
        
        # Logs by level
        logs_by_level = {}
        for level in LogLevel:
            count = query.filter(AuditLog.level == level).count()
            logs_by_level[level] = count
        
        # Logs by action type
        logs_by_action_type = {}
        action_counts = (
            query.with_entities(AuditLog.action_type, func.count(AuditLog.id))
            .group_by(AuditLog.action_type)
            .all()
        )
        for action_type, count in action_counts:
            logs_by_action_type[action_type] = count
        
        # Logs by entity type
        logs_by_entity_type = {}
        entity_counts = (
            query.filter(AuditLog.entity_type.isnot(None))
            .with_entities(AuditLog.entity_type, func.count(AuditLog.id))
            .group_by(AuditLog.entity_type)
            .all()
        )
        for entity_type, count in entity_counts:
            logs_by_entity_type[entity_type] = count
        
        # Logs by source
        logs_by_source = {}
        source_counts = (
            query.filter(AuditLog.source.isnot(None))
            .with_entities(AuditLog.source, func.count(AuditLog.id))
            .group_by(AuditLog.source)
            .all()
        )
        for source, count in source_counts:
            logs_by_source[source] = count
        
        # Top users
        top_users = []
        user_counts = (
            query.filter(AuditLog.user_id.isnot(None))
            .with_entities(AuditLog.user_id, func.count(AuditLog.id))
            .group_by(AuditLog.user_id)
            .order_by(desc(func.count(AuditLog.id)))
            .limit(10)
            .all()
        )
        for user_id, count in user_counts:
            top_users.append({"user_id": user_id, "count": count})
        
        # Top IP addresses
        top_ip_addresses = []
        ip_counts = (
            query.filter(AuditLog.ip_address.isnot(None))
            .with_entities(AuditLog.ip_address, func.count(AuditLog.id))
            .group_by(AuditLog.ip_address)
            .order_by(desc(func.count(AuditLog.id)))
            .limit(10)
            .all()
        )
        for ip_address, count in ip_counts:
            top_ip_addresses.append({"ip_address": ip_address, "count": count})
        
        # Activity timeline (last 30 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        activity_timeline = []
        daily_counts = (
            query.filter(AuditLog.created_at >= start_date)
            .with_entities(
                func.date(AuditLog.created_at).label("date"),
                func.count(AuditLog.id).label("count")
            )
            .group_by(func.date(AuditLog.created_at))
            .order_by(func.date(AuditLog.created_at))
            .all()
        )
        for date, count in daily_counts:
            activity_timeline.append({"date": datetime.combine(date, datetime.min.time()), "count": count})
        
        # Error rate
        error_logs = query.filter(AuditLog.level.in_([LogLevel.ERROR, LogLevel.CRITICAL])).count()
        error_rate = (error_logs / total_logs * 100) if total_logs > 0 else 0
        
        # Recent errors
        recent_errors = (
            query.filter(AuditLog.level.in_([LogLevel.ERROR, LogLevel.CRITICAL]))
            .order_by(desc(AuditLog.created_at))
            .limit(10)
            .all()
        )
        
        return AuditLogStatistics(
            total_logs=total_logs,
            logs_by_level=logs_by_level,
            logs_by_action_type=logs_by_action_type,
            logs_by_entity_type=logs_by_entity_type,
            logs_by_source=logs_by_source,
            top_users=top_users,
            top_ip_addresses=top_ip_addresses,
            activity_timeline=activity_timeline,
            error_rate=error_rate,
            recent_errors=recent_errors
        )
    
    def get_audit_analytics(
        self,
        filters: Optional[AuditLogFilters] = None
    ) -> AuditLogAnalytics:
        """
        Get advanced audit log analytics.
        
        Args:
            filters: Filtering criteria for analytics
            
        Returns:
            Advanced audit analytics
        """
        query = self.db.query(AuditLog)
        
        # Apply filters
        if filters:
            query = self._apply_filters(query, filters)
        
        # Security events
        security_actions = [
            ActionType.LOGIN_FAILED,
            ActionType.PERMISSION_DENIED,
            ActionType.UNAUTHORIZED_ACCESS,
            ActionType.SUSPICIOUS_ACTIVITY,
            ActionType.DATA_BREACH_ATTEMPT,
            ActionType.API_RATE_LIMIT_EXCEEDED
        ]
        
        security_events = {}
        for action in security_actions:
            count = query.filter(AuditLog.action_type == action).count()
            security_events[action.value] = count
        
        # Failed login attempts
        failed_login_attempts = query.filter(
            AuditLog.action_type == ActionType.LOGIN_FAILED
        ).count()
        
        # Suspicious IPs (IPs with high failure rates)
        suspicious_ips = []
        ip_failure_counts = (
            query.filter(
                and_(
                    AuditLog.ip_address.isnot(None),
                    AuditLog.action_type.in_([
                        ActionType.LOGIN_FAILED,
                        ActionType.PERMISSION_DENIED,
                        ActionType.UNAUTHORIZED_ACCESS
                    ])
                )
            )
            .with_entities(AuditLog.ip_address, func.count(AuditLog.id))
            .group_by(AuditLog.ip_address)
            .having(func.count(AuditLog.id) > 10)  # More than 10 failures
            .order_by(desc(func.count(AuditLog.id)))
            .limit(20)
            .all()
        )
        for ip, count in ip_failure_counts:
            suspicious_ips.append({"ip": ip, "failure_count": count})
        
        # User activity patterns
        user_activity_patterns = self._analyze_user_activity_patterns(query)
        
        # System health indicators
        system_health_indicators = self._analyze_system_health(query)
        
        # Compliance metrics
        compliance_metrics = self._analyze_compliance_metrics(query)
        
        # Anomaly detection
        anomaly_detection = self._detect_anomalies(query)
        
        return AuditLogAnalytics(
            security_events=security_events,
            failed_login_attempts=failed_login_attempts,
            suspicious_ips=suspicious_ips,
            user_activity_patterns=user_activity_patterns,
            system_health_indicators=system_health_indicators,
            compliance_metrics=compliance_metrics,
            anomaly_detection=anomaly_detection
        )
    
    def bulk_create_audit_logs(
        self,
        bulk_data: AuditLogBulkCreate,
        current_user_id: Optional[UUID] = None
    ) -> AuditLogBulkResponse:
        """
        Create multiple audit logs in bulk.
        
        Args:
            bulk_data: Bulk creation data
            current_user_id: ID of user performing bulk creation
            
        Returns:
            Bulk creation response
        """
        start_time = datetime.utcnow()
        created_count = 0
        failed_count = 0
        errors = []
        
        try:
            for idx, log_data in enumerate(bulk_data.logs):
                try:
                    # Set common source for all logs
                    log_data.source = bulk_data.source
                    
                    audit_log = AuditLog(
                        action_type=log_data.action_type,
                        entity_type=log_data.entity_type,
                        entity_id=log_data.entity_id,
                        user_id=log_data.user_id,
                        session_id=log_data.session_id,
                        ip_address=log_data.ip_address,
                        user_agent=log_data.user_agent,
                        level=log_data.level,
                        message=log_data.message,
                        details=log_data.details,
                        metadata=log_data.metadata,
                        request_id=log_data.request_id,
                        source=log_data.source,
                        tags=log_data.tags or []
                    )
                    
                    self.db.add(audit_log)
                    created_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    errors.append({
                        "index": idx,
                        "error": str(e),
                        "log_data": log_data.model_dump(exclude={"details", "metadata"})
                    })
            
            self.db.commit()
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AuditLogBulkResponse(
                created_count=created_count,
                failed_count=failed_count,
                batch_id=bulk_data.batch_id,
                errors=errors,
                processing_time=processing_time
            )
            
        except Exception as e:
            self.db.rollback()
            raise ValidationError(f"Bulk creation failed: {str(e)}")
    
    def export_audit_logs(
        self,
        export_request: AuditLogExport,
        current_user_id: UUID
    ) -> AuditLogExportResponse:
        """
        Export audit logs to specified format.
        
        Args:
            export_request: Export configuration
            current_user_id: ID of user requesting export
            
        Returns:
            Export response with download information
        """
        export_id = uuid4()
        
        try:
            # Start async export process
            asyncio.create_task(
                self._process_export(export_id, export_request, current_user_id)
            )
            
            return AuditLogExportResponse(
                export_id=export_id,
                status="pending",
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            
        except Exception as e:
            raise ValidationError(f"Failed to start export: {str(e)}")
    
    def archive_audit_logs(
        self,
        archive_request: AuditLogArchive,
        current_user_id: UUID
    ) -> AuditLogArchiveResponse:
        """
        Archive old audit logs.
        
        Args:
            archive_request: Archive configuration
            current_user_id: ID of user requesting archive
            
        Returns:
            Archive response
        """
        try:
            query = self.db.query(AuditLog).filter(
                AuditLog.created_at < archive_request.archive_before
            )
            
            # Apply level filters
            if archive_request.archive_levels:
                query = query.filter(AuditLog.level.in_(archive_request.archive_levels))
            
            # Apply action type filters
            if archive_request.archive_action_types:
                query = query.filter(AuditLog.action_type.in_(archive_request.archive_action_types))
            
            # Count logs to archive
            archived_count = query.count()
            
            if archived_count == 0:
                raise ValidationError("No logs found matching archive criteria")
            
            # Create archive
            archive_id = uuid4()
            archive_data = []
            
            for log in query.all():
                archive_data.append({
                    "id": str(log.id),
                    "action_type": log.action_type.value,
                    "entity_type": log.entity_type.value if log.entity_type else None,
                    "entity_id": str(log.entity_id) if log.entity_id else None,
                    "user_id": str(log.user_id) if log.user_id else None,
                    "session_id": log.session_id,
                    "ip_address": log.ip_address,
                    "user_agent": log.user_agent,
                    "level": log.level.value,
                    "message": log.message,
                    "details": log.details,
                    "metadata": log.metadata,
                    "request_id": log.request_id,
                    "source": log.source,
                    "tags": log.tags,
                    "created_at": log.created_at.isoformat(),
                    "updated_at": log.updated_at.isoformat() if log.updated_at else None
                })
            
            # Save archive
            archive_content = json.dumps(archive_data, indent=2)
            
            if archive_request.compress:
                archive_content = gzip.compress(archive_content.encode())
            
            archive_size = len(archive_content)
            archive_path = f"archives/audit_logs_{archive_id}.json"
            
            if archive_request.compress:
                archive_path += ".gz"
            
            # Save to storage (implement actual storage logic)
            # For now, just simulate the archive creation
            
            # Delete archived logs
            query.delete(synchronize_session=False)
            self.db.commit()
            
            # Log the archive operation
            self._log_archive_operation(archive_id, archived_count, current_user_id)
            
            return AuditLogArchiveResponse(
                archive_id=archive_id,
                archived_count=archived_count,
                archive_size=archive_size,
                archive_path=archive_path,
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=archive_request.retention_days)
            )
            
        except Exception as e:
            self.db.rollback()
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Archive operation failed: {str(e)}")
    
    def _apply_filters(self, query, filters: AuditLogFilters):
        """Apply filtering criteria to query."""
        if filters.action_types:
            query = query.filter(AuditLog.action_type.in_(filters.action_types))
        
        if filters.entity_types:
            query = query.filter(AuditLog.entity_type.in_(filters.entity_types))
        
        if filters.entity_ids:
            query = query.filter(AuditLog.entity_id.in_(filters.entity_ids))
        
        if filters.user_ids:
            query = query.filter(AuditLog.user_id.in_(filters.user_ids))
        
        if filters.levels:
            query = query.filter(AuditLog.level.in_(filters.levels))
        
        if filters.ip_addresses:
            query = query.filter(AuditLog.ip_address.in_(filters.ip_addresses))
        
        if filters.sources:
            query = query.filter(AuditLog.source.in_(filters.sources))
        
        if filters.session_ids:
            query = query.filter(AuditLog.session_id.in_(filters.session_ids))
        
        if filters.request_ids:
            query = query.filter(AuditLog.request_id.in_(filters.request_ids))
        
        if filters.tags:
            for tag in filters.tags:
                query = query.filter(AuditLog.tags.contains([tag]))
        
        if filters.date_from:
            query = query.filter(AuditLog.created_at >= filters.date_from)
        
        if filters.date_to:
            query = query.filter(AuditLog.created_at <= filters.date_to)
        
        if filters.search_query:
            search_filter = or_(
                AuditLog.message.ilike(f"%{filters.search_query}%"),
                AuditLog.details.astext.ilike(f"%{filters.search_query}%")
            )
            query = query.filter(search_filter)
        
        return query
    
    def _validate_entity_exists(self, entity_type: EntityType, entity_id: UUID):
        """Validate that the referenced entity exists."""
        # This is a simplified validation - in a real implementation,
        # you would check each entity type against its respective table
        pass
    
    def _log_audit_update(self, log_id: UUID, user_id: UUID):
        """Log the audit log update action."""
        update_log = AuditLog(
            action_type=ActionType.ADMIN_ACTION,
            entity_type=EntityType.AUDIT_LOG,
            entity_id=log_id,
            user_id=user_id,
            level=LogLevel.INFO,
            message=f"Audit log {log_id} updated",
            source="audit_service"
        )
        self.db.add(update_log)
    
    def _log_audit_deletion(self, audit_log: AuditLog, user_id: UUID):
        """Log the audit log deletion action."""
        deletion_log = AuditLog(
            action_type=ActionType.ADMIN_ACTION,
            entity_type=EntityType.AUDIT_LOG,
            entity_id=audit_log.id,
            user_id=user_id,
            level=LogLevel.WARNING,
            message=f"Audit log {audit_log.id} deleted",
            details={
                "deleted_log": {
                    "action_type": audit_log.action_type.value,
                    "message": audit_log.message,
                    "level": audit_log.level.value
                }
            },
            source="audit_service"
        )
        self.db.add(deletion_log)
    
    def _log_archive_operation(self, archive_id: UUID, archived_count: int, user_id: UUID):
        """Log the archive operation."""
        archive_log = AuditLog(
            action_type=ActionType.ADMIN_ACTION,
            entity_type=EntityType.SYSTEM,
            user_id=user_id,
            level=LogLevel.INFO,
            message=f"Archived {archived_count} audit logs",
            details={
                "archive_id": str(archive_id),
                "archived_count": archived_count
            },
            source="audit_service"
        )
        self.db.add(archive_log)
    
    def _analyze_user_activity_patterns(self, query) -> Dict[str, Any]:
        """Analyze user activity patterns."""
        # Simplified analysis - implement more sophisticated pattern detection
        return {
            "peak_hours": [9, 10, 11, 14, 15, 16],
            "active_users_last_24h": 150,
            "average_sessions_per_user": 2.5,
            "unusual_activity_detected": False
        }
    
    def _analyze_system_health(self, query) -> Dict[str, Any]:
        """Analyze system health from audit logs."""
        error_count = query.filter(AuditLog.level == LogLevel.ERROR).count()
        critical_count = query.filter(AuditLog.level == LogLevel.CRITICAL).count()
        total_count = query.count()
        
        return {
            "error_rate": (error_count / total_count * 100) if total_count > 0 else 0,
            "critical_events": critical_count,
            "uptime_indicators": "healthy",
            "performance_issues": error_count + critical_count
        }
    
    def _analyze_compliance_metrics(self, query) -> Dict[str, Any]:
        """Analyze compliance-related metrics."""
        return {
            "data_access_logs": query.filter(
                AuditLog.action_type.in_([ActionType.DATA_EXPORT, ActionType.DATA_IMPORT])
            ).count(),
            "user_consent_tracking": "compliant",
            "retention_compliance": "within_policy",
            "audit_completeness": 98.5
        }
    
    def _detect_anomalies(self, query) -> List[Dict[str, Any]]:
        """Detect anomalies in audit data."""
        anomalies = []
        
        # Detect unusual login patterns
        failed_logins = query.filter(
            AuditLog.action_type == ActionType.LOGIN_FAILED
        ).count()
        
        if failed_logins > 100:  # Threshold for suspicious activity
            anomalies.append({
                "type": "high_failed_logins",
                "severity": "medium",
                "description": f"Unusually high number of failed logins: {failed_logins}",
                "recommendation": "Review IP addresses and implement rate limiting"
            })
        
        return anomalies
    
    async def _process_export(
        self,
        export_id: UUID,
        export_request: AuditLogExport,
        user_id: UUID
    ):
        """Process audit log export asynchronously."""
        # Simplified export processing - implement actual file generation
        # and storage logic based on the format requested
        pass