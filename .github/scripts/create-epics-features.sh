#!/bin/bash

# Create GitHub Project structure with Epics and Features
set -e

echo "🏗️  Creating GitHub Project structure with Epics and Features..."

# Project ID from the created project
PROJECT_ID="4"

# Create Epic Issues
echo "📊 Creating Epic Issues..."

# Epic 1: Infrastructure & Setup
gh issue create \
  --title "Epic: Infrastructure & Project Setup" \
  --body "## Epic Overview
This epic encompasses all foundational infrastructure, project setup, and development environment configuration.

## Scope
- GitHub project management setup
- CI/CD pipeline configuration  
- Infrastructure foundation (Docker, environments)
- Backend and Frontend project initialization
- Observability stack setup (Grafana, Mimir, Loki, Tempo)
- Authentication infrastructure
- Database setup

## Success Criteria
- [ ] Complete development environment ready
- [ ] All CI/CD pipelines functional
- [ ] Observability stack operational
- [ ] Multi-environment Docker setup complete
- [ ] Authentication and database infrastructure ready

## Related Features
- Project Setup & GitHub Management
- CI/CD Pipeline Setup
- Infrastructure Foundation
- Backend Project Initialization
- Frontend Project Initialization
- Observability Stack Setup
- Multi-Environment Docker Setup
- Authentication & Security Infrastructure
- Database Infrastructure Setup

## Tasks Included
T001-T051 (51 tasks)

**Priority**: High
**Phase**: 1 - Infrastructure Setup" \
  --label "epic,priority:high,infrastructure" \
  --repo ChPfisterer/betting-league-championship

# Epic 2: Test Development (TDD)
gh issue create \
  --title "Epic: Test Development (TDD Methodology)" \
  --body "## Epic Overview
This epic implements comprehensive Test-Driven Development methodology with contract tests, unit tests, and integration tests written BEFORE any implementation.

## TDD Approach
Following strict Red-Green-Refactor methodology:
1. **Contract Tests First**: API endpoint contracts
2. **Unit Tests**: Models, services, business logic
3. **Integration Tests**: Database, external services, end-to-end flows

## Scope
- Contract tests for all API endpoints (14 endpoints)
- Unit tests for all database models (13 entities)
- Unit tests for all service layers
- Integration tests for critical user journeys
- WebSocket contract testing

## Success Criteria
- [ ] All API contracts defined and tested
- [ ] 100% model test coverage
- [ ] All service logic has unit tests
- [ ] Integration test suite covers critical paths
- [ ] TDD workflow established and documented

## Related Features
- Contract Tests (API endpoints)
- Database Model Tests
- Service Layer Tests

## Tasks Included
T052-T079 (28 tasks)

**Priority**: High
**Phase**: 2 - Test Development (TDD)" \
  --label "epic,priority:high,tdd" \
  --repo ChPfisterer/betting-league-championship

# Epic 3: Core Implementation
gh issue create \
  --title "Epic: Core Implementation (Backend & Frontend)" \
  --body "## Epic Overview
This epic implements the core application functionality including backend models, services, API endpoints, and frontend components - all AFTER tests are written and failing.

## Implementation Strategy
- Models implemented only after model tests exist
- Services implemented only after service tests exist
- API endpoints implemented only after contract tests exist
- Frontend components follow component-first TDD

## Scope
- Backend database models (13 entities)
- Backend service layer (authentication, user, group, betting, match, ranking)
- REST API implementation (14 endpoints)
- WebSocket real-time features
- Frontend components (authentication, groups, betting, leaderboard, matches)
- Frontend services and API integration

## Success Criteria
- [ ] All database models implemented and tested
- [ ] All service layers functional
- [ ] Complete REST API operational
- [ ] Real-time WebSocket features working
- [ ] Frontend application fully functional
- [ ] All tests passing (80%+ backend, 70%+ frontend coverage)

## Related Features
- Backend Models Implementation
- Backend Services Implementation
- API Implementation
- Real-time Features (WebSocket)
- Frontend Components
- Frontend Services & Integration

## Tasks Included
T080-T120 (41 tasks)

**Priority**: High
**Phase**: 3 - Core Implementation" \
  --label "epic,priority:high,implementation" \
  --repo ChPfisterer/betting-league-championship

# Epic 4: Integration & Quality Assurance
gh issue create \
  --title "Epic: Integration & Quality Assurance" \
  --body "## Epic Overview
This epic focuses on integration testing, observability implementation, and end-to-end quality assurance to ensure the complete system works together reliably.

## Quality Focus
- Integration testing between all system components
- Observability and monitoring implementation
- Performance optimization and monitoring
- End-to-end user journey validation

## Scope
- Database integration tests
- Keycloak authentication integration
- End-to-end user journey tests
- WebSocket integration testing
- Custom metrics and monitoring
- Grafana dashboards
- Performance alerting
- Health check endpoints

## Success Criteria
- [ ] All integrations tested and functional
- [ ] Complete observability stack operational
- [ ] Performance monitoring and alerting active
- [ ] System health monitoring in place
- [ ] All quality gates passing

