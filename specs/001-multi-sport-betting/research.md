# Research: Multi-Sport Betting Platform

## Technology Stack Research

### Backend Framework: FastAPI
**Decision**: FastAPI 0.115.13 (latest stable)
**Rationale**: 
- High performance async framework ideal for real-time features
- Automatic OpenAPI/Swagger documentation generation
- Built-in data validation with Pydantic 2.7+
- Excellent WebSocket support for live rankings
- Strong typing support for maintainable code
- Native OAuth 2.0/OpenID Connect support for Keycloak integration
- Latest version includes performance improvements and security updates

**Alternatives considered**: 
- Django: More heavyweight, less suitable for real-time features
- Flask: Requires more manual configuration, less type safety

### Frontend Framework: Angular
**Decision**: Angular 20.1.4 (latest stable with standalone components)
**Rationale**:
- Mature framework with strong TypeScript support
- Comprehensive ecosystem for enterprise applications
- Built-in reactive forms perfect for betting interfaces
- RxJS for handling real-time updates and notifications
- Angular Material 20.x for responsive mobile-first design
- Strong routing and state management capabilities
- Latest version includes performance improvements and new features
- Improved standalone component architecture

**Alternatives considered**:
- React: Requires more third-party libraries for complete solution
- Vue.js: Smaller ecosystem for complex enterprise features

### Database: PostgreSQL
**Decision**: PostgreSQL 17.6 (latest stable)
**Rationale**:
- ACID compliance essential for betting data integrity
- Complex queries for ranking calculations and statistics
- Enhanced JSON/JSONB support for flexible competition configurations
- Strong performance under concurrent load with new optimizations
- Excellent transaction isolation for concurrent betting
- Rich indexing capabilities for fast leaderboard queries
- Latest version includes performance improvements and new features
- Enhanced security and reliability features

**Alternatives considered**:
- MySQL: Less advanced SQL features for complex rankings
- MongoDB: Lacks ACID compliance needed for financial integrity

### Authentication: Keycloak with OAuth 2.0/OIDC
**Decision**: Keycloak 26.3.2 (latest stable) with state-of-the-art OAuth 2.0/OIDC
**Rationale**:
- **OAuth 2.0 Authorization Framework**: RFC 6749 compliant implementation
- **OpenID Connect 1.0**: Identity layer on top of OAuth 2.0 for authentication
- **PKCE (Proof Key for Code Exchange)**: RFC 7636 for enhanced security in public clients
- **JWT Access Tokens**: RFC 7519 with RS256/ES256 signing algorithms
- **Token Introspection**: RFC 7662 for real-time token validation
- **Device Authorization Grant**: RFC 8628 for IoT and limited input devices
- **Built-in Identity Providers**: Google, Facebook, Apple, GitHub, Microsoft with OIDC
- **Advanced Security Features**: MFA, risk-based authentication, adaptive security
- **Session Management**: OIDC Session Management 1.0 and Front-Channel Logout
- **Scalable Multi-Realm Architecture**: Tenant isolation and customization
- **Standards Compliance**: FIDO2/WebAuthn, SAML 2.0, OAuth 2.1 draft support
- **Cloud-Native Design**: Kubernetes-ready with horizontal scaling

**Security Implementation**:
- **Authorization Code Flow with PKCE**: For frontend SPA security
- **Client Credentials Flow**: For backend service-to-service communication
- **Refresh Token Rotation**: Enhanced security with automatic rotation
- **Scope-Based Authorization**: Fine-grained permissions and resource access
- **Role-Based Access Control (RBAC)**: Group admin privileges and user roles

**Alternatives considered**:
- Auth0: Commercial solution, higher costs, less customization
- AWS Cognito: Vendor lock-in, limited customization options
- Custom implementation: Security risks, compliance overhead, maintenance burden

## Integration Patterns Research

### OAuth 2.0/OIDC Authentication Flow
**Decision**: Authorization Code Flow with PKCE for frontend, Client Credentials for backend
**Rationale**:
- **Frontend (Angular SPA)**: Authorization Code Flow + PKCE (RFC 7636)
  - Redirects to Keycloak for authentication
  - PKCE prevents authorization code interception attacks
  - Automatic token refresh with rotation
  - Silent authentication for seamless UX
