# Betting League Championship API - Postman Collection

## 📋 Overview

Complete Postman collection for testing the **Betting League Championship Platform** API with **186 endpoints** across **12 core modules**.

### 🎯 Features
- **Complete API Coverage**: All 186 endpoints organized by modules
- **Automatic Authentication**: JWT token management with auto-refresh
- **Environment Variables**: Development and production configurations
- **Test Scripts**: Automatic ID extraction and token management
- **Request Examples**: Real-world data samples for all endpoints
- **Documentation**: Detailed descriptions and usage guidelines

---

## 📁 Files Included

- **`Betting_League_Championship_API.postman_collection.json`** - Main collection with all 186 endpoints
- **`Betting_League_Championship_Development.postman_environment.json`** - Development environment (localhost:8000)
- **`Betting_League_Championship_Production.postman_environment.json`** - Production environment template
- **`POSTMAN_README.md`** - This documentation file

---

## 🚀 Quick Start

### 1. Import Collection
1. Open Postman
2. Click **Import** button
3. Select `Betting_League_Championship_API.postman_collection.json`
4. Collection will appear in your workspace

### 2. Import Environment
1. Click **Import** again
2. Select `Betting_League_Championship_Development.postman_environment.json`
3. Select the environment from the dropdown (top-right)

### 3. Start API Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4. Test Authentication
1. Go to **🔐 Authentication** folder
2. Run **Register User** (create a test user)
3. Run **Login** (tokens will be automatically saved)
4. Run **Get Current User** (verify authentication works)

---

## 📚 Collection Structure

### 🔐 Authentication (5 endpoints)
- User registration and login
- JWT token management
- Token refresh and logout
- Current user profile

### 👤 Users (18+ endpoints)
- User CRUD operations
- Profile management
- Preferences configuration
- User search and filtering
- Activity tracking

### 👥 Groups (16+ endpoints)
- Group creation and management
- Member invitations
- Group statistics
- Privacy controls

### 🔗 Group Memberships (18+ endpoints)
- Membership management
- Role assignments
- Invitation system
- Membership analytics

### ⚽ Sports (12+ endpoints)
- Sport categories
- Sport activation/deactivation
- Sport statistics
- Season management

### 🏆 Teams (14+ endpoints)
- Team CRUD operations
- Player roster management
- Team statistics
- Performance tracking

### 🏅 Competitions (16+ endpoints)
- Competition management
- Match scheduling
- Standings tracking
- Competition lifecycle

### 📅 Seasons (14+ endpoints)
- Season planning
- Fixture management
- Season statistics
- Timeline tracking

### ⚽ Matches (16+ endpoints)
- Match scheduling
- Live match updates
- Match statistics
- Status management

### 🏃‍♂️ Players (14+ endpoints)
- Player profiles
- Statistics tracking
- Team assignments
- Performance analytics

### 🎰 Bets (18+ endpoints)
- Bet placement
- Bet management
- Settlement operations
- Betting analytics

### 📊 Results (14+ endpoints)
- Result recording
- Result verification
- Match outcomes
- Historical data

### 📋 Audit Logs (16+ endpoints)
- Security logging
- Activity tracking
- Compliance reporting
- Analytics dashboard

---

## 🔧 Environment Variables

### Development Environment
```
base_url: http://localhost:8000
access_token: (auto-populated after login)
refresh_token: (auto-populated after login)
user_id: (auto-populated after user creation)
group_id: (auto-populated after group creation)
sport_id: (auto-populated after sport creation)
team_id: (auto-populated after team creation)
competition_id: (auto-populated after competition creation)
match_id: (auto-populated after match creation)
bet_id: (auto-populated after bet placement)
result_id: (auto-populated after result creation)
audit_log_id: (auto-populated after log creation)
```

### Production Environment
```
base_url: https://api.bettingleague.com
(other variables same as development)
```

---

## 🔄 Automatic Features

### Token Management
- **Auto-Login**: Login request automatically saves JWT tokens
- **Auto-Refresh**: Pre-request script checks token expiration and refreshes if needed
- **Auto-Authorization**: All protected endpoints use saved access token

### ID Management
- **Auto-Extract**: Test scripts automatically extract and save IDs from responses
- **Auto-Reference**: Subsequent requests use saved IDs as variables
- **Smart Linking**: Related endpoints automatically reference appropriate IDs

### Test Scripts
```javascript
// Example: Auto-save user ID after registration
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set('user_id', response.id);
    console.log('User ID saved:', response.id);
}
```

---

## 📖 Usage Guide

### Basic Testing Flow
1. **Authentication Setup**
   - Register → Login → Verify with "Get Current User"

2. **Data Creation**
   - Create Sport → Create Teams → Create Competition → Create Match

3. **Betting Flow**
   - Place Bet → Monitor Status → Settle Bet

