# Betting League Championship - AI Development Guide

A multi-sport betting platform with FastAPI backend, Angular frontend, PostgreSQL database, and Keycloak OAuth 2.0 authentication.

## Architecture Overview

**Backend**: FastAPI app at `backend/src/` with layered architecture:
- `models/` - SQLAlchemy models with strict enum validation (BetType, BetStatus, MarketType)
- `api/v1/endpoints/` - Versioned REST endpoints with dependency injection
- `services/` - Business logic layer (KeycloakService for OAuth integration)
- `core/` - Shared utilities (database, config, security with Pydantic settings)

**Frontend**: Angular 20 standalone components at `frontend/betting-league-app/src/app/`:
- `core/` - Services, guards, interceptors (auth.interceptor.ts for token management)
- `features/` - Feature modules (betting, groups, competitions)
- `shared/` - Reusable components and utilities

**Database**: PostgreSQL 17.6 with complex relational schema for sports betting data, managed via SQLAlchemy with Alembic migrations.

## Development Workflow

```bash
# Full development environment (includes DB, Keycloak, backend, frontend)
./start-dev-full.sh

# Individual services
./start-backend.sh     # FastAPI server on :8000
./start-frontend.sh    # Angular dev server on :4200
docker-compose -f docker-compose.dev.yml up  # DB + Keycloak only
```

**Backend Setup**:
- Python 3.12 with virtual environment in `.venv/`
- Dependencies managed via `pyproject.toml` (base, dev, test, prod requirements)
- Run from `backend/` directory: `cd src && python -m main` or `uvicorn main:app --reload`

**Testing**: 
- Backend: `cd backend && pytest` (contract tests in `tests/conftest.py`)
- **Follow TDD methodology** - Write tests first, then implement features
- Code quality: `ruff check .` and `ruff format .` (configured in `pyproject.toml`)

**Database Migrations**:
- **No Alembic** - Manual schema management due to complex indices and foreign key constraints
- Use direct SQL or SQLAlchemy schema creation for database changes
- Consider migration tooling improvements if you can handle the complex relational structure

## Critical Patterns

**Database Dependencies**: FastAPI uses dependency injection pattern:
```python
from core.database import get_db
def endpoint(db: Session = Depends(get_db)):
```

**Authentication Flow**: 
- Keycloak OAuth 2.0 via `keycloak_auth.py` endpoints
- JWT validation in `services/keycloak_service.py`
- Angular auth interceptor automatically adds tokens

**Model Validation**: 
- Strict enum validation in models (e.g., `BetStatus.PENDING`)
- Custom validators using `@validates` decorator
- Decimal precision for monetary values

**API Versioning**: All endpoints under `/api/v1/` prefix with separate routers per domain (auth, bets, competitions, etc.)

**Configuration**: Pydantic settings in `core/config.py` with environment variable support for database URLs, CORS origins, and security keys.

**Data Seeding**: Use `./seed-data.sh` or `complete_data_seeder.py` for test data (Bundesliga teams/matches included).

## Betting Domain Rules

**Scoring System**: 
- Users predict both winner and exact final score
- 1 point for correct winner prediction
- 3 points total (1 + 2 bonus) for exact score match
- NO default bets - users must actively place bets to participate

**Betting Deadlines**:
- Default: 1 hour before match start (admin configurable)
- Deadline change policy: Changes prohibited for next upcoming match or simultaneous matches
- Only future matches can have deadline modifications
- Deadlines become permanently fixed once match becomes "next"

## Key Integration Points

- **Keycloak**: OAuth 2.0 server on port 8080 (realm: `betting-championship`)
- **Database**: PostgreSQL on port 5432 (DB: `betting_championship`)
- **API Documentation**: FastAPI auto-generates docs at `/docs` and `/redoc`
- **CORS**: Configured for Angular dev server (localhost:4200) in both backend config and main.py