- **Backend (FastAPI)**: Client Credentials Flow for service authentication
  - Machine-to-machine authentication for internal services
  - JWT Bearer token validation with JWK Set rotation
  - Scope-based authorization for API endpoints
  - Token introspection for real-time validation
- **Social Login Integration**: OIDC federation with external providers
  - Google, Facebook, Apple identity providers
  - Automatic user provisioning and profile mapping
  - Consistent token format across all authentication methods

### Real-time Updates Architecture
**Decision**: WebSocket + Server-Sent Events hybrid with OAuth 2.0 Bearer tokens
**Rationale**:
- WebSockets for bi-directional real-time ranking updates
- SSE for one-way notifications (match updates, deadline alerts)
- Bearer token authentication for WebSocket connections
- FastAPI WebSocket support with Redis for scaling
- Angular WebSocket services with automatic token refresh

### Database Schema Patterns
**Decision**: Normalized relational design with event sourcing for bets
**Rationale**:
- Complex relationships between sports, competitions, teams, users
- Event sourcing for bet history and audit trails
- Optimized views for ranking calculations
- SQLAlchemy ORM with Alembic migrations

### API Design Patterns
**Decision**: RESTful API with OAuth 2.0 Bearer tokens and OpenAPI 3.1 security schemes
**Rationale**:
- **REST with OAuth 2.0**: Bearer token authentication for all protected endpoints
- **OpenAPI 3.1 Security**: Comprehensive security scheme documentation
- **Scope-Based Authorization**: Different scopes for user actions vs admin operations
- **Token Validation Middleware**: Automatic JWT validation and user context injection
- **Rate Limiting**: Per-user rate limiting based on OAuth 2.0 subject claims
- **GraphQL Authorization**: Potential GraphQL endpoint with field-level authorization
- **Error Handling**: OAuth 2.0 compliant error responses (RFC 6749)
- **CORS Configuration**: Strict origin validation for SPA applications

## Observability and Monitoring (Core Learning Requirement)

### Grafana Stack Integration (Essential)
**Decision**: Complete Grafana observability stack for comprehensive learning experience
**Rationale**: 
- **Learning Objective**: Hands-on experience with all Grafana ecosystem components
- **Production Value**: Industry-standard observability solution
- **Comprehensive Coverage**: Metrics, logs, traces, and telemetry collection
- **Real-world Skills**: Direct experience with modern observability practices
- **Unified Experience**: Single stack for all observability needs

**Core Components (All Required)**:
- **Grafana 11.3.0**: Dashboards and visualization platform (learning focus: dashboard creation, alerting)
- **Mimir 2.14.1**: Prometheus-compatible metrics storage (learning focus: time-series data, PromQL)
- **Loki 3.2.0**: Log aggregation and querying (learning focus: log parsing, LogQL)
- **Tempo 2.6.1**: Distributed tracing backend (learning focus: trace analysis, service maps)
- **Alloy 1.4.2**: Telemetry collection and processing (learning focus: data collection, routing)
- **OpenTelemetry 1.31.0**: Instrumentation for traces, metrics, and logs (learning focus: auto-instrumentation, manual spans)

**Learning Implementation Strategy**:
- **Development Environment**: Full stack deployed for immediate learning
- **Instrumentation**: Both auto and manual OpenTelemetry implementation
- **Dashboard Creation**: Custom dashboards for application and business metrics
- **Alert Management**: Practical alerting rules and notification channels
- **Query Learning**: Hands-on PromQL and LogQL query development
- **Trace Analysis**: End-to-end request tracing and performance optimization

**Implementation**:
- OpenTelemetry instrumentation for FastAPI backend
- Browser instrumentation for Angular frontend
- Container metrics collection via cAdvisor 0.49.1
- Database metrics via PostgreSQL Exporter 0.15.0
- Keycloak metrics via built-in Prometheus endpoint
- Redis metrics via Redis Exporter 1.61.0
- Custom business metrics for betting operations
- Prometheus 2.54.1 for local development metrics collection

**Alternatives Considered**: 
- ELK Stack: More complex setup, higher resource usage
- New Relic/Datadog: Vendor lock-in, higher costs
- Prometheus + Jaeger: More components to manage

