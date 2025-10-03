# Quickstart Guide: Multi-Sport Betting Platform

This guide provides step-by-step instructions to set up, deploy, and test the multi-sport betting platform across three environments: development, test, and production.

## Prerequisites

- Docker 27.3.1+ and Docker Compose
- Git
- Node.js 20.18.0+ (for frontend development)
- Python 3.12.7+ (for backend development)  
- PostgreSQL 17.6+ (if running locally without Docker)

## Environment Overview

The platform supports three distinct environments:
- **Development**: Local development with hot reload and debugging
- **Test**: CI/CD and automated testing environment
- **Production**: Optimized production deployment

## Quick Setup (Development Environment)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd betting-league-championship

# Copy environment configuration
cp infrastructure/environments/dev/.env.dev .env
```

### 2. Start Development Environment
```bash
# Start all services (backend, frontend, database, keycloak, observability)
docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d

# Check services are running
docker-compose -f infrastructure/docker/docker-compose.dev.yml ps
```

### 3. Initialize Database and Keycloak
```bash
# Run database migrations
docker-compose -f infrastructure/docker/docker-compose.dev.yml exec backend alembic upgrade head

# Import Keycloak realm configuration
docker-compose -f infrastructure/docker/docker-compose.dev.yml exec keycloak /opt/keycloak/bin/kc.sh import --file /opt/keycloak/data/import/dev/keycloak-realm.json

# Create initial admin user
docker-compose -f infrastructure/docker/docker-compose.dev.yml exec backend python -m src.core.create_admin_user
```

### 4. Verify Development Setup (Including Grafana Stack Learning)
- **Frontend**: http://localhost:4200 (Angular dev server with hot reload)
- **Backend API**: http://localhost:8000/docs (FastAPI Swagger UI)
- **Keycloak Admin**: http://localhost:8080/admin (admin/admin)
- **Grafana Dashboards**: http://localhost:3000 (admin/admin) - Core Learning Component
- **Database**: localhost:5432 (postgres/postgres)

### 5. Grafana Stack Learning Verification
```bash
# Verify all Grafana components are running
docker-compose -f infrastructure/docker/docker-compose.dev.yml ps grafana mimir loki tempo alloy

# Access Grafana and explore components
# Grafana: http://localhost:3000 (dashboards, alerting)
# Mimir: Integrated with Grafana for metrics (PromQL queries)
# Loki: Integrated with Grafana for logs (LogQL queries) 
# Tempo: Integrated with Grafana for traces (trace analysis)
# Alloy: Collecting telemetry data from all services

# Verify OpenTelemetry instrumentation
curl http://localhost:8000/metrics  # Application metrics
curl http://localhost:8000/health   # Health endpoints with traces
```

## Test Environment Setup

### 1. Start Test Environment
```bash
# Start test environment
docker-compose -f infrastructure/docker/docker-compose.test.yml up -d

# Run automated tests
docker-compose -f infrastructure/docker/docker-compose.test.yml exec backend pytest
docker-compose -f infrastructure/docker/docker-compose.test.yml exec frontend npm run test:ci
```

### 2. Test Environment Services
- **Backend API**: http://localhost:8001/docs
- **Frontend**: http://localhost:4201
- **Database**: localhost:5433 (test database)

## Production Environment Setup

### 1. Start Production Environment
```bash
# Copy production environment configuration
cp infrastructure/environments/prod/.env.prod .env

# Start production environment
docker-compose -f infrastructure/docker/docker-compose.prod.yml up -d
```

### 2. Production Environment Services
- **Frontend**: http://localhost (served by Nginx)
- **Backend API**: http://localhost/api (proxied by Nginx)
- **Grafana**: http://localhost:3000 (monitoring dashboards)

### 6. Test-Driven Development Verification
```bash
# Verify TDD setup is working
cd backend
pytest --version
pytest tests/ -v --tb=short  # Should show failing tests initially (Red phase)

cd ../frontend  
npm test -- --watch=false --browsers=ChromeHeadless  # Angular unit tests

# TDD Workflow Example:
# 1. RED: Write failing test
# 2. GREEN: Write minimal code to pass
# 3. REFACTOR: Improve code quality
# 4. Repeat for each feature

# Contract testing verification
cd backend
pytest tests/contract/ -v  # API contract tests
```

### 7. Development TDD Workflow
```bash
# Backend TDD Example
cd backend

# 1. Write failing test first (RED)
# tests/unit/test_betting_service.py
def test_place_bet_should_create_bet_record():
    # Test implementation here
    assert False  # Initially failing

# 2. Run test to see it fail
pytest tests/unit/test_betting_service.py::test_place_bet_should_create_bet_record -v

