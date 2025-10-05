# 🔍 Field Naming Consistency Analysis
## Betting League Championship Platform

This document provides field-by-field naming consistency analysis across the entire technology stack.

## 📊 Analysis Summary

| Status | Description |
|--------|-------------|
| 🟢 Full Stack | Field exists in Database, API Schema, and Seed Data |
| 🟡 DB + API | Field exists in Database and API Schema (most common) |
| 🔵 DB Only | Field exists only in Database Model |
| 🟠 API Only | Field exists only in API Schema |
| 🔴 Seed Only | Field exists only in Seed Data |

## 🏷️ User Field Analysis

**Total Fields:** 54 | **Full Stack:** 0 | **DB + API:** 8

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `100` | N/A | raise ValueError('Name must not exceed 100 characters') | ❌ | 🟠 API Only |
| `128` | N/A | raise ValueError('Password must not exceed 128 characters') | ❌ | 🟠 API Only |
| `3` | N/A | raise ValueError('Username must be at least 3 characters long') | ❌ | 🟠 API Only |
| `50` | N/A | raise ValueError('Username must not exceed 50 characters') | ❌ | 🟠 API Only |
| `8` | N/A | raise ValueError('Password must be at least 8 characters long') | ❌ | 🟠 API Only |
| `Config` | N/A | """Pydantic config for ORM mode.""" | ❌ | 🟠 API Only |
| `None` | N/A | v | ❌ | 🟠 API Only |
| `access_token` | N/A | str | ❌ | 🟠 API Only |
| `avatar_url` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `biography` | TEXT | N/A | ❌ | 🔵 DB Only |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `currency` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `current_password` | N/A | str | ❌ | 🟠 API Only |
| `date_of_birth` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `deleted_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `display_name` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `email` | VARCHAR | Optional[EmailStr] | ❌ | 🟡 DB + API |
| `email_verified` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `expires_in` | N/A | int | ❌ | 🟠 API Only |
| `failed_login_attempts` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `first_name` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `is_active` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `is_verified` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `kyc_status` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `kyc_verified_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `language` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `last_login` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `last_login_at` | N/A | Optional[datetime] | ❌ | 🟠 API Only |
| `last_login_ip` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `last_name` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `locked_until` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `marketing_consent` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `new_password` | N/A | str | ❌ | 🟠 API Only |
| `notifications_enabled` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `password` | N/A | str | ❌ | 🟠 API Only |
| `password_changed_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `password_hash` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `phone_number` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `phone_verified` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `privacy_policy_accepted` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `role` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `status` | VARCHAR | UserStatus | ❌ | 🟡 DB + API |
| `terms_accepted` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `terms_accepted_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `timezone` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `token_type` | N/A | str | ❌ | 🟠 API Only |
| `total_bets` | N/A | int | ❌ | 🟠 API Only |
| `total_winnings` | N/A | float | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | Optional[datetime] | ❌ | 🟡 DB + API |
| `user` | N/A | UserResponse | ❌ | 🟠 API Only |
| `username` | VARCHAR | str | ❌ | 🟡 DB + API |
| `website_url` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `win_rate` | N/A | float | ❌ | 🟠 API Only |

**Consistency Rate:** 14.8% (8/54 fields consistent)

---

## 🏷️ Sport Field Analysis

