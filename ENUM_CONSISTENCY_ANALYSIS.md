# 🔢 Enum Consistency Analysis
## Betting League Championship Platform

This document analyzes enum value consistency across Database Models, API Schemas, and Seed Data.

## 📊 Enum Consistency Summary

| Metric | Value |
|--------|-------|
| **Total Enums Found** | 11 |
| **Consistent Enums** | 0 |
| **Consistency Rate** | 0.0% |
| **Total Inconsistencies** | 11 |

## 🏷️ User Enum Analysis

### Database Model Enums
- **UserStatus** (enum_class)
  - Values: Account locked until this timestamp, AuditLog.user_id, Current account status, GBP, Hashed password for authentication, IP address of last login, Know Your Customer verification status, Last successful login timestamp, Number of consecutive failed login attempts, URL to user, UTC, Unique user identifier, Unique username for login, User, User email address, User role and permissions level, When KYC verification was completed, When password was last changed, When terms were accepted, When the user account was created, When the user account was deleted (soft delete), When the user account was last updated, Whether email address has been verified, Whether phone number has been verified, Whether to send notifications to user, Whether user account is active, Whether user account is verified, Whether user consents to marketing communications, Whether user has accepted privacy policy, Whether user has accepted terms of service, active, admin, all, delete-orphan, banned, ck_users_date_of_birth_past, ck_users_failed_login_attempts, ck_users_first_name_length, ck_users_kyc_status, ck_users_last_name_length, ck_users_role, ck_users_status, ck_users_username_length, deactivated, dynamic, en, in_progress, moderator, not_started, pending, pending_review, rejected, super_admin, suspended, user, users, verified, {self.email}, {self.username}
  - Used by fields: 

### API Schema Enums
- **rStatus** (imported_enum)
  - Used by fields: status

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum UserStatus not found in schema

### 💡 Recommendations
- Add UserStatus to schema for fields: 

---

## 🏷️ Bet Enum Analysis

### Database Model Enums
- **BetType** (enum_class)
  - Values: Actual payout amount, Additional notes about the bet, Amount staked on the bet, Commission charged on the bet, Current status of the bet, Device information when bet was placed, Handicap value for handicap bets, ID of the match being bet on, ID of the promotion if bonus applied, ID of the user who placed the bet, IP address from which bet was placed, Market type (match_winner, over_under, etc.), Maximum liability for this bet, Odds at which the bet was placed, Potential payout if bet wins, Reason for voiding the bet if applicable, Risk category assessment, Specific selection (home, away, over, under, etc.), Type of bet (single, multiple, etc.), Unique identifier for the bet, When the bet record was created, When the bet record was last updated, When the bet was placed, When the bet was settled, Whether a bonus was applied to this bet, accumulator, bets, both_teams_score, cancelled, ck_bets_bet_type, ck_bets_commission_non_negative, ck_bets_market_type, ck_bets_odds_minimum, ck_bets_payout_amount_non_negative, ck_bets_potential_payout_minimum, ck_bets_risk_category, ck_bets_settled_after_placed, ck_bets_stake_amount_positive, ck_bets_status, correct_score, double_chance, each_way, first_goalscorer, fk_bets_match_id, fk_bets_user_id, handicap, high, lost, low, match_winner, matched, multiple, normal, over_under, partially_matched, pending, settled, single, system, total_goals, very_high, void, won, {self.status}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum BetType not found in schema

### 💡 Recommendations
- Add BetType to schema for fields: 

---

## 🏷️ Competition Enum Analysis

### Database Model Enums
- **CompetitionFormat** (enum_class)
  - Values: Competition end date, Competition format (league, tournament, etc.), Competition name, Competition rules and regulations, Competition start date, Current competition status, Deadline for team/participant registration, Detailed competition description, Entry fee to participate, ID of the organizing group (optional), ID of the season this competition belongs to, ID of the sport for this competition, ID of the user who created the competition, Maximum number of participants allowed, Minimum number of participants required, Point scoring system configuration, Prize distribution configuration, Total prize pool for winners, URL to competition banner image, URL to competition logo, URL-friendly competition identifier, Unique identifier for the competition, When betting closes for this competition, When the competition was created, When the competition was last updated, Whether public betting is allowed, Who can view this competition, active, cancelled, ck_competitions_date_order, ck_competitions_entry_fee, ck_competitions_format_type, ck_competitions_max_participants, ck_competitions_min_participants, ck_competitions_name_length, ck_competitions_prize_pool, ck_competitions_slug_length, ck_competitions_status, ck_competitions_visibility, competitions, completed, draft, elimination, fk_competitions_created_by, fk_competitions_group_id, fk_competitions_season_id, fk_competitions_sport_id, group_only, knockout, ladder, league, paused, private, public, registration_closed, registration_open, round_robin, swiss_system, tournament, upcoming, {self.name}, {self.status}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum CompetitionFormat not found in schema

### 💡 Recommendations
- Add CompetitionFormat to schema for fields: 

---

## 🏷️ Result Enum Analysis

