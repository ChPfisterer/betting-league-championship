# 🗄️ Comprehensive Database Field Analysis
## Betting League Championship Platform

This document provides a complete mapping of all field names across database tables, data models, API schemas, and seed data implementations.

---

## 📊 Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Entities** | 12 |
| **Total Database Tables** | 12 |
| **Total Model Fields** | 295 |
| **Total API Schema Fields** | 502 |
| **Seed Data Field References** | 22 |

---

## 🗂️ Detailed Field Mapping by Entity

### 👤 **User Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `users` | `id`, `username`, `email`, `password_hash`, `first_name`, `last_name`, `display_name`, `date_of_birth`, `phone_number`, `status`, `role`, `is_active`, `is_verified`, `email_verified`, `phone_verified`, `kyc_status`, `last_login`, `failed_login_attempts`, `locked_until`, `created_at`, `updated_at` |
| **Model Fields (36)** | User | All database fields + validation methods + relationships |
| **API Schema Fields (11)** | UserSchema | `id`, `username`, `first_name`, `last_name`, `password`, `current_password`, `total_bets`, `total_winnings`, `win_rate`, `last_login_at`, `expires_in` |
| **Seed Data Fields** | WorldCupSeeder | `username`, `email`, `first_name`, `last_name`, `role`, `status` |

### ⚽ **Sport Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `sports` | `id`, `name`, `slug`, `category`, `is_active`, `description`, `rules`, `icon_url`, `color_scheme`, `default_bet_types`, `scoring_system`, `match_duration`, `season_structure`, `popularity_score`, `created_at`, `updated_at` |
| **Model Fields (16)** | Sport | All database fields + relationships + validation |
| **API Schema Fields (9)** | SportSchema | `id`, `name`, `description`, `rules`, `is_active`, `total_teams`, `total_matches`, `total_competitions`, `active_competitions` |
| **Seed Data Fields** | WorldCupSeeder | `name`, `slug`, `description`, `category`, `rules`, `popularity_score`, `is_active` |

### 🏈 **Team Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `teams` | `id`, `name`, `slug`, `short_name`, `sport_id`, `is_active`, `description`, `logo_url`, `banner_url`, `primary_color`, `secondary_color`, `founded_year`, `home_venue`, `country`, `city`, `website`, `social_links`, `coach_name`, `captain_id`, `max_players`, `current_league`, `league_position`, `created_at`, `updated_at` |
| **Model Fields (24)** | Team | All database fields + player relationships + validation |
| **API Schema Fields (16)** | TeamSchema | `id`, `name`, `short_name`, `sport_id`, `sport_name`, `country`, `city`, `founded_year`, `logo_url`, `website_url`, `is_active`, `total_matches`, `wins`, `losses`, `draws`, `win_percentage` |
| **Seed Data Fields** | WorldCupSeeder | `name`, `short_name`, `country`, `logo_url` |

### 🏃‍♂️ **Player Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `players` | `id`, `first_name`, `middle_name`, `last_name`, `display_name`, `nickname`, `sport_id`, `position`, `jersey_number`, `date_of_birth`, `nationality`, `height_cm`, `weight_kg`, `preferred_foot`, `market_value`, `salary`, `current_team_id`, `agent_name`, `contract_start`, `contract_end`, `is_active`, `injury_status`, `retirement_date`, `biography`, `social_media`, `profile_image_url`, `created_at`, `updated_at` |
| **Model Fields (29)** | Player | All database fields + team relationships + statistics |
| **API Schema Fields (60)** | PlayerSchema | Comprehensive player stats including `assists`, `biography`, `contract_history`, `detailed_stats`, `market_value`, `performance_rating`, `transfer_history`, etc. |
| **Seed Data Fields** | WorldCupSeeder | `name`, `first_name`, `last_name`, `position`, `jersey_number`, `nationality`, `market_value`, `salary` |

### 🏆 **Competition Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `competitions` | `id`, `name`, `slug`, `description`, `sport_id`, `season_id`, `format_type`, `status`, `start_date`, `end_date`, `registration_deadline`, `betting_closes_at`, `logo_url`, `banner_url`, `max_participants`, `min_participants`, `entry_fee`, `prize_pool`, `prize_distribution`, `visibility`, `allow_public_betting`, `rules`, `point_system`, `group_id`, `created_by`, `created_at`, `updated_at` |
| **Model Fields (27)** | Competition | All database fields + season/sport relationships + match management |
| **API Schema Fields (36)** | CompetitionSchema | Includes `allow_betting`, `completed_matches`, `days_remaining`, `is_public`, `max_teams`, `min_teams`, `prize_pool`, `tournament_bracket`, etc. |
| **Seed Data Fields** | WorldCupSeeder | `name`, `description`, `format_type`, `start_date`, `end_date` |

