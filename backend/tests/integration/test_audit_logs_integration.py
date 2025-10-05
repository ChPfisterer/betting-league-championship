"""
Comprehensive integration tests for Audit Log API functionality.

These tests verify the complete audit log system including:
- Basic CRUD operations
- Security monitoring features
- Analytics and reporting
- Bulk operations and export
- Archive functionality
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi.testclient import TestClient


class TestAuditLogCRUD:
    """Test basic CRUD operations for audit logs."""
    
    async def test_create_audit_log_success(self, client: TestClient, admin_headers):
        """Test successful audit log creation."""
        log_data = {
            "action_type": "user_created",
            "entity_type": "user",
            "entity_id": str(uuid4()),
            "user_id": str(uuid4()),
            "level": "info",
            "message": "New user account created successfully",
            "details": {
                "username": "testuser",
                "email": "test@example.com",
                "ip_address": "192.168.1.1"
            },
            "source": "web_api",
            "tags": ["user_management", "registration"]
        }
        
        response = client.post(
            "/api/v1/audit-logs/",
            json=log_data,
            headers=admin_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify response structure
        assert "id" in data
        assert data["action_type"] == "user_created"
        assert data["entity_type"] == "user"
        assert data["level"] == "info"
        assert data["message"] == "New user account created successfully"
        assert data["source"] == "web_api"
        assert "created_at" in data
        
        return data["id"]
    
    async def test_get_audit_log_success(self, client: TestClient, admin_headers):
        """Test successful audit log retrieval."""
        # First create an audit log
        log_id = await self.test_create_audit_log_success(client, admin_headers)
        
        # Then retrieve it
        response = client.get(
            f"/api/v1/audit-logs/{log_id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == log_id
        assert data["action_type"] == "user_created"
        assert data["level"] == "info"
    
    async def test_get_audit_log_with_user(self, client: TestClient, admin_headers):
        """Test audit log retrieval with user information."""
        log_id = await self.test_create_audit_log_success(client, admin_headers)
        
        response = client.get(
            f"/api/v1/audit-logs/{log_id}/with-user",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "audit_log" in data
        assert data["audit_log"]["id"] == log_id
        # User information should be included if available
        assert "user" in data
    
    async def test_get_audit_log_with_details(self, client: TestClient, admin_headers):
        """Test audit log retrieval with full details."""
        log_id = await self.test_create_audit_log_success(client, admin_headers)
        
        response = client.get(
            f"/api/v1/audit-logs/{log_id}/with-details",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "audit_log" in data
        assert "details" in data["audit_log"]
        assert "tags" in data["audit_log"]
    
    async def test_update_audit_log_success(self, client: TestClient, admin_headers):
        """Test successful audit log update."""
        log_id = await self.test_create_audit_log_success(client, admin_headers)
        
        update_data = {
            "tags": ["reviewed", "processed", "user_management"],
            "metadata": {
                "reviewer": "admin_user",
                "review_date": "2025-10-03T10:00:00Z",
                "status": "reviewed"
            }
        }
        
        response = client.put(
            f"/api/v1/audit-logs/{log_id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "reviewed" in data["tags"]
        assert "processed" in data["tags"]
        assert data["metadata"]["reviewer"] == "admin_user"
    
    async def test_list_audit_logs_success(self, client: TestClient, admin_headers):
        """Test successful audit log listing."""
        # Create multiple audit logs
        await self.test_create_audit_log_success(client, admin_headers)
        await self.test_create_audit_log_success(client, admin_headers)
        
        response = client.get(
            "/api/v1/audit-logs/",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 2
        
        # Verify structure of returned logs
        log = data[0]
        assert "id" in log
        assert "action_type" in log
        assert "created_at" in log
    
    async def test_delete_audit_log_success(self, client: TestClient, admin_headers):
        """Test successful audit log deletion."""
        log_id = await self.test_create_audit_log_success(client, admin_headers)
        
        response = client.delete(
            f"/api/v1/audit-logs/{log_id}",
            headers=admin_headers
        )
        
        assert response.status_code == 204
        
        # Verify log is deleted
        response = client.get(
            f"/api/v1/audit-logs/{log_id}",
            headers=admin_headers
        )
        assert response.status_code == 404


class TestAuditLogFiltering:
    """Test audit log filtering and search functionality."""
    
    async def test_filter_by_action_type(self, client: TestClient, admin_headers):
        """Test filtering audit logs by action type."""
        response = client.get(
            "/api/v1/audit-logs/?action_type=user_created",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        if data:  # If there are results
            for log in data:
                assert log["action_type"] == "user_created"
    
    async def test_filter_by_level(self, client: TestClient, admin_headers):
        """Test filtering audit logs by level."""
        response = client.get(
            "/api/v1/audit-logs/?level=warning",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        if data:  # If there are results
            for log in data:
                assert log["level"] == "warning"
    
    async def test_filter_by_date_range(self, client: TestClient, admin_headers):
        """Test filtering audit logs by date range."""
        date_from = (datetime.utcnow() - timedelta(days=1)).isoformat()
        date_to = datetime.utcnow().isoformat()
        
        response = client.get(
            f"/api/v1/audit-logs/?date_from={date_from}&date_to={date_to}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return logs within date range
        assert isinstance(data, list)
    
    async def test_search_audit_logs(self, client: TestClient, admin_headers):
        """Test searching audit logs with filters."""
        search_data = {
            "action_types": ["user_created", "user_updated"],
            "entity_types": ["user"],
            "levels": ["info", "warning"],
            "search_query": "user",
            "date_from": (datetime.utcnow() - timedelta(days=7)).isoformat(),
            "date_to": datetime.utcnow().isoformat()
        }
        
        response = client.post(
            "/api/v1/audit-logs/search",
            json=search_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        # If results exist, verify they match filters
        if data:
            for log in data:
                assert log["action_type"] in ["user_created", "user_updated"]
                assert log["entity_type"] == "user"
                assert log["level"] in ["info", "warning"]


class TestAuditLogStatistics:
    """Test audit log statistics and analytics."""
    
    async def test_get_audit_statistics(self, client: TestClient, admin_headers):
        """Test getting audit log statistics."""
        response = client.get(
            "/api/v1/audit-logs/statistics/overview",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify statistics structure
        expected_fields = [
            "total_logs", "logs_by_level", "logs_by_action_type",
            "logs_by_entity_type", "error_rate", "activity_timeline"
        ]
        
        for field in expected_fields:
            assert field in data
        
        # Verify data types
        assert isinstance(data["total_logs"], int)
        assert isinstance(data["logs_by_level"], dict)
        assert isinstance(data["logs_by_action_type"], dict)
        assert isinstance(data["error_rate"], (int, float))
    
    async def test_get_security_analytics(self, client: TestClient, admin_headers):
        """Test getting security analytics."""
        response = client.get(
            "/api/v1/audit-logs/analytics/security",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify analytics structure
        expected_fields = [
            "security_events", "failed_login_attempts", "suspicious_ips",
            "user_activity_patterns", "system_health_indicators"
        ]
        
        for field in expected_fields:
            assert field in data
        
        # Verify data types
        assert isinstance(data["security_events"], int)
        assert isinstance(data["failed_login_attempts"], int)
        assert isinstance(data["suspicious_ips"], list)
    
    async def test_get_statistics_with_filters(self, client: TestClient, admin_headers):
        """Test getting statistics with date filters."""
        date_from = (datetime.utcnow() - timedelta(days=7)).isoformat()
        
        response = client.get(
            f"/api/v1/audit-logs/statistics/overview?date_from={date_from}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total_logs" in data
        assert isinstance(data["total_logs"], int)


class TestAuditLogBulkOperations:
    """Test bulk operations for audit logs."""
    
    async def test_bulk_create_audit_logs(self, client: TestClient, admin_headers):
        """Test bulk creation of audit logs."""
        bulk_data = {
            "logs": [
                {
                    "action_type": "user_created",
                    "message": "User 1 created via bulk import",
                    "level": "info",
                    "details": {"batch_number": 1}
                },
                {
                    "action_type": "user_updated",
                    "message": "User 2 updated via bulk import",
                    "level": "info",
                    "details": {"batch_number": 1}
                },
                {
                    "action_type": "user_deleted",
                    "message": "User 3 deleted via bulk import",
                    "level": "warning",
                    "details": {"batch_number": 1}
                }
            ],
            "source": "bulk_import_api",
            "batch_id": "batch_001"
        }
        
        response = client.post(
            "/api/v1/audit-logs/bulk",
            json=bulk_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify bulk response structure
        assert "created_count" in data
        assert "failed_count" in data
        assert "processing_time" in data
        
        assert data["created_count"] == 3
        assert data["failed_count"] == 0
    
    async def test_bulk_create_with_validation_errors(self, client: TestClient, admin_headers):
        """Test bulk creation with some invalid logs."""
        bulk_data = {
            "logs": [
                {
                    "action_type": "user_created",
                    "message": "Valid log",
                    "level": "info"
                },
                {
                    "action_type": "invalid_action",  # Invalid action type
                    "message": "Invalid log",
                    "level": "info"
                },
                {
                    "action_type": "user_updated",
                    "message": "Another valid log",
                    "level": "warning"
                }
            ],
            "source": "bulk_test",
            "ignore_errors": True
        }
        
        response = client.post(
            "/api/v1/audit-logs/bulk",
            json=bulk_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have created valid logs and skipped invalid ones
        assert data["created_count"] == 2
        assert data["failed_count"] == 1


class TestAuditLogExport:
    """Test audit log export functionality."""
    
    async def test_export_audit_logs_json(self, client: TestClient, admin_headers):
        """Test exporting audit logs in JSON format."""
        export_data = {
            "format": "json",
            "include_details": True,
            "compress": False,
            "filters": {
                "action_types": ["user_created", "user_updated"],
                "date_from": (datetime.utcnow() - timedelta(days=30)).isoformat()
            }
        }
        
        response = client.post(
            "/api/v1/audit-logs/export",
            json=export_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify export response structure
        assert "export_id" in data
        assert "status" in data
        assert "created_at" in data
        assert data["status"] in ["pending", "processing", "completed"]
    
    async def test_export_audit_logs_csv(self, client: TestClient, admin_headers):
        """Test exporting audit logs in CSV format."""
        export_data = {
            "format": "csv",
            "include_details": False,
            "compress": True
        }
        
        response = client.post(
            "/api/v1/audit-logs/export",
            json=export_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "export_id" in data
        assert "status" in data


class TestAuditLogArchive:
    """Test audit log archive functionality."""
    
    async def test_archive_old_logs(self, client: TestClient, admin_headers):
        """Test archiving old audit logs."""
        archive_data = {
            "archive_before": (datetime.utcnow() - timedelta(days=365)).isoformat(),
            "archive_levels": ["debug", "info"],
            "compress": True,
            "retention_days": 2555
        }
        
        response = client.post(
            "/api/v1/audit-logs/archive",
            json=archive_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify archive response structure
        assert "archive_id" in data
        assert "status" in data
        assert "estimated_logs" in data
        assert data["status"] in ["pending", "processing", "completed"]
    
    async def test_archive_with_selective_levels(self, client: TestClient, admin_headers):
        """Test archiving with selective log levels."""
        archive_data = {
            "archive_before": (datetime.utcnow() - timedelta(days=90)).isoformat(),
            "archive_levels": ["debug"],  # Only archive debug logs
            "compress": True
        }
        
        response = client.post(
            "/api/v1/audit-logs/archive",
            json=archive_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "archive_id" in data


class TestAuditLogUserActivity:
    """Test user activity tracking through audit logs."""
    
    async def test_get_user_activity(self, client: TestClient, admin_headers):
        """Test getting user activity from audit logs."""
        user_id = uuid4()
        
        response = client.get(
            f"/api/v1/audit-logs/user/{user_id}/activity",
            headers=admin_headers
        )
        
        assert response.status_code in [200, 404]  # 404 if user has no activity
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            
            # If there are activities, verify structure
            if data:
                activity = data[0]
                assert "action_type" in activity
                assert "created_at" in activity
                assert activity["user_id"] == str(user_id)
    
    async def test_get_user_activity_with_filters(self, client: TestClient, admin_headers):
        """Test getting user activity with action type filters."""
        user_id = uuid4()
        
        response = client.get(
            f"/api/v1/audit-logs/user/{user_id}/activity?action_types=user_login&action_types=user_logout",
            headers=admin_headers
        )
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify filtered results
            if data:
                for activity in data:
                    assert activity["action_type"] in ["user_login", "user_logout"]


class TestAuditLogEntityHistory:
    """Test entity history tracking through audit logs."""
    
    async def test_get_entity_history(self, client: TestClient, admin_headers):
        """Test getting entity history from audit logs."""
        entity_id = uuid4()
        
        response = client.get(
            f"/api/v1/audit-logs/entity/user/{entity_id}/history",
            headers=admin_headers
        )
        
        assert response.status_code in [200, 404]  # 404 if entity has no history
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            
            # If there's history, verify structure
            if data:
                entry = data[0]
                assert "action_type" in entry
                assert "created_at" in entry
                assert entry["entity_id"] == str(entity_id)
                assert entry["entity_type"] == "user"
    
    async def test_get_entity_history_with_pagination(self, client: TestClient, admin_headers):
        """Test getting entity history with pagination."""
        entity_id = uuid4()
        
        response = client.get(
            f"/api/v1/audit-logs/entity/user/{entity_id}/history?skip=0&limit=5",
            headers=admin_headers
        )
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            assert len(data) <= 5  # Should respect limit


class TestAuditLogValidation:
    """Test audit log validation and error handling."""
    
    async def test_create_audit_log_missing_required_fields(self, client: TestClient, admin_headers):
        """Test audit log creation with missing required fields."""
        incomplete_data = {
            "message": "Test message"
            # Missing action_type and level
        }
        
        response = client.post(
            "/api/v1/audit-logs/",
            json=incomplete_data,
            headers=admin_headers
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data
    
    async def test_create_audit_log_invalid_action_type(self, client: TestClient, admin_headers):
        """Test audit log creation with invalid action type."""
        invalid_data = {
            "action_type": "invalid_action_type",
            "message": "Test message",
            "level": "info"
        }
        
        response = client.post(
            "/api/v1/audit-logs/",
            json=invalid_data,
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    async def test_create_audit_log_invalid_level(self, client: TestClient, admin_headers):
        """Test audit log creation with invalid level."""
        invalid_data = {
            "action_type": "user_created",
            "message": "Test message",
            "level": "invalid_level"
        }
        
        response = client.post(
            "/api/v1/audit-logs/",
            json=invalid_data,
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    async def test_get_nonexistent_audit_log(self, client: TestClient, admin_headers):
        """Test getting a non-existent audit log."""
        fake_id = uuid4()
        
        response = client.get(
            f"/api/v1/audit-logs/{fake_id}",
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    async def test_update_nonexistent_audit_log(self, client: TestClient, admin_headers):
        """Test updating a non-existent audit log."""
        fake_id = uuid4()
        update_data = {"tags": ["test"]}
        
        response = client.put(
            f"/api/v1/audit-logs/{fake_id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 404


class TestAuditLogPermissions:
    """Test audit log access permissions."""
    
    async def test_unauthorized_access(self, client: TestClient):
        """Test accessing audit logs without authentication."""
        response = client.get("/api/v1/audit-logs/")
        
        assert response.status_code == 401
    
    async def test_user_cannot_access_audit_logs(self, client: TestClient, user_headers):
        """Test that regular users cannot access audit logs."""
        response = client.get(
            "/api/v1/audit-logs/",
            headers=user_headers
        )
        
        # Should be forbidden for regular users
        assert response.status_code == 403
    
    async def test_user_cannot_create_audit_logs(self, client: TestClient, user_headers):
        """Test that regular users cannot create audit logs."""
        log_data = {
            "action_type": "user_created",
            "message": "Test log",
            "level": "info"
        }
        
        response = client.post(
            "/api/v1/audit-logs/",
            json=log_data,
            headers=user_headers
        )
        
        assert response.status_code == 403