### Database Model Enums
- **ResultStatus** (enum_class)
  - Values: Additional match statistics, Additional notes about the result, Away team corner kicks, Away team final score, Away team penalty shootout score, Away team possession percentage, Away team red cards, Away team score at half time, Away team score in extra time, Away team total shots, Away team yellow cards, Current status of the match result, Home team corner kicks, Home team final score, Home team penalty shootout score, Home team possession percentage, Home team red cards, Home team score at half time, Home team score in extra time, Home team total shots, Home team yellow cards, ID of the match this result belongs to, ID of the winning team (null for draw), Official who verified the result, Timeline of match events, Unique identifier for the result, When the match finished, When the match started, When the result record was created, When the result record was last updated, When the result was officially verified, Whether the result is official, abandoned, cancelled, ck_results_away_score_non_negative, ck_results_corners_away_non_negative, ck_results_corners_home_non_negative, ck_results_extra_time_away_score_non_negative, ck_results_extra_time_home_score_non_negative, ck_results_finished_after_started, ck_results_half_time_away_score_non_negative, ck_results_half_time_home_score_non_negative, ck_results_home_score_non_negative, ck_results_penalty_away_score_non_negative, ck_results_penalty_home_score_non_negative, ck_results_possession_away_percentage, ck_results_possession_home_percentage, ck_results_red_cards_away_non_negative, ck_results_red_cards_home_non_negative, ck_results_shots_away_non_negative, ck_results_shots_home_non_negative, ck_results_status, ck_results_verified_after_started, ck_results_yellow_cards_away_non_negative, ck_results_yellow_cards_home_non_negative, corner, extra_time, final, fk_results_match_id, fk_results_winner_team_id, free_kick, full_time, goal, half_time, kickoff, live, offside, own_goal, penalties, penalty, postponed, red_card, results, scheduled, second_half, substitution, yellow_card, {self.status}
  - Used by fields: 

### API Schema Enums
- **tStatus** (imported_enum)
  - Used by fields: status

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum ResultStatus not found in schema

### 💡 Recommendations
- Add ResultStatus to schema for fields: 

---

## 🏷️ Sport Enum Analysis