### 📅 **Season Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `seasons` | `id`, `name`, `slug`, `description`, `sport_id`, `year`, `start_date`, `end_date`, `registration_start`, `registration_end`, `status`, `is_current`, `max_competitions`, `prize_pool_total`, `rules`, `season_format`, `playoff_format`, `promotion_rules`, `relegation_rules`, `point_system`, `tie_breaker_rules`, `created_at`, `updated_at` |
| **Model Fields (23)** | Season | All database fields + competition relationships + season management |
| **API Schema Fields (40)** | SeasonSchema | Includes `allow_betting`, `completed_matches`, `average_goals_per_match`, `standings`, `top_scorers`, etc. |
| **Seed Data Fields** | WorldCupSeeder | `name`, `slug`, `year`, `start_date`, `end_date`, `status` |

### ⚽ **Match Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `matches` | `id`, `competition_id`, `home_team_id`, `away_team_id`, `scheduled_at`, `started_at`, `finished_at`, `betting_closes_at`, `round_number`, `match_day`, `venue`, `referee`, `status`, `home_score`, `away_score`, `extra_time_home_score`, `extra_time_away_score`, `penalties_home_score`, `penalties_away_score`, `match_events`, `weather_conditions`, `attendance`, `live_odds`, `notes`, `created_at`, `updated_at` |
| **Model Fields (26)** | Match | All database fields + team relationships + betting integration |
| **API Schema Fields (59)** | MatchSchema | Extensive match data including `allow_betting`, `away_team_bets`, `draw_odds`, `live_commentary`, `match_statistics`, `predictions`, etc. |
| **Seed Data Fields** | WorldCupSeeder | `home_team_id`, `away_team_id`, `scheduled_at`, `status`, `home_score`, `away_score`, `venue`, `referee` |

### 🎯 **Bet Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `bets` | `id`, `user_id`, `match_id`, `bet_type`, `market_type`, `stake_amount`, `odds`, `potential_payout`, `payout_amount`, `commission`, `selection`, `handicap`, `status`, `void_reason`, `risk_category`, `max_liability`, `bonus_applied`, `promotion_id`, `notes`, `ip_address`, `device_info`, `placed_at`, `settled_at`, `created_at`, `updated_at` |
| **Model Fields (25)** | Bet | All database fields + user/match relationships + payout calculations |
| **API Schema Fields (69)** | BetSchema | Comprehensive betting data including `active_bettors`, `average_odds`, `bet_type_stats`, `live_odds`, `market_analysis`, etc. |
| **Seed Data Fields** | WorldCupSeeder | Currently not implemented in seed data |

### 📊 **Result Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `results` | `id`, `match_id`, `home_score`, `away_score`, `half_time_home_score`, `half_time_away_score`, `extra_time_home_score`, `extra_time_away_score`, `penalty_home_score`, `penalty_away_score`, `winner_team_id`, `status`, `is_official`, `verified_by`, `verified_at`, `possession_home`, `possession_away`, `shots_home`, `shots_away`, `corners_home`, `corners_away`, `yellow_cards_home`, `yellow_cards_away`, `red_cards_home`, `red_cards_away`, `match_events`, `statistics`, `notes`, `started_at`, `finished_at`, `created_at`, `updated_at` |
| **Model Fields (32)** | Result | All database fields + match relationships + detailed statistics |
| **API Schema Fields (63)** | ResultSchema | Detailed result analytics including `average_goals_per_match`, `both_teams_scored`, `clean_sheets`, `performance_metrics`, etc. |
| **Seed Data Fields** | WorldCupSeeder | `home_score`, `away_score` (embedded in match data) |

### 👥 **Group Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `groups` | `id`, `name`, `description`, `creator_id`, `is_private`, `max_members`, `allow_member_invites`, `auto_approve_members`, `point_system`, `avatar_url`, `banner_url`, `rules_text`, `join_code`, `entry_fee`, `prize_pool`, `created_at`, `updated_at` |
| **Model Fields (17)** | Group | All database fields + creator relationships + member management |
| **API Schema Fields (17)** | GroupSchema | Group management fields including `active_bets`, `member_count`, `leaderboard`, etc. |
| **Seed Data Fields** | WorldCupSeeder | `name`, `description`, `creator`, `is_private` |

### 🤝 **GroupMembership Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `group_memberships` | `id`, `group_id`, `user_id`, `role`, `status`, `invited_by_id`, `invitation_sent_at`, `joined_at`, `left_at`, `banned_at`, `banned_by_id`, `ban_reason`, `notes`, `created_at`, `updated_at` |
| **Model Fields (15)** | GroupMembership | All database fields + user/group relationships + membership lifecycle |
| **API Schema Fields (49)** | GroupMembershipSchema | Membership management including `approval_workflow`, `invitation_management`, `role_permissions`, etc. |
| **Seed Data Fields** | WorldCupSeeder | `role`, `status` (created automatically for group creators) |

