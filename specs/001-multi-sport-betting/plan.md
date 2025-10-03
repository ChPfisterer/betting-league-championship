
# Implementation Plan: Multi-Sport Betting Platform

**Branch**: `001-multi-sport-betting` | **Date**: October 3, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mul### Test-Driven Development (TDD) Methodology
- **Red-Green-Refactor Cycle**: Write failing tests, implement minimum code, refactor for quality
- **Contract-First Development**: API contracts drive both frontend and backend tests
- **Test Categories**: Unit tests, integration tests, contract tests, end-to-end tests
- **Quality Gates**: All tests must pass before code review and merge
- **Test Coverage**: Minimum 80% code coverage for backend, 70% for frontend
- **Continuous Testing**: Automated test execution on every commit and PR

### Testing Strategy (TDD Focus)
- **Backend TDD**: pytest with factory patterns, fixtures, and test data builders
- **Frontend TDD**: Jasmine/Karma with component testing and service mocking
- **API Contract Testing**: OpenAPI-driven contract tests using generated schemas
- **Integration Testing**: Real database and service integration with Testcontainers
- **End-to-End Testing**: User journey validation with Playwright or Cypress
- **Performance Testing**: Load testing and response time validation

### Development Workflowi-sport-betting/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Comprehensive multi-sport betting platform supporting soccer, handball, and extensible sports architecture. Users register, join groups, place bets on match outcomes, and compete through live rankings. Features include OAuth 2.0/Keycloak authentication, private/public groups with admin controls, provisional results system, and anti-gaming deadline policies. Technical approach: Python FastAPI backend, Angular frontend, PostgreSQL database, Keycloak IAM, containerized deployment with Docker Compose across dev/test/prod environments.

### Latest Stable Versions (October 2025)
- **FastAPI**: 0.115.13 (with Pydantic 2.7+ support)
- **Angular**: 20.1.4 (with enhanced standalone components)  
- **PostgreSQL**: 17.6 (with performance and security improvements)
- **Keycloak**: 26.3.2 (with improved container support)
- **Python**: 3.12.7 (latest stable runtime)
- **Node.js**: 20.18.0 (LTS for Angular development)
- **Docker**: 27.3.1 (latest stable with multi-platform support)
- **Grafana Stack**: 11.3.0 (Grafana), 2.14.1 (Mimir), 3.2.0 (Loki), 2.6.1 (Tempo), 1.4.2 (Alloy)
- **OpenTelemetry**: 1.31.0 (latest instrumentation libraries)

## Technical Context
**Language/Version**: Python 3.12 (backend), TypeScript/Angular 20 (frontend)  
**Primary Dependencies**: FastAPI 0.115.x, Angular 20.x, PostgreSQL 17.x, Keycloak 26.x  
**Storage**: PostgreSQL 17.6 database with complex relational schema for sports betting data  
**Testing**: pytest (backend), Jasmine/Karma (frontend), **Test-Driven Development (TDD)** methodology, contract testing  
**Target Platform**: Docker containers with multi-environment Docker Compose deployment (dev/test/prod) and GitHub Actions CI/CD  
**Project Type**: web - frontend + backend architecture with containerized services and automated deployment  
**Performance Goals**: Support concurrent betting, real-time rankings, <500ms API response times (development realistic)  
**Constraints**: Multi-environment deployment (dev/test/prod), Keycloak integration, mobile-responsive design, development-focused approach, **TDD workflow**  
**Scale/Scope**: Multi-sport competitions, group management, complex scoring rules, basic audit trails, essential observability, future scalability