## Related Features
- Integration Tests
- Observability Implementation

## Tasks Included
T121-T129 (9 tasks)

**Priority**: Medium
**Phase**: 4 - Integration & Features" \
  --label "epic,priority:medium,integration" \
  --repo ChPfisterer/betting-league-championship

# Epic 5: Deployment & Operations
gh issue create \
  --title "Epic: Deployment & Operations" \
  --body "## Epic Overview
This epic covers deployment automation, operational procedures, documentation, and production readiness to ensure the system can be reliably deployed and maintained.

## Operations Focus
- Automated deployment processes
- Database migration automation
- Backup and recovery procedures
- Documentation and runbooks
- Production monitoring

## Scope
- CI/CD deployment automation
- Database migration automation
- PostgreSQL backup automation
- API documentation generation
- Deployment runbooks
- Troubleshooting guides
- README and quickstart documentation

## Success Criteria
- [ ] Automated deployment pipeline functional
- [ ] Database operations automated
- [ ] Backup and recovery procedures established
- [ ] Complete documentation available
- [ ] Production deployment successful

## Related Features
- Deployment & Operations

## Tasks Included
T131-T138 (8 tasks)

**Priority**: Medium
**Phase**: 5 - Polish & Deployment" \
  --label "epic,priority:medium,deployment" \
  --repo ChPfisterer/betting-league-championship

echo "✅ Epic issues created successfully!"
echo ""

# Create Feature Issues
echo "🔧 Creating Feature Issues..."

# Feature 1: Project Setup & GitHub Management
gh issue create \
  --title "Feature: Project Setup & GitHub Management" \
  --body "## Feature Overview
Establish complete GitHub project management infrastructure with templates, workflows, and branch protection.

## User Stories
- As a developer, I want standardized issue templates for consistent reporting
- As a project manager, I want automated branch protection and PR workflows
- As a team, we want CI/CD pipelines for automated testing and deployment

## Implementation Tasks
- T001: Create GitHub project with kanban board
- T002: Create GitHub issue templates
- T003: Create pull request template
- T004: Setup GitHub branch protection rules

## Acceptance Criteria
- [ ] GitHub project board operational
- [ ] Issue and PR templates available
- [ ] Branch protection rules enforced
- [ ] Automated workflows functional

**Parent Epic**: Infrastructure & Project Setup
**Priority**: High" \
  --label "feature,priority:high,infrastructure" \
  --repo ChPfisterer/betting-league-championship

# Feature 2: CI/CD Pipeline Setup
gh issue create \
  --title "Feature: CI/CD Pipeline Setup" \
  --body "## Feature Overview
Implement comprehensive CI/CD pipelines for development, testing, and production environments with automated testing and deployment.

## User Stories
- As a developer, I want automated testing on every feature branch
- As a DevOps engineer, I want automated deployment to test and production environments
- As a security officer, I want automated vulnerability scanning

## Implementation Tasks
- T006: Create GitHub Actions workflow for feature branch testing
- T007: Create GitHub Actions workflow for test environment deployment
- T008: Create GitHub Actions workflow for production deployment
- T009: Create GitHub Actions workflow for container builds
- T010: Create GitHub Actions workflow for security scanning

## Acceptance Criteria
- [ ] Feature branch testing automated
- [ ] Test environment deployment automated
- [ ] Production deployment automated
- [ ] Container builds automated
- [ ] Security scanning integrated

**Parent Epic**: Infrastructure & Project Setup
**Priority**: High" \
  --label "feature,priority:high,infrastructure" \
  --repo ChPfisterer/betting-league-championship

# Feature 3: Backend Project Initialization
gh issue create \
  --title "Feature: Backend Project Initialization" \
  --body "## Feature Overview
Initialize FastAPI backend project with proper structure, dependencies, and development tools.

## User Stories
- As a backend developer, I want a properly structured Python project
- As a developer, I want automated code formatting and linting
- As a DBA, I want database migration management

## Implementation Tasks
- T018: Initialize Python backend project with FastAPI
- T019: Setup backend requirements files
- T020: Configure backend linting and formatting
- T021: Setup Alembic for database migrations
- T022: Create backend Docker configurations

## Acceptance Criteria
- [ ] FastAPI project structure established
- [ ] Dependencies properly organized
- [ ] Code quality tools configured
- [ ] Database migrations ready
- [ ] Docker configurations available

**Parent Epic**: Infrastructure & Project Setup
**Priority**: High" \
  --label "feature,priority:high,backend" \
  --repo ChPfisterer/betting-league-championship

# Feature 4: Frontend Project Initialization
gh issue create \
  --title "Feature: Frontend Project Initialization" \
  --body "## Feature Overview
Initialize Angular frontend project with proper structure, UI framework, and development tools.

## User Stories
- As a frontend developer, I want a properly structured Angular project
- As a UI/UX developer, I want a responsive UI framework
- As a developer, I want automated code formatting and linting

