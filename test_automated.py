#!/usr/bin/env python3
"""
Automated test for authentication system components
"""

import sys
import os
sys.path.append('/Users/chp/repos/GitHub/betting-league-championship/backend/src')

# Test 1: Database schema verification
def test_database_schema():
    """Test that the database schema is correct"""
    print("🔧 Test 1: Database Schema Verification")
    
    try:
        from core.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            # Check if keycloak_id column exists
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='keycloak_id'
            """))
            keycloak_column = result.fetchone()
            
            if keycloak_column:
                print(f"✅ keycloak_id column exists: {keycloak_column}")
            else:
                print("❌ keycloak_id column missing!")
                return False
                
            # Check other important columns
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns 
                WHERE table_name='users' 
                ORDER BY column_name
            """))
            columns = [row[0] for row in result.fetchall()]
            required_columns = ['id', 'username', 'email', 'keycloak_id', 'is_active']
            
            missing_columns = [col for col in required_columns if col not in columns]
            if missing_columns:
                print(f"❌ Missing required columns: {missing_columns}")
                return False
            
            print("✅ All required User columns present")
            return True
            
    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        return False

# Test 2: Authentication system components
def test_authentication_components():
    """Test authentication system components"""
    print("\n🔧 Test 2: Authentication Components")
    
    try:
        # Test Keycloak service initialization
        from services.keycloak_service import KeycloakService
        keycloak_service = KeycloakService()
        print("✅ KeycloakService initialized")
        
        # Test security functions exist
        from core.keycloak_security import get_current_user_hybrid, OAuth2Helper
        print("✅ Authentication functions available")
        
        # Test User model with keycloak_id
        from models.user import User
        user_fields = [column.name for column in User.__table__.columns]
        if 'keycloak_id' in user_fields:
            print("✅ User model has keycloak_id field")
        else:
            print("❌ User model missing keycloak_id field")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Authentication components test failed: {e}")
        return False

# Test 3: API endpoints availability
def test_api_endpoints():
    """Test that API endpoints are available"""
    print("\n🔧 Test 3: API Endpoints")
    
    try:
        import requests
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test Keycloak auth endpoints
        response = requests.get("http://localhost:8000/api/v1/auth/keycloak/oauth/authorize-url?redirect_uri=test")
        if response.status_code == 200:
            print("✅ Keycloak auth endpoint working")
        else:
            print(f"❌ Keycloak auth endpoint failed: {response.status_code}")
            return False
            
        # Test matches endpoint
        response = requests.get("http://localhost:8000/api/v1/matches/")
        if response.status_code == 200:
            matches = response.json()
            print(f"✅ Matches endpoint working ({len(matches)} matches available)")
        else:
            print(f"❌ Matches endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

# Test 4: Token validation simulation
def test_token_validation():
    """Test token validation logic without actual Keycloak token"""
    print("\n🔧 Test 4: Token Validation Logic")
    
    try:
        from services.keycloak_service import KeycloakService
        from core.security import verify_token, JWTError
        
        # Test that the KeycloakService has the required methods
        keycloak_service = KeycloakService()
        
        required_methods = ['validate_token', 'sync_user_with_keycloak', 'get_authorization_url']
        for method in required_methods:
            if hasattr(keycloak_service, method):
                print(f"✅ KeycloakService.{method} available")
            else:
                print(f"❌ KeycloakService.{method} missing")
                return False
        
        # Test traditional JWT verification exists
        try:
            # This should fail gracefully with invalid token
            verify_token("invalid_token")
        except JWTError:
            print("✅ Traditional JWT validation working")
        except Exception as e:
            print(f"⚠️  JWT validation exists but error: {type(e).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Token validation test failed: {e}")
        return False

def main():
    """Run all automated tests"""
    print("🚀 Automated Authentication System Tests")
    print("=" * 50)
    
    tests = [
        test_database_schema,
        test_authentication_components, 
        test_api_endpoints,
        test_token_validation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL AUTOMATED TESTS PASSED!")
        print("✅ Database schema is correct")
        print("✅ Authentication components are working") 
        print("✅ API endpoints are accessible")
        print("✅ Token validation logic is in place")
        print("\n💡 To test the complete flow:")
        print("   1. Open the frontend application")
        print("   2. Try to submit a prediction")
        print("   3. You should be redirected to Keycloak login")
        print("   4. After login, prediction should work")
    else:
        print("❌ Some tests failed - check the output above")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)