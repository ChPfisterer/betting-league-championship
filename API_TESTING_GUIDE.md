# API Testing Guide - Updated Environment

## 🚀 Development Environment Status

**Environment**: ✅ RUNNING  
**API URL**: http://localhost:8000  
**API Docs**: http://localhost:8000/docs  
**Adminer**: http://localhost:8080  
**Keycloak**: http://localhost:8090  

## 🧪 Quick API Tests

### 1. Health Check
```bash
curl http://localhost:8000/docs -I
# Expected: HTTP/1.1 200 OK
```

### 2. API Info
```bash
curl http://localhost:8000/openapi.json | jq '.info'
# Expected: API title and version info
```

### 3. Authentication Test
```bash
# Register new user (will show validation if data invalid)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User",
    "date_of_birth": "1990-01-01T00:00:00Z"
  }'
```

### 4. Enum Validation Test
```bash
# Test invalid user status (should show enum validation)
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "invalid_status",
    "username": "testuser2",
    "email": "test2@example.com"
  }'
# Expected: Validation error showing valid enum options
```

## 📬 Postman Collection Updates

✅ **Updated Postman Collection**: `Betting_League_Championship_API.postman_collection.json`
- Added enum validation information
- Updated description with latest features
- Synchronized with current API endpoints

✅ **Environment Files Ready**:
- Development: `Betting_League_Championship_Development.postman_environment.json`
- Production: `Betting_League_Championship_Production.postman_environment.json`

## 🔧 Import Instructions

1. **Import Collection**: Import `Betting_League_Championship_API.postman_collection.json`
2. **Import Environment**: Import `Betting_League_Championship_Development.postman_environment.json`
3. **Select Environment**: Choose "Betting League Championship - Development"
4. **Test API**: Start with Authentication → Register User

## 🎯 Key Testing Areas

### Enum Validation Testing
- Test UserStatus enum: `pending`, `active`, `suspended`, `banned`, `deactivated`
- Test BetStatus enum: `pending`, `matched`, `settled`, `cancelled`, `void`, `won`, `lost`
- Test invalid enum values to see validation errors

### Field Architecture Testing
- 295 Database fields
- 502 API Schema fields  
- 25.1% field overlap (DB + API)
- Test field validation and type checking

### Authentication Flow
1. Register → Login → Get JWT token
2. Use JWT for protected endpoints
3. Test token refresh functionality

---

**Ready for Testing!** 🎉

Your development environment is now running with all the latest changes, including:
- ✅ Enhanced enum validation system
- ✅ Comprehensive field architecture  
- ✅ Updated Postman collections
- ✅ All 147 API endpoints available