# 3. Write minimal implementation (GREEN)
# src/services/betting_service.py - implement just enough to pass

# 4. Run test to see it pass
pytest tests/unit/test_betting_service.py::test_place_bet_should_create_bet_record -v

# 5. Refactor code while keeping tests green (REFACTOR)
```

### 8. Frontend TDD Workflow
```bash
# Frontend TDD Example
cd frontend

# 1. Write failing component test first (RED)
# src/app/features/betting/components/bet-form.component.spec.ts

# 2. Run test to see it fail
ng test --watch=false --browsers=ChromeHeadless

# 3. Implement component (GREEN)
# 4. Refactor while keeping tests green (REFACTOR)
```

## CI/CD Pipeline Setup

### 1. GitHub Container Registry Setup
```bash
# Create GitHub Personal Access Token with packages:write scope
# Configure repository secrets in GitHub settings

# Repository Secrets Required:
# - GHCR_TOKEN: GitHub Personal Access Token
# - DOCKER_USERNAME: GitHub username
# - PROD_DEPLOY_KEY: Production deployment key (if using external hosting)
```

### 2. Enable GitHub Actions
```bash
# Navigate to repository Settings > Actions > General
# Enable "Allow all actions and reusable workflows"
# Set workflow permissions to "Read and write permissions"

# Configure branch protection rules for main branch:
# - Require status checks to pass before merging
# - Require branches to be up to date before merging
# - Require review from code owners
```

### 3. Automated Pipeline Triggers

**Development Pipeline** (Feature Branches):
```bash
# Triggered on: Push to feature/* branches
# Actions: Unit tests, integration tests, container builds
# Duration: ~5-10 minutes
```

**Test Pipeline** (Pull Requests):
```bash
# Triggered on: Pull request creation/update
# Actions: Full test suite, security scanning, test deployment
# Duration: ~15-20 minutes
```

**Production Pipeline** (Main Branch):
```bash
# Triggered on: Merge to main branch
# Actions: Production build, security validation, deployment
# Duration: ~20-30 minutes (including manual approval)
```

### 4. Container Image Management
```bash
# View published images
# GitHub Repository > Packages

# Pull specific versions
docker pull ghcr.io/username/betting-platform-backend:latest
docker pull ghcr.io/username/betting-platform-frontend:v1.0.0

# Run with specific versions
docker-compose -f infrastructure/docker/docker-compose.prod.yml up -d
```

### 5. Monitoring CI/CD Pipeline
- **GitHub Actions**: Repository > Actions tab
- **Build Status**: README.md badges for build status
- **Container Registry**: Repository > Packages
- **Security Alerts**: Repository > Security tab
- **Dependency Updates**: Automated Dependabot PRs

### 6. CI/CD Workflow Examples

**Feature Development Workflow**:
```bash
# 1. Create feature branch
git checkout -b feature/123-user-authentication

# 2. Make changes and commit
git add .
git commit -m "feat: implement OAuth 2.0 authentication"
git push origin feature/123-user-authentication

# 3. GitHub Actions automatically:
#    - Runs unit tests
#    - Builds containers
#    - Runs security scans
#    - Reports status on commit
```

**Pull Request Workflow**:
```bash
# 1. Create pull request (triggers test deployment)
# 2. GitHub Actions automatically:
#    - Runs full test suite
#    - Deploys to test environment
#    - Runs integration tests
#    - Posts test results as PR comment

# 3. Review and merge
# 4. Automatic cleanup of test deployment
```

**Production Release Workflow**:
```bash
# 1. Merge to main branch (triggers production pipeline)
# 2. GitHub Actions automatically:
#    - Builds production containers
#    - Runs security validation
#    - Waits for manual approval
#    - Deploys to production
#    - Runs smoke tests
#    - Sends deployment notifications
```

## Development Best Practices

### Local Development Focus
```bash
# Quick start for development
docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d

# Focus on functionality over optimization
# - Hot reload for rapid iteration
# - Simple debugging and logging
# - Essential monitoring only
# - Basic security (OAuth 2.0 with Keycloak)
```

### Future Scaling Considerations
```bash
# Architecture supports future scaling:
# - Stateless backend services (easy to scale horizontally)
# - Redis caching layer (can cluster when needed)
# - Load balancer ready (can add Nginx/HAProxy)
# - Database design supports read replicas
# - Monitoring stack can be enhanced

# Current focus: Build it right, scale it later
```

### Essential Monitoring (Grafana Stack Learning Focus)
```bash
# Complete Grafana observability stack for learning
# Grafana: http://localhost:3000 (dashboard creation, alerting setup)
# All components integrated for comprehensive observability learning:

# 1. Metrics (Mimir + PromQL)
# - Application performance metrics
# - Business metrics (betting activity)
# - Infrastructure metrics (containers, database)

