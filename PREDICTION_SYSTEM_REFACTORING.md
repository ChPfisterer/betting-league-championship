# Prediction System Refactoring Summary

## Overview

The betting system has been refactored from a traditional sports betting platform to a specification-compliant prediction contest system. This document summarizes the changes made to align with the original specification requirements.

## Key Changes Made

### 1. **Database Schema Migration** (`backend/migrate_bet_model.py`)

**Added Fields:**
- `group_id UUID` - Links predictions to specific groups (FOREIGN KEY to groups table)
- `predicted_winner VARCHAR(10)` - User's winner prediction (HOME/AWAY/DRAW)  
- `predicted_home_score INTEGER` - User's predicted home team score
- `predicted_away_score INTEGER` - User's predicted away team score
- `points_earned INTEGER` - Points earned from prediction (0, 1, or 3)
- `is_processed BOOLEAN` - Whether prediction has been scored

**Constraints Added:**
- Check constraint for `predicted_winner` values (HOME, AWAY, DRAW)
- Check constraint for non-negative predicted scores
- Foreign key constraint linking `group_id` to groups table

**Legacy Fields Retained:**
- Financial fields (`stake_amount`, `odds`, `potential_payout`) are kept for backward compatibility but set to default values
- Original `bet_type` and `market_type` fields are reused for the new prediction system

### 2. **New API Schemas** (`backend/src/api/schemas/prediction.py`)

**Core Models:**
- `PredictionBase` - Base prediction data (match_id, group_id, winner, scores)
- `PredictionCreate` - Request schema for creating predictions
- `PredictionUpdate` - Request schema for updating predictions  
- `PredictionResponse` - Response schema with points and processing status
- `UserPredictionStats` - User statistics (total points, win rate, etc.)

**Enums:**
- `PredictedWinner` - HOME, AWAY, DRAW values
- `PredictionStatus` - pending, processed status values

### 3. **Prediction Service Logic** (`backend/src/services/prediction_service.py`)

**Specification-Compliant Scoring:**
- **3 points total** for exact score match (winner + exact final score)
- **1 point** for correct winner prediction only
- **0 points** for incorrect predictions

**Business Logic:**
- Deadline enforcement (default: 1 hour before match start)
- Group membership validation
- Prediction updates allowed before deadline
- Batch processing of match predictions after results are available

**Key Methods:**
- `create_prediction()` - Create/update predictions with validation
- `process_match_predictions()` - Award points after match completion
- `get_group_leaderboard()` - Ranked leaderboard with tiebreaker rules
- `get_user_stats()` - Comprehensive user prediction statistics

### 4. **New API Endpoints** (`backend/src/api/v1/endpoints/predictions.py`)

**Endpoints Added:**
- `POST /predictions/` - Create new prediction
- `GET /predictions/my-predictions` - Get user's predictions
- `GET /predictions/stats/user` - Get user prediction statistics
- `GET /predictions/leaderboard/{group_id}` - Get group leaderboard
- `POST /predictions/process-match/{match_id}` - Process completed match (admin)

**Authentication:** All endpoints use `get_current_user_hybrid` for Keycloak OAuth integration

### 5. **Router Integration** (`backend/src/api/v1/__init__.py`)

- Added prediction router to main API router
- Prediction endpoints available at `/api/v1/predictions/*`
- Tagged as "Predictions" in OpenAPI documentation

## Specification Compliance

### ✅ **Implemented Requirements**

1. **Points-Based Scoring System**
   - 1 point for correct winner prediction ✅
   - 3 points total for exact score match ✅
   - 0 points for incorrect predictions ✅

2. **Group-Based Predictions**
   - Predictions linked to specific groups ✅
   - Group leaderboards with proper ranking ✅
   - Group membership context ✅

3. **Prediction Types**
   - Winner prediction (HOME/AWAY/DRAW) ✅
   - Exact final score prediction ✅
   - Combined scoring logic ✅

4. **Deadline Management**
   - Default 1-hour deadline before match start ✅
   - Deadline validation for new predictions ✅
   - Prediction updates allowed before deadline ✅

### 🔄 **Partially Implemented**

1. **Group Membership Validation**
   - Service method exists but returns `True` for all users
   - Requires implementation of GroupMembership model validation

2. **Admin-Configurable Deadlines**
   - Basic deadline logic implemented
   - Group-specific deadline overrides not yet implemented

3. **Batch Match Processing**
   - Core logic implemented in service
   - Automated processing triggers not implemented (currently manual endpoint)

### ❌ **Removed from Legacy System**

1. **Financial Elements**
   - No stake amounts or real money involved ✅
   - No odds calculations ✅
   - No payout processing ✅
   - No commission tracking ✅

2. **Complex Market Types**
   - Simplified from multiple market types to simple winner+score predictions ✅
   - Removed handicap, over/under, and other complex betting markets ✅

## Database Migration Instructions

### Prerequisites
1. **Backup your database** before running migration
2. Ensure no active betting operations during migration
3. Test migration on development environment first

### Running the Migration

```bash
# From backend directory
cd backend

# Run the migration script
python migrate_bet_model.py
```

### Migration Results
- Existing bet records will have new fields added with NULL values
- No data loss occurs - all existing data is preserved
- New predictions will use the spec-compliant fields
- Legacy betting functionality remains available but deprecated

## Testing

### Test Coverage (`backend/tests/test_predictions.py`)

**Unit Tests:**
- Points calculation logic for all scenarios
- Winner determination from match scores
- Deadline validation logic

**Integration Tests:**
- Full prediction creation flow
- Match processing and points awarding
- Group leaderboard generation

**API Tests:**
- All prediction endpoints
- Authentication integration
- Error handling scenarios

### Running Tests

```bash
# From backend directory
cd backend
pytest tests/test_predictions.py -v
```

## Next Steps

### Immediate Tasks
1. **Complete Group Membership Validation**
   - Implement proper group membership checking
   - Add group admin authorization for deadline changes

2. **Frontend Integration**
   - Update Angular components to use prediction endpoints
   - Remove odds/money-related UI elements
   - Implement points-based leaderboard display

3. **Automated Processing**
   - Set up automated match result processing
   - Implement scheduled points calculation
   - Add notification system for completed matches

### Future Enhancements
1. **Advanced Statistics**
   - Historical prediction accuracy trends
   - Head-to-head user comparisons
   - Seasonal/tournament statistics

2. **Enhanced Deadline Management**
   - Group-specific deadline configuration
   - Deadline change notifications
   - Timezone-aware deadline handling

3. **Improved User Experience**
   - Prediction confidence levels
   - Match prediction suggestions based on history
   - Social features (prediction sharing, group chat)

## API Documentation

The new prediction endpoints are automatically documented in the FastAPI OpenAPI schema:
- **Development:** http://localhost:8000/docs
- **Production:** Check deployment documentation for URL

All endpoints require valid Keycloak authentication tokens and follow the existing authentication patterns established in the platform.

## Compatibility Notes

- **Backward Compatibility:** Existing bet model fields are preserved
- **Legacy Endpoints:** Traditional betting endpoints still function but are deprecated
- **Database:** No breaking changes to existing table structure
- **Authentication:** Uses existing Keycloak integration without changes

This refactoring successfully transforms the platform from a traditional sports betting system to a simple, engaging prediction contest that aligns with the original specification while maintaining data integrity and system stability.