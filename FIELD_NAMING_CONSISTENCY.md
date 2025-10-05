# 🔍 Field Naming Consistency Analysis
## Betting League Championship Platform

This document analyzes field naming consistency across the entire technology stack.

## 🔍 AuditLog Field Consistency Analysis
**Database Table:** `audit_logs`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `01T00` | ❌ | ✅ | ❌ | 🟡 Partial |
| `02T00` | ❌ | ✅ | ❌ | 🟡 Partial |
| `05T10` | ❌ | ✅ | ❌ | 🟡 Partial |
| `05T23` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `action_type` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `action_types` | ❌ | ✅ | ❌ | 🟡 Partial |
| `activity_timeline` | ❌ | ✅ | ❌ | 🟡 Partial |
| `additional_data` | ✅ | ❌ | ❌ | 🟡 Partial |
| `allowed_formats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `anomaly_detection` | ❌ | ✅ | ❌ | 🟡 Partial |
| `archive_action_types` | ❌ | ✅ | ❌ | 🟡 Partial |
| `archive_before` | ❌ | ✅ | ❌ | 🟡 Partial |
| `archive_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `archive_levels` | ❌ | ✅ | ❌ | 🟡 Partial |
| `archive_path` | ❌ | ✅ | ❌ | 🟡 Partial |
| `archive_size` | ❌ | ✅ | ❌ | 🟡 Partial |
| `archived_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `batch_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `changes` | ✅ | ❌ | ❌ | 🟡 Partial |
| `compliance_metrics` | ❌ | ✅ | ❌ | 🟡 Partial |
| `compress` | ❌ | ✅ | ❌ | 🟡 Partial |
| `context` | ❌ | ✅ | ❌ | 🟡 Partial |
| `correlation_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `created_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `date_from` | ❌ | ✅ | ❌ | 🟡 Partial |
| `date_to` | ❌ | ✅ | ❌ | 🟡 Partial |
| `details` | ❌ | ✅ | ❌ | 🟡 Partial |
| `device_info` | ✅ | ❌ | ❌ | 🟡 Partial |
| `entity` | ❌ | ✅ | ❌ | 🟡 Partial |
| `entity_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `entity_ids` | ❌ | ✅ | ❌ | 🟡 Partial |
| `entity_type` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `entity_types` | ❌ | ✅ | ❌ | 🟡 Partial |
| `error_rate` | ❌ | ✅ | ❌ | 🟡 Partial |
| `errors` | ❌ | ✅ | ❌ | 🟡 Partial |
| `expires_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `export_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `failed_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `failed_login_attempts` | ❌ | ✅ | ❌ | 🟡 Partial |
| `file_size` | ❌ | ✅ | ❌ | 🟡 Partial |
| `file_url` | ❌ | ✅ | ❌ | 🟡 Partial |
| `filters` | ❌ | ✅ | ❌ | 🟡 Partial |
| `flagged` | ✅ | ❌ | ❌ | 🟡 Partial |
| `format` | ❌ | ✅ | ❌ | 🟡 Partial |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `include_details` | ❌ | ✅ | ❌ | 🟡 Partial |
| `ip_address` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `ip_addresses` | ❌ | ✅ | ❌ | 🟡 Partial |
| `level` | ❌ | ✅ | ❌ | 🟡 Partial |
| `levels` | ❌ | ✅ | ❌ | 🟡 Partial |
| `location` | ✅ | ❌ | ❌ | 🟡 Partial |
| `log_level` | ✅ | ❌ | ❌ | 🟡 Partial |
| `logs` | ❌ | ✅ | ❌ | 🟡 Partial |
| `logs_by_action_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `logs_by_entity_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `logs_by_level` | ❌ | ✅ | ❌ | 🟡 Partial |
| `logs_by_source` | ❌ | ✅ | ❌ | 🟡 Partial |
| `message` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `metadata` | ❌ | ✅ | ❌ | 🟡 Partial |
| `new_values` | ✅ | ❌ | ❌ | 🟡 Partial |
| `notes` | ✅ | ❌ | ❌ | 🟡 Partial |
| `previous_values` | ✅ | ❌ | ❌ | 🟡 Partial |
| `processing_time` | ❌ | ✅ | ❌ | 🟡 Partial |
| `recent_errors` | ❌ | ✅ | ❌ | 🟡 Partial |
| `record_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `request_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `request_ids` | ❌ | ✅ | ❌ | 🟡 Partial |
| `retention_days` | ❌ | ✅ | ❌ | 🟡 Partial |
| `reviewed_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `reviewed_by` | ✅ | ❌ | ❌ | 🟡 Partial |
| `risk_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `search_query` | ❌ | ✅ | ❌ | 🟡 Partial |
| `security_events` | ❌ | ✅ | ❌ | 🟡 Partial |
| `session_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `session_ids` | ❌ | ✅ | ❌ | 🟡 Partial |
| `source` | ❌ | ✅ | ❌ | 🟡 Partial |
| `sources` | ❌ | ✅ | ❌ | 🟡 Partial |
| `status` | ❌ | ✅ | ❌ | 🟡 Partial |
| `suspicious_ips` | ❌ | ✅ | ❌ | 🟡 Partial |
| `system_health_indicators` | ❌ | ✅ | ❌ | 🟡 Partial |
| `tags` | ❌ | ✅ | ❌ | 🟡 Partial |
| `timestamp` | ✅ | ❌ | ❌ | 🟡 Partial |
| `top_ip_addresses` | ❌ | ✅ | ❌ | 🟡 Partial |
| `top_users` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_logs` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `user_activity_patterns` | ❌ | ✅ | ❌ | 🟡 Partial |
| `user_agent` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `user_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `user_ids` | ❌ | ✅ | ❌ | 🟡 Partial |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 11.7% (11/94 fields)

---

## 🔍 Bet Field Consistency Analysis
**Database Table:** `bets`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `01` | ❌ | ✅ | ❌ | 🟡 Partial |
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `MATCH_WINNER` | ❌ | ✅ | ❌ | 🟡 Partial |
| `Note` | ❌ | ✅ | ❌ | 🟡 Partial |
| `active_bettors` | ❌ | ✅ | ❌ | 🟡 Partial |
| `actual_payout` | ❌ | ✅ | ❌ | 🟡 Partial |
| `amount` | ❌ | ✅ | ❌ | 🟡 Partial |
| `average_bet_size` | ❌ | ✅ | ❌ | 🟡 Partial |
| `average_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `away_handicap_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `away_win_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `bet_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `bet_parameters` | ❌ | ✅ | ❌ | 🟡 Partial |
| `bet_type` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `bet_type_stats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `bonus_applied` | ✅ | ❌ | ❌ | 🟡 Partial |
| `bookmaker` | ❌ | ✅ | ❌ | 🟡 Partial |
| `both_teams_score_no` | ❌ | ✅ | ❌ | 🟡 Partial |
| `both_teams_score_yes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `commission` | ✅ | ❌ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `data` | ❌ | ✅ | ❌ | 🟡 Partial |
| `device_info` | ✅ | ❌ | ❌ | 🟡 Partial |
| `draw_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `entries` | ❌ | ✅ | ❌ | 🟡 Partial |
| `group_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `handicap` | ✅ | ❌ | ❌ | 🟡 Partial |
| `handicap_line` | ❌ | ✅ | ❌ | 🟡 Partial |
| `handicap_value` | ❌ | ✅ | ❌ | 🟡 Partial |
| `home_handicap_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `home_win_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `house_edge` | ❌ | ✅ | ❌ | 🟡 Partial |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `ip_address` | ✅ | ❌ | ❌ | 🟡 Partial |
| `is_active` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_over` | ❌ | ✅ | ❌ | 🟡 Partial |
| `last_updated` | ❌ | ✅ | ❌ | 🟡 Partial |
| `lost_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `market_type` | ✅ | ❌ | ❌ | 🟡 Partial |
| `match` | ❌ | ✅ | ❌ | 🟡 Partial |
| `match_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `max_liability` | ✅ | ❌ | ❌ | 🟡 Partial |
| `most_bet_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `notes` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `odds` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `outcome` | ❌ | ✅ | ❌ | 🟡 Partial |
| `over_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `payout_amount` | ✅ | ❌ | ❌ | 🟡 Partial |
| `pending_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `period` | ❌ | ✅ | ❌ | 🟡 Partial |
| `placed_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `popular_bet_types` | ❌ | ✅ | ❌ | 🟡 Partial |
| `potential_payout` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `potential_return` | ❌ | ✅ | ❌ | 🟡 Partial |
| `predicted_away_score` | ❌ | ✅ | ❌ | 🟡 Partial |
| `predicted_home_score` | ❌ | ✅ | ❌ | 🟡 Partial |
| `profit_loss` | ❌ | ✅ | ❌ | 🟡 Partial |
| `promotion_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `return_to_player` | ❌ | ✅ | ❌ | 🟡 Partial |
| `risk_category` | ✅ | ❌ | ❌ | 🟡 Partial |
| `selection` | ✅ | ❌ | ❌ | 🟡 Partial |
| `settled_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `settled_by` | ❌ | ✅ | ❌ | 🟡 Partial |
| `settlement_reason` | ❌ | ✅ | ❌ | 🟡 Partial |
| `slip_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `stake_amount` | ✅ | ❌ | ❌ | 🟡 Partial |
| `stats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `status` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `summary_stats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_amount` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_amount_wagered` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bets_placed` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_goals_line` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_payout` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_payouts` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_stake` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_value` | ❌ | ✅ | ❌ | 🟡 Partial |
| `under_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `user_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |
| `void_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `void_reason` | ✅ | ❌ | ❌ | 🟡 Partial |
| `win_rate` | ❌ | ✅ | ❌ | 🟡 Partial |
| `won_bets` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 13.6% (12/88 fields)