# 2. Logs (Loki + LogQL) 
# - Centralized application logs
# - Structured logging with correlation IDs
# - Log aggregation and search

# 3. Traces (Tempo + OpenTelemetry)
# - Distributed tracing across services
# - Performance bottleneck identification
# - Request flow visualization

# 4. Data Collection (Alloy)
# - Telemetry data collection and routing
# - Multiple data source integration
# - Configuration and pipeline management

# Learning objectives: Hands-on experience with all Grafana stack components
```

### Simple Backup Strategy
```bash
# Basic PostgreSQL backup
docker-compose exec postgres pg_dump -U betting_user betting_platform_dev > backup.sql

# Simple restore
docker-compose exec -T postgres psql -U betting_user betting_platform_dev < backup.sql

# Automated daily backups (simple cron job)
# No complex disaster recovery until scale demands it
```

## Environment Management

### Switch Between Environments
```bash
# Development
export COMPOSE_FILE=infrastructure/docker/docker-compose.dev.yml
docker-compose up -d

# Test
export COMPOSE_FILE=infrastructure/docker/docker-compose.test.yml
docker-compose up -d

# Production
export COMPOSE_FILE=infrastructure/docker/docker-compose.prod.yml
docker-compose up -d
```

### Environment-Specific Commands
```bash
# Development with hot reload
docker-compose -f infrastructure/docker/docker-compose.dev.yml up

# Test with automated testing
docker-compose -f infrastructure/docker/docker-compose.test.yml run --rm backend pytest
docker-compose -f infrastructure/docker/docker-compose.test.yml run --rm frontend npm test

# Production with optimized builds
docker-compose -f infrastructure/docker/docker-compose.prod.yml up -d --build
```

## Development Setup (Local Services)
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Define FastAPI Application Dependencies in requirements.txt
fastapi[standard]>=0.115.13,<0.116.0
pydantic>=2.7.0,<3.0.0
sqlalchemy>=2.0.23,<3.0.0
alembic>=1.13.0,<2.0.0
psycopg2-binary>=2.9.9,<3.0.0
python-keycloak>=4.6.0,<5.0.0
uvicorn[standard]>=0.24.0,<1.0.0
pytest>=7.4.3,<8.0.0
httpx>=0.25.2,<1.0.0

# Setup environment variables
cp .env.example .env
# Edit .env with your local settings

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies (package.json should include):
# "@angular/core": "^20.1.4"
# "@angular/common": "^20.1.4"  
# "@angular/platform-browser": "^20.1.4"
# "@angular/material": "^20.1.2"
# "typescript": "~5.5.0"
# "keycloak-angular": "^15.2.1"
npm install

# Start development server
ng serve --host 0.0.0.0 --port 4200
```

### Database Setup (Local PostgreSQL)
```bash
# Create database
createdb betting_platform_dev

# Create user
psql -c "CREATE USER betting_user WITH PASSWORD 'your_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE betting_platform_dev TO betting_user;"
```

## Environment Configurations

### Development (dev)
```bash
# Start dev environment
docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d

# Environment characteristics:
# - Hot reload enabled
# - Debug logging
# - Local file storage
# - Sample data loaded
# - CORS enabled for localhost
```

### Test (test)
```bash
# Start test environment
docker-compose -f infrastructure/docker/docker-compose.test.yml up -d

# Environment characteristics:
# - Production-like setup
# - Test data fixtures
# - Performance monitoring
# - Automated test suite execution
```

### Production (prod)
```bash
# Start production environment (minimal example)
docker-compose -f infrastructure/docker/docker-compose.prod.yml up -d

# Environment characteristics:
# - Optimized builds
# - Security hardening
# - SSL/TLS enabled
# - Monitoring and logging
# - Backup automation
```

## Initial Data and Testing

### Load Sample Data
```bash
# Load sports and competitions
docker-compose exec backend python -m src.scripts.load_sample_data

# Create test users and groups
docker-compose exec backend python -m src.scripts.create_test_users

# Load upcoming matches
docker-compose exec backend python -m src.scripts.load_test_matches
```

### Run Test Suite
```bash
# Backend tests
cd backend
pytest tests/ -v --cov=src

# Frontend tests
cd frontend
npm test
npm run e2e

# Integration tests
cd backend
pytest tests/integration/ -v

# Contract tests
cd backend
pytest tests/contract/ -v
```

## User Journey Testing

### 1. User Registration and Authentication
```bash
# Test user registration
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!",
    "display_name": "Test User"
  }'

# Test authentication
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com", 
    "password": "SecurePassword123!"
  }'
```

