#!/usr/bin/env python3
"""
Keycloak OAuth 2.0 Integration Test Script

This script demonstrates the complete OAuth flow integration
and can be used for automated testing.
"""

import requests
import json
import webbrowser
from urllib.parse import urlparse, parse_qs


class KeycloakOAuthTester:
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1/auth/keycloak"
        self.redirect_uri = "http://localhost:4200/auth/callback"
        
    def step1_get_authorization_url(self):
        """Step 1: Get authorization URL from our API"""
        print("🔧 Step 1: Getting authorization URL...")
        
        response = requests.get(f"{self.base_url}/oauth/authorize-url", params={
            "redirect_uri": self.redirect_uri
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Authorization URL: {data['authorize_url']}")
            print(f"✅ State: {data['state']}")
            return data['authorize_url'], data['state']
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None, None
    
    def step2_manual_login_instructions(self, auth_url):
        """Step 2: Instructions for manual login"""
        print("\n🔧 Step 2: Manual Login Required")
        print("Please follow these steps:")
        print(f"1. Open this URL in your browser: {auth_url}")
        print("2. Login with your Keycloak credentials")
        print("3. After login, you'll be redirected to a URL like:")
        print(f"   {self.redirect_uri}?code=SOME_CODE&state=SOME_STATE")
        print("4. Copy the 'code' parameter from the redirected URL")
        
        # Optionally open browser automatically
        try:
            webbrowser.open(auth_url)
            print("✅ Browser opened automatically")
        except:
            print("⚠️  Could not open browser automatically")
        
        return input("\nEnter the authorization code from the redirect URL: ").strip()
    
    def step3_exchange_code_for_token(self, code, state):
        """Step 3: Exchange authorization code for tokens"""
        print(f"\n🔧 Step 3: Exchanging code for tokens...")
        
        response = requests.post(f"{self.base_url}/oauth/token", json={
            "code": code,
            "redirect_uri": self.redirect_uri,
            "state": state
        })
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Token exchange successful!")
            print(f"✅ Access Token: {data['access_token'][:50]}...")
            print(f"✅ Refresh Token: {data['refresh_token'][:50]}...")
            print(f"✅ Expires in: {data['expires_in']} seconds")
            return data
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
    
    def step4_test_user_info(self, access_token):
        """Step 4: Test user info endpoint"""
        print(f"\n🔧 Step 4: Testing user info endpoint...")
        
        response = requests.get(f"{self.base_url}/user/info", headers={
            "Authorization": f"Bearer {access_token}"
        })
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User info retrieved successfully!")
            print(f"✅ User: {json.dumps(data, indent=2)}")
            return data
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
    
    def step5_test_token_refresh(self, refresh_token):
        """Step 5: Test token refresh"""
        print(f"\n🔧 Step 5: Testing token refresh...")
        
        response = requests.post(f"{self.base_url}/oauth/refresh", json={
            "refresh_token": refresh_token
        })
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Token refresh successful!")
            print(f"✅ New Access Token: {data['access_token'][:50]}...")
            return data
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
    
    def step6_test_logout(self, refresh_token):
        """Step 6: Test logout"""
        print(f"\n🔧 Step 6: Testing logout...")
        
        response = requests.post(f"{self.base_url}/oauth/logout", json={
            "refresh_token": refresh_token
        })
        
        if response.status_code == 200:
            print("✅ Logout successful!")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    
    def run_complete_flow(self):
        """Run the complete OAuth flow test"""
        print("🚀 Starting Keycloak OAuth 2.0 Integration Test")
        print("=" * 50)
        
        # Step 1: Get authorization URL
        auth_url, state = self.step1_get_authorization_url()
        if not auth_url:
            return False
        
        # Step 2: Manual login
        code = self.step2_manual_login_instructions(auth_url)
        if not code:
            print("❌ No authorization code provided")
            return False
        
        # Step 3: Exchange code for token
        token_data = self.step3_exchange_code_for_token(code, state)
        if not token_data:
            return False
        
        # Step 4: Test user info
        user_info = self.step4_test_user_info(token_data['access_token'])
        if not user_info:
            return False
        
        # Step 5: Test token refresh
        new_token_data = self.step5_test_token_refresh(token_data['refresh_token'])
        if not new_token_data:
            return False
        
        # Step 6: Test logout
        logout_success = self.step6_test_logout(token_data['refresh_token'])
        
        print("\n" + "=" * 50)
        if logout_success:
            print("🎉 Complete OAuth flow test SUCCESSFUL!")
        else:
            print("⚠️  OAuth flow test completed with logout issues")
        
        return logout_success


if __name__ == "__main__":
    tester = KeycloakOAuthTester()
    tester.run_complete_flow()