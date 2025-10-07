#!/usr/bin/env python3
"""
Test script for complete authentication and prediction flow
"""

import requests
import json
import sys
from urllib.parse import urlparse, parse_qs

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:4200"

def test_step_1_get_auth_url():
    """Step 1: Get Keycloak authorization URL"""
    print("🔧 Step 1: Getting Keycloak authorization URL...")
    
    response = requests.get(f"{BASE_URL}/api/v1/auth/keycloak/oauth/authorize-url", params={
        "redirect_uri": f"{FRONTEND_URL}/auth/callback"
    })
    
    if response.status_code != 200:
        print(f"❌ Failed to get auth URL: {response.text}")
        return None, None
    
    data = response.json()
    auth_url = data["authorize_url"]
    state = data["state"]
    
    print(f"✅ Authorization URL generated")
    print(f"🔗 URL: {auth_url}")
    print(f"🔑 State: {state}")
    
    return auth_url, state

def test_step_2_manual_login(auth_url):
    """Step 2: Manual login instructions"""
    print(f"\n🔧 Step 2: Manual Keycloak Login Required")
    print("=" * 50)
    print(f"1. Open this URL in your browser:")
    print(f"   {auth_url}")
    print(f"2. Login with username: testuser, password: testpass")
    print(f"3. After login, you'll be redirected to a localhost URL")
    print(f"4. Copy the 'code' parameter from the URL")
    print(f"5. Paste the code below:")
    
    code = input("\nEnter the authorization code: ").strip()
    return code if code else None

def test_step_3_exchange_token(code, state):
    """Step 3: Exchange code for token"""
    print(f"\n🔧 Step 3: Exchanging authorization code for token...")
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/keycloak/oauth/token", json={
        "code": code,
        "redirect_uri": f"{FRONTEND_URL}/auth/callback",
        "state": state
    })
    
    if response.status_code != 200:
        print(f"❌ Token exchange failed: {response.text}")
        return None
    
    token_data = response.json()
    print(f"✅ Token exchange successful!")
    print(f"🎫 Access token: {token_data['access_token'][:50]}...")
    print(f"👤 User ID: {token_data['user_id']}")
    print(f"📧 Username: {token_data['username']}")
    
    return token_data

def test_step_4_test_prediction(access_token):
    """Step 4: Test prediction submission"""
    print(f"\n🔧 Step 4: Testing prediction submission...")
    
    # First, get a match to bet on
    matches_response = requests.get(f"{BASE_URL}/api/v1/matches/")
    if matches_response.status_code != 200:
        print(f"❌ Failed to get matches: {matches_response.text}")
        return False
    
    matches = matches_response.json()
    if not matches:
        print("❌ No matches available for testing")
        return False
    
    # Use the first match
    match = matches[0]
    match_id = match["id"]
    print(f"🏆 Using match: {match['home_team']['name']} vs {match['away_team']['name']}")
    
    # Submit prediction
    prediction_data = {
        "match_id": match_id,
        "bet_type": "single",
        "predicted_outcome": "home",
        "amount": 50.0,
        "odds": 2.5,
        "potential_payout": 125.0
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/bets/", json=prediction_data, headers=headers)
    
    if response.status_code == 201:
        bet_data = response.json()
        print(f"✅ Prediction submitted successfully!")
        print(f"🎯 Bet ID: {bet_data['id']}")
        print(f"💰 Amount: {bet_data['amount']}")
        print(f"📈 Odds: {bet_data['odds']}")
        print(f"🎰 Potential Payout: {bet_data['potential_payout']}")
        return True
    else:
        print(f"❌ Prediction submission failed: {response.text}")
        return False

def test_step_5_verify_user_sync(access_token):
    """Step 5: Verify user was synced correctly"""
    print(f"\n🔧 Step 5: Verifying user synchronization...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Get user info
    response = requests.get(f"{BASE_URL}/api/v1/auth/keycloak/user/info", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to get user info: {response.text}")
        return False
    
    user_info = response.json()
    print(f"✅ User synchronized successfully!")
    print(f"👤 User ID: {user_info['id']}")
    print(f"📧 Email: {user_info['email']}")
    print(f"🔑 Keycloak ID: {user_info.get('keycloak_id', 'NOT SET')}")
    
    return True

def main():
    """Main test flow"""
    print("🚀 Testing Complete Authentication & Prediction Flow")
    print("=" * 60)
    
    try:
        # Step 1: Get auth URL
        auth_url, state = test_step_1_get_auth_url()
        if not auth_url:
            return False
        
        # Step 2: Manual login
        code = test_step_2_manual_login(auth_url)
        if not code:
            print("❌ No authorization code provided")
            return False
        
        # Step 3: Exchange for token
        token_data = test_step_3_exchange_token(code, state)
        if not token_data:
            return False
        
        # Step 4: Test prediction
        prediction_success = test_step_4_test_prediction(token_data['access_token'])
        
        # Step 5: Verify user sync
        user_sync_success = test_step_5_verify_user_sync(token_data['access_token'])
        
        # Final result
        if prediction_success and user_sync_success:
            print(f"\n🎉 ALL TESTS PASSED!")
            print(f"✅ Authentication: Working")
            print(f"✅ User Sync: Working")
            print(f"✅ Prediction Submission: Working")
            print(f"✅ Keycloak Integration: Working")
            return True
        else:
            print(f"\n❌ Some tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)