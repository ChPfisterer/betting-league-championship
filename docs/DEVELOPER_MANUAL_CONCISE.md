# Betting League Championship Platform
## Developer Manual v1.0

### 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture) 
3. [API Reference](#api-reference)
4. [Database](#database)
5. [Security](#security)
6. [Development](#development)
7. [Examples](#examples)
8. [Deployment](#deployment)

---

## 🎯 Overview

**Multi-sport betting platform** with social features, real-time updates, and enterprise-grade security.

### Tech Stack
- **Backend**: Python 3.12 + FastAPI 0.115.x
- **Database**: PostgreSQL 17.x  
- **Authentication**: JWT + Keycloak ready
- **Validation**: Pydantic v2
- **Testing**: Comprehensive TDD with pytest

### Key Features
✅ **186 API Endpoints** across 12 core modules  
✅ **Multi-sport Support** (football, basketball, tennis, etc.)  
✅ **Social Betting** with groups and memberships  
✅ **Real-time Updates** for live matches and betting  
✅ **Enterprise Security** with audit logging  
✅ **Risk Management** with fraud detection  
✅ **GDPR Compliant** with data export/deletion  

---

## 🏗️ Architecture

### System Overview
```
Frontend (Angular 20) ←→ Backend API (FastAPI) ←→ Database (PostgreSQL)
                            ↓
                       Auth Server (Keycloak)
```

### Backend Layers

#### 1. **API Layer** (`src/api/`)
- RESTful endpoints with OpenAPI documentation
- Pydantic schemas for request/response validation
- JWT authentication middleware
- Standardized error handling

#### 2. **Service Layer** (`src/services/`)
- Business logic separation
- Data validation and transformation
- Inter-service communication
- Transaction management

#### 3. **Data Layer** (`src/models/`)
- SQLAlchemy ORM models
- Database relationships and constraints
- Performance indexes
- Data validation

#### 4. **Core Layer** (`src/core/`)
- Configuration management
- Security utilities
- Database connection handling
- Shared utilities

---

## 🚀 API Reference

### Base URLs
- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://api.bettingleague.com/api/v1`

### Core APIs (186 Endpoints Total)

#### 🔐 Authentication (5 endpoints)
```http
POST   /auth/register     # User registration
POST   /auth/login        # User login with JWT
POST   /auth/logout       # Secure logout
POST   /auth/refresh      # Token refresh
GET    /auth/me          # Current user profile
```

#### 👤 Users API (18 endpoints)
```http
GET    /users/                    # List users with filtering
POST   /users/                    # Create new user
GET    /users/{id}               # Get user details
PUT    /users/{id}               # Update user profile
DELETE /users/{id}               # Delete user (soft delete)
GET    /users/{id}/profile       # Detailed profile
PUT    /users/{id}/preferences   # Update preferences
POST   /users/search             # Advanced user search
GET    /users/{id}/activity      # User activity history
PUT    /users/{id}/kyc           # KYC verification
```

#### 👥 Groups API (16 endpoints)
```http
GET    /groups/                  # List groups
POST   /groups/                  # Create group
GET    /groups/{id}             # Group details
PUT    /groups/{id}             # Update group
DELETE /groups/{id}             # Delete group
GET    /groups/{id}/members     # Group members
POST   /groups/{id}/invite      # Invite member
GET    /groups/{id}/statistics  # Group analytics
```

#### 🏃‍♂️ Group Memberships API (18 endpoints)
```http
GET    /group-memberships/                    # List memberships
POST   /group-memberships/                    # Create membership
GET    /group-memberships/{id}               # Membership details
PUT    /group-memberships/{id}/role          # Change member role
DELETE /group-memberships/{id}               # Remove membership
POST   /group-memberships/invite             # Send invitation
GET    /group-memberships/user/{user_id}     # User's memberships
```

#### ⚽ Sports API (12 endpoints)
```http
GET    /sports/                 # List all sports
POST   /sports/                 # Add new sport
GET    /sports/{id}            # Sport details
PUT    /sports/{id}            # Update sport
DELETE /sports/{id}            # Remove sport
GET    /sports/{id}/seasons    # Sport seasons
GET    /sports/{id}/statistics # Sport analytics
PUT    /sports/{id}/activate   # Activate/deactivate
```

#### 🏆 Teams API (14 endpoints)
```http
GET    /teams/                  # List teams
POST   /teams/                  # Create team
GET    /teams/{id}             # Team details
PUT    /teams/{id}             # Update team
DELETE /teams/{id}             # Delete team
GET    /teams/{id}/players     # Team roster
POST   /teams/{id}/players     # Add player to team
GET    /teams/{id}/statistics  # Team performance
```

#### 🏅 Competitions API (16 endpoints)
```http
GET    /competitions/                    # List competitions
POST   /competitions/                    # Create competition
GET    /competitions/{id}               # Competition details
PUT    /competitions/{id}               # Update competition
DELETE /competitions/{id}               # Delete competition
GET    /competitions/{id}/matches       # Competition matches
GET    /competitions/{id}/standings     # Current standings
POST   /competitions/{id}/start         # Start competition
```

#### 📅 Seasons API (14 endpoints)
```http
GET    /seasons/                # List seasons
POST   /seasons/                # Create season
GET    /seasons/{id}           # Season details
PUT    /seasons/{id}           # Update season
DELETE /seasons/{id}           # Delete season
GET    /seasons/{id}/matches   # Season fixtures
PUT    /seasons/{id}/start     # Start season
```

#### ⚽ Matches API (16 endpoints)
```http
GET    /matches/                      # List matches
POST   /matches/                      # Schedule match
GET    /matches/{id}                 # Match details
PUT    /matches/{id}                 # Update match
PUT    /matches/{id}/status          # Update status
GET    /matches/{id}/statistics      # Match stats
POST   /matches/search               # Search matches
GET    /matches/upcoming             # Upcoming fixtures
GET    /matches/live                 # Live matches
```

#### 🏃‍♂️ Players API (14 endpoints)
```http
GET    /players/                 # List players
POST   /players/                 # Add player
GET    /players/{id}            # Player profile
PUT    /players/{id}            # Update player
DELETE /players/{id}            # Remove player
GET    /players/{id}/statistics # Player stats
POST   /players/search          # Search players
```

#### 🎰 Bets API (18 endpoints)
```http
GET    /bets/                    # List bets
POST   /bets/                    # Place bet
GET    /bets/{id}               # Bet details
PUT    /bets/{id}               # Update bet
DELETE /bets/{id}               # Cancel bet
POST   /bets/{id}/settle        # Settle bet
GET    /bets/user/{user_id}     # User's bets
GET    /bets/statistics         # Betting analytics
POST   /bets/bulk               # Bulk operations
GET    /bets/{id}/history       # Bet history
```

#### 📊 Results API (14 endpoints)
```http
GET    /results/                     # List results
POST   /results/                     # Record result
GET    /results/{id}                # Result details
PUT    /results/{id}                # Update result
PUT    /results/{id}/verify         # Verify result
GET    /results/match/{match_id}    # Match results
POST   /results/bulk                # Bulk results
```

#### 📋 Audit Logs API (16 endpoints)
```http
GET    /audit-logs/                           # List audit logs
POST   /audit-logs/                           # Create log entry
GET    /audit-logs/{id}                      # Log details
GET    /audit-logs/statistics/overview       # Statistics
GET    /audit-logs/analytics/security        # Security analytics
POST   /audit-logs/search                    # Search logs
POST   /audit-logs/export                    # Export logs
POST   /audit-logs/archive                   # Archive logs
GET    /audit-logs/user/{user_id}/activity   # User activity
```

---

## 🗄️ Database

### Core Tables

#### Users
```sql
users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    role VARCHAR(20) DEFAULT 'user',
    kyc_status VARCHAR(20) DEFAULT 'not_started',
    created_at TIMESTAMP DEFAULT NOW()
)
```

#### Bets
```sql
bets (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    match_id UUID REFERENCES matches(id),
    bet_type VARCHAR(50),
    stake DECIMAL(10,2),
    odds DECIMAL(8,3),
    potential_payout DECIMAL(12,2),
    status VARCHAR(20) DEFAULT 'pending',
    placed_at TIMESTAMP DEFAULT NOW()
)
```

#### Groups
```sql
groups (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    privacy VARCHAR(20) DEFAULT 'public',
    max_members INTEGER DEFAULT 100,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
)
```

### Relationships
- **Users** → **Bets** (1:many)
- **Users** ↔ **Groups** (many:many via GroupMemberships)
- **Matches** → **Bets** (1:many)
- **Teams** ↔ **Players** (many:many)
- **Competitions** → **Seasons** → **Matches** (hierarchical)

### Performance
- **50+ Strategic Indexes** for query optimization
- **Composite Indexes** for common query patterns
- **Foreign Key Indexes** for relationship queries
- **JSON Indexes** for flexible data storage

### Field Architecture (817 Total Fields)

#### Distribution Summary
| Layer | Fields | % | Description |
|-------|--------|---|-------------|
| Database | 295 | 36% | Core persistence fields |
| API Schema | 502 | 61% | Validation + computed fields |
| Seed Data | 20 | 3% | Test data fields |

#### Key Consistency Metrics
- **DB + API Overlap**: 205 fields (25.1%) - Clean separation of concerns
- **API Validation Layer**: 297 API-only fields for business logic
- **Internal DB Fields**: 90 database-only fields for optimization

### Enum System (23 Core Enums)

#### Critical Business Enums
```python
# User Management
UserStatus: pending | active | suspended | banned | deactivated
UserRole: user | moderator | admin | super_admin  
KYCStatus: not_started | in_progress | pending_review | verified | rejected

# Betting Core
BetStatus: pending | matched | settled | cancelled | void | won | lost
BetType: single | multiple | accumulator | system | each_way
MarketType: match_winner | over_under | handicap | both_teams_score

# Competition
MatchStatus: scheduled | live | halftime | finished | postponed | cancelled
CompetitionType: league | cup | tournament | playoff | friendly
```

#### Validation System
✅ **100% Enum Compliance** in seed data  
✅ **Type-safe validation** with detailed error messages  
✅ **Centralized enum definitions** across all layers  

---

## 🔐 Security

### JWT Authentication
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "user",
  "exp": 1672531200,
  "iat": 1672444800
}
```

### Authorization Levels
- **Public**: No auth required
- **User**: Basic user access
- **Moderator**: Elevated privileges  
- **Admin**: Administrative access
- **Super Admin**: Full system access

### Security Features
✅ **Bcrypt Password Hashing** with salt  
✅ **JWT Token Authentication** with refresh  
✅ **Rate Limiting** on all endpoints  
✅ **Comprehensive Audit Logging** (60+ action types)  
✅ **Input Validation** and sanitization  
✅ **CORS Protection** and security headers  
✅ **Role-Based Access Control** (RBAC)  

### Audit Logging
- **60+ Action Types**: User actions, betting, admin operations
- **Security Events**: Login failures, suspicious activity
- **Compliance**: GDPR data requests, audit trails
- **Analytics**: User behavior, system health

---

## 💻 Development

### Quick Start
```bash
# Clone and setup
git clone https://github.com/ChPfisterer/betting-league-championship.git
cd betting-league-championship/backend

# Virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements/dev.txt

# Setup database
createdb betting_championship
alembic upgrade head

# Run development server
uvicorn main:app --reload --port 8000
```

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@localhost/betting_championship
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ENVIRONMENT=development
```

### Docker Development
```bash
# Run with Docker Compose
docker-compose up -d

# Services available:
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Database: localhost:5432
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test types
pytest tests/api/          # Contract tests
pytest tests/integration/  # Integration tests
pytest tests/models/       # Model tests
```

---

## 📝 Examples

### Authentication Flow
```python
import requests

# Login
login_response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "username": "user@example.com",
    "password": "password123"
})

token_data = login_response.json()
headers = {"Authorization": f"Bearer {token_data['access_token']}"}

# Get current user
user_response = requests.get(
    "http://localhost:8000/api/v1/auth/me",
    headers=headers
)
```

### Place a Bet
```python
bet_data = {
    "match_id": "match-uuid-here",
    "bet_type": "match_winner",
    "selection": "home_team",
    "stake": 10.00,
    "odds": 2.50
}

bet_response = requests.post(
    "http://localhost:8000/api/v1/bets/",
    json=bet_data,
    headers=headers
)
```

### Create and Manage Group
```python
# Create group
group_data = {
    "name": "My Betting Group",
    "description": "Friends betting together",
    "privacy": "private",
    "max_members": 20
}

group_response = requests.post(
    "http://localhost:8000/api/v1/groups/",
    json=group_data,
    headers=headers
)

group_id = group_response.json()["id"]

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

### Search and Filter
```python
# Search users
user_search = requests.get(
    "http://localhost:8000/api/v1/users/",
    params={
        "query": "john",
        "status": "active",
        "skip": 0,
        "limit": 10
    },
    headers=headers
)

# Filter bets
bet_filter = requests.get(
    "http://localhost:8000/api/v1/bets/",
    params={
        "status": "won",
        "date_from": "2025-01-01",
        "date_to": "2025-12-31",
        "min_stake": 5.00
    },
    headers=headers
)
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] Database migrations applied  
- [ ] SSL certificates installed
- [ ] Monitoring and logging setup
- [ ] Backup strategy implemented
- [ ] Load balancing configured
- [ ] Rate limiting enabled
- [ ] Security headers configured

### Docker Production
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements/prod.txt .
RUN pip install -r prod.txt
COPY src/ ./src/
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Configuration
```bash
# Production settings
DATABASE_URL=postgresql://user:pass@prod-db/betting_championship
SECRET_KEY=production-secret-key
ENVIRONMENT=production
ALLOWED_HOSTS=["api.bettingleague.com"]
CORS_ORIGINS=["https://bettingleague.com"]
```

---

## 🔧 Troubleshooting

### Common Issues

#### Database Connection
```bash
# Test connection
psql -h localhost -U postgres -d betting_championship

# Check environment
echo $DATABASE_URL

# View logs
docker logs betting_championship_db
```

#### Authentication Problems
```bash
# Verify JWT secret
echo $SECRET_KEY

# Decode token (for debugging)
python -c "import jwt; print(jwt.decode('token', options={'verify_signature': False}))"
```

#### Performance Issues
```bash
# Enable SQL logging (development)
# Monitor slow queries
# Check database indexes
# Verify connection pooling

# Test API performance
curl -w "Time: %{time_total}s\n" http://localhost:8000/api/v1/users/
```

### Error Codes
- **400**: Bad Request - Invalid input
- **401**: Unauthorized - Authentication required
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource doesn't exist
- **422**: Validation Error - Input validation failed
- **500**: Internal Server Error - Server-side error

---

## 📚 Resources

### Documentation
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **GitHub**: https://github.com/ChPfisterer/betting-league-championship

### Support
- **GitHub Issues**: Report bugs and feature requests
- **Tests**: Check `tests/` directory for usage examples
- **Database Schema**: See `alembic/versions/` for migrations

---

## ✅ Summary

The **Betting League Championship Platform** provides:

🎯 **Complete Backend Ecosystem** - 186 endpoints across 12 modules  
🔐 **Enterprise Security** - JWT auth with comprehensive audit logging  
📊 **Advanced Features** - Social betting, risk management, analytics  
🧪 **Comprehensive Testing** - TDD methodology with extensive coverage  
🚀 **Production Ready** - Scalable architecture with performance optimization  

**Version**: 1.0  
**Last Updated**: October 5, 2025  
**API Version**: v1

---

*This manual provides complete guidance for developing with the Betting League Championship platform. For additional support, refer to the GitHub repository or contact the development team.*