**Total Fields:** 26 | **Full Stack:** 0 | **DB + API:** 7

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `100` | N/A | raise ValueError('Sport name must not exceed 100 characters') | ❌ | 🟠 API Only |
| `1000` | N/A | raise ValueError('Description must not exceed 1000 characters') | ❌ | 🟠 API Only |
| `2` | N/A | raise ValueError('Sport name must be at least 2 characters long') | ❌ | 🟠 API Only |
| `5000` | N/A | raise ValueError('Rules must not exceed 5000 characters') | ❌ | 🟠 API Only |
| `Config` | N/A | """Pydantic config for ORM mode.""" | ❌ | 🟠 API Only |
| `None` | N/A | v | ❌ | 🟠 API Only |
| `active_competitions` | N/A | int | ❌ | 🟠 API Only |
| `category` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `color_scheme` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `default_bet_types` | JSON | N/A | ❌ | 🔵 DB Only |
| `description` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `icon_url` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `is_active` | BOOLEAN | bool | ❌ | 🟡 DB + API |
| `match_duration` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `name` | VARCHAR | str | ❌ | 🟡 DB + API |
| `popularity_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `rules` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `scoring_system` | JSON | N/A | ❌ | 🔵 DB Only |
| `season_structure` | JSON | N/A | ❌ | 🔵 DB Only |
| `slug` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `total_competitions` | N/A | int | ❌ | 🟠 API Only |
| `total_matches` | N/A | int | ❌ | 🟠 API Only |
| `total_teams` | N/A | int | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |

**Consistency Rate:** 26.9% (7/26 fields consistent)

---

## 🏷️ Team Field Analysis

**Total Fields:** 38 | **Full Stack:** 0 | **DB + API:** 11

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `10` | N/A | raise ValueError('Short name must not exceed 10 characters') | ❌ | 🟠 API Only |
| `100` | N/A | raise ValueError('Location field must not exceed 100 characters') | ❌ | 🟠 API Only |
| `2` | N/A | raise ValueError('Team name must be at least 2 characters long') | ❌ | 🟠 API Only |
| `500` | N/A | raise ValueError('URL must not exceed 500 characters') | ❌ | 🟠 API Only |
| `Config` | N/A | """Pydantic config for ORM mode.""" | ❌ | 🟠 API Only |
| `None` | N/A | v | ❌ | 🟠 API Only |
| `banner_url` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `captain_id` | UUID | N/A | ❌ | 🔵 DB Only |
| `city` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `coach_name` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `country` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `current_league` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `description` | TEXT | N/A | ❌ | 🔵 DB Only |
| `draws` | N/A | int | ❌ | 🟠 API Only |
| `founded_year` | INTEGER | Optional[int] | ❌ | 🟡 DB + API |
| `home_venue` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `is_active` | BOOLEAN | bool | ❌ | 🟡 DB + API |
| `league_position` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `logo_url` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `losses` | N/A | int | ❌ | 🟠 API Only |
| `max_players` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `name` | VARCHAR | str | ❌ | 🟡 DB + API |
| `primary_color` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `secondary_color` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `short_name` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `slug` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `social_links` | JSON | N/A | ❌ | 🔵 DB Only |
| `sport_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `sport_name` | N/A | str | ❌ | 🟠 API Only |
| `total_matches` | N/A | int | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `v` | N/A | raise ValueError('Sport ID is required') | ❌ | 🟠 API Only |
| `website` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `website_url` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `win_percentage` | N/A | float | ❌ | 🟠 API Only |
| `wins` | N/A | int | ❌ | 🟠 API Only |

**Consistency Rate:** 28.9% (11/38 fields consistent)

---

## 🏷️ Player Field Analysis

