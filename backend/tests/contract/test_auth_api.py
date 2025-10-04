"""
Contract tests for authentication API endpoints.

Following TDD methodology - these tests MUST FAIL initially and drive API implementation.
Tests define the API contract that the backend must implement.

Endpoints tested:
- POST /auth/register - User registration
- POST /auth/token - User authentication (login) 
- POST /auth/refresh - Token refresh
- POST /auth/logout - User logout
- GET /auth/me - Get current user profile
- PUT /auth/password - Change password
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Test client for authentication API tests."""
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
def sample_login_data():
    """Sample user login data."""
    return {
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }


class TestAuthRegistration:
    """Test cases for user registration endpoint."""
    
    def test_register_new_user_returns_201(self, client, sample_user_data):
        """Test that registering a new user returns 201 Created."""
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "user_id" in data
        assert data["email"] == sample_user_data["email"]
        assert data["display_name"] == sample_user_data["display_name"]
        assert "password" not in data  # Password should not be returned
        assert "created_at" in data
        assert data["is_active"] is True
    
    def test_register_duplicate_email_returns_409(self, client, sample_user_data):
        """Test that registering with duplicate email returns 409 Conflict."""
        # First registration should succeed
        client.post("/auth/register", json=sample_user_data)
        
        # Second registration with same email should fail
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 409
        data = response.json()
        assert "detail" in data
        assert "email already exists" in data["detail"].lower()
    
    def test_register_invalid_email_returns_422(self, client, sample_user_data):
        """Test that registering with invalid email returns 422 Unprocessable Entity."""
        sample_user_data["email"] = "invalid-email"
        
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_register_weak_password_returns_422(self, client, sample_user_data):
        """Test that registering with weak password returns 422 Unprocessable Entity."""
        sample_user_data["password"] = "weak"
        
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_register_missing_fields_returns_422(self, client):
        """Test that registering with missing required fields returns 422."""
        incomplete_data = {"email": "test@example.com"}
        
        response = client.post("/auth/register", json=incomplete_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestAuthLogin:
    """Test cases for user login/token endpoint."""
    
    def test_login_valid_credentials_returns_200(self, client, sample_user_data, sample_login_data):
        """Test that login with valid credentials returns 200 OK with tokens."""
        # Register user first
        client.post("/auth/register", json=sample_user_data)
        
        response = client.post("/auth/token", json=sample_login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    def test_login_invalid_email_returns_401(self, client):
        """Test that login with invalid email returns 401 Unauthorized."""
        invalid_login = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        
        response = client.post("/auth/token", json=invalid_login)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid credentials" in data["detail"].lower()
    
    def test_login_invalid_password_returns_401(self, client, sample_user_data):
        """Test that login with invalid password returns 401 Unauthorized."""
        # Register user first
        client.post("/auth/register", json=sample_user_data)
        
        invalid_login = {
            "email": sample_user_data["email"],
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/token", json=invalid_login)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid credentials" in data["detail"].lower()
    
    def test_login_missing_fields_returns_422(self, client):
        """Test that login with missing fields returns 422."""
        incomplete_login = {"email": "test@example.com"}
        
        response = client.post("/auth/token", json=incomplete_login)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestAuthRefresh:
    """Test cases for token refresh endpoint."""
    
    def test_refresh_valid_token_returns_200(self, client, sample_user_data, sample_login_data):
        """Test that refresh with valid refresh token returns 200 OK with new tokens."""
        # Register and login user first
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/token", json=sample_login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    def test_refresh_invalid_token_returns_401(self, client):
        """Test that refresh with invalid token returns 401 Unauthorized."""
        invalid_refresh = {"refresh_token": "invalid_token"}
        
        response = client.post("/auth/refresh", json=invalid_refresh)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid token" in data["detail"].lower()
    
    def test_refresh_missing_token_returns_422(self, client):
        """Test that refresh with missing token returns 422."""
        response = client.post("/auth/refresh", json={})
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestAuthLogout:
    """Test cases for user logout endpoint."""
    
    def test_logout_valid_token_returns_204(self, client, sample_user_data, sample_login_data):
        """Test that logout with valid token returns 204 No Content."""
        # Register and login user first
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/token", json=sample_login_data)
        access_token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/auth/logout", headers=headers)
        
        assert response.status_code == 204
    
    def test_logout_invalid_token_returns_401(self, client):
        """Test that logout with invalid token returns 401 Unauthorized."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/auth/logout", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid token" in data["detail"].lower()
    
    def test_logout_missing_token_returns_401(self, client):
        """Test that logout without token returns 401 Unauthorized."""
        response = client.post("/auth/logout")
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "missing authorization" in data["detail"].lower()


class TestAuthProfile:
    """Test cases for get current user profile endpoint."""
    
    def test_get_profile_valid_token_returns_200(self, client, sample_user_data, sample_login_data):
        """Test that getting profile with valid token returns 200 OK with user data."""
        # Register and login user first
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/token", json=sample_login_data)
        access_token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["display_name"] == sample_user_data["display_name"]
        assert "user_id" in data
        assert "created_at" in data
        assert data["is_active"] is True
        assert "password" not in data  # Password should not be returned
    
    def test_get_profile_invalid_token_returns_401(self, client):
        """Test that getting profile with invalid token returns 401 Unauthorized."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid token" in data["detail"].lower()
    
    def test_get_profile_missing_token_returns_401(self, client):
        """Test that getting profile without token returns 401 Unauthorized."""
        response = client.get("/auth/me")
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "missing authorization" in data["detail"].lower()


class TestPasswordChange:
    """Test cases for password change endpoint."""
    
    def test_change_password_valid_data_returns_200(self, client, sample_user_data, sample_login_data):
        """Test that changing password with valid data returns 200 OK."""
        # Register and login user first
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/token", json=sample_login_data)
        access_token = login_response.json()["access_token"]
        
        password_data = {
            "current_password": sample_user_data["password"],
            "new_password": "NewSecurePassword456!"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put("/auth/password", json=password_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "password updated" in data["message"].lower()
    
    def test_change_password_wrong_current_returns_400(self, client, sample_user_data, sample_login_data):
        """Test that changing password with wrong current password returns 400 Bad Request."""
        # Register and login user first
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/token", json=sample_login_data)
        access_token = login_response.json()["access_token"]
        
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "NewSecurePassword456!"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put("/auth/password", json=password_data, headers=headers)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "current password is incorrect" in data["detail"].lower()
    
    def test_change_password_weak_new_returns_422(self, client, sample_user_data, sample_login_data):
        """Test that changing to weak password returns 422 Unprocessable Entity."""
        # Register and login user first
        client.post("/auth/register", json=sample_user_data)
        login_response = client.post("/auth/token", json=sample_login_data)
        access_token = login_response.json()["access_token"]
        
        password_data = {
            "current_password": sample_user_data["password"],
            "new_password": "weak"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put("/auth/password", json=password_data, headers=headers)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_change_password_invalid_token_returns_401(self, client):
        """Test that changing password with invalid token returns 401 Unauthorized."""
        password_data = {
            "current_password": "oldpassword",
            "new_password": "NewSecurePassword456!"
        }
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.put("/auth/password", json=password_data, headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid token" in data["detail"].lower()