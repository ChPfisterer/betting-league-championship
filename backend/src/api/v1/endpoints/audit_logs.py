"""
Audit Log API endpoints for comprehensive activity tracking and monitoring.

This module provides comprehensive CRUD operations for audit log management,
including security monitoring, compliance reporting, and system analytics
for the betting platform.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, http_not_found, http_conflict
from core.keycloak_security import get_current_user_hybrid
from models import User, AuditLog
from api.schemas.audit_log import (
    AuditLogCreate,
    AuditLogUpdate,
    AuditLogResponse,
    AuditLogSummary,
    AuditLogWithUser,
    AuditLogWithEntity,
    AuditLogWithDetails,
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
from services.audit_log_service import AuditLogService


router = APIRouter()


@router.post(
    "/",
    response_model=AuditLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Audit Log",
    description="Create a new audit log entry with comprehensive tracking"
)
async def create_audit_log(
    log_data: AuditLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogResponse:
    """
    Create a new audit log entry.
    
    Args:
        log_data: Audit log creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created audit log details
        
    Raises:
        HTTPException: If validation fails
    """
    service = AuditLogService(db)
    try:
        audit_log = service.create_audit_log(log_data, current_user.id)
        return AuditLogResponse.model_validate(audit_log)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=List[AuditLogSummary],
    summary="List Audit Logs",
    description="List audit logs with comprehensive filtering and pagination"
)
async def list_audit_logs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    action_type: Optional[ActionType] = Query(None, description="Filter by action type"),
    entity_type: Optional[EntityType] = Query(None, description="Filter by entity type"),
    entity_id: Optional[UUID] = Query(None, description="Filter by entity ID"),
    user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
    level: Optional[LogLevel] = Query(None, description="Filter by log level"),
    ip_address: Optional[str] = Query(None, description="Filter by IP address"),
    source: Optional[str] = Query(None, description="Filter by source system"),
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    request_id: Optional[str] = Query(None, description="Filter by request ID"),
    date_from: Optional[datetime] = Query(None, description="Filter logs from this date"),
    date_to: Optional[datetime] = Query(None, description="Filter logs until this date"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[AuditLogSummary]:
    """
    List audit logs with filtering options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        action_type: Filter by action type
        entity_type: Filter by entity type
        entity_id: Filter by entity ID
        user_id: Filter by user ID
        level: Filter by log level
        ip_address: Filter by IP address
        source: Filter by source system
        session_id: Filter by session ID
        request_id: Filter by request ID
        date_from: Filter logs from this date
        date_to: Filter logs until this date
        sort_by: Field to sort by
        sort_order: Sort order (asc/desc)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of audit log summaries
    """
    service = AuditLogService(db)
    
    # Build filters
    filters = AuditLogFilters(
        action_types=[action_type] if action_type else None,
        entity_types=[entity_type] if entity_type else None,
        entity_ids=[entity_id] if entity_id else None,
        user_ids=[user_id] if user_id else None,
        levels=[level] if level else None,
        ip_addresses=[ip_address] if ip_address else None,
        sources=[source] if source else None,
        session_ids=[session_id] if session_id else None,
        request_ids=[request_id] if request_id else None,
        date_from=date_from,
        date_to=date_to
    )
    
    audit_logs = service.list_audit_logs(
        skip=skip,
        limit=limit,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return [AuditLogSummary.model_validate(log) for log in audit_logs]


@router.get(
    "/{log_id}",
    response_model=AuditLogResponse,
    summary="Get Audit Log",
    description="Get audit log details by ID"
)
async def get_audit_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogResponse:
    """
    Get audit log by ID.
    
    Args:
        log_id: Audit log unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Audit log details
        
    Raises:
        HTTPException: If audit log not found
    """
    service = AuditLogService(db)
    audit_log = service.get_audit_log(log_id)
    
    if not audit_log:
        raise http_not_found(f"Audit log with ID {log_id} not found")
        
    return AuditLogResponse.model_validate(audit_log)


@router.get(
    "/{log_id}/with-user",
    response_model=AuditLogWithUser,
    summary="Get Audit Log with User",
    description="Get audit log details including user information"
)
async def get_audit_log_with_user(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogWithUser:
    """
    Get audit log with user details.
    
    Args:
        log_id: Audit log unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Audit log details with user information
        
    Raises:
        HTTPException: If audit log not found
    """
    service = AuditLogService(db)
    audit_log = service.get_audit_log(log_id)
    
    if not audit_log:
        raise http_not_found(f"Audit log with ID {log_id} not found")
    
    # Load user relationship
    user = None
    if audit_log.user_id:
        user = db.query(User).filter(User.id == audit_log.user_id).first()
    
    log_dict = AuditLogResponse.model_validate(audit_log).model_dump()
    log_dict['user'] = user
    
    return AuditLogWithUser.model_validate(log_dict)


@router.get(
    "/{log_id}/with-details",
    response_model=AuditLogWithDetails,
    summary="Get Audit Log with Full Context",
    description="Get audit log with user, entity, and contextual information"
)
async def get_audit_log_with_details(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogWithDetails:
    """
    Get audit log with full contextual information.
    
    Args:
        log_id: Audit log unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Audit log details with full context
        
    Raises:
        HTTPException: If audit log not found
    """
    service = AuditLogService(db)
    audit_log = service.get_audit_log(log_id)
    
    if not audit_log:
        raise http_not_found(f"Audit log with ID {log_id} not found")
    
    # Load related entities
    user = None
    if audit_log.user_id:
        user = db.query(User).filter(User.id == audit_log.user_id).first()
    
    # Entity loading would depend on entity_type
    entity = None
    
    # Additional context
    context = {
        "related_logs_count": db.query(AuditLog).filter(
            AuditLog.session_id == audit_log.session_id
        ).count() if audit_log.session_id else 0,
        "ip_activity_count": db.query(AuditLog).filter(
            AuditLog.ip_address == audit_log.ip_address
        ).count() if audit_log.ip_address else 0
    }
    
    log_dict = AuditLogResponse.model_validate(audit_log).model_dump()
    log_dict.update({
        'user': user,
        'entity': entity,
        'context': context
    })
    
    return AuditLogWithDetails.model_validate(log_dict)


@router.get(
    "/statistics/overview",
    response_model=AuditLogStatistics,
    summary="Get Audit Statistics",
    description="Get comprehensive audit log statistics and metrics"
)
async def get_audit_statistics(
    date_from: Optional[datetime] = Query(None, description="Statistics from this date"),
    date_to: Optional[datetime] = Query(None, description="Statistics until this date"),
    action_types: Optional[List[ActionType]] = Query(None, description="Filter by action types"),
    entity_types: Optional[List[EntityType]] = Query(None, description="Filter by entity types"),
    levels: Optional[List[LogLevel]] = Query(None, description="Filter by log levels"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogStatistics:
    """
    Get comprehensive audit log statistics.
    
    Args:
        date_from: Statistics from this date
        date_to: Statistics until this date
        action_types: Filter by action types
        entity_types: Filter by entity types
        levels: Filter by log levels
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Comprehensive audit log statistics
    """
    service = AuditLogService(db)
    
    filters = AuditLogFilters(
        date_from=date_from,
        date_to=date_to,
        action_types=action_types,
        entity_types=entity_types,
        levels=levels
    )
    
    return service.get_audit_statistics(filters)


@router.get(
    "/analytics/security",
    response_model=AuditLogAnalytics,
    summary="Get Security Analytics",
    description="Get advanced security analytics and insights"
)
async def get_security_analytics(
    date_from: Optional[datetime] = Query(None, description="Analytics from this date"),
    date_to: Optional[datetime] = Query(None, description="Analytics until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogAnalytics:
    """
    Get advanced security analytics.
    
    Args:
        date_from: Analytics from this date
        date_to: Analytics until this date
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Advanced security analytics
    """
    service = AuditLogService(db)
    
    filters = AuditLogFilters(
        date_from=date_from,
        date_to=date_to
    )
    
    return service.get_audit_analytics(filters)


@router.put(
    "/{log_id}",
    response_model=AuditLogResponse,
    summary="Update Audit Log",
    description="Update audit log (limited fields only)"
)
async def update_audit_log(
    log_id: UUID,
    update_data: AuditLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogResponse:
    """
    Update audit log (limited fields only).
    
    Args:
        log_id: Audit log unique identifier
        update_data: Updated audit log data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated audit log details
        
    Raises:
        HTTPException: If audit log not found or cannot be updated
    """
    service = AuditLogService(db)
    try:
        audit_log = service.update_audit_log(log_id, update_data, current_user.id)
        if not audit_log:
            raise http_not_found(f"Audit log with ID {log_id} not found")
        return AuditLogResponse.model_validate(audit_log)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/search",
    response_model=List[AuditLogSummary],
    summary="Search Audit Logs",
    description="Search audit logs with advanced filtering and text search"
)
async def search_audit_logs(
    filters: AuditLogFilters,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[AuditLogSummary]:
    """
    Search audit logs with advanced filtering.
    
    Args:
        filters: Search and filter criteria
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of matching audit logs
    """
    service = AuditLogService(db)
    
    if filters.search_query:
        audit_logs = service.search_audit_logs(
            search_query=filters.search_query,
            filters=filters,
            skip=skip,
            limit=limit
        )
    else:
        audit_logs = service.list_audit_logs(
            skip=skip,
            limit=limit,
            filters=filters
        )
    
    return [AuditLogSummary.model_validate(log) for log in audit_logs]


@router.post(
    "/bulk",
    response_model=AuditLogBulkResponse,
    summary="Bulk Create Audit Logs",
    description="Create multiple audit logs in a single operation"
)
async def bulk_create_audit_logs(
    bulk_data: AuditLogBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogBulkResponse:
    """
    Create multiple audit logs in bulk.
    
    Args:
        bulk_data: Bulk creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Bulk creation summary
    """
    service = AuditLogService(db)
    try:
        result = service.bulk_create_audit_logs(bulk_data, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/export",
    response_model=AuditLogExportResponse,
    summary="Export Audit Logs",
    description="Export audit logs to specified format"
)
async def export_audit_logs(
    export_request: AuditLogExport,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogExportResponse:
    """
    Export audit logs to specified format.
    
    Args:
        export_request: Export configuration
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Export response with download information
    """
    service = AuditLogService(db)
    try:
        result = service.export_audit_logs(export_request, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/archive",
    response_model=AuditLogArchiveResponse,
    summary="Archive Audit Logs",
    description="Archive old audit logs for long-term storage"
)
async def archive_audit_logs(
    archive_request: AuditLogArchive,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> AuditLogArchiveResponse:
    """
    Archive old audit logs.
    
    Args:
        archive_request: Archive configuration
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Archive response
    """
    service = AuditLogService(db)
    try:
        result = service.archive_audit_logs(archive_request, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/user/{user_id}/activity",
    response_model=List[AuditLogSummary],
    summary="Get User Activity",
    description="Get audit logs for a specific user"
)
async def get_user_activity(
    user_id: UUID,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    action_types: Optional[List[ActionType]] = Query(None, description="Filter by action types"),
    date_from: Optional[datetime] = Query(None, description="Activity from this date"),
    date_to: Optional[datetime] = Query(None, description="Activity until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[AuditLogSummary]:
    """
    Get audit logs for a specific user.
    
    Args:
        user_id: User unique identifier
        skip: Number of records to skip
        limit: Maximum number of records to return
        action_types: Filter by action types
        date_from: Activity from this date
        date_to: Activity until this date
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of user's audit logs
    """
    service = AuditLogService(db)
    
    filters = AuditLogFilters(
        user_ids=[user_id],
        action_types=action_types,
        date_from=date_from,
        date_to=date_to
    )
    
    audit_logs = service.list_audit_logs(
        skip=skip,
        limit=limit,
        filters=filters
    )
    return [AuditLogSummary.model_validate(log) for log in audit_logs]


@router.get(
    "/entity/{entity_type}/{entity_id}/history",
    response_model=List[AuditLogSummary],
    summary="Get Entity History",
    description="Get audit logs for a specific entity"
)
async def get_entity_history(
    entity_type: EntityType,
    entity_id: UUID,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    action_types: Optional[List[ActionType]] = Query(None, description="Filter by action types"),
    date_from: Optional[datetime] = Query(None, description="History from this date"),
    date_to: Optional[datetime] = Query(None, description="History until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> List[AuditLogSummary]:
    """
    Get audit logs for a specific entity.
    
    Args:
        entity_type: Type of entity
        entity_id: Entity unique identifier
        skip: Number of records to skip
        limit: Maximum number of records to return
        action_types: Filter by action types
        date_from: History from this date
        date_to: History until this date
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of entity's audit logs
    """
    service = AuditLogService(db)
    
    filters = AuditLogFilters(
        entity_types=[entity_type],
        entity_ids=[entity_id],
        action_types=action_types,
        date_from=date_from,
        date_to=date_to
    )
    
    audit_logs = service.list_audit_logs(
        skip=skip,
        limit=limit,
        filters=filters
    )
    return [AuditLogSummary.model_validate(log) for log in audit_logs]


@router.delete(
    "/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Audit Log",
    description="Delete an audit log (admin only)"
)
async def delete_audit_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_hybrid)
) -> None:
    """
    Delete audit log (admin only).
    
    Args:
        log_id: Audit log unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If audit log not found or cannot be deleted
    """
    service = AuditLogService(db)
    try:
        deleted = service.delete_audit_log(log_id, current_user.id)
        if not deleted:
            raise http_not_found(f"Audit log with ID {log_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
