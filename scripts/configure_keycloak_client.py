#!/usr/bin/env python3
"""
Configure Keycloak client for OAuth 2.0 Authorization Code Flow
This script fixes the client configuration issues found during testing.
"""

import requests
import json
import sys

KEYCLOAK_URL = "http://localhost:8090"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
REALM = "betting-platform"
CLIENT_ID = "betting-api"
CLIENT_SECRET = "betting-api-secret"

def get_admin_token():
    """Get admin access token"""
    url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Failed to get admin token: {response.text}")
        return None

def configure_client(admin_token):
    """Configure the betting-api client properly"""
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    # First, get the client
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to get clients: {response.text}")
        return False
    
    clients = response.json()
    client_uuid = None
    
    for client in clients:
        if client["clientId"] == CLIENT_ID:
            client_uuid = client["id"]
            break
    
    if not client_uuid:
        print(f"Client {CLIENT_ID} not found!")
        return False
    
    print(f"Found client {CLIENT_ID} with UUID: {client_uuid}")
    
    # Configure the client
    client_config = {
        "clientId": CLIENT_ID,
        "enabled": True,
        "clientAuthenticatorType": "client-secret",
        "secret": CLIENT_SECRET,
        "standardFlowEnabled": True,  # Authorization Code Flow
        "directAccessGrantsEnabled": True,  # Direct Grant
        "serviceAccountsEnabled": True,  # Client Credentials
        "publicClient": False,  # Confidential client
        "protocol": "openid-connect",
        "redirectUris": [
            "http://localhost:4200/*",
            "http://localhost:3000/*"
        ],
        "webOrigins": [
            "http://localhost:4200",
            "http://localhost:3000"
        ],
        "attributes": {
            "access.token.lifespan": "3600",
            "client.secret.creation.time": "1696636800"
        }
    }
    
    # Update the client
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients/{client_uuid}"
    response = requests.put(url, headers=headers, json=client_config)
    
    if response.status_code in [200, 204]:
        print("✅ Client configuration updated successfully!")
        return True
    else:
        print(f"Failed to update client: {response.text}")
        return False

def test_client_credentials(admin_token):
    """Test the client credentials after configuration"""
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ Client credentials test: SUCCESS")
        token_data = response.json()
        print(f"   Access token received (expires in {token_data.get('expires_in')} seconds)")
        return True
    else:
        print(f"❌ Client credentials test: FAILED - {response.text}")
        return False

def main():
    print("🔧 Configuring Keycloak client for OAuth 2.0...")
    
    # Get admin token
    admin_token = get_admin_token()
    if not admin_token:
        sys.exit(1)
    
    print("✅ Admin token obtained")
    
    # Configure client
    if not configure_client(admin_token):
        sys.exit(1)
    
    # Test client credentials
    if not test_client_credentials(admin_token):
        sys.exit(1)
    
    print("\n🎉 Keycloak client configuration complete!")
    print("OAuth 2.0 Authorization Code Flow is now ready for testing.")

if __name__ == "__main__":
    main()