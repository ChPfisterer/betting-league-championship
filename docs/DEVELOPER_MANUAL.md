# Betting League Championship - Developer Manual

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [API Reference](#api-reference)
4. [Database Schema](#database-schema)
5. [Authentication & Security](#authentication--security)
6. [Development Setup](#development-setup)
7. [API Usage Examples](#api-usage-examples)
8. [Testing Guide](#testing-guide)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Betting League Championship platform is a comprehensive multi-sport betting application built with modern technologies and enterprise-grade architecture.

### Key Features
- **Multi-sport Support**: Football, basketball, tennis, and more
- **Social Betting**: Group-based betting with friends and communities
- **Real-time Updates**: Live match tracking and betting
- **Enterprise Security**: JWT authentication with comprehensive audit logging
- **Risk Management**: Advanced betting controls and fraud detection
- **Compliance Ready**: GDPR compliant with full audit trails

### Technology Stack
- **Backend**: Python 3.12 + FastAPI 0.115.x
- **Database**: PostgreSQL 17.x with advanced indexing
- **Authentication**: JWT with Keycloak integration ready
- **Validation**: Pydantic v2 with comprehensive schemas
- **Testing**: Comprehensive TDD with pytest
- **Documentation**: Auto-generated OpenAPI 3.0

---

## Architecture

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (Angular 20)  │────│   (FastAPI)     │────│   (PostgreSQL)  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   Keycloak      │
                       │   (Auth Server) │
                       │                 │
                       └─────────────────┘
```

### Backend Architecture Layers

#### 1. API Layer (`src/api/`)
- **FastAPI Routes**: RESTful endpoints with automatic OpenAPI documentation
- **Request/Response Schemas**: Pydantic models for validation
- **Error Handling**: Standardized error responses
- **Authentication**: JWT middleware integration

#### 2. Service Layer (`src/services/`)
- **Business Logic**: Core application logic separated from API concerns
- **Data Validation**: Business rule enforcement
- **Inter-service Communication**: Clean service dependencies
- **Transaction Management**: Database transaction handling

#### 3. Data Layer (`src/models/`)
- **SQLAlchemy Models**: Database entity definitions
- **Relationships**: Foreign key relationships and constraints
- **Validation**: Database-level data integrity
- **Indexing**: Performance optimization

#### 4. Core Layer (`src/core/`)
- **Configuration**: Environment and application settings
- **Security**: Authentication and authorization utilities
- **Database**: Connection management and session handling
- **Utilities**: Shared utility functions

### Design Patterns
- **Repository Pattern**: Data access abstraction
- **Service Layer Pattern**: Business logic encapsulation
- **Dependency Injection**: Loose coupling between components
- **Factory Pattern**: Object creation and configuration

---

## API Reference

### Base URL
```
Production: https://api.bettingleague.com/api/v1
Development: http://localhost:8000/api/v1
```

### API Overview (186 Endpoints)

#### 🔐 Authentication API
```
POST   /auth/register     # User registration
POST   /auth/login        # User login
POST   /auth/logout       # User logout  
POST   /auth/refresh      # Token refresh
GET    /auth/me          # Current user profile
```

#### 👤 Users API (18 endpoints)
```
GET    /users/                    # List users
POST   /users/                    # Create user
GET    /users/{id}               # Get user
PUT    /users/{id}               # Update user
DELETE /users/{id}               # Delete user
GET    /users/{id}/profile       # User profile
PUT    /users/{id}/preferences   # Update preferences
POST   /users/search             # Search users
GET    /users/{id}/activity      # User activity
PUT    /users/{id}/kyc           # KYC verification
# ... 8 more endpoints
```

#### 👥 Groups API (16 endpoints)
```
GET    /groups/                  # List groups
POST   /groups/                  # Create group
GET    /groups/{id}             # Get group
PUT    /groups/{id}             # Update group
DELETE /groups/{id}             # Delete group
GET    /groups/{id}/members     # Group members
POST   /groups/{id}/invite      # Invite member
GET    /groups/{id}/statistics  # Group stats
# ... 8 more endpoints
```

#### 🏃‍♂️ Group Memberships API (18 endpoints)
```
GET    /group-memberships/                    # List memberships
POST   /group-memberships/                    # Create membership
GET    /group-memberships/{id}               # Get membership
PUT    /group-memberships/{id}               # Update membership
DELETE /group-memberships/{id}               # Remove membership
POST   /group-memberships/invite             # Send invitation
PUT    /group-memberships/{id}/role          # Change role
GET    /group-memberships/user/{user_id}     # User memberships
# ... 10 more endpoints
```

#### ⚽ Sports API (12 endpoints)
```
GET    /sports/                 # List sports
POST   /sports/                 # Create sport
GET    /sports/{id}            # Get sport
PUT    /sports/{id}            # Update sport
DELETE /sports/{id}            # Delete sport
GET    /sports/{id}/seasons    # Sport seasons
GET    /sports/{id}/statistics # Sport statistics
PUT    /sports/{id}/activate   # Activate sport
# ... 4 more endpoints
```

#### 🏆 Teams API (14 endpoints)
```
GET    /teams/                  # List teams
POST   /teams/                  # Create team
GET    /teams/{id}             # Get team
PUT    /teams/{id}             # Update team
DELETE /teams/{id}             # Delete team
GET    /teams/{id}/players     # Team players
POST   /teams/{id}/players     # Add player
GET    /teams/{id}/statistics  # Team statistics
# ... 6 more endpoints
```

#### 🏅 Competitions API (16 endpoints)
```
GET    /competitions/                    # List competitions
POST   /competitions/                    # Create competition
GET    /competitions/{id}               # Get competition
PUT    /competitions/{id}               # Update competition
DELETE /competitions/{id}               # Delete competition
GET    /competitions/{id}/matches       # Competition matches
GET    /competitions/{id}/standings     # Competition standings
POST   /competitions/{id}/start         # Start competition
# ... 8 more endpoints
```

#### 📅 Seasons API (14 endpoints)
```
GET    /seasons/                # List seasons
POST   /seasons/                # Create season
GET    /seasons/{id}           # Get season
PUT    /seasons/{id}           # Update season
DELETE /seasons/{id}           # Delete season
GET    /seasons/{id}/matches   # Season matches
GET    /seasons/{id}/teams     # Season teams
PUT    /seasons/{id}/start     # Start season
# ... 6 more endpoints
```

#### ⚽ Matches API (16 endpoints)
```
GET    /matches/                      # List matches
POST   /matches/                      # Create match
GET    /matches/{id}                 # Get match
PUT    /matches/{id}                 # Update match
DELETE /matches/{id}                 # Delete match
PUT    /matches/{id}/status          # Update status
GET    /matches/{id}/statistics      # Match statistics
POST   /matches/search               # Search matches
GET    /matches/upcoming             # Upcoming matches
GET    /matches/live                 # Live matches
# ... 6 more endpoints
```

#### 🏃‍♂️ Players API (14 endpoints)
```
GET    /players/                 # List players
POST   /players/                 # Create player
GET    /players/{id}            # Get player
PUT    /players/{id}            # Update player
DELETE /players/{id}            # Delete player
GET    /players/{id}/statistics # Player statistics
POST   /players/search          # Search players
GET    /players/{id}/matches    # Player matches
# ... 6 more endpoints
```

#### 🎰 Bets API (18 endpoints)
```
GET    /bets/                    # List bets
POST   /bets/                    # Place bet
GET    /bets/{id}               # Get bet
PUT    /bets/{id}               # Update bet
DELETE /bets/{id}               # Cancel bet
POST   /bets/{id}/settle        # Settle bet
GET    /bets/user/{user_id}     # User bets
GET    /bets/statistics         # Betting statistics
POST   /bets/bulk               # Bulk operations
GET    /bets/{id}/history       # Bet history
# ... 8 more endpoints
```

#### 📊 Results API (14 endpoints)
```
GET    /results/                     # List results
POST   /results/                     # Create result
GET    /results/{id}                # Get result
PUT    /results/{id}                # Update result
DELETE /results/{id}                # Delete result
PUT    /results/{id}/verify         # Verify result
GET    /results/match/{match_id}    # Match results
POST   /results/bulk                # Bulk results
# ... 6 more endpoints
```

#### 📋 Audit Logs API (16 endpoints)
```
GET    /audit-logs/                           # List audit logs
POST   /audit-logs/                           # Create audit log
GET    /audit-logs/{id}                      # Get audit log
PUT    /audit-logs/{id}                      # Update audit log
DELETE /audit-logs/{id}                      # Delete audit log
GET    /audit-logs/statistics/overview       # Statistics
GET    /audit-logs/analytics/security        # Security analytics
POST   /audit-logs/search                    # Search logs
POST   /audit-logs/bulk                      # Bulk operations
POST   /audit-logs/export                    # Export logs
POST   /audit-logs/archive                   # Archive logs
GET    /audit-logs/user/{user_id}/activity   # User activity
# ... 4 more endpoints
```

---

## Database Schema

### Core Entities

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth TIMESTAMP WITH TIME ZONE NOT NULL,
    phone_number VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    role VARCHAR(20) DEFAULT 'user',
    kyc_status VARCHAR(20) DEFAULT 'not_started',
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Groups Table
```sql
CREATE TABLE groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    privacy VARCHAR(20) DEFAULT 'public',
    max_members INTEGER DEFAULT 100,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Bets Table
```sql
CREATE TABLE bets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) NOT NULL,
    match_id UUID REFERENCES matches(id) NOT NULL,
    bet_type VARCHAR(50) NOT NULL,
    stake DECIMAL(10,2) NOT NULL,
    odds DECIMAL(8,3) NOT NULL,
    potential_payout DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    placed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    settled_at TIMESTAMP WITH TIME ZONE
);
```

### Relationships
- **One-to-Many**: User → Bets, Group → Memberships, Match → Bets
- **Many-to-Many**: Users ↔ Groups (via GroupMemberships), Teams ↔ Players
- **Hierarchical**: Competitions → Seasons → Matches

### Indexes
- **Performance Indexes**: 50+ strategic indexes for query optimization
- **Unique Constraints**: Username, email uniqueness
- **Foreign Key Indexes**: All relationship indexes
- **Composite Indexes**: Multi-column indexes for common queries

---

## Authentication & Security

### JWT Authentication

#### Token Structure
```json
{
  "sub": "user_id",
  "email": "user@example.com", 
  "role": "user",
  "exp": 1672531200,
  "iat": 1672444800
}
```

#### Authentication Flow
1. **Login**: `POST /auth/login` with credentials
2. **Token Response**: Access token + refresh token
3. **Protected Requests**: Include `Authorization: Bearer <token>`
4. **Token Refresh**: `POST /auth/refresh` when token expires

### Authorization Levels
- **Public**: No authentication required
- **User**: Basic user authentication required
- **Moderator**: Moderator role or higher
- **Admin**: Admin role required
- **Super Admin**: Highest privilege level

### Security Features
- **Password Hashing**: Bcrypt with salt
- **Rate Limiting**: API endpoint protection
- **Audit Logging**: All actions tracked
- **Data Validation**: Input sanitization
- **CORS Protection**: Cross-origin request security

---

## Development Setup

### Prerequisites
```bash
# Required software
Python 3.12+
PostgreSQL 17.x
Node.js 18+ (for frontend)
Docker & Docker Compose
```

### Backend Setup
```bash
# Clone repository
git clone https://github.com/ChPfisterer/betting-league-championship.git
cd betting-league-championship

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
cd backend
pip install -r requirements/dev.txt

# Setup database
createdb betting_championship
alembic upgrade head

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables
```bash
# .env file
DATABASE_URL=postgresql://user:pass@localhost/betting_championship
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ENVIRONMENT=development
```

### Docker Setup
```bash
# Run with Docker Compose
docker-compose up -d

# Access services
# API: http://localhost:8000
# Database: localhost:5432
# Documentation: http://localhost:8000/docs
```

---

## API Usage Examples

### Authentication Example
```python
import requests

# Login
response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "username": "user@example.com",
    "password": "password123"
})
token_data = response.json()
access_token = token_data["access_token"]

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {access_token}"}
user_response = requests.get(
    "http://localhost:8000/api/v1/auth/me", 
    headers=headers
)
```

### Create and Place Bet
```python
# Create a bet
bet_data = {
    "match_id": "match-uuid-here",
    "bet_type": "match_winner",
    "selection": "home_team",
    "stake": 10.00,
    "odds": 2.50
}

response = requests.post(
    "http://localhost:8000/api/v1/bets/",
    json=bet_data,
    headers=headers
)
bet = response.json()
```

### Group Management
```python
# Create a group
group_data = {
    "name": "My Betting Group",
    "description": "Friends betting group",
    "privacy": "private",
    "max_members": 20
}

response = requests.post(
    "http://localhost:8000/api/v1/groups/",
    json=group_data,
    headers=headers
)

# Invite member
invite_data = {
    "email": "friend@example.com",
    "role": "member",
    "message": "Join our betting group!"
}

requests.post(
    f"http://localhost:8000/api/v1/groups/{group_id}/invite",
    json=invite_data,
    headers=headers
)
```

### Search and Filtering
```python
# Search users
search_params = {
    "query": "john",
    "status": "active",
    "skip": 0,
    "limit": 10
}

response = requests.get(
    "http://localhost:8000/api/v1/users/",
    params=search_params,
    headers=headers
)

# Advanced bet filtering
bet_filters = {
    "user_id": "user-uuid",
    "status": "won",
    "date_from": "2025-01-01",
    "date_to": "2025-12-31",
    "min_stake": 5.00
}

response = requests.get(
    "http://localhost:8000/api/v1/bets/",
    params=bet_filters,
    headers=headers
)
```

---

## Testing Guide

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/api/test_users.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run contract tests only
pytest tests/api/

# Run integration tests
pytest tests/integration/
```

### Test Structure
```
tests/
├── api/                    # Contract tests
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_bets.py
│   └── ...
├── integration/            # Integration tests
│   ├── test_betting_flow.py
│   ├── test_user_journey.py
│   └── ...
├── models/                 # Model tests
│   ├── test_user_model.py
│   ├── test_bet_model.py
│   └── ...
└── conftest.py            # Test configuration
```

### Test Examples
```python
# Contract test example
def test_create_user_success(client, admin_headers):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "date_of_birth": "1990-01-01"
    }
    
    response = client.post(
        "/api/v1/users/",
        json=user_data,
        headers=admin_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
```

---

## Deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL certificates installed
- [ ] Monitoring setup (logs, metrics)
- [ ] Backup strategy implemented
- [ ] Load balancer configured
- [ ] Rate limiting enabled

### Docker Production
```dockerfile
# Production Dockerfile example
FROM python:3.12-slim

WORKDIR /app
COPY requirements/prod.txt .
RUN pip install -r prod.txt

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY main.py .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Configuration
```bash
# Production environment variables
DATABASE_URL=postgresql://user:pass@db-server/betting_championship
SECRET_KEY=production-secret-key
ENVIRONMENT=production
ALLOWED_HOSTS=["api.bettingleague.com"]
CORS_ORIGINS=["https://bettingleague.com"]
```

---

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database connection
psql -h localhost -U postgres -d betting_championship

# Verify environment variables
echo $DATABASE_URL

# Check database logs
docker logs betting_championship_db
```

#### Authentication Problems
```bash
# Verify JWT secret key
echo $SECRET_KEY

# Check token expiration
python -c "import jwt; print(jwt.decode('your-token', options={'verify_signature': False}))"

# Clear expired sessions
# Restart application server
```

#### Performance Issues
```bash
# Check database queries
# Enable SQL logging in development
# Monitor slow query log
# Verify database indexes

# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/api/v1/users/"
```

### Error Codes
- **400**: Bad Request - Invalid input data
- **401**: Unauthorized - Authentication required
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource doesn't exist
- **422**: Validation Error - Input validation failed
- **500**: Internal Server Error - Server-side error

### Support Resources
- **API Documentation**: http://localhost:8000/docs
- **GitHub Issues**: https://github.com/ChPfisterer/betting-league-championship/issues
- **Database Schema**: See migrations in `alembic/versions/`
- **Test Examples**: Check `tests/` directory for usage examples

---

## Conclusion

This developer manual provides comprehensive guidance for working with the Betting League Championship platform. The architecture is designed for scalability, maintainability, and enterprise-grade security.

For additional support or questions, please refer to the GitHub repository or contact the development team.

**Version**: 1.0  
**Last Updated**: October 5, 2025  
**API Version**: v1