### 📝 **AuditLog Entity**
| Component | Table Name | Key Fields |
|-----------|------------|------------|
| **Database Table** | `audit_logs` | `id`, `action_type`, `entity_type`, `entity_id`, `user_id`, `log_level`, `message`, `timestamp`, `session_id`, `request_id`, `correlation_id`, `ip_address`, `user_agent`, `device_info`, `location`, `changes`, `previous_values`, `new_values`, `risk_score`, `flagged`, `reviewed_by`, `reviewed_at`, `notes`, `additional_data`, `created_at` |
| **Model Fields (25)** | AuditLog | All database fields + user relationships + security tracking |
| **API Schema Fields (73)** | AuditLogSchema | Comprehensive audit features including `anomaly_detection`, `compliance_metrics`, `security_analysis`, etc. |
| **Seed Data Fields** | WorldCupSeeder | Currently not implemented in seed data |

---

## 🎯 Key Observations

### **Field Coverage Analysis:**
1. **Database Models**: Comprehensive with 295 total fields across 12 entities
2. **API Schemas**: Extended with 502 fields including computed properties and aggregations  
3. **Seed Data**: Focused on essential fields (22 total) for realistic FIFA World Cup 2022 data

### **Entity Complexity Ranking:**
1. **Most Complex**: AuditLog (73 API fields), Bet (69 API fields), Result (63 API fields)
2. **Medium Complex**: Player (60 API fields), Match (59 API fields), GroupMembership (49 API fields)
3. **Least Complex**: Sport (9 API fields), Team (16 API fields), Group (17 API fields)

### **Seed Data Implementation:**
- ✅ **Fully Implemented**: User, Sport, Team, Player, Competition, Season, Match, Group
- ⚠️ **Partially Implemented**: GroupMembership (auto-created for group creators)
- ❌ **Not Implemented**: Bet, Result (as separate entities), AuditLog

### **API Schema Extensions:**
- Heavy focus on **analytics and statistics** (betting odds, performance metrics)
- **Relationship data** (nested team/user information) 
- **Computed fields** (win percentages, averages, totals)
- **Business logic fields** (betting controls, approval workflows)

---

## 📈 Implementation Status

| Entity | Database ✅ | Model ✅ | API Schema ✅ | Seed Data |
|--------|-------------|----------|---------------|-----------|
| User | ✅ | ✅ | ✅ | ✅ |
| Sport | ✅ | ✅ | ✅ | ✅ |
| Team | ✅ | ✅ | ✅ | ✅ |
| Player | ✅ | ✅ | ✅ | ✅ |
| Competition | ✅ | ✅ | ✅ | ✅ |
| Season | ✅ | ✅ | ✅ | ✅ |
| Match | ✅ | ✅ | ✅ | ✅ |
| Group | ✅ | ✅ | ✅ | ✅ |
| GroupMembership | ✅ | ✅ | ✅ | ⚠️ |
| Bet | ✅ | ✅ | ✅ | ❌ |
| Result | ✅ | ✅ | ✅ | ❌ |
| AuditLog | ✅ | ✅ | ✅ | ❌ |

**Legend:** ✅ Complete | ⚠️ Partial | ❌ Not Implemented

---

## 🔍 Field-by-Field Naming Consistency Analysis

For detailed field-by-field consistency analysis showing exactly how each field name maps across Database Models, API Schemas, and Seed Data, see the comprehensive analysis in:

**[📋 ENHANCED_FIELD_CONSISTENCY.md](./ENHANCED_FIELD_CONSISTENCY.md)**

### Key Consistency Findings:

| Entity | Total Fields | Consistent Fields | Consistency Rate |
|--------|--------------|-------------------|------------------|
| **Team** | 38 | 11 | 28.9% |
| **Player** | 74 | 20 | 27.0% |
| **Sport** | 26 | 7 | 26.9% |
| **Competition** | 55 | 13 | 23.6% |
| **Season** | 54 | 12 | 22.2% |
| **User** | 54 | 8 | 14.8% |
| **Match** | 71 | 17 | 23.9% |
| **Bet** | 88 | 12 | 13.6% |
| **Result** | 94 | 8 | 8.5% |
| **Group** | 82 | 17 | 20.7% |
| **GroupMembership** | 64 | 9 | 14.1% |
| **AuditLog** | 94 | 11 | 11.7% |

### Consistency Status Legend:
- **🟢 Full Stack**: Field exists in Database, API Schema, and Seed Data  
- **🟡 DB + API**: Field exists in Database and API Schema (most common for production fields)
- **🔵 DB Only**: Field exists only in Database Model  
- **🟠 API Only**: Field exists only in API Schema (computed/derived fields)
- **🔴 Seed Only**: Field exists only in Seed Data

### Key Observations:
1. **Most fields follow Database + API pattern** - Core business logic fields are properly mapped
2. **API-only fields** are typically computed properties, validation messages, or aggregated data
3. **Database-only fields** are often internal system fields not exposed via API
4. **Seed data coverage** focuses on essential fields needed for realistic testing data
5. **Higher consistency rates** in core entities (Team, Player, Sport) indicate mature data modeling

---

*Generated on: 5 October 2025*  
*Total Fields Analyzed: 817*  
*Database Tables: 12*  
*API Endpoints: 186*  
*Field Consistency Analysis: Complete*