## CI/CD Pipeline and Automation

### GitHub Actions CI/CD Strategy
**Decision**: Comprehensive CI/CD pipeline using GitHub Actions with multi-environment deployment
**Rationale**: 
- Native GitHub integration with issue tracking and project management
- Free CI/CD minutes for open source and generous limits for private repos
- Built-in container registry (GitHub Container Registry)
- Advanced security features and dependency scanning
- Matrix builds for multiple environments and platforms

**Pipeline Architecture**:
- **Feature Branch CI**: Automated testing and container builds on every push
- **Pull Request CI**: Full integration testing with test environment deployment
- **Main Branch CD**: Automated production deployment with manual approval gates
- **Release Pipeline**: Versioned container images and GitHub releases
- **Security Pipeline**: Daily vulnerability scanning and dependency updates

### Container Registry and Image Management
**Decision**: GitHub Container Registry (GHCR) for container image storage
**Rationale**:
- Seamless integration with GitHub Actions
- Private registry with fine-grained access controls
- Multi-architecture image support
- Vulnerability scanning and security insights
- Cost-effective for GitHub-hosted projects

**Image Strategy**:
- **Development Images**: `ghcr.io/owner/betting-platform-backend:dev-{sha}`
- **Test Images**: `ghcr.io/owner/betting-platform-backend:test-{version}`
- **Production Images**: `ghcr.io/owner/betting-platform-backend:v{major.minor.patch}`
- **Multi-arch Support**: AMD64 and ARM64 for different deployment targets

### Quality Gates and Automation
**Decision**: Comprehensive quality gates with automated testing and security scanning
**Rationale**:
- Early detection of issues through automated testing
- Security-first approach with vulnerability scanning
- Code quality enforcement through automated checks
- Performance regression detection

**Quality Gates**:
- **Unit Tests**: Backend (pytest) and Frontend (Jest/Jasmine)
- **Integration Tests**: API contract testing and end-to-end scenarios
- **Security Scanning**: Container vulnerability scanning, dependency checks
- **Code Quality**: Linting, formatting, and complexity analysis
- **Performance Tests**: Load testing and response time validation
- **Compliance**: License compliance and security policy enforcement

### Environment-Specific Deployment
**Development Environment**:
- Trigger: Push to feature branches
- Actions: Run tests, build containers, deploy to dev environment
- Notifications: Slack/Teams integration for build status

**Test Environment**:
- Trigger: Pull request creation/update
- Actions: Full integration testing, security scanning, test deployment
- Approvals: Automatic deployment with rollback capabilities

**Production Environment**:
- Trigger: Merge to main branch or release tag
- Actions: Production build, security validation, manual approval gate
- Approvals: Required reviewer approval for production deployment
- Rollback: Automated rollback procedures for failed deployments

**Alternatives Considered**: 
- Jenkins: More complex setup, requires self-hosting
- GitLab CI: Vendor lock-in, migration complexity
- Azure DevOps: Less integrated with GitHub ecosystem
- AWS CodePipeline: Higher complexity and costs

## Deployment and Infrastructure

### Multi-Environment Docker Compose Strategy
**Decision**: Three-environment deployment architecture (dev/test/prod) using Docker Compose
**Rationale**: 
- Consistent deployment across all environments
- Environment-specific configurations without code changes
- Easy scaling and service orchestration
- Development-production parity
- Simplified CI/CD pipeline integration

**Environment Configurations**:
- **Development**: Hot reload, debug mode, local volumes, simplified auth
- **Test**: Production-like setup, automated testing, CI/CD integration
- **Production**: Optimized builds, security hardening, monitoring, backups

### Container Architecture (Development Focused)
**Decision**: Simple Docker Compose setup with scaling potential
**Rationale**:
- Focus on developer experience and rapid iteration
- Multi-stage builds for efficiency but not over-optimization
- Single-node deployment with Docker Compose
- Environment-specific configurations for dev/test/prod
- Future: Can migrate to Kubernetes when scaling is needed

