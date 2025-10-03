# Complete Specification Recreation Prompt

## For /specify command:

```
Multi-Sport Betting Platform - Create a comprehensive responsive web application supporting multiple sports (soccer, handball, extensible to others) and competition types: international championships (World Cup, European Championships), domestic leagues (Bundesliga, Premier League, La Liga), and tournament formats (knockout vs round-robin). 

Core Features: Users register with email/password/display name, authenticate via Keycloak IAM with OAuth 2.0/OpenID Connect plus social login (Google, Facebook, Apple). Group management includes private groups (invitation codes) and public groups (admin approval required) with advanced admin capabilities: invite/remove users, edit settings, delegate admin rights, set custom betting deadlines per competition, customize scoring rules. Member limits with paid extension opportunities for monetization. 

Betting System: Users predict both winner and exact final score earning 1 point for correct winner, 3 points total (1+2 bonus) for exact score. NO default bets - users must actively place bets to participate. Configurable betting deadlines (default 1 hour before match, admin customizable) with refined policy: deadline changes prohibited for next upcoming match or simultaneous matches, only modifiable for future matches, becoming permanently fixed once match becomes next. 

Match Management: Manual result entry initially with architecture supporting future sports API integration. Provisional results system for immediate engagement with final results within 24-48 hours including user notifications for changes. Live ranking updates during matches. Match rescheduling notifications for all participants with updated deadlines. 

Data Architecture: Store teams, players, lineups, competitions (tournaments vs leagues), seasons, and comprehensive betting data. Support season-based competitions with multiple matchdays/rounds. Database design for User, Group, Game, Bet, Result, Competition, Season, Team, Player, Sport entities. 

Edge Cases Resolved: 1) Betting after deadline shows disabled UI with clear messaging, 2) Delayed results use provisional+final system with notifications, 3) Group access issues handled with member limits and 72-hour invitation expiry showing Group not found for inaccessible groups, 4) Ranking ties resolved by sequence: total points → exact score predictions → correct winner predictions → registration date, 5) Deadline changes use refined anti-gaming policy. 

Quality Systems: Fair tiebreaker sequences prioritizing skill, transparent audit trails for admin actions, group invitation security (72-hour expiry), concurrent betting conflict handling, permanent data persistence, secure session management, responsive mobile-first design. 

Technical Foundation: Multi-competition architecture supporting both knockout tournaments and round-robin leagues, real-time provisional rankings for engagement, API-ready for sports data integration, scalable design for new sports/competitions, comprehensive error handling and edge case management. 

Business Features: Group member limits with paid extensions, live engagement through provisional rankings, transparent fair play systems, no gaming opportunities, comprehensive admin controls, audit trails for accountability, monetization through premium group features.
```

## For /plan command:

```
Create a comprehensive implementation plan for the multi-sport betting platform with the following specific requirements:

**Technology Stack (Latest Stable Versions):**
- Backend: FastAPI 0.115.x (Python 3.12+)
- Frontend: Angular 20.x with TypeScript
- Database: PostgreSQL 17.x
- Authentication: Keycloak 26.x with OAuth 2.0/OIDC
- Containerization: Docker 27.x with multi-environment setup

**Observability Stack (Learning Requirement):**
- Complete Grafana Stack: Grafana 11.3+, Mimir 2.14+, Loki 3.2+, Tempo 2.6+, Alloy 1.4+
- OpenTelemetry 1.31+ for instrumentation
- Purpose: Hands-on learning with industry-standard observability tools
- Include learning objectives for each component (dashboard creation, PromQL/LogQL, tracing, telemetry collection)

**Development Methodology (Core Requirement):**
- Strict Test-Driven Development (TDD) approach
- Red-Green-Refactor cycle for all code development
- Test coverage requirements: 80% backend, 70% frontend
- Testing pyramid: Unit → Integration → E2E tests
- Contract-first development with OpenAPI specifications

**GitHub Project Management:**
- Create GitHub project with Issues tracking
- Branch strategy: new branch for each task/feature
- Pull Requests with issue linking
- CI/CD pipeline with GitHub Actions for container builds

**Deployment Strategy:**
- Three environments: development, staging, production
- Docker Compose configurations for each environment
- Environment-specific configuration files
- Automated container building and deployment

**Development Philosophy:**
- Development-first approach: functional and well-architected but not over-engineered
- Focus on learning objectives (Grafana stack, TDD, OpenTelemetry)
- Scalable design with simple initial implementation
- Quality through testing rather than enterprise complexity

**Task Breakdown Requirements:**
- 90-105 numbered tasks across 19+ categories
- TDD ordering: Contract → Test → Implementation workflow
- All tests must be written before implementation code
- Include Grafana stack setup and learning milestones
- GitHub project management tasks included
- CI/CD pipeline implementation tasks

**Specific Focus Areas:**
1. Complete Grafana observability stack integration for learning
2. Strict TDD methodology with comprehensive test coverage
3. OAuth 2.0/OIDC security with Keycloak
4. Real-time features with WebSocket support
5. Multi-sport and multi-competition architecture
6. Responsive mobile-first design
7. GitHub project management and CI/CD automation

Generate a comprehensive plan that balances learning objectives with practical development, emphasizing the Grafana stack and TDD methodology as core educational requirements.
```

## Key Context for Recreation:

1. **Learning Focus**: This is primarily an educational project focused on:
   - Complete Grafana observability stack (all 5 components)
   - Test-Driven Development methodology
   - Modern web application architecture
   - OAuth 2.0/OIDC security implementation

2. **Development Approach**: 
   - Not enterprise-scale but enterprise-ready
   - Focus on functionality and learning over complexity
   - Strict TDD methodology as non-negotiable requirement
   - Quality through testing rather than over-engineering

3. **Technology Emphasis**:
   - Latest stable versions of all components
   - Complete observability stack for hands-on experience
   - Modern containerized deployment
   - GitHub-based project management and CI/CD

4. **Expected Outcome**:
   - Complete specification with 51+ functional requirements
   - Comprehensive implementation plan with 90-105 TDD-ordered tasks
   - Learning guides for Grafana stack and TDD methodology
   - Ready-to-execute development roadmap

This prompt should recreate the entire specification and planning process that led to our current comprehensive documentation suite.