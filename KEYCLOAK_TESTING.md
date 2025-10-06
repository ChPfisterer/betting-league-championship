# Keycloak OAuth 2.0 Integration Testing Guide

## ✅ Quick Status Check

All OAuth endpoints are functional and accessible:

```bash
# Test Authorization URL Generation
curl -s "http://localhost:8000/api/v1/auth/keycloak/oauth/authorize-url?redirect_uri=http://localhost:4200/auth/callback" | jq .

# Expected: Authorization URL with state parameter
```

## 🔄 Complete OAuth Flow Testing

### Step 1: Get Authorization URL
```bash
AUTH_RESPONSE=$(curl -s "http://localhost:8000/api/v1/auth/keycloak/oauth/authorize-url?redirect_uri=http://localhost:4200/auth/callback")
echo $AUTH_RESPONSE | jq .

# Extract the authorization URL and state
AUTH_URL=$(echo $AUTH_RESPONSE | jq -r '.authorize_url')
STATE=$(echo $AUTH_RESPONSE | jq -r '.state')

echo "Authorization URL: $AUTH_URL"
echo "State: $STATE"
```

### Step 2: Manual Browser Login
1. Open the authorization URL in a browser
2. Login with Keycloak credentials (from realm configuration):
   - **Admin**: `admin` / `admin123` 
   - **Test User**: `testuser` / `test123`
   - **Moderator**: `moderator` / `mod123`
3. After successful login, you'll be redirected to: 
   `http://localhost:4200/auth/callback?code=AUTHORIZATION_CODE&state=STATE_VALUE`
4. Copy the `code` parameter from the URL

### Step 3: Exchange Authorization Code for Token
```bash
# Replace AUTHORIZATION_CODE with the actual code from step 2
# Replace STATE_VALUE with the state from step 1
curl -X POST http://localhost:8000/api/v1/auth/keycloak/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "code": "AUTHORIZATION_CODE",
    "redirect_uri": "http://localhost:4200/auth/callback",
    "state": "STATE_VALUE"
  }' | jq .
```

### Step 4: Test User Info with Token
```bash
# Replace YOUR_ACCESS_TOKEN with the actual token from step 3
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/v1/auth/keycloak/user/info | jq .
```

### Step 5: Test Token Refresh
```bash
# Replace YOUR_REFRESH_TOKEN with refresh token from step 3
curl -X POST http://localhost:8000/api/v1/auth/keycloak/oauth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }' | jq .
```

### Step 6: Test Logout
```bash
# Replace YOUR_REFRESH_TOKEN with refresh token
curl -X POST http://localhost:8000/api/v1/auth/keycloak/oauth/logout \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }' | jq .
```

## 🎯 Available Endpoints

All endpoints are under `/api/v1/auth/keycloak/`:

- `GET /oauth/authorize-url` - Generate authorization URL
- `POST /oauth/token` - Exchange code for tokens
- `POST /oauth/refresh` - Refresh access token
- `POST /oauth/logout` - Logout and revoke tokens
- `GET /user/info` - Get user information (requires Bearer token)

## 🔧 Environment Configuration

Current configuration:
- **Keycloak External URL**: `http://localhost:8090` (for frontend redirects)
- **Keycloak Internal URL**: `http://keycloak:8080` (for backend communication)
- **Client ID**: `betting-api`
- **Client Secret**: `dev-client-secret` ✅ **FIXED**
- **Realm**: `betting-platform`
- **Test Users**: `admin/admin123`, `testuser/test123`, `moderator/mod123`

## 🏁 Integration Status

### ✅ Completed
- OAuth 2.0 Authorization Code Flow implementation
- Manual HTTP requests to bypass library issues
- Token validation using Keycloak public keys
- User synchronization between Keycloak and local database
- Environment configuration for dual URL setup
- Security middleware integration
- All endpoints functional and accessible

### 🔄 Ready for Frontend Integration
- Authorization URL generation works
- Token exchange endpoint ready
- User info endpoint secured
- Refresh token flow implemented
- Logout functionality complete

## 🚀 Next Steps for Frontend

1. Implement Angular OAuth service using these endpoints
2. Add redirect handling for `/auth/callback`
3. Store tokens securely (HttpOnly cookies recommended)
4. Add authentication guards for protected routes
5. Implement automatic token refresh logic

## 🛠 Development Notes

- Used direct HTTP requests instead of python-keycloak library
- Bypassed AsyncClient initialization issues
- Manual token validation using public key cryptography
- Backward compatibility with existing JWT authentication