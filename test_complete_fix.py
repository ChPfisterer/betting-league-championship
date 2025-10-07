#!/usr/bin/env python3
"""
Direct test of the authentication fix
"""

import sys
import os
sys.path.append('/Users/chp/repos/GitHub/betting-league-championship/backend/src')

def test_user_sync_simulation():
    """Test the user synchronization with mock Keycloak data"""
    print("🔧 Testing User Synchronization with Mock Keycloak Data")
    
    try:
        from services.keycloak_service import KeycloakService
        from core.database import SessionLocal
        from models.user import User
        
        # Create mock token info (simulating what Keycloak would return)
        mock_token_info = {
            "sub": "keycloak-user-123",
            "preferred_username": "testuser",
            "email": "testuser@example.com",
            "given_name": "Test",
            "family_name": "User",
            "realm_access": {
                "roles": ["user"]
            }
        }
        
        print(f"📝 Mock token data: {mock_token_info}")
        
        # Test sync function
        keycloak_service = KeycloakService()
        
        try:
            user = keycloak_service.sync_user_with_keycloak(mock_token_info)
            print(f"✅ User sync successful!")
            print(f"👤 User ID: {user.id}")
            print(f"🔑 Keycloak ID: {user.keycloak_id}")
            print(f"📧 Email: {user.email}")
            print(f"👋 Name: {user.first_name} {user.last_name}")
            return True
            
        except Exception as sync_error:
            print(f"❌ User sync failed: {sync_error}")
            return False
            
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        return False

def test_authentication_endpoints():
    """Test authentication endpoints directly"""
    print("\n🔧 Testing Authentication Endpoints")
    
    import requests
    
    try:
        # Test 1: Authorization URL
        response = requests.get("http://localhost:8000/api/v1/auth/keycloak/oauth/authorize-url", 
                              params={"redirect_uri": "http://localhost:4200/auth/callback"})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Authorization URL endpoint working")
            state = data["state"]
        else:
            print(f"❌ Authorization URL failed: {response.text}")
            return False
        
        # Test 2: Health check
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print(f"✅ Backend health check passed")
        else:
            print(f"❌ Backend health check failed")
            return False
        
        # Test 3: Matches endpoint (should work without auth)
        response = requests.get("http://localhost:8000/api/v1/matches/")
        if response.status_code == 200:
            matches = response.json()
            print(f"✅ Matches endpoint working ({len(matches)} matches)")
        else:
            print(f"❌ Matches endpoint failed: {response.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        return False

def test_database_integrity():
    """Test database structure is correct"""
    print("\n🔧 Testing Database Integrity")
    
    try:
        from core.database import engine
        from sqlalchemy import text
        from models.user import User
        
        with engine.connect() as conn:
            # Check users table exists
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_name='users'"))
            if not result.fetchone():
                print("❌ Users table doesn't exist")
                return False
            print("✅ Users table exists")
            
            # Check keycloak_id column
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='keycloak_id'
            """))
            keycloak_col = result.fetchone()
            if keycloak_col:
                print(f"✅ keycloak_id column: {keycloak_col}")
            else:
                print("❌ keycloak_id column missing")
                return False
            
            # Test that we can create a user with keycloak_id
            try:
                from sqlalchemy.orm import Session
                db = Session(engine)
                
                # Check if test user already exists
                existing = db.query(User).filter(User.username == "test_keycloak_user").first()
                if existing:
                    db.delete(existing)
                    db.commit()
                
                # Create test user with keycloak_id
                test_user = User(
                    username="test_keycloak_user",
                    email="test_keycloak@example.com", 
                    password_hash="dummy_hash",
                    first_name="Test",
                    last_name="User",
                    keycloak_id="test-keycloak-123",
                    is_active=True
                )
                
                db.add(test_user)
                db.commit()
                
                # Verify it was created
                created_user = db.query(User).filter(User.keycloak_id == "test-keycloak-123").first()
                if created_user:
                    print(f"✅ User creation with keycloak_id successful")
                    print(f"   ID: {created_user.id}")
                    print(f"   Keycloak ID: {created_user.keycloak_id}")
                    
                    # Clean up
                    db.delete(created_user)
                    db.commit()
                else:
                    print("❌ User creation verification failed")
                    return False
                    
                db.close()
                
            except Exception as user_error:
                print(f"❌ User creation test failed: {user_error}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database integrity test failed: {e}")
        return False

def main():
    """Run comprehensive tests"""
    print("🚀 COMPREHENSIVE AUTHENTICATION FIX VERIFICATION")
    print("=" * 60)
    
    tests = [
        ("Database Integrity", test_database_integrity),
        ("Authentication Endpoints", test_authentication_endpoints),  
        ("User Sync Simulation", test_user_sync_simulation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"📊 {test_name}: {'✅ PASSED' if result else '❌ FAILED'}")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Final summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n{'='*60}")
    print(f"📊 FINAL RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL" 
        print(f"{status} {test_name}")
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! The authentication fix is working!")
        print(f"\n✅ What's been fixed:")
        print(f"   • Database has keycloak_id field")
        print(f"   • User model supports Keycloak integration") 
        print(f"   • Authentication endpoints are working")
        print(f"   • User synchronization logic works")
        print(f"\n💡 Next steps:")
        print(f"   • Start frontend: cd frontend/betting-league-app && npm start")
        print(f"   • Open http://localhost:4200")
        print(f"   • Try to place a prediction")
        print(f"   • You should be redirected to Keycloak login")
        print(f"   • After login, prediction should work without errors")
    else:
        print(f"\n❌ Some issues remain - check failed tests above")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)