### 2. Group Management
```bash
# Create private group
curl -X POST http://localhost:8000/groups \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Group",
    "type": "private",
    "description": "Test betting group"
  }'

# Join group with invitation code
curl -X POST http://localhost:8000/groups/<group_id>/join \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "invitation_code": "<invitation_code>"
  }'
```

### 3. Betting Workflow
```bash
# Get upcoming matches
curl -X GET "http://localhost:8000/matches?group_id=<group_id>" \
  -H "Authorization: Bearer <token>"

# Place bet
curl -X POST http://localhost:8000/matches/<match_id>/bet \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "group_id": "<group_id>",
    "predicted_winner": "home",
    "predicted_home_score": 2,
    "predicted_away_score": 1
  }'

# Check leaderboard
curl -X GET "http://localhost:8000/groups/<group_id>/leaderboard" \
  -H "Authorization: Bearer <token>"
```

### 4. Real-time Features
```bash
# Test WebSocket connection
wscat -c "ws://localhost:8000/ws/updates?token=<bearer_token>"

# Subscribe to group updates
{"type": "subscribe", "event": "group_updates", "data": {"group_id": "<group_id>"}}

# Subscribe to match updates  
{"type": "subscribe", "event": "match_updates", "data": {"match_id": "<match_id>"}}
```

## Admin Operations

### Match Management
```bash
# Create new match
curl -X POST http://localhost:8000/admin/matches \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "season_id": "<season_id>",
    "home_team_id": "<team_id>",
    "away_team_id": "<team_id>",
    "scheduled_at": "2025-10-05T15:00:00Z",
    "matchday": 1
  }'

# Enter provisional result
curl -X POST http://localhost:8000/admin/matches/<match_id>/result \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "home_score": 2,
    "away_score": 1,
    "is_provisional": true
  }'

# Finalize result
curl -X PUT http://localhost:8000/admin/matches/<match_id>/result/finalize \
  -H "Authorization: Bearer <admin_token>"
```

### Group Administration
```bash
# Get group audit trail
curl -X GET "http://localhost:8000/admin/groups/<group_id>/audit" \
  -H "Authorization: Bearer <admin_token>"

# Update group settings
curl -X PUT http://localhost:8000/admin/groups/<group_id>/settings \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "custom_deadline_offset": "PT2H",
    "member_limit": 100
  }'
```

## Monitoring and Debugging

### Health Checks
```bash
# Check service health
curl http://localhost:8000/health
curl http://localhost:4200/health
curl http://localhost:8080/health/ready

# Check database connectivity
docker-compose exec backend python -c "from src.database.connection import get_db; next(get_db())"
```

### Logs and Monitoring
```bash
# View service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
docker-compose logs -f keycloak

# Monitor database performance
docker-compose exec postgres psql -U betting_user -d betting_platform_dev -c "
  SELECT query, calls, total_time, mean_time 
  FROM pg_stat_statements 
  ORDER BY total_time DESC 
  LIMIT 10;"
```

### Debug Real-time Features
```bash
# Test WebSocket broadcast
docker-compose exec backend python -m src.scripts.test_websocket_broadcast

# Check Redis connection (if using Redis for WebSocket scaling)
docker-compose exec redis redis-cli ping
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using the ports
   lsof -i :4200  # Frontend
   lsof -i :8000  # Backend
   lsof -i :5432  # PostgreSQL
   lsof -i :8080  # Keycloak
   ```

2. **Database Connection Issues**
   ```bash
   # Reset database
   docker-compose down -v
   docker-compose up -d postgres
   docker-compose exec backend alembic upgrade head
   ```

3. **Keycloak Authentication Issues**
   ```bash
   # Restart Keycloak and reimport realm
   docker-compose restart keycloak
   # Wait for startup, then reimport realm configuration
   ```

4. **Frontend Build Issues**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ng build
   ```

### Performance Testing
```bash
# Load test the API
cd backend
locust -f tests/performance/locustfile.py --host=http://localhost:8000

# Test concurrent betting
python tests/performance/concurrent_betting_test.py

# WebSocket stress test
python tests/performance/websocket_stress_test.py
```

## Next Steps

After completing the quickstart:

1. **Explore the API**: Visit http://localhost:8000/docs for interactive API documentation
2. **Frontend Development**: Navigate to http://localhost:4200 and explore the Angular application
3. **Admin Interface**: Access Keycloak admin at http://localhost:8080/admin to manage users and groups
4. **Database Management**: Use your preferred PostgreSQL client to connect to localhost:5432
5. **Customize Configuration**: Modify environment files in `infrastructure/` for your specific needs

## Support

- **API Documentation**: http://localhost:8000/docs
- **WebSocket Events**: See `contracts/websocket.md`
- **Database Schema**: See `data-model.md`
- **Architecture**: See `plan.md`