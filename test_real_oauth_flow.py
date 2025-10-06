#!/usr/bin/env python3
"""
Real OAuth 2.0 Flow Test with Backend Callback

This script demonstrates the complete OAuth flow using the backend callback endpoint.
"""

import requests
import webbrowser
import json

def test_real_oauth_flow():
    """Test the complete OAuth flow with real user login"""
    print("🚀 Testing REAL OAuth 2.0 Flow with Backend Callback")
    print("=" * 60)
    
    # Step 1: Get authorization URL
    print("\n🔧 Step 1: Getting authorization URL...")
    response = requests.get("http://localhost:8000/api/v1/auth/keycloak/oauth/authorize-url", params={
        "redirect_uri": "http://localhost:8000/auth/callback"
    })
    
    if response.status_code != 200:
        print(f"❌ Error getting authorization URL: {response.text}")
        return False
    
    data = response.json()
    auth_url = data['authorize_url']
    state = data['state']
    
    print(f"✅ Authorization URL generated")
    print(f"✅ State: {state}")
    
    # Step 2: Open browser for login
    print(f"\n🔧 Step 2: Opening browser for login...")
    print(f"📝 URL: {auth_url}")
    print(f"\n🔐 Login with one of these test users:")
    print(f"   • admin / admin123")
    print(f"   • testuser / test123")
    print(f"   • moderator / mod123")
    print(f"\n📋 After login, you'll see a page with:")
    print(f"   • Authorization code")
    print(f"   • Copy button to get the code")
    print(f"   • Ready-to-use curl command")
    
    try:
        webbrowser.open(auth_url)
        print("✅ Browser opened automatically")
    except:
        print("⚠️  Could not open browser automatically")
        print(f"Please manually open: {auth_url}")
    
    print(f"\n⏳ Waiting for you to complete login...")
    print(f"💡 Once you see the callback page, copy the authorization code and paste it here.")
    
    # Wait for user to complete login
    auth_code = input("\n📋 Enter the authorization code from the callback page: ").strip()
    
    if not auth_code:
        print("❌ No authorization code provided")
        return False
    
    # Step 3: Exchange code for tokens
    print(f"\n🔧 Step 3: Exchanging authorization code for tokens...")
    token_response = requests.post("http://localhost:8000/api/v1/auth/keycloak/oauth/token", json={
        "code": auth_code,
        "redirect_uri": "http://localhost:8000/auth/callback",
        "state": state
    })
    
    if token_response.status_code != 200:
        print(f"❌ Token exchange failed: {token_response.text}")
        return False
    
    tokens = token_response.json()
    print("✅ Token exchange successful!")
    print(f"✅ Access Token: {tokens['access_token'][:50]}...")
    print(f"✅ Refresh Token: {tokens['refresh_token'][:50]}...")
    print(f"✅ Expires in: {tokens['expires_in']} seconds")
    
    # Step 4: Test user info
    print(f"\n🔧 Step 4: Getting user information...")
    user_response = requests.get("http://localhost:8000/api/v1/auth/keycloak/user/info", headers={
        "Authorization": f"Bearer {tokens['access_token']}"
    })
    
    if user_response.status_code != 200:
        print(f"❌ User info failed: {user_response.text}")
        return False
    
    user_info = user_response.json()
    print("✅ User info retrieved successfully!")
    print(f"✅ User: {json.dumps(user_info, indent=2)}")
    
    # Step 5: Test token refresh
    print(f"\n🔧 Step 5: Testing token refresh...")
    refresh_response = requests.post("http://localhost:8000/api/v1/auth/keycloak/oauth/refresh", json={
        "refresh_token": tokens['refresh_token']
    })
    
    if refresh_response.status_code != 200:
        print(f"❌ Token refresh failed: {refresh_response.text}")
        return False
    
    new_tokens = refresh_response.json()
    print("✅ Token refresh successful!")
    print(f"✅ New Access Token: {new_tokens['access_token'][:50]}...")
    
    # Step 6: Test logout
    print(f"\n🔧 Step 6: Testing logout...")
    logout_response = requests.post("http://localhost:8000/api/v1/auth/keycloak/oauth/logout", json={
        "refresh_token": tokens['refresh_token']
    })
    
    if logout_response.status_code != 200:
        print(f"❌ Logout failed: {logout_response.text}")
        return False
    
    print("✅ Logout successful!")
    
    print("\n" + "=" * 60)
    print("🎉 COMPLETE OAUTH 2.0 FLOW TEST SUCCESSFUL!")
    print("✅ All OAuth endpoints working with real user authentication")
    print("✅ Token exchange, validation, refresh, and logout all functional")
    print("✅ Ready for frontend integration!")
    
    return True

if __name__ == "__main__":
    test_real_oauth_flow()