## Implementation Tasks
- T023: Initialize Angular frontend project
- T024: Configure Angular environments
- T025: Setup frontend linting and formatting
- T026: Configure Angular Material UI library
- T027: Create frontend Docker configurations

## Acceptance Criteria
- [ ] Angular project structure established
- [ ] Environment configurations ready
- [ ] Code quality tools configured
- [ ] UI framework integrated
- [ ] Docker configurations available

**Parent Epic**: Infrastructure & Project Setup
**Priority**: High" \
  --label "feature,priority:high,frontend" \
  --repo ChPfisterer/betting-league-championship

# Feature 5: Contract Tests (API Endpoints)
gh issue create \
  --title "Feature: Contract Tests (API Endpoints)" \
  --body "## Feature Overview
Implement contract tests for all API endpoints following TDD methodology - these tests must be written BEFORE any API implementation.

## TDD Approach
1. **RED**: Write failing contract tests for each API endpoint
2. **GREEN**: Implement minimal API endpoints to pass tests
3. **REFACTOR**: Improve API implementation while keeping tests green

## User Stories
- As an API consumer, I want reliable and tested API contracts
- As a developer, I want clear API specifications driven by tests
- As a QA engineer, I want automated API testing

## Implementation Tasks
- T052: Create authentication contract tests
- T053: Create user profile contract tests
- T054: Create groups contract tests
- T055: Create sports contract tests
- T056: Create competitions contract tests
- T057: Create matches contract tests
- T058: Create betting contract tests
- T059: Create leaderboard contract tests
- T060: Create WebSocket contract tests

## Acceptance Criteria
- [ ] All 14 API endpoints have contract tests
- [ ] WebSocket events are contract tested
- [ ] Tests fail initially (RED phase)
- [ ] Contract tests are comprehensive and clear

**Parent Epic**: Test Development (TDD Methodology)
**Priority**: High" \
  --label "feature,priority:high,tdd,tests" \
  --repo ChPfisterer/betting-league-championship

# Feature 6: Database Model Tests
gh issue create \
  --title "Feature: Database Model Tests" \
  --body "## Feature Overview
Implement comprehensive unit tests for all database models following TDD methodology - these tests must be written BEFORE model implementation.

## TDD Approach
1. **RED**: Write failing tests for each database model
2. **GREEN**: Implement minimal models to pass tests
3. **REFACTOR**: Improve model implementation while keeping tests green

## User Stories
- As a developer, I want well-tested database models
- As a DBA, I want validated model relationships and constraints
- As a QA engineer, I want automated model testing

## Implementation Tasks
- T061: Create User model tests
- T062: Create Group model tests
- T063: Create GroupMembership model tests
- T064: Create Sport model tests
- T065: Create Competition model tests
- T066: Create Season model tests
- T067: Create Team model tests
- T068: Create Player model tests
- T069: Create Match model tests
- T070: Create Bet model tests
- T071: Create Result model tests
- T072: Create AuditLog model tests

## Acceptance Criteria
- [ ] All 13 database entities have unit tests
- [ ] Model relationships are tested
- [ ] Validation rules are tested
- [ ] Tests fail initially (RED phase)

**Parent Epic**: Test Development (TDD Methodology)
**Priority**: High" \
  --label "feature,priority:high,tdd,tests" \
  --repo ChPfisterer/betting-league-championship

# Feature 7: Service Layer Tests
gh issue create \
  --title "Feature: Service Layer Tests" \
  --body "## Feature Overview
Implement comprehensive unit tests for all service layer components following TDD methodology - these tests must be written BEFORE service implementation.

## TDD Approach
1. **RED**: Write failing tests for each service component
2. **GREEN**: Implement minimal services to pass tests
3. **REFACTOR**: Improve service implementation while keeping tests green

## User Stories
- As a developer, I want well-tested business logic
- As a product owner, I want validated betting and scoring logic
- As a QA engineer, I want automated service testing

## Implementation Tasks
- T073: Create authentication service tests
- T074: Create user service tests
- T075: Create group service tests
- T076: Create betting service tests
- T077: Create match service tests
- T078: Create ranking service tests
- T079: Create notification service tests

## Acceptance Criteria
- [ ] All business logic services have unit tests
- [ ] Complex betting logic is thoroughly tested
- [ ] Service interactions are tested
- [ ] Tests fail initially (RED phase)

**Parent Epic**: Test Development (TDD Methodology)
**Priority**: High" \
  --label "feature,priority:high,tdd,tests" \
  --repo ChPfisterer/betting-league-championship

echo "✅ Feature issues created successfully!"
echo ""
echo "📊 Summary:"
echo "   - Created GitHub Project: https://github.com/users/ChPfisterer/projects/4"
echo "   - Created 5 Epic issues for high-level organization"
echo "   - Created 7 Feature issues for mid-level grouping"
echo "   - Total: 12 organizational issues + 80 task issues = 92 total issues"
echo ""
echo "🎯 Next Steps:"
echo "   1. Add all task issues to the GitHub project"
echo "   2. Link task issues to their parent features"
echo "   3. Link feature issues to their parent epics"
echo "   4. Configure project board columns and automation"