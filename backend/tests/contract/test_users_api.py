"""
Contract tests for user profile API endpoints.

Following TDD methodology - these tests MUST FAIL initially and drive API implementation.
Tests define the API contract that the backend must implement.

Endpoints tested:
- GET /users/me - Get current user profile (duplicate with /auth/me for consistency)
- PUT /users/me - Update current user profile
- GET /users/{user_id} - Get user profile by ID (public info only)
- DELETE /users/me - Delete user account
- GET /users/search - Search users by display name or email
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Test client for user profile API tests."""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Sample user registration data."""
    return {
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "display_name": "Test User"
    }


@pytest.fixture
def authenticated_headers(client, sample_user_data):
    """Get authentication headers for a registered user."""
    # Register user
    client.post("/auth/register", json=sample_user_data)
    
    # Login to get token
    login_data = {
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    }
    login_response = client.post("/auth/token", json=login_data)
    access_token = login_response.json()["access_token"]
    
    return {"Authorization": f"Bearer {access_token}"}


class TestUserProfile:
    """Test cases for getting current user profile endpoint."""
    
    def test_get_my_profile_returns_200(self, client, authenticated_headers, sample_user_data):
        """Test that getting own profile returns 200 OK with user data."""
        response = client.get("/users/me", headers=authenticated_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["display_name"] == sample_user_data["display_name"]
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["is_active"] is True
        assert "password" not in data  # Password should not be returned
        assert "groups_count" in data
        assert "total_bets" in data
        assert "total_points" in data
    
    def test_get_my_profile_invalid_token_returns_401(self, client):
        """Test that getting profile with invalid token returns 401 Unauthorized."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid token" in data["detail"].lower()
    
    def test_get_my_profile_missing_token_returns_401(self, client):
        """Test that getting profile without token returns 401 Unauthorized."""
        response = client.get("/users/me")
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "missing authorization" in data["detail"].lower()


