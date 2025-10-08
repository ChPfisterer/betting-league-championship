#!/usr/bin/env python3
"""
Direct test of the Keycloak user sync fix
"""

import sys
import os
sys.path.insert(0, '/Users/chp/repos/GitHub/betting-league-championship/backend/src')

from datetime import datetime, timezone
from services.keycloak_service import KeycloakService

def test_user_sync_with_missing_email():
    """Test user sync when token is missing email field"""
    print("🔧 Testing user sync with missing email...")
    
    # Simulate token data that's missing email (common with some OAuth providers)
    token_info_missing_email = {
        'sub': 'test-keycloak-id-123',
        'preferred_username': 'testuser_no_email',
        'email': None,  # This is the key issue we're fixing
        'given_name': None,
        'family_name': None,
        'realm_access': {'roles': ['default-roles-betting-platform']}
    }
    
    print("Token data (missing email):")
    print(f"  - sub: {token_info_missing_email['sub']}")
    print(f"  - username: {token_info_missing_email['preferred_username']}")
    print(f"  - email: {token_info_missing_email['email']}")
    print(f"  - given_name: {token_info_missing_email['given_name']}")
    print(f"  - family_name: {token_info_missing_email['family_name']}")
    
    try:
        service = KeycloakService()
        user = service.sync_user_with_keycloak(token_info_missing_email)
        
        print("✅ User creation succeeded!")
        print(f"  - Username: {user.username}")
        print(f"  - Email: {user.email}")
        print(f"  - First name: {user.first_name}")
        print(f"  - Last name: {user.last_name}")
        print(f"  - Display name: {user.display_name}")
        print(f"  - Keycloak ID: {user.keycloak_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_sync_with_empty_names():
    """Test user sync when token has empty names"""
    print("\n🔧 Testing user sync with empty names...")
    
    token_info_empty_names = {
        'sub': 'test-keycloak-id-456',
        'preferred_username': 'testuser_empty_names',
        'email': 'test@example.com',  # Email provided this time
        'given_name': '',  # Empty string
        'family_name': '',  # Empty string
        'realm_access': {'roles': ['default-roles-betting-platform']}
    }
    
    print("Token data (empty names):")
    print(f"  - username: {token_info_empty_names['preferred_username']}")
    print(f"  - email: {token_info_empty_names['email']}")
    print(f"  - given_name: '{token_info_empty_names['given_name']}'")
    print(f"  - family_name: '{token_info_empty_names['family_name']}'")
    
    try:
        service = KeycloakService()
        user = service.sync_user_with_keycloak(token_info_empty_names)
        
        print("✅ User creation succeeded!")
        print(f"  - Username: {user.username}")
        print(f"  - Email: {user.email}")
        print(f"  - First name: '{user.first_name}'")
        print(f"  - Last name: '{user.last_name}'")
        print(f"  - Display name: '{user.display_name}'")
        
        return True
        
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Keycloak User Sync Fixes")
    print("=" * 50)
    
    # Test 1: Missing email field
    success1 = test_user_sync_with_missing_email()
    
    # Test 2: Empty name fields
    success2 = test_user_sync_with_empty_names()
    
    print("\n📊 Test Results:")
    print(f"  Missing email test: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"  Empty names test: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! The authentication fix is working correctly.")
    else:
        print("\n⚠️  Some tests failed. The fix may need additional work.")