**Total Fields:** 74 | **Full Stack:** 0 | **DB + API:** 20

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `60` | N/A | raise ValueError('Player age must be between 10 and 60 years') | ❌ | 🟠 API Only |
| `Config` | N/A | from_attributes | ❌ | 🟠 API Only |
| `None` | N/A | today | ❌ | 🟠 API Only |
| `age_max` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `age_min` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `agent_contact` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `agent_name` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `assists` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `biography` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `contract_end` | Date | Optional[date] | ❌ | 🟡 DB + API |
| `contract_history` | N/A | List[dict] | ❌ | 🟠 API Only |
| `contract_start` | Date | Optional[date] | ❌ | 🟡 DB + API |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `current_team_id` | UUID | N/A | ❌ | 🔵 DB Only |
| `data` | N/A | return f"{info.data['first_name']} {info.data['last_name']}" | ❌ | 🟠 API Only |
| `date_of_birth` | Date | Optional[date] | ❌ | 🟡 DB + API |
| `description` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `detailed_stats` | N/A | Optional[dict] | ❌ | 🟠 API Only |
| `display_name` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `expected_return` | N/A | Optional[date] | ❌ | 🟠 API Only |
| `first_name` | VARCHAR | str | ❌ | 🟡 DB + API |
| `from_team_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |
| `goals_scored` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `height_cm` | INTEGER | Optional[int] | ❌ | 🟡 DB + API |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `injury_date` | N/A | date | ❌ | 🟠 API Only |
| `injury_status` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `injury_type` | N/A | str | ❌ | 🟠 API Only |
| `is_active` | BOOLEAN | bool | ❌ | 🟡 DB + API |
| `is_captain` | N/A | Optional[bool] | ❌ | 🟠 API Only |
| `is_resolved` | N/A | bool | ❌ | 🟠 API Only |
| `is_vice_captain` | N/A | Optional[bool] | ❌ | 🟠 API Only |
| `jersey_number` | INTEGER | Optional[int] | ❌ | 🟡 DB + API |
| `last_name` | VARCHAR | str | ❌ | 🟡 DB + API |
| `last_updated` | N/A | datetime | ❌ | 🟠 API Only |
| `market_value` | Numeric(12 | Optional[float] | ❌ | 🟡 DB + API |
| `market_value_max` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `market_value_min` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `match_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |
| `matches_played` | N/A | int | ❌ | 🟠 API Only |
| `matches_started` | N/A | int | ❌ | 🟠 API Only |
| `middle_name` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `minutes_played` | N/A | int | ❌ | 🟠 API Only |
| `nationality` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `nickname` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `notes` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `photo_url` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `player_id` | N/A | UUID | ❌ | 🟠 API Only |
| `position` | VARCHAR | Optional[PlayerPosition] | ❌ | 🟡 DB + API |
| `preferred_foot` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `profile_image_url` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `rating` | N/A | float | ❌ | 🟠 API Only |
| `rating_source` | N/A | str | ❌ | 🟠 API Only |
| `red_cards` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `retirement_date` | Date | N/A | ❌ | 🔵 DB Only |
| `salary` | Numeric(12 | Optional[float] | ❌ | 🟡 DB + API |
| `season_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |
| `secondary_positions` | N/A | Optional[List[PlayerPosition]] | ❌ | 🟠 API Only |
| `severity` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `social_media` | JSON | Optional[dict] | ❌ | 🟡 DB + API |
| `sport_id` | UUID | N/A | ❌ | 🔵 DB Only |
| `stats` | N/A | PlayerStats | ❌ | 🟠 API Only |
| `status` | N/A | Optional[PlayerStatus] | ❌ | 🟠 API Only |
| `team` | N/A | dict | ❌ | 🟠 API Only |
| `team_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |
| `to_team_id` | N/A | UUID | ❌ | 🟠 API Only |
| `transfer_date` | N/A | date | ❌ | 🟠 API Only |
| `transfer_fee` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `transfer_history` | N/A | List[PlayerTransfer] | ❌ | 🟠 API Only |
| `transfer_type` | N/A | str | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `v` | N/A | Optional[date]) -> Optional[date]: | ❌ | 🟠 API Only |
| `weight_kg` | Numeric(5 | Optional[float] | ❌ | 🟡 DB + API |
| `yellow_cards` | N/A | Optional[int] | ❌ | 🟠 API Only |

**Consistency Rate:** 27.0% (20/74 fields consistent)

---

## 🏷️ Competition Field Analysis

**Total Fields:** 55 | **Full Stack:** 0 | **DB + API:** 13

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `Config` | N/A | from_attributes | ❌ | 🟠 API Only |
| `None` | N/A | if v < info.data['min_teams']: | ❌ | 🟠 API Only |
| `allow_betting` | N/A | bool | ❌ | 🟠 API Only |
| `allow_public_betting` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `banner_url` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `betting_closes_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `competition_id` | N/A | UUID | ❌ | 🟠 API Only |
| `completed_matches` | N/A | int | ❌ | 🟠 API Only |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `created_by` | UUID | N/A | ❌ | 🔵 DB Only |
| `days_remaining` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `description` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `end_date` | TIMESTAMP | Optional[datetime] | ❌ | 🟡 DB + API |
| `entry_fee` | Numeric(10 | Optional[float] | ❌ | 🟡 DB + API |
| `format` | N/A | CompetitionFormat | ❌ | 🟠 API Only |
| `format_type` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `group_id` | UUID | N/A | ❌ | 🔵 DB Only |
| `http` | N/A | //') or v.startswith('https://')): | ❌ | 🟠 API Only |
| `https` | N/A | //{v}' | ❌ | 🟠 API Only |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `is_active` | N/A | bool | ❌ | 🟠 API Only |
| `is_public` | N/A | bool | ❌ | 🟠 API Only |
| `location` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `logo_url` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `max_participants` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `max_teams` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `min_participants` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `min_teams` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `name` | VARCHAR | str | ❌ | 🟡 DB + API |
| `participation_rate` | N/A | float | ❌ | 🟠 API Only |
| `pending_matches` | N/A | int | ❌ | 🟠 API Only |
| `point_system` | JSON | N/A | ❌ | 🔵 DB Only |
| `prize_distribution` | JSON | N/A | ❌ | 🔵 DB Only |
| `prize_pool` | Numeric(12 | Optional[float] | ❌ | 🟡 DB + API |
| `registration_deadline` | TIMESTAMP | Optional[datetime] | ❌ | 🟡 DB + API |
| `registration_notes` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `registration_open` | N/A | bool | ❌ | 🟠 API Only |
| `rules` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `season_id` | UUID | N/A | ❌ | 🔵 DB Only |
| `slug` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `sport` | N/A | SportSummary | ❌ | 🟠 API Only |
| `sport_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `start_date` | TIMESTAMP | Optional[datetime] | ❌ | 🟡 DB + API |
| `stats` | N/A | CompetitionStats | ❌ | 🟠 API Only |
| `status` | VARCHAR | CompetitionStatus | ❌ | 🟡 DB + API |
| `team_id` | N/A | UUID | ❌ | 🟠 API Only |
| `teams` | N/A | List[TeamSummary] | ❌ | 🟠 API Only |
| `total_bet_amount` | N/A | float | ❌ | 🟠 API Only |
| `total_bets` | N/A | int | ❌ | 🟠 API Only |
| `total_matches` | N/A | int | ❌ | 🟠 API Only |
| `total_teams` | N/A | int | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `v` | N/A | Optional[str]) -> Optional[str]: | ❌ | 🟠 API Only |
| `visibility` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `website` | N/A | Optional[str] | ❌ | 🟠 API Only |

