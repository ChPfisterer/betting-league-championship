# Data Model: Multi-Sport Betting Platform

## Entity Relationship Overview

The platform's data model supports multi-sport betting with complex group management, competition structures, and real-time ranking calculations. The design prioritizes data integrity, audit trails, and performance for concurrent betting scenarios.

## Core Entities

### User
**Purpose**: Platform participants with authentication and profile management
**Fields**:
- `id` (UUID, primary key)
- `email` (string, unique, required)
- `display_name` (string, required)
- `registration_date` (timestamp, required)
- `keycloak_id` (UUID, unique, required) - Link to Keycloak user
- `is_active` (boolean, default: true)
- `last_login` (timestamp, nullable)
- `created_at` (timestamp, required)
- `updated_at` (timestamp, required)

**Relationships**:
- One-to-many with Bet
- Many-to-many with Group (through GroupMembership)
- One-to-many with GroupMembership

**Validation Rules**:
- Email must be valid format and unique
- Display name minimum 2 characters, maximum 50
- Keycloak ID must reference valid Keycloak user

### Group
**Purpose**: Betting communities with configurable rules and member management
**Fields**:
- `id` (UUID, primary key)
- `name` (string, required, max 100 chars)
- `description` (text, nullable)
- `type` (enum: PRIVATE, PUBLIC, required)
- `invitation_code` (string, nullable, unique) - For private groups
- `member_limit` (integer, default: 50)
- `is_active` (boolean, default: true)
- `requires_approval` (boolean, default: false) - For public groups
- `custom_scoring_rules` (JSONB, nullable) - Configurable scoring
- `created_at` (timestamp, required)
- `updated_at` (timestamp, required)

**Relationships**:
- Many-to-many with User (through GroupMembership)
- One-to-many with GroupMembership
- One-to-many with Bet
- One-to-many with GroupCompetitionSettings

**Validation Rules**:
- Private groups must have invitation_code
- Public groups cannot have invitation_code
- Member limit minimum 2, maximum 1000 (with paid extensions)
- Invitation codes expire after 72 hours

### GroupMembership
**Purpose**: Junction table for user-group relationships with roles and status
**Fields**:
- `id` (UUID, primary key)
- `user_id` (UUID, foreign key to User, required)
- `group_id` (UUID, foreign key to Group, required)
- `role` (enum: MEMBER, ADMIN, OWNER, required)
- `status` (enum: ACTIVE, PENDING, REMOVED, required)
- `joined_at` (timestamp, required)
- `invitation_expires_at` (timestamp, nullable)
- `invited_by` (UUID, foreign key to User, nullable)

**Relationships**:
- Many-to-one with User
- Many-to-one with Group

**Validation Rules**:
- Unique constraint on (user_id, group_id)
- Only one OWNER per group
- Invitation expiry maximum 72 hours from creation

### Sport
**Purpose**: Supported sports with extensible configuration
**Fields**:
- `id` (UUID, primary key)
- `name` (string, required, unique)
- `display_name` (string, required)
- `is_active` (boolean, default: true)
- `rules_config` (JSONB, nullable) - Sport-specific rules
- `scoring_config` (JSONB, nullable) - Default scoring rules
- `created_at` (timestamp, required)

**Relationships**:
- One-to-many with Competition
- One-to-many with Team

**Validation Rules**:
- Name must be lowercase, alphanumeric + underscores
- Display name maximum 50 characters

### Competition
**Purpose**: Tournaments and leagues with format and administrative settings
**Fields**:
- `id` (UUID, primary key)
- `sport_id` (UUID, foreign key to Sport, required)
- `name` (string, required)
- `type` (enum: TOURNAMENT, LEAGUE, required)
- `format` (enum: KNOCKOUT, ROUND_ROBIN, MIXED, required)
- `is_active` (boolean, default: true)
- `start_date` (date, required)
- `end_date` (date, nullable)
- `config` (JSONB, nullable) - Competition-specific settings
- `created_at` (timestamp, required)
- `updated_at` (timestamp, required)