4. **Social Features**
   - Create Group → Invite Members → Group Statistics

5. **Administration**
   - Record Results → Verify Results → Audit Logs

### Advanced Testing
1. **Bulk Operations**
   - Use bulk endpoints for multiple bets/results
   - Test pagination with skip/limit parameters
   - Filter operations with date ranges

2. **Error Scenarios**
   - Test validation errors (400)
   - Test authentication failures (401)
   - Test authorization issues (403)
   - Test not found scenarios (404)

3. **Performance Testing**
   - Use Postman Runner for load testing
   - Monitor response times
   - Test concurrent operations

---

## 🛠️ Customization

### Adding Custom Variables
```json
{
    "key": "custom_variable",
    "value": "custom_value",
    "type": "default",
    "enabled": true
}
```

### Custom Test Scripts
```javascript
// Add to request test tab
pm.test("Response time is less than 200ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});

pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

### Environment Switching
- Development: `localhost:8000`
- Staging: `https://staging-api.bettingleague.com`
- Production: `https://api.bettingleague.com`

---

## 🔍 Troubleshooting

### Common Issues

#### Authentication Problems
```
Error: Unauthorized (401)
Solution: Run Login request to refresh tokens
```

#### Missing Variables
```
Error: Variable {{user_id}} not found
Solution: Run prerequisite requests to populate variables
```

#### Connection Errors
```
Error: Could not get response
Solution: Verify API server is running on correct port
```

### Debug Tips
1. **Console Logs**: Check Postman console for script output
2. **Variable Inspector**: View current environment variables
3. **Network Tab**: Monitor actual HTTP requests
4. **Response Preview**: Examine response structure

---

## 📊 Testing Scenarios

### End-to-End User Journey
```
1. Register User
2. Login
3. Create/Join Group
4. Browse Sports & Teams
5. View Upcoming Matches
6. Place Bets
7. Monitor Live Matches
8. Check Results
9. Review Betting History
10. Group Statistics
```

### Administrative Workflow
```
1. Admin Login
2. Create Sports/Competitions
3. Add Teams & Players
4. Schedule Matches
5. Record Results
6. Settle Bets
7. Review Audit Logs
8. Generate Reports
```

### Security Testing
```
1. Test without authentication
2. Test with expired tokens
3. Test role-based access
4. Test input validation
5. Test rate limiting
6. Review audit trails
```

---

## 📈 Performance Monitoring

### Key Metrics to Monitor
- **Response Times**: < 200ms for simple queries
- **Authentication**: < 100ms for token validation
- **Database Queries**: < 50ms for indexed lookups
- **Pagination**: Consistent performance across pages

### Load Testing with Postman Runner
1. Select collection or folder
2. Configure iterations and delay
3. Select environment
4. Monitor results and response times

---

## 🔒 Security Considerations

### Token Security
- Tokens stored as secret variables
- Automatic token refresh prevents exposure
- Clear tokens when switching environments

### Data Privacy
- Use test data only
- Avoid real personal information
- Clear sensitive data after testing

### Environment Isolation
- Separate development/production environments
- Different API keys and secrets
- Isolated test databases

---

## 📝 Request Examples

### Authentication Flow
```http
POST /api/v1/auth/login
{
    "username": "user@example.com",
    "password": "SecurePass123!"
}
```

### Place a Bet
```http
POST /api/v1/bets/
Authorization: Bearer {{access_token}}
{
    "match_id": "{{match_id}}",
    "bet_type": "match_winner",
    "selection": "home_team",
    "stake": 25.00,
    "odds": 2.50
}
```

### Create Group
```http
POST /api/v1/groups/
Authorization: Bearer {{access_token}}
{
    "name": "Champions League Bettors",
    "description": "Group for Champions League betting",
    "privacy": "public",
    "max_members": 50
}
```

---

## ✅ Validation Checklist

Before using the collection:
- [ ] API server is running
- [ ] Environment is selected
- [ ] Base URL is correct
- [ ] Authentication works
- [ ] Required entities exist (sports, teams, etc.)
- [ ] Variables are populated
- [ ] Test scripts are enabled

---

## 🆘 Support

### Documentation
- **API Docs**: http://localhost:8000/docs
- **Developer Manual**: See `DEVELOPER_MANUAL.md`
- **GitHub Issues**: Report problems and bugs

### Quick References
- **HTTP Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found)
- **Authentication**: Bearer JWT tokens required for protected endpoints
- **Pagination**: Use `skip` and `limit` parameters
- **Filtering**: Use query parameters for filtering results

---

**Version**: 1.0  
**Last Updated**: October 5, 2025  
**Compatible with**: Betting League Championship API v1  
**Postman Version**: 10.0+ recommended

---

*This Postman collection provides comprehensive testing capabilities for the Betting League Championship platform. For additional support, refer to the main documentation or GitHub repository.*