---

## 🔍 Competition Field Consistency Analysis
**Database Table:** `competitions`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `allow_betting` | ❌ | ✅ | ❌ | 🟡 Partial |
| `allow_public_betting` | ✅ | ❌ | ❌ | 🟡 Partial |
| `banner_url` | ✅ | ❌ | ❌ | 🟡 Partial |
| `betting_closes_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `competition_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `completed_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `created_by` | ✅ | ❌ | ❌ | 🟡 Partial |
| `days_remaining` | ❌ | ✅ | ❌ | 🟡 Partial |
| `description` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `end_date` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `entry_fee` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `format` | ❌ | ✅ | ❌ | 🟡 Partial |
| `format_type` | ✅ | ❌ | ❌ | 🟡 Partial |
| `group_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `http` | ❌ | ✅ | ❌ | 🟡 Partial |
| `https` | ❌ | ✅ | ❌ | 🟡 Partial |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `is_active` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_public` | ❌ | ✅ | ❌ | 🟡 Partial |
| `location` | ❌ | ✅ | ❌ | 🟡 Partial |
| `logo_url` | ✅ | ❌ | ❌ | 🟡 Partial |
| `max_participants` | ✅ | ❌ | ❌ | 🟡 Partial |
| `max_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `min_participants` | ✅ | ❌ | ❌ | 🟡 Partial |
| `min_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `participation_rate` | ❌ | ✅ | ❌ | 🟡 Partial |
| `pending_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `point_system` | ✅ | ❌ | ❌ | 🟡 Partial |
| `prize_distribution` | ✅ | ❌ | ❌ | 🟡 Partial |
| `prize_pool` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `registration_deadline` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `registration_notes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `registration_open` | ❌ | ✅ | ❌ | 🟡 Partial |
| `rules` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `season_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `slug` | ✅ | ❌ | ❌ | 🟡 Partial |
| `sport` | ❌ | ✅ | ❌ | 🟡 Partial |
| `sport_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `start_date` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `stats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `status` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `team_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bet_amount` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |
| `visibility` | ✅ | ❌ | ❌ | 🟡 Partial |
| `website` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 23.6% (13/55 fields)