**Relationships**:
- Many-to-one with Sport
- One-to-many with Season
- One-to-many with GroupCompetitionSettings

**Validation Rules**:
- End date must be after start date
- Active competitions cannot have overlapping seasons for same sport

### Season
**Purpose**: Time-bounded competition periods with multiple rounds/matchdays
**Fields**:
- `id` (UUID, primary key)
- `competition_id` (UUID, foreign key to Competition, required)
- `name` (string, required)
- `year` (integer, required)
- `start_date` (date, required)
- `end_date` (date, required)
- `is_active` (boolean, default: true)
- `current_matchday` (integer, default: 1)
- `total_matchdays` (integer, required)
- `created_at` (timestamp, required)

**Relationships**:
- Many-to-one with Competition
- One-to-many with Match

**Validation Rules**:
- End date must be after start date
- Year must match start_date year
- Current matchday cannot exceed total matchdays

### Team
**Purpose**: Competing entities with sport-specific attributes
**Fields**:
- `id` (UUID, primary key)
- `sport_id` (UUID, foreign key to Sport, required)
- `name` (string, required)
- `short_name` (string, required, max 10 chars)
- `country_code` (string, nullable, 3 chars) - ISO country code
- `logo_url` (string, nullable)
- `is_active` (boolean, default: true)
- `attributes` (JSONB, nullable) - Sport-specific data
- `created_at` (timestamp, required)

**Relationships**:
- Many-to-one with Sport
- One-to-many with Player
- One-to-many with Match (as home_team)
- One-to-many with Match (as away_team)

**Validation Rules**:
- Name unique within sport
- Short name unique within sport
- Country code must be valid ISO 3166-1 alpha-3

### Player
**Purpose**: Individual athletes with team affiliations
**Fields**:
- `id` (UUID, primary key)
- `team_id` (UUID, foreign key to Team, required)
- `name` (string, required)
- `position` (string, nullable)
- `jersey_number` (integer, nullable)
- `is_active` (boolean, default: true)
- `attributes` (JSONB, nullable) - Sport-specific stats
- `created_at` (timestamp, required)

**Relationships**:
- Many-to-one with Team

**Validation Rules**:
- Jersey number unique within team
- Jersey number between 1 and 99

### Match
**Purpose**: Individual contests between teams with scheduling and results
**Fields**:
- `id` (UUID, primary key)
- `season_id` (UUID, foreign key to Season, required)
- `home_team_id` (UUID, foreign key to Team, required)
- `away_team_id` (UUID, foreign key to Team, required)
- `matchday` (integer, required)
- `scheduled_at` (timestamp, required)
- `betting_deadline` (timestamp, required)
- `status` (enum: SCHEDULED, LIVE, FINISHED, CANCELLED, required)
- `is_deadline_locked` (boolean, default: false)
- `home_score` (integer, nullable)
- `away_score` (integer, nullable)
- `created_at` (timestamp, required)
- `updated_at` (timestamp, required)

**Relationships**:
- Many-to-one with Season
- Many-to-one with Team (home_team)
- Many-to-one with Team (away_team)
- One-to-many with Bet
- One-to-one with Result

**Validation Rules**:
- Home team cannot equal away team
- Betting deadline must be before scheduled_at
- Scores only allowed when status is FINISHED
- Deadline becomes locked when match is "next" upcoming

### Bet
**Purpose**: User predictions with winner choice and exact score
**Fields**:
- `id` (UUID, primary key)
- `user_id` (UUID, foreign key to User, required)
- `match_id` (UUID, foreign key to Match, required)
- `group_id` (UUID, foreign key to Group, required)
- `predicted_winner` (enum: HOME, AWAY, DRAW, required)
- `predicted_home_score` (integer, required)
- `predicted_away_score` (integer, required)
- `points_earned` (integer, default: 0)
- `is_processed` (boolean, default: false)
- `placed_at` (timestamp, required)
- `created_at` (timestamp, required)