**User-Specified Technical Details**: 
- Backend: Python FastAPI 0.115.x (latest stable)
- Frontend: Angular 20.x (latest stable) 
- Database: PostgreSQL 17.6 (latest stable)
- IAM: Keycloak 26.3.x (latest stable)
- Deployment: Docker containers with Docker Compose
- Multi-environment: dev, test, prod configurations with separate compose files
- Containerization: Multi-stage Docker builds with environment-specific optimizations
- CI/CD: GitHub Actions with automated testing, building, and deployment
- Container Registry: GitHub Container Registry (GHCR) for image management
- **Observability Stack**: Complete Grafana ecosystem (Grafana, Mimir, Loki, Tempo, Alloy) - Core Learning Requirement
- **Telemetry**: OpenTelemetry for comprehensive instrumentation - Core Learning Requirement
- Issue tracking: GitHub Issues with GitHub Projects
- Git workflow: Feature branches with pull requests

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Initial Assessment**: ✅ PASS
- Architecture follows separation of concerns (frontend/backend/database)
- Technology choices are mature and well-supported
- Containerization supports development best practices
- Multi-environment deployment supports proper CI/CD
- No excessive complexity violations identified
- Requirements are testable and implementable

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
backend/
├── src/
│   ├── models/           # SQLAlchemy models for all entities
│   ├── schemas/          # Pydantic schemas for API contracts
│   ├── services/         # Business logic services
│   ├── api/              # FastAPI routers and endpoints
│   ├── auth/             # Keycloak integration and auth middleware
│   ├── database/         # Database configuration and migrations
│   └── core/             # Configuration and utilities
├── tests/
│   ├── contract/         # API contract tests
│   ├── integration/      # Service integration tests
│   └── unit/             # Unit tests for business logic
├── alembic/              # Database migrations
├── docker/               # Docker configurations
│   ├── Dockerfile.dev    # Development container
│   ├── Dockerfile.prod   # Production container
│   └── entrypoint.sh     # Container entrypoint script
├── config/               # Environment-specific configurations
│   ├── settings.py       # Configuration classes
│   ├── dev.py           # Development settings
│   ├── test.py          # Test settings
│   └── prod.py          # Production settings
└── requirements/         # Environment-specific dependencies
    ├── base.txt         # Base requirements
    ├── dev.txt          # Development requirements
    ├── test.txt         # Test requirements
    └── prod.txt         # Production requirements

frontend/
├── src/
│   ├── app/
│   │   ├── core/         # Guards, interceptors, services
│   │   ├── features/     # Feature modules (auth, betting, groups)
│   │   ├── shared/       # Shared components and services
│   │   └── layout/       # Application layout components
│   ├── assets/           # Static assets
│   └── environments/     # Environment configurations
│       ├── environment.dev.ts
│       ├── environment.test.ts
│       └── environment.prod.ts
├── tests/
│   ├── e2e/              # End-to-end tests
│   ├── integration/      # Component integration tests
│   └── unit/             # Unit tests for components/services
├── docker/               # Frontend container configurations
│   ├── Dockerfile.dev    # Development container with hot reload
│   ├── Dockerfile.prod   # Production container with nginx
│   ├── nginx.dev.conf    # Development nginx configuration
│   └── nginx.prod.conf   # Production nginx configuration
└── config/               # Build configurations
    ├── angular.dev.json  # Development build config
    ├── angular.test.json # Test build config
    └── angular.prod.json # Production build config

infrastructure/
├── docker/
│   ├── docker-compose.dev.yml      # Development environment
│   ├── docker-compose.test.yml     # Test environment
│   ├── docker-compose.prod.yml     # Production environment
│   ├── docker-compose.base.yml     # Base services (shared)
│   └── dockerfiles/                # Environment-specific Dockerfiles
│       ├── backend.dev.Dockerfile
│       ├── backend.prod.Dockerfile
│       ├── frontend.dev.Dockerfile
│       └── frontend.prod.Dockerfile
├── environments/
│   ├── dev/                        # Development configurations
│   │   ├── .env.dev
│   │   ├── keycloak-realm.json
│   │   ├── postgres-init.sql
│   │   └── grafana-datasources.yml
│   ├── test/                       # Test configurations
│   │   ├── .env.test
│   │   ├── keycloak-realm.json
│   │   ├── postgres-init.sql
│   │   └── grafana-datasources.yml
│   └── prod/                       # Production configurations
│       ├── .env.prod
│       ├── keycloak-realm.json
│       ├── postgres-init.sql
│       └── grafana-datasources.yml
├── keycloak/             # Keycloak realm and client configurations
├── postgres/             # Database initialization scripts
├── grafana/              # Grafana dashboards and configurations
├── observability/        # Mimir, Loki, Tempo, Alloy configurations
│   ├── prometheus/       # Prometheus configuration (for local dev)
│   ├── exporters/        # PostgreSQL, Redis, cAdvisor exporters
│   └── dashboards/       # Pre-built Grafana dashboards
├── backup/               # Simple backup scripts and policies
│   └── postgres-backup/  # Basic database backup scripts
└── nginx/                # Reverse proxy configurations