---

## 🔍 Group Field Consistency Analysis
**Database Table:** `groups`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `0` | ❌ | ✅ | ❌ | 🟡 Partial |
| `01T00` | ❌ | ✅ | ❌ | 🟡 Partial |
| `05T14` | ❌ | ✅ | ❌ | 🟡 Partial |
| `10` | ❌ | ✅ | ❌ | 🟡 Partial |
| `100` | ❌ | ✅ | ❌ | 🟡 Partial |
| `1000` | ❌ | ✅ | ❌ | 🟡 Partial |
| `12T14` | ❌ | ✅ | ❌ | 🟡 Partial |
| `3` | ❌ | ✅ | ❌ | 🟡 Partial |
| `50` | ❌ | ✅ | ❌ | 🟡 Partial |
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `MEMBER` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `OWNER` | ❌ | ✅ | ❌ | 🟡 Partial |
| `active_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `active_members` | ❌ | ✅ | ❌ | 🟡 Partial |
| `allow_member_invites` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `approved` | ❌ | ✅ | ❌ | 🟡 Partial |
| `approved_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `approved_by` | ❌ | ✅ | ❌ | 🟡 Partial |
| `approved_by_user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `auto_approve_members` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `avatar_url` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `average_membership_duration` | ❌ | ✅ | ❌ | 🟡 Partial |
| `banner_url` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `changes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `confirmation` | ❌ | ✅ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `created_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `created_memberships` | ❌ | ✅ | ❌ | 🟡 Partial |
| `creator_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `default_role` | ❌ | ✅ | ❌ | 🟡 Partial |
| `description` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `email` | ❌ | ✅ | ❌ | 🟡 Partial |
| `entry_fee` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `error_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `errors` | ❌ | ✅ | ❌ | 🟡 Partial |
| `expires_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `group` | ❌ | ✅ | ❌ | 🟡 Partial |
| `group_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `https` | ❌ | ✅ | ❌ | 🟡 Partial |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `invitation_message` | ❌ | ✅ | ❌ | 🟡 Partial |
| `invitation_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `invited_by` | ❌ | ✅ | ❌ | 🟡 Partial |
| `invited_by_user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `invited_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_private` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `join_code` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `joined_after` | ❌ | ✅ | ❌ | 🟡 Partial |
| `joined_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `joined_before` | ❌ | ✅ | ❌ | 🟡 Partial |
| `last_updated` | ❌ | ✅ | ❌ | 🟡 Partial |
| `max_members` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `member_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `membership_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `memberships` | ❌ | ✅ | ❌ | 🟡 Partial |
| `message` | ❌ | ✅ | ❌ | 🟡 Partial |
| `name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `new_owner_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `notes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `pending_members` | ❌ | ✅ | ❌ | 🟡 Partial |
| `point_system` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `prize_pool` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `reason` | ❌ | ✅ | ❌ | 🟡 Partial |
| `recent_departures` | ❌ | ✅ | ❌ | 🟡 Partial |
| `recent_joins` | ❌ | ✅ | ❌ | 🟡 Partial |
| `role` | ❌ | ✅ | ❌ | 🟡 Partial |
| `role_distribution` | ❌ | ✅ | ❌ | 🟡 Partial |
| `rules_text` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `search_term` | ❌ | ✅ | ❌ | 🟡 Partial |
| `send_invitations` | ❌ | ✅ | ❌ | 🟡 Partial |
| `status` | ❌ | ✅ | ❌ | 🟡 Partial |
| `suspended_members` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_members` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_updates` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_winnings` | ❌ | ✅ | ❌ | 🟡 Partial |
| `transfer_ownership` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `user_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 20.7% (17/82 fields)

---

## 🔍 GroupMembership Field Consistency Analysis
**Database Table:** `group_memberships`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `0` | ❌ | ✅ | ❌ | 🟡 Partial |
| `01T00` | ❌ | ✅ | ❌ | 🟡 Partial |
| `05T14` | ❌ | ✅ | ❌ | 🟡 Partial |
| `12T14` | ❌ | ✅ | ❌ | 🟡 Partial |
| `50` | ❌ | ✅ | ❌ | 🟡 Partial |
| `MEMBER` | ❌ | ✅ | ❌ | 🟡 Partial |
| `OWNER` | ❌ | ✅ | ❌ | 🟡 Partial |
| `active_members` | ❌ | ✅ | ❌ | 🟡 Partial |
| `approved` | ❌ | ✅ | ❌ | 🟡 Partial |
| `approved_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `approved_by` | ❌ | ✅ | ❌ | 🟡 Partial |
| `approved_by_user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `average_membership_duration` | ❌ | ✅ | ❌ | 🟡 Partial |
| `ban_reason` | ✅ | ❌ | ❌ | 🟡 Partial |
| `banned_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `banned_by_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `changes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `confirmation` | ❌ | ✅ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `created_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `created_memberships` | ❌ | ✅ | ❌ | 🟡 Partial |
| `default_role` | ❌ | ✅ | ❌ | 🟡 Partial |
| `email` | ❌ | ✅ | ❌ | 🟡 Partial |
| `error_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `errors` | ❌ | ✅ | ❌ | 🟡 Partial |
| `expires_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `group` | ❌ | ✅ | ❌ | 🟡 Partial |
| `group_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `https` | ❌ | ✅ | ❌ | 🟡 Partial |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `invitation_message` | ❌ | ✅ | ❌ | 🟡 Partial |
| `invitation_sent_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `invitation_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `invited_by` | ❌ | ✅ | ❌ | 🟡 Partial |
| `invited_by_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `invited_by_user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `invited_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `joined_after` | ❌ | ✅ | ❌ | 🟡 Partial |
| `joined_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `joined_before` | ❌ | ✅ | ❌ | 🟡 Partial |
| `last_updated` | ❌ | ✅ | ❌ | 🟡 Partial |
| `left_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `membership_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `memberships` | ❌ | ✅ | ❌ | 🟡 Partial |
| `message` | ❌ | ✅ | ❌ | 🟡 Partial |
| `new_owner_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `notes` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `pending_members` | ❌ | ✅ | ❌ | 🟡 Partial |
| `reason` | ❌ | ✅ | ❌ | 🟡 Partial |
| `recent_departures` | ❌ | ✅ | ❌ | 🟡 Partial |
| `recent_joins` | ❌ | ✅ | ❌ | 🟡 Partial |
| `role` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `role_distribution` | ❌ | ✅ | ❌ | 🟡 Partial |
| `search_term` | ❌ | ✅ | ❌ | 🟡 Partial |
| `send_invitations` | ❌ | ✅ | ❌ | 🟡 Partial |
| `status` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `suspended_members` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_members` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_updates` | ❌ | ✅ | ❌ | 🟡 Partial |
| `transfer_ownership` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `user_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 14.1% (9/64 fields)