**Relationships**:
- Many-to-one with User
- Many-to-one with Match
- Many-to-one with Group

**Validation Rules**:
- Unique constraint on (user_id, match_id, group_id)
- Scores must be non-negative
- Cannot be placed after betting deadline
- Predicted winner must match score logic (draw = equal scores)

### Result
**Purpose**: Match outcomes with provisional and final states
**Fields**:
- `id` (UUID, primary key)
- `match_id` (UUID, foreign key to Match, required)
- `home_score` (integer, required)
- `away_score` (integer, required)
- `winner` (enum: HOME, AWAY, DRAW, required)
- `is_provisional` (boolean, default: true)
- `finalized_at` (timestamp, nullable)
- `entered_by` (UUID, foreign key to User, required)
- `created_at` (timestamp, required)
- `updated_at` (timestamp, required)

**Relationships**:
- One-to-one with Match
- Many-to-one with User (entered_by)

**Validation Rules**:
- Scores must be non-negative
- Winner must match score logic
- Final results cannot be modified
- Provisional results must be finalized within 48 hours

### GroupCompetitionSettings
**Purpose**: Group-specific settings for competitions (deadlines, scoring)
**Fields**:
- `id` (UUID, primary key)
- `group_id` (UUID, foreign key to Group, required)
- `competition_id` (UUID, foreign key to Competition, required)
- `custom_deadline_offset` (interval, nullable) - Override default 1 hour
- `custom_scoring_rules` (JSONB, nullable) - Override group scoring
- `is_active` (boolean, default: true)
- `created_at` (timestamp, required)

**Relationships**:
- Many-to-one with Group
- Many-to-one with Competition

**Validation Rules**:
- Unique constraint on (group_id, competition_id)
- Deadline offset minimum 5 minutes, maximum 24 hours

## Audit and Security

### AuditLog
**Purpose**: Comprehensive audit trail for admin actions
**Fields**:
- `id` (UUID, primary key)
- `user_id` (UUID, foreign key to User, required)
- `action` (string, required)
- `resource_type` (string, required)
- `resource_id` (UUID, required)
- `old_values` (JSONB, nullable)
- `new_values` (JSONB, nullable)
- `ip_address` (inet, nullable)
- `user_agent` (string, nullable)
- `created_at` (timestamp, required)

**Validation Rules**:
- All admin actions must be logged
- Immutable records (no updates/deletes)
- Retention policy of 7 years for compliance

## Indexing Strategy

### Performance Indexes
- `User.email` (unique)
- `User.keycloak_id` (unique)
- `Group.invitation_code` (unique, sparse)
- `Match.betting_deadline` (for deadline queries)
- `Match.scheduled_at` (for match scheduling)
- `Bet.user_id, match_id, group_id` (unique composite)
- `GroupMembership.user_id, group_id` (unique composite)

### Ranking Calculation Indexes
- `Bet.group_id, points_earned` (for leaderboards)
- `Bet.user_id, group_id` (for user statistics)
- `Match.season_id, matchday` (for competition progress)

## Database Constraints

### Referential Integrity
- All foreign keys enforce ON DELETE RESTRICT
- Cascade deletes only for dependent entities (GroupMembership, Bet)
- Audit logs maintain references to deleted entities via UUID

### Business Logic Constraints
- Check constraints for score non-negativity
- Check constraints for date ordering
- Trigger-based validation for betting deadlines
- Row-level security for multi-tenant data isolation

## Migration Strategy

### Alembic Migrations
- Version-controlled schema changes
- Environment-specific migration scripts
- Rollback procedures for each migration
- Data migration scripts for schema changes

### Seeding Data
- Initial sports and competition data
- Test user and group data for development
- Reference data for countries and time zones
- Sample betting scenarios for testing