class TestUpdateProfile:
    """Test cases for updating current user profile endpoint."""
    
    def test_update_profile_valid_data_returns_200(self, client, authenticated_headers):
        """Test that updating profile with valid data returns 200 OK."""
        update_data = {
            "display_name": "Updated Test User",
            "bio": "This is my updated bio",
            "favorite_teams": ["Team A", "Team B"]
        }
        
        response = client.put("/users/me", json=update_data, headers=authenticated_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["display_name"] == update_data["display_name"]
        assert data["bio"] == update_data["bio"]
        assert data["favorite_teams"] == update_data["favorite_teams"]
        assert "updated_at" in data
    
    def test_update_profile_partial_data_returns_200(self, client, authenticated_headers):
        """Test that updating profile with partial data returns 200 OK."""
        update_data = {"display_name": "Partially Updated User"}
        
        response = client.put("/users/me", json=update_data, headers=authenticated_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["display_name"] == update_data["display_name"]
    
    def test_update_profile_duplicate_display_name_returns_409(self, client, authenticated_headers):
        """Test that updating to duplicate display name returns 409 Conflict."""
        # Create another user first
        other_user_data = {
            "email": "other@example.com",
            "password": "SecurePassword123!",
            "display_name": "Other User"
        }
        client.post("/auth/register", json=other_user_data)
        
        # Try to update to the other user's display name
        update_data = {"display_name": "Other User"}
        response = client.put("/users/me", json=update_data, headers=authenticated_headers)
        
        assert response.status_code == 409
        data = response.json()
        assert "detail" in data
        assert "display name already exists" in data["detail"].lower()
    
    def test_update_profile_invalid_data_returns_422(self, client, authenticated_headers):
        """Test that updating profile with invalid data returns 422."""
        update_data = {
            "display_name": "",  # Empty display name should be invalid
            "bio": "a" * 1001  # Bio too long
        }
        
        response = client.put("/users/me", json=update_data, headers=authenticated_headers)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_update_profile_invalid_token_returns_401(self, client):
        """Test that updating profile with invalid token returns 401 Unauthorized."""
        update_data = {"display_name": "Updated Name"}
        headers = {"Authorization": "Bearer invalid_token"}
        
        response = client.put("/users/me", json=update_data, headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid token" in data["detail"].lower()


class TestGetUserById:
    """Test cases for getting user profile by ID endpoint."""
    
    def test_get_user_by_id_returns_200(self, client, authenticated_headers, sample_user_data):
        """Test that getting user by ID returns 200 OK with public user data."""
        # Get current user's ID
        profile_response = client.get("/users/me", headers=authenticated_headers)
        user_id = profile_response.json()["user_id"]
        
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id
        assert data["display_name"] == sample_user_data["display_name"]
        assert "created_at" in data
        assert "groups_count" in data
        assert "total_bets" in data
        assert "total_points" in data
        # Private information should not be included
        assert "email" not in data
        assert "password" not in data
        assert "is_active" not in data
    
    def test_get_user_by_id_nonexistent_returns_404(self, client):
        """Test that getting nonexistent user by ID returns 404 Not Found."""
        nonexistent_id = "550e8400-e29b-41d4-a716-446655440000"
        
        response = client.get(f"/users/{nonexistent_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "user not found" in data["detail"].lower()
    
    def test_get_user_by_id_invalid_uuid_returns_422(self, client):
        """Test that getting user with invalid UUID returns 422."""
        invalid_id = "not-a-uuid"
        
        response = client.get(f"/users/{invalid_id}")
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestDeleteAccount:
    """Test cases for deleting user account endpoint."""
    
    def test_delete_account_returns_204(self, client, authenticated_headers):
        """Test that deleting account returns 204 No Content."""
        response = client.delete("/users/me", headers=authenticated_headers)
        
        assert response.status_code == 204
    
    def test_delete_account_confirms_deletion(self, client, authenticated_headers):
        """Test that account is actually deleted after deletion request."""
        # Delete account
        client.delete("/users/me", headers=authenticated_headers)
        
        # Try to access profile - should fail
        response = client.get("/users/me", headers=authenticated_headers)
        assert response.status_code == 401
    
    def test_delete_account_invalid_token_returns_401(self, client):
        """Test that deleting account with invalid token returns 401 Unauthorized."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.delete("/users/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid token" in data["detail"].lower()
    
    def test_delete_account_missing_token_returns_401(self, client):
        """Test that deleting account without token returns 401 Unauthorized."""
        response = client.delete("/users/me")
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "missing authorization" in data["detail"].lower()


class TestSearchUsers:
    """Test cases for searching users endpoint."""
    
    def test_search_users_by_display_name_returns_200(self, client, authenticated_headers):
        """Test that searching users by display name returns 200 OK with results."""
        # Create additional test users
        test_users = [
            {"email": "alice@example.com", "password": "SecurePassword123!", "display_name": "Alice Smith"},
            {"email": "bob@example.com", "password": "SecurePassword123!", "display_name": "Bob Johnson"},
            {"email": "charlie@example.com", "password": "SecurePassword123!", "display_name": "Charlie Brown"}
        ]
        for user in test_users:
            client.post("/auth/register", json=user)
        
        # Search for users with "alice" in name
        response = client.get("/users/search?q=alice", headers=authenticated_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert len(data["users"]) > 0
        
        # Check that search result contains Alice
        user_names = [user["display_name"] for user in data["users"]]
        assert any("Alice" in name for name in user_names)
    
    def test_search_users_with_pagination_returns_200(self, client, authenticated_headers):
        """Test that searching users with pagination parameters returns 200 OK."""
        response = client.get("/users/search?q=test&page=1&per_page=10", headers=authenticated_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total" in data
        assert data["page"] == 1
        assert data["per_page"] == 10
    
    def test_search_users_empty_query_returns_422(self, client, authenticated_headers):
        """Test that searching with empty query returns 422."""
        response = client.get("/users/search?q=", headers=authenticated_headers)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_search_users_no_results_returns_200(self, client, authenticated_headers):
        """Test that searching with no results returns 200 OK with empty list."""
        response = client.get("/users/search?q=nonexistentuser12345", headers=authenticated_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert data["users"] == []
        assert data["total"] == 0
    
    def test_search_users_invalid_token_returns_401(self, client):
        """Test that searching users with invalid token returns 401 Unauthorized."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/search?q=test", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid token" in data["detail"].lower()
    
    def test_search_users_missing_token_returns_401(self, client):
        """Test that searching users without token returns 401 Unauthorized."""
        response = client.get("/users/search?q=test")
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "missing authorization" in data["detail"].lower()