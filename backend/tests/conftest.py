"""
Pytest configuration and shared fixtures for contract tests.

This file provides common test fixtures and configuration for all contract tests.
Following TDD methodology - these fixtures support API contract testing.
"""
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture(scope="session")
def test_app():
    """FastAPI test application instance."""
    return app


@pytest.fixture
def client(test_app):
    """Sync test client for API contract tests."""
    return TestClient(test_app)


@pytest_asyncio.fixture
async def async_client(test_app):
    """Async test client for API contract tests."""
    from httpx import ASGITransport
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://testserver") as client:
        yield client


@pytest.fixture
def sample_user_registration():
    """Sample user registration data for tests."""
    return {
        "email": "testuser@example.com",
        "password": "SecurePassword123!",
        "display_name": "Test User"
    }


@pytest.fixture
def sample_admin_registration():
    """Sample admin user registration data for tests."""
    return {
        "email": "admin@example.com",
        "password": "AdminPassword123!",
        "display_name": "Admin User"
    }


@pytest.fixture
def sample_login_credentials():
    """Sample login credentials for tests."""
    return {
        "email": "testuser@example.com",
        "password": "SecurePassword123!"
    }


@pytest.fixture
def authenticated_user(client, sample_user_registration, sample_login_credentials):
    """Create and authenticate a test user, return user data and headers."""
    # Register user
    register_response = client.post("/auth/register", json=sample_user_registration)
    assert register_response.status_code == 201
    user_data = register_response.json()
    
    # Login to get token
    login_response = client.post("/auth/token", json=sample_login_credentials)
    assert login_response.status_code == 200
    token_data = login_response.json()
    
    # Return user data and authentication headers
    return {
        "user": user_data,
        "token": token_data,
        "headers": {"Authorization": f"Bearer {token_data['access_token']}"}
    }


@pytest.fixture
def auth_headers():
    """Mock authentication headers for contract tests (TDD phase)."""
    # During TDD contract phase, we use mock headers since auth endpoints don't exist yet
    return {"Authorization": "Bearer mock_jwt_token_for_contract_tests"}


@pytest.fixture
def sample_group_data():
    """Sample group creation data for tests."""
    return {
        "name": "Test Betting Group",
        "description": "A test group for contract testing",
        "settings": {
            "is_private": False,
            "max_members": 50,
            "allow_member_invites": True,
            "point_system": "standard"
        }
    }


@pytest.fixture
def sample_sport_data():
    """Sample sport data for tests."""
    return {
        "name": "Football",
        "display_name": "Football",
        "description": "Association Football (Soccer)",
        "is_active": True
    }


@pytest.fixture
def sample_competition_data():
    """Sample competition data for tests."""
    return {
        "name": "Premier League",
        "display_name": "English Premier League",
        "description": "Top tier of English football",
        "sport_id": None,  # Will be set in tests
        "country": "England",
        "competition_type": "league",
        "is_active": True
    }


@pytest.fixture
def sample_team_data():
    """Sample team data for tests."""
    return {
        "name": "Manchester United",
        "display_name": "Manchester United FC",
        "short_name": "MUN",
        "logo_url": "https://example.com/logos/mun.png",
        "country": "England",
        "is_active": True
    }


@pytest.fixture
def sample_match_data():
    """Sample match data for tests."""
    return {
        "home_team_id": None,  # Will be set in tests
        "away_team_id": None,  # Will be set in tests
        "competition_id": None,  # Will be set in tests
        "season_id": None,  # Will be set in tests
        "scheduled_time": "2024-12-15T15:00:00Z",
        "venue": "Old Trafford",
        "round_info": "Matchday 15"
    }


@pytest.fixture
def sample_bet_data():
    """Sample bet data for tests."""
    return {
        "match_id": None,  # Will be set in tests
        "bet_type": "match_result",
        "prediction": {
            "home_score": 2,
            "away_score": 1
        },
        "confidence": 8
    }


# Test database configuration
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Setup test database before running tests."""
    # This will be implemented when we have database setup
    # For now, this is a placeholder for TDD
    yield
    # Cleanup will go here


# Error response helpers
@pytest.fixture
def assert_error_response():
    """Helper function to assert error response structure."""
    def _assert_error_response(response, expected_status, expected_detail_contains=None):
        assert response.status_code == expected_status
        data = response.json()
        assert "detail" in data
        if expected_detail_contains:
            assert expected_detail_contains.lower() in data["detail"].lower()
        return data
    return _assert_error_response


# Pagination helpers
@pytest.fixture
def assert_paginated_response():
    """Helper function to assert paginated response structure."""
    def _assert_paginated_response(response, expected_status=200):
        assert response.status_code == expected_status
        data = response.json()
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert "pages" in data
        assert isinstance(data.get("total"), int)
        assert isinstance(data.get("page"), int)
        assert isinstance(data.get("per_page"), int)
        assert isinstance(data.get("pages"), int)
        return data
    return _assert_paginated_response