---

## 🔍 Match Field Consistency Analysis
**Database Table:** `matches`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `allow_betting` | ❌ | ✅ | ❌ | 🟡 Partial |
| `attendance` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `away_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `away_score` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `away_team` | ❌ | ✅ | ❌ | 🟡 Partial |
| `away_team_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `away_team_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `betting_closes_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `competition` | ❌ | ✅ | ❌ | 🟡 Partial |
| `competition_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `confidence` | ❌ | ✅ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `data` | ❌ | ✅ | ❌ | 🟡 Partial |
| `description` | ❌ | ✅ | ❌ | 🟡 Partial |
| `draw_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `draw_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `duration_minutes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `event_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `events` | ❌ | ✅ | ❌ | 🟡 Partial |
| `extra_time_away_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `extra_time_home_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `finished_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `home_odds` | ❌ | ✅ | ❌ | 🟡 Partial |
| `home_score` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `home_team` | ❌ | ✅ | ❌ | 🟡 Partial |
| `home_team_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `home_team_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `is_active` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_draw` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_final` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_home_game` | ❌ | ✅ | ❌ | 🟡 Partial |
| `last_updated` | ❌ | ✅ | ❌ | 🟡 Partial |
| `live_odds` | ✅ | ❌ | ❌ | 🟡 Partial |
| `match_day` | ✅ | ❌ | ❌ | 🟡 Partial |
| `match_events` | ✅ | ❌ | ❌ | 🟡 Partial |
| `match_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `match_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `minute` | ❌ | ✅ | ❌ | 🟡 Partial |
| `notes` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `penalties_away_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `penalties_home_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `period` | ❌ | ✅ | ❌ | 🟡 Partial |
| `player_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `predicted_away_score` | ❌ | ✅ | ❌ | 🟡 Partial |
| `predicted_home_score` | ❌ | ✅ | ❌ | 🟡 Partial |
| `predicted_winner` | ❌ | ✅ | ❌ | 🟡 Partial |
| `referee` | ✅ | ❌ | ❌ | 🟡 Partial |
| `round_number` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `scheduled_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `season_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `sport` | ❌ | ✅ | ❌ | 🟡 Partial |
| `started_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `stats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `status` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `status_reason` | ❌ | ✅ | ❌ | 🟡 Partial |
| `team_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bet_amount` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `tv_viewers` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |
| `venue` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `venue_city` | ❌ | ✅ | ❌ | 🟡 Partial |
| `venue_country` | ❌ | ✅ | ❌ | 🟡 Partial |
| `venue_name` | ❌ | ✅ | ❌ | 🟡 Partial |
| `verified` | ❌ | ✅ | ❌ | 🟡 Partial |
| `weather_conditions` | ✅ | ❌ | ❌ | 🟡 Partial |
| `week_number` | ❌ | ✅ | ❌ | 🟡 Partial |
| `winner_team_id` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 23.9% (17/71 fields)