### Environment Management (Pragmatic Approach)
**Decision**: Three environments with increasing complexity
**Rationale**:
- **Development**: Simple setup, hot reload, basic features
- **Test**: Production-like but simplified, automated testing
- **Production**: Stable and monitored but not over-engineered
- Environment variables for configuration differences
- Docker secrets for basic secret management
- Future: Can add advanced secret management when needed

### Backup and Recovery (Essential but Simple)
**Decision**: Basic backup strategy with automated daily backups
**Rationale**:
- Automated PostgreSQL backups using pg_dump
- Simple retention policy (7 days local, 30 days archive)
- Basic disaster recovery documentation
- Focus on data integrity over complex failover scenarios
- Future: Can add point-in-time recovery and replication when needed

### Containerization Strategy
**Decision**: Multi-stage Docker builds with Docker Compose orchestration
**Rationale**:
- Python 3.12-slim base images for optimized backend containers
- Node.js 20-alpine images for efficient frontend builds
- PostgreSQL 17.6-alpine containers for lightweight database deployment
- Keycloak 26.3.2 official containers with Quarkus-based performance improvements
- Multi-stage builds for optimized production images
- Environment-specific compose files for dev/test/prod
- Health checks and dependency management
- Latest container versions include security patches and performance improvements

### Environment Management
**Decision**: Configuration-driven deployment with environment files
**Rationale**:
- Environment variables for sensitive configuration
- Separate .env files for each deployment stage
- Docker secrets for production credentials
- Database migrations automated in deployment pipeline
- Container orchestration with proper networking and volumes

### Container Version Specifications
**Backend**: python:3.12-slim (latest stable Python runtime)
**Frontend Build**: node:20-alpine (for Angular CLI and build processes)  
**Frontend Serve**: nginx:alpine (for serving static files)
**Database**: postgres:17.6-alpine (latest stable PostgreSQL)
**IAM**: keycloak/keycloak:26.3.2 (latest stable Keycloak)
**Cache**: redis:7-alpine (for session storage and WebSocket scaling)

## Performance and Scaling Research

### Development-First Scaling Approach
**Decision**: Simple, scalable architecture without premature optimization
**Rationale**:
- Focus on functional requirements and clean architecture
- Use proven technologies that can scale when needed
- Avoid complex distributed systems until traffic demands it
- Design for horizontal scaling but implement vertical scaling first
- Keep infrastructure simple with Docker Compose for development

### Caching Strategy (Simple Start)
**Decision**: Single Redis instance with application-level caching
**Rationale**:
- Redis for session storage and basic ranking cache
- Simple TTL-based cache invalidation
- Application-level caching for frequently accessed data
- Future: Can add Redis clustering when traffic increases
- Future: Can add CDN when global distribution is needed

### Database Performance (Development Focus)
**Decision**: Single PostgreSQL instance with good indexing
**Rationale**:
- Focus on proper indexing and query optimization
- Use connection pooling within the application
- Materialized views for complex ranking calculations
- Future: Can add read replicas when read traffic increases
- Future: Can implement partitioning when dataset grows large

### Scalability Design Principles
**Decision**: Build for future scaling without current complexity
**Rationale**:
- Stateless backend services (easy to scale horizontally)
- Database-agnostic queries (easy to add read replicas)
- Environment-based configuration (easy to tune for scale)
- Modular service architecture (easy to split into microservices)
- Load balancer-ready (can add when needed)

### Performance Targets (Realistic for Development)
**Decision**: Reasonable performance goals for small-scale deployment
**Rationale**:
- API response time: <500ms (95th percentile) - realistic for development
- Concurrent users: 100-500 simultaneous users initially
- Database queries: <100ms for ranking calculations
- WebSocket latency: <200ms for real-time updates
- System availability: 99% uptime (not enterprise 99.9%)
- Focus on functionality over extreme performance initially

### Monitoring and Observability (Development Appropriate)
**Decision**: Essential monitoring without enterprise complexity
**Rationale**:
- Grafana stack for comprehensive observability (future-proof)
- Focus on application metrics and error tracking
- Basic performance monitoring and alerting
- Structured logging for debugging
- Future: Can add advanced APM when scaling up

## Security Research