.github/
├── workflows/            # CI/CD pipelines with branch protection
│   ├── ci-development.yml       # Development environment CI
│   ├── ci-test.yml              # Test environment CI/CD
│   ├── ci-production.yml        # Production deployment
│   ├── build-containers.yml     # Container build and push
│   ├── security-scan.yml        # Security scanning
│   └── dependency-update.yml    # Automated dependency updates
├── ISSUE_TEMPLATE/       # Issue templates for project management
├── PULL_REQUEST_TEMPLATE.md  # PR template with issue linking
└── projects/             # GitHub Projects kanban configuration
```

**Structure Decision**: Web application architecture selected with separate backend and frontend services. This supports the requirement for a comprehensive responsive web application with proper separation of concerns, independent scaling, and multi-environment deployment. The structure accommodates the complex data model, authentication integration, and real-time features required for the betting platform.

## Development Workflow

### GitHub Project Management
- **GitHub Projects**: Use GitHub Projects (Beta) for kanban-style project management
- **Issue Tracking**: All features, bugs, and tasks tracked as GitHub Issues
- **Milestones**: Phase-based milestones for release planning
- **Labels**: Standardized labels for priority, type, component, and status
- **Templates**: Issue and PR templates for consistency and traceability

### Branching Strategy (Git Flow)
- **Main Branch**: `main` - production-ready code only
- **Development Branch**: `develop` - integration branch for features
- **Feature Branches**: `feature/issue-number-description` for each task
- **Release Branches**: `release/version` for release preparation
- **Hotfix Branches**: `hotfix/issue-description` for critical fixes

### Pull Request Workflow
- **Branch per Task**: Each GitHub Issue gets its own feature branch
- **PR Requirements**: Automated checks, code review, issue linking
- **Issue Linking**: Use "Closes #123" in PR description for automatic linking
- **Review Process**: Minimum 1 reviewer, all checks must pass
- **Merge Strategy**: Squash and merge for clean history

### CI/CD Pipeline (GitHub Actions)
- **Development CI**: Automated testing on feature branches
- **Test Environment**: Automated deployment to test environment
- **Production Deployment**: Automated release pipeline with approvals
- **Container Registry**: GitHub Container Registry (GHCR) for image storage
- **Security Scanning**: Vulnerability scanning for containers and dependencies
- **Quality Gates**: Code coverage, security checks, performance tests

### Pipeline Triggers
- **Feature Branches**: Run tests and build containers
- **Pull Requests**: Full CI pipeline with deployment to test environment
- **Main Branch**: Deploy to production with manual approval
- **Release Tags**: Create versioned container images and releases
- **Scheduled**: Daily dependency updates and security scans

### Observability Stack (Grafana) - Core Learning Requirement
- **Grafana 11.3.0**: Dashboards and visualization platform (learning focus: dashboard design, alerting)
- **Mimir 2.14.1**: Prometheus-compatible metrics storage (learning focus: time-series data, PromQL queries)
- **Loki 3.2.0**: Log aggregation and querying (learning focus: log parsing, LogQL syntax)
- **Tempo 2.6.1**: Distributed tracing backend (learning focus: trace analysis, service mapping)
- **Alloy 1.4.2**: Telemetry collection and processing (learning focus: data collection, routing, transformation)
- **OpenTelemetry 1.31.0**: Instrumentation for traces, metrics, and logs (learning focus: auto-instrumentation, custom spans)

### Learning Objectives for Grafana Stack
- **Hands-on Experience**: Deploy and configure all components from scratch
- **Dashboard Creation**: Build custom dashboards for application metrics
- **Query Languages**: Learn PromQL for metrics and LogQL for logs
- **Alerting**: Configure alerting rules and notification channels
- **Trace Analysis**: Understand distributed tracing and performance optimization
- **Data Collection**: Configure Alloy for telemetry collection and routing

### Monitoring Requirements (Comprehensive Learning Focus)
- **Application Metrics**: Request latency, throughput, error rates, response times (via OpenTelemetry)
- **Business Metrics**: Bet placement rates, user activity, match statistics (custom metrics)
- **Infrastructure Metrics**: CPU, memory, disk, network usage (via Alloy collection)
- **Distributed Tracing**: End-to-end request tracing with OpenTelemetry (manual and auto-instrumentation)
- **Centralized Logging**: Structured logs with correlation IDs (Loki aggregation)
- **Custom Dashboards**: Application-specific Grafana dashboards with PromQL queries
- **Alerting Rules**: Practical alerting for errors, performance, and business metrics
- **Health Checks**: Service readiness and liveness probes
- **Learning Focus**: Hands-on experience with all Grafana stack components
- **Query Learning**: Practical PromQL and LogQL development
- **Trace Analysis**: Performance optimization through distributed tracing

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh copilot`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each API endpoint → contract test task [P]
- Each database entity → SQLAlchemy model creation task [P] 
- Each user story from spec → integration test task
- Infrastructure setup tasks for Docker, Keycloak, PostgreSQL
- Multi-environment containerization tasks (dev/test/prod)
- Environment-specific configuration tasks
- CI/CD pipeline setup tasks (GitHub Actions workflows)
- Container registry and image management tasks
- Observability setup tasks for Grafana stack (Mimir, Loki, Tempo, Alloy)
- Frontend component tasks based on API contracts
- WebSocket implementation tasks for real-time features
- Authentication integration tasks for Keycloak
- Admin interface tasks for match and group management
- GitHub project management setup (issues, templates, workflows)