### Database Model Enums
- **SportCategory** (enum_class)
  - Values: Color scheme for UI representation, Default betting types available for this sport, Detailed description of the sport, Popularity score for ranking sports, Scoring system configuration, Season structure and schedule information, Sport category classification, Sport name (e.g., , Sport rules and regulations, Typical match duration in minutes, URL to sport icon/logo, URL-friendly sport identifier, Unique identifier for the sport, When the sport was created, When the sport was last updated, Whether sport is active for betting, ck_sports_category, ck_sports_match_duration, ck_sports_name_length, ck_sports_popularity_score, ck_sports_slug_length, combat_sport, esport, individual_sport, racing, sports, team_sport, water_sport, winter_sport, {self.category}, {self.name}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum SportCategory not found in schema

### 💡 Recommendations
- Add SportCategory to schema for fields: 

---

## 🏷️ Player Enum Analysis

### Database Model Enums
- **InjuryStatus** (enum_class)
  - Values: Agent contact information, Contract end date, Contract start date, Date when player retired (if applicable), ID of the player, ID of the sport the player participates in, Player, Preferred display name for the player, Social media profiles and handles, URL to player, Unique identifier for the player, When the player record was created, When the player record was last updated, Whether the player is currently active, both, ck_players_birth_date, ck_players_contract_dates, ck_players_first_name_length, ck_players_height, ck_players_injury_status, ck_players_jersey_number, ck_players_last_name_length, ck_players_market_value, ck_players_preferred_foot, ck_players_retirement_date, ck_players_salary, ck_players_weight, doubtful, fit, fk_players_current_team_id, fk_players_sport_id, injured, left, players, recovering, right, suspended, {self.full_name}, {self.position}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum InjuryStatus not found in schema

### 💡 Recommendations
- Add InjuryStatus to schema for fields: 

---

## 🏷️ Group Enum Analysis

### Database Model Enums
- **PointSystem** (enum_class)
  - Values: Custom rules and guidelines for the group, Entry fee required to join group, Group description and purpose, Group name, ID of the user who created the group, Maximum number of members allowed, Point system used for scoring, Total prize pool for group competitions, URL to group avatar image, URL to group banner image, Unique code for joining private groups, Unique identifier for the group, When the group was created, When the group was last updated, Whether group is private (invite only), Whether members can invite others, Whether to auto-approve new members, ck_groups_description_length, ck_groups_entry_fee, ck_groups_max_members, ck_groups_name_length, ck_groups_point_system, ck_groups_prize_pool, confidence, custom, fk_groups_creator_id, groups, spread, standard, {self.name}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum PointSystem not found in schema

### 💡 Recommendations
- Add PointSystem to schema for fields: 

---

## 🏷️ Season Enum Analysis

### Database Model Enums
- **SeasonStatus** (enum_class)
  - Values: Current season status, Detailed season description, ID of the sport for this season, Maximum number of competitions allowed, Playoff format if applicable, Point scoring system for the season, Primary year for the season, Rules for breaking ties in standings, Rules for promotion to higher divisions, Rules for relegation to lower divisions, Season end date, Season format (e.g., , Season name (e.g., , Season start date, Season-specific rules and regulations, Total prize pool for the season, URL-friendly season identifier, Unique identifier for the season, When team/participant registration closes, When team/participant registration opens, When the season was created, When the season was last updated, Whether this is the current active season for the sport, active, cancelled, ck_seasons_date_order, ck_seasons_max_competitions, ck_seasons_name_length, ck_seasons_prize_pool, ck_seasons_registration_order, ck_seasons_slug_length, ck_seasons_status, ck_seasons_year_range, completed, fk_seasons_sport_id, playoffs, registration, seasons, upcoming, {self.name}, {self.status}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum SeasonStatus not found in schema

### 💡 Recommendations
- Add SeasonStatus to schema for fields: 

---

## 🏷️ Group_Membership Enum Analysis

### Database Model Enums
- **MembershipRole** (enum_class)
  - Values: Additional notes about the membership, ID of the group, ID of the user, ID of the user who banned this member, ID of the user who sent the invitation, Reason for the ban, Role of the user in the group, Status of the membership, Unique identifier for the membership, When the invitation was sent, When the membership record was created, When the membership was last updated, When the user joined the group, When the user left the group, When the user was banned, active, admin, banned, ck_group_memberships_banned_after_joined, ck_group_memberships_invitation_before_joined, ck_group_memberships_left_after_joined, ck_group_memberships_role, ck_group_memberships_status, creator, fk_group_memberships_banned_by_id, fk_group_memberships_group_id, fk_group_memberships_invited_by_id, fk_group_memberships_user_id, group_memberships, invited, left, member, moderator, pending, uq_group_memberships_group_user, {self.role}, {self.status}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum MembershipRole not found in schema

### 💡 Recommendations
- Add MembershipRole to schema for fields: 

---

## 🏷️ Audit_Log Enum Analysis

### Database Model Enums
- **ActionType** (enum_class)
  - Values: Additional device information, Additional notes or comments, Additional structured data related to the action, Correlation ID for tracking related actions, Geographic location information, Human-readable description of the action, ID of the admin who reviewed this entry, ID of the entity being acted upon, ID of the user performing the action, IP address of the client, New values after the change, Previous values before the change, Request ID for tracing across services, Risk score of the action (0-100), Session ID when the action was performed, Severity level of the log entry, Summary of changes made, Type of action performed, Type of entity being acted upon, Unique identifier for the audit log entry, User agent string from the client, When the action occurred, When the audit log entry was created, When this entry was reviewed, Whether this action has been flagged for review, admin, audit_logs, bet, bet_place, bet_settle, ck_audit_logs_action_type, ck_audit_logs_entity_type, ck_audit_logs_log_level, ck_audit_logs_message_length, ck_audit_logs_reviewed_after_action, ck_audit_logs_risk_score_range, competition, create, critical, debug, delete, error, fk_audit_logs_reviewed_by, fk_audit_logs_user_id, group, info, login, logout, match, password_change, payment, player, reactivation, read, result, season, suspension, system, team, transfer, update, user, verification, warning, {self.action_type}, {self.entity_type}, {self.log_level}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum ActionType not found in schema

### 💡 Recommendations
- Add ActionType to schema for fields: 

---

## 🏷️ Match Enum Analysis

### Database Model Enums
- **MatchStatus** (enum_class)
  - Values: Additional match notes, Away team penalty shootout score, Away team score in extra time, Away team score in regular time, Current match status, Home team penalty shootout score, Home team score in extra time, Home team score in regular time, ID of the away team, ID of the competition this match belongs to, ID of the home team, Live betting odds during the match, Match day number, Match events (goals, cards, substitutions, etc.), Match referee, Number of spectators, Round number in the competition, Unique identifier for the match, Venue where the match is played, Weather conditions during the match, When betting closes for this match, When the match actually started, When the match finished, When the match is scheduled to start, When the match was created, When the match was last updated, cancelled, ck_matches_attendance, ck_matches_away_score, ck_matches_different_teams, ck_matches_extra_time_away_score, ck_matches_extra_time_home_score, ck_matches_finish_after_start, ck_matches_home_score, ck_matches_match_day, ck_matches_penalties_away_score, ck_matches_penalties_home_score, ck_matches_round_number, ck_matches_status, extra_time, finished, fk_matches_away_team_id, fk_matches_competition_id, fk_matches_home_team_id, halftime, live, matches, penalties, postponed, scheduled, {self.status}
  - Used by fields: 

### 🔴 Inconsistencies Found
- **Missing Schema Enum**: Model enum MatchStatus not found in schema

### 💡 Recommendations
- Add MatchStatus to schema for fields: 

---

## 🌱 Seed Data Enum Usage

- **status_values**: active, completed, final, finished, fit, verified
- **role_values**: admin
- **category_values**: team_sport
- **format_values**: knockout
- **visibility_values**: public

*Generated on: 5 October 2025*