### OAuth 2.0/OIDC Security Framework
**Decision**: Defense-in-depth with multiple security layers
**Rationale**:
- **Token Security**: JWT with RS256/ES256 asymmetric signing
- **PKCE Implementation**: SHA256 code challenge for authorization flows
- **Refresh Token Security**: Rotation with family detection and revocation
- **Scope Validation**: Fine-grained permissions with least privilege principle
- **CORS Protection**: Strict origin validation for cross-origin requests
- **CSRF Protection**: State parameter validation in OAuth flows
- **Session Security**: HttpOnly, Secure, SameSite cookie attributes
- **Token Binding**: Optional token binding for enhanced security

### Data Protection
**Decision**: Encryption at rest and in transit with OAuth 2.0 audit logging
**Rationale**:
- **TLS 1.3**: All API communications with perfect forward secrecy
- **Database Encryption**: AES-256 encryption for sensitive user data
- **Token Storage**: Secure storage with automatic expiration
- **Audit Trails**: OAuth 2.0 events, token usage, and admin actions
- **GDPR Compliance**: User consent management and data portability
- **Privacy by Design**: Minimal data collection and retention policies

### Anti-gaming Measures
**Decision**: Server-side validation with OAuth 2.0 user context
**Rationale**:
- **Authenticated Actions**: All betting actions require valid OAuth 2.0 tokens
- **User Context Validation**: Token subject claim validation for user identity
- **Deadline Enforcement**: Server-side validation with authenticated user context
- **Immutable Records**: Betting records with user identity from JWT claims
- **Race Condition Handling**: Optimistic locking with user session validation
- **Time Synchronization**: NTP synchronization with token timestamp validation

## Development Workflow Research

### Test-Driven Development (TDD) Methodology (Core Requirement)
**Decision**: Strict TDD approach with Red-Green-Refactor cycle
**Rationale**:
- **Quality Assurance**: Tests written first ensure comprehensive coverage
- **Design Improvement**: Writing tests first leads to better API design
- **Regression Prevention**: Comprehensive test suite prevents future bugs
- **Documentation**: Tests serve as living documentation of behavior
- **Confidence**: Safe refactoring and feature addition with test safety net
- **Learning Benefit**: TDD practices are industry-standard best practices

**TDD Workflow Implementation**:
- **Red Phase**: Write failing test for desired functionality
- **Green Phase**: Write minimal code to make test pass
- **Refactor Phase**: Improve code quality while keeping tests green
- **Contract-First**: API contracts drive both frontend and backend tests
- **No Implementation Without Tests**: Zero tolerance policy for untested code

### Testing Strategy
**Decision**: Multi-layer testing pyramid with TDD at each level
**Rationale**:
- **Unit Tests**: Fast feedback loop for individual components
- **Integration Tests**: Verify component interactions work correctly
- **Contract Tests**: Ensure API contracts are followed by both sides
- **End-to-End Tests**: Validate complete user workflows
- **Performance Tests**: Ensure system meets performance requirements

**Testing Tools and Frameworks**:
- **Backend TDD**: pytest with factory patterns for test data
- **Frontend TDD**: Jasmine/Karma with component testing
- **Contract Testing**: OpenAPI-driven tests with schema validation
- **Integration Testing**: Testcontainers for real database testing
- **E2E Testing**: Playwright for user journey validation
- **Load Testing**: Locust for performance validation

### CI/CD Pipeline
**Decision**: TDD-integrated continuous integration with quality gates
**Rationale**:
- **Test-First Culture**: No code can be merged without tests
- **Automated Quality**: CI pipeline enforces TDD workflow
- **Fast Feedback**: Immediate notification of test failures
- **Coverage Requirements**: Minimum coverage thresholds enforced
- **Performance Monitoring**: Automated performance regression detection

## GitHub Project Management Research

### Issue Tracking Strategy
**Decision**: GitHub Issues with custom templates and labels
**Rationale**:
- Feature, bug, and epic issue templates
- Labels for components (backend, frontend, devops)
- Milestone tracking for release planning
- Integration with GitHub Projects for kanban workflow

### Project Board Configuration
**Decision**: Automated GitHub Projects board with custom fields
**Rationale**:
- Automated issue movement based on PR status
- Custom fields for priority, component, effort estimation
- Epic tracking with issue linking
- Sprint planning with milestone integration