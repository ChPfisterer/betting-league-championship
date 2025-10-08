#!/usr/bin/env python3
"""
Test script to verify the authentication fix for missing email issue.
"""

import requests
import json
import time
from urllib.parse import urlparse, parse_qs

def get_keycloak_token():
    """Get a token directly from Keycloak for testing."""
    # Step 1: Get access token using admin console credentials  
    token_url = "http://localhost:8090/realms/betting-platform/protocol/openid-connect/token"
    
    # Create or use existing test user
    data = {
        'grant_type': 'password',
        'client_id': 'betting-api',
        'username': 'testuser',
        'password': 'testpass123',
        'scope': 'openid profile email'
    }
    
    print("Requesting token from Keycloak...")
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get('access_token')
    else:
        print(f"Failed to get token: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_backend_api(token):
    """Test the backend API with the token."""
    if not token:
        print("No token available for testing")
        return
        
    print(f"\nTesting backend API with token...")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test the /users/me endpoint
    api_url = "http://localhost:8000/api/v1/users/me"
    response = requests.get(api_url, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Authentication flow working correctly!")
        user_data = response.json()
        print(f"User: {user_data.get('username')} (email: {user_data.get('email')})")
    elif response.status_code == 500:
        print("❌ Still getting 500 error - authentication flow not fixed")
    elif response.status_code == 401:
        print("❌ Token authentication failed")
    else:
        print(f"❌ Unexpected response code: {response.status_code}")

def decode_token(token):
    """Decode token to see its contents (for debugging)."""
    import base64
    import json
    
    try:
        # Split token parts
        parts = token.split('.')
        if len(parts) != 3:
            print("Invalid JWT token format")
            return
            
        # Decode payload (add padding if needed)
        payload = parts[1]
        missing_padding = len(payload) % 4
        if missing_padding:
            payload += '=' * (4 - missing_padding)
            
        decoded_payload = base64.urlsafe_b64decode(payload)
        token_data = json.loads(decoded_payload.decode('utf-8'))
        
        print("\nToken payload:")
        print(json.dumps(token_data, indent=2))
        
        # Check for email field
        email = token_data.get('email')
        if email:
            print(f"✅ Token contains email: {email}")
        else:
            print("⚠️  Token missing email field - testing our fix")
            
    except Exception as e:
        print(f"Error decoding token: {e}")

if __name__ == "__main__":
    print("🔧 Testing authentication fix for missing email...")
    
    # Get token from Keycloak
    token = get_keycloak_token()
    
    if token:
        print("✅ Got token from Keycloak")
        decode_token(token)
        test_backend_api(token)
    else:
        print("❌ Failed to get token from Keycloak")
        print("Make sure testuser exists in Keycloak or check credentials")