---

## 🔍 Player Field Consistency Analysis
**Database Table:** `players`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `60` | ❌ | ✅ | ❌ | 🟡 Partial |
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `age_max` | ❌ | ✅ | ❌ | 🟡 Partial |
| `age_min` | ❌ | ✅ | ❌ | 🟡 Partial |
| `agent_contact` | ✅ | ❌ | ❌ | 🟡 Partial |
| `agent_name` | ✅ | ❌ | ❌ | 🟡 Partial |
| `assists` | ❌ | ✅ | ❌ | 🟡 Partial |
| `biography` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `contract_end` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `contract_history` | ❌ | ✅ | ❌ | 🟡 Partial |
| `contract_start` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `current_team_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `data` | ❌ | ✅ | ❌ | 🟡 Partial |
| `date_of_birth` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `description` | ❌ | ✅ | ❌ | 🟡 Partial |
| `detailed_stats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `display_name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `expected_return` | ❌ | ✅ | ❌ | 🟡 Partial |
| `first_name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `from_team_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `goals_scored` | ❌ | ✅ | ❌ | 🟡 Partial |
| `height_cm` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `injury_date` | ❌ | ✅ | ❌ | 🟡 Partial |
| `injury_status` | ✅ | ❌ | ❌ | 🟡 Partial |
| `injury_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_active` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `is_captain` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_resolved` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_vice_captain` | ❌ | ✅ | ❌ | 🟡 Partial |
| `jersey_number` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `last_name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `last_updated` | ❌ | ✅ | ❌ | 🟡 Partial |
| `market_value` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `market_value_max` | ❌ | ✅ | ❌ | 🟡 Partial |
| `market_value_min` | ❌ | ✅ | ❌ | 🟡 Partial |
| `match_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `matches_played` | ❌ | ✅ | ❌ | 🟡 Partial |
| `matches_started` | ❌ | ✅ | ❌ | 🟡 Partial |
| `middle_name` | ✅ | ❌ | ❌ | 🟡 Partial |
| `minutes_played` | ❌ | ✅ | ❌ | 🟡 Partial |
| `nationality` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `nickname` | ✅ | ❌ | ❌ | 🟡 Partial |
| `notes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `photo_url` | ❌ | ✅ | ❌ | 🟡 Partial |
| `player_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `position` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `preferred_foot` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `profile_image_url` | ✅ | ❌ | ❌ | 🟡 Partial |
| `rating` | ❌ | ✅ | ❌ | 🟡 Partial |
| `rating_source` | ❌ | ✅ | ❌ | 🟡 Partial |
| `red_cards` | ❌ | ✅ | ❌ | 🟡 Partial |
| `retirement_date` | ✅ | ❌ | ❌ | 🟡 Partial |
| `salary` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `season_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `secondary_positions` | ❌ | ✅ | ❌ | 🟡 Partial |
| `severity` | ❌ | ✅ | ❌ | 🟡 Partial |
| `social_media` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `sport_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `stats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `status` | ❌ | ✅ | ❌ | 🟡 Partial |
| `team` | ❌ | ✅ | ❌ | 🟡 Partial |
| `team_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `to_team_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `transfer_date` | ❌ | ✅ | ❌ | 🟡 Partial |
| `transfer_fee` | ❌ | ✅ | ❌ | 🟡 Partial |
| `transfer_history` | ❌ | ✅ | ❌ | 🟡 Partial |
| `transfer_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |
| `weight_kg` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `yellow_cards` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 27.0% (20/74 fields)

---

## 🔍 Result Field Consistency Analysis
**Database Table:** `results`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `0` | ❌ | ✅ | ❌ | 🟡 Partial |
| `05T14` | ❌ | ✅ | ❌ | 🟡 Partial |
| `05T15` | ❌ | ✅ | ❌ | 🟡 Partial |
| `100` | ❌ | ✅ | ❌ | 🟡 Partial |
| `45` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `additional_data` | ❌ | ✅ | ❌ | 🟡 Partial |
| `allowed_priorities` | ❌ | ✅ | ❌ | 🟡 Partial |
| `average_goals_per_match` | ❌ | ✅ | ❌ | 🟡 Partial |
| `away_score` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `away_win_percentage` | ❌ | ✅ | ❌ | 🟡 Partial |
| `away_wins` | ❌ | ✅ | ❌ | 🟡 Partial |
| `both_teams_scored` | ❌ | ✅ | ❌ | 🟡 Partial |
| `both_teams_scored_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `changes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `clean_sheet` | ❌ | ✅ | ❌ | 🟡 Partial |
| `clean_sheets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `confirmation_notes` | ❌ | ✅ | ❌ | 🟡 Partial |
| `confirmed` | ❌ | ✅ | ❌ | 🟡 Partial |
| `confirmed_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `confirmed_results` | ❌ | ✅ | ❌ | 🟡 Partial |
| `corners_away` | ✅ | ❌ | ❌ | 🟡 Partial |
| `corners_home` | ✅ | ❌ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `created_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `created_results` | ❌ | ✅ | ❌ | 🟡 Partial |
| `dispute_reason` | ❌ | ✅ | ❌ | 🟡 Partial |
| `disputed_by` | ❌ | ✅ | ❌ | 🟡 Partial |
| `disputed_results` | ❌ | ✅ | ❌ | 🟡 Partial |
| `draw_percentage` | ❌ | ✅ | ❌ | 🟡 Partial |
| `draws` | ❌ | ✅ | ❌ | 🟡 Partial |
| `error_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `errors` | ❌ | ✅ | ❌ | 🟡 Partial |
| `evidence` | ❌ | ✅ | ❌ | 🟡 Partial |
| `extra_time_away_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `extra_time_home_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `finished_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `first_recorded` | ❌ | ✅ | ❌ | 🟡 Partial |
| `half_time_away_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `half_time_home_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `highest_scoring_match` | ❌ | ✅ | ❌ | 🟡 Partial |
| `home_score` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `home_win_percentage` | ❌ | ✅ | ❌ | 🟡 Partial |
| `home_wins` | ❌ | ✅ | ❌ | 🟡 Partial |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `is_official` | ✅ | ❌ | ❌ | 🟡 Partial |
| `is_valid` | ❌ | ✅ | ❌ | 🟡 Partial |
| `last_updated` | ❌ | ✅ | ❌ | 🟡 Partial |
| `match` | ❌ | ✅ | ❌ | 🟡 Partial |
| `match_events` | ✅ | ❌ | ❌ | 🟡 Partial |
| `match_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `match_result` | ❌ | ✅ | ❌ | 🟡 Partial |
| `most_goals_by_team` | ❌ | ✅ | ❌ | 🟡 Partial |
| `notes` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `outcome_data` | ❌ | ✅ | ❌ | 🟡 Partial |
| `override_validation` | ❌ | ✅ | ❌ | 🟡 Partial |
| `penalty_away_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `penalty_home_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `pending_results` | ❌ | ✅ | ❌ | 🟡 Partial |
| `period_end` | ❌ | ✅ | ❌ | 🟡 Partial |
| `period_start` | ❌ | ✅ | ❌ | 🟡 Partial |
| `possession_away` | ✅ | ❌ | ❌ | 🟡 Partial |
| `possession_home` | ✅ | ❌ | ❌ | 🟡 Partial |
| `priority` | ❌ | ✅ | ❌ | 🟡 Partial |
| `recorded_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `recorded_by` | ❌ | ✅ | ❌ | 🟡 Partial |
| `recorded_by_user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `red_cards_away` | ✅ | ❌ | ❌ | 🟡 Partial |
| `red_cards_home` | ✅ | ❌ | ❌ | 🟡 Partial |
| `result_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `result_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `results` | ❌ | ✅ | ❌ | 🟡 Partial |
| `shots_away` | ✅ | ❌ | ❌ | 🟡 Partial |
| `shots_home` | ✅ | ❌ | ❌ | 🟡 Partial |
| `skip_duplicates` | ❌ | ✅ | ❌ | 🟡 Partial |
| `skipped_count` | ❌ | ✅ | ❌ | 🟡 Partial |
| `started_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `statistics` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `status` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `suggested_corrections` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_goals` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_results` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_updates` | ❌ | ✅ | ❌ | 🟡 Partial |
| `try` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `validate_all` | ❌ | ✅ | ❌ | 🟡 Partial |
| `validation_errors` | ❌ | ✅ | ❌ | 🟡 Partial |
| `validation_warnings` | ❌ | ✅ | ❌ | 🟡 Partial |
| `verified_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `verified_by` | ✅ | ❌ | ❌ | 🟡 Partial |
| `winner_team_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `yellow_cards_away` | ✅ | ❌ | ❌ | 🟡 Partial |
| `yellow_cards_home` | ✅ | ❌ | ❌ | 🟡 Partial |

**Consistency Rate:** 8.5% (8/94 fields)

---

## 🔍 Season Field Consistency Analysis
**Database Table:** `seasons`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `allow_betting` | ❌ | ✅ | ❌ | 🟡 Partial |
| `allow_draws` | ❌ | ✅ | ❌ | 🟡 Partial |
| `average_goals_per_match` | ❌ | ✅ | ❌ | 🟡 Partial |
| `competitions` | ❌ | ✅ | ❌ | 🟡 Partial |
| `completed_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `days_remaining` | ❌ | ✅ | ❌ | 🟡 Partial |
| `description` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `end_date` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `is_active` | ❌ | ✅ | ❌ | 🟡 Partial |
| `is_current` | ✅ | ❌ | ❌ | 🟡 Partial |
| `is_public` | ❌ | ✅ | ❌ | 🟡 Partial |
| `last_updated` | ❌ | ✅ | ❌ | 🟡 Partial |
| `max_competitions` | ✅ | ❌ | ❌ | 🟡 Partial |
| `max_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `min_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `pending_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `playoff_format` | ✅ | ❌ | ❌ | 🟡 Partial |
| `playoff_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `point_system` | ✅ | ❌ | ❌ | 🟡 Partial |
| `points_for_draw` | ❌ | ✅ | ❌ | 🟡 Partial |
| `points_for_loss` | ❌ | ✅ | ❌ | 🟡 Partial |
| `points_for_win` | ❌ | ✅ | ❌ | 🟡 Partial |
| `prize_pool_total` | ✅ | ❌ | ❌ | 🟡 Partial |
| `progress_percentage` | ❌ | ✅ | ❌ | 🟡 Partial |
| `promotion_rules` | ✅ | ❌ | ❌ | 🟡 Partial |
| `promotion_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `registration_end` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `registration_start` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `relegation_rules` | ✅ | ❌ | ❌ | 🟡 Partial |
| `relegation_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `rules` | ✅ | ❌ | ❌ | 🟡 Partial |
| `season_format` | ✅ | ❌ | ❌ | 🟡 Partial |
| `season_id` | ❌ | ✅ | ❌ | 🟡 Partial |
| `season_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `slug` | ✅ | ❌ | ❌ | 🟡 Partial |
| `sport_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `standings` | ❌ | ✅ | ❌ | 🟡 Partial |
| `start_date` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `stats` | ❌ | ✅ | ❌ | 🟡 Partial |
| `status` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `tie_breaker_rules` | ✅ | ❌ | ❌ | 🟡 Partial |
| `total_bet_amount` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_competitions` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |
| `year` | ✅ | ✅ | ❌ | 🟢 Consistent |

**Consistency Rate:** 22.2% (12/54 fields)

---

## 🔍 Sport Field Consistency Analysis
**Database Table:** `sports`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `100` | ❌ | ✅ | ❌ | 🟡 Partial |
| `1000` | ❌ | ✅ | ❌ | 🟡 Partial |
| `2` | ❌ | ✅ | ❌ | 🟡 Partial |
| `5000` | ❌ | ✅ | ❌ | 🟡 Partial |
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `active_competitions` | ❌ | ✅ | ❌ | 🟡 Partial |
| `category` | ✅ | ❌ | ❌ | 🟡 Partial |
| `color_scheme` | ✅ | ❌ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `default_bet_types` | ✅ | ❌ | ❌ | 🟡 Partial |
| `description` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `icon_url` | ✅ | ❌ | ❌ | 🟡 Partial |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `is_active` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `match_duration` | ✅ | ❌ | ❌ | 🟡 Partial |
| `name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `popularity_score` | ✅ | ❌ | ❌ | 🟡 Partial |
| `rules` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `scoring_system` | ✅ | ❌ | ❌ | 🟡 Partial |
| `season_structure` | ✅ | ❌ | ❌ | 🟡 Partial |
| `slug` | ✅ | ❌ | ❌ | 🟡 Partial |
| `total_competitions` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_teams` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |

**Consistency Rate:** 26.9% (7/26 fields)

---

## 🔍 Team Field Consistency Analysis
**Database Table:** `teams`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `10` | ❌ | ✅ | ❌ | 🟡 Partial |
| `100` | ❌ | ✅ | ❌ | 🟡 Partial |
| `2` | ❌ | ✅ | ❌ | 🟡 Partial |
| `500` | ❌ | ✅ | ❌ | 🟡 Partial |
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `banner_url` | ✅ | ❌ | ❌ | 🟡 Partial |
| `captain_id` | ✅ | ❌ | ❌ | 🟡 Partial |
| `city` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `coach_name` | ✅ | ❌ | ❌ | 🟡 Partial |
| `country` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `current_league` | ✅ | ❌ | ❌ | 🟡 Partial |
| `description` | ✅ | ❌ | ❌ | 🟡 Partial |
| `draws` | ❌ | ✅ | ❌ | 🟡 Partial |
| `founded_year` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `home_venue` | ✅ | ❌ | ❌ | 🟡 Partial |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `is_active` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `league_position` | ✅ | ❌ | ❌ | 🟡 Partial |
| `logo_url` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `losses` | ❌ | ✅ | ❌ | 🟡 Partial |
| `max_players` | ✅ | ❌ | ❌ | 🟡 Partial |
| `name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `primary_color` | ✅ | ❌ | ❌ | 🟡 Partial |
| `secondary_color` | ✅ | ❌ | ❌ | 🟡 Partial |
| `short_name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `slug` | ✅ | ❌ | ❌ | 🟡 Partial |
| `social_links` | ✅ | ❌ | ❌ | 🟡 Partial |
| `sport_id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `sport_name` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_matches` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `v` | ❌ | ✅ | ❌ | 🟡 Partial |
| `website` | ✅ | ❌ | ❌ | 🟡 Partial |
| `website_url` | ❌ | ✅ | ❌ | 🟡 Partial |
| `win_percentage` | ❌ | ✅ | ❌ | 🟡 Partial |
| `wins` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 28.9% (11/38 fields)

---

## 🔍 User Field Consistency Analysis
**Database Table:** `users`

| Field Name | Database Model | API Schema | Seed Data | Status |
|------------|----------------|------------|-----------|---------|
| `100` | ❌ | ✅ | ❌ | 🟡 Partial |
| `128` | ❌ | ✅ | ❌ | 🟡 Partial |
| `3` | ❌ | ✅ | ❌ | 🟡 Partial |
| `50` | ❌ | ✅ | ❌ | 🟡 Partial |
| `8` | ❌ | ✅ | ❌ | 🟡 Partial |
| `Config` | ❌ | ✅ | ❌ | 🟡 Partial |
| `None` | ❌ | ✅ | ❌ | 🟡 Partial |
| `access_token` | ❌ | ✅ | ❌ | 🟡 Partial |
| `audit_logs` | ✅ | ❌ | ❌ | 🟡 Partial |
| `avatar_url` | ✅ | ❌ | ❌ | 🟡 Partial |
| `biography` | ✅ | ❌ | ❌ | 🟡 Partial |
| `created_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `currency` | ✅ | ❌ | ❌ | 🟡 Partial |
| `current_password` | ❌ | ✅ | ❌ | 🟡 Partial |
| `date_of_birth` | ✅ | ❌ | ❌ | 🟡 Partial |
| `deleted_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `display_name` | ✅ | ❌ | ❌ | 🟡 Partial |
| `email` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `email_verified` | ✅ | ❌ | ❌ | 🟡 Partial |
| `expires_in` | ❌ | ✅ | ❌ | 🟡 Partial |
| `failed_login_attempts` | ✅ | ❌ | ❌ | 🟡 Partial |
| `first_name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `id` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `is_active` | ✅ | ❌ | ❌ | 🟡 Partial |
| `is_verified` | ✅ | ❌ | ❌ | 🟡 Partial |
| `kyc_status` | ✅ | ❌ | ❌ | 🟡 Partial |
| `kyc_verified_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `language` | ✅ | ❌ | ❌ | 🟡 Partial |
| `last_login` | ✅ | ❌ | ❌ | 🟡 Partial |
| `last_login_at` | ❌ | ✅ | ❌ | 🟡 Partial |
| `last_login_ip` | ✅ | ❌ | ❌ | 🟡 Partial |
| `last_name` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `locked_until` | ✅ | ❌ | ❌ | 🟡 Partial |
| `marketing_consent` | ✅ | ❌ | ❌ | 🟡 Partial |
| `new_password` | ❌ | ✅ | ❌ | 🟡 Partial |
| `notifications_enabled` | ✅ | ❌ | ❌ | 🟡 Partial |
| `password` | ❌ | ✅ | ❌ | 🟡 Partial |
| `password_changed_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `password_hash` | ✅ | ❌ | ❌ | 🟡 Partial |
| `phone_number` | ✅ | ❌ | ❌ | 🟡 Partial |
| `phone_verified` | ✅ | ❌ | ❌ | 🟡 Partial |
| `privacy_policy_accepted` | ✅ | ❌ | ❌ | 🟡 Partial |
| `role` | ✅ | ❌ | ❌ | 🟡 Partial |
| `status` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `terms_accepted` | ✅ | ❌ | ❌ | 🟡 Partial |
| `terms_accepted_at` | ✅ | ❌ | ❌ | 🟡 Partial |
| `timezone` | ✅ | ❌ | ❌ | 🟡 Partial |
| `token_type` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_bets` | ❌ | ✅ | ❌ | 🟡 Partial |
| `total_winnings` | ❌ | ✅ | ❌ | 🟡 Partial |
| `updated_at` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `user` | ❌ | ✅ | ❌ | 🟡 Partial |
| `username` | ✅ | ✅ | ❌ | 🟢 Consistent |
| `website_url` | ✅ | ❌ | ❌ | 🟡 Partial |
| `win_rate` | ❌ | ✅ | ❌ | 🟡 Partial |

**Consistency Rate:** 14.5% (8/55 fields)

---

*Generated on: 5 October 2025*
*Total Entities Analyzed: 12*
