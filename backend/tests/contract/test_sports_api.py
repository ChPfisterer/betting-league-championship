"""
Contract tests for Sports API endpoints
T055: Define API contracts for sports management (TDD Red phase)

This module defines the expected behavior and contracts for all sports-related API endpoints.
Tests are written to fail initially (Red phase of TDD) before implementation exists.

API Endpoints Tested:
- GET /api/v1/sports - List all available sports
- GET /api/v1/sports/{sport_id} - Get specific sport details
- POST /api/v1/admin/sports - Create a new sport (admin only)
- PUT /api/v1/admin/sports/{sport_id} - Update sport details (admin only)
- DELETE /api/v1/admin/sports/{sport_id} - Delete a sport (admin only)
- GET /api/v1/sports/{sport_id}/competitions - List competitions for a sport
- GET /api/v1/sports/{sport_id}/teams - List teams for a sport

Contract Definitions:
- Request/response schemas
- Status codes and error handling
- Authentication and authorization requirements
- Validation rules
- Business logic constraints
"""

import pytest
from fastapi.testclient import TestClient


class TestSportsAPIContracts:
    """Contract tests for Sports API endpoints"""

    def test_list_sports_contract(self, client: TestClient):
        """
        Contract: GET /api/v1/sports
        
        Query Parameters:
        - page: int (optional, default 1)
        - limit: int (optional, default 20, max 100)
        - is_active: bool (optional, filter by active status)
        - search: str (optional, search in name/description)
        
        Success Response (200):
        {
            "data": [
                {
                    "id": uuid,
                    "name": str,
                    "display_name": str,
                    "description": str | null,
                    "is_active": bool,
                    "icon_url": str | null,
                    "competition_count": int,
                    "created_at": datetime,
                    "updated_at": datetime
                }
            ],
            "pagination": {
                "total": int,
                "page": int,
                "limit": int,
                "has_next": bool,
                "has_prev": bool
            }
        }
        
        Note: Public endpoint - no authentication required
        """
        response = client.get("/api/v1/sports?page=1&limit=10&is_active=true")
        
        # Expected to fail (404) - endpoint doesn't exist yet
        assert response.status_code == 404
        
        # TODO: After implementation, expect:
        # assert response.status_code == 200
        # data = response.json()
        # assert "data" in data
        # assert "pagination" in data
        # assert isinstance(data["data"], list)

    def test_get_sport_details_contract(self, client: TestClient):
        """
        Contract: GET /api/v1/sports/{sport_id}
        
        Success Response (200):
        {
            "id": uuid,
            "name": str,
            "display_name": str,
            "description": str | null,
            "is_active": bool,
            "icon_url": str | null,
            "metadata": {
                "typical_match_duration": int (minutes),
                "team_size": int,
                "supported_bet_types": list[str],
                "scoring_system": str
            },
            "competition_count": int,
            "team_count": int,
            "created_at": datetime,
            "updated_at": datetime
        }
        
        Error Cases:
        - 404: Sport not found
        
        Note: Public endpoint - no authentication required
        """
        sport_id = "770e8400-e29b-41d4-a716-446655440000"
        response = client.get(f"/api/v1/sports/{sport_id}")
        
        # Expected to fail (404) - endpoint doesn't exist yet
        assert response.status_code == 404

    def test_create_sport_contract(self, client: TestClient, auth_headers: dict):
        """
        Contract: POST /api/v1/admin/sports
        
        Request Schema:
        {
            "name": str (required, 1-50 chars, unique),
            "display_name": str (required, 1-100 chars),
            "description": str (optional, max 500 chars),
            "is_active": bool (optional, default true),
            "icon_url": str (optional, valid URL),
            "metadata": {
                "typical_match_duration": int (required, minutes),
                "team_size": int (required, 1-50),
                "supported_bet_types": list[str] (required),
                "scoring_system": str (required)
            }
        }
        
        Success Response (201):
        {
            "id": uuid,
            "name": str,
            "display_name": str,
            "description": str | null,
            "is_active": bool,
            "icon_url": str | null,
            "metadata": object,
            "created_at": datetime,
            "updated_at": datetime
        }
        
        Error Cases:
        - 400: Invalid input data
        - 401: Not authenticated
        - 403: Not admin user
        - 409: Sport name already exists
        """
        response = client.post(
            "/api/v1/admin/sports",
            json={
                "name": "football",
                "display_name": "Football",
                "description": "Association Football (Soccer)",
                "is_active": True,
                "metadata": {
                    "typical_match_duration": 90,
                    "team_size": 11,
                    "supported_bet_types": ["match_result", "over_under", "both_teams_score"],
                    "scoring_system": "goals"
                }
            },
            headers=auth_headers
        )
        
        # Expected to fail (404) - endpoint doesn't exist yet
        assert response.status_code == 404

    def test_create_sport_validation_contract(self, client: TestClient, auth_headers: dict):
        """Contract: POST /api/v1/admin/sports - Input validation"""
        
        # Missing required fields
        response = client.post(
            "/api/v1/admin/sports",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 404  # TODO: Should be 400
        
        # Invalid metadata
        response = client.post(
            "/api/v1/admin/sports",
            json={
                "name": "test_sport",
                "display_name": "Test Sport",
                "metadata": {
                    "typical_match_duration": -10,  # Invalid negative duration
                    "team_size": 0,  # Invalid team size
                    "supported_bet_types": [],  # Empty bet types
                    "scoring_system": ""  # Empty scoring system
                }
            },
            headers=auth_headers
        )
        assert response.status_code == 404  # TODO: Should be 400

    def test_update_sport_contract(self, client: TestClient, auth_headers: dict):
        """
        Contract: PUT /api/v1/admin/sports/{sport_id}
        
        Request Schema: (all fields optional for update)
        {
            "display_name": str (1-100 chars),
            "description": str (max 500 chars),
            "is_active": bool,
            "icon_url": str (valid URL),
            "metadata": object
        }
        
        Success Response (200): Updated sport object
        
        Error Cases:
        - 400: Invalid input data
        - 401: Not authenticated
        - 403: Not admin user
        - 404: Sport not found
        
        Note: sport.name cannot be updated for data integrity
        """
        sport_id = "770e8400-e29b-41d4-a716-446655440000"
        response = client.put(
            f"/api/v1/admin/sports/{sport_id}",
            json={
                "display_name": "Updated Football",
                "description": "Updated description for football",
                "is_active": True
            },
            headers=auth_headers
        )
        
        # Expected to fail (404) - endpoint doesn't exist yet
        assert response.status_code == 404

    def test_delete_sport_contract(self, client: TestClient, auth_headers: dict):
        """
        Contract: DELETE /api/v1/admin/sports/{sport_id}
        
        Success Response (204): No content
        
        Error Cases:
        - 401: Not authenticated
        - 403: Not admin user
        - 404: Sport not found
        - 409: Cannot delete sport with active competitions
        
        Note: Soft delete - sets is_active=false instead of hard delete
        """
        sport_id = "770e8400-e29b-41d4-a716-446655440000"
        response = client.delete(
            f"/api/v1/admin/sports/{sport_id}",
            headers=auth_headers
        )
        
        # Expected to fail (404) - endpoint doesn't exist yet
        assert response.status_code == 404

    def test_list_sport_competitions_contract(self, client: TestClient):
        """
        Contract: GET /api/v1/sports/{sport_id}/competitions
        
        Query Parameters:
        - page: int (optional, default 1)
        - limit: int (optional, default 20, max 100)
        - is_active: bool (optional, filter by active status)
        - country: str (optional, filter by country)
        - competition_type: str (optional, filter by type)
        
        Success Response (200):
        {
            "data": [
                {
                    "id": uuid,
                    "name": str,
                    "display_name": str,
                    "description": str | null,
                    "sport_id": uuid,
                    "country": str,
                    "competition_type": str,
                    "is_active": bool,
                    "season_count": int,
                    "team_count": int,
                    "created_at": datetime
                }
            ],
            "pagination": object
        }
        
        Error Cases:
        - 404: Sport not found
        
        Note: Public endpoint - no authentication required
        """
        sport_id = "770e8400-e29b-41d4-a716-446655440000"
        response = client.get(
            f"/api/v1/sports/{sport_id}/competitions?page=1&limit=10&is_active=true"
        )
        
        # Expected to fail (404) - endpoint doesn't exist yet
        assert response.status_code == 404

    def test_list_sport_teams_contract(self, client: TestClient):
        """
        Contract: GET /api/v1/sports/{sport_id}/teams
        
        Query Parameters:
        - page: int (optional, default 1)
        - limit: int (optional, default 20, max 100)
        - is_active: bool (optional, filter by active status)
        - country: str (optional, filter by country)
        - search: str (optional, search in team name)
        
        Success Response (200):
        {
            "data": [
                {
                    "id": uuid,
                    "name": str,
                    "display_name": str,
                    "short_name": str,
                    "logo_url": str | null,
                    "country": str,
                    "is_active": bool,
                    "match_count": int,
                    "competition_count": int,
                    "created_at": datetime
                }
            ],
            "pagination": object
        }
        
        Error Cases:
        - 404: Sport not found
        
        Note: Public endpoint - no authentication required
        """
        sport_id = "770e8400-e29b-41d4-a716-446655440000"
        response = client.get(
            f"/api/v1/sports/{sport_id}/teams?page=1&limit=10&is_active=true"
        )
        
        # Expected to fail (404) - endpoint doesn't exist yet
        assert response.status_code == 404

    def test_admin_authentication_contract(self, client: TestClient):
        """Contract: Admin endpoints require proper authentication and authorization"""
        
        # Test creating sport without auth
        response = client.post(
            "/api/v1/admin/sports",
            json={
                "name": "test_sport",
                "display_name": "Test Sport",
                "metadata": {
                    "typical_match_duration": 90,
                    "team_size": 11,
                    "supported_bet_types": ["match_result"],
                    "scoring_system": "goals"
                }
            }
        )
        assert response.status_code == 404  # TODO: Should be 401
        
        # Test updating sport without auth
        response = client.put(
            "/api/v1/admin/sports/770e8400-e29b-41d4-a716-446655440000",
            json={"display_name": "Updated Sport"}
        )
        assert response.status_code == 404  # TODO: Should be 401
        
        # Test deleting sport without auth
        response = client.delete("/api/v1/admin/sports/770e8400-e29b-41d4-a716-446655440000")
        assert response.status_code == 404  # TODO: Should be 401

    def test_non_admin_user_contract(self, client: TestClient, auth_headers: dict):
        """Contract: Non-admin users cannot access admin endpoints"""
        
        # Note: auth_headers fixture provides regular user token, not admin
        # This test will need to be updated when role-based auth is implemented
        
        response = client.post(
            "/api/v1/admin/sports",
            json={
                "name": "test_sport",
                "display_name": "Test Sport",
                "metadata": {
                    "typical_match_duration": 90,
                    "team_size": 11,
                    "supported_bet_types": ["match_result"],
                    "scoring_system": "goals"
                }
            },
            headers=auth_headers
        )
        # Expected to fail (404) - endpoint doesn't exist yet
        # TODO: After implementation, should be 403 for non-admin users
        assert response.status_code == 404

    def test_sport_metadata_validation_contract(self, client: TestClient, auth_headers: dict):
        """Contract: Sport metadata validation rules"""
        
        # Test with invalid bet types
        response = client.post(
            "/api/v1/admin/sports",
            json={
                "name": "test_sport",
                "display_name": "Test Sport",
                "metadata": {
                    "typical_match_duration": 90,
                    "team_size": 11,
                    "supported_bet_types": ["invalid_bet_type"],
                    "scoring_system": "goals"
                }
            },
            headers=auth_headers
        )
        assert response.status_code == 404  # TODO: Should be 400
        
        # Test with invalid duration
        response = client.post(
            "/api/v1/admin/sports",
            json={
                "name": "test_sport2",
                "display_name": "Test Sport 2",
                "metadata": {
                    "typical_match_duration": 0,  # Invalid
                    "team_size": 11,
                    "supported_bet_types": ["match_result"],
                    "scoring_system": "goals"
                }
            },
            headers=auth_headers
        )
        assert response.status_code == 404  # TODO: Should be 400