**Consistency Rate:** 23.6% (13/55 fields consistent)

---

## 🏷️ Season Field Analysis

**Total Fields:** 54 | **Full Stack:** 0 | **DB + API:** 12

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `Config` | N/A | from_attributes | ❌ | 🟠 API Only |
| `None` | N/A | if v > info.data['max_teams']: | ❌ | 🟠 API Only |
| `allow_betting` | N/A | Optional[bool] | ❌ | 🟠 API Only |
| `allow_draws` | N/A | Optional[bool] | ❌ | 🟠 API Only |
| `average_goals_per_match` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `competitions` | N/A | List[CompetitionSummary] | ❌ | 🟠 API Only |
| `completed_matches` | N/A | int | ❌ | 🟠 API Only |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `days_remaining` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `description` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `end_date` | TIMESTAMP | date | ❌ | 🟡 DB + API |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `is_active` | N/A | bool | ❌ | 🟠 API Only |
| `is_current` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `is_public` | N/A | bool | ❌ | 🟠 API Only |
| `last_updated` | N/A | datetime | ❌ | 🟠 API Only |
| `max_competitions` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `max_teams` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `min_teams` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `name` | VARCHAR | str | ❌ | 🟡 DB + API |
| `pending_matches` | N/A | int | ❌ | 🟠 API Only |
| `playoff_format` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `playoff_teams` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `point_system` | JSON | N/A | ❌ | 🔵 DB Only |
| `points_for_draw` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `points_for_loss` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `points_for_win` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `prize_pool_total` | Numeric(12 | N/A | ❌ | 🔵 DB Only |
| `progress_percentage` | N/A | float | ❌ | 🟠 API Only |
| `promotion_rules` | JSON | N/A | ❌ | 🔵 DB Only |
| `promotion_teams` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `registration_end` | TIMESTAMP | Optional[date] | ❌ | 🟡 DB + API |
| `registration_start` | TIMESTAMP | Optional[date] | ❌ | 🟡 DB + API |
| `relegation_rules` | JSON | N/A | ❌ | 🔵 DB Only |
| `relegation_teams` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `rules` | TEXT | N/A | ❌ | 🔵 DB Only |
| `season_format` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `season_id` | N/A | UUID | ❌ | 🟠 API Only |
| `season_type` | N/A | SeasonType | ❌ | 🟠 API Only |
| `slug` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `sport_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `standings` | N/A | List[dict] | ❌ | 🟠 API Only |
| `start_date` | TIMESTAMP | date | ❌ | 🟡 DB + API |
| `stats` | N/A | SeasonStats | ❌ | 🟠 API Only |
| `status` | VARCHAR | SeasonStatus | ❌ | 🟡 DB + API |
| `tie_breaker_rules` | JSON | N/A | ❌ | 🔵 DB Only |
| `total_bet_amount` | N/A | float | ❌ | 🟠 API Only |
| `total_bets` | N/A | int | ❌ | 🟠 API Only |
| `total_competitions` | N/A | int | ❌ | 🟠 API Only |
| `total_matches` | N/A | int | ❌ | 🟠 API Only |
| `total_teams` | N/A | int | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `v` | N/A | Optional[int], info) -> Optional[int]: | ❌ | 🟠 API Only |
| `year` | INTEGER | int | ❌ | 🟡 DB + API |

**Consistency Rate:** 22.2% (12/54 fields consistent)

---

## 🏷️ Match Field Analysis

**Total Fields:** 71 | **Full Stack:** 0 | **DB + API:** 17

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `Config` | N/A | from_attributes | ❌ | 🟠 API Only |
| `allow_betting` | N/A | Optional[bool] | ❌ | 🟠 API Only |
| `attendance` | INTEGER | Optional[int] | ❌ | 🟡 DB + API |
| `away_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `away_score` | INTEGER | int | ❌ | 🟡 DB + API |
| `away_team` | N/A | dict | ❌ | 🟠 API Only |
| `away_team_bets` | N/A | int | ❌ | 🟠 API Only |
| `away_team_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `betting_closes_at` | TIMESTAMP | Optional[datetime] | ❌ | 🟡 DB + API |
| `competition` | N/A | dict | ❌ | 🟠 API Only |
| `competition_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `confidence` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `data` | N/A | if v > info.data['scheduled_at']: | ❌ | 🟠 API Only |
| `description` | N/A | str | ❌ | 🟠 API Only |
| `draw_bets` | N/A | int | ❌ | 🟠 API Only |
| `draw_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `duration_minutes` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `event_type` | N/A | str | ❌ | 🟠 API Only |
| `events` | N/A | List[dict] | ❌ | 🟠 API Only |
| `extra_time_away_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `extra_time_home_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `finished_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `home_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `home_score` | INTEGER | int | ❌ | 🟡 DB + API |
| `home_team` | N/A | dict | ❌ | 🟠 API Only |
| `home_team_bets` | N/A | int | ❌ | 🟠 API Only |
| `home_team_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `is_active` | N/A | Optional[bool] | ❌ | 🟠 API Only |
| `is_draw` | N/A | bool | ❌ | 🟠 API Only |
| `is_final` | N/A | bool | ❌ | 🟠 API Only |
| `is_home_game` | N/A | Optional[bool] | ❌ | 🟠 API Only |
| `last_updated` | N/A | datetime | ❌ | 🟠 API Only |
| `live_odds` | JSON | N/A | ❌ | 🔵 DB Only |
| `match_day` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `match_events` | JSON | N/A | ❌ | 🔵 DB Only |
| `match_id` | N/A | UUID | ❌ | 🟠 API Only |
| `match_type` | N/A | Optional[MatchType] | ❌ | 🟠 API Only |
| `minute` | N/A | int | ❌ | 🟠 API Only |
| `notes` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `penalties_away_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `penalties_home_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `period` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `player_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |
| `predicted_away_score` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `predicted_home_score` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `predicted_winner` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `referee` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `round_number` | INTEGER | Optional[int] | ❌ | 🟡 DB + API |
| `scheduled_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `season_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |
| `sport` | N/A | Optional[dict] | ❌ | 🟠 API Only |
| `started_at` | TIMESTAMP | Optional[datetime] | ❌ | 🟡 DB + API |
| `stats` | N/A | MatchStats | ❌ | 🟠 API Only |
| `status` | VARCHAR | MatchStatus | ❌ | 🟡 DB + API |
| `status_reason` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `team_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |
| `total_bet_amount` | N/A | float | ❌ | 🟠 API Only |
| `total_bets` | N/A | int | ❌ | 🟠 API Only |
| `tv_viewers` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `v` | N/A | UUID, info) -> UUID: | ❌ | 🟠 API Only |
| `venue` | VARCHAR | Optional[MatchVenue] | ❌ | 🟡 DB + API |
| `venue_city` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `venue_country` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `venue_name` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `verified` | N/A | bool | ❌ | 🟠 API Only |
| `weather_conditions` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `week_number` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `winner_team_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |

**Consistency Rate:** 23.9% (17/71 fields consistent)

---

## 🏷️ Bet Field Analysis

**Total Fields:** 88 | **Full Stack:** 0 | **DB + API:** 12

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `01` | N/A | raise ValueError('Total stake must equal sum of individual bet amounts') | ❌ | 🟠 API Only |
| `Config` | N/A | from_attributes | ❌ | 🟠 API Only |
| `MATCH_WINNER` | N/A | if v is None: | ❌ | 🟠 API Only |
| `Note` | N/A | In a real implementation, this would check the database | ❌ | 🟠 API Only |
| `active_bettors` | N/A | int | ❌ | 🟠 API Only |
| `actual_payout` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `amount` | N/A | float | ❌ | 🟠 API Only |
| `average_bet_size` | N/A | float | ❌ | 🟠 API Only |
| `average_odds` | N/A | float | ❌ | 🟠 API Only |
| `away_handicap_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `away_win_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `bet_id` | N/A | UUID | ❌ | 🟠 API Only |
| `bet_parameters` | N/A | Optional[dict] | ❌ | 🟠 API Only |
| `bet_type` | VARCHAR | BetType | ❌ | 🟡 DB + API |
| `bet_type_stats` | N/A | dict | ❌ | 🟠 API Only |
| `bets` | N/A | List[BetCreate] | ❌ | 🟠 API Only |
| `bonus_applied` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `bookmaker` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `both_teams_score_no` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `both_teams_score_yes` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `commission` | Numeric(8 | N/A | ❌ | 🔵 DB Only |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `data` | N/A | expected_total | ❌ | 🟠 API Only |
| `device_info` | JSON | N/A | ❌ | 🔵 DB Only |
| `draw_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `entries` | N/A | List[dict] | ❌ | 🟠 API Only |
| `group_id` | N/A | Optional[UUID] | ❌ | 🟠 API Only |
| `handicap` | Numeric(5 | N/A | ❌ | 🔵 DB Only |
| `handicap_line` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `handicap_value` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `home_handicap_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `home_win_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `house_edge` | N/A | float | ❌ | 🟠 API Only |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `ip_address` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `is_active` | N/A | bool | ❌ | 🟠 API Only |
| `is_over` | N/A | Optional[bool] | ❌ | 🟠 API Only |
| `last_updated` | N/A | datetime | ❌ | 🟠 API Only |
| `lost_bets` | N/A | int | ❌ | 🟠 API Only |
| `market_type` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `match` | N/A | dict | ❌ | 🟠 API Only |
| `match_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `max_liability` | Numeric(12 | N/A | ❌ | 🔵 DB Only |
| `most_bet_matches` | N/A | List[dict] | ❌ | 🟠 API Only |
| `notes` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `odds` | Numeric(8 | float | ❌ | 🟡 DB + API |
| `outcome` | N/A | Optional[BetOutcome] | ❌ | 🟠 API Only |
| `over_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `payout_amount` | Numeric(12 | N/A | ❌ | 🔵 DB Only |
| `pending_bets` | N/A | int | ❌ | 🟠 API Only |
| `period` | N/A | str | ❌ | 🟠 API Only |
| `placed_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `popular_bet_types` | N/A | dict | ❌ | 🟠 API Only |
| `potential_payout` | Numeric(12 | float | ❌ | 🟡 DB + API |
| `potential_return` | N/A | float | ❌ | 🟠 API Only |
| `predicted_away_score` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `predicted_home_score` | N/A | Optional[int] | ❌ | 🟠 API Only |
| `profit_loss` | N/A | float | ❌ | 🟠 API Only |
| `promotion_id` | UUID | N/A | ❌ | 🔵 DB Only |
| `return_to_player` | N/A | float | ❌ | 🟠 API Only |
| `risk_category` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `selection` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `settled_at` | TIMESTAMP | Optional[datetime] | ❌ | 🟡 DB + API |
| `settled_by` | N/A | UUID | ❌ | 🟠 API Only |
| `settlement_reason` | N/A | str | ❌ | 🟠 API Only |
| `slip_type` | N/A | str | ❌ | 🟠 API Only |
| `stake_amount` | Numeric(10 | N/A | ❌ | 🔵 DB Only |
| `stats` | N/A | BetStats | ❌ | 🟠 API Only |
| `status` | VARCHAR | BetStatus | ❌ | 🟡 DB + API |
| `summary_stats` | N/A | BetStats | ❌ | 🟠 API Only |
| `total_amount` | N/A | float | ❌ | 🟠 API Only |
| `total_amount_wagered` | N/A | float | ❌ | 🟠 API Only |
| `total_bets` | N/A | int | ❌ | 🟠 API Only |
| `total_bets_placed` | N/A | int | ❌ | 🟠 API Only |
| `total_goals_line` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `total_payout` | N/A | float | ❌ | 🟠 API Only |
| `total_payouts` | N/A | float | ❌ | 🟠 API Only |
| `total_stake` | N/A | float | ❌ | 🟠 API Only |
| `total_value` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `under_odds` | N/A | Optional[float] | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `user` | N/A | dict | ❌ | 🟠 API Only |
| `user_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `v` | N/A | float, info) -> float: | ❌ | 🟠 API Only |
| `void_bets` | N/A | int | ❌ | 🟠 API Only |
| `void_reason` | TEXT | N/A | ❌ | 🔵 DB Only |
| `win_rate` | N/A | float | ❌ | 🟠 API Only |
| `won_bets` | N/A | int | ❌ | 🟠 API Only |

**Consistency Rate:** 13.6% (12/88 fields consistent)

---

## 🏷️ Result Field Analysis

**Total Fields:** 94 | **Full Stack:** 0 | **DB + API:** 8

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `0` | N/A | raise ValueError("At least one result must be provided") | ❌ | 🟠 API Only |
| `05T14` | N/A | 30:00Z", | ❌ | 🟠 API Only |
| `05T15` | N/A | 00:00Z", | ❌ | 🟠 API Only |
| `100` | N/A | raise ValueError("Maximum 100 results can be created at once") | ❌ | 🟠 API Only |
| `45` | N/A | 23", "67:12"], | ❌ | 🟠 API Only |
| `None` | N/A | if not isinstance(v, dict): | ❌ | 🟠 API Only |
| `additional_data` | N/A | Optional[Dict[str, Any]] | ❌ | 🟠 API Only |
| `allowed_priorities` | N/A | raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}") | ❌ | 🟠 API Only |
| `average_goals_per_match` | N/A | Decimal | ❌ | 🟠 API Only |
| `away_score` | INTEGER | Optional[int] | ❌ | 🟡 DB + API |
| `away_win_percentage` | N/A | Optional[Decimal] | ❌ | 🟠 API Only |
| `away_wins` | N/A | int | ❌ | 🟠 API Only |
| `both_teams_scored` | N/A | bool | ❌ | 🟠 API Only |
| `both_teams_scored_count` | N/A | int | ❌ | 🟠 API Only |
| `changes` | N/A | List[Dict[str, Any]] | ❌ | 🟠 API Only |
| `clean_sheet` | N/A | bool | ❌ | 🟠 API Only |
| `clean_sheets` | N/A | int | ❌ | 🟠 API Only |
| `confirmation_notes` | N/A | Optional[str] | ❌ | 🟠 API Only |
| `confirmed` | N/A | bool | ❌ | 🟠 API Only |
| `confirmed_at` | N/A | Optional[datetime] | ❌ | 🟠 API Only |
| `confirmed_results` | N/A | int | ❌ | 🟠 API Only |
| `corners_away` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `corners_home` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `created_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `created_count` | N/A | int | ❌ | 🟠 API Only |
| `created_results` | N/A | List[UUID] | ❌ | 🟠 API Only |
| `dispute_reason` | N/A | str | ❌ | 🟠 API Only |
| `disputed_by` | N/A | UUID | ❌ | 🟠 API Only |
| `disputed_results` | N/A | int | ❌ | 🟠 API Only |
| `draw_percentage` | N/A | Optional[Decimal] | ❌ | 🟠 API Only |
| `draws` | N/A | int | ❌ | 🟠 API Only |
| `error_count` | N/A | int | ❌ | 🟠 API Only |
| `errors` | N/A | List[Dict[str, Any]] | ❌ | 🟠 API Only |
| `evidence` | N/A | Optional[Dict[str, Any]] | ❌ | 🟠 API Only |
| `extra_time_away_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `extra_time_home_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `finished_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `first_recorded` | N/A | datetime | ❌ | 🟠 API Only |
| `half_time_away_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `half_time_home_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `highest_scoring_match` | N/A | Optional[Dict[str, Any]] | ❌ | 🟠 API Only |
| `home_score` | INTEGER | Optional[int] | ❌ | 🟡 DB + API |
| `home_win_percentage` | N/A | Optional[Decimal] | ❌ | 🟠 API Only |
| `home_wins` | N/A | int | ❌ | 🟠 API Only |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `is_official` | BOOLEAN | N/A | ❌ | 🔵 DB Only |
| `is_valid` | N/A | bool | ❌ | 🟠 API Only |
| `last_updated` | N/A | Optional[datetime] | ❌ | 🟠 API Only |
| `match` | N/A | Optional[Dict[str, Any]] | ❌ | 🟠 API Only |
| `match_events` | JSON | N/A | ❌ | 🔵 DB Only |
| `match_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `match_result` | N/A | str | ❌ | 🟠 API Only |
| `most_goals_by_team` | N/A | Optional[Dict[str, Any]] | ❌ | 🟠 API Only |
| `notes` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `outcome_data` | N/A | Dict[str, Any] | ❌ | 🟠 API Only |
| `override_validation` | N/A | bool | ❌ | 🟠 API Only |
| `penalty_away_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `penalty_home_score` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `pending_results` | N/A | int | ❌ | 🟠 API Only |
| `period_end` | N/A | datetime | ❌ | 🟠 API Only |
| `period_start` | N/A | datetime | ❌ | 🟠 API Only |
| `possession_away` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `possession_home` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `priority` | N/A | str | ❌ | 🟠 API Only |
| `recorded_at` | N/A | datetime | ❌ | 🟠 API Only |
| `recorded_by` | N/A | UUID | ❌ | 🟠 API Only |
| `recorded_by_user` | N/A | Optional[Dict[str, Any]] | ❌ | 🟠 API Only |
| `red_cards_away` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `red_cards_home` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `result_id` | N/A | UUID | ❌ | 🟠 API Only |
| `result_type` | N/A | ResultType | ❌ | 🟠 API Only |
| `results` | N/A | List[ResultCreate] | ❌ | 🟠 API Only |
| `shots_away` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `shots_home` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `skip_duplicates` | N/A | bool | ❌ | 🟠 API Only |
| `skipped_count` | N/A | int | ❌ | 🟠 API Only |
| `started_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `statistics` | JSON | Optional[Dict[str, Any]] | ❌ | 🟡 DB + API |
| `status` | VARCHAR | ResultStatus | ❌ | 🟡 DB + API |
| `suggested_corrections` | N/A | Optional[Dict[str, Any]] | ❌ | 🟠 API Only |
| `total_goals` | N/A | int | ❌ | 🟠 API Only |
| `total_matches` | N/A | int | ❌ | 🟠 API Only |
| `total_results` | N/A | int | ❌ | 🟠 API Only |
| `total_updates` | N/A | int | ❌ | 🟠 API Only |
| `try` | N/A | import json | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | Optional[datetime] | ❌ | 🟡 DB + API |
| `validate_all` | N/A | bool | ❌ | 🟠 API Only |
| `validation_errors` | N/A | List[str] | ❌ | 🟠 API Only |
| `validation_warnings` | N/A | List[str] | ❌ | 🟠 API Only |
| `verified_at` | TIMESTAMP | N/A | ❌ | 🔵 DB Only |
| `verified_by` | VARCHAR | N/A | ❌ | 🔵 DB Only |
| `winner_team_id` | UUID | N/A | ❌ | 🔵 DB Only |
| `yellow_cards_away` | INTEGER | N/A | ❌ | 🔵 DB Only |
| `yellow_cards_home` | INTEGER | N/A | ❌ | 🔵 DB Only |

**Consistency Rate:** 8.5% (8/94 fields consistent)

---

## 🏷️ Group Field Analysis

**Total Fields:** 28 | **Full Stack:** 0 | **DB + API:** 17

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|
| `0` | N/A | raise ValueError('Max members must be greater than 0') | ❌ | 🟠 API Only |
| `10` | N/A | raise ValueError('Group description must be at least 10 characters long') | ❌ | 🟠 API Only |
| `100` | N/A | raise ValueError('Group name must not exceed 100 characters') | ❌ | 🟠 API Only |
| `1000` | N/A | raise ValueError('Max members cannot exceed 1000') | ❌ | 🟠 API Only |
| `3` | N/A | raise ValueError('Group name must be at least 3 characters long') | ❌ | 🟠 API Only |
| `Config` | N/A | """Pydantic config for ORM mode.""" | ❌ | 🟠 API Only |
| `None` | N/A | if v < | ❌ | 🟠 API Only |
| `active_bets` | N/A | int | ❌ | 🟠 API Only |
| `allow_member_invites` | BOOLEAN | Optional[bool] | ❌ | 🟡 DB + API |
| `auto_approve_members` | BOOLEAN | Optional[bool] | ❌ | 🟡 DB + API |
| `avatar_url` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `banner_url` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `created_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |
| `creator_id` | UUID | UUID | ❌ | 🟡 DB + API |
| `description` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `entry_fee` | Numeric(10 | Optional[float] | ❌ | 🟡 DB + API |
| `id` | UUID | UUID | ❌ | 🟡 DB + API |
| `is_private` | BOOLEAN | bool | ❌ | 🟡 DB + API |
| `join_code` | VARCHAR | Optional[str] | ❌ | 🟡 DB + API |
| `max_members` | INTEGER | Optional[int] | ❌ | 🟡 DB + API |
| `member_count` | N/A | int | ❌ | 🟠 API Only |
| `name` | VARCHAR | str | ❌ | 🟡 DB + API |
| `point_system` | VARCHAR | PointSystem | ❌ | 🟡 DB + API |
| `prize_pool` | Numeric(12 | Optional[float] | ❌ | 🟡 DB + API |
| `rules_text` | TEXT | Optional[str] | ❌ | 🟡 DB + API |
| `total_bets` | N/A | int | ❌ | 🟠 API Only |
| `total_winnings` | N/A | float | ❌ | 🟠 API Only |
| `updated_at` | TIMESTAMP | datetime | ❌ | 🟡 DB + API |

**Consistency Rate:** 60.7% (17/28 fields consistent)

---

## 🏷️ GroupMembership Field Analysis

**Total Fields:** 0 | **Full Stack:** 0 | **DB + API:** 0

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|

---

## 🏷️ AuditLog Field Analysis

**Total Fields:** 0 | **Full Stack:** 0 | **DB + API:** 0

| Field Name | Database Type | API Schema Type | Seed Data | Status |
|------------|---------------|-----------------|-----------|---------|

---

*Generated on: 5 October 2025*
*Total Entities Analyzed: 12*