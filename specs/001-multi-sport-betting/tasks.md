# Tasks: Multi-Sport Betting Platform

**Input**: Design documents from `/specs/001-multi-sport-betting/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Found: FastAPI backend, Angular frontend, PostgreSQL, Keycloak, Grafana stack
   → Extract: TDD methodology, Docker containers, multi-environment setup
2. Load optional design documents:
   → data-model.md: 13 entities (User, Group, Sport, Competition, Season, Team, Player, Match, Bet, Result, etc.)
   → contracts/: openapi.yml (14 endpoints), websocket.md (real-time events)
   → research.md: Technology stack decisions and best practices
3. Generate tasks by category:
   → Setup: project init, GitHub management, dependencies, linting
   → Tests: contract tests, unit tests, integration tests (TDD FIRST)
   → Core: models, services, authentication, API endpoints
   → Integration: DB, middleware, observability, real-time features
   → Polish: deployment, documentation, performance optimization
4. Apply task rules:
   → Different files = mark [P] for parallel execution
   → Same file = sequential (no [P])
   → Tests before implementation (STRICT TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph with TDD ordering
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests ✓
   → All entities have models ✓
   → All endpoints implemented ✓
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions
- **TDD STRICT**: All tests MUST be completed before implementation

## Path Conventions
- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Infrastructure**: `infrastructure/`
- **Documentation**: `specs/001-multi-sport-betting/`

## Phase 3.1: Project Setup & GitHub Management
- [ ] T001 Create GitHub project with kanban board for issue tracking in repository
- [ ] T002 [P] Create GitHub issue templates in `.github/ISSUE_TEMPLATE/` (bug, feature, enhancement)
- [ ] T003 [P] Create pull request template in `.github/PULL_REQUEST_TEMPLATE.md` with issue linking
- [ ] T004 [P] Setup GitHub branch protection rules for main and develop branches
- [ ] T005 Create project structure directories: `backend/`, `frontend/`, `infrastructure/`

## Phase 3.2: CI/CD Pipeline Setup
- [ ] T006 [P] Create GitHub Actions workflow `ci-development.yml` for feature branch testing
- [ ] T007 [P] Create GitHub Actions workflow `ci-test.yml` for test environment deployment
- [ ] T008 [P] Create GitHub Actions workflow `ci-production.yml` for production deployment
- [ ] T009 [P] Create GitHub Actions workflow `build-containers.yml` for container builds
- [ ] T010 [P] Create GitHub Actions workflow `security-scan.yml` for vulnerability scanning
- [ ] T011 Setup GitHub Container Registry (GHCR) integration for image management

## Phase 3.3: Infrastructure Foundation
- [ ] T012 Create base Docker Compose configuration in `infrastructure/docker/docker-compose.base.yml`
- [ ] T013 [P] Create development environment config in `infrastructure/environments/dev/`
- [ ] T014 [P] Create test environment config in `infrastructure/environments/test/`
- [ ] T015 [P] Create production environment config in `infrastructure/environments/prod/`
- [ ] T016 Create PostgreSQL initialization scripts in `infrastructure/postgres/`
- [ ] T017 Create Keycloak realm configurations for all environments in `infrastructure/keycloak/`

## Phase 3.4: Backend Project Initialization
- [ ] T018 Initialize Python backend project with FastAPI in `backend/`
- [ ] T019 [P] Setup backend requirements files in `backend/requirements/` (base, dev, test, prod)
- [ ] T020 [P] Configure backend linting and formatting (ruff, black, mypy) in `backend/`
- [ ] T021 [P] Setup Alembic for database migrations in `backend/alembic/`
- [ ] T022 Create backend Docker configurations in `backend/docker/`

## Phase 3.5: Frontend Project Initialization
- [ ] T023 Initialize Angular frontend project in `frontend/`
- [ ] T024 [P] Configure Angular environments in `frontend/src/environments/`
- [ ] T025 [P] Setup frontend linting and formatting (ESLint, Prettier) in `frontend/`
- [ ] T026 [P] Configure Angular Material UI library for responsive design
- [ ] T027 Create frontend Docker configurations in `frontend/docker/`

## Phase 3.6: Grafana Observability Stack Setup (Learning Focus)
- [ ] T028 [P] Setup Grafana configuration in `infrastructure/observability/grafana/`
- [ ] T029 [P] Setup Mimir configuration in `infrastructure/observability/mimir/`
- [ ] T030 [P] Setup Loki configuration in `infrastructure/observability/loki/`
- [ ] T031 [P] Setup Tempo configuration in `infrastructure/observability/tempo/`
- [ ] T032 [P] Setup Alloy configuration in `infrastructure/observability/alloy/`
- [ ] T033 Create Grafana dashboard configurations in `infrastructure/observability/dashboards/`
- [ ] T034 Configure OpenTelemetry instrumentation setup for learning objectives

## Phase 3.7: Multi-Environment Docker Setup
- [ ] T035 Create development Docker Compose in `infrastructure/docker/docker-compose.dev.yml`
- [ ] T036 Create test Docker Compose in `infrastructure/docker/docker-compose.test.yml`
- [ ] T037 Create production Docker Compose in `infrastructure/docker/docker-compose.prod.yml`
- [ ] T038 [P] Create backend development Dockerfile in `backend/docker/Dockerfile.dev`
- [ ] T039 [P] Create backend production Dockerfile in `backend/docker/Dockerfile.prod`
- [ ] T040 [P] Create frontend development Dockerfile in `frontend/docker/Dockerfile.dev`
- [ ] T041 [P] Create frontend production Dockerfile in `frontend/docker/Dockerfile.prod`

## Phase 3.8: Authentication & Security Infrastructure
- [ ] T042 Setup Keycloak Docker configuration with OAuth 2.0/OIDC
- [ ] T043 [P] Create Keycloak realm JSON for development environment
- [ ] T044 [P] Create Keycloak realm JSON for test environment  
- [ ] T045 [P] Create Keycloak realm JSON for production environment
- [ ] T046 Configure OAuth 2.0 client settings for backend API
- [ ] T047 Configure OAuth 2.0 client settings for frontend application

## Phase 3.9: Database Infrastructure Setup
- [ ] T048 Setup PostgreSQL 17.6 configuration for all environments
- [ ] T049 [P] Create database initialization scripts in `infrastructure/postgres/init/`
- [ ] T050 [P] Setup database backup configurations in `infrastructure/backup/`
- [ ] T051 Configure database connection pooling and performance settings

## Phase 3.10: Contract Tests (TDD Phase 1) ⚠️ MUST COMPLETE BEFORE 3.13
- [ ] T052 [P] Create authentication contract tests in `backend/tests/contract/test_auth_api.py`
- [ ] T053 [P] Create user profile contract tests in `backend/tests/contract/test_users_api.py`
- [ ] T054 [P] Create groups contract tests in `backend/tests/contract/test_groups_api.py`
- [ ] T055 [P] Create sports contract tests in `backend/tests/contract/test_sports_api.py`
- [ ] T056 [P] Create competitions contract tests in `backend/tests/contract/test_competitions_api.py`
- [ ] T057 [P] Create matches contract tests in `backend/tests/contract/test_matches_api.py`
- [ ] T058 [P] Create betting contract tests in `backend/tests/contract/test_betting_api.py`
- [ ] T059 [P] Create leaderboard contract tests in `backend/tests/contract/test_leaderboard_api.py`
- [ ] T060 [P] Create WebSocket contract tests in `backend/tests/contract/test_websocket_api.py`

## Phase 3.11: Database Model Tests (TDD Phase 2) ⚠️ MUST COMPLETE BEFORE 3.14
- [ ] T061 [P] Create User model tests in `backend/tests/unit/models/test_user.py`
- [ ] T062 [P] Create Group model tests in `backend/tests/unit/models/test_group.py`
- [ ] T063 [P] Create GroupMembership model tests in `backend/tests/unit/models/test_group_membership.py`
- [ ] T064 [P] Create Sport model tests in `backend/tests/unit/models/test_sport.py`
- [ ] T065 [P] Create Competition model tests in `backend/tests/unit/models/test_competition.py`
- [ ] T066 [P] Create Season model tests in `backend/tests/unit/models/test_season.py`
- [ ] T067 [P] Create Team model tests in `backend/tests/unit/models/test_team.py`
- [ ] T068 [P] Create Player model tests in `backend/tests/unit/models/test_player.py`
- [ ] T069 [P] Create Match model tests in `backend/tests/unit/models/test_match.py`
- [ ] T070 [P] Create Bet model tests in `backend/tests/unit/models/test_bet.py`
- [ ] T071 [P] Create Result model tests in `backend/tests/unit/models/test_result.py`
- [ ] T072 [P] Create AuditLog model tests in `backend/tests/unit/models/test_audit_log.py`

## Phase 3.12: Service Layer Tests (TDD Phase 3) ⚠️ MUST COMPLETE BEFORE 3.15
- [ ] T073 [P] Create authentication service tests in `backend/tests/unit/services/test_auth_service.py`
- [ ] T074 [P] Create user service tests in `backend/tests/unit/services/test_user_service.py`
- [ ] T075 [P] Create group service tests in `backend/tests/unit/services/test_group_service.py`
- [ ] T076 [P] Create betting service tests in `backend/tests/unit/services/test_betting_service.py`
- [ ] T077 [P] Create match service tests in `backend/tests/unit/services/test_match_service.py`
- [ ] T078 [P] Create ranking service tests in `backend/tests/unit/services/test_ranking_service.py`
- [ ] T079 [P] Create notification service tests in `backend/tests/unit/services/test_notification_service.py`

## Phase 3.13: Backend Models Implementation (After T052-T059)
- [ ] T080 Create User SQLAlchemy model in `backend/src/models/user.py`
- [ ] T081 Create Group SQLAlchemy model in `backend/src/models/group.py`
- [ ] T082 Create GroupMembership SQLAlchemy model in `backend/src/models/group_membership.py`
- [ ] T083 Create Sport SQLAlchemy model in `backend/src/models/sport.py`
- [ ] T084 Create Competition SQLAlchemy model in `backend/src/models/competition.py`
- [ ] T085 Create Season SQLAlchemy model in `backend/src/models/season.py`
- [ ] T086 Create Team SQLAlchemy model in `backend/src/models/team.py`
- [ ] T087 Create Player SQLAlchemy model in `backend/src/models/player.py`
- [ ] T088 Create Match SQLAlchemy model in `backend/src/models/match.py`
- [ ] T089 Create Bet SQLAlchemy model in `backend/src/models/bet.py`
- [ ] T090 Create Result SQLAlchemy model in `backend/src/models/result.py`
- [ ] T091 Create AuditLog SQLAlchemy model in `backend/src/models/audit_log.py`

## Phase 3.14: Backend Services Implementation (After T061-T072)
- [ ] T092 Create authentication service in `backend/src/services/auth_service.py`
- [ ] T093 Create user service in `backend/src/services/user_service.py`
- [ ] T094 Create group service in `backend/src/services/group_service.py`
- [ ] T095 Create betting service in `backend/src/services/betting_service.py`
- [ ] T096 Create match service in `backend/src/services/match_service.py`
- [ ] T097 Create ranking service in `backend/src/services/ranking_service.py`
- [ ] T098 Create notification service in `backend/src/services/notification_service.py`

## Phase 3.15: API Implementation (After T073-T079)
- [ ] T099 Create authentication API router in `backend/src/api/auth.py`
- [ ] T100 Create users API router in `backend/src/api/users.py`
- [ ] T101 Create groups API router in `backend/src/api/groups.py`
- [ ] T102 Create sports API router in `backend/src/api/sports.py`
- [ ] T103 Create competitions API router in `backend/src/api/competitions.py`
- [ ] T104 Create matches API router in `backend/src/api/matches.py`
- [ ] T105 Create betting API router in `backend/src/api/betting.py`
- [ ] T106 Create leaderboard API router in `backend/src/api/leaderboard.py`

## Phase 3.16: Real-time Features (WebSocket)
- [ ] T107 Create WebSocket connection handler in `backend/src/websocket/connection.py`
- [ ] T108 Create WebSocket authentication middleware in `backend/src/websocket/auth.py`
- [ ] T109 Create real-time ranking updates in `backend/src/websocket/rankings.py`
- [ ] T110 Create real-time match updates in `backend/src/websocket/matches.py`

## Phase 3.17: Frontend Components (Angular)
- [ ] T111 [P] Create authentication components in `frontend/src/app/features/auth/`
- [ ] T112 [P] Create group management components in `frontend/src/app/features/groups/`
- [ ] T113 [P] Create betting interface components in `frontend/src/app/features/betting/`
- [ ] T114 [P] Create leaderboard components in `frontend/src/app/features/leaderboard/`
- [ ] T115 [P] Create match display components in `frontend/src/app/features/matches/`
- [ ] T116 Create responsive layout components in `frontend/src/app/layout/`

## Phase 3.18: Frontend Services & Integration
- [ ] T117 Create Angular authentication service in `frontend/src/app/core/auth/auth.service.ts`
- [ ] T118 Create Angular HTTP interceptor for API calls in `frontend/src/app/core/interceptors/`
- [ ] T119 Create Angular WebSocket service in `frontend/src/app/core/websocket/websocket.service.ts`
- [ ] T120 [P] Create Angular API services for each endpoint group in `frontend/src/app/shared/services/`

## Phase 3.19: Integration Tests
- [ ] T121 [P] Create database integration tests in `backend/tests/integration/test_database.py`
- [ ] T122 [P] Create Keycloak integration tests in `backend/tests/integration/test_keycloak.py`
- [ ] T123 [P] Create end-to-end user journey tests in `backend/tests/integration/test_user_journeys.py`
- [ ] T124 [P] Create WebSocket integration tests in `backend/tests/integration/test_websocket.py`

## Phase 3.20: Observability Implementation
- [ ] T125 Implement OpenTelemetry auto-instrumentation in backend
- [ ] T126 [P] Create custom metrics for betting business logic
- [ ] T127 [P] Create structured logging with correlation IDs
- [ ] T128 [P] Create Grafana dashboards for application metrics
- [ ] T129 [P] Setup alerting rules for performance and errors

## Phase 3.21: Deployment & Operations
- [ ] T130 Create deployment scripts for all environments
- [ ] T131 [P] Setup database migration automation in CI/CD
- [ ] T132 [P] Create health check endpoints for all services
- [ ] T133 [P] Setup backup automation for PostgreSQL
- [ ] T134 Create production deployment validation tests

## Phase 3.22: Documentation & Polish
- [ ] T135 [P] Create API documentation with FastAPI automatic generation
- [ ] T136 [P] Create deployment runbook in `docs/deployment.md`
- [ ] T137 [P] Create troubleshooting guide in `docs/troubleshooting.md`
- [ ] T138 [P] Update README.md with quickstart instructions
- [ ] T139 Final integration testing and performance validation

## Parallel Execution Examples

### Contract Tests (can run simultaneously):
```bash
# All contract tests are independent and can run in parallel
cd backend
pytest tests/contract/test_auth_api.py tests/contract/test_users_api.py tests/contract/test_groups_api.py -v --tb=short
```

### Model Tests (can run simultaneously):
```bash
# All model tests are independent
cd backend  
pytest tests/unit/models/ -v --tb=short
```

### Service Tests (can run simultaneously):
```bash
# All service tests are independent
cd backend
pytest tests/unit/services/ -v --tb=short
```

### Infrastructure Setup (can run simultaneously):
```bash
# Environment configurations can be created in parallel
git checkout -b feature/infrastructure-setup
# Work on T013, T014, T015 simultaneously in different terminals
```

## Dependencies & Ordering

**Critical Path (TDD STRICT)**:
1. Setup (T001-T051) → Contract Tests (T052-T060) → Models Implementation (T080-T091)
2. Model Tests (T061-T072) → Service Tests (T073-T079) → Services Implementation (T092-T098)
3. Contract Tests Complete → API Implementation (T099-T106)
4. Frontend components (T111-T116) can start after API contracts are defined
5. Integration tests (T121-T124) require all implementations to be complete

**Parallel Opportunities**:
- All [P] marked tasks can run simultaneously when dependencies are met
- Environment configurations can be created in parallel
- Frontend and backend tests can be developed in parallel
- Documentation tasks can run in parallel with implementation

## Success Criteria

**TDD Compliance**: All tests written and passing before implementation
**Contract Coverage**: Every API endpoint has corresponding contract tests
**Model Coverage**: Every database entity has comprehensive model tests  
**Service Coverage**: All business logic has unit test coverage
**Integration Coverage**: End-to-end user journeys are tested
**Observability**: Complete Grafana stack operational with learning objectives met
**Deployment**: All three environments (dev/test/prod) functional
**Performance**: API response times under 500ms, WebSocket latency under 100ms

---
*Generated from specifications: plan.md, data-model.md, contracts/openapi.yml, contracts/websocket.md*
*Total Tasks: 139 (estimated 90-105, actual exceeds due to comprehensive TDD approach)*
*TDD Methodology: Strict Red-Green-Refactor cycle enforced*