**Ordering Strategy**:
- **TDD order (STRICT)**: All tests before implementation - NO EXCEPTIONS
- **Contract-First**: API contracts before any endpoint implementation
- **Test Categories**: Contract tests → Unit tests → Integration tests → Implementation
- **Dependency order**: Infrastructure → Containerization → Observability → Tests → Implementation
- **GitHub project setup**: Before feature development
- **Environment configurations**: Before service deployment
- **Base Docker images**: Before environment-specific builds
- **Database models**: Only after database tests are written
- **Authentication setup**: Only after auth tests are written
- **Core betting logic**: Only after business logic tests are written
- **Mark [P] for parallel execution**: Independent test files can run in parallel

**Estimated Task Categories** (TDD Methodology):
1. **Project Setup** (3-5 tasks): GitHub templates, workflows, branching strategy
2. **CI/CD Pipeline** (6-8 tasks): GitHub Actions workflows, container registry, deployment automation
3. **Infrastructure Setup** (8-10 tasks): Docker configs, multi-environment setup, database
4. **Containerization** (6-8 tasks): Dockerfiles, compose files, environment configs
5. **Security Essentials** (4-6 tasks): OAuth 2.0/OIDC, basic audit logging, secret management
6. **Grafana Observability Stack** (10-12 tasks): Grafana, Mimir, Loki, Tempo, Alloy setup and configuration
7. **OpenTelemetry Implementation** (6-8 tasks): Auto-instrumentation, custom spans, metrics collection
8. **Dashboard & Alerting** (5-7 tasks): Custom dashboards, alerting rules, query development
9. **Backup & Monitoring** (3-5 tasks): Database backups, health checks
10. **Contract Tests (TDD Phase 1)** (12-15 tasks): API contract tests for all endpoints [BEFORE implementation]
11. **Unit Tests (TDD Phase 2)** (10-12 tasks): Business logic and service unit tests [BEFORE implementation]
12. **Integration Tests (TDD Phase 3)** (8-10 tasks): Database and service integration tests [BEFORE implementation]
13. **Backend Implementation** (8-10 tasks): Models, authentication, core services [AFTER tests]
14. **API Implementation** (12-15 tasks): REST endpoints, WebSocket handlers [AFTER contract tests]
15. **Frontend Implementation** (10-12 tasks): Components, routing, services [AFTER component tests]
16. **Business Logic Implementation** (8-10 tasks): Betting system, rankings [AFTER business logic tests]
17. **Admin Features** (5-7 tasks): Match management, group administration
18. **End-to-End Testing** (4-6 tasks): User journey validation, performance tests
19. **Deployment & Operations** (4-6 tasks): Environment deployment, basic operations

**Estimated Output**: 90-105 numbered, ordered tasks in tasks.md with **STRICT TDD ordering** and parallel execution markers

**TDD Focus**: All implementation tasks have corresponding test tasks that MUST be completed first

**Priority Levels**:
- P0: Core functionality (auth, basic betting, groups)
- P1: Enhanced features (real-time updates, admin tools)
- P2: Advanced features (detailed statistics